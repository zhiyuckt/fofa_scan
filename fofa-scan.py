import time,os,re,requests,base64,random,sys,xlwt
from bs4 import BeautifulSoup
from urllib.parse import quote
def User_gent():
    agent=[
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36',
      'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0;',
      'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.6; rv,2.0.1) Gecko/20100101 Firefox/4.0.1',
      'Opera/9.80 (Macintosh; Intel Mac OS X 10.6.8; U; en) Presto/2.8.131 Version/11.11',
      'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_0) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.56 Safari/535.11',
      'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; 360SE)',
      'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:58.0) Gecko/20100101 Firefox/58.0'
    ]
    fackender={}
    fackender['user-agent']=agent[random.randint(0,len(agent)-1)]
    fackender['Cookie']="_fofapro_ars_session="+cookie+",result_per_page=2000"
    return (fackender)

def get_result(search):
    tmp_url="https://fofa.so/result?"+"&qbase64="+quote(base64.b64encode(search.encode('utf-8')), 'utf-8')
    res = requests.get(url = tmp_url)
    soup = BeautifulSoup(res.text, 'lxml')
    number = soup.select('#rs')[0].span.string.replace(',','')
    print("[+][+][+] " + "共找到" + number + "个结果 [+][+][+]")
    return number
def setup_ip(url,result,filename,IP,url2,title,code):  #获取网址，并保存到csv文档
    r=requests.get(url=url,headers=User_gent()).text
    time.sleep(5)
    soup=BeautifulSoup(r,'lxml')
    for soup2 in soup.find_all('div',class_='right-list-view-item clearfix'):  #获取域名fl box-sizing
        try:
            result.append(soup2.select('a[target="_blank"]')[0].get('href'))    #保存url到数组result中，为后续方便提取
            title.append(soup2.select('div[class="time"]')[0].string)   #保存title到数组title中，为后续方便提取
            IP.append(soup2.select('a[class="second"]')[0].string)        #保存IP到数组IP中，为后续方便提取
            code.append(soup2.select('div[class="scroll-wrap-res"]')[0].string.split('\r\n')[0].strip())  #保存code到数组code中，为后续方便提取
        except:
            pass

#获取去http协议的域名
    for i in range(0,len(result)):
        pattern=re.compile(r'http[s]?://')   #利用正则匹配前面http和https
        try:
            url1 = re.split(pattern,result[i])[1]  #获取数组1的数据
            url=url1.strip('\n')   #去除换行符
            url2.append(url)
        except:
            url1 = re.split(pattern,result[i])[0] #获取数组1的数据
            url=url1.strip('\n')   #去除换行符
            url2.append(url)

#写入xls文件
    f = xlwt.Workbook()
    write = f.add_sheet(filename,cell_overwrite_ok=True)
    tableTitle = ['Url','Title','Code','Ip','Url2']
    for col in range(len(tableTitle)):
        write.write(0,col,tableTitle[col])
        first=write.col(col)
        first.width=400*20
    j=1
    if j<2:
        for i in range(0,len(result)):
            write.write(j,0,result[i])  #写入Url
            write.write(j,1,title[i])  #写入title
            write.write(j,2,code[i])  #写入IP
            write.write(j,3,IP[i])  #写入url2
            write.write(j,4,url2[i])  #写入url2
            j+=1

    f.save(filename+'.xls')

if __name__=='__main__':
    page_num=0
    if len(sys.argv) < 3:
        print(
                '''python fofa-scan.py 内容 保存的文件名 _fofapro_ars_session\n  Ps: python3 fofa-scan.py domain="baidu.com" baidu 76c903103f3e5495f10fe0550ecfc5d3''')
        exit(0)
    search = sys.argv[1]
    print(search)
    filename = sys.argv[2]
    cookie = sys.argv[3]

    get_number=get_result(search)    #获取到要抓取的数量
    page_num = (int(get_number) // 2000) + 1
    result = []
    IP=[]
    ulr2=[]
    title=[]
    code=[]

    for page in range(1,page_num+1):
        print("[+] 抓取第 %d 页..." % (page))
        setup_ip("https://fofa.so/result?"+"&qbase64="+quote(base64.b64encode(search.encode('utf-8')), 'utf-8')+"&page="+str(page),result,filename,IP,ulr2,title,code)
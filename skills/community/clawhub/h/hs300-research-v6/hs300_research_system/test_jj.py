import io, sys
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
import requests
import re

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36', 'Referer': 'https://data.eastmoney.com/'}

# 获取东方财富数据中心的集合竞价页面
url = 'https://data.eastmoney.com/jj/index.html'
try:
    r = requests.get(url, headers=headers, timeout=10)
    print('status:', r.status_code, 'len:', len(r.text))
    # 查找API相关字符串
    apis = re.findall(r'["\']([^"\']*reportName[^"\']*)["\']', r.text)
    print('reportName patterns:', len(apis))
    for a in apis[:10]:
        print(' ', a[:150])
    
    # 查找所有JS文件
    js_files = re.findall(r'src="([^"]+\.js[^"]*)"', r.text)
    print('JS files:', len(js_files))
    for j in js_files[:10]:
        print(' ', j[:150])
except Exception as e:
    print('err:', e)

print('---')

# 尝试获取集合竞价页面的JS文件
js_url = 'https://data.eastmoney.com/jj/js/jjlist.js'
try:
    r2 = requests.get(js_url, headers=headers, timeout=10)
    print('jjlist.js status:', r2.status_code, 'len:', len(r2.text))
    if r2.status_code == 200:
        apis2 = re.findall(r'["\']([^"\']*reportName[^"\']*)["\']', r2.text)
        print('reportName in js:', len(apis2))
        for a in apis2[:10]:
            print(' ', a[:150])
except Exception as e:
    print('js err:', e)

print('---')

# 尝试数据中心API - 使用已知的报告名
base = 'https://datacenter-web.eastmoney.com/api/data/v1/get'
# 尝试量比排行
test_reports = [
    'RPT_LB_LIST',
    'RPT_AMOUNT_RATIO',
    'RPT_VOL_RATIO',
    'RPT_MARKET_AUK',
    'RPT_AUK',
    'RPT_AUCTION_DATA',
    'RPT_CALL_AUCTION',
    'RPT_JJJJ_DATA',
    'RPT_JHJJ',
    'RPT_MARKET_TRADE',
    'RPT_AUK_STOCK',
    'RPT_AUCTION_STOCK',
    'RPT_DAILYBILLBOARD_DETAILSNEW',  # 这个已知可用
]

for name in test_reports:
    url3 = base + '?reportName=' + name + '&columns=ALL&filter=&pageNumber=1&pageSize=5'
    try:
        r3 = requests.get(url3, headers=headers, timeout=10)
        if r3.status_code == 200:
            data = r3.json()
            result = data.get('result', {})
            if result:
                data_list = result.get('data', [])
                if data_list:
                    print('%s: OK, %d records, columns: %s' % (name, len(data_list), list(data_list[0].keys())[:10]))
                else:
                    print('%s: OK, empty (pages=%s)' % (name, result.get('pages')))
            else:
                print('%s: no result' % name)
    except Exception as e:
        print('%s: err=%s' % (name, e))

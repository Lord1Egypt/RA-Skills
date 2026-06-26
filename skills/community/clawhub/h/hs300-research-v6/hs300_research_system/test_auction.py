import io, sys
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
import requests
import json

headers = {'User-Agent': 'Mozilla/5.0', 'Referer': 'https://data.eastmoney.com/'}

# 尝试东方财富数据中心的市场行情报告
reports = [
    # 实时行情
    'RPT_REALTIME_DATA',
    'RPT_TRADE_DATA',
    'RPT_MARKET_TRADE',
    # 量比排行
    'RPT_LB_LIST',
    'RPT_LB_DATA',
    'RPT_VOL_RATIO',
    'RPT_AMOUNT_RATIO',
    # 换手率
    'RPT_HSL_LIST',
    'RPT_TURNOVER',
    # 竞价相关
    'RPT_CALL_AUCTION_DATA',
    'RPT_JHJJ_DATA',
    'RPT_JHJJ',
    'RPT_PRE_AUCTION',
    'RPT_MORNING_AUCTION',
    'RPT_925_AUCTION',
    'RPT_AUCTION_STOCK',
    'RPT_AUCTION_LIST',
    'RPT_JJJJ_STOCK',
    'RPT_AUK_VOL',
    'RPT_VOL_AUCTION',
    'RPT_AUCTION_VOL',
]

base = 'https://datacenter-web.eastmoney.com/api/data/v1/get'
for name in reports:
    url = base + '?reportName=' + name + '&columns=ALL&filter=&pageNumber=1&pageSize=5'
    try:
        r = requests.get(url, headers=headers, timeout=10)
        if r.status_code == 200 and len(r.text) > 50:
            data = r.json()
            result = data.get('result', {}) if isinstance(data, dict) else None
            if result:
                data_list = result.get('data', [])
                if data_list:
                    print('%s: OK, %d records' % (name, len(data_list)))
                    print('  columns:', list(data_list[0].keys())[:10])
                    print('  first:', json.dumps(data_list[0], ensure_ascii=False)[:200])
                else:
                    print('%s: OK, empty data, pages=%s, count=%s' % (name, result.get('pages'), result.get('count')))
            else:
                print('%s: no result' % name)
        else:
            print('%s: status=%d, len=%d' % (name, r.status_code, len(r.text)))
    except Exception as e:
        print('%s: err=%s' % (name, e))

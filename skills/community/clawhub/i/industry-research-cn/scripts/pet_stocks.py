import requests, json

# 搜索宠物食品相关A股个股
# 数据源：东方财富

def search_pet_stocks():
    url = 'https://push2.eastmoney.com/api/qt/clist/get?pn=1&pz=50&po=1&np=1&fltt=2&invt=2&fid=f3&fs=m%3A90+t%3A2+f%3A!50&fields=f12%2Cf14%2Cf3%2Cf62'
    r = requests.get(url, timeout=10, headers={'User-Agent': 'Mozilla/5.0', 'Referer': 'https://quote.eastmoney.com/'})
    data = r.json()
    stocks = data['data']['diff']

    pet_names = ['乖宝', '中宠', '佩蒂', '源飞', '天元', '依依', '朝云', '益方', '华亨', '宠物']
    results = []
    for s in stocks:
        name = s.get('f14', '')
        code = s.get('f12', '')
        for kw in pet_names:
            if kw in name:
                chg = s.get('f3', 0)
                results.append((name, code, chg))
                break

    return results


def get_realtime(code):
    """获取个股实时价格"""
    market = '1' if code.startswith('6') else '0'
    url = f'https://qt.gtimg.cn/q=sz{code}'
    r = requests.get(url, timeout=5)
    import sys
    sys.stdout.reconfigure(encoding='utf-8')
    fields = r.text.split('~')
    try:
        name = fields[1]
        price = fields[3]
        yesterday = fields[4]
        change = fields[31]
        pct = fields[32]
        return f'{name} ({code}) 现价:{price} 昨收:{yesterday} 涨跌:{change} ({pct}%)'
    except:
        return f'{code} 数据解析失败'


if __name__ == '__main__':
    print('=== 宠物食品相关A股 ===\n')
    results = search_pet_stocks()
    for name, code, chg in results:
        print(f'{name} ({code}) 涨幅:{chg}%')

    print('\n=== 实时价格 ===')
    for name, code, _ in results:
        try:
            print(get_realtime(code))
        except Exception as e:
            print(f'{code} error: {e}')

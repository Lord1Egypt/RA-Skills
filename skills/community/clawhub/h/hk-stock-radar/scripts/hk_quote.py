"""
新浪财经港股个股实时行情
用法: python hk_quote.py hk00700
       python hk_quote.py hk00700 hk09988 hk03690
"""
import requests
import sys

def get_hk_quote(codes):
    if isinstance(codes, str):
        codes = [codes]
    url = f"https://hq.sinajs.cn/list={','.join(codes)}"
    headers = {"Referer": "http://finance.sina.com.cn"}
    r = requests.get(url, headers=headers, timeout=10)
    r.encoding = 'gbk'
    for line in r.text.strip().split('\n'):
        if '=' not in line:
            continue
        key, data = line.split('=')
        code = key.split('_')[-1].replace('"', '')  # e.g. hk00700
        vals = data.replace('"', '').replace(';', '').split(',')
        if len(vals) < 6:
            continue
        try:
            # 新浪港股格式: 0=代码,1=名称,2=现价,3=昨收,4=今开,5=高,6=低,7=涨跌额,8=涨跌幅%
            name = vals[1]
            price = float(vals[2])
            prev = float(vals[3])
            chg = price - prev
            pct = chg / prev * 100
            high = float(vals[5])
            low = float(vals[6])
            vol = float(vals[12]) / 1e4 if len(vals) > 12 else 0  # 成交量（手）
            arrow = "🔴" if pct > 0 else "🟢" if pct < 0 else "⚪"
            print(f"{arrow} {name:12s} {code:8s} 现价:{price:.2f} "
                  f"涨跌:{chg:+.2f}({pct:+.2f}%) 高:{high:.2f} 低:{low:.2f} 量:{vol:.0f}手")
        except (ValueError, IndexError):
            continue

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("用法: python hk_quote.py hk00700 [hk09988 ...]")
        sys.exit(1)
    get_hk_quote(sys.argv[1:])

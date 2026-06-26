"""
东方财富港股行业板块涨跌榜
"""
import requests
import sys

def get_hk_sector_ranking(top=20):
    url = "http://push2.eastmoney.com/api/qt/clist/get"
    params = {
        "pn": 1, "pz": top, "po": 1, "np": 1,
        "fltt": 2, "invt": 2,
        "fid": "f3",
        "fs": "m:1+t:23",  # 港股行业板块
        "fields": "f12,f14,f2,f3,f5,f6,f8"
    }
    headers = {"Referer": "http://quote.eastmoney.com/"}
    r = requests.get(url, params=params, headers=headers, timeout=10)
    r.raise_for_status()
    diff = r.json()["data"]["diff"]
    return diff

def format_sector(s):
    pct = s["f3"]
    arrow = "🔴" if pct > 0 else "🟢" if pct < 0 else "⚪"
    return f"{arrow} {s['f14']:15s} {'+' if pct>=0 else ''}{pct}%  成交额:{s['f6']/1e8:.1f}亿"

if __name__ == "__main__":
    top = int(sys.argv[1]) if len(sys.argv) > 1 else 20
    print("\n=== 港股板块涨跌榜 ===")
    data = get_hk_sector_ranking(top)
    print("\n【涨幅榜】")
    for s in sorted(data, key=lambda x: x["f3"], reverse=True)[:10]:
        print(format_sector(s))
    print("\n【跌幅榜】")
    for s in sorted(data, key=lambda x: x["f3"])[:10]:
        print(format_sector(s))

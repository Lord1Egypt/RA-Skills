"""
港股主要指数实时行情
恒生指数、恒生科技、恒生国企指数
"""
import requests

HK_INDICES = {
    "hkHSI": "恒生指数",
    "hkHSTECH": "恒生科技",
    "hkHSCEI": "恒生国企指数",
}

def get_hk_indices():
    codes = ",".join(HK_INDICES.keys())
    url = f"https://hq.sinajs.cn/list={codes}"
    headers = {"Referer": "http://finance.sina.com.cn"}
    try:
        r = requests.get(url, headers=headers, timeout=10)
        r.raise_for_status()
    except requests.RequestException:
        return {}
    r.encoding = 'gbk'
    results = {}
    for line in r.text.strip().split('\n'):
        if '=' not in line:
            continue
        key, data = line.split('=', 1)
        code = key.split('_')[-1].replace('"', '')  # e.g. hkHSI
        if code not in HK_INDICES:
            continue
        vals = data.replace('"', '').replace(';', '').split(',')
        if len(vals) < 9:
            continue
        try:
            name = vals[1]  # 恒生指数
            price = float(vals[6])
            prev = float(vals[3])
            if prev == 0:
                continue
            chg = price - prev
            pct = chg / prev * 100
            arrow = "🔴" if pct > 0 else "🟢" if pct < 0 else "⚪"
            results[code] = f"{arrow} {name}: {price:.2f} {chg:+.2f}({pct:+.2f}%)"
        except (ValueError, IndexError):
            continue
    return results

if __name__ == "__main__":
    print("\n=== 港股主要指数 ===")
    indices = get_hk_indices()
    for v in indices.values():
        print(v)

import json, sys, requests
sys.path.insert(0, r'C:\Users\Administrator\.qclaw\workspace-ag01\scripts')
sys.path.insert(0, r'C:\Users\Administrator\.qclaw\workspace-ag01\skills\trend-launch-scanner')
from unified_score import calc_unified_score
from trend_scanner import fetch_kline_tencent, add_indicators

CODES = ['000338', '002037', '000415', '002363']

def get_name(code):
    prefix = 'sz' if code.startswith(('0', '3')) else 'sh'
    try:
        r = requests.get(f'https://qt.gtimg.cn/q={prefix}{code}', timeout=3)
        return r.content.split(b'~')[1].decode('gbk', errors='replace')
    except Exception:
        return code

def get_price(code):
    prefix = 'sz' if code.startswith(('0', '3')) else 'sh'
    try:
        r = requests.get(f'https://qt.gtimg.cn/q={prefix}{code}', timeout=3)
        return float(r.content.split(b'~')[3].decode('gbk'))
    except Exception:
        return 0

out = {}
for code in CODES:
    name = get_name(code)
    cur_price = get_price(code)
    df = fetch_kline_tencent(code, days=80)
    if df is not None and len(df) >= 25:
        df = add_indicators(df)
        s = calc_unified_score(df)
        out[code] = {
            "name": name, "cur_price": cur_price,
            "final_score": s.get('final_score'),
            "macd_score": s.get('macd_score'),
            "ma_score": s.get('ma_score'),
            "rsi_score": s.get('rsi_score'),
            "vol_score": s.get('vol_score'),
            "rsi": s.get('rsi'),
            "rsi_stage": s.get('rsi_stage'),
            "signal_type": s.get('signal_type'),
            "oversold_bonus": s.get('oversold_bonus'),
            "oversold_signal": s.get('oversold_signal'),
        }
    else:
        out[code] = {"name": name, "cur_price": cur_price, "error": "no data"}

with open(r'C:\Users\Administrator\.qclaw\workspace-ag01\data\_holdings_detail.json', 'w', encoding='utf-8') as f:
    json.dump(out, f, ensure_ascii=False, indent=2)
print("done")

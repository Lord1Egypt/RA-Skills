"""
持仓诊断 v4 - 统一入口
数据源：scripts/_holdings_std.py（唯一持仓定义）
评分：scripts/unified_score.py v5.0
卖出：skills/holdings-analysis/sell_signal.py
"""
import json, os, sys, requests, numpy as np, pandas as pd
from datetime import date

# ─── 路径设置 ──────────────────────────────────────────────────────
_BASE = os.path.dirname(os.path.abspath(__file__))
_WORKSPACE = r'C:\Users\Administrator\.qclaw\workspace-ag01'
sys.path.insert(0, os.path.join(_WORKSPACE, 'scripts'))
sys.path.insert(0, os.path.join(_WORKSPACE, 'skills', 'trend-launch-scanner'))

# ─── 持仓数据（唯一数据源：scripts/_holdings_std.py）───────────────
_std = os.path.join(_WORKSPACE, 'scripts', '_holdings_std.py')
_h = {}
exec(open(_std, encoding='utf-8').read(), _h)
HOLDINGS = _h.get('HOLDINGS', [])

# ─── 外部模块 ─────────────────────────────────────────────────────
from unified_score import calc_unified_score
from sell_signal import calc_sell_score, add_indicators as sell_add_indicators
from trend_scanner import fetch_kline_tencent, add_indicators

# ─── 评分和卖出信号已改为调用外部模块 ─────────────────────────────
# calc_unified_score → scripts/unified_score.py v5.0
# calc_sell_score    → skills/holdings-analysis/sell_signal.py
# fetch_kline_tencent, add_indicators → skills/trend-launch-scanner/trend_scanner.py

# ─── 工具函数 ────────────────────────────────────────────────────────
def get_name(code):
    prefix='sz' if code.startswith(('0','3')) else 'sh'
    try:
        r=requests.get(f'https://qt.gtimg.cn/q={prefix}{code}',timeout=3)
        return r.content.split(b'~')[1].decode('gbk',errors='replace')
    except: return code

def get_price(code):
    prefix='sz' if code.startswith(('0','3')) else 'sh'
    try:
        r=requests.get(f'https://qt.gtimg.cn/q={prefix}{code}',timeout=3)
        return float(r.content.split(b'~')[3].decode('gbk'))
    except: return 0

# ─── 主逻辑 ─────────────────────────────────────────────────────────
results=[]
for h in HOLDINGS:
    code=h['code']; name=get_name(code)
    cur=get_price(code); bp=h['buy_price']
    profit_pct=(cur/bp-1)*100 if cur else 0
    days=(date.today()-date.fromisoformat(h['buy_date'])).days
    df=fetch_kline_tencent(code,80)
    buy_s=None; sell_s=None
    if df is not None and len(df)>=25:
        df1=add_indicators(df.copy())
        buy_s=calc_unified_score(df1, buy_price=bp)
        df2=sell_add_indicators(df.copy())
        sell_s=calc_sell_score(df2, bp, h['buy_date'])
    bsv=buy_s['final_score'] if buy_s else 0
    macd_s=buy_s.get('macd_score',0) if buy_s else 0
    ma_s=buy_s.get('ma_score',0) if buy_s else 0
    rsi_s=buy_s.get('rsi_score',0) if buy_s else 0
    vol_s=buy_s.get('vol_score',0) if buy_s else 0
    ssv=sell_s['sell_score'] if sell_s else 0
    sell_action=sell_s.get('action','') if sell_s else ''
    sell_signals=[s[0] for s in (sell_s.get('sell_signals',[]) if sell_s else [])]
    # 兼容旧sell_signal.py返回的action格式
    if '建议卖出' in sell_action: ov='SELL'
    elif '警惕风险' in sell_action or 'WARNING' in sell_action: ov='WARNING'
    elif sell_s and sell_s.get('sell_score',0)>=40: ov='SELL'
    elif sell_s and sell_s.get('sell_score',0)>=25: ov='WARNING'
    else: ov='HOLD'
    status='PASS' if bsv>=55 else 'FAIL'
    if ov=='SELL': status='SELL'
    elif ov=='WARNING': status='WARN'
    results.append({'code':code,'name':name,'cur_price':cur,'buy_price':bp,
        'profit_pct':round(profit_pct,2),'days':days,'buy_score':bsv,
        'macd_score':macd_s,'ma_score':ma_s,'rsi_score':rsi_s,'vol_score':vol_s,
        'sell_score':ssv,'action':ov,'signals':sell_signals,
        'rsi':round(buy_s['rsi'],1) if buy_s else 0,'overall':ov,'status':status})

total_profit=sum(r['profit_pct'] for r in results)
out={'date':str(date.today()),'positions':results,
     'summary':{'total_profit':round(total_profit,2),
                'avg_buy_score':round(sum(r['buy_score'] for r in results)/max(1,len(results)),1),
                'avg_sell_score':round(sum(r['sell_score'] for r in results)/max(1,len(results)),1),
                'sell_count':sum(1 for r in results if r['sell_score']>=40),
                'warning_count':sum(1 for r in results if 25<=r['sell_score']<40)}}
out_path=os.path.join(_BASE,'holdings_result.json')
with open(out_path,'w',encoding='utf-8') as f:
    json.dump(out,f,ensure_ascii=False,indent=2)

today_str=date.today().strftime('%m-%d')
print('=== HOLDINGS ANALYSIS {} ==='.format(today_str))
for r in results:
    print('  [{}]  {} {} score={} profit={:+.1f}% close={:.2f} buy={:.2f}'.format(
        r['status'].upper(), r['code'], r['name'][:6], r['buy_score'],
        r['profit_pct'], r['cur_price'], r['buy_price']))
    print('        sell_score={} {} signals={}'.format(
        r['sell_score'], r['overall'], r['signals']))

print()
print('Total positions: {}'.format(len(results)))
print('Overall P&L: {:+.1f}%'.format(total_profit/len(results) if results else 0))
print('Avg buy_score: {}  Avg sell_score: {}'.format(
    out['summary']['avg_buy_score'], out['summary']['avg_sell_score']))
print('Sell signals: {}  Warnings: {}'.format(
    out['summary']['sell_count'], out['summary']['warning_count']))
print('OK -> {}'.format(out_path))

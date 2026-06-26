#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
沪深300多因子投研分析 v5.1 — 修复版
数据源: JQData(全量) + AKShare(4个可用接口)
"""
import io, sys
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
import pandas as pd
import numpy as np
import logging
from datetime import datetime, timedelta

logging.basicConfig(level=logging.INFO, format='%(message)s')
logger = logging.getLogger(__name__)

# ==================== 初始化 ====================
import jqdatasdk as jq
jq.auth('13918681158', 'Yindb1158')
import akshare as ak

print("=" * 80)
print("  沪深300多因子投研分析 v5.1")
print("  生成时间: %s" % datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
print("  数据源: JQData(主线) + AKShare(补充)")
print("=" * 80)

# ==================== 1. 沪深300成分股 ====================
print("\n[1/6] 获取沪深300成分股...")
hs300_df = ak.index_stock_cons_csindex(symbol="000300")
if hs300_df is not None and len(hs300_df) > 0:
    cols = list(hs300_df.columns)
    code_col = [c for c in cols if '成分' in c and '代' in c]
    name_col = [c for c in cols if '成分' in c and '名' in c]
    
    if code_col:
        raw_codes = hs300_df[code_col[0]].tolist()
    else:
        raw_codes = hs300_df[cols[4]].tolist() if len(cols) > 4 else []
    
    # 清洗6位代码
    test_codes = []
    for c in raw_codes:
        s = str(c).strip().zfill(6)
        if len(s) == 6 and s.isdigit():
            test_codes.append(s)
    test_codes = list(dict.fromkeys(test_codes))[:20]
    logger.info("  成分股: %d 只 → 取前%d只分析" % (len(raw_codes), len(test_codes)))
else:
    test_codes = ['600519','000001','601318','600036','000333','601012',
                  '600900','600276','300750','601888','600309','000651',
                  '601166','600030','002415','601398','601288','601988',
                  '600048','002594']

name_map = {}
jq_codes = {}
for code in test_codes:
    suffix = 'XSHG' if code.startswith('6') else 'XSHE'
    jq_code = '%s.%s' % (code, suffix)
    jq_codes[code] = jq_code
    try:
        sec = jq.get_security_info(jq_code)
        if sec:
            name_map[code] = sec.display_name
    except:
        name_map[code] = ''

# ==================== 2. 日K线 (JQData) ====================
print("\n[2/6] 获取日K线 (JQData)...")

daily_data = {}
kline_ok = 0
for code in test_codes:
    jq_code = jq_codes[code]
    try:
        df = jq.get_price(jq_code, count=120, frequency='daily',
                          end_date='2026-02-10',
                          fields=['open', 'close', 'high', 'low', 'volume', 'money'])
        if df is not None and len(df) >= 30:
            df['pct_chg'] = df['close'].pct_change() * 100
            df['amount'] = df.get('money', df['volume'] * df['close'])
            daily_data[code] = df
            kline_ok += 1
    except Exception as e:
        pass
logger.info("  日K线成功: %d/%d 只" % (kline_ok, len(test_codes)))

# ==================== 3. 基本面 (JQData - 逐股查询) ====================
print("\n[3/6] 获取基本面 (JQData逐股)...")

fundamentals = {}
fund_ok = 0
for code in test_codes:
    jq_code = jq_codes[code]
    try:
        result = {'code': code, 'name': name_map.get(code, '')}
        
        # 估值
        try:
            val = jq.get_fundamentals(
                jq.query(jq.valuation.pe_ratio, jq.valuation.pb_ratio,
                         jq.valuation.ps_ratio, jq.valuation.market_cap)
                .filter(jq.valuation.code == jq_code),
                date='2026-02-10'
            )
            if val is not None and len(val) > 0:
                result['pe'] = round(float(val['pe_ratio'].iloc[0]), 2) if val['pe_ratio'].notna().any() else None
                result['pb'] = round(float(val['pb_ratio'].iloc[0]), 2) if val['pb_ratio'].notna().any() else None
                result['ps'] = round(float(val['ps_ratio'].iloc[0]), 2) if val['ps_ratio'].notna().any() else None
                result['market_cap'] = round(float(val['market_cap'].iloc[0]), 2) if val['market_cap'].notna().any() else None
        except:
            pass
        
        # 财务指标
        try:
            ind = jq.get_fundamentals(
                jq.query(jq.indicator.roe, jq.indicator.roa,
                         jq.indicator.gross_profit_margin, jq.indicator.net_profit_margin)
                .filter(jq.indicator.code == jq_code),
                date='2026-02-10'
            )
            if ind is not None and len(ind) > 0:
                result['roe'] = round(float(ind['roe'].iloc[0]), 2) if ind['roe'].notna().any() else None
                result['roa'] = round(float(ind['roa'].iloc[0]), 2) if ind['roa'].notna().any() else None
                result['gross_margin'] = round(float(ind['gross_profit_margin'].iloc[0]), 2) if ind['gross_profit_margin'].notna().any() else None
                result['net_margin'] = round(float(ind['net_profit_margin'].iloc[0]), 2) if ind['net_profit_margin'].notna().any() else None
        except:
            pass
        
        # 营收利润增长
        try:
            curr = jq.get_fundamentals(
                jq.query(jq.income.operating_revenue, jq.income.net_profit)
                .filter(jq.income.code == jq_code),
                date='2026-02-10'
            )
            prev = jq.get_fundamentals(
                jq.query(jq.income.operating_revenue, jq.income.net_profit)
                .filter(jq.income.code == jq_code),
                date='2025-02-10'
            )
            if curr is not None and prev is not None and len(curr) > 0 and len(prev) > 0:
                c_rev = float(curr['operating_revenue'].iloc[0]) if curr['operating_revenue'].notna().any() else None
                p_rev = float(prev['operating_revenue'].iloc[0]) if prev['operating_revenue'].notna().any() else None
                c_prof = float(curr['net_profit'].iloc[0]) if curr['net_profit'].notna().any() else None
                p_prof = float(prev['net_profit'].iloc[0]) if prev['net_profit'].notna().any() else None
                if c_rev and p_rev and p_rev > 0:
                    result['rev_growth'] = round((c_rev / p_rev - 1) * 100, 2)
                if c_prof and p_prof and p_prof > 0:
                    result['prof_growth'] = round((c_prof / p_prof - 1) * 100, 2)
        except:
            pass
        
        if result.get('pe') or result.get('roe'):
            fundamentals[code] = result
            fund_ok += 1
    except:
        pass

logger.info("  基本面成功: %d/%d 只" % (fund_ok, len(test_codes)))

# ==================== 4. 技术面 ====================
print("\n[4/6] 技术面分析...")

tech_signals = {}
for code, df in daily_data.items():
    close = df['close']
    result = {}
    
    # MACD
    ema12 = close.ewm(span=12).mean()
    ema26 = close.ewm(span=26).mean()
    dif = ema12 - ema26
    dea = dif.ewm(span=9).mean()
    macd = 2 * (dif - dea)
    result['macd_golden'] = macd.iloc[-1] > 0 and macd.iloc[-2] <= 0
    
    # KDJ
    low_9 = df['low'].rolling(9).min()
    high_9 = df['high'].rolling(9).max()
    rsv = (close - low_9) / (high_9 - low_9) * 100
    k = rsv.ewm(com=2).mean()
    d = k.ewm(com=2).mean()
    j = 3 * k - 2 * d
    result['kdj_golden'] = (j.iloc[-1] > d.iloc[-1]) and (j.iloc[-2] <= d.iloc[-2])
    
    # 均线
    ma5 = close.rolling(5).mean()
    ma20 = close.rolling(20).mean()
    ma60 = close.rolling(60).mean()
    if len(df) >= 60:
        result['ma_bull'] = ma5.iloc[-1] > ma20.iloc[-1] > ma60.iloc[-1]
        result['ma_bear'] = ma5.iloc[-1] < ma20.iloc[-1] < ma60.iloc[-1]
    else:
        result['ma_bull'] = False
        result['ma_bear'] = False
    
    # 涨跌幅
    result['ret_1m'] = round((close.iloc[-1] / close.iloc[-21] - 1) * 100, 2) if len(df) >= 21 else 0
    result['ret_3m'] = round((close.iloc[-1] / close.iloc[-60] - 1) * 100, 2) if len(df) >= 60 else 0
    result['latest_close'] = round(close.iloc[-1], 2)
    result['latest_date'] = str(df.index[-1])[:10] if hasattr(df.index[-1], 'strftime') else str(df.index[-1])[:10]
    
    tech_signals[code] = result

logger.info("  技术面完成: %d/%d 只" % (len(tech_signals), len(test_codes)))

# ==================== 5. 多因子评分 ====================
print("\n[5/6] 多因子评分...")

def sf(v, default=None):
    try:
        f = float(v)
        return f if not (np.isinf(f) or np.isnan(f)) else default
    except:
        return default

def score_stock(code):
    f = fundamentals.get(code, {})
    t = tech_signals.get(code, {})
    score = 0
    
    pe = sf(f.get('pe')); pb = sf(f.get('pb'))
    if pe and pe > 0:
        if pe < 10: score += 30
        elif pe < 15: score += 25
        elif pe < 20: score += 20
        elif pe < 30: score += 15
        elif pe < 50: score += 10
        else: score += 5
    if pb and pb > 0:
        if pb < 1: score += 10
        elif pb < 2: score += 8
        elif pb < 4: score += 6
        elif pb < 6: score += 4
        else: score += 2
    
    roe = sf(f.get('roe'))
    if roe and roe > 0:
        if roe > 20: score += 10
        elif roe > 15: score += 8
        elif roe > 10: score += 6
        elif roe > 5: score += 4
        else: score += 2
    
    rg = sf(f.get('rev_growth')); pg = sf(f.get('prof_growth'))
    if rg and rg > 0: score += 5
    if pg and pg > 0: score += 5
    if rg and rg > 20: score += 3
    if pg and pg > 20: score += 3
    
    r1 = sf(t.get('ret_1m'), 0); r3 = sf(t.get('ret_3m'), 0)
    if r1 > 0: score += 5
    if r3 > 0: score += 5
    if r1 > 5: score += 3
    if r3 > 10: score += 3
    
    if t.get('macd_golden'): score += 8
    if t.get('kdj_golden'): score += 5
    if t.get('ma_bull'): score += 5
    
    risk = 0
    if t.get('ma_bear'): risk += 1
    if pe and pe > 50: risk += 1
    if rg and rg < -20: risk += 1
    
    return score, risk

results = []
for code in test_codes:
    if code in fundamentals or code in tech_signals:
        score, risk = score_stock(code)
        f = fundamentals.get(code, {})
        t = tech_signals.get(code, {})
        results.append({
            '代码': code,
            '名称': f.get('name', name_map.get(code, '')),
            '最新价': sf(t.get('latest_close')),
            'PE': sf(f.get('pe')),
            'PB': sf(f.get('pb')),
            'ROE': sf(f.get('roe')),
            '营收增长': sf(f.get('rev_growth')),
            '利润增长': sf(f.get('prof_growth')),
            '1月涨幅': sf(t.get('ret_1m'), 0),
            '3月涨幅': sf(t.get('ret_3m'), 0),
            '综合得分': score,
            '风险等级': risk,
            'MACD金叉': t.get('macd_golden', False),
            'KDJ金叉': t.get('kdj_golden', False),
            '均线多头': t.get('ma_bull', False),
            '均线空头': t.get('ma_bear', False),
        })

df_results = pd.DataFrame(results).sort_values('综合得分', ascending=False)

# ==================== 6. AKShare附加 ====================
print("\n[6/6] AKShare附加数据...")

# 分红送配
try:
    fhps = ak.stock_fhps_em()
    logger.info("  分红送配: %d 条" % len(fhps) if fhps is not None else 0)
except: pass

# 个股资金流 (3只)
ff_ok = 0
for code in test_codes[:3]:
    try:
        mkt = 'sh' if code.startswith('6') else 'sz'
        ff = ak.stock_individual_fund_flow(stock=code, market=mkt)
        if ff is not None and len(ff) > 0:
            ff_ok += 1
    except: pass
logger.info("  个股资金流: %d/3 只" % ff_ok)

# 龙虎榜
try:
    lhb = ak.stock_lhb_detail_em(start_date="20260209", end_date="20260210")
    logger.info("  龙虎榜: %d 条" % len(lhb) if lhb is not None else 0)
except: pass

# ==================== 报告输出 ====================
print("\n" + "=" * 80)
print("  分析报告")
print("=" * 80)

macd_n = sum(1 for r in results if r['MACD金叉'])
kdj_n = sum(1 for r in results if r['KDJ金叉'])
bull_n = sum(1 for r in results if r['均线多头'])
bear_n = sum(1 for r in results if r['均线空头'])
print("\n技术信号: MACD金叉:%d | KDJ金叉:%d | 均线多头:%d | 均线空头:%d" % (macd_n, kdj_n, bull_n, bear_n))

pe_v = [r['PE'] for r in results if r['PE'] and r['PE'] > 0]
roe_v = [r['ROE'] for r in results if r['ROE'] and r['ROE'] > 0]
print("基本面: PE均值=%.1f | ROE均值=%.1f%%" % (np.mean(pe_v) if pe_v else 0, np.mean(roe_v) if roe_v else 0))

print("\n潜力个股 TOP 10:")
print("-" * 100)
fmt = "  %-2d. %-6s %-8s  价:%-8.2f PE:%-6.1f ROE:%-6.1f%% 营收:%-6.1f%% 利润:%-6.1f%% 得分:%-6.1f 风险:%s 1月:%+.1f%%"
for i, (_, row) in enumerate(df_results.head(10).iterrows()):
    rl = '低' if row['风险等级'] == 0 else ('中' if row['风险等级'] <= 1 else '高')
    print(fmt % (i+1, row['代码'], row['名称'] or '',
        row['最新价'] or 0, row['PE'] or 0, row['ROE'] or 0,
        row['营收增长'] or 0, row['利润增长'] or 0,
        row['综合得分'], rl, row['1月涨幅']))

hr = df_results[df_results['风险等级'] >= 2].sort_values('综合得分')
if len(hr) > 0:
    print("\n高风险:")
    for _, r in hr.iterrows():
        mt = '空头' if r['均线空头'] else ('多头' if r['均线多头'] else '中性')
        print("  ⚠ %s %-8s 得分:%.1f PE:%.1f 均线:%s" % (r['代码'], r['名称'] or '', r['综合得分'], r['PE'] or 0, mt))

try:
    fhps = ak.stock_fhps_em()
    if fhps is not None and len(fhps) > 0:
        print("\n分红送配 (前5):")
        for _, r in fhps.head(5).iterrows():
            print("  %s %s  分红比例:%.1f%%  股息率:%.4f%%" % (r['代码'], r['名称'], r['现金分红-现金分红比例'], r['现金分红-股息率']))
except: pass

print("\n" + "=" * 80)
print("  数据源使用")
print("=" * 80)
print("  JQData:    日K线/估值/财务指标/收入表 (主力)")
print("  AKShare:   沪深300成分股/分红送配/个股资金流/龙虎榜 (补充)")
print("\n  被拦截接口: 东方财富HTTP / AKShare push2")

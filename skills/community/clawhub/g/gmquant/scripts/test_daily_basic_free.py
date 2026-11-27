# -*- coding: utf-8 -*-
"""测试 stk_get_daily_basic / stk_get_daily_basic_pt 的 free_shr、free_turnrate 新字段"""
import sys, io, os
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
from gm.api import *

TOKEN = os.environ.get('GM_TOKEN', '')
set_token(TOKEN)

SYM = 'SHSE.600519'

print('=' * 70)
print('TEST A: stk_get_daily_basic_pt 查询 free_shr / free_turnrate')
print('=' * 70)
try:
    df = stk_get_daily_basic_pt(
        symbols=[SYM],
        fields='tclose,turnrate,ttl_shr,circ_shr,ttl_shr_unl,ttl_shr_ltd,a_shr_unl,h_shr_unl,free_shr,free_turnrate',
        trade_date=None, df=True)
    print(df.to_string())
    print('\n字段列表:', list(df.columns))
    for f in ['free_shr', 'free_turnrate']:
        print(f'  含 {f} ->', 'PASS' if f in df.columns else 'FAIL')
except Exception as e:
    print(f'  EXCEPTION: {type(e).__name__}: {e}')

print()
print('=' * 70)
print('TEST B: stk_get_daily_basic（时序）查询 free_shr / free_turnrate')
print('=' * 70)
try:
    df2 = stk_get_daily_basic(
        symbol=SYM,
        fields='tclose,turnrate,ttl_shr,circ_shr,free_shr,free_turnrate',
        start_date='2026-11-20', end_date='2026-11-26', df=True)
    print(df2.to_string())
    for f in ['free_shr', 'free_turnrate']:
        print(f'  含 {f} ->', 'PASS' if f in df2.columns else 'FAIL')
except Exception as e:
    print(f'  EXCEPTION: {type(e).__name__}: {e}')

print()
print('=' * 70)
print('TEST C: 用 free_shr * 上一交易日收盘价 计算自由流通市值')
print('=' * 70)
try:
    # 取最近5个交易日的 free_shr 和 tclose
    d = stk_get_daily_basic(symbol=SYM, fields='tclose,free_shr,free_turnrate',
                            start_date='2026-11-18', end_date='2026-11-26', df=True)
    if d is None or len(d) == 0:
        print('  无数据返回')
    else:
        d = d.sort_values('trade_date').reset_index(drop=True)
        print(d.to_string())
        if len(d) >= 2:
            prev_close = d.loc[len(d) - 2, 'tclose']
            today_free_shr = d.loc[len(d) - 1, 'free_shr']
            fmv = today_free_shr * prev_close
            print(f'\n  上一交易日收盘价 = {prev_close}')
            print(f'  当日 free_shr     = {today_free_shr:.0f} 股')
            print(f'  自由流通市值      = {fmv/1e8:.2f} 亿元')
            print(f'  (= free_shr {today_free_shr:.0f} × 前收盘 {prev_close})')
            # 交叉验证：用 free_turnrate 反推成交量
            ft = d.loc[len(d) - 1, 'free_turnrate']
            if ft and ft > 0:
                vol_implied = ft / 100.0 * today_free_shr
                print(f'\n  用 free_turnrate 反推成交量 = {ft}% × {today_free_shr:.0f} = {vol_implied:.0f} 股')
                print(f'  与 free_shr 口径自洽性: 可验证')
except Exception as e:
    print(f'  EXCEPTION: {type(e).__name__}: {e}')

print()
print('=' * 70)
print('TEST D: 同时取 tclose 与 free_shr 用 shift 计算（策略内常用写法）')
print('=' * 70)
try:
    import pandas as pd
    d3 = stk_get_daily_basic(symbol=SYM, fields='tclose,circ_shr,free_shr',
                             start_date='2026-11-18', end_date='2026-11-26', df=True)
    if d3 is not None and len(d3) > 0:
        d3 = d3.sort_values('trade_date').reset_index(drop=True)
        d3['free_mv'] = d3['free_shr'] * d3['tclose'].shift(1)
        d3['circ_mv'] = d3['circ_shr'] * d3['tclose'].shift(1)
        d3['free_mv_yi'] = d3['free_mv'] / 1e8
        d3['circ_mv_yi'] = d3['circ_mv'] / 1e8
        print(d3[['trade_date', 'tclose', 'free_shr', 'free_mv_yi', 'circ_mv_yi']].to_string())
        print('\n  注：第1行 free_mv 为 NaN（无前一日收盘价），符合预期')
except Exception as e:
    print(f'  EXCEPTION: {type(e).__name__}: {e}')

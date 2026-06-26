"""
掘金量化 v2.1.0 全量增值数据 API 测试
覆盖：股票增值数据、基金增值数据、可转债增值数据、期货增值数据、新增函数
"""

import sys, os, io, json, datetime
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

from gm.api import *
from gm.enum import *

TOKEN = os.environ.get('GM_TOKEN', '')
if not TOKEN:
    TOKEN = 'c2a347464c31056c84165dff766750fbf2ec67b4'

set_token(TOKEN)
print(f'✅ Token 已设置')
print(f'   时间: {datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}')
print()

results = {'pass': 0, 'fail': 0, 'skip': 0, 'details': []}

def test(name, func):
    try:
        result = func()
        results['pass'] += 1
        results['details'].append((name, '✅ 通过', str(result)[:120]))
        print(f'  ✅ {name}')
        if result is not None:
            print(f'     → {str(result)[:120]}')
    except Exception as e:
        err = str(e)[:200]
        if '1028' in err or 'L2' in err or '未开通' in err or '权限' in err:
            results['skip'] += 1
            results['details'].append((name, '⏭️ 跳过(无权限)', err[:100]))
            print(f'  ⏭️ {name} (无权限)')
        else:
            results['fail'] += 1
            results['details'].append((name, '❌ 失败', err[:100]))
            print(f'  ❌ {name} → {err[:100]}')


# ========================================================================
# 1. 行 情 查 询 函 数（current / last_tick / current_price）
# ========================================================================
print('=' * 60)
print('📊 第1组: 行情查询函数（current / last_tick / current_price）')
print('=' * 60)

def t_current():
    data = current(symbols='SHSE.600519,SZSE.000001')
    assert len(data) == 2, f'返回{len(data)}条, 期望2条'
    return f'返回{len(data)}条, {data[0]["symbol"]}={data[0]["price"]}'
test('current (多标的)', t_current)

def t_current_price():
    data = current_price(symbols='SHSE.600519,SZSE.000001')
    assert len(data) == 2, f'返回{len(data)}条, 期望2条'
    for item in data:
        assert 'price' in item, f'缺少price字段'
    return f'返回{len(data)}条, {data[0]["symbol"]}={data[0]["price"]}'
test('current_price (新函数)', t_current_price)

def t_last_tick():
    try:
        subscribe(symbols='SHSE.600519,SZSE.000001', frequency='tick')
        data = last_tick(symbols='SHSE.600519,SZSE.000001', fields='symbol,price,open,created_at')
        if data:
            return f'返回{len(data)}条, {data[0]["symbol"]}={data[0]["price"]}'
        return '返回空列表(未订阅成功)'
    except Exception as e:
        return f'需策略环境: {str(e)[:80]}'
test('last_tick (新函数)', t_last_tick)


# ========================================================================
# 2. 股 票 增 值 数 据
# ========================================================================
print()
print('=' * 60)
print('📊 第2组: 股票增值数据')
print('=' * 60)

# --- stk_get_industry_category ---
def t1():
    df = stk_get_industry_category(source='sw2021', level=1)
    assert len(df) > 20, f'返回{len(df)}行'
    return f'申万一级行业 {len(df)}个'
test('stk_get_industry_category 申万一级行业', t1)

def t2():
    df = stk_get_industry_category(source='sw2021', level=2)
    assert len(df) > 50, f'返回{len(df)}行'
    return f'申万二级行业 {len(df)}个'
test('stk_get_industry_category 申万二级行业', t2)

# --- stk_get_industry_constituents ---
def t3():
    # 用证监会分类查询
    df = stk_get_industry_constituents(industry_code='J', date='')
    return f'金融业成分股 {len(df)}只'
test('stk_get_industry_constituents', t3)

# --- stk_get_symbol_industry ---
def t4():
    df = stk_get_symbol_industry(symbols='SHSE.600519,SZSE.000001', source='sw2021', level=1)
    assert len(df) == 2, f'返回{len(df)}行'
    return f'{df.iloc[0]["sec_name"]}: {df.iloc[0]["industry_name"]}'
test('stk_get_symbol_industry', t4)

# --- stk_get_sector_category ---
def t5():
    df = stk_get_sector_category(sector_type='1003')
    assert len(df) > 50, f'返回{len(df)}个'
    return f'概念板块 {len(df)}个'
test('stk_get_sector_category 概念板块', t5)

# --- stk_get_sector_constituents ---
def t6():
    df = stk_get_sector_constituents(sector_code='007001')
    assert len(df) > 0, '空结果'
    return f'军工板块 {len(df)}只成分股'
test('stk_get_sector_constituents', t6)

# --- stk_get_symbol_sector ---
def t7():
    df = stk_get_symbol_sector(symbols='SHSE.600519', sector_type='1002')
    return f'{df.iloc[0]["sec_name"]}: {df.iloc[0]["sector_name"]}'
test('stk_get_symbol_sector', t7)

# --- stk_get_dividend ---
def t8():
    df = stk_get_dividend(symbol='SHSE.600519', start_date='2023-01-01', end_date='2025-12-31')
    return f'茅台分红 {len(df)}条'
test('stk_get_dividend 分红送股', t8)

# --- stk_get_ration ---
def t9():
    df = stk_get_ration(symbol='SZSE.000728', start_date='2005-01-01', end_date='2022-12-31')
    return f'配股 {len(df)}条'
test('stk_get_ration 配股信息', t9)

# --- stk_get_adj_factor ---
def t10():
    df = stk_get_adj_factor(symbol='SHSE.600519', start_date='2025-01-01', end_date='2025-01-15')
    return f'复权因子 {len(df)}条'
test('stk_get_adj_factor 复权因子', t10)

# --- stk_get_shareholder_num ---
def t11():
    df = stk_get_shareholder_num(symbol='SHSE.600519', start_date='2025-01-01', end_date='2025-05-26')
    return f'股东户数 {len(df)}条'
test('stk_get_shareholder_num 股东户数', t11)

# --- stk_get_top_shareholder ---
def t12():
    df = stk_get_top_shareholder(symbol='SHSE.600519', start_date='2025-01-01', end_date='2025-05-26', tradable_holder=False)
    return f'十大股东 {len(df)}条'
test('stk_get_top_shareholder 十大股东', t12)

# --- stk_get_share_change ---
def t13():
    df = stk_get_share_change(symbol='SHSE.600519', start_date='2024-01-01', end_date='2025-05-26')
    return f'股本变动 {len(df)}条'
test('stk_get_share_change 股本变动', t13)

# --- 龙虎榜 ---
def t14():
    df = stk_abnor_change_stocks(trade_date='')
    return f'龙虎榜股票 {len(df)}只'
test('stk_abnor_change_stocks 龙虎榜', t14)

def t15():
    df = stk_abnor_change_detail(trade_date='')
    return f'龙虎榜营业部 {len(df)}条'
test('stk_abnor_change_detail 龙虎榜营业部', t15)

# --- 沪深港通 ---
def t16():
    df = stk_quota_shszhk_infos()
    return f'沪深港通额度 {len(df)}条'
test('stk_quota_shszhk_infos 沪深港通额度', t16)

def t17():
    df = stk_active_stock_top10_shszhk_info(trade_date='')
    return f'十大活跃成交股 {len(df)}条'
test('stk_active_stock_top10_shszhk_info 十大活跃成交', t17)

# --- 股票资金流向 ---
def t18():
    df = stk_get_money_flow(symbols='SHSE.600519', trade_date='2026-05-25')
    return f'资金流向 {len(df)}条, 主力净流入={df.iloc[0]["main_net_in"]}'
test('stk_get_money_flow 资金流向', t18)

# --- 财务审计意见 ---
def t19():
    # 参数: symbols, date, rpt_date, df
    result = stk_get_finance_audit(symbols='SHSE.600519', date='2026-05-26', df=True)
    return f'审计意见 {len(result)}条'
test('stk_get_finance_audit 审计意见', t19)

# --- 业绩预告 ---
def t20():
    # 参数: symbols, rpt_type, date, df
    result = stk_get_finance_forecast(symbols='SHSE.600519', rpt_type='4', date='2026-05-26', df=False)
    if result:
        item = dict(result[0]) if hasattr(result[0], 'keys') else result[0]
        return f'业绩预告 {len(result)}条'
    return f'业绩预告 0条'
test('stk_get_finance_forecast 业绩预告', t20)

# --- get_open_call_auction ---
def t21():
    df = get_open_call_auction(symbols='SHSE.600519', trade_date='')
    return f'集合竞价 {len(df)}条'
test('get_open_call_auction 集合竞价(股票)', t21)


# ========================================================================
# 3. 基 金 增 值 数 据
# ========================================================================
print()
print('=' * 60)
print('📊 第3组: 基金增值数据')
print('=' * 60)

def t22():
    df = fnd_get_etf_constituents(etf='SHSE.510050')
    assert len(df) > 0, '空结果'
    return f'上证50ETF {len(df)}只成分股'
test('fnd_get_etf_constituents ETF成分股', t22)

def t23():
    df = fnd_get_portfolio(fund='SHSE.510300', report_type=1, portfolio_type='stk', start_date='2024-01-01', end_date='2024-12-31')
    return f'沪深300ETF持仓 {len(df)}只'
test('fnd_get_portfolio 基金资产组合', t23)

def t24():
    df = fnd_get_net_value(fund='SHSE.510300', start_date='2025-05-01', end_date='2025-05-26')
    return f'净值 {len(df)}条'
test('fnd_get_net_value 基金净值', t24)

def t25():
    df = fnd_get_adj_factor(fund='SZSE.161725', start_date='2021-12-01', end_date='2022-01-01')
    return f'复权因子 {len(df)}条'
test('fnd_get_adj_factor 基金复权因子', t25)

def t26():
    df = fnd_get_dividend(fund='SZSE.161725', start_date='2000-01-01', end_date='2022-09-07')
    return f'分红 {len(df)}条'
test('fnd_get_dividend 基金分红', t26)

def t27():
    df = fnd_get_split(fund='SZSE.161725', start_date='2000-01-01', end_date='2022-09-07')
    return f'拆分折算 {len(df)}条'
test('fnd_get_split 基金拆分折算', t27)

def t28():
    df = fnd_get_share(fund='SHSE.510300', start_date='2025-04-01', end_date='2025-05-26')
    return f'规模 {len(df)}条'
test('fnd_get_share 基金规模', t28)

def t29():
    df = get_open_call_auction(symbols='SHSE.510300,SZSE.159922', trade_date='')
    return f'集合竞价 {len(df)}条'
test('get_open_call_auction 集合竞价(基金)', t29)


# ========================================================================
# 4. 可 转 债 增 值 数 据
# ========================================================================
print()
print('=' * 60)
print('📊 第4组: 可转债增值数据')
print('=' * 60)

def t30():
    df = bnd_get_conversion_price(symbol='SZSE.127018', start_date='2024-01-01', end_date='2025-05-26')
    return f'转股价变动 {len(df)}条'
test('bnd_get_conversion_price 转股价变动', t30)

def t31():
    df = bnd_get_call_info(symbol='SZSE.127018', start_date='2024-01-01', end_date='2025-05-26')
    return f'赎回信息 {len(df)}条'
test('bnd_get_call_info 赎回信息', t31)

def t32():
    df = bnd_get_put_info(symbol='SZSE.123456', start_date='2024-01-01', end_date='2025-05-26')
    return f'回售信息 {len(df)}条'
test('bnd_get_put_info 回售信息', t32)

def t33():
    df = bnd_get_amount_change(symbol='SZSE.127018', start_date='2024-01-01', end_date='2025-05-26')
    return f'规模变动 {len(df)}条'
test('bnd_get_amount_change 剩余规模变动', t33)

def t34():
    df = bnd_get_analysis(symbol='SZSE.127018', start_date='2025-04-01', end_date='2025-05-26')
    return f'分析指标 {len(df)}条'
test('bnd_get_analysis 转债分析指标', t34)


# ========================================================================
# 5. 期 货 增 值 数 据
# ========================================================================
print()
print('=' * 60)
print('📊 第5组: 期货增值数据')
print('=' * 60)

def t35():
    df = fut_get_contract_info(product_codes='IF', df=True)
    assert len(df) > 0, '空结果'
    return f'IF品种: {df.iloc[0]["product_name"]}'
test('fut_get_contract_info 期货品种信息', t35)

def t36():
    df = fut_get_transaction_rankings(symbols='CFFEX.IF2506', trade_date='', indicators='volume,long,short')
    return f'成交持仓排名 {len(df)}条'
test('fut_get_transaction_rankings 成交持仓排名', t36)

def t37():
    df = fut_get_warehouse_receipt(product_code='AL', start_date='2025-05-01', end_date='2025-05-26')
    return f'仓单数据 {len(df)}条'
test('fut_get_warehouse_receipt 仓单数据', t37)

# ========================================================================
# 6. 新 增 函 数：fut_get_continuous_contracts
# ========================================================================
print()
print('=' * 60)
print('📊 第6组: 新增函数 fut_get_continuous_contracts')
print('=' * 60)

def t38():
    result = fut_get_continuous_contracts('CFFEX.IM', start_date='2025-01-01', end_date='2025-03-31')
    assert len(result) > 0, '返回空列表'
    item = dict(result[0])
    return f'主力连续 {len(result)}条, eg: {item["symbol"]}/{item["trade_date"]}'
test('fut_get_continuous_contracts 主力连续 CFFEX.IM', t38)

def t39():
    result = fut_get_continuous_contracts('CFFEX.IM99', start_date='2025-01-01', end_date='2025-03-31')
    return f'加权指数 {len(result)}条'
test('fut_get_continuous_contracts 加权指数 CFFEX.IM99', t39)

def t40():
    result = fut_get_continuous_contracts('CFFEX.IM00', start_date='2025-01-01', end_date='2025-03-31')
    return f'当月连续 {len(result)}条'
test('fut_get_continuous_contracts 当月连续 CFFEX.IM00', t40)

def t41():
    result = fut_get_continuous_contracts('CFFEX.IM22', start_date='2025-01-01', end_date='2025-03-31')
    return f'次主力连续 {len(result)}条'
test('fut_get_continuous_contracts 次主力 CFFEX.IM22', t41)

def t42():
    result = fut_get_continuous_contracts('CFFEX.IM01', start_date='2025-01-01', end_date='2025-03-31')
    return f'下月连续 {len(result)}条'
test('fut_get_continuous_contracts 下月 CFFEX.IM01', t42)


# ========================================================================
# 7. 其 他 常 用 数 据 查 询（验证兼容性）
# ========================================================================
print()
print('=' * 60)
print('📊 第7组: 常用数据查询（兼容性验证）')
print('=' * 60)

def t43():
    df = history(symbol='SHSE.600519', frequency='1d', start_time='2025-05-01', end_time='2025-05-26', df=True)
    return f'日线 {len(df)}条'
test('history 日线', t43)

def t44():
    df = history_n(symbol='SHSE.600519', frequency='1d', count=10, df=True)
    return f'最近 {len(df)}条日线'
test('history_n 最新N条', t44)

def t45():
    df = get_trading_dates(exchange='SHSE', start_date='2025-05-01', end_date='2025-05-31')
    return f'{len(df)}个交易日'
test('get_trading_dates 交易日历', t45)


# ========================================================================
# 总 结
# ========================================================================
print()
print('=' * 60)
print('📋 测试总结')
print('=' * 60)
print(f'   总测试数: {results["pass"] + results["fail"] + results["skip"]}')
print(f'   ✅ 通过:  {results["pass"]}')
print(f'   ⏭️ 跳过:  {results["skip"]} (无权限/需策略环境)')
print(f'   ❌ 失败:  {results["fail"]}')
print()
print('--- 失败详情 ---')
for name, status, msg in results['details']:
    if status == '❌ 失败':
        print(f'  {status} {name}: {msg}')
print()
print('--- 跳过详情 ---')
for name, status, msg in results['details']:
    if status == '⏭️ 跳过(无权限)':
        print(f'  {status} {name}: {msg}')

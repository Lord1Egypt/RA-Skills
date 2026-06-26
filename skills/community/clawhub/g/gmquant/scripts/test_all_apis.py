"""
掘金量化 SDK API 全量测试脚本
测试所有非交易类 API（数据查询类，不需要策略 run 环境）

使用前：
1. 确保掘金终端已打开并登录
2. 将下面的 YOUR_TOKEN 替换为你的真实 token
   （掘金终端 -> 系统设置 -> 密钥管理）
"""

import sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

from gm.api import *
import traceback
from datetime import datetime, timedelta

# ============================
# !! 运行前请修改此 Token !!
# ============================
TOKEN = 'c2a347464c31056c84165dff766750fbf2ec67b4'

# 测试结果统计
results = []


def test(name, func):
    """统一测试执行 + 结果记录"""
    print(f'\n{"="*50}')
    print(f'[测试] {name}')
    try:
        result = func()
        status = 'PASS'
        if result is None:
            detail = '返回 None（可能无数据或连接问题）'
        elif hasattr(result, '__len__'):
            detail = f'返回 {type(result).__name__}，长度={len(result)}'
        else:
            detail = f'返回 {type(result).__name__}: {str(result)[:100]}'
        print(f'✅ {status}: {detail}')
    except Exception as e:
        status = 'FAIL'
        detail = str(e)[:200]
        print(f'❌ {status}: {detail}')
        traceback.print_exc()
    results.append({'name': name, 'status': status, 'detail': detail})


# ============================
# 初始化 Token
# ============================
print('\n' + '='*60)
print('掘金量化 SDK API 测试')
print('='*60)
set_token(TOKEN)
print(f'Token 已设置: {TOKEN[:8]}...')


# ----------------------------
# 1. 行情数据查询
# ----------------------------

def t_current():
    return current(symbols='SZSE.000001,SHSE.600000')

def t_history_daily():
    return history(symbol='SHSE.600000', frequency='1d',
                   start_time='2024-01-01', end_time='2024-01-31',
                   fields='open,high,low,close,volume,eob',
                   adjust=ADJUST_PREV, df=True)

def t_history_minute():
    return history(symbol='SHSE.600000', frequency='60s',
                   start_time='2024-01-15 09:30:00',
                   end_time='2024-01-15 11:30:00',
                   adjust=ADJUST_NONE, df=True)

def t_history_multi():
    return history(symbol='SHSE.600000,SZSE.000001', frequency='1d',
                   start_time='2024-01-01', end_time='2024-01-10',
                   df=True)

def t_history_n():
    return history_n(symbol='SHSE.600519', frequency='1d', count=20,
                     end_time='2024-12-31 15:30:00',
                     fields='symbol,open,close,eob',
                     adjust=ADJUST_PREV, df=True)

def t_history_tick():
    return history(symbol='SZSE.000001', frequency='tick',
                   start_time='2024-01-15 09:30:00',
                   end_time='2024-01-15 09:35:00',
                   df=True)

test('current - 当前行情快照', t_current)
test('history - 日线数据（前复权，DataFrame）', t_history_daily)
test('history - 分钟线数据', t_history_minute)
test('history - 多标的日线', t_history_multi)
test('history_n - 最新N条日线', t_history_n)
test('history - tick 数据', t_history_tick)


# ----------------------------
# 2. 标的信息查询
# ----------------------------

def t_get_symbol_infos_stock():
    return get_symbol_infos(sec_type1=1010,
                            symbols='SHSE.600000,SZSE.000001', df=True)

def t_get_symbol_infos_etf():
    return get_symbol_infos(sec_type1=1020, sec_type2=102001,
                            exchanges='SHSE', df=True)

def t_get_symbol_infos_cb():
    return get_symbol_infos(sec_type1=1030, sec_type2=103001, df=True)

def t_get_symbol_infos_fut():
    return get_symbol_infos(sec_type1=1040, sec_type2=104001, df=True)

def t_get_symbol_infos_opt():
    return get_symbol_infos(sec_type1=1050, sec_type2=105001,
                            exchanges='SHSE', df=True)

def t_get_symbol_infos_index():
    return get_symbol_infos(sec_type1=1060, sec_type2=106001, df=True)

def t_get_symbols_latest():
    return get_symbols(sec_type1=1010, sec_type2=101001,
                       skip_suspended=True, skip_st=True, df=True)

def t_get_symbols_date():
    return get_symbols(sec_type1=1010,
                       symbols='SHSE.600000,SZSE.000001',
                       trade_date='2024-01-15', df=True)

def t_get_history_symbol():
    return get_history_symbol(symbol='SHSE.600000',
                              start_date='2024-01-01',
                              end_date='2024-01-31', df=True)

test('get_symbol_infos - 指定股票基本信息', t_get_symbol_infos_stock)
test('get_symbol_infos - 上交所ETF列表', t_get_symbol_infos_etf)
test('get_symbol_infos - 可转债列表', t_get_symbol_infos_cb)
test('get_symbol_infos - 股指期货', t_get_symbol_infos_fut)
test('get_symbol_infos - 上交所股票期权', t_get_symbol_infos_opt)
test('get_symbol_infos - 股票指数', t_get_symbol_infos_index)
test('get_symbols - 全A股最新截面', t_get_symbols_latest)
test('get_symbols - 指定交易日', t_get_symbols_date)
test('get_history_symbol - 标的历史日度信息', t_get_history_symbol)


# ----------------------------
# 3. 交易日历
# ----------------------------

def t_get_trading_dates():
    return get_trading_dates('SHSE', '2024-01-01', '2024-12-31')

def t_get_prev_trading_date():
    return get_previous_trading_date('SHSE', '2024-01-15')

def t_get_next_trading_date():
    return get_next_trading_date('SHSE', '2024-01-15')

test('get_trading_dates - 全年交易日', t_get_trading_dates)
test('get_previous_trading_date - 上一交易日', t_get_prev_trading_date)
test('get_next_trading_date - 下一交易日', t_get_next_trading_date)


# ----------------------------
# 4. L2 行情（付费版）
# ----------------------------

def t_l2ticks():
    return get_history_l2ticks('SHSE.600519',
                               '2024-11-25 14:00:00',
                               '2024-11-25 14:10:00', df=True)

def t_l2bars():
    return get_history_l2bars('SHSE.600000', '60s',
                              '2024-11-25 09:30:00',
                              '2024-11-25 11:30:00', df=True)

def t_l2transactions():
    return get_history_l2transactions('SHSE.600000',
                                     '2024-11-25 14:00:00',
                                     '2024-11-25 14:10:00', df=True)

def t_l2orders():
    return get_history_l2orders('SZSE.000001',
                                '2024-11-25 14:00:00',
                                '2024-11-25 14:10:00', df=True)

def t_l2orders_queue():
    return get_history_l2orders_queue('SZSE.000001',
                                     '2024-11-25 14:00:00',
                                     '2024-11-25 14:10:00', df=True)

test('get_history_l2ticks - L2 历史Tick（付费）', t_l2ticks)
test('get_history_l2bars - L2 历史Bar（付费）', t_l2bars)
test('get_history_l2transactions - L2 逐笔成交（付费）', t_l2transactions)
test('get_history_l2orders - L2 逐笔委托（付费，深市）', t_l2orders)
test('get_history_l2orders_queue - L2 委托队列（付费）', t_l2orders_queue)


# ----------------------------
# 5. 账户查询（需要账户登录）
# ----------------------------

def t_get_cash():
    return get_cash()

def t_get_orders():
    return get_orders()

def t_get_execution_reports():
    return get_execution_reports()

def t_get_position():
    return get_position()

test('get_cash - 账户资金', t_get_cash)
test('get_orders - 委托列表', t_get_orders)
test('get_execution_reports - 成交回报', t_get_execution_reports)
test('get_position - 持仓列表', t_get_position)


# ----------------------------
# 汇总报告
# ----------------------------

print('\n\n' + '='*60)
print('📊 测试结果汇总')
print('='*60)

passed = [r for r in results if r['status'] == 'PASS']
failed = [r for r in results if r['status'] == 'FAIL']

print(f'总计: {len(results)} 个测试')
print(f'✅ 通过: {len(passed)}')
print(f'❌ 失败: {len(failed)}')

if failed:
    print('\n--- 失败详情 ---')
    for r in failed:
        print(f'  ❌ {r["name"]}')
        print(f'     原因: {r["detail"]}')

print('\n--- 完整结果 ---')
for r in results:
    icon = '✅' if r['status'] == 'PASS' else '❌'
    print(f'  {icon} {r["name"]}')
    print(f'     {r["detail"]}')

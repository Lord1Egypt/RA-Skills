"""
在 run() 策略环境内测试 get_cash 和 get_position
使用 MODE_BACKTEST 模式，不依赖实时行情
"""

import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

from gm.api import *

TOKEN = 'c2a347464c31056c84165dff766750fbf2ec67b4'

results = []


def init(context):
    """策略初始化"""
    schedule(schedule_func=run_test, date_rule='1d', time_rule='09:35:00')


def on_bar(context, bars):
    pass


def on_tick(context, tick):
    pass


def run_test(context):
    """定时执行账户 API 测试"""
    print('\n\n========== 策略环境内账户 API 测试 ==========')

    # --- get_cash ---
    try:
        cash = get_cash()
        print(f'[OK] get_cash: 返回 {type(cash).__name__}')
        if hasattr(cash, '__dict__') or isinstance(cash, dict):
            if isinstance(cash, dict):
                for k, v in list(cash.items())[:10]:
                    print(f'  {k} = {v}')
            else:
                for attr in ['account_id', 'available', 'nav', 'pnl', 'fpnl',
                             'margin', 'accumulated_return', 'daily_pnl']:
                    if hasattr(cash, attr):
                        print(f'  {attr} = {getattr(cash, attr)}')
        results.append({'name': 'get_cash - 账户资金 (策略环境)', 'status': 'PASS', 'detail': str(type(cash))})
    except Exception as e:
        print(f'[FAIL] get_cash: {e}')
        results.append({'name': 'get_cash - 账户资金 (策略环境)', 'status': 'FAIL', 'detail': str(e)[:200]})

    # --- get_position ---
    try:
        pos = get_position()
        print(f'[OK] get_position: 返回 {type(pos).__name__}, 长度={len(pos)}')
        if len(pos) > 0:
            p0 = pos[0]
            if isinstance(p0, dict):
                for k in list(p0.keys())[:8]:
                    print(f'  [{k}]={p0[k]}')
            else:
                for attr in ['symbol', 'side', 'position', 'available', 'vwap',
                             'pnl', 'fpnl', 'price']:
                    if hasattr(p0, attr):
                        print(f'  {attr}={getattr(p0, attr)}')
        else:
            print('  (空仓，无持仓)')
        results.append({'name': 'get_position - 持仓列表 (策略环境)', 'status': 'PASS', 'detail': f'{type(pos).__name__} len={len(pos)}'})
    except Exception as e:
        print(f'[FAIL] get_position: {e}')
        results.append({'name': 'get_position - 持仓列表 (策略环境)', 'status': 'FAIL', 'detail': str(e)[:200]})

    # --- get_orders ---
    try:
        orders = get_orders()
        print(f'[OK] get_orders: 返回 {type(orders).__name__}, 长度={len(orders)}')
        results.append({'name': 'get_orders (策略环境)', 'status': 'PASS', 'detail': f'len={len(orders)}'})
    except Exception as e:
        print(f'[FAIL] get_orders: {e}')
        results.append({'name': 'get_orders (策略环境)', 'status': 'FAIL', 'detail': str(e)[:200]})

    # --- get_execution_reports ---
    try:
        reports = get_execution_reports()
        print(f'[OK] get_execution_reports: 返回 {type(reports).__name__}, 长度={len(reports)}')
        results.append({'name': 'get_execution_reports (策略环境)', 'status': 'PASS', 'detail': f'len={len(reports)}'})
    except Exception as e:
        print(f'[FAIL] get_execution_reports: {e}')
        results.append({'name': 'get_execution_reports (策略环境)', 'status': 'FAIL', 'detail': str(e)[:200]})

    # --- 汇总 ---
    print('\n\n========== 汇总 ==========')
    passed = [r for r in results if r['status'] == 'PASS']
    failed = [r for r in results if r['status'] == 'FAIL']
    print(f'总计: {len(results)} | 通过: {len(passed)} | 失败: {len(failed)}')
    for r in results:
        icon = '[OK]' if r['status'] == 'PASS' else '[FAIL]'
        print(f'  {icon} {r["name"]}: {r["detail"]}')


if __name__ == '__main__':
    set_token(TOKEN)
    print(f'Token 已设置: {TOKEN[:8]}...')
    print('启动回测模式测试账户 API...')
    try:
        run(strategy_id='test_account_api_v2',
            filename='test_account_apis',
            mode=MODE_BACKTEST,
            token=TOKEN,
            backtest_start_time='2026-04-15 09:30:00',
            backtest_end_time='2026-04-17 15:30:00',
            backtest_initial_cash=1000000,
            backtest_adjust=ADJUST_PREV)
    except SystemExit:
        pass
    except Exception as e:
        print(f'运行异常: {e}')
        import traceback
        traceback.print_exc()

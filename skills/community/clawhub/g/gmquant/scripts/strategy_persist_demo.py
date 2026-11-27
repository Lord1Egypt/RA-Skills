# -*- coding: utf-8 -*-
"""在真实策略 run 场景下测试 persist_init / persist_set / persist_get"""
import sys, io, os
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

from gm.api import *

BUCKET = 'gmquant_run_test'
SYMBOLS = 'SHSE.600519'
FREQUENCY = '1d'


def init(context):
    # 非实时模式建议 is_async=False
    st = persist_init(BUCKET, is_async=False)
    print(f'[init] persist_init status={st}')

    # 初始化股票池（首次创建）
    old = persist_get('stock_pool')
    if old is None:
        persist_set('stock_pool', SYMBOLS)
        print(f'[init] 首次写入 stock_pool = {SYMBOLS}')
    else:
        print(f'[init] 已存在 stock_pool = {old}')

    # 初始化运行计数（演示跨 bar 状态持久化）
    cnt = persist_get('bar_count')
    context.bar_count = int(cnt) if cnt else 0
    print(f'[init] 恢复 bar_count = {context.bar_count}')

    # 对象读写演示
    meta = persist_get_obj('meta')
    if meta is None:
        persist_set_obj('meta', {'strategy': 'persist_run_test', 'bars': 0})
        print('[init] 首次写入 meta 对象')
    else:
        print(f'[init] 已有 meta = {meta}')

    subscribe(symbols=SYMBOLS, frequency=FREQUENCY, count=5)


def on_bar(context, bars):
    context.bar_count += 1
    # 每根 bar 更新计数
    st = persist_set('bar_count', str(context.bar_count))
    # 更新对象
    persist_set_obj('meta', {'strategy': 'persist_run_test', 'bars': context.bar_count})
    if context.bar_count <= 3 or context.bar_count % 5 == 0:
        keys = persist_get_all_keys()
        print(f'[on_bar] bar#{context.bar_count} set_status={st} keys={keys} '
              f'meta={persist_get_obj("meta")}')


def on_backtest_finished(context, indicator):
    print('\n=== 回测结束 ===')
    print('最终 bar_count =', persist_get('bar_count'))
    print('最终 meta =', persist_get_obj('meta'))
    print('bucket 内全部 key =', persist_get_all_keys())
    print('本地全部 bucket =', persist_get_all_buckets())
    print('\n>>> persist 在策略 run 场景下工作正常' )


if __name__ == '__main__':
    TOKEN = os.environ.get('GM_TOKEN', '')
    run(
        strategy_id='gmquant_persist_test',
        filename='strategy_persist_test',
        mode=MODE_BACKTEST,
        token=TOKEN,
        backtest_start_time='2026-11-16 09:00:00',
        backtest_end_time='2026-11-26 16:00:00',
        backtest_initial_cash=1000000,
        backtest_commission_ratio=0.00025,
        backtest_slippage_ratio=0.001,
        backtest_adjust=ADJUST_PREV,
    )

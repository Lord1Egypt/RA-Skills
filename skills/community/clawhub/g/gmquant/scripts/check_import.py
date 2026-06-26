"""
掘金量化 SDK - 快速连通性测试
无需 Token 即可验证 gm 包是否安装正确
"""
from gm.api import *
import inspect

print('='*50)
print('掘金量化 SDK 包导入测试')
print('='*50)

# 检查所有关键函数是否可导入
apis_to_check = [
    # 基础
    'set_token', 'run', 'stop', 'schedule',
    # 数据订阅
    'subscribe', 'unsubscribe', 'current',
    # 行情查询
    'history', 'history_n',
    # L2
    'get_history_l2ticks', 'get_history_l2bars',
    'get_history_l2transactions', 'get_history_l2orders',
    'get_history_l2orders_queue',
    # 标的信息
    'get_symbol_infos', 'get_symbols', 'get_history_symbol',
    # 交易日历
    'get_trading_dates', 'get_previous_trading_date', 'get_next_trading_date',
    # 下单
    'order_volume', 'order_value', 'order_percent',
    'order_target_volume', 'order_target_value', 'order_target_percent',
    'order_cancel', 'order_close_all',
    # 算法单
    'algo_order',
    # 账户查询
    'get_orders', 'get_execution_reports', 'get_cash', 'get_position',
    # 可转债
    'bond_convertible_call', 'bond_convertible_put', 'bond_convertible_put_cancel',
    # 日志
    'log', 'add_parameter',
    # 枚举
    'MODE_LIVE', 'MODE_BACKTEST',
    'ADJUST_NONE', 'ADJUST_PREV', 'ADJUST_POST',
    'OrderSide_Buy', 'OrderSide_Sell',
    'OrderType_Limit', 'OrderType_Market',
    'PositionEffect_Open', 'PositionEffect_Close',
    'PositionSide_Long', 'PositionSide_Short',
]

ok = []
missing = []

for name in apis_to_check:
    obj = globals().get(name)
    if obj is not None:
        ok.append(name)
    else:
        missing.append(name)

print(f'\n✅ 已找到 {len(ok)}/{len(apis_to_check)} 个 API')

if missing:
    print(f'\n❌ 缺失 {len(missing)} 个:')
    for m in missing:
        print(f'   - {m}')
else:
    print('\n🎉 所有 API 均可导入！')

print('\n--- 函数签名抽查 ---')
for fn_name in ['history', 'subscribe', 'get_symbol_infos', 'order_volume']:
    fn = globals().get(fn_name)
    if fn and callable(fn):
        try:
            sig = str(inspect.signature(fn))
            print(f'  {fn_name}{sig[:120]}')
        except (ValueError, TypeError):
            print(f'  {fn_name}: (内置函数，无法获取签名)')

print('\n✅ gm 包基础检测完成！')
print('如需运行完整 API 测试，请打开掘金终端并运行 test_all_apis.py')

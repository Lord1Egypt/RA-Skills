import MetaTrader5 as mt5
from datetime import datetime, timedelta

print("MT5 K线读取测试")
print("=" * 50)

# 1. 初始化
if not mt5.initialize():
    print("ERROR: MT5初始化失败")
    exit()
print("OK: MT5初始化成功")

# 2. 登录
if not mt5.login(277528870, "KKx88088@@@@", server="Exness-MT5Trial5"):
    print("ERROR: 登录失败")
    mt5.shutdown()
    exit()
print("OK: 登录成功")

# 3. 选择品种
symbol = "XAUUSDm"
if not mt5.symbol_select(symbol, True):
    print(f"ERROR: 无法选择品种 {symbol}")
    mt5.shutdown()
    exit()
print(f"OK: 品种 {symbol} 已选择")

print("\n" + "-" * 50)
print("测试1: 实时价格")
print("-" * 50)

tick = mt5.symbol_info_tick(symbol)
if tick:
    print(f"OK: 实时价格获取成功")
    print(f"  买价 (bid): {tick.bid:.3f}")
    print(f"  卖价 (ask): {tick.ask:.3f}")
    print(f"  最后价 (last): {tick.last}")
    print(f"  时间: {datetime.fromtimestamp(tick.time)}")
else:
    print(f"ERROR: 无法获取实时价格")

print("\n" + "-" * 50)
print("测试2: K线数据 (M1)")
print("-" * 50)

now = datetime.now()
rates = mt5.copy_rates_from(symbol, mt5.TIMEFRAME_M1, now, 10)

if rates is not None:
    print(f"OK: 获取到 {len(rates)} 根M1 K线")
    if len(rates) > 0:
        print("最近3根K线:")
        for i in range(min(3, len(rates))):
            idx = len(rates) - 1 - i
            rate = rates[idx]
            time_str = datetime.fromtimestamp(rate[0]).strftime('%Y-%m-%d %H:%M:%S')
            print(f"  [{i+1}] {time_str}")
            print(f"      开盘: {rate[1]:.3f}")
            print(f"      最高: {rate[2]:.3f}")
            print(f"      最低: {rate[3]:.3f}")
            print(f"      收盘: {rate[4]:.3f}")
            print(f"      成交量: {rate[5]}")
else:
    print("ERROR: 无法获取K线数据")

print("\n" + "-" * 50)
print("测试3: K线数据 (H1)")
print("-" * 50)

rates = mt5.copy_rates_from(symbol, mt5.TIMEFRAME_H1, now, 5)

if rates is not None:
    print(f"OK: 获取到 {len(rates)} 根H1 K线")
    if len(rates) > 0:
        print("最近2根H1 K线:")
        for i in range(min(2, len(rates))):
            idx = len(rates) - 1 - i
            rate = rates[idx]
            time_str = datetime.fromtimestamp(rate[0]).strftime('%Y-%m-%d %H:%M')
            print(f"  [{i+1}] {time_str}")
            print(f"      开盘: {rate[1]:.3f}")
            print(f"      收盘: {rate[4]:.3f}")
else:
    print("ERROR: 无法获取H1 K线数据")

print("\n" + "-" * 50)
print("测试4: K线数据 (D1)")
print("-" * 50)

rates = mt5.copy_rates_from(symbol, mt5.TIMEFRAME_D1, now, 3)

if rates is not None:
    print(f"OK: 获取到 {len(rates)} 根D1 K线")
    if len(rates) > 0:
        print("最近3根D1 K线:")
        for i in range(min(3, len(rates))):
            idx = len(rates) - 1 - i
            rate = rates[idx]
            time_str = datetime.fromtimestamp(rate[0]).strftime('%Y-%m-%d')
            print(f"  [{i+1}] {time_str}")
            print(f"      开盘: {rate[1]:.3f}")
            print(f"      收盘: {rate[4]:.3f}")
else:
    print("ERROR: 无法获取D1 K线数据")

print("\n" + "=" * 50)
print("测试完成")
mt5.shutdown()
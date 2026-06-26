import MetaTrader5 as mt5
from datetime import datetime

print("=" * 70)
print("MT5 账户快照")
print(f"时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
print("账户: 277528870 | 服务器: Exness-MT5Trial5")
print("品种: XAUUSDm")
print("=" * 70)

# 初始化
if not mt5.initialize():
    print("ERROR: MT5初始化失败")
    exit()

# 登录
if not mt5.login(277528870, "KKx88088@@@@", server="Exness-MT5Trial5"):
    print("ERROR: 登录失败")
    mt5.shutdown()
    exit()

# 选择品种
if not mt5.symbol_select("XAUUSDm", True):
    print("ERROR: 无法选择品种 XAUUSDm")
    mt5.shutdown()
    exit()

# 获取行情
tick = mt5.symbol_info_tick("XAUUSDm")
if tick:
    print("[市场] 实时行情")
    print(f"   买价: {tick.bid:.3f}")
    print(f"   卖价: {tick.ask:.3f}")
    print(f"   点差: {tick.ask - tick.bid:.3f}")
    print(f"   时间: {datetime.fromtimestamp(tick.time)}")
else:
    print("[市场] 无法获取行情")

# 账户信息
account = mt5.account_info()
if account:
    print("\n[账户] 账户状态")
    print(f"   余额: ${account.balance:.2f}")
    print(f"   净值: ${account.equity:.2f}")
    print(f"   可用保证金: ${account.margin_free:.2f}")
    print(f"   杠杆: 1:{account.leverage}")

# 持仓信息
positions = mt5.positions_get(symbol="XAUUSDm")
if positions:
    total_profit = sum(pos.profit for pos in positions)
    print(f"\n[持仓] 持仓 ({len(positions)}个)")
    for i, pos in enumerate(positions[:3]):  # 最多显示3个
        pos_type = "买入" if pos.type == 0 else "卖出"
        profit_symbol = "+" if pos.profit > 0 else ""
        print(f"   {i+1}. 订单 {pos.ticket} {pos_type} {pos.volume}手")
        print(f"      开仓价: {pos.price_open:.3f}")
        print(f"      现价: {pos.price_current:.3f}")
        print(f"      盈亏: {profit_symbol}${pos.profit:.2f}")
    
    if len(positions) > 3:
        print(f"   ... 还有 {len(positions) - 3} 个持仓")
    
    print(f"   总盈亏: ${total_profit:.2f}")
else:
    print("\n[持仓] 无持仓")

print("\n" + "=" * 70)
print("快速命令:")
print("   买入: /exec py -3.14 mt5_buy.py <手数> [价格] [止损] [止盈]")
print("   卖出: /exec py -3.14 mt5_sell.py <手数> [价格] [止损] [止盈]")
print("   平仓: /exec py -3.14 mt5_close_all.py")
print("   再次查看: /exec py -3.14 mt5_snapshot.py")
print("=" * 70)

mt5.shutdown()
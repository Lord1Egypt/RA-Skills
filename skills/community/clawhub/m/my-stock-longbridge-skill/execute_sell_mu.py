from stock_manager import manage_order
from longbridge.openapi import OrderSide

try:
    manage_order(action="sell", symbol="MU.US", quantity=1, side=OrderSide.Sell)
except Exception as e:
    print(f"执行失败: {e}")

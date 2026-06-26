from stock_manager import manage_order
from longbridge.openapi import OrderSide

try:
    manage_order(action="sell", symbol="NVDA.US", quantity=3, side=OrderSide.Sell, force=True)
except Exception as e:
    print(f"执行失败: {e}")

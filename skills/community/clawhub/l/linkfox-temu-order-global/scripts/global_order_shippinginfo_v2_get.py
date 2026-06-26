#!/usr/bin/env python3
"""bg.order.shippinginfo.v2.get — 订单收货地址查询 V2."""
import _global_order_script as m

if __name__ == "__main__":
    m.run_cli(
        "bg.order.shippinginfo.v2.get",
        "global_order_shippinginfo_v2_get.py '<JSON>'",
    )

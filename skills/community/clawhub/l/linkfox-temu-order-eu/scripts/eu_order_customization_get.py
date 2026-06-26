#!/usr/bin/env python3
"""bg.order.customization.get — 订单定制商品内容批量查询."""
import _eu_order_script as m

if __name__ == "__main__":
    m.run_cli(
        "bg.order.customization.get",
        "eu_order_customization_get.py '<JSON>'",
    )

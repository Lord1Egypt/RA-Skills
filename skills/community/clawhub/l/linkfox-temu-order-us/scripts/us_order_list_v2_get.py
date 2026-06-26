#!/usr/bin/env python3
"""bg.order.list.v2.get — 订单列表查询 V2."""
import _us_order_script as m

if __name__ == "__main__":
    m.run_cli(
        "bg.order.list.v2.get",
        "us_order_list_v2_get.py '<JSON>'",
    )

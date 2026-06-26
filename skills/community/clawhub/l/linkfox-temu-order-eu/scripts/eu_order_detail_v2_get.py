#!/usr/bin/env python3
"""bg.order.detail.v2.get — 订单详情查询 V2."""
import _eu_order_script as m

if __name__ == "__main__":
    m.run_cli(
        "bg.order.detail.v2.get",
        "eu_order_detail_v2_get.py '<JSON>'",
    )

#!/usr/bin/env python3
"""bg.order.combinedshipment.list.get — 可合并发货订单组列表."""
import _eu_order_script as m

if __name__ == "__main__":
    m.run_cli(
        "bg.order.combinedshipment.list.get",
        "eu_order_combinedshipment_list_get.py '<JSON>'",
    )

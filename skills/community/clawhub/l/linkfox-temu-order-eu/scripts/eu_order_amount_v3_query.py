#!/usr/bin/env python3
"""temu.order.amount.v3.query — 订单金额查询 V3."""
import _eu_order_script as m

if __name__ == "__main__":
    m.run_cli(
        "temu.order.amount.v3.query",
        "eu_order_amount_v3_query.py '<JSON>'",
    )

#!/usr/bin/env python3
"""bg.order.amount.query — 订单金额/供货价查询（自研 ERP）."""
import _global_order_script as m

if __name__ == "__main__":
    m.run_cli(
        "bg.order.amount.query",
        "global_order_amount_query.py '<JSON>'",
    )

#!/usr/bin/env python3
"""temu.order.cancel.outofstock.apply — 缺货取消申请."""
import _eu_cancel_order_script as m

if __name__ == "__main__":
    m.run_cli(
        "temu.order.cancel.outofstock.apply",
        "eu_seller_cancel_order_cancel_outofstock_apply.py '<JSON>'",
    )

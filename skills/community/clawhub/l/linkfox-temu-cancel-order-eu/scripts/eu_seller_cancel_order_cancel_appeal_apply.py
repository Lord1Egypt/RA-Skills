#!/usr/bin/env python3
"""temu.order.cancel.appeal.apply — 卖家发起取消申请."""
import _eu_cancel_order_script as m

if __name__ == "__main__":
    m.run_cli(
        "temu.order.cancel.appeal.apply",
        "eu_seller_cancel_order_cancel_appeal_apply.py '<JSON>'",
    )

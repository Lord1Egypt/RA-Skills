#!/usr/bin/env python3
"""bg.aftersales.cancel.agree — 同意取消订单."""
import _global_cancel_order_script as m

if __name__ == "__main__":
    m.run_cli(
        "bg.aftersales.cancel.agree",
        "global_cancel_aftersales_cancel_agree.py '<JSON>'",
    )

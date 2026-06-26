#!/usr/bin/env python3
"""bg.aftersales.parentreturnorder.get — 父退货物流信息."""
import _global_returns_refunds_script as m

if __name__ == "__main__":
    m.run_cli(
        "bg.aftersales.parentreturnorder.get",
        "global_returns_refunds_aftersales_parentreturnorder_get.py '<JSON>'",
    )

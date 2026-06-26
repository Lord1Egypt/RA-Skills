#!/usr/bin/env python3
"""temu.aftersales.returnlabel.prepare.get — 退货面单准备信息."""
import _eu_returns_refunds_script as m

if __name__ == "__main__":
    m.run_cli(
        "temu.aftersales.returnlabel.prepare.get",
        "eu_returns_refunds_aftersales_returnlabel_prepare_get.py '<JSON>'",
    )

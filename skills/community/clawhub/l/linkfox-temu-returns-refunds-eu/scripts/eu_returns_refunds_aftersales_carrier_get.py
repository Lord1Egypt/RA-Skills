#!/usr/bin/env python3
"""temu.aftersales.carrier.get — 承运商列表."""
import _eu_returns_refunds_script as m

if __name__ == "__main__":
    m.run_cli(
        "temu.aftersales.carrier.get",
        "eu_returns_refunds_aftersales_carrier_get.py '<JSON>'",
    )

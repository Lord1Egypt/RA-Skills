#!/usr/bin/env python3
"""temu.aftersales.returnaddress.get — 退货地址查询."""
import _us_returns_refunds_script as m

if __name__ == "__main__":
    m.run_cli(
        "temu.aftersales.returnaddress.get",
        "us_returns_refunds_aftersales_returnaddress_get.py '<JSON>'",
    )

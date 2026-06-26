#!/usr/bin/env python3
"""bg.aftersales.aftersales.list.get — 子售后单列表查询."""
import _us_returns_refunds_script as m

if __name__ == "__main__":
    m.run_cli(
        "bg.aftersales.aftersales.list.get",
        "us_returns_refunds_aftersales_aftersales_list_get.py '<JSON>'",
    )

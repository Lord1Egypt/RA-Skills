#!/usr/bin/env python3
"""bg.aftersales.cancel.list.get — 取消订单售后列表查询."""
import _global_cancel_order_script as m

if __name__ == "__main__":
    m.run_cli(
        "bg.aftersales.cancel.list.get",
        "global_cancel_aftersales_cancel_list_get.py '<JSON>'",
    )

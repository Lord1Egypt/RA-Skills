#!/usr/bin/env python3
"""bg.logistics.warehouse.list.get — 店铺仓库列表（含购标能力筛选）."""
import _us_fulfillment_script as m

if __name__ == "__main__":
    m.run_cli(
        "bg.logistics.warehouse.list.get",
        "us_buy_shipping_logistics_warehouse_list_get.py '<JSON>'",
    )

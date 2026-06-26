#!/usr/bin/env python3
"""temu.logistics.shiplogisticstype.get — 在线发货物流类型列表（购标前）."""
import _eu_fulfillment_script as m

if __name__ == "__main__":
    m.run_cli(
        "temu.logistics.shiplogisticstype.get",
        "eu_buy_shipping_logistics_shiplogisticstype_get.py '<JSON>'",
    )

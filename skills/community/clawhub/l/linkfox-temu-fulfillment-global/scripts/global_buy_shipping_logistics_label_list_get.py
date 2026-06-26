#!/usr/bin/env python3
"""temu.logistics.label.list.get — 查询 Temu 平台购标面单列表."""
import _global_fulfillment_script as m

if __name__ == "__main__":
    m.run_cli(
        "temu.logistics.label.list.get",
        "global_buy_shipping_logistics_label_list_get.py '<JSON>'",
    )

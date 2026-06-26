#!/usr/bin/env python3
"""temu.logistics.scanform.create — 按校验条件创建 Scan Form（物流扫描单）."""
import _eu_fulfillment_script as m

if __name__ == "__main__":
    m.run_cli(
        "temu.logistics.scanform.create",
        "eu_buy_shipping_logistics_scanform_create.py '<JSON>'",
    )

#!/usr/bin/env python3
"""temu.logistics.scanform.get — 查询 Scan Form 详情（状态、筛选分页）."""
import _us_fulfillment_script as m

if __name__ == "__main__":
    m.run_cli(
        "temu.logistics.scanform.get",
        "us_buy_shipping_logistics_scanform_get.py '<JSON>'",
    )

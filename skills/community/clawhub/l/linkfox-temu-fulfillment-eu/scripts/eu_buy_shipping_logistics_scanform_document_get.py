#!/usr/bin/env python3
"""temu.logistics.scanform.document.get — 获取 Scan Form 文档 URL."""
import _eu_fulfillment_script as m

if __name__ == "__main__":
    m.run_cli(
        "temu.logistics.scanform.document.get",
        "eu_buy_shipping_logistics_scanform_document_get.py '<JSON>'",
    )

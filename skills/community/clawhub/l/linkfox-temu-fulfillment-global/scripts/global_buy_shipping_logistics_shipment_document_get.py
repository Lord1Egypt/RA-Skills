#!/usr/bin/env python3
"""bg.logistics.shipment.document.get — 获取购标成功包裹的面单/运单文档 URL."""
import _global_fulfillment_script as m

if __name__ == "__main__":
    m.run_cli(
        "bg.logistics.shipment.document.get",
        "global_buy_shipping_logistics_shipment_document_get.py '<JSON>'",
    )

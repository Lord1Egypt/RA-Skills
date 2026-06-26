#!/usr/bin/env python3
"""bg.local.goods.priceorder.change.sku.price — 白名单商家批量修改 SKU 基础价."""
import _us_price_script as m

if __name__ == "__main__":
    m.run_cli(
        "bg.local.goods.priceorder.change.sku.price",
        "us_price_priceorder_change_sku_price.py '<JSON>'",
    )

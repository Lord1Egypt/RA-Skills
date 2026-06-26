#!/usr/bin/env python3
"""temu.local.goods.sku.stock.query — SKU库存查询."""
import _us_product_script as m

if __name__ == "__main__":
    m.run_cli("temu.local.goods.sku.stock.query", "us_manage_sku_stock_query.py '<JSON>'")

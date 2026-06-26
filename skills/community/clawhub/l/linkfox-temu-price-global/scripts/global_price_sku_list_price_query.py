#!/usr/bin/env python3
"""bg.local.goods.sku.list.price.query — SKU 供货价列表查询."""
import _global_price_script as m

if __name__ == "__main__":
    m.run_cli(
        "bg.local.goods.sku.list.price.query",
        "global_price_sku_list_price_query.py \'<JSON>\'",
    )

#!/usr/bin/env python3
"""bg.goods.category.mapping — 商品类目映射（名称推荐类目）."""
import _us_product_script as m

if __name__ == "__main__":
    m.run_cli(
        "bg.goods.category.mapping",
        "us_goods_category_mapping.py '<JSON with goodsName, goodsNameEn>'",
    )

#!/usr/bin/env python3
"""temu.local.product.variation.get — 获取商品规格（Partner US V2）."""
import _us_product_script as m

if __name__ == "__main__":
    m.run_cli("temu.local.product.variation.get", "us_goods_variation.py '<JSON>'")

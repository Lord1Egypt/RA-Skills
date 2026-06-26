#!/usr/bin/env python3
"""temu.local.goods.v2.add — 发布商品."""
import _us_product_script as m

if __name__ == "__main__":
    m.run_cli("temu.local.goods.v2.add", "us_goods_add.py '<JSON with goods payload>'")

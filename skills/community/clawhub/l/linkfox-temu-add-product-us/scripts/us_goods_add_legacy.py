#!/usr/bin/env python3
"""temu.goods.add — 发布商品（半托管/跨境发品，非 V2）."""
import _us_product_script as m

if __name__ == "__main__":
    m.run_cli("temu.goods.add", "us_goods_add_legacy.py '<JSON with goods payload>'")

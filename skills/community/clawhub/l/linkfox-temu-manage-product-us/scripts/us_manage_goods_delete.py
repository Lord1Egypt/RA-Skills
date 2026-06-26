#!/usr/bin/env python3
"""temu.local.goods.delete — 删除商品."""
import _us_product_script as m

if __name__ == "__main__":
    m.run_cli("temu.local.goods.delete", "us_manage_goods_delete.py '<JSON>'")

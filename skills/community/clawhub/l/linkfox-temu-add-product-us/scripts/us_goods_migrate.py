#!/usr/bin/env python3
"""temu.goods.migrate — 半托管搬运同主体全托管货品."""
import _us_product_script as m

if __name__ == "__main__":
    m.run_cli("temu.goods.migrate", "us_goods_migrate.py '<JSON>'")

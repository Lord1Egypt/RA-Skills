#!/usr/bin/env python3
"""temu.local.goods.image.v2.upload — 商品图片上传 V2（Partner US）."""
import _us_product_script as m

if __name__ == "__main__":
    m.run_cli("temu.local.goods.image.v2.upload", "us_goods_image_upload.py '<JSON>'")

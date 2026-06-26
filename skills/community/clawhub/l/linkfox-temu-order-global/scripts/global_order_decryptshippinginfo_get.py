#!/usr/bin/env python3
"""bg.order.decryptshippinginfo.get — 订单敏感收货地址解密查询."""
import _global_order_script as m

if __name__ == "__main__":
    m.run_cli(
        "bg.order.decryptshippinginfo.get",
        "global_order_decryptshippinginfo_get.py '<JSON>'",
    )

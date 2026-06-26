#!/usr/bin/env python3
"""temu.order.cancel.outofstock.result.get — 查询缺货取消审核结果."""
import _global_cancel_order_script as m

if __name__ == "__main__":
    m.run_cli(
        "temu.order.cancel.outofstock.result.get",
        "global_seller_cancel_order_cancel_outofstock_result_get.py '<JSON>'",
    )

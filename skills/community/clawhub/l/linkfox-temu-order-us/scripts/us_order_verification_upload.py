#!/usr/bin/env python3
"""temu.local.order.verification.upload — 订单 SN/IMEI 或二手鉴真信息上传."""
import _us_order_script as m

if __name__ == "__main__":
    m.run_cli(
        "temu.local.order.verification.upload",
        "us_order_verification_upload.py '<JSON>'",
    )

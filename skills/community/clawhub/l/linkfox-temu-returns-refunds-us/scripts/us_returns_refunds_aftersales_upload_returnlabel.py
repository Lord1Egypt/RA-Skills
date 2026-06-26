#!/usr/bin/env python3
"""temu.aftersales.upload.returnlabel — 上传退货面单."""
import _us_returns_refunds_script as m

if __name__ == "__main__":
    m.run_cli(
        "temu.aftersales.upload.returnlabel",
        "us_returns_refunds_aftersales_upload_returnlabel.py '<JSON>'",
    )

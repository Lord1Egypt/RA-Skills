#!/usr/bin/env python3
"""temu.pay.tax.merchant.upload.invoice — 商家上传发票."""
import _eu_tax_script as m

if __name__ == "__main__":
    m.run_cli(
        "temu.pay.tax.merchant.upload.invoice",
        "eu_tax_merchant_upload_invoice.py \'<JSON>\'",
    )

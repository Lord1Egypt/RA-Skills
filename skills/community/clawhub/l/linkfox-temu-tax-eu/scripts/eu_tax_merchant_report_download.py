#!/usr/bin/env python3
"""temu.pay.tax.merchant.report.download — 商家税务报表下载."""
import _eu_tax_script as m

if __name__ == "__main__":
    m.run_cli(
        "temu.pay.tax.merchant.report.download",
        "eu_tax_merchant_report_download.py \'<JSON>\'",
    )

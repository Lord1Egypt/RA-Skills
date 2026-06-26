#!/usr/bin/env python3
"""temu.pay.tax.invoice.info.query — 发票信息查询."""
import _eu_tax_script as m

if __name__ == "__main__":
    m.run_cli(
        "temu.pay.tax.invoice.info.query",
        "eu_tax_invoice_info_query.py \'<JSON>\'",
    )

#!/usr/bin/env python3
"""temu.pay.tax.invoice.detail.query — 发票明细查询."""
import _eu_tax_script as m

if __name__ == "__main__":
    m.run_cli(
        "temu.pay.tax.invoice.detail.query",
        "eu_tax_invoice_detail_query.py \'<JSON>\'",
    )

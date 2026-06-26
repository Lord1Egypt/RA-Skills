#!/usr/bin/env python3
"""temu.pay.tax.invoice.pdf.download — 发票 PDF 下载."""
import _eu_tax_script as m

if __name__ == "__main__":
    m.run_cli(
        "temu.pay.tax.invoice.pdf.download",
        "eu_tax_invoice_pdf_download.py \'<JSON>\'",
    )

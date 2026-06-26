#!/usr/bin/env python3
"""temu.pay.tax.apply.export.report — 申请导出税务报表."""
import _eu_tax_script as m

if __name__ == "__main__":
    m.run_cli(
        "temu.pay.tax.apply.export.report",
        "eu_tax_apply_export_report.py \'<JSON>\'",
    )

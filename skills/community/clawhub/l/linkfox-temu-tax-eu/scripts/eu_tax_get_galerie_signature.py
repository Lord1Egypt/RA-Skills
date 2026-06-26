#!/usr/bin/env python3
"""temu.pay.tax.get.galerie.signature — 获取 Galerie 签名."""
import _eu_tax_script as m

if __name__ == "__main__":
    m.run_cli(
        "temu.pay.tax.get.galerie.signature",
        "eu_tax_get_galerie_signature.py \'<JSON>\'",
    )

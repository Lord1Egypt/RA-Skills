#!/usr/bin/env python3
"""bg.arbok.open.cert.uploadProductCert — 上传商品资质."""
import _global_compliance_script as m

if __name__ == "__main__":
    m.run_cli(
        "bg.arbok.open.cert.uploadProductCert",
        "global_compliance_arbok_cert_upload_product_cert.py \'<JSON>\'",
    )

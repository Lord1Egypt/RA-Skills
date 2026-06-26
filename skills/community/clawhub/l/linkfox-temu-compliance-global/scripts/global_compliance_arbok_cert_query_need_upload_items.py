#!/usr/bin/env python3
"""bg.arbok.open.cert.queryNeedUploadItems — 待上传资质项查询."""
import _global_compliance_script as m

if __name__ == "__main__":
    m.run_cli(
        "bg.arbok.open.cert.queryNeedUploadItems",
        "global_compliance_arbok_cert_query_need_upload_items.py \'<JSON>\'",
    )

#!/usr/bin/env python3
"""bg.compliance.metadata.get — 合规模板元数据查询."""
import _global_compliance_script as m

if __name__ == "__main__":
    m.run_cli(
        "bg.compliance.metadata.get",
        "global_compliance_metadata_get.py \'<JSON>\'",
    )

#!/usr/bin/env python3
"""temu.searchrec.ad.log.query — 广告操作日志查询."""
import _global_ads_script as m

if __name__ == "__main__":
    m.run_cli(
        "temu.searchrec.ad.log.query",
        "global_ads_searchrec_ad_log_query.py '<JSON>'",
    )

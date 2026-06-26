#!/usr/bin/env python3
"""temu.searchrec.ad.create — 创建广告."""
import _us_ads_script as m

if __name__ == "__main__":
    m.run_cli(
        "temu.searchrec.ad.create",
        "us_ads_searchrec_ad_create.py '<JSON>'",
    )

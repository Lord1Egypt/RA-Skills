#!/usr/bin/env python3
"""temu.searchrec.ad.roas.pred — 广告 ROAS 预测."""
import _us_ads_script as m

if __name__ == "__main__":
    m.run_cli(
        "temu.searchrec.ad.roas.pred",
        "us_ads_searchrec_ad_roas_pred.py '<JSON>'",
    )

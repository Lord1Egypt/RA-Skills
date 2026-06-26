#!/usr/bin/env python3
"""temu.track.trackinginfo.get — 物流轨迹详情查询."""
import _global_fulfillment_script as m

if __name__ == "__main__":
    m.run_cli(
        "temu.track.trackinginfo.get",
        "global_tracking_track_trackinginfo_get.py '<JSON>'",
    )

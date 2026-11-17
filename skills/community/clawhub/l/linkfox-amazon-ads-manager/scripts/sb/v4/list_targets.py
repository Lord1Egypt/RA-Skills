#!/usr/bin/env python3
"""List SB targets for V4 campaigns.

Required JSON: profileId, region.
Accepts Amazon-native payload.filters, or top-level campaignIdFilter /
adGroupIdFilter / stateFilter / targetIdFilter / creativeTypeFilter.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from _sb_common import run_post_token_list  # noqa: E402

if __name__ == "__main__":
    run_post_token_list(
        __doc__,
        path="sb/targets/list",
        content_type="application/vnd.sblisttargets.v3.2+json",
        response_key="targets",
        api_version="V4",
        resource_version="V3.2_SHARED_TARGETING",
        map_target_filters=True,
    )

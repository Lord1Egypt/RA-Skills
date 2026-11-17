#!/usr/bin/env python3
"""Create SB V3 Legacy campaigns.

Required JSON: profileId, region, payload (Amazon-native request body).
V3 entry points reject an explicitly identified MULTI_AD_GROUP campaign.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from _sb_common import run_mutation  # noqa: E402

if __name__ == "__main__":
    run_mutation(
        __doc__,
        path="sb/campaigns",
        method="POST",
        content_type="application/vnd.sbcampaign.v3+json",
        api_version="V3",
        resource_version="V3",
    )

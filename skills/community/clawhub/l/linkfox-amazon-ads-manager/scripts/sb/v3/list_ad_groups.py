#!/usr/bin/env python3
"""List SB V3 Legacy ad groups.

Required JSON: profileId, region. Optional: filters, fetchAll, maxResults.
V3 entry points are for LEGACY campaigns only; they never auto-fallback from V4.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from _sb_common import run_get_offset_list  # noqa: E402

if __name__ == "__main__":
    run_get_offset_list(
        __doc__,
        path="sb/adGroups",
        response_key="adGroups",
        query_keys=['adGroupIdFilter', 'campaignIdFilter', 'stateFilter', 'nameFilter', 'creativeType'],
        api_version="V3",
        resource_version="V3",
    )

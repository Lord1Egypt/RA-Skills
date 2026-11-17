#!/usr/bin/env python3
"""List SB keywords for V3 campaigns.

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
        path="sb/keywords",
        response_key="keywords",
        query_keys=['keywordIdFilter', 'adGroupIdFilter', 'campaignIdFilter', 'stateFilter', 'matchTypeFilter', 'keywordText', 'creativeType', 'locale'],
        api_version="V3",
        resource_version="V3_SHARED_TARGETING",
    )

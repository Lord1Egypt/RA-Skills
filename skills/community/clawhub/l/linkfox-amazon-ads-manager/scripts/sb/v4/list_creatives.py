#!/usr/bin/env python3
"""List SB V4 ad creatives.

Required JSON: profileId, region. Pass Amazon-native list body in payload;
filters/maxResults/nextToken are also accepted at the top level.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from _sb_common import run_post_token_list  # noqa: E402

if __name__ == "__main__":
    run_post_token_list(
        __doc__,
        path="sb/ads/creatives/list",
        content_type="application/vnd.sbadcreativeresource.v4+json",
        response_key="creatives",
        api_version="V4",
        resource_version="V4",
    )

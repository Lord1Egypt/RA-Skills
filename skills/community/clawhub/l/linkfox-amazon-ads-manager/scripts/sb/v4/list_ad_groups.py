#!/usr/bin/env python3
"""List Sponsored Brands V4 ad groups."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from _sb_common import build_filter_body, parse_argv_params, run_post_token_list  # noqa: E402

if __name__ == "__main__":
    params = parse_argv_params(__doc__)
    body = build_filter_body(
        params,
        ["adGroupIdFilter", "campaignIdFilter", "stateFilter", "nameFilter"],
    )
    body.update(params.get("payload") or {})
    run_post_token_list(
        __doc__,
        path="sb/v4/adGroups/list",
        content_type="application/vnd.sbadgroupresource.v4+json",
        response_key="adGroups",
        api_version="V4",
        resource_version="V4",
        params=params,
        request_body=body,
    )

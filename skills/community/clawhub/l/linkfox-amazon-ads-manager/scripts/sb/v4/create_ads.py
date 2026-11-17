#!/usr/bin/env python3
"""Create Sponsored Brands V4 ads.

Required JSON: profileId, region, adType, payload.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from _sb_common import emit_structured_error, parse_argv_params, run_mutation  # noqa: E402

if __name__ == "__main__":
    params = parse_argv_params(__doc__)
    ad_type = params.get("adType")
    allowed = {
        "autoCollection",
        "manualCollection",
        "brandVideo",
        "video",
        "productCollection",
        "productCollectionExtended",
        "storeSpotlight",
    }
    if ad_type not in allowed:
        emit_structured_error(
            code="SB_INVALID_AD_TYPE",
            message=f"adType must be one of: {', '.join(sorted(allowed))}",
            extra={"adType": ad_type, "apiVersion": "V4"},
        )
    run_mutation(
        __doc__,
        path=f"sb/v4/ads/{ad_type}",
        method="POST",
        content_type="application/vnd.sbadresource.v4+json",
        api_version="V4",
        resource_version="V4",
        params=params,
    )

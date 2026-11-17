#!/usr/bin/env python3
"""Create a new creative version for an SB V4 ad.

Required JSON: profileId, region, creativeType, payload.
creativeType: productCollection | productCollectionExtended | storeSpotlight |
video | brandVideo
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from _sb_common import emit_structured_error, parse_argv_params, run_mutation  # noqa: E402

if __name__ == "__main__":
    params = parse_argv_params(__doc__)
    creative_type = params.get("creativeType")
    allowed = {
        "productCollection",
        "productCollectionExtended",
        "storeSpotlight",
        "video",
        "brandVideo",
    }
    if creative_type not in allowed:
        emit_structured_error(
            code="SB_INVALID_CREATIVE_TYPE",
            message=f"creativeType must be one of: {', '.join(sorted(allowed))}",
            extra={"creativeType": creative_type, "apiVersion": "V4"},
        )
    run_mutation(
        __doc__,
        path=f"sb/ads/creatives/{creative_type}",
        method="POST",
        content_type="application/vnd.sbadcreativeresource.v4+json",
        api_version="V4",
        resource_version="V4",
        params=params,
    )

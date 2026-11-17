#!/usr/bin/env python3
"""POST Sponsored Brands V4 campaigns; payload is Amazon-native."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from _sb_common import run_mutation  # noqa: E402

if __name__ == "__main__":
    run_mutation(
        __doc__,
        path="sb/v4/campaigns",
        method="POST",
        content_type="application/vnd.sbcampaignresource.v4+json",
        api_version="V4",
        resource_version="V4",
    )

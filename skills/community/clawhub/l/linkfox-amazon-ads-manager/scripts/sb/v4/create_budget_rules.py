#!/usr/bin/env python3
"""Create Sponsored Brands budget rules for V4 campaign management."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from _sb_common import run_mutation  # noqa: E402

if __name__ == "__main__":
    run_mutation(
        __doc__,
        path="sb/budgetRules",
        method="POST",
        content_type="application/json",
        api_version="V4",
        resource_version="SHARED",
    )

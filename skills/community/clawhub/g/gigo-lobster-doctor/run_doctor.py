#!/usr/bin/env python3

from __future__ import annotations

from entrypoint_helpers import run_profile


if __name__ == "__main__":
    raise SystemExit(
        run_profile(
            active_skill="gigo-lobster-doctor",
            default_args=["--auto-yes", "--doctor"],
            output_slug="gigo-lobster-doctor",
        )
    )

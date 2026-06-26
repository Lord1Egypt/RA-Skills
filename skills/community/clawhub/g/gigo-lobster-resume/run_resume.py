#!/usr/bin/env python3

from __future__ import annotations

from entrypoint_helpers import run_profile


if __name__ == "__main__":
    raise SystemExit(
        run_profile(
            active_skill="gigo-lobster-resume",
            default_args=["--auto-yes", "--upload-mode", "upload", "--checkpoint-policy", "resume"],
            output_slug="gigo-lobster-taster",
        )
    )

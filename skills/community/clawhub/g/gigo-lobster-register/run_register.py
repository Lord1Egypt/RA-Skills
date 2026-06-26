#!/usr/bin/env python3

from __future__ import annotations

from entrypoint_helpers import run_profile


if __name__ == "__main__":
    raise SystemExit(
        run_profile(
            active_skill="gigo-lobster-register",
            default_args=["--auto-yes", "--upload-mode", "register", "--checkpoint-policy", "fresh"],
            output_slug="gigo-lobster-register",
        )
    )

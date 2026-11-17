#!/usr/bin/env python3
"""Report whether an already-installed, offline OMR candidate is detected.

This probe never installs software, starts an OMR process, uploads a score, or
changes a file.  It exists so a host can select the correct recognition path
before it promises a PDF/image workflow.
"""

from __future__ import annotations

import argparse
import json
import shutil

from optional_omr_discovery import find_audiveris, find_oemer


def installed_audiveris() -> tuple[str | None, str | None]:
    """Find a command-line install or the standard macOS app bundle, read-only."""
    return find_audiveris()


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--format", choices=("json", "text"), default="json")
    args = parser.parse_args()
    audiveris, install_kind = installed_audiveris()
    oemer, oemer_install_kind = find_oemer()
    java = shutil.which("java")
    # File discovery proves only that an executable exists. It does not prove
    # that its Java/OCR runtime can process this particular machine's score.
    # Conflating those two states previously let a user choose an apparently
    # available route which then failed only after work had started.
    payload = {
        "offline_omr_detected": bool(audiveris),
        "offline_omr_runtime_verified": False,
        "offline_omr_available": bool(audiveris),
        "candidate": "Audiveris" if audiveris else None,
        "executable": audiveris,
        "installation_kind": install_kind,
        "java_available": bool(java),
        "mode": "optional-candidate-only-unprobed" if audiveris else "visual-review-only",
        "next_action": (
            "Audiveris was detected but has not been runtime-verified. If the user permits, try one local candidate export; "
            "only a completed export establishes that this machine can use the optional route."
            if audiveris else
            "No local Audiveris install was found. Continue with the visual-facts and local-review workflow; "
            "do not install it automatically or use a cloud service."
        ),
        "candidates": [
            {
                "name": "Audiveris", "detected": bool(audiveris), "executable": audiveris,
                "installation_kind": install_kind, "accepts": ["pdf", "image"],
                "license": "AGPL-3.0 external application", "default": False,
            },
            {
                "name": "Oemer", "detected": bool(oemer), "executable": oemer,
                "installation_kind": oemer_install_kind, "accepts": ["image"],
                "license": "MIT code; separately installed model runtime", "default": False,
                "note": "Use only after the user separately installs it; first use may download model files.",
            },
            {
                "name": "Visual review", "detected": True, "accepts": ["pdf", "image"],
                "license": "no external runtime", "default": True,
            },
        ],
    }
    if args.format == "text":
        print(payload["next_action"])
    else:
        print(json.dumps(payload, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

#!/usr/bin/env python3
from __future__ import annotations

import argparse
from pathlib import Path

from common import PROFILE_DIR, ValidationError, load_application_content, load_json, write_text


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Generate plain-text application from application_content.json schema_version 2."
    )
    parser.add_argument("--content", required=True, type=Path)
    parser.add_argument("--output", required=True, type=Path)
    parser.add_argument("--profile", type=Path, default=PROFILE_DIR / "master_profile.json")
    args = parser.parse_args()

    try:
        profile = load_json(args.profile)
        raw = load_json(args.content)
        legacy_kind = None if isinstance(raw, dict) and raw.get("schema_version") == 2 else "plain_text"
        content = load_application_content(args.content, profile, legacy_kind=legacy_kind)
        plain = content["plain_text"]
        parts = [plain["subject"], plain["salutation"], *plain["paragraphs"], plain["closing"], plain["signatory"]]
        write_text(args.output, "\n\n".join(part.strip() for part in parts) + "\n")
    except (OSError, ValidationError) as error:
        parser.error(str(error))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

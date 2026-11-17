#!/usr/bin/env python3
"""Convert the documented v1 cover-letter/plain-text inputs into the v2 content model."""
from __future__ import annotations

import argparse
import json
from pathlib import Path

from common import (
    ValidationError,
    legacy_cover_to_content,
    legacy_plain_to_content,
    load_json,
    write_text,
)


def main() -> int:
    parser = argparse.ArgumentParser(description="Create application_content.json schema_version 2 from v1 inputs.")
    parser.add_argument("--cover-letter", type=Path, help="Legacy cover_letter.json")
    parser.add_argument("--indeed-text", type=Path, help="Legacy indeed_text.json")
    parser.add_argument("--job", type=Path, help="job.json (required when no cover letter supplies a company)")
    parser.add_argument("--profile", required=True, type=Path, help="master_profile.json")
    parser.add_argument("--output", required=True, type=Path)
    args = parser.parse_args()
    if not args.cover_letter and not args.indeed_text:
        parser.error("at least one of --cover-letter or --indeed-text is required")

    try:
        profile = load_json(args.profile)
        job = load_json(args.job) if args.job else {}
        if not isinstance(profile, dict):
            raise ValidationError("profile must contain a JSON object")
        if not isinstance(job, dict):
            raise ValidationError("job must contain a JSON object")
        cover_content = legacy_cover_to_content(load_json(args.cover_letter), profile, job) if args.cover_letter else None
        if args.indeed_text:
            if not cover_content and not job.get("company"):
                raise ValidationError("--job with a non-empty company is required when converting plain text alone")
            plain_content = legacy_plain_to_content(load_json(args.indeed_text), profile, job)
        else:
            plain_content = None
        content = cover_content or plain_content
        assert content is not None
        if plain_content:
            content["plain_text"] = plain_content["plain_text"]
        write_text(args.output, json.dumps(content, ensure_ascii=False, indent=2) + "\n")
    except (OSError, ValidationError) as error:
        parser.error(str(error))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

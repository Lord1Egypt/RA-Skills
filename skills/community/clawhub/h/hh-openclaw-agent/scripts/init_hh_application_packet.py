#!/usr/bin/env python3
"""Create a machine-readable packet for one hh.ru application run."""

from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path

VALID_REVIEW_STATUS = {"pending", "approved", "rejected"}


def dedupe(values: list[str]) -> list[str]:
    seen: set[str] = set()
    out: list[str] = []
    for value in values:
        normalized = value.strip()
        if not normalized or normalized in seen:
            continue
        seen.add(normalized)
        out.append(normalized)
    return out


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out", required=True, help="Output JSON file.")
    parser.add_argument("--packet-id", required=True, help="Stable packet identifier.")
    parser.add_argument("--vacancy-id", required=True, help="HH vacancy id.")
    parser.add_argument("--vacancy-title", required=True, help="Vacancy title.")
    parser.add_argument("--company-name", required=True, help="Employer name.")
    parser.add_argument("--resume-title", required=True, help="Resume title used for the response.")
    parser.add_argument("--vacancy-url", required=True, help="Public vacancy URL.")
    parser.add_argument("--apply-url", required=True, help="Direct apply URL used in the browser flow.")
    parser.add_argument("--browser-profile", default="", help="OpenClaw browser profile label.")
    parser.add_argument("--cover-letter", default="", help="Cover letter body.")
    parser.add_argument("--review-status", choices=sorted(VALID_REVIEW_STATUS), default="pending", help="Current review state.")
    parser.add_argument("--reviewer", default="", help="Reviewer name or label.")
    parser.add_argument("--blocked-action", action="append", default=[], help="Repeatable blocked-action note.")
    args = parser.parse_args()

    out_path = Path(args.out).expanduser().resolve()
    out_path.parent.mkdir(parents=True, exist_ok=True)

    payload = {
        "schema_version": "1.0",
        "created_utc": datetime.now(timezone.utc).isoformat(),
        "packet": {
            "packet_id": args.packet_id.strip(),
            "vacancy_id": args.vacancy_id.strip(),
            "vacancy_title": args.vacancy_title.strip(),
            "company_name": args.company_name.strip(),
            "resume_title": args.resume_title.strip(),
            "vacancy_url": args.vacancy_url.strip(),
            "apply_url": args.apply_url.strip(),
            "browser_profile": args.browser_profile.strip(),
        },
        "content": {
            "cover_letter": args.cover_letter.strip(),
        },
        "review": {
            "status": args.review_status,
            "reviewer": args.reviewer.strip(),
            "requires_human_review": True,
            "blocked_actions": dedupe(args.blocked_action),
        },
        "steps": [],
        "summary": {
            "status": "draft",
            "effects": [],
            "submitted": False,
            "issue_keys": [],
        },
    }

    out_path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    print(out_path)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

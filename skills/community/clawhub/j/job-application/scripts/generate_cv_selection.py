#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from typing import Any

from common import (
    CV_COLLECTIONS,
    CV_SCHEMA_VERSION,
    PROFILE_DIR,
    ValidationError,
    load_cv_limits,
    load_json,
    load_limit_file,
    selection_hash,
    validate_cv_selection,
)


def terms(value: Any) -> set[str]:
    if isinstance(value, dict):
        text = " ".join(str(item) for item in value.values())
    elif isinstance(value, list):
        text = " ".join(str(item) for item in value)
    else:
        text = str(value)
    return set(re.findall(r"[a-zA-ZÀ-ÿ0-9+#.]+", text.lower()))


def ranked(items: list[dict[str, Any]], job_terms: set[str]) -> list[str]:
    def score(item: dict[str, Any]) -> tuple[int, int, str]:
        item_terms = terms(item)
        return len(item_terms & job_terms), int(item.get("score", 0)), str(item["id"])

    return [item["id"] for item in sorted(items, key=score, reverse=True)]


def adaptive_selection(items: list[dict[str, Any]], job_terms: set[str], base_ids: list[str], limit: int) -> list[str]:
    """Prefer records matching the new job, then retain valid base choices, deterministically."""
    ordered = ranked(items, job_terms)
    matches = [record_id for record_id in ordered if terms(next(item for item in items if item["id"] == record_id)) & job_terms]
    candidates = matches + [record_id for record_id in base_ids if record_id not in matches]
    candidates += [record_id for record_id in ordered if record_id not in candidates]
    return candidates[:limit]


def build_selection(job: dict[str, Any], profile_dir: Path, limits: dict[str, int],
                    base: dict[str, Any] | None, mode: str, base_path: Path | None) -> dict[str, Any]:
    profile = load_json(profile_dir / "master_profile.json")
    job_terms = terms(job)
    result: dict[str, Any] = {
        "schema_version": CV_SCHEMA_VERSION,
        "target_title": job.get("role") or profile.get("default_target_title"),
        "language": job.get("language") or profile.get("default_language"),
        "about_me": (base or {}).get("about_me") or " ".join(profile["about_me_base"]),
        "limits": limits,
    }
    for field, filename in CV_COLLECTIONS.items():
        records = load_json(profile_dir / filename)
        inherited = (base or {}).get(field, [])
        if mode == "strict" and base is not None:
            if len(inherited) > limits[field]:
                raise ValidationError(
                    f"Base selection has {len(inherited)} {field} records but limits.{field} is {limits[field]}"
                )
            result[field] = inherited
        else:
            result[field] = adaptive_selection(records, job_terms, inherited, limits[field])
    if base_path is not None:
        result["derived_from"] = {
            "path": str(base_path.resolve()),
            "input_hash": selection_hash(base_path),
            "mode": mode,
        }
    return validate_cv_selection(result, profile_dir)


def main() -> int:
    parser = argparse.ArgumentParser(description="Suggest deterministic CV records relevant to a job description.")
    parser.add_argument("--job", required=True, type=Path)
    parser.add_argument("--output", required=True, type=Path)
    parser.add_argument("--profile-dir", type=Path, default=PROFILE_DIR)
    parser.add_argument("--limits", type=Path, help="JSON file with CV limits or a {limits: {...}} object")
    parser.add_argument("--base", type=Path, help="Existing cv_selection.json used as a local base")
    parser.add_argument("--mode", choices=("adaptive", "strict"), default="adaptive",
                        help="Base inheritance mode (default: adaptive)")
    args = parser.parse_args()

    try:
        profile_dir = args.profile_dir.expanduser().resolve()
        job = load_json(args.job)
        if not isinstance(job, dict):
            raise ValidationError("job.json must contain a JSON object")
        base_path = args.base.expanduser().resolve() if args.base else None
        if args.mode == "strict" and base_path is None:
            raise ValidationError("--mode strict requires --base <cv_selection.json>")
        base = validate_cv_selection(load_json(base_path), profile_dir) if base_path else None
        limits = load_limit_file(args.limits) if args.limits else (base or {}).get("limits", load_cv_limits())
        result = build_selection(job, profile_dir, limits, base, args.mode, base_path)
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    except (OSError, ValidationError) as error:
        parser.error(str(error))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

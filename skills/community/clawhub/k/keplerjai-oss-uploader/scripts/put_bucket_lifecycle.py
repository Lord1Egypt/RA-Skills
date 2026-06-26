#!/usr/bin/env python3
"""
Apply Aliyun OSS bucket lifecycle for the configured upload prefix:
objects expire (delete) `expire_days` after last modified time.

Requires RAM permission oss:PutBucketLifecycle (and oss:GetBucketLifecycle for merge).
"""

from __future__ import annotations

import argparse
import os
import sys
from pathlib import Path

_scripts = Path(__file__).resolve().parent
if str(_scripts) not in sys.path:
    sys.path.insert(0, str(_scripts))

from oss_lifecycle import sync_upload_prefix_lifecycle  # noqa: E402
from skill_config import load_config_json, load_dotenv  # noqa: E402


def _env(name: str, default: str | None = None) -> str:
    v = os.environ.get(name, default)
    if v is None or v == "":
        raise SystemExit(f"Missing required environment variable: {name}")
    return v


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Put OSS bucket lifecycle (upload prefix, expiration by days)"
    )
    parser.add_argument(
        "--days",
        type=int,
        default=0,
        help="Expiration days after last modified (default: from KEPLERJAI_OSS_OBJECT_LIFECYCLE_DAYS or config)",
    )
    parser.add_argument(
        "--prefix",
        default="",
        help="Override upload dir prefix (no leading/trailing slashes); default from KEPLERJAI_OSS_UPLOAD_DIR",
    )
    parser.add_argument(
        "--rule-id",
        default="",
        help="Lifecycle rule ID (default: KEPLERJAI_OSS_LIFECYCLE_RULE_ID or keplerjai-oss-upload-expire)",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Print planned bucket/prefix/days/rule_id without calling OSS",
    )
    args = parser.parse_args()

    skill_root = Path(__file__).resolve().parent.parent
    load_dotenv(skill_root)
    load_config_json(skill_root)

    access_key_id = _env("KEPLERJAI_OSS_ACCESS_KEY_ID")
    access_key_secret = _env("KEPLERJAI_OSS_ACCESS_KEY_SECRET")
    endpoint = _env("KEPLERJAI_OSS_ENDPOINT")
    bucket_name = _env("KEPLERJAI_OSS_BUCKET")

    upload_dir = (
        args.prefix.strip().strip("/")
        if args.prefix.strip()
        else os.environ.get("KEPLERJAI_OSS_UPLOAD_DIR", "upload").strip().strip("/")
    )

    days = args.days
    if days <= 0:
        raw = os.environ.get("KEPLERJAI_OSS_OBJECT_LIFECYCLE_DAYS", "").strip()
        if not raw:
            raise SystemExit(
                "Set --days N or KEPLERJAI_OSS_OBJECT_LIFECYCLE_DAYS / config.json objectLifecycleExpireDays"
            )
        days = int(raw)

    rule_id = args.rule_id.strip() or os.environ.get(
        "KEPLERJAI_OSS_LIFECYCLE_RULE_ID", ""
    ).strip()

    if args.dry_run:
        rid = rule_id or "keplerjai-oss-upload-expire"
        pfx = upload_dir.strip().strip("/") or "upload"
        print(
            f"dry_run bucket={bucket_name} rule_id={rid} object_prefix={pfx!r}/ "
            f"expiration_days={days} (no API call)"
        )
        return

    try:
        msg = sync_upload_prefix_lifecycle(
            access_key_id=access_key_id,
            access_key_secret=access_key_secret,
            endpoint=endpoint,
            bucket_name=bucket_name,
            upload_dir=upload_dir,
            expire_days=days,
            rule_id=rule_id,
        )
    except Exception as e:  # noqa: BLE001 — surface OSS errors to CLI
        raise SystemExit(str(e)) from e

    print(msg)


if __name__ == "__main__":
    main()

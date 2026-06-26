#!/usr/bin/env python3
"""
Upload a local file to Aliyun OSS (static asset bucket).
Configuration via environment variables (see config.example.env in skill root).
"""

from __future__ import annotations

import argparse
import mimetypes
import os
import re
import secrets
import sys
from datetime import datetime, timezone
from pathlib import Path

_scripts_dir = Path(__file__).resolve().parent
if str(_scripts_dir) not in sys.path:
    sys.path.insert(0, str(_scripts_dir))

from skill_config import load_config_json, load_dotenv  # noqa: E402


def _env(name: str, default: str | None = None) -> str:
    v = os.environ.get(name, default)
    if v is None or v == "":
        raise SystemExit(f"Missing required environment variable: {name}")
    return v


def _default_alphabet() -> str:
    return os.environ.get(
        "KEPLERJAI_OSS_NAME_ALPHABET",
        "123QRSTUabcdVWXYZHijKLAWDCABDstEFGuvwxyzGHIJklmnopqr234560178912",
    )


def _random_name(ext: str, length: int = 16) -> str:
    alphabet = _default_alphabet()
    body = "".join(secrets.choice(alphabet) for _ in range(length))
    ext = ext if ext.startswith(".") else f".{ext}" if ext else ""
    return f"{body}{ext}"


def _safe_stem(original_name: str, max_len: int = 80) -> str:
    stem = Path(original_name).stem
    out: list[str] = []
    for c in stem:
        if c.isascii() and (c.isalnum() or c in "._-"):
            out.append(c)
        elif not c.isascii() and c.isalnum():
            out.append(c)
        else:
            out.append("_")
    s = "".join(out).strip("._") or "file"
    s = re.sub(r"_+", "_", s)
    return s[:max_len]


def _use_utc_path() -> bool:
    return os.environ.get("KEPLERJAI_OSS_PATH_UTC", "").strip().lower() in (
        "1",
        "true",
        "yes",
    )


def _dated_object_key(upload_dir: str, local: Path, suffix: str) -> str:
    use_utc = _use_utc_path()
    now = datetime.now(timezone.utc) if use_utc else datetime.now().astimezone()
    year = now.strftime("%Y")
    month = now.strftime("%m")
    ts_ms = int(now.timestamp() * 1000)
    ext = suffix if suffix.startswith(".") else (f".{suffix}" if suffix else "")
    stem = _safe_stem(local.name)
    filename = f"{ts_ms}_{stem}{ext}"
    return f"{upload_dir}/{year}/{month}/{filename}"


def _lifecycle_days() -> int:
    raw = os.environ.get("KEPLERJAI_OSS_OBJECT_LIFECYCLE_DAYS", "").strip()
    if not raw:
        return 0
    try:
        return int(raw)
    except ValueError:
        return 0


def main() -> None:
    parser = argparse.ArgumentParser(description="Upload file to Aliyun OSS")
    parser.add_argument("local_path", type=Path, help="Local file to upload")
    parser.add_argument(
        "--key",
        "-k",
        help="Object key under bucket (no leading slash). If omitted, uses dated layout or --flat",
    )
    parser.add_argument(
        "--flat",
        action="store_true",
        help="Use uploadDir/randomName+ext instead of uploadDir/YYYY/MM/{ts}_{name}",
    )
    parser.add_argument(
        "--content-type",
        "-t",
        help="Override Content-Type (default: guessed from file name)",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Print target key and public URL without uploading",
    )
    parser.add_argument(
        "--sync-lifecycle",
        action="store_true",
        help="After upload, call PutBucketLifecycle (merge by rule id); needs days from env/config",
    )
    args = parser.parse_args()

    skill_root = Path(__file__).resolve().parent.parent
    load_dotenv(skill_root)
    load_config_json(skill_root)

    local = args.local_path.resolve()
    if not local.is_file():
        raise SystemExit(f"Not a file: {local}")

    access_key_id = _env("KEPLERJAI_OSS_ACCESS_KEY_ID")
    access_key_secret = _env("KEPLERJAI_OSS_ACCESS_KEY_SECRET")
    endpoint = _env("KEPLERJAI_OSS_ENDPOINT")
    bucket_name = _env("KEPLERJAI_OSS_BUCKET")
    upload_dir = os.environ.get("KEPLERJAI_OSS_UPLOAD_DIR", "upload").strip().strip("/")
    bind_host = os.environ.get("KEPLERJAI_OSS_BIND_HOST", "").rstrip("/")

    suffix = local.suffix.lower() or mimetypes.guess_extension(
        mimetypes.guess_type(local.name)[0] or ""
    ) or ""
    if suffix and not suffix.startswith("."):
        suffix = f".{suffix}"

    if args.key:
        object_key = args.key.lstrip("/")
    elif args.flat:
        object_key = f"{upload_dir}/{_random_name(suffix)}"
    else:
        object_key = _dated_object_key(upload_dir, local, suffix)

    content_type = args.content_type
    if not content_type:
        content_type, _ = mimetypes.guess_type(local.name)
        content_type = content_type or "application/octet-stream"

    public_url = ""
    if bind_host:
        public_url = f"{bind_host}/{object_key}"

    if args.dry_run:
        print(f"object_key={object_key}")
        print(f"content_type={content_type}")
        if public_url:
            print(f"public_url={public_url}")
        return

    try:
        import oss2  # type: ignore
    except ImportError:
        raise SystemExit(
            "oss2 is not installed. Run: pip install -r requirements.txt "
            f"(from skill directory)"
        ) from None

    ep = endpoint if endpoint.startswith("http") else f"https://{endpoint}"
    auth = oss2.Auth(access_key_id, access_key_secret)
    bucket = oss2.Bucket(auth, ep, bucket_name)

    headers = {"Content-Type": content_type}
    bucket.put_object_from_file(object_key, str(local), headers=headers)

    print(f"ok object_key={object_key}")
    if public_url:
        print(f"public_url={public_url}")

    sync_lc = args.sync_lifecycle or os.environ.get(
        "KEPLERJAI_OSS_SYNC_LIFECYCLE_ON_UPLOAD", ""
    ).strip().lower() in ("1", "true", "yes", "on")
    days = _lifecycle_days()
    if sync_lc:
        if days <= 0:
            print(
                "lifecycle_skip=未设置 KEPLERJAI_OSS_OBJECT_LIFECYCLE_DAYS（或 config.json objectLifecycleExpireDays），"
                "已跳过 PutBucketLifecycle",
                file=sys.stderr,
            )
        else:
            from oss_lifecycle import sync_upload_prefix_lifecycle  # noqa: PLC0415

            rule_id = os.environ.get("KEPLERJAI_OSS_LIFECYCLE_RULE_ID", "").strip()
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
                print(msg, file=sys.stderr)
            except Exception as e:  # noqa: BLE001
                print(f"lifecycle_error={e}", file=sys.stderr)
    elif days > 0:
        print(
            f"lifecycle_reminder=已为 bucket「{bucket_name}」约定前缀「{upload_dir}/」保留 {days} 天；"
            f"可运行 `python scripts/put_bucket_lifecycle.py` 或上传时加 `--sync-lifecycle` 写入生命周期规则。",
            file=sys.stderr,
        )


if __name__ == "__main__":
    main()

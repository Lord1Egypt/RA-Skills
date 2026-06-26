#!/usr/bin/env python3
"""Upload generated artifacts to Alibaba Cloud OSS and print a signed URL."""

from __future__ import annotations

import argparse
import datetime as dt
import json
import mimetypes
import os
from pathlib import Path
import tempfile
import time
from typing import Iterable
import uuid
import zipfile


def env(name: str, default: str | None = None) -> str | None:
    value = os.environ.get(name)
    return value if value not in (None, "") else default


def require(value: str | None, name: str) -> str:
    if not value:
        raise SystemExit(f"Missing required configuration: {name}")
    return value


def make_bucket(
    endpoint: str,
    bucket: str,
    access_key_id: str,
    access_key_secret: str,
    security_token: str | None,
) -> object:
    try:
        import oss2
    except ImportError as exc:
        raise SystemExit(
            "Missing Python dependency: oss2. Install it with `python3 -m pip install oss2`."
        ) from exc

    auth = (
        oss2.StsAuth(access_key_id, access_key_secret, security_token)
        if security_token
        else oss2.Auth(access_key_id, access_key_secret)
    )
    return oss2.Bucket(auth, endpoint, bucket, is_cname=env("OSS_IS_CNAME") == "1")


def build_signed_get_url(
    endpoint: str,
    bucket: str,
    key: str,
    access_key_id: str,
    access_key_secret: str,
    expires_in: int,
    security_token: str | None,
) -> tuple[str, int]:
    expires = int(time.time()) + expires_in
    client = make_bucket(endpoint, bucket, access_key_id, access_key_secret, security_token)
    return client.sign_url("GET", key, expires_in), expires


def iter_files(path: Path) -> Iterable[Path]:
    for item in sorted(path.rglob("*")):
        if item.is_file():
            yield item


def make_archive(paths: list[Path]) -> Path:
    timestamp = dt.datetime.now(dt.UTC).strftime("%Y%m%dT%H%M%SZ")
    archive = Path(tempfile.gettempdir()) / f"openclaw-artifact-{timestamp}-{uuid.uuid4().hex[:8]}.zip"
    with zipfile.ZipFile(archive, "w", compression=zipfile.ZIP_DEFLATED) as zf:
        for source in paths:
            if source.is_dir():
                base = source.parent
                for file_path in iter_files(source):
                    zf.write(file_path, file_path.relative_to(base).as_posix())
            else:
                zf.write(source, source.name)
    return archive


def resolve_source(paths: list[str]) -> Path:
    if not paths:
        raise SystemExit("At least one artifact path is required")
    resolved = [Path(p).expanduser().resolve() for p in paths]
    missing = [str(p) for p in resolved if not p.exists()]
    if missing:
        raise SystemExit("Artifact path not found: " + ", ".join(missing))
    if len(resolved) == 1 and resolved[0].is_file():
        return resolved[0]
    return make_archive(resolved)


def default_object_key(prefix: str, source: Path) -> str:
    clean_prefix = prefix.strip("/")
    timestamp = dt.datetime.now(dt.UTC).strftime("%Y/%m/%d")
    safe_name = source.name.replace("\\", "_").replace("/", "_")
    unique = uuid.uuid4().hex[:12]
    parts = [part for part in [clean_prefix, timestamp, f"{unique}-{safe_name}"] if part]
    return "/".join(parts)


def upload_file(
    source: Path,
    bucket: str,
    key: str,
    endpoint: str,
    access_key_id: str,
    access_key_secret: str,
    security_token: str | None,
) -> None:
    try:
        import oss2
    except ImportError as exc:
        raise SystemExit(
            "Missing Python dependency: oss2. Install it with `python3 -m pip install oss2`."
        ) from exc

    content_type = mimetypes.guess_type(source.name)[0] or "application/octet-stream"
    client = make_bucket(endpoint, bucket, access_key_id, access_key_secret, security_token)
    try:
        client.put_object_from_file(key, str(source), headers={"Content-Type": content_type})
    except oss2.exceptions.OssError as exc:
        raise SystemExit(f"OSS upload failed: {exc}") from exc


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("paths", nargs="+", help="Files or directories to upload")
    parser.add_argument("--bucket", default=env("OSS_BUCKET"))
    parser.add_argument("--endpoint", default=env("OSS_ENDPOINT"))
    parser.add_argument("--public-endpoint", default=env("OSS_PUBLIC_ENDPOINT") or env("OSS_ENDPOINT"))
    parser.add_argument("--prefix", default=env("OSS_PREFIX", "openclaw-artifacts"))
    parser.add_argument("--expires", type=int, default=int(env("OSS_EXPIRES", "3600") or "3600"))
    parser.add_argument("--object-key", help="Explicit object key. Allowed only for a single file.")
    parser.add_argument("--json", action="store_true", help="Print JSON only")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    access_key_id = require(env("OSS_ACCESS_KEY_ID"), "OSS_ACCESS_KEY_ID")
    access_key_secret = require(env("OSS_ACCESS_KEY_SECRET"), "OSS_ACCESS_KEY_SECRET")
    bucket = require(args.bucket, "OSS_BUCKET")
    endpoint = require(args.endpoint, "OSS_ENDPOINT")
    public_endpoint = require(args.public_endpoint, "OSS_PUBLIC_ENDPOINT or OSS_ENDPOINT")
    security_token = env("OSS_STS_TOKEN")

    source = resolve_source(args.paths)
    original_paths = [Path(p).expanduser().resolve() for p in args.paths]
    if args.object_key and (len(original_paths) != 1 or original_paths[0].is_dir()):
        raise SystemExit("--object-key is only supported for a single file upload")
    key = args.object_key or default_object_key(args.prefix, source)

    upload_file(source, bucket, key, endpoint, access_key_id, access_key_secret, security_token)
    download_url, expires_epoch = build_signed_get_url(
        public_endpoint,
        bucket,
        key,
        access_key_id,
        access_key_secret,
        args.expires,
        security_token,
    )
    result = {
        "bucket": bucket,
        "object_key": key,
        "download_url": download_url,
        "expires_at": dt.datetime.fromtimestamp(expires_epoch, dt.UTC)
        .replace(microsecond=0)
        .isoformat()
        .replace("+00:00", "Z"),
        "source": str(source),
    }
    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return
    print(f"object_key: {result['object_key']}")
    print(f"download_url: {result['download_url']}")
    print(f"expires_at: {result['expires_at']}")
    print(f"source: {result['source']}")


if __name__ == "__main__":
    main()

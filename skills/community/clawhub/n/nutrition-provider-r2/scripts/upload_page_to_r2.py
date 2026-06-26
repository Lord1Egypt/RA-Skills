#!/usr/bin/env -S uv run
# /// script
# requires-python = ">=3.10"
# dependencies = [
#   "boto3>=1.34.0",
#   "botocore>=1.34.0",
# ]
# ///
"""Upload one provider record, or extract and upload provider records from a page payload, to Cloudflare R2.

Usage examples:
  uv run upload_page_to_r2.py --input tmp/food-10001.json --page-index 1 --food-id 10001 --skip-existing
  cat tmp/food-10001.json | uv run upload_page_to_r2.py --page-index 1 --food-id 10001 --content-type application/json
  uv run upload_page_to_r2.py --input tmp/food-10001.json --key raw/site/run/page-0001/food-10001.json
  uv run upload_page_to_r2.py --input tmp/page-0001.json --page-index 1 --extract-foods --skip-existing
  uv run upload_page_to_r2.py --input tmp/page-0001.json --page-index 1 --failed
"""

from __future__ import annotations

import argparse
import json
import mimetypes
import os
import re
import sys
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime, timezone
from pathlib import Path

import boto3
from botocore.config import Config
from botocore.exceptions import ClientError


DEFAULT_SOURCE_NAME = "nutrition-provider"
DEFAULT_PREFIX = "raw"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", help="Path to the local file to upload. If omitted, read bytes from stdin.")
    parser.add_argument("--key", help="Explicit R2 object key. Overrides generated key settings.")
    parser.add_argument("--page-index", type=int, help="1-based page index used when generating the object key.")
    parser.add_argument("--food-id", help="Stable identifier for one provider record, such as provider _id or code.")
    parser.add_argument(
        "--extract-foods",
        action="store_true",
        help="Treat the input as a page payload and upload one object per record from the page's data array.",
    )
    parser.add_argument(
        "--content-type",
        help="Uploaded object content type. If omitted, infer from input path or object key and otherwise fall back safely.",
    )
    parser.add_argument("--prefix", help="R2 key prefix. Defaults to $R2_PREFIX or 'raw'.")
    parser.add_argument("--source-name", help="Source name segment. Defaults to $SOURCE_NAME or 'nutrition-provider'.")
    parser.add_argument("--run-id", help="Run identifier. Defaults to $RUN_ID or current UTC timestamp.")
    parser.add_argument("--failed", action="store_true", help="Store the object under a failures/ prefix.")
    parser.add_argument(
        "--skip-existing",
        action="store_true",
        help="Skip upload when an object with the same key already exists.",
    )
    parser.add_argument(
        "--max-workers",
        type=int,
        default=8,
        help="Maximum parallel uploads when --extract-foods is used. Default: 8.",
    )
    parser.add_argument(
        "--food-id-fields",
        default="_id,code",
        help="Comma-separated ordered fields to try when deriving a stable record id in --extract-foods mode.",
    )
    return parser.parse_args()


def require_env(name: str) -> str:
    value = os.getenv(name)
    if not value:
        raise SystemExit(f"Missing environment variable: {name}")
    return value


def read_payload(input_path: str | None) -> bytes:
    if input_path:
        return Path(input_path).read_bytes()
    data = sys.stdin.buffer.read()
    if not data:
        raise SystemExit("No input payload provided. Pass --input or pipe bytes to stdin.")
    return data


def build_client():
    account_id = require_env("R2_ACCOUNT_ID")
    access_key = require_env("R2_ACCESS_KEY_ID")
    secret_key = require_env("R2_SECRET_ACCESS_KEY")
    endpoint = f"https://{account_id}.r2.cloudflarestorage.com"
    return boto3.client(
        "s3",
        endpoint_url=endpoint,
        aws_access_key_id=access_key,
        aws_secret_access_key=secret_key,
        config=Config(signature_version="s3v4", retries={"max_attempts": 5, "mode": "standard"}),
    )


def current_run_id() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H-%M-%SZ")


def require_page_index(page_index: int | None) -> int:
    if page_index is None:
        raise SystemExit("Missing --page-index. Pass --key explicitly or provide --page-index for generated keys.")
    if page_index < 1:
        raise SystemExit("--page-index must be a positive integer.")
    return page_index


def sanitize_key_segment(value: str) -> str:
    cleaned = re.sub(r"[^A-Za-z0-9._-]+", "-", value.strip())
    cleaned = cleaned.strip("-._")
    if not cleaned:
        raise SystemExit("Invalid empty key segment after sanitizing --food-id.")
    return cleaned


def parse_json_payload(payload: bytes) -> object:
    try:
        return json.loads(payload.decode("utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError) as error:
        raise SystemExit(f"Expected valid UTF-8 JSON payload: {error}") from error


def extract_foods(document: object) -> list[dict]:
    if isinstance(document, dict):
        if isinstance(document.get("data"), list):
            foods = document["data"]
        elif isinstance(document.get("raw"), dict) and isinstance(document["raw"].get("data"), list):
            foods = document["raw"]["data"]
        else:
            raise SystemExit("Could not find a record list. Expected `data` or `raw.data` in the page payload.")
    elif isinstance(document, list):
        foods = document
    else:
        raise SystemExit("Expected a JSON object or array when using --extract-foods.")

    normalized = [food for food in foods if isinstance(food, dict)]
    if not normalized:
        raise SystemExit("No provider records found to upload.")
    return normalized


def derive_food_id(food: dict, id_fields: list[str]) -> str:
    for field in id_fields:
        raw_value = food.get(field)
        if raw_value is None:
            continue
        text = str(raw_value).strip()
        if text:
            return sanitize_key_segment(text)
    raise SystemExit(f"Could not derive record id from fields: {', '.join(id_fields)}")


def choose_extension(content_type: str | None, input_path: str | None, key: str | None) -> str:
    candidates = []
    if input_path:
        candidates.append(Path(input_path).suffix.lower())
    if key:
        candidates.append(Path(key).suffix.lower())
    if content_type:
        guessed = mimetypes.guess_extension(content_type, strict=False)
        if guessed:
            candidates.append(guessed.lower())

    for candidate in candidates:
        if candidate in {".json", ".html", ".htm", ".txt", ".xml"}:
            return ".html" if candidate == ".htm" else candidate
        if candidate:
            return candidate
    return ".bin"


def infer_content_type(content_type: str | None, input_path: str | None, key: str | None) -> str:
    if content_type:
        return content_type

    for guess_target in (input_path, key):
        if guess_target:
            guessed, _ = mimetypes.guess_type(guess_target)
            if guessed:
                return guessed

    return "application/octet-stream"


def build_key(args: argparse.Namespace) -> str:
    if args.key:
        return args.key

    page_index = require_page_index(args.page_index)
    prefix = args.prefix or os.getenv("R2_PREFIX") or DEFAULT_PREFIX
    source_name = args.source_name or os.getenv("SOURCE_NAME") or DEFAULT_SOURCE_NAME
    run_id = args.run_id or os.getenv("RUN_ID") or current_run_id()
    extension = choose_extension(args.content_type, args.input, None)
    parts = [prefix.strip("/"), source_name.strip("/"), run_id.strip("/")]
    if args.failed:
        parts.append("failures")
    if args.food_id:
        food_id = sanitize_key_segment(args.food_id)
        parts.append(f"page-{page_index:04d}")
        parts.append(f"food-{food_id}{extension}")
    else:
        parts.append(f"page-{page_index:04d}{extension}")
    return "/".join(parts)


def build_food_key(args: argparse.Namespace, food_id: str) -> str:
    base_key_args = argparse.Namespace(**vars(args))
    base_key_args.key = None
    base_key_args.food_id = food_id
    return build_key(base_key_args)


def object_exists(client, bucket: str, key: str) -> bool:
    try:
        client.head_object(Bucket=bucket, Key=key)
        return True
    except ClientError as error:
        error_code = str(error.response.get("Error", {}).get("Code", ""))
        if error_code in {"404", "NoSuchKey", "NotFound"}:
            return False
        raise


def upload_object(client, bucket: str, key: str, payload: bytes, content_type: str, skip_existing: bool) -> str:
    if skip_existing and object_exists(client, bucket, key):
        return f"skipped s3://{bucket}/{key} ({content_type})"
    client.put_object(Bucket=bucket, Key=key, Body=payload, ContentType=content_type)
    return f"uploaded s3://{bucket}/{key} ({content_type})"


def upload_foods_from_page(args: argparse.Namespace, client, bucket: str, payload: bytes) -> int:
    if args.food_id:
        raise SystemExit("--food-id cannot be combined with --extract-foods.")
    if args.failed:
        raise SystemExit("--failed cannot be combined with --extract-foods.")
    if args.max_workers < 1:
        raise SystemExit("--max-workers must be at least 1.")

    page_index = require_page_index(args.page_index)
    del page_index  # validated above; key generation reads args.page_index directly
    document = parse_json_payload(payload)
    foods = extract_foods(document)
    id_fields = [field.strip() for field in args.food_id_fields.split(",") if field.strip()]
    if not id_fields:
        raise SystemExit("--food-id-fields must contain at least one field name.")

    content_type = args.content_type or "application/json"
    upload_jobs: list[tuple[str, bytes]] = []
    for food in foods:
        food_id = derive_food_id(food, id_fields)
        key = build_food_key(args, food_id)
        food_payload = json.dumps(food, ensure_ascii=False, separators=(",", ":")).encode("utf-8")
        upload_jobs.append((key, food_payload))

    seen_keys: set[str] = set()
    deduped_jobs: list[tuple[str, bytes]] = []
    for key, food_payload in upload_jobs:
        if key in seen_keys:
            continue
        seen_keys.add(key)
        deduped_jobs.append((key, food_payload))

    with ThreadPoolExecutor(max_workers=args.max_workers) as executor:
        futures = {
            executor.submit(upload_object, client, bucket, key, food_payload, content_type, args.skip_existing): key
            for key, food_payload in deduped_jobs
        }
        for future in as_completed(futures):
            print(future.result())

    print(
        f"completed {len(deduped_jobs)} record uploads from page-{args.page_index:04d} "
        f"(source items: {len(foods)}, unique keys: {len(deduped_jobs)})"
    )
    return 0


def main() -> int:
    args = parse_args()
    bucket = require_env("R2_BUCKET")
    payload = read_payload(args.input)
    client = build_client()
    if args.extract_foods:
        return upload_foods_from_page(args, client, bucket, payload)

    key = build_key(args)
    content_type = infer_content_type(args.content_type, args.input, key)
    print(upload_object(client, bucket, key, payload, content_type, args.skip_existing))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

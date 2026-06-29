#!/usr/bin/env python3
"""
Generic PixelLab API client for the pixellab-ai skill.

The client reads PIXELLAB_API_KEY from the environment, sends Bearer-token
GET/POST/PATCH requests to PixelLab /v1 or /v2 paths, optionally polls
background jobs, writes JSON results, and downloads asset URLs discovered in
asset-shaped response fields.
"""

from __future__ import annotations

import argparse
import base64
import binascii
import json
import os
import pathlib
import re
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from typing import Any, Iterable


OFFICIAL_BASE_URL = "https://api.pixellab.ai"
DEFAULT_BASE_URL = OFFICIAL_BASE_URL
DEFAULT_TIMEOUT = int(os.environ.get("PIXELLAB_TIMEOUT_SEC", "180"))
DEFAULT_POLL_INTERVAL = float(os.environ.get("PIXELLAB_POLL_INTERVAL_SEC", "5"))
DEFAULT_MAX_POLLS = int(os.environ.get("PIXELLAB_MAX_POLLS", "360"))
DEFAULT_MAX_DOWNLOAD_BYTES = int(os.environ.get("PIXELLAB_MAX_DOWNLOAD_BYTES", str(100 * 1024 * 1024)))
DEFAULT_DOWNLOAD_RETRIES = int(os.environ.get("PIXELLAB_DOWNLOAD_RETRIES", "6"))
DEFAULT_DOWNLOAD_RETRY_DELAY = float(os.environ.get("PIXELLAB_DOWNLOAD_RETRY_DELAY_SEC", "5"))
RETRYABLE_STATUSES = {429, 502, 503, 504, 529}
ASSET_URL_KEYS = {
    "asseturl",
    "asseturls",
    "downloadurl",
    "fileurl",
    "gifurl",
    "imageurl",
    "imageurls",
    "outputurl",
    "outputurls",
    "pngurl",
    "resulturl",
    "resulturls",
    "spriteurl",
    "spritesheeturl",
    "spritesheetimageurl",
    "urltoimage",
    "videourl",
}
TOP_LEVEL_ASSET_URL_KEYS = {
    "asseturl",
    "asseturls",
    "downloadurl",
    "fileurl",
    "gifurl",
    "imageurl",
    "imageurls",
    "outputurl",
    "outputurls",
    "pngurl",
    "resulturl",
    "resulturls",
    "spriteurl",
    "spritesheeturl",
    "spritesheetimageurl",
    "urltoimage",
    "videourl",
}
ASSET_CONTAINER_KEYS = {
    "asset",
    "assets",
    "file",
    "files",
    "generated",
    "generation",
    "generations",
    "image",
    "images",
    "output",
    "outputs",
    "result",
    "results",
    "sprite",
    "sprites",
    "spritesheet",
    "video",
    "videos",
}
GENERIC_URL_KEYS = {"href", "src", "url"}


def eprint(*args: Any) -> None:
    print(*args, file=sys.stderr)


def load_env_file(path: pathlib.Path) -> None:
    if not path.exists() or not path.is_file():
        return
    for raw_line in path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        key = key.strip()
        value = value.strip().strip("'\"")
        if key and key not in os.environ:
            os.environ[key] = value


def load_explicit_env_file(explicit_path: str | None = None) -> None:
    if not explicit_path:
        return
    load_env_file(pathlib.Path(explicit_path).expanduser().resolve())


def resolve_base_url(allow_custom_base: bool = False) -> str:
    raw = os.environ.get("PIXELLAB_API_BASE", OFFICIAL_BASE_URL).strip().rstrip("/")
    base_url = raw or OFFICIAL_BASE_URL
    parsed = urllib.parse.urlparse(base_url)
    if parsed.scheme != "https" or not parsed.netloc:
        raise ValueError("PIXELLAB_API_BASE must be an HTTPS URL.")
    if base_url != OFFICIAL_BASE_URL and not allow_custom_base:
        raise ValueError(
            "PIXELLAB_API_BASE is not the official PixelLab API. "
            "Unset it or pass --allow-custom-base only for a trusted test endpoint."
        )
    return base_url


def load_payload(args: argparse.Namespace) -> Any:
    if args.payload_file:
        with open(args.payload_file, "r", encoding="utf-8") as f:
            return json.load(f)
    if args.payload:
        return json.loads(args.payload)
    return None


def validate_api_path(path: str) -> str:
    if path.startswith("http://") or path.startswith("https://"):
        raise ValueError("Pass a PixelLab API path like /v2/create-image-pixflux, not a full URL.")
    normalized = path if path.startswith("/") else f"/{path}"
    if not (normalized.startswith("/v1/") or normalized.startswith("/v2/")):
        raise ValueError("Only PixelLab /v1/ or /v2/ API paths are accepted.")
    if ".." in normalized:
        raise ValueError("API path must not contain '..'.")
    return normalized


def request_json(
    method: str,
    url: str,
    api_key: str,
    payload: Any = None,
    timeout: int = DEFAULT_TIMEOUT,
    max_retries: int = 5,
    quiet: bool = False,
) -> Any:
    body: bytes | None = None
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Accept": "application/json",
    }
    if payload is not None:
        body = json.dumps(payload).encode("utf-8")
        headers["Content-Type"] = "application/json"

    method_upper = method.upper()
    retry_limit = max_retries if method_upper in {"GET", "HEAD"} else 0
    last_err: Exception | None = None
    for attempt in range(retry_limit + 1):
        req = urllib.request.Request(url=url, data=body, method=method_upper, headers=headers)
        try:
            with urllib.request.urlopen(req, timeout=timeout) as resp:
                raw = resp.read()
                if not raw:
                    return {}
                content_type = resp.headers.get("Content-Type", "")
                if "application/json" in content_type or raw[:1] in (b"{", b"["):
                    return json.loads(raw.decode("utf-8"))
                return {"raw_text": raw.decode("utf-8", errors="replace")}
        except urllib.error.HTTPError as err:
            raw = err.read().decode("utf-8", errors="replace")
            status = err.code
            last_err = err
            if status in RETRYABLE_STATUSES and attempt < retry_limit:
                sleep_s = min(2**attempt, 20)
                if not quiet:
                    eprint(f"[retry] HTTP {status}; sleeping {sleep_s}s")
                time.sleep(sleep_s)
                continue
            raise RuntimeError(f"HTTP {status}: {raw}") from err
        except Exception as err:
            last_err = err
            if attempt < retry_limit:
                sleep_s = min(2**attempt, 20)
                if not quiet:
                    eprint(f"[retry] transient error: {err}; sleeping {sleep_s}s")
                time.sleep(sleep_s)
                continue
            raise
    raise RuntimeError(f"Request failed after retries: {last_err}")


def find_job_ids(obj: Any) -> list[str]:
    job_ids: list[str] = []
    seen: set[str] = set()

    def add_job_id(value: Any) -> None:
        if isinstance(value, str) and value not in seen:
            job_ids.append(value)
            seen.add(value)

    queue = [obj]
    while queue:
        cur = queue.pop(0)
        if isinstance(cur, dict):
            for key, value in cur.items():
                key_lower = key.lower()
                if key_lower in {"job_id", "background_job_id", "backgroundjobid"}:
                    add_job_id(value)
                elif key_lower in {"job_ids", "background_job_ids", "backgroundjobids"} and isinstance(value, list):
                    for item in value:
                        add_job_id(item)
                queue.append(value)
        elif isinstance(cur, list):
            queue.extend(cur)
    return job_ids


def is_safe_job_id(job_id: str) -> bool:
    if not job_id or job_id in {".", ".."}:
        return False
    if any(ch in job_id for ch in "/\\?#"):
        return False
    return not any(ord(ch) < 32 for ch in job_id)


def job_id_from_background_job_path(path: str) -> str | None:
    prefix = "/v2/background-jobs/"
    if not path.startswith(prefix):
        return None
    job_id = path[len(prefix) :].strip("/")
    if not job_id or "/" in job_id:
        return None
    decoded_job_id = urllib.parse.unquote(job_id)
    if not is_safe_job_id(decoded_job_id):
        return None
    return decoded_job_id


def has_nonempty_output(obj: Any) -> bool:
    if not isinstance(obj, dict):
        return False
    for key in ("result", "results", "output", "outputs", "images", "assets"):
        value = obj.get(key)
        if value not in (None, "", [], {}):
            return True
    return False


def poll_background_job(
    base_url: str,
    job_id: str,
    api_key: str,
    poll_interval: float,
    max_polls: int,
    timeout: int,
    max_retries: int,
    quiet: bool = False,
    progress_jsonl: str | None = None,
) -> Any:
    if not is_safe_job_id(job_id):
        raise ValueError("background job id contains unsafe path characters")
    path = f"/v2/background-jobs/{urllib.parse.quote(job_id, safe='')}"
    url = f"{base_url}{path}"
    for poll_idx in range(max_polls):
        data = request_json("GET", url, api_key, timeout=timeout, max_retries=max_retries, quiet=quiet)
        status = str(data.get("status") or data.get("job_status") or data.get("state") or "").lower()
        append_progress_event(progress_jsonl, {"event": "polling", "job_id": job_id, "poll": poll_idx + 1, "status": status or "unknown"})

        if status in {"completed", "complete", "succeeded", "success", "done"}:
            append_progress_event(progress_jsonl, {"event": "completed", "job_id": job_id, "poll": poll_idx + 1})
            return data
        if status in {"failed", "error", "cancelled", "canceled"}:
            append_progress_event(progress_jsonl, {"event": "failed", "job_id": job_id, "poll": poll_idx + 1, "status": status})
            raise RuntimeError(f"Background job failed: {json.dumps(data, indent=2)}")

        if not status and has_nonempty_output(data):
            append_progress_event(progress_jsonl, {"event": "completed", "job_id": job_id, "poll": poll_idx + 1, "status": "implicit-output"})
            return data

        if not quiet and ((poll_idx + 1) == 1 or (poll_idx + 1) % 10 == 0):
            eprint(f"[poll {poll_idx + 1}/{max_polls}] status={status or 'unknown'}")
        time.sleep(poll_interval)

    raise TimeoutError(f"Background job {job_id} did not finish within polling budget.")


def looks_like_url(value: str) -> bool:
    return bool(re.match(r"^https?://", value))


def normalize_key(key: Any) -> str:
    return re.sub(r"[^a-z0-9]+", "", str(key).lower())


def is_asset_url_path(path: tuple[str, ...]) -> bool:
    if not path:
        return False
    leaf = path[-1]
    if leaf in TOP_LEVEL_ASSET_URL_KEYS:
        return True
    if leaf in ASSET_URL_KEYS:
        return any(part in ASSET_CONTAINER_KEYS for part in path[:-1])
    if leaf in ASSET_CONTAINER_KEYS:
        return True
    return leaf in GENERIC_URL_KEYS and any(part in ASSET_CONTAINER_KEYS for part in path[:-1])


def iter_asset_urls(obj: Any, path: tuple[str, ...] = ()) -> Iterable[str]:
    if isinstance(obj, str):
        if looks_like_url(obj) and is_asset_url_path(path):
            yield obj
        return
    if isinstance(obj, dict):
        for key, value in obj.items():
            yield from iter_asset_urls(value, path + (normalize_key(key),))
    elif isinstance(obj, list):
        for item in obj:
            yield from iter_asset_urls(item, path)


def iter_all_urls(obj: Any) -> Iterable[str]:
    if isinstance(obj, str):
        if looks_like_url(obj):
            yield obj
        return
    if isinstance(obj, dict):
        for value in obj.values():
            yield from iter_all_urls(value)
    elif isinstance(obj, list):
        for item in obj:
            yield from iter_all_urls(item)


def iter_base64_images(obj: Any) -> Iterable[tuple[str, str]]:
    if isinstance(obj, dict):
        encoded = obj.get("base64")
        if isinstance(encoded, str) and str(obj.get("type", "base64")).lower() == "base64":
            image_format = str(obj.get("format") or "").lower()
            yield encoded, image_format
        for value in obj.values():
            yield from iter_base64_images(value)
    elif isinstance(obj, list):
        for item in obj:
            yield from iter_base64_images(item)


def slugify(value: str, fallback: str = "image") -> str:
    slug = re.sub(r"[^a-zA-Z0-9._-]+", "-", value.strip()).strip("-._")
    return slug or fallback


def safe_filename_from_url(url: str, index: int) -> str:
    parsed = urllib.parse.urlparse(url)
    name = pathlib.Path(parsed.path).name or f"download-{index}.bin"
    safe = re.sub(r"[^A-Za-z0-9._-]+", "_", name)
    return safe or f"download-{index}.bin"


def download_one(url: str, destination: pathlib.Path, timeout: int, max_bytes: int) -> None:
    total = 0
    request = urllib.request.Request(
        url,
        headers={
            "User-Agent": "pixellab-ai-skill/1.5 (+https://www.pixellab.ai/)",
            "Accept": "image/png,image/*,*/*",
        },
    )
    with urllib.request.urlopen(request, timeout=timeout) as resp, open(destination, "wb") as f:
        while True:
            chunk = resp.read(1024 * 256)
            if not chunk:
                break
            total += len(chunk)
            if total > max_bytes:
                raise RuntimeError(f"download exceeded {max_bytes} bytes")
            f.write(chunk)


def unique_destination(download_dir: pathlib.Path, filename: str, reserved_names: set[str]) -> pathlib.Path:
    candidate = filename
    stem = pathlib.Path(filename).stem
    suffix = pathlib.Path(filename).suffix
    counter = 2
    while candidate in reserved_names or (download_dir / candidate).exists():
        candidate = f"{stem}-{counter}{suffix}"
        counter += 1
    reserved_names.add(candidate)
    return download_dir / candidate


def download_assets(
    urls: list[str],
    download_dir: pathlib.Path,
    timeout: int,
    max_bytes: int,
    retries: int,
    retry_delay: float,
) -> tuple[list[str], list[str]]:
    download_dir.mkdir(parents=True, exist_ok=True)
    saved: list[str] = []
    reserved_names: set[str] = set()
    failures: list[str] = []
    for index, url in enumerate(urls, start=1):
        filename = safe_filename_from_url(url, index)
        destination = unique_destination(download_dir, filename, reserved_names)
        last_error: Exception | None = None
        for attempt in range(retries + 1):
            try:
                download_one(url, destination, timeout=timeout, max_bytes=max_bytes)
                saved.append(str(destination))
                last_error = None
                break
            except Exception as err:
                last_error = err
                if destination.exists():
                    destination.unlink()
                if attempt < retries:
                    time.sleep(retry_delay)
        if last_error is not None:
            failures.append(f"{url}: {last_error}")
            eprint(f"[warn] failed to download {url}: {last_error}")
    return saved, failures


def infer_image_format(data: bytes) -> str | None:
    if data.startswith(b"\x89PNG\r\n\x1a\n"):
        return "png"
    if data.startswith(b"\xff\xd8\xff"):
        return "jpg"
    if data.startswith(b"GIF87a") or data.startswith(b"GIF89a"):
        return "gif"
    if data.startswith(b"RIFF") and data[8:12] == b"WEBP":
        return "webp"
    return None


def save_base64_assets(result: Any, download_dir: pathlib.Path, asset_slug: str = "image") -> list[str]:
    download_dir.mkdir(parents=True, exist_ok=True)
    saved: list[str] = []
    reserved_names: set[str] = set()
    safe_slug = slugify(asset_slug, fallback="image")
    candidate_index = 1
    for field_index, (encoded, image_format) in enumerate(iter_base64_images(result), start=1):
        if "," in encoded and encoded[:20].lower().startswith("data:"):
            encoded = encoded.split(",", 1)[1]
        cleaned = re.sub(r"\s+", "", encoded)
        try:
            decoded = base64.b64decode(cleaned, validate=True)
        except (binascii.Error, ValueError) as err:
            raise RuntimeError(f"failed to decode base64 image field {field_index}: {err}") from err
        detected_format = infer_image_format(decoded)
        if detected_format is None:
            eprint(f"[warn] skipped base64 field {field_index}: decoded bytes are not a recognized image")
            continue
        safe_format = re.sub(r"[^A-Za-z0-9]+", "", image_format or detected_format) or detected_format
        destination = unique_destination(download_dir, f"{safe_slug}-candidate-{candidate_index:02d}.{safe_format}", reserved_names)
        destination.write_bytes(decoded)
        saved.append(str(destination))
        candidate_index += 1
    return saved


def sum_usage_cost_usd(obj: Any) -> float:
    total = 0.0
    if isinstance(obj, dict):
        if str(obj.get("type", "")).lower() == "usd" and "usd" in obj:
            try:
                total += float(obj["usd"])
            except (TypeError, ValueError):
                pass
        for key, value in obj.items():
            if str(key).lower() == "usage_cost_usd":
                try:
                    total += float(value)
                except (TypeError, ValueError):
                    pass
            else:
                total += sum_usage_cost_usd(value)
    elif isinstance(obj, list):
        for item in obj:
            total += sum_usage_cost_usd(item)
    return round(total, 6)


def top_level_keys(obj: Any) -> list[str]:
    if isinstance(obj, dict):
        return sorted(str(key) for key in obj.keys())
    return [type(obj).__name__]


def build_compact_result(
    status: str,
    method: str,
    path: str,
    result: Any,
    result_file: str | None,
    downloaded_files: list[str],
    decoded_files: list[str],
    discovered_urls: list[str],
    error: dict[str, Any] | None,
    asset_validation: dict[str, Any] | None = None,
    download_errors: list[str] | None = None,
) -> dict[str, Any]:
    job_ids = find_job_ids(result)
    compact = {
        "status": status,
        "method": method.upper(),
        "endpoint": path,
        "result_file": result_file,
        "job_ids": job_ids,
        "usage_cost_usd": sum_usage_cost_usd(result),
        "result_keys": top_level_keys(result),
        "discovered_url_count": len(discovered_urls),
        "downloaded_files": downloaded_files,
        "download_error_count": len(download_errors or []),
        "download_errors": list(download_errors or []),
        "decoded_files": decoded_files,
        "candidate_count": len(downloaded_files) + len(decoded_files),
        "error": error,
    }
    if asset_validation is not None:
        compact["asset_validation"] = asset_validation
    return compact


def build_error_result(
    status: str,
    method: str,
    path: str,
    payload_file: str | None,
    error_code: str,
    message: str,
    job_id: str | None = None,
    job_ids: list[str] | None = None,
) -> dict[str, Any]:
    ids = list(job_ids or [])
    if job_id and job_id not in ids:
        ids.insert(0, job_id)
    return {
        "status": status,
        "method": method.upper(),
        "endpoint": path,
        "payload_file": payload_file,
        "error_code": error_code,
        "message": message,
        "job_id": ids[0] if ids else None,
        "job_ids": ids,
    }


def classify_error_code(err: Exception) -> str:
    message = str(err)
    match = re.search(r"HTTP\s+(\d{3})", message)
    if match:
        return f"http_{match.group(1)}"
    if isinstance(err, TimeoutError):
        return "timeout"
    return err.__class__.__name__


def load_job_ids_from_result_file(path: pathlib.Path) -> list[str]:
    data = json.loads(path.read_text(encoding="utf-8"))
    return find_job_ids(data)


def append_progress_event(progress_jsonl: str | None, event: dict[str, Any]) -> None:
    if not progress_jsonl:
        return
    path = pathlib.Path(progress_jsonl)
    path.parent.mkdir(parents=True, exist_ok=True)
    payload = {"ts": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()), **event}
    with open(path, "a", encoding="utf-8") as f:
        f.write(json.dumps(payload, ensure_ascii=True) + "\n")


def write_json_file(path: str | None, data: Any) -> None:
    if not path:
        return
    result_path = pathlib.Path(path)
    result_path.parent.mkdir(parents=True, exist_ok=True)
    result_path.write_text(json.dumps(data, indent=2, ensure_ascii=True) + "\n", encoding="utf-8")


def parse_size(raw: str | None) -> tuple[int, int] | None:
    if raw is None:
        return None
    match = re.fullmatch(r"(\d+)x(\d+)", raw.strip().lower())
    if not match:
        raise ValueError("expected --expect-size like 128x128")
    return int(match.group(1)), int(match.group(2))


def read_png_meta(path: pathlib.Path) -> dict[str, Any] | None:
    with open(path, "rb") as f:
        header = f.read(33)
    if len(header) < 33 or header[:8] != b"\x89PNG\r\n\x1a\n" or header[12:16] != b"IHDR":
        return None
    return {
        "width": int.from_bytes(header[16:20], "big"),
        "height": int.from_bytes(header[20:24], "big"),
        "bit_depth": header[24],
        "color_type": header[25],
    }


def validate_saved_assets(paths: list[str], expected_size: tuple[int, int] | None = None, require_alpha: bool = False) -> dict[str, Any]:
    issues: list[str] = []
    inspected: list[dict[str, Any]] = []
    for raw_path in paths:
        path = pathlib.Path(raw_path)
        meta = read_png_meta(path) if path.suffix.lower() == ".png" else None
        record: dict[str, Any] = {"path": str(path), "png": bool(meta)}
        if meta:
            record.update(meta)
            size = (meta["width"], meta["height"])
            if expected_size and size != expected_size:
                issues.append(f"{path.name}: expected size {expected_size[0]}x{expected_size[1]}, got {size[0]}x{size[1]}")
            if require_alpha and meta["color_type"] != 6:
                issues.append(f"{path.name}: expected RGBA PNG with alpha, got color_type {meta['color_type']}")
        inspected.append(record)
    return {"ok": not issues, "inspected": inspected, "issues": issues}


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Call PixelLab API /v1 or /v2 endpoints.")
    parser.add_argument("method", choices=["get", "post", "patch", "poll-result-file"])
    parser.add_argument("path", help="API path such as /v2/create-image-pixflux or /v1/balance, or a prior result file for poll-result-file")
    parser.add_argument("--payload", help="Inline JSON payload")
    parser.add_argument("--payload-file", help="Path to JSON payload file")
    parser.add_argument("--download-dir", help="Directory where discovered asset-field URLs will be downloaded")
    parser.add_argument("--result-file", help="Where to write compact metadata JSON")
    parser.add_argument("--raw-result-file", help="Optional path for the full raw PixelLab JSON response")
    parser.add_argument("--poll", action="store_true", help="Poll if a background job id is returned")
    parser.add_argument("--submit-only", action="store_true", help="For async POSTs, write returned job ids immediately and exit without polling")
    parser.add_argument("--quiet", action="store_true", help="Suppress polling/retry chatter; stdout remains compact JSON")
    parser.add_argument("--summary", action="store_true", help="Print compact metadata JSON. This is the default unless --print-full-result is used.")
    parser.add_argument("--print-full-result", action="store_true", help="Print full raw JSON to stdout. Avoid in Codex runs when results may contain base64.")
    parser.add_argument("--progress-jsonl", help="Append machine-readable progress events")
    parser.add_argument("--asset-slug", default="image", help="Slug used for decoded base64 candidate filenames")
    parser.add_argument("--expect-size", help="Validate decoded/downloaded PNG dimensions, e.g. 128x128")
    parser.add_argument("--require-alpha", action="store_true", help="Validate decoded/downloaded PNGs are RGBA when possible")
    parser.add_argument("--env-file", help="Optional explicit KEY=VALUE file to load before reading PIXELLAB_API_KEY")
    parser.add_argument(
        "--allow-custom-base",
        action="store_true",
        help="Allow PIXELLAB_API_BASE to point at a trusted non-production HTTPS endpoint.",
    )
    parser.add_argument("--timeout", type=int, default=DEFAULT_TIMEOUT)
    parser.add_argument("--max-retries", type=int, default=5, help="Retry budget for GET/polling requests; POST generation calls are not retried automatically.")
    parser.add_argument("--poll-interval", type=float, default=DEFAULT_POLL_INTERVAL)
    parser.add_argument("--max-polls", type=int, default=DEFAULT_MAX_POLLS)
    parser.add_argument("--max-download-bytes", type=int, default=DEFAULT_MAX_DOWNLOAD_BYTES)
    parser.add_argument("--download-retries", type=int, default=DEFAULT_DOWNLOAD_RETRIES)
    parser.add_argument("--download-retry-delay", type=float, default=DEFAULT_DOWNLOAD_RETRY_DELAY)
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    load_explicit_env_file(args.env_file)

    api_key = os.environ.get("PIXELLAB_API_KEY")
    if not api_key:
        error = build_error_result(
            status="failed",
            method=args.method,
            path=args.path,
            payload_file=args.payload_file,
            error_code="missing_api_key",
            message="PIXELLAB_API_KEY is not set. Configure it locally; do not place it in the skill package.",
        )
        write_json_file(args.result_file, error)
        eprint(error["message"])
        return 2

    try:
        base_url = resolve_base_url(args.allow_custom_base)
        payload = None
        if args.method == "poll-result-file":
            prior_result_path = pathlib.Path(args.path)
            job_ids = load_job_ids_from_result_file(prior_result_path)
            if not job_ids:
                raise RuntimeError(f"no job ids found in {prior_result_path}")
            path = str(prior_result_path)
            result: Any = {"job_ids": job_ids}
        else:
            path = validate_api_path(args.path)
            payload = load_payload(args)
            result = request_json(
                args.method.upper(),
                f"{base_url}{path}",
                api_key,
                payload=payload,
                timeout=args.timeout,
                max_retries=args.max_retries,
                quiet=args.quiet,
            )

        job_ids = find_job_ids(result)
        if args.poll and not job_ids:
            path_job_id = job_id_from_background_job_path(path)
            if path_job_id:
                job_ids = [path_job_id]
        append_progress_event(args.progress_jsonl, {"event": "submitted", "method": args.method.upper(), "endpoint": path, "job_ids": job_ids})

        should_poll = args.poll or args.method == "poll-result-file"
        if should_poll and job_ids and args.method != "poll-result-file":
            submitted = build_compact_result(
                status="submitted",
                method=args.method,
                path=path,
                result=result,
                result_file=args.result_file,
                downloaded_files=[],
                decoded_files=[],
                discovered_urls=[],
                error=None,
            )
            write_json_file(args.result_file, submitted)
            write_json_file(args.raw_result_file, result)

        if args.submit_only:
            compact = build_compact_result(
                status="submitted",
                method=args.method,
                path=path,
                result=result,
                result_file=args.result_file,
                downloaded_files=[],
                decoded_files=[],
                discovered_urls=[],
                error=None,
            )
            write_json_file(args.result_file, compact)
            write_json_file(args.raw_result_file, result)
            print(json.dumps(result if args.print_full_result else compact, indent=2, ensure_ascii=True))
            return 0

        if should_poll and job_ids:
            polled_jobs: list[dict[str, Any]] = []
            initial_result = result
            for job_id in job_ids:
                if not args.quiet:
                    eprint(f"[info] polling background job {job_id}")
                try:
                    polled_jobs.append(
                        {
                            "job_id": job_id,
                            "result": poll_background_job(
                                base_url,
                                job_id,
                                api_key,
                                poll_interval=args.poll_interval,
                                max_polls=args.max_polls,
                                timeout=args.timeout,
                                max_retries=args.max_retries,
                                quiet=args.quiet,
                                progress_jsonl=args.progress_jsonl,
                            ),
                        }
                    )
                except TimeoutError as err:
                    timeout_result = build_error_result(
                        status="timeout",
                        method=args.method,
                        path=path,
                        payload_file=args.payload_file,
                        error_code="timeout",
                        message=str(err),
                        job_id=job_id,
                        job_ids=job_ids,
                    )
                    write_json_file(args.result_file, timeout_result)
                    append_progress_event(args.progress_jsonl, {"event": "timeout", "job_id": job_id, "endpoint": path})
                    eprint(json.dumps(timeout_result, ensure_ascii=True))
                    return 3
            if len(polled_jobs) == 1:
                result = polled_jobs[0]["result"]
            else:
                result = {
                    "initial_result": initial_result,
                    "polled_jobs": polled_jobs,
                }

        request_urls = set(iter_all_urls(payload))
        discovered_urls = [url for url in iter_asset_urls(result) if url not in request_urls]
        output: Any = result
        decoded_files: list[str] = []
        downloaded_files: list[str] = []
        download_errors: list[str] = []
        if args.download_dir:
            output_dir = pathlib.Path(args.download_dir)
            if discovered_urls:
                downloaded_files, download_errors = download_assets(
                    discovered_urls,
                    output_dir,
                    timeout=args.timeout,
                    max_bytes=args.max_download_bytes,
                    retries=args.download_retries,
                    retry_delay=args.download_retry_delay,
                )
                append_progress_event(
                    args.progress_jsonl,
                    {"event": "downloaded", "files": downloaded_files, "download_errors": download_errors},
                )
            decoded_files = save_base64_assets(result, output_dir, asset_slug=args.asset_slug)
            if decoded_files:
                append_progress_event(args.progress_jsonl, {"event": "decoded", "files": decoded_files})

        asset_validation = None
        if downloaded_files or decoded_files:
            asset_validation = validate_saved_assets(
                downloaded_files + decoded_files,
                expected_size=parse_size(args.expect_size),
                require_alpha=args.require_alpha,
            )
            if not asset_validation["ok"]:
                append_progress_event(args.progress_jsonl, {"event": "failed", "endpoint": path, "validation_issues": asset_validation["issues"]})

        error = None
        status = "completed" if not asset_validation or asset_validation["ok"] else "failed"
        if download_errors:
            error = {
                "error_code": "download_failed",
                "message": f"failed to download {len(download_errors)} discovered asset URL(s)",
            }
            if not downloaded_files and not decoded_files:
                status = "failed"
            elif status == "completed":
                status = "completed_with_download_errors"
        compact = build_compact_result(
            status=status,
            method=args.method,
            path=path,
            result=result,
            result_file=args.result_file,
            downloaded_files=downloaded_files,
            decoded_files=decoded_files,
            discovered_urls=discovered_urls,
            error=error,
            asset_validation=asset_validation,
            download_errors=download_errors,
        )
        write_json_file(args.result_file, compact)
        write_json_file(args.raw_result_file, result)
        print(json.dumps(result if args.print_full_result else compact, indent=2, ensure_ascii=True))

        return 0 if status == "completed" else 5
    except Exception as err:
        error = build_error_result(
            status="failed",
            method=args.method,
            path=args.path,
            payload_file=args.payload_file,
            error_code=classify_error_code(err),
            message=str(err),
        )
        write_json_file(args.result_file, error)
        append_progress_event(args.progress_jsonl, {"event": "failed", "endpoint": args.path, "error_code": error["error_code"], "message": error["message"]})
        eprint(json.dumps(error, ensure_ascii=True))
        return 1


if __name__ == "__main__":
    raise SystemExit(main())

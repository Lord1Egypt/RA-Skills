#!/usr/bin/env python3
"""Convert diagram images with the official LayerBack API."""

from __future__ import annotations

import argparse
import json
import os
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path
from typing import Any, Dict, Optional


DEFAULT_API_BASE_URL = "https://layerback.com/api/v1"
MAX_FILE_SIZE = 20 * 1024 * 1024
INPUT_EXTENSIONS = {".png", ".jpg", ".jpeg", ".webp"}
OUTPUT_FORMATS = ("vsdx", "pptx", "drawio", "svg", "ir", "preview")


class NoRedirect(urllib.request.HTTPRedirectHandler):
    """Expose the signed download redirect so the API key is not forwarded."""

    def redirect_request(self, req, fp, code, msg, headers, newurl):
        return None


def die(message: str, code: int = 1) -> None:
    print(f"Error: {message}", file=sys.stderr)
    raise SystemExit(code)


def decode_json(raw: bytes) -> Dict[str, Any]:
    try:
        payload = json.loads(raw.decode("utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise RuntimeError("LayerBack returned an invalid JSON response.") from exc
    if not isinstance(payload, dict):
        raise RuntimeError("LayerBack returned an unexpected response.")
    return payload


def error_message(exc: urllib.error.HTTPError) -> str:
    raw = exc.read()
    try:
        payload = decode_json(raw)
        value = payload.get("error")
        if isinstance(value, dict):
            message = value.get("message") or value.get("code")
        else:
            message = value
        if message:
            return f"HTTP {exc.code}: {message}"
    except RuntimeError:
        pass
    return f"HTTP {exc.code}: {exc.reason}"


def api_json(
    method: str,
    url: str,
    api_key: str,
    *,
    body: Optional[bytes] = None,
    content_type: Optional[str] = None,
) -> Dict[str, Any]:
    headers = {
        "Accept": "application/json",
        "User-Agent": "LayerBack-Skill/1.0",
        "x-api-key": api_key,
    }
    if content_type:
        headers["Content-Type"] = content_type
    request = urllib.request.Request(url, data=body, headers=headers, method=method)
    try:
        with urllib.request.urlopen(request, timeout=120) as response:
            return decode_json(response.read())
    except urllib.error.HTTPError as exc:
        raise RuntimeError(error_message(exc)) from exc
    except urllib.error.URLError as exc:
        raise RuntimeError(f"Network request failed: {exc.reason}") from exc


def wait_for_job(
    api_base_url: str,
    api_key: str,
    job_id: str,
    timeout_seconds: int,
) -> Dict[str, Any]:
    deadline = time.monotonic() + timeout_seconds
    job_url = f"{api_base_url}/jobs/{urllib.parse.quote(job_id, safe='')}"
    while True:
        job = api_json("GET", job_url, api_key)
        status = job.get("status")
        if status == "succeeded":
            return job
        if status == "failed":
            raise RuntimeError(str(job.get("error") or "LayerBack conversion failed."))
        if status not in {"queued", "running"}:
            raise RuntimeError(f"LayerBack returned unknown job status: {status}")
        if time.monotonic() >= deadline:
            raise RuntimeError(f"Timed out waiting for LayerBack job {job_id}.")
        time.sleep(2)


def download_artifact(
    api_base_url: str,
    api_key: str,
    job_id: str,
    output_format: str,
    destination: Path,
) -> None:
    encoded_id = urllib.parse.quote(job_id, safe="")
    encoded_format = urllib.parse.quote(output_format, safe="")
    url = f"{api_base_url}/jobs/{encoded_id}/download?format={encoded_format}"
    request = urllib.request.Request(
        url,
        headers={
            "User-Agent": "LayerBack-Skill/1.0",
            "x-api-key": api_key,
        },
        method="GET",
    )
    destination.parent.mkdir(parents=True, exist_ok=True)
    opener = urllib.request.build_opener(NoRedirect)
    try:
        with opener.open(request, timeout=120) as response:
            raw = response.read()
    except urllib.error.HTTPError as exc:
        if exc.code in {301, 302, 303, 307, 308}:
            location = exc.headers.get("Location")
            if not location:
                raise RuntimeError("LayerBack download redirect had no location.") from exc
            signed_url = urllib.parse.urljoin(url, location)
            signed_request = urllib.request.Request(
                signed_url,
                headers={"User-Agent": "LayerBack-Skill/1.0"},
                method="GET",
            )
            try:
                with urllib.request.urlopen(signed_request, timeout=120) as response:
                    raw = response.read()
            except (urllib.error.HTTPError, urllib.error.URLError) as signed_exc:
                raise RuntimeError(
                    f"Artifact download failed: {signed_exc}"
                ) from signed_exc
        else:
            raise RuntimeError(error_message(exc)) from exc
    except urllib.error.URLError as exc:
        raise RuntimeError(f"Artifact download failed: {exc.reason}") from exc
    destination.write_bytes(raw)


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Convert a diagram image with the official LayerBack API."
    )
    parser.add_argument("input", help="PNG, JPEG, or WebP diagram image.")
    parser.add_argument("--out", help="Output file path.")
    parser.add_argument("--format", choices=OUTPUT_FORMATS, default="vsdx")
    parser.add_argument(
        "--timeout",
        type=int,
        default=300,
        help="Maximum seconds to wait for conversion (default: 300).",
    )
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()

    api_key = os.getenv("LAYERBACK_API_KEY", "").strip()
    if not api_key:
        die(
            "LAYERBACK_API_KEY is required. Create one at "
            "https://layerback.com/settings/apikeys."
        )
    if args.timeout < 30:
        die("--timeout must be at least 30 seconds.")

    source = Path(args.input).expanduser().resolve()
    if not source.is_file():
        die(f"Input file does not exist: {source}")
    if source.suffix.lower() not in INPUT_EXTENSIONS:
        die("Input must be a PNG, JPEG, or WebP image.")
    file_size = source.stat().st_size
    if file_size == 0:
        die("Input file is empty.")
    if file_size > MAX_FILE_SIZE:
        die("Input file exceeds the LayerBack limit of 20 MB.")

    api_base_url = os.getenv(
        "LAYERBACK_API_BASE_URL", DEFAULT_API_BASE_URL
    ).strip().rstrip("/")
    parsed_base_url = urllib.parse.urlparse(api_base_url)
    local_hosts = {"localhost", "127.0.0.1", "::1"}
    if parsed_base_url.scheme != "https" and not (
        parsed_base_url.scheme == "http" and parsed_base_url.hostname in local_hosts
    ):
        die("LAYERBACK_API_BASE_URL must use HTTPS (HTTP is allowed for localhost).")

    destination = (
        Path(args.out).expanduser().resolve()
        if args.out
        else source.with_suffix(f".{args.format}")
    )
    started = time.monotonic()
    try:
        created = api_json(
            "POST",
            f"{api_base_url}/convert",
            api_key,
            body=source.read_bytes(),
            content_type="application/octet-stream",
        )
        job_id = str(created.get("job_id") or "")
        if not job_id:
            raise RuntimeError("LayerBack did not return a job ID.")
        job = wait_for_job(api_base_url, api_key, job_id, args.timeout)
        formats = job.get("formats") or []
        if formats and args.format not in formats:
            raise RuntimeError(
                f"Requested format {args.format} is not available for this job."
            )
        download_artifact(
            api_base_url,
            api_key,
            job_id,
            args.format,
            destination,
        )
    except RuntimeError as exc:
        die(str(exc))

    output = {
        "status": "ok",
        "backend": "layerback",
        "job_id": job_id,
        "format": args.format,
        "input": str(source),
        "out": str(destination),
        "elapsed_seconds": round(time.monotonic() - started, 2),
    }
    if args.json:
        print(json.dumps(output, ensure_ascii=False))
    else:
        print(f"Artifact saved: {destination}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

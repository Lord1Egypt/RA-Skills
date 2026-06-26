#!/usr/bin/env python3
import argparse
import base64
import binascii
import json
import os
import sys
import time
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, Optional
from urllib.parse import urlparse

import requests

BASE_URL = os.environ.get("MINIMAX_BASE_URL", "https://api.minimaxi.com")
API_KEY_ENV = "MINIMAX_API_KEY"
ROOT = Path(__file__).resolve().parents[1]
OUTPUT_DIR = ROOT / "outputs"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


class MiniMaxError(RuntimeError):
    pass


def get_api_key() -> str:
    key = os.environ.get(API_KEY_ENV)
    if not key:
        raise MiniMaxError(f"Missing {API_KEY_ENV} in environment")
    return key


def headers(extra: Optional[Dict[str, str]] = None) -> Dict[str, str]:
    h = {"Authorization": f"Bearer {get_api_key()}"}
    if extra:
        h.update(extra)
    return h


def request_json(method: str, path: str, *, params=None, json_body=None, timeout: int = 180) -> Dict[str, Any]:
    resp = requests.request(
        method,
        BASE_URL + path,
        headers=headers({"Content-Type": "application/json"}),
        params=params,
        json=json_body,
        timeout=timeout,
    )
    try:
        data = resp.json()
    except Exception as e:
        raise MiniMaxError(f"HTTP {resp.status_code} non-JSON response: {resp.text[:500]}") from e
    if resp.status_code >= 400:
        raise MiniMaxError(f"HTTP {resp.status_code}: {json.dumps(data, ensure_ascii=False)}")
    base = data.get("base_resp") or {}
    status_code = base.get("status_code", 0)
    if status_code not in (0, None):
        trace_id = data.get("trace_id")
        raise MiniMaxError(
            f"MiniMax error status_code={status_code} status_msg={base.get('status_msg')} trace_id={trace_id}"
        )
    return data


def request_multipart(path: str, *, data=None, files=None, timeout: int = 180) -> Dict[str, Any]:
    resp = requests.post(
        BASE_URL + path,
        headers={"Authorization": f"Bearer {get_api_key()}"},
        data=data,
        files=files,
        timeout=timeout,
    )
    try:
        payload = resp.json()
    except Exception as e:
        raise MiniMaxError(f"HTTP {resp.status_code} non-JSON response: {resp.text[:500]}") from e
    if resp.status_code >= 400:
        raise MiniMaxError(f"HTTP {resp.status_code}: {json.dumps(payload, ensure_ascii=False)}")
    base = payload.get("base_resp") or {}
    status_code = base.get("status_code", 0)
    if status_code not in (0, None):
        raise MiniMaxError(
            f"MiniMax error status_code={status_code} status_msg={base.get('status_msg')}"
        )
    return payload


def request_stream_download(path: str, params: Dict[str, Any], out_path: Path, timeout: int = 600) -> Path:
    out_path.parent.mkdir(parents=True, exist_ok=True)
    with requests.get(BASE_URL + path, headers=headers(), params=params, stream=True, timeout=timeout) as resp:
        if resp.status_code >= 400:
            try:
                j = resp.json()
            except Exception:
                j = {"text": resp.text[:500]}
            raise MiniMaxError(f"HTTP {resp.status_code}: {json.dumps(j, ensure_ascii=False)}")
        with out_path.open("wb") as f:
            for chunk in resp.iter_content(chunk_size=8192):
                if chunk:
                    f.write(chunk)
    return out_path


def download_url(url: str, out_path: Path, timeout: int = 600) -> Path:
    out_path.parent.mkdir(parents=True, exist_ok=True)
    with requests.get(url, stream=True, timeout=timeout) as resp:
        resp.raise_for_status()
        with out_path.open("wb") as f:
            for chunk in resp.iter_content(chunk_size=8192):
                if chunk:
                    f.write(chunk)
    return out_path


def decode_hex_to_file(hex_string: str, out_path: Path) -> Path:
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_bytes(bytes.fromhex(hex_string))
    return out_path


def timestamp_slug() -> str:
    return datetime.now().strftime("%Y%m%d-%H%M%S")


def safe_ext_from_url(url: str, fallback: str) -> str:
    parsed = urlparse(url)
    suffix = Path(parsed.path).suffix
    return suffix if suffix else fallback


def print_json(obj: Dict[str, Any]) -> None:
    print(json.dumps(obj, ensure_ascii=False, indent=2))


def add_common_output_args(parser: argparse.ArgumentParser, default_prefix: str) -> None:
    parser.add_argument("--output", help="explicit output path")
    parser.add_argument("--prefix", default=default_prefix, help="filename prefix when --output not set")


def resolve_output_path(explicit: Optional[str], prefix: str, extension: str) -> Path:
    if explicit:
        return Path(explicit).expanduser().resolve()
    return (OUTPUT_DIR / f"{prefix}-{timestamp_slug()}{extension}").resolve()


def fail(msg: str, trace_id: Optional[str] = None, **extra: Any) -> None:
    payload = {"ok": False, "error": msg}
    if trace_id:
        payload["trace_id"] = trace_id
    payload.update(extra)
    print_json(payload)
    sys.exit(1)

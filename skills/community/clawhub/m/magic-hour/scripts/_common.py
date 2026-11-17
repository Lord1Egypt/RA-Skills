"""Shared helpers for the Magic Hour ClawHub skill scripts (stdlib + magic_hour SDK)."""

from __future__ import annotations

import json
import os
import sys
from typing import Any, Dict, List, Optional

ENV_VAR = "MAGIC_HOUR_API_KEY"
DEFAULT_VIDEO_MODEL = "wan-2.2"
DEFAULT_IMAGE_MODEL = "default"
RESOLUTIONS = ("480p", "720p", "1080p")
ASPECT_RATIOS = ("16:9", "9:16", "1:1")


def _r(lo: int, hi: int) -> List[int]:
    return list(range(lo, hi + 1))


# id -> (allowed durations, credits/sec, max resolution, free)
VIDEO_MODELS: Dict[str, Dict[str, Any]] = {
    "wan-2.2": {"durations": _r(3, 10) + [15], "cps": 24, "max_res": None, "free": True},
    "ltx-2.3": {"durations": _r(1, 10) + [15, 20, 25, 30], "cps": 24, "max_res": None, "free": True},
    "minimax-h3": {"durations": _r(1, 10) + [15, 20, 25, 30], "cps": 24, "max_res": "1080p", "free": True},
    "seedance-1.5": {"durations": _r(4, 12), "cps": 30, "max_res": None, "free": False},
    "kling-2.6": {"durations": [5, 10], "cps": 36, "max_res": None, "free": False},
    "kling-3.0": {"durations": _r(3, 15), "cps": 48, "max_res": None, "free": False},
    "veo3.1-lite": {"durations": [4, 6, 8, 16, 24, 32, 40, 48, 56], "cps": 48, "max_res": None, "free": False},
    "veo3.1": {"durations": [4, 6, 8, 16, 24, 32, 40, 48, 56], "cps": 96, "max_res": None, "free": False},
    "veo3.1-audio": {"durations": [4, 6, 8, 16, 24, 32, 40, 48, 56], "cps": 96, "max_res": None, "free": False},
    "sora-2": {"durations": [4, 8, 12, 24, 36, 48, 60], "cps": 120, "max_res": "720p", "free": False},
    "seedance-2.0-mini": {"durations": _r(4, 15), "cps": 96, "max_res": "720p", "free": False},
    "seedance-2.0": {"durations": _r(4, 15), "cps": 120, "max_res": "720p", "free": False},
    "seedance-2.5": {"durations": _r(4, 30), "cps": 120, "max_res": "720p", "free": False},
}

IMAGE_MODELS = [
    "default", "gpt-image-2", "nano-banana-pro", "seedream-5-pro",
    "flux-2-klein", "z-image-turbo", "qwen-edit",
]


def get_client(api_key: Optional[str] = None, timeout: Optional[float] = None):
    key = api_key or os.environ.get(ENV_VAR)
    if not key:
        fail(
            f"{ENV_VAR} is not set. Get a free key (400 credits + 100/day, no card) "
            "at https://magichour.ai/developer"
        )
    try:
        from magic_hour import Client
    except ImportError:
        fail("magic_hour SDK not installed. Run: pip install magic_hour")
    kwargs: Dict[str, Any] = {"token": key}
    if timeout is not None:
        kwargs["timeout"] = timeout
    return Client(**kwargs)


def validate_video(model: str, duration: int, resolution: str) -> Optional[str]:
    """Return a warning string (not fatal) if the request looks invalid for the model."""
    spec = VIDEO_MODELS.get(model)
    if spec is None:
        return f"unknown model '{model}'; passing through to the API"
    problems = []
    if duration not in spec["durations"]:
        problems.append(f"duration {duration}s not in allowed {spec['durations']}")
    if spec["max_res"] and RESOLUTIONS.index(resolution) > RESOLUTIONS.index(spec["max_res"]):
        problems.append(f"resolution {resolution} exceeds max {spec['max_res']}")
    return "; ".join(problems) or None


def estimate_credits(model: str, duration: int) -> Optional[int]:
    spec = VIDEO_MODELS.get(model)
    return spec["cps"] * duration if spec else None


def _urls(response: Any) -> List[str]:
    out = []
    for item in getattr(response, "downloads", None) or []:
        url = item.get("url") if isinstance(item, dict) else getattr(item, "url", None)
        if url:
            out.append(url)
    return out


def serialize(response: Any, *, model: str, kind: str) -> Dict[str, Any]:
    urls = _urls(response)
    payload: Dict[str, Any] = {
        "project_id": getattr(response, "id", None),
        "status": getattr(response, "status", None),
        "model": model,
        "url": urls[0] if urls else None,
        "urls": urls,
        "credits_charged": getattr(response, "credits_charged", None),
    }
    if kind == "video":
        for k in ("width", "height", "fps"):
            payload[k] = getattr(response, k, None)
    paths = getattr(response, "downloaded_paths", None)
    if paths:
        payload["downloaded_paths"] = list(paths)
    err = getattr(response, "error", None)
    if err is not None:
        payload["error"] = err if isinstance(err, dict) else (
            err.model_dump() if hasattr(err, "model_dump") else {"message": str(err)}
        )
    return payload


def emit(payload: Dict[str, Any]) -> None:
    print(json.dumps(payload))


def fail(message: str, status_code: Optional[int] = None) -> None:
    payload: Dict[str, Any] = {"status": "error", "error": {"message": message}}
    if status_code is not None:
        payload["error"]["status_code"] = status_code
    print(json.dumps(payload))
    sys.exit(1)


def run(fn) -> None:
    """Run a generate callable, print JSON, exit non-zero on API errors."""
    try:
        emit(fn())
    except SystemExit:
        raise
    except Exception as exc:  # noqa: BLE001 - surface any SDK/HTTP error as JSON
        fail(str(exc), getattr(exc, "status_code", None))


def download_kwargs(download_dir: Optional[str]) -> Dict[str, Any]:
    if download_dir:
        os.makedirs(download_dir, exist_ok=True)
        return {"download_outputs": True, "download_directory": download_dir}
    return {"download_outputs": False}

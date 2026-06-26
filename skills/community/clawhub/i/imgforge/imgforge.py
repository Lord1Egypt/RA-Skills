#!/usr/bin/env python3
"""
imgforge — text-to-image via ModelScope's Z-Image-Turbo endpoint.

A lightweight CLI that talks to the ModelScope async inference API.
Uses only Python stdlib; Pillow is auto-detected for format conversion.
"""

import argparse
import json
import os
import pathlib
import sys
import time
import urllib.error
import urllib.request

_ENDPOINT = "https://api-inference.modelscope.ai"
_MODEL = "Tongyi-MAI/Z-Image-Turbo"


# ── HTTP helpers ──────────────────────────────────────────────────────

def _post(path: str, token: str, payload: dict, extra: dict | None = None) -> dict:
    hdrs = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}
    if extra:
        hdrs.update(extra)
    body = json.dumps(payload, ensure_ascii=False).encode("utf-8")
    req = urllib.request.Request(f"{_ENDPOINT}{path}", data=body, headers=hdrs, method="POST")
    with urllib.request.urlopen(req, timeout=60) as r:
        return json.loads(r.read())


def _get(path: str, token: str, extra: dict | None = None) -> dict:
    hdrs = {"Authorization": f"Bearer {token}"}
    if extra:
        hdrs.update(extra)
    req = urllib.request.Request(f"{_ENDPOINT}{path}", headers=hdrs, method="GET")
    with urllib.request.urlopen(req, timeout=60) as r:
        return json.loads(r.read())


def _fetch_bytes(url: str) -> bytes:
    with urllib.request.urlopen(url, timeout=120) as r:
        return r.read()


# ── Core logic ────────────────────────────────────────────────────────

def _create_task(token: str, prompt: str, w: int, h: int) -> str:
    resp = _post(
        "/v1/images/generations", token,
        {"model": _MODEL, "prompt": prompt, "width": w, "height": h},
        extra={"X-ModelScope-Async-Mode": "true"},
    )
    return resp["task_id"]


def _await_task(token: str, tid: str, limit: float = 150) -> str:
    end = time.monotonic() + limit
    while time.monotonic() < end:
        data = _get(f"/v1/tasks/{tid}", token, extra={"X-ModelScope-Task-Type": "image_generation"})
        st = data.get("task_status", "")
        if st == "SUCCEED":
            return data["output_images"][0]
        if st == "FAILED":
            raise RuntimeError(data.get("error", "Task failed with no details."))
        time.sleep(4)
    raise TimeoutError(f"No result after {limit:.0f}s — the API may be overloaded.")


def _save(raw: bytes, dest: pathlib.Path) -> None:
    dest.parent.mkdir(parents=True, exist_ok=True)
    try:
        from PIL import Image
        from io import BytesIO
        Image.open(BytesIO(raw)).save(dest)
    except ImportError:
        dest.write_bytes(raw)


# ── CLI ───────────────────────────────────────────────────────────────

def main() -> None:
    ap = argparse.ArgumentParser(
        prog="imgforge",
        description="Generate an image from text (free, via Z-Image-Turbo).",
    )
    ap.add_argument("prompt", help="Describe the image you want")
    ap.add_argument("-o", "--out", default="output.jpg", help="Save path (default: output.jpg)")
    ap.add_argument("-W", "--width", type=int, default=1024, help="Width 512-2048 (default: 1024)")
    ap.add_argument("-H", "--height", type=int, default=1024, help="Height 512-2048 (default: 1024)")
    ap.add_argument("--json", dest="as_json", action="store_true", help="Machine-readable JSON output")
    args = ap.parse_args()

    token = os.environ.get("MODELSCOPE_API_KEY", "")
    if not token:
        sys.exit(
            "MODELSCOPE_API_KEY is not set.\n\n"
            "Get a free token:\n"
            "  1. Alibaba Cloud  → https://www.alibabacloud.com/campaign/benefits?referral_code=A9242N\n"
            "  2. ModelScope      → https://modelscope.ai/register?inviteCode=futurizerush&invitorName=futurizerush&login=true&logintype=register\n"
            "  3. Create token    → https://modelscope.ai/my/access/token\n\n"
            "Then:  export MODELSCOPE_API_KEY='ms-...'"
        )

    dest = pathlib.Path(args.out).expanduser()
    try:
        if not args.as_json:
            print(f"[imgforge] prompt: {args.prompt[:90]}{'…' if len(args.prompt) > 90 else ''}")

        tid = _create_task(token, args.prompt, args.width, args.height)
        if not args.as_json:
            print(f"[imgforge] task {tid} — generating…")

        url = _await_task(token, tid)
        _save(_fetch_bytes(url), dest)

        if args.as_json:
            print(json.dumps({"ok": True, "path": str(dest), "task": tid}))
        else:
            print(f"[imgforge] saved → {dest}")

    except (RuntimeError, TimeoutError, urllib.error.HTTPError) as e:
        if args.as_json:
            print(json.dumps({"ok": False, "error": str(e)}))
        else:
            print(f"[imgforge] error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()

# Python reference (all platforms, zero dependencies)

> Requires Python 3.6+. Uses only stdlib (`urllib`, `json`, `base64`, `uuid`).

Save the script below as `generate.py`.

## Usage

```bash
# Text-to-image
python3 generate.py --prompt "a cute cat" --size 1024x1024 --quality low --format jpeg

# Image edit (image-to-image) — pass one or more local image paths
python3 generate.py --prompt "add a hat" --image ./cat.png --image ./hat.png --format png

# Image edit with mask
python3 generate.py --prompt "replace sky with sunset" --image ./scene.png --mask ./mask.png

# Use a different edit model
python3 generate.py --prompt "..." --image ./input.png --model flux-kontext-max
```

## Options

- `--prompt` — required, **max 1000 chars**
- `--size` — `1024x1024`, `1536x1024`, `1024x1536`, `2048x2048`, `2048x1152`, `3840x2160`, `2160x3840`, `auto`, or custom `WxH` (W,H multiples of 16; max side 3840; ratio ≤ 3:1; total pixels 655360–8294400)
- `--quality` — `low`, `medium`, `high`, `auto` (default `auto`)
- `--format` — `png`, `jpeg`, `webp`
- `--n` — number of images, **1–10** (default 1)
- `--model` — default `gpt-image-2`; for edits also accepts `gpt-image-1`, `gpt-image-1-all`, `gpt-image-2-all`, `flux-kontext-pro`, `flux-kontext-max`
- `--image PATH` — local image for editing (repeat, up to 16, total ≤ 50MB); switches to `/images/edits`
- `--mask PATH` — optional PNG mask for editing (≤ 4MB, same WxH as first image)
- `--background` — `opaque`, `auto`, `transparent` (edit only)
- `--moderation` — `low`, `auto` (edit only)

```python
#!/usr/bin/env python3
from __future__ import annotations

import argparse
import base64
import datetime as _dt
import json
import mimetypes
import os
import re
import sys
import urllib.error
import urllib.request
import uuid


API_BASE = "https://wellapi.ai/v1"
DEFAULT_MODEL = "gpt-image-2"
EDIT_MODELS = {
    "gpt-image-1", "gpt-image-1-all",
    "gpt-image-2", "gpt-image-2-all",
    "flux-kontext-pro", "flux-kontext-max",
}
PRESET_SIZES = {
    "1024x1024", "1536x1024", "1024x1536",
    "2048x2048", "2048x1152",
    "3840x2160", "2160x3840",
    "auto",
}
MAX_EDIT_IMAGES = 16
MAX_EDIT_TOTAL_BYTES = 50 * 1024 * 1024  # 50 MB
MAX_MASK_BYTES = 4 * 1024 * 1024         # 4 MB
MAX_PROMPT_CHARS = 1000

_UA = ("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
       "(KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36")


def _validate_size(size: str) -> None:
    if size in PRESET_SIZES:
        return
    m = re.fullmatch(r"(\d+)x(\d+)", size)
    if not m:
        raise ValueError(f"Invalid --size '{size}'. Use a preset (e.g. 1024x1024, auto) or WxH.")
    w, h = int(m.group(1)), int(m.group(2))
    if w % 16 or h % 16:
        raise ValueError(f"--size {size}: width and height must be multiples of 16.")
    if max(w, h) > 3840:
        raise ValueError(f"--size {size}: longest side must be ≤ 3840.")
    ratio = max(w, h) / min(w, h)
    if ratio > 3.0 + 1e-9:
        raise ValueError(f"--size {size}: ratio {ratio:.2f} exceeds 3:1.")
    total = w * h
    if total < 655_360 or total > 8_294_400:
        raise ValueError(f"--size {size}: total pixels {total} outside [655360, 8294400].")


def _post_json(url: str, api_key: str, payload: dict, timeout_s: int = 300) -> dict:
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
        "User-Agent": _UA,
        "Accept": "application/json",
    }
    data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(url, data=data, headers=headers, method="POST")
    try:
        with urllib.request.urlopen(req, timeout=timeout_s) as resp:
            body = resp.read()
    except urllib.error.HTTPError as e:
        err_body = e.read()
        raise RuntimeError(f"HTTP {e.code} {e.reason}: {err_body.decode('utf-8', 'replace')}") from None
    except urllib.error.URLError as e:
        raise RuntimeError(f"Network error: {e.reason}") from None
    try:
        return json.loads(body.decode("utf-8"))
    except Exception:
        raise RuntimeError(f"Non-JSON response: {body[:200]!r}") from None


def _post_multipart(url: str, api_key: str, fields: list, files: list, timeout_s: int = 300) -> dict:
    """fields: list of (name, str_value); files: list of (name, filename, bytes, content_type)."""
    boundary = "----WellAPIBoundary" + uuid.uuid4().hex
    parts = []
    for name, value in fields:
        parts.append(f"--{boundary}".encode())
        parts.append(f'Content-Disposition: form-data; name="{name}"'.encode())
        parts.append(b"")
        parts.append(str(value).encode("utf-8"))
    for name, filename, content, ctype in files:
        parts.append(f"--{boundary}".encode())
        parts.append(
            f'Content-Disposition: form-data; name="{name}"; filename="{filename}"'.encode("utf-8")
        )
        parts.append(f"Content-Type: {ctype}".encode())
        parts.append(b"")
        parts.append(content)
    parts.append(f"--{boundary}--".encode())
    parts.append(b"")
    body = b"\r\n".join(parts)

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": f"multipart/form-data; boundary={boundary}",
        "User-Agent": _UA,
        "Accept": "application/json",
        "Content-Length": str(len(body)),
    }
    req = urllib.request.Request(url, data=body, headers=headers, method="POST")
    try:
        with urllib.request.urlopen(req, timeout=timeout_s) as resp:
            resp_body = resp.read()
    except urllib.error.HTTPError as e:
        err_body = e.read()
        raise RuntimeError(f"HTTP {e.code} {e.reason}: {err_body.decode('utf-8', 'replace')}") from None
    except urllib.error.URLError as e:
        raise RuntimeError(f"Network error: {e.reason}") from None
    try:
        return json.loads(resp_body.decode("utf-8"))
    except Exception:
        raise RuntimeError(f"Non-JSON response: {resp_body[:200]!r}") from None


def _ext_for_format(fmt: str) -> str:
    fmt = (fmt or "").lower()
    if fmt in ("jpg", "jpeg"):
        return ".jpg"
    if fmt == "webp":
        return ".webp"
    return ".png"


def _default_out_file(ext: str, index: int = 0, total: int = 1) -> str:
    ts = _dt.datetime.now().strftime("%Y%m%d-%H%M%S-%f")
    suffix = f"-{index + 1}" if total > 1 else ""
    return f"wellapi-{ts}{suffix}{ext}"


def _resolve_api_key(cli_value: str | None) -> str:
    key = (cli_value or os.getenv("WELLAPI_API_KEY") or "").strip()
    if not key and sys.stdin.isatty():
        try:
            key = input("Enter WELLAPI_API_KEY: ").strip()
        except EOFError:
            key = ""
    return key


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(description="Generate / edit images via WellAPI gpt-image-2.")
    parser.add_argument("--api-key", default=None, help="WellAPI key (or set WELLAPI_API_KEY).")
    parser.add_argument("--prompt", required=True, help="Image prompt (max 1000 chars).")
    parser.add_argument("--model", default=DEFAULT_MODEL,
                        help=f"Model name (default {DEFAULT_MODEL}).")
    parser.add_argument("--size", default="auto", help="Image size (preset or WxH).")
    parser.add_argument("--quality", default="auto",
                        choices=["low", "medium", "high", "auto"],
                        help="Image quality (default auto).")
    parser.add_argument("--format", dest="fmt", default="png",
                        choices=["png", "jpeg", "webp"], help="Output format (default png).")
    parser.add_argument("--n", type=int, default=1, help="Number of images (1-10).")
    parser.add_argument("--image", action="append", default=None,
                        help="Local image file path for edit. Repeat for multiple (up to 16, total ≤ 50MB).")
    parser.add_argument("--mask", default=None,
                        help="Optional PNG mask for edit (≤ 4MB, same WxH as first image).")
    parser.add_argument("--background", default=None,
                        choices=["opaque", "auto", "transparent"],
                        help="Edit only: background handling.")
    parser.add_argument("--moderation", default=None,
                        choices=["low", "auto"],
                        help="Edit only: content moderation level.")
    parser.add_argument("--out", default=None,
                        help="Output filename (single image) or prefix (multi-image).")
    parser.add_argument("--verbose", action="store_true", help="Print debug info.")
    args = parser.parse_args(argv)

    api_key = _resolve_api_key(args.api_key)
    if not api_key:
        print("Error: WELLAPI_API_KEY not provided.", file=sys.stderr)
        return 2

    if len(args.prompt) > MAX_PROMPT_CHARS:
        print(f"Error: prompt exceeds {MAX_PROMPT_CHARS} chars.", file=sys.stderr)
        return 2

    if args.n < 1 or args.n > 10:
        print("Error: --n must be between 1 and 10.", file=sys.stderr)
        return 2

    try:
        _validate_size(args.size)
    except ValueError as e:
        print(f"Error: {e}", file=sys.stderr)
        return 2

    is_edit = bool(args.image)
    if is_edit:
        if len(args.image) > MAX_EDIT_IMAGES:
            print(f"Error: max {MAX_EDIT_IMAGES} reference images allowed.", file=sys.stderr)
            return 2
        total_bytes = 0
        image_payloads = []
        for p in args.image:
            if not os.path.isfile(p):
                print(f"Error: image file not found: {p}", file=sys.stderr)
                return 2
            with open(p, "rb") as f:
                content = f.read()
            total_bytes += len(content)
            ctype, _ = mimetypes.guess_type(p)
            if not ctype:
                ctype = "application/octet-stream"
            image_payloads.append((os.path.basename(p), content, ctype))
        if total_bytes > MAX_EDIT_TOTAL_BYTES:
            print(f"Error: total image size {total_bytes} bytes exceeds 50MB limit.", file=sys.stderr)
            return 2

        mask_payload = None
        if args.mask:
            if not os.path.isfile(args.mask):
                print(f"Error: mask file not found: {args.mask}", file=sys.stderr)
                return 2
            with open(args.mask, "rb") as f:
                mask_bytes = f.read()
            if len(mask_bytes) > MAX_MASK_BYTES:
                print("Error: mask exceeds 4MB limit.", file=sys.stderr)
                return 2
            mask_payload = (os.path.basename(args.mask), mask_bytes, "image/png")

        if args.model not in EDIT_MODELS:
            print(f"Warning: model '{args.model}' not in known edit-model list; sending anyway.",
                  file=sys.stderr)
    else:
        if args.mask or args.background or args.moderation:
            print("Note: --mask/--background/--moderation only apply to image edits; ignored.",
                  file=sys.stderr)

    if args.verbose:
        mode = "edit (image-to-image)" if is_edit else "text-to-image"
        print(f"Mode: {mode}")
        print(f"Model={args.model} size={args.size} quality={args.quality} "
              f"format={args.fmt} n={args.n}")

    if is_edit:
        fields = [
            ("model", args.model),
            ("prompt", args.prompt),
            ("n", str(args.n)),
            ("size", args.size),
            ("quality", args.quality),
            ("format", args.fmt),
        ]
        if args.background:
            fields.append(("background", args.background))
        if args.moderation:
            fields.append(("moderation", args.moderation))

        files = []
        for fname, content, ctype in image_payloads:
            files.append(("image", fname, content, ctype))
        if mask_payload:
            files.append(("mask", mask_payload[0], mask_payload[1], mask_payload[2]))

        resp = _post_multipart(f"{API_BASE}/images/edits", api_key, fields, files)
    else:
        payload = {
            "model": args.model,
            "prompt": args.prompt,
            "n": args.n,
            "size": args.size,
            "quality": args.quality,
            "format": args.fmt,
        }
        resp = _post_json(f"{API_BASE}/images/generations", api_key, payload)

    data = resp.get("data") or []
    if not data:
        raise RuntimeError(f"No image data in response: {resp}")

    output_format = (resp.get("output_format") or args.fmt or "png").lower()
    ext = _ext_for_format(output_format)
    total = len(data)

    for i, item in enumerate(data):
        b64 = item.get("b64_json")
        if not b64:
            raise RuntimeError(f"Missing b64_json in data[{i}]: {item}")
        try:
            img_bytes = base64.b64decode(b64)
        except Exception as e:
            raise RuntimeError(f"Invalid base64 in data[{i}]: {e}") from None

        if args.out:
            base = args.out
            root, given_ext = os.path.splitext(base)
            if total > 1:
                out_file = f"{root}-{i + 1}{given_ext or ext}"
            else:
                out_file = base if given_ext else base + ext
        else:
            out_file = _default_out_file(ext, i, total)

        out_file = os.path.abspath(out_file)
        with open(out_file, "wb") as f:
            f.write(img_bytes)

        if args.verbose:
            print(f"Saved: {out_file} ({len(img_bytes)} bytes)")
        print(f"MEDIA:{out_file}")

    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main(sys.argv[1:]))
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        raise SystemExit(1)
```

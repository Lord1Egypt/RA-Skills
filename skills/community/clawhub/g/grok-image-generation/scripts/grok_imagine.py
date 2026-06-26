#!/usr/bin/env python3
import argparse
import base64
import json
import mimetypes
import os
import sys
import time
from pathlib import Path
from urllib import request, error

BASE_URL = "https://api.x.ai/v1"
DEFAULT_MODEL = "grok-imagine-image-quality"


def http_json(url: str, payload: dict, api_key: str) -> dict:
    data = json.dumps(payload).encode("utf-8")
    req = request.Request(
        url,
        data=data,
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        },
        method="POST",
    )
    try:
        with request.urlopen(req, timeout=300) as resp:
            return json.loads(resp.read().decode("utf-8", errors="replace"))
    except error.HTTPError as e:
        body = e.read().decode("utf-8", errors="replace")
        raise RuntimeError(f"HTTP {e.code}: {body}")
    except error.URLError as e:
        raise RuntimeError(f"Request failed: {e}")


def image_to_data_uri(path: Path) -> str:
    mime, _ = mimetypes.guess_type(path.name)
    if not mime:
        mime = "image/png"
    raw = path.read_bytes()
    return f"data:{mime};base64,{base64.b64encode(raw).decode('ascii')}"


def ext_from_item(item: dict) -> str:
    mime = (item.get("mime_type") or "").lower()
    if "jpeg" in mime or "jpg" in mime:
        return ".jpg"
    if "webp" in mime:
        return ".webp"
    if "png" in mime:
        return ".png"
    return ".png"


def download(url: str, dest: Path):
    with request.urlopen(url, timeout=300) as resp:
        dest.write_bytes(resp.read())


def save_outputs(result: dict, out_dir: Path, prefix: str) -> list[str]:
    out_dir.mkdir(parents=True, exist_ok=True)
    data = result.get("data", [])
    ts = time.strftime("%Y%m%d_%H%M%S")
    saved: list[str] = []
    for i, item in enumerate(data, start=1):
        base = out_dir / f"{prefix}_{ts}_{i:02d}"
        if item.get("b64_json"):
            path = base.with_suffix(ext_from_item(item))
            path.write_bytes(base64.b64decode(item["b64_json"]))
            saved.append(str(path))
        elif item.get("url"):
            path = base.with_suffix(ext_from_item(item))
            download(item["url"], path)
            saved.append(str(path))
        else:
            path = base.with_suffix(".json")
            path.write_text(json.dumps(item, indent=2, ensure_ascii=False), encoding="utf-8")
            saved.append(str(path))
    meta = out_dir / f"{prefix}_{ts}_response.json"
    meta.write_text(json.dumps(result, indent=2, ensure_ascii=False), encoding="utf-8")
    saved.append(str(meta))
    return saved


def cmd_generate(args) -> int:
    payload = {
        "model": args.model,
        "prompt": args.prompt,
        "n": args.n,
        "aspect_ratio": args.aspect_ratio,
        "resolution": args.resolution,
        "response_format": args.response_format,
    }
    result = http_json(f"{BASE_URL}/images/generations", payload, args.api_key)
    saved = save_outputs(result, Path(args.output_dir), args.prefix)
    print(json.dumps({"mode": "generate", "model": args.model, "files": saved}, ensure_ascii=False))
    return 0


def build_edit_image_payload(paths: list[str], urls: list[str]) -> list[dict] | dict:
    refs: list[dict] = []
    for p in paths:
        uri = image_to_data_uri(Path(p))
        refs.append({"url": uri, "type": "image_url"})
    for u in urls:
        refs.append({"url": u, "type": "image_url"})
    if not refs:
        raise RuntimeError("Provide at least one --image or --image-url for edit mode")
    if len(refs) == 1:
        return refs[0]
    if len(refs) > 3:
        raise RuntimeError("xAI image edit supports up to 3 source images")
    return refs


def cmd_edit(args) -> int:
    image_payload = build_edit_image_payload(args.image or [], args.image_url or [])
    payload = {
        "model": args.model,
        "prompt": args.prompt,
        "image": image_payload,
        "n": args.n,
        "response_format": args.response_format,
    }
    if args.aspect_ratio:
        payload["aspect_ratio"] = args.aspect_ratio
    if args.resolution:
        payload["resolution"] = args.resolution
    result = http_json(f"{BASE_URL}/images/edits", payload, args.api_key)
    saved = save_outputs(result, Path(args.output_dir), args.prefix)
    print(json.dumps({"mode": "edit", "model": args.model, "files": saved}, ensure_ascii=False))
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description="Generate or edit images with xAI Grok Imagine")
    parser.add_argument("--api-key", default=os.environ.get("XAI_API_KEY"))
    sub = parser.add_subparsers(dest="mode", required=True)

    g = sub.add_parser("generate", help="Generate new images from a prompt")
    g.add_argument("prompt")
    g.add_argument("--model", default=DEFAULT_MODEL)
    g.add_argument("--n", type=int, default=1)
    g.add_argument("--aspect-ratio", default="1:1")
    g.add_argument("--resolution", default="1k")
    g.add_argument("--response-format", choices=["url", "b64_json"], default="url")
    g.add_argument("--output-dir", default=str(Path.cwd() / "output" / "grok-images"))
    g.add_argument("--prefix", default="grok-gen")
    g.set_defaults(func=cmd_generate)

    e = sub.add_parser("edit", help="Edit one to three source images with a prompt")
    e.add_argument("prompt")
    e.add_argument("--image", action="append", help="Local image path; repeat up to 3 times")
    e.add_argument("--image-url", action="append", help="Public image URL; repeat up to 3 times")
    e.add_argument("--model", default=DEFAULT_MODEL)
    e.add_argument("--n", type=int, default=1)
    e.add_argument("--aspect-ratio", default=None)
    e.add_argument("--resolution", default=None)
    e.add_argument("--response-format", choices=["url", "b64_json"], default="url")
    e.add_argument("--output-dir", default=str(Path.cwd() / "output" / "grok-images"))
    e.add_argument("--prefix", default="grok-edit")
    e.set_defaults(func=cmd_edit)

    args = parser.parse_args()
    if not args.api_key:
        print("XAI_API_KEY is not set", file=sys.stderr)
        return 2
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())

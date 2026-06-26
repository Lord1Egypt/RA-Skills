#!/usr/bin/env python3
import argparse
import base64
import mimetypes
from pathlib import Path
from typing import List

from common import (
    MiniMaxError,
    decode_hex_to_file,
    download_url,
    print_json,
    request_json,
    resolve_output_path,
    add_common_output_args,
    safe_ext_from_url,
)


def file_to_data_url(path: str) -> str:
    p = Path(path).expanduser().resolve()
    mime, _ = mimetypes.guess_type(str(p))
    if not mime:
        mime = "image/png"
    b64 = base64.b64encode(p.read_bytes()).decode("ascii")
    return f"data:{mime};base64,{b64}"


def normalize_image_ref(value: str) -> str:
    if value.startswith("http://") or value.startswith("https://") or value.startswith("data:"):
        return value
    return file_to_data_url(value)


def save_base64_image(data: str, out_path: Path) -> Path:
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_bytes(base64.b64decode(data))
    return out_path


def main() -> None:
    ap = argparse.ArgumentParser(description="MiniMax image generation wrapper")
    ap.add_argument("--model", default="image-01")
    ap.add_argument("--prompt", required=True)
    ap.add_argument("--aspect-ratio", default="1:1", choices=["1:1", "16:9", "4:3", "3:2", "2:3", "3:4", "9:16", "21:9"])
    ap.add_argument("--width", type=int)
    ap.add_argument("--height", type=int)
    ap.add_argument("--response-format", default="url", choices=["url", "base64"])
    ap.add_argument("--seed", type=int)
    ap.add_argument("-n", type=int, default=1)
    ap.add_argument("--prompt-optimizer", action="store_true")
    ap.add_argument("--watermark", action="store_true")
    ap.add_argument("--style-type")
    ap.add_argument("--style-weight", type=float, default=0.8)
    ap.add_argument(
        "--subject-reference",
        action="append",
        default=[],
        help="reference image URL, data URL, or local path; repeatable",
    )
    ap.add_argument("--subject-type", default="character")
    add_common_output_args(ap, "image")
    args = ap.parse_args()

    body = {
        "model": args.model,
        "prompt": args.prompt,
        "response_format": args.response_format,
        "n": args.n,
        "prompt_optimizer": args.prompt_optimizer,
        "aigc_watermark": args.watermark,
    }
    if args.aspect_ratio:
        body["aspect_ratio"] = args.aspect_ratio
    if args.width is not None and args.height is not None:
        body["width"] = args.width
        body["height"] = args.height
    if args.seed is not None:
        body["seed"] = args.seed
    if args.style_type:
        body["style"] = {
            "style_type": args.style_type,
            "style_weight": args.style_weight,
        }
    if args.subject_reference:
        body["subject_reference"] = [
            {"type": args.subject_type, "image_file": normalize_image_ref(item)} for item in args.subject_reference
        ]

    try:
        data = request_json("POST", "/v1/image_generation", json_body=body, timeout=600)
    except MiniMaxError as e:
        raise SystemExit(str(e))

    trace_id = data.get("trace_id")
    data_obj = data.get("data") or {}
    urls: List[str] = data_obj.get("image_urls") or []
    b64s: List[str] = data_obj.get("image_base64") or []
    paths = []

    if args.response_format == "url":
        for i, url in enumerate(urls, 1):
            out_path = resolve_output_path(None, f"{args.prefix}-{i}", ".png")
            ext = safe_ext_from_url(url, ".png")
            out_path = out_path.with_suffix(ext)
            download_url(url, out_path)
            paths.append(str(out_path))
    else:
        for i, image_b64 in enumerate(b64s, 1):
            out_path = resolve_output_path(None, f"{args.prefix}-{i}", ".png")
            save_base64_image(image_b64, out_path)
            paths.append(str(out_path))

    print_json(
        {
            "ok": True,
            "trace_id": trace_id,
            "id": data.get("id"),
            "paths": paths,
            "count": len(paths),
            "meta": data.get("metadata") or {},
        }
    )


if __name__ == "__main__":
    main()

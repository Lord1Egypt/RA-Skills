#!/usr/bin/env python3
"""OpenClaw Seedream image generation (M1/M2)."""
from __future__ import annotations

import sys, os
import uuid
from typing import Any

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'scripts'))


from common.base_image import run_task, parse_common_args
from common.task_client import parse_images


def _parse_images(value: str | None) -> list[str] | None:
    return parse_images(value)


def run(
    version: str,
    prompt: str,
    negative_prompt: str | None = None,
    resolution: str = "2048*2048",
    images: str | list[str] | None = None,
    is_sequential_image: bool = False,
    img_count: int = 1,
    request_id: str | None = None,
    authorization: str | None = None,
) -> dict[str, Any]:
    """
    Run Seedream image generation task.

    Args:
        version: "M1" or "M2"
        prompt: Text prompt
        negative_prompt: Negative prompt
        resolution: "WIDTH*HEIGHT" string (e.g., "2048*2048")
        images: Comma-separated file paths (str) or list of base64 strings
        is_sequential_image: Enable sequential image mode
        img_count: Number of images to generate
        request_id: Optional request ID
        authorization: Optional Bearer token
    """
    if request_id is None:
        request_id = str(uuid.uuid4())

    final_images = []
    if isinstance(images, str):
        final_images = parse_images(images)
    elif isinstance(images, list):
        final_images = images

    # Validate
    if not is_sequential_image and img_count > 4:
        raise ValueError("img_count must be <= 4 when is_sequential_image is False.")
    
    try:
        w_str, h_str = resolution.split("*")
        w, h = int(w_str), int(h_str)
    except Exception as exc:
        raise ValueError(f"Invalid resolution format: {resolution}. Use WIDTH*HEIGHT.") from exc

    if max(w, h) / min(w, h) > 16:
        raise ValueError(f"Resolution ratio {resolution} is not supported.")
    
    pixels = w * h
    if pixels > 4096 * 4096:
        raise ValueError(f"Resolution {resolution} is too large.")
    
    if version == "M2":
        if pixels < 2560 * 1440:
            raise ValueError(f"Resolution {resolution} is too small for M2.")
    else:
        if pixels < 1280 * 720:
            raise ValueError(f"Resolution {resolution} is too small for M1.")

    payload = {
        "module": "hidream-M",
        "version": version,
        "request_id": request_id,
        "prompt": prompt,
        "negative_prompt": negative_prompt,
        "images": final_images,
        "resolution": resolution,
        "is_sequential_image": is_sequential_image,
        "img_count": img_count,
    }

    return run_task(payload, authorization)


def parse_args():
    parser = parse_common_args("Seedream image generation")
    parser.add_argument(
        "--version",
        required=True,
        choices=["M1", "M2"],
        help="Seedream version.",
    )
    parser.add_argument("--prompt", required=True, help="Text prompt.")
    parser.add_argument("--negative-prompt", help="Negative prompt.")
    parser.add_argument("--images", help="Comma-separated image URLs/base64.")
    parser.add_argument(
        "--resolution",
        default="2048*2048",
        help="Output resolution WIDTH*HEIGHT.",
    )
    parser.add_argument(
        "--is-sequential-image",
        action="store_true",
        help="Enable sequential image mode.",
    )
    parser.add_argument(
        "--img-count",
        type=int,
        default=1,
        help="Requested output image count.",
    )
    args = parser.parse_args()
    return args


def main_entry() -> int:
    args = parse_args()
    try:
        result = run(
            version=args.version,
            prompt=args.prompt,
            negative_prompt=args.negative_prompt,
            resolution=args.resolution,
            images=args.images,
            is_sequential_image=args.is_sequential_image,
            img_count=args.img_count,
            request_id=args.request_id,
            authorization=args.authorization,
        )
        import json
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return 0
    except Exception as exc:
        print(str(exc), file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main_entry())

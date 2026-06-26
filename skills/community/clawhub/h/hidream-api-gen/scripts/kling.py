#!/usr/bin/env python3
"""OpenClaw Kling video generation."""

from __future__ import annotations
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "scripts"))

import uuid
from typing import Any

from common.base_video import run_task, parse_common_args
from common.task_client import parse_images


def run(
    version: str,
    prompt: str = "",
    negative_prompt: str = "",
    images: str | list[str] | None = None,
    sound: str = "off",
    wh_ratio: str | None = None,
    duration: int = 5,
    request_id: str | None = None,
    authorization: str | None = None,
) -> dict[str, Any]:
    """
    Run Kling video generation task.
    
    Args:
        version: Model version (e.g., "Q2.5T-std")
        prompt: Text prompt
        negative_prompt: Negative prompt
        images: Comma-separated file paths (str) or list of base64 strings
        sound: "on" or "off"
        wh_ratio: Aspect ratio (e.g., "16:9")
        duration: Duration in seconds (5 or 10)
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
    if sound == "on":
        if version != "Q2.6-pro":
            raise ValueError("sound=on only supported by Q2.6-pro.")
        if not final_images:
            raise ValueError("sound=on requires image inputs.")

    payload = {
        "module": "hidream-Q2",
        "version": version,
        "request_id": request_id,
        "prompt": prompt,
        "negative_prompt": negative_prompt,
        "images": final_images,
        "sound": sound,
        "wh_ratio": wh_ratio,
        "duration": duration,
    }
    
    return run_task(payload, authorization)


def parse_args():
    parser = parse_common_args("Kling video generation")
    parser.add_argument(
        "--version",
        required=True,
        choices=["Q2.5T-std", "Q2.5T-pro", "Q2.6-pro"],
        help="Kling model version.",
    )
    parser.add_argument("--prompt", default="", help="Text prompt.")
    parser.add_argument("--negative-prompt", default="", help="Negative prompt.")
    parser.add_argument("--images", help="Comma-separated image URLs/base64.")
    parser.add_argument(
        "--sound",
        choices=["on", "off"],
        default="off",
        help="Enable sound (only Q2.6-pro image-to-video).",
    )
    parser.add_argument(
        "--wh-ratio",
        choices=["16:9", "9:16", "1:1"],
        help="Aspect ratio (only when no images).",
    )
    parser.add_argument(
        "--duration",
        type=int,
        choices=[5, 10],
        default=5,
        help="Video duration seconds.",
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
            images=args.images,
            sound=args.sound,
            wh_ratio=args.wh_ratio,
            duration=args.duration,
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

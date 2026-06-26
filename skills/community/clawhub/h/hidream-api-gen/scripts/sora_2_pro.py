#!/usr/bin/env python3
"""OpenClaw Sora 2 Pro video generation."""
from __future__ import annotations
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "scripts"))


from typing import Any

from common.base_video import main, parse_common_args
from common.task_client import parse_images


def _parse_images(value: str | None) -> list[str] | None:
    return parse_images(value)


def build_payload(args) -> dict[str, Any]:
    return {
        "module": "sora",
        "version": "sora-2-p",
        "request_id": args.request_id,
        "prompt": args.prompt,
        "images": _parse_images(args.images),
        "resolution": args.resolution,
        "wh_ratio": args.wh_ratio,
        "duration": args.duration,
    }


def parse_args():
    parser = parse_common_args("Sora 2 Pro video generation")
    parser.add_argument("--prompt", required=True, help="Text prompt.")
    parser.add_argument("--images", help="Comma-separated image URLs/base64.")
    parser.add_argument(
        "--resolution",
        required=True,
        choices=["720p", "1080p"],
        help="Video resolution.",
    )
    parser.add_argument(
        "--wh-ratio",
        required=True,
        choices=["9:16", "16:9"],
        help="Video aspect ratio.",
    )
    parser.add_argument(
        "--duration",
        required=True,
        type=int,
        choices=[4, 8, 12],
        help="Video duration seconds.",
    )
    return parser.parse_args()


def main_entry() -> int:
    args = parse_args()
    payload = build_payload(args)
    return main(payload, args)


if __name__ == "__main__":
    raise SystemExit(main_entry())

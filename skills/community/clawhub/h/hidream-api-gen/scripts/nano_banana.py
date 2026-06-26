#!/usr/bin/env python3
"""OpenClaw Nano Banana image generation."""

from __future__ import annotations
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "scripts"))

from typing import Any

from common.base_image import main, parse_common_args
from common.task_client import parse_images


def _parse_images(value: str | None) -> list[str] | None:
    return parse_images(value)


def build_payload(args) -> dict[str, Any]:
    return {
        "module": "hidream-G",
        "version": args.version,
        "request_id": args.request_id,
        "prompt": args.prompt,
        "images": _parse_images(args.images),
        "resolution": args.resolution,
        "wh_ratio": args.wh_ratio,
        "img_count": args.img_count,
    }


def parse_args():
    parser = parse_common_args("Nano Banana image generation")
    parser.add_argument(
        "--version",
        required=True,
        choices=["G-pro", "G-std"],
        help="Nano Banana version.",
    )
    parser.add_argument("--prompt", required=True, help="Text prompt.")
    parser.add_argument("--images", help="Comma-separated image URLs/base64.")
    parser.add_argument(
        "--resolution",
        required=True,
        choices=["1K", "2K", "4K"],
        help="Output resolution.",
    )
    parser.add_argument(
        "--wh-ratio",
        required=True,
        choices=[
            "1:1",
            "2:3",
            "3:2",
            "3:4",
            "4:3",
            "4:5",
            "5:4",
            "9:16",
            "16:9",
            "21:9",
            "keep",
        ],
        help="Output aspect ratio.",
    )
    parser.add_argument(
        "--img-count",
        type=int,
        default=1,
        choices=[1, 2, 3, 4],
        help="Image count.",
    )
    return parser.parse_args()


def main_entry() -> int:
    args = parse_args()
    payload = build_payload(args)
    return main(payload, args)


if __name__ == "__main__":
    raise SystemExit(main_entry())

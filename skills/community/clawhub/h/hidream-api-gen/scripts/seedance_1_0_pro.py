#!/usr/bin/env python3
"""OpenClaw Seedance 1.0 Pro video generation."""

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
        "module": "hidream-R",
        "version": "R1",
        "request_id": args.request_id,
        "prompt": args.prompt,
        "images": _parse_images(args.images),
        "duration": args.duration,
        "wh_ratio": args.wh_ratio,
        "resolution": args.resolution,
        "generate_audio": args.generate_audio,
    }


def parse_args():
    parser = parse_common_args("Seedance 1.0 Pro video generation")
    parser.add_argument("--prompt", required=True, help="Text prompt.")
    parser.add_argument("--images", help="Comma-separated image URLs/base64.")
    parser.add_argument(
        "--duration",
        type=int,
        choices=[5, 10],
        default=5,
        help="Video duration seconds.",
    )
    parser.add_argument(
        "--wh-ratio",
        choices=["16:9", "9:16", "1:1", "4:3", "3:4", "adaptive"],
        default="adaptive",
        help="Video aspect ratio.",
    )
    parser.add_argument(
        "--resolution",
        choices=["480p", "720p", "1080p"],
        default="480p",
        help="Video resolution.",
    )
    parser.add_argument(
        "--generate-audio",
        default=False,
        help="Generate audio.",
    )
    return parser.parse_args()


def main_entry() -> int:
    args = parse_args()
    payload = build_payload(args)
    return main(payload, args)


if __name__ == "__main__":
    raise SystemExit(main_entry())

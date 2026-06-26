#!/usr/bin/env python3
"""OpenClaw Minimax Hailuo 02 video generation."""

from __future__ import annotations
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "scripts"))

from typing import Any

from common.base_video import main, parse_common_args
from common.task_client import parse_images


def _parse_images(value: str | None) -> list[str] | None:
    return parse_images(value)


def _validate(args) -> None:
    if args.duration == 10 and args.resolution == "1080p":
        raise ValueError("1080p resolution does not support 10s duration.")
    images = _parse_images(args.images)
    if images and len(images) == 2 and args.resolution == "512p":
        raise ValueError("512p resolution does not support first/last frames.")


def build_payload(args) -> dict[str, Any]:
    return {
        "module": "mnmax",
        "version": "hl-02",
        "request_id": args.request_id,
        "prompt": args.prompt,
        "duration": args.duration,
        "resolution": args.resolution,
        "images": _parse_images(args.images),
    }


def parse_args():
    parser = parse_common_args("Minimax Hailuo 02 video generation")
    parser.add_argument("--prompt", required=True, help="Text prompt.")
    parser.add_argument("--images", help="Comma-separated image URLs/base64.")
    parser.add_argument(
        "--duration",
        type=int,
        choices=[6, 10],
        default=6,
        help="Video duration seconds.",
    )
    parser.add_argument(
        "--resolution",
        choices=["512p", "768p", "1080p"],
        default="768p",
        help="Video resolution.",
    )
    args = parser.parse_args()
    _validate(args)
    return args


def main_entry() -> int:
    args = parse_args()
    payload = build_payload(args)
    return main(payload, args)


if __name__ == "__main__":
    raise SystemExit(main_entry())

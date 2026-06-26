from __future__ import annotations

import argparse

from ima_runtime.shared.config import DEFAULT_BASE_URL, VIDEO_TASK_TYPES


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="IMA AI Creation Script — reliable task creation via Open API",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument(
        "--api-key",
        required=False,
        help="IMA Open API key (starts with ima_). Can also use IMA_API_KEY env var",
    )
    parser.add_argument("--task-type", required=True, choices=list(VIDEO_TASK_TYPES), help="Task type to create")
    parser.add_argument("--model-id", help="Model ID from product list")
    parser.add_argument("--version-id", help="Specific version ID — overrides latest")
    parser.add_argument("--prompt", help="Generation prompt (required unless --list-models)")
    parser.add_argument(
        "--input-images",
        nargs="*",
        action="append",
        default=[],
        help="Input image URLs or local file paths (for image_to_video, first_last_frame_to_video, etc.). "
        "Can be repeated multiple times; values are merged. "
        "Local files will be automatically uploaded using the API key.",
    )
    parser.add_argument(
        "--reference-images",
        nargs="*",
        action="append",
        default=[],
        help="Reference image URLs or local file paths for reference_image_to_video. "
        "Can be repeated multiple times; values are merged.",
    )
    parser.add_argument(
        "--reference-videos",
        nargs="*",
        action="append",
        default=[],
        help="Reference video URLs or local file paths for Seedance reference_image_to_video. "
        "Can be repeated multiple times; values are merged.",
    )
    parser.add_argument(
        "--reference-audios",
        nargs="*",
        action="append",
        default=[],
        help="Reference audio URLs or local file paths for Seedance reference_image_to_video. "
        "Can be repeated multiple times; values are merged.",
    )
    parser.add_argument("--size", help="Optional size override")
    parser.add_argument("--extra-params", help='JSON string of extra parameters, e.g. \'{"duration":"5"}\'')
    parser.add_argument("--language", default="en", help="Language for product labels (en/zh)")
    parser.add_argument("--base-url", default=DEFAULT_BASE_URL, help="API base URL")
    parser.add_argument("--user-id", default="default", help="User ID for preference memory")
    parser.add_argument("--list-models", action="store_true", help="List all available models for --task-type and exit")
    parser.add_argument("--output-json", action="store_true", help="Output final result as JSON (for agent parsing)")
    return parser

from __future__ import annotations

import argparse

from ima_runtime.shared.config import DEFAULT_BASE_URL, IMAGE_TASK_TYPES


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="IMA Image Creation Script — specialized for image generation via Open API",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument(
        "--api-key",
        required=False,
        help="IMA Open API key (starts with ima_). Can also use IMA_API_KEY env var",
    )
    parser.add_argument(
        "--task-type",
        required=True,
        choices=list(IMAGE_TASK_TYPES),
        help="Task type: text_to_image or image_to_image",
    )
    parser.add_argument("--model-id", help="Model ID from product list (e.g. doubao-seedream-4.5)")
    parser.add_argument("--version-id", help="Specific version ID — overrides auto-select of latest")
    parser.add_argument("--prompt", help="Generation prompt (required unless --list-models)")
    parser.add_argument(
        "--input-images",
        nargs="*",
        action="append",
        default=[],
        help="Input image URLs or local file paths (required for image_to_image). "
        "Can be repeated multiple times; values are merged. "
        "Local files will be automatically uploaded using the API key.",
    )
    parser.add_argument("--size", help="Override size parameter (e.g. 4k, 2k, 2048x2048)")
    parser.add_argument("--extra-params", help='JSON string of extra inner parameters, e.g. \'{"n":2}\'')
    parser.add_argument("--language", default="en", help="Language for product labels (en/zh)")
    parser.add_argument("--base-url", default=DEFAULT_BASE_URL, help="API base URL")
    parser.add_argument("--user-id", default="default", help="User ID for preference memory")
    parser.add_argument("--list-models", action="store_true", help="List all available models for --task-type and exit")
    parser.add_argument("--output-json", action="store_true", help="Output final result as JSON (for agent parsing)")
    return parser

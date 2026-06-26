#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import os
import sys
from types import SimpleNamespace

from ima_logger import cleanup_old_logs, setup_logger
from parse_user_request import parse_request
from validate_params import validate_request

from ima_runtime.cli_flow import run_cli


def _flatten_media(values) -> list[str]:
    result: list[str] = []
    for value in values or []:
        if isinstance(value, list):
            result.extend(str(v) for v in value if str(v).strip())
        elif value is not None and str(value).strip():
            result.append(str(value))
    return result


def _split_media_by_type(parsed: dict) -> tuple[list[list[str]], list[list[str]], list[list[str]], list[list[str]]]:
    input_images: list[str] = []
    reference_images: list[str] = []
    reference_videos: list[str] = []
    reference_audios: list[str] = []
    task_type = parsed["task_type"]
    for asset in parsed["media_assets"]:
        if task_type == "image_to_video":
            input_images.append(asset["source"])
        elif task_type == "first_last_frame_to_video":
            input_images.append(asset["source"])
        elif task_type == "reference_image_to_video":
            if asset["media_type"] == "image":
                reference_images.append(asset["source"])
            elif asset["media_type"] == "video":
                reference_videos.append(asset["source"])
            elif asset["media_type"] == "audio":
                reference_audios.append(asset["source"])
    return ([input_images] if input_images else [], [reference_images] if reference_images else [], [reference_videos] if reference_videos else [], [reference_audios] if reference_audios else [])


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Parse, validate, route, and optionally execute a free-form video generation request")
    parser.add_argument("--request", required=True, help="Free-form user request")
    parser.add_argument("--media", nargs="*", action="append", default=[], help="Optional media paths or URLs referenced by the request")
    parser.add_argument("--api-key", help="IMA API key; falls back to IMA_API_KEY")
    parser.add_argument("--base-url", default="https://api.imastudio.com", help="API base URL")
    parser.add_argument("--language", default="en", help="Catalog language")
    parser.add_argument("--user-id", default="default", help="User ID for preference memory")
    parser.add_argument("--dry-run", action="store_true", help="Only parse and validate; do not execute")
    parser.add_argument("--output-json", action="store_true", help="Output structured result as JSON")
    return parser


def main() -> int:
    args = build_parser().parse_args()
    api_key = args.api_key or os.getenv("IMA_API_KEY")
    if not api_key:
        print("IMA_API_KEY is required.", file=sys.stderr)
        return 1

    media = _flatten_media(args.media)
    parsed = parse_request(args.request, media)
    validated = validate_request(args.request, media, base_url=args.base_url, api_key=api_key, language=args.language)
    if args.dry_run or validated.get("status") != "ok":
        payload = {"parsed": parsed, "validated": validated}
        if args.output_json:
            print(json.dumps(payload, ensure_ascii=False, indent=2))
        else:
            print(payload)
        return 0 if validated.get("status") == "ok" else 1

    input_images, reference_images, reference_videos, reference_audios = _split_media_by_type(parsed)
    constraints = dict(parsed.get("constraints") or {})
    cli_args = SimpleNamespace(
        api_key=api_key,
        base_url=args.base_url,
        task_type=validated["task_type"],
        language=args.language,
        list_models=False,
        output_json=args.output_json,
        model_id=validated["selected_model"]["model_id"],
        user_id=args.user_id,
        input_images=input_images,
        reference_images=reference_images,
        reference_videos=reference_videos,
        reference_audios=reference_audios,
        prompt=parsed["generation_prompt"],
        version_id=validated["selected_model"].get("version_id"),
        size=None,
        extra_params=json.dumps(constraints) if constraints else None,
    )

    logger = setup_logger("ima_skills")
    cleanup_old_logs(days=7)
    return run_cli(cli_args, logger=logger)


if __name__ == "__main__":
    sys.exit(main())

#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import re
import sys
from typing import Any

from ima_runtime.shared.media_utils import detect_media_type


MODEL_ALIAS_PATTERNS = (
    ("ima-pro-fast", (r"\bima-pro-fast\b", r"\bseedance 2\.0 fast\b", r"\bvideo pro fast\b", r"\b极速\b")),
    ("ima-pro", (r"\bima-pro\b", r"\bseedance 2\.0\b", r"\bvideo pro\b", r"\b专业版\b", r"\b高质量\b")),
    ("kling-video-o1", (r"\bkling o1\b", r"\bkling\b")),
    ("wan2.6-i2v", (r"\bwan 2\.6\b", r"\bwan\b")),
)


def _flatten_media(values) -> list[str]:
    result: list[str] = []
    for value in values or []:
        if isinstance(value, list):
            result.extend(str(v) for v in value if str(v).strip())
        elif value is not None and str(value).strip():
            result.append(str(value))
    return result


def _extract_duration(text: str) -> int | None:
    match = re.search(r"(\d{1,2})\s*(?:s|sec|secs|second|seconds|秒)", text, re.IGNORECASE)
    return int(match.group(1)) if match else None


def _extract_resolution(text: str) -> str | None:
    match = re.search(r"\b(480p|540p|720p|768p|1080p|1080P|720P)\b", text, re.IGNORECASE)
    return match.group(1) if match else None


def _extract_aspect_ratio(text: str) -> str | None:
    match = re.search(r"\b(1:1|4:3|3:4|16:9|9:16|21:9)\b", text)
    if match:
        return match.group(1)
    if re.search(r"\badaptive\b|\bauto\b|自适应", text, re.IGNORECASE):
        return "adaptive"
    return None


def _extract_audio_toggle(text: str) -> bool | None:
    if re.search(r"\bsilent\b|\bmute\b|无声|静音", text, re.IGNORECASE):
        return False
    if re.search(r"\bwith audio\b|\bvoiceover\b|\bbgm\b|\bmusic\b|带音频|有声音|旁白|配音", text, re.IGNORECASE):
        return True
    return None


def _extract_model_id(text: str) -> str | None:
    lowered = text.lower()
    for model_id, patterns in MODEL_ALIAS_PATTERNS:
        for pattern in patterns:
            if re.search(pattern, lowered, re.IGNORECASE):
                return model_id
    return None


def _semantic_intent(text: str) -> dict[str, bool]:
    lowered = text.lower()
    return {
        "speed_priority": bool(re.search(r"\bquick\b|\bfast\b|\bdraft\b|\bpreview\b|\blow[- ]?cost\b|快速|预览|草稿|省点", lowered)),
        "quality_priority": bool(re.search(r"\bcinematic\b|\bfinal\b|\bhigh quality\b|\bquality\b|\bpremium\b|\bfilm\b|电影感|最终|高质量|高保真|高清|超清|高画质|成片", lowered)),
        "reference_intent": bool(re.search(r"\breference\b|\bstyle\b|\bsame character\b|\bconsistency\b|参考|风格|一致性", lowered)),
        "first_last_intent": bool(re.search(r"\bfirst frame\b|\blast frame\b|\bstart frame\b|\bend frame\b|首帧|尾帧|从.*到", lowered)),
        "animate_intent": bool(re.search(r"\banimate\b|\bmake .* move\b|让.*动起来|图生视频", lowered)),
    }


def _build_media_assets(media: list[str]) -> list[dict[str, str]]:
    assets: list[dict[str, str]] = []
    for source in media:
        media_type = detect_media_type(source)
        assets.append({"source": source, "media_type": media_type})
    return assets


def parse_request(request: str, media: list[str] | None = None) -> dict[str, Any]:
    media = media or []
    semantic = _semantic_intent(request)
    media_assets = _build_media_assets(media)
    media_types = {asset["media_type"] for asset in media_assets}
    text = request.strip()

    constraints: dict[str, Any] = {}
    duration = _extract_duration(text)
    if duration is not None:
        constraints["duration"] = duration
    resolution = _extract_resolution(text)
    if resolution is not None:
        constraints["resolution"] = resolution
    aspect_ratio = _extract_aspect_ratio(text)
    if aspect_ratio is not None:
        constraints["aspect_ratio"] = aspect_ratio
    audio_toggle = _extract_audio_toggle(text)
    if audio_toggle is not None:
        constraints["audio"] = audio_toggle

    explicit_model_id = _extract_model_id(text)

    clarification: dict[str, Any] | None = None
    task_type = "text_to_video"
    video_mode = None

    if semantic["first_last_intent"]:
        video_mode = "first_last_frame"
        task_type = "first_last_frame_to_video"
    elif semantic["reference_intent"]:
        video_mode = "reference"
        task_type = "reference_image_to_video"
    elif "video" in media_types or "audio" in media_types:
        video_mode = "reference"
        task_type = "reference_image_to_video"
    elif len(media_assets) == 1 and any(asset["media_type"] == "image" for asset in media_assets):
        task_type = "image_to_video"
    elif len(media_assets) >= 2:
        clarification = {
            "reason": "video image roles ambiguous",
            "question": "这些素材分别是什么角色？是首帧/尾帧，还是参考图/参考视频，还是只让其中一张图动起来？",
            "options": ("首帧/尾帧", "参考素材", "只动其中一张"),
        }
        task_type = "undetermined"

    return {
        "request": text,
        "generation_prompt": text,
        "task_type": task_type,
        "intent_hints": {k: v for k, v in {"task_type": None if task_type == "undetermined" else task_type, "video_mode": video_mode}.items() if v is not None},
        "constraints": constraints,
        "semantic_intent": semantic,
        "explicit_model_id": explicit_model_id,
        "media_assets": media_assets,
        "clarification": clarification,
    }


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Parse a free-form user request into a structured video generation intent")
    parser.add_argument("--request", required=True, help="Free-form user request")
    parser.add_argument("--media", nargs="*", action="append", default=[], help="Optional media paths or URLs referenced by the request")
    parser.add_argument("--output-json", action="store_true", help="Output parsed structure as JSON")
    return parser


def main() -> int:
    args = build_parser().parse_args()
    parsed = parse_request(args.request, _flatten_media(args.media))
    if args.output_json:
        print(json.dumps(parsed, ensure_ascii=False, indent=2))
    else:
        print(parsed)
    return 0


if __name__ == "__main__":
    sys.exit(main())

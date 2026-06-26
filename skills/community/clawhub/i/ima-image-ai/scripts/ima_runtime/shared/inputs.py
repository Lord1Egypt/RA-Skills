from __future__ import annotations

import logging
import mimetypes
import os
from pathlib import Path

from ima_runtime.shared.client import get_upload_token, upload_to_oss
from ima_runtime.shared.config import DEFAULT_IM_BASE_URL

logger = logging.getLogger("ima_skills")


def flatten_input_images_args(raw_groups) -> list[str]:
    flattened: list[str] = []
    for group in raw_groups or []:
        if isinstance(group, list):
            flattened.extend([str(v) for v in group if str(v).strip()])
        elif group is not None and str(group).strip():
            flattened.append(str(group))
    return flattened


def validate_and_filter_inputs(task_type: str, input_images: list[str]) -> list[str]:
    if task_type == "text_to_image":
        return []
    if task_type == "image_to_image" and len(input_images) < 1:
        raise ValueError("image_to_image requires at least 1 input image")
    return input_images


def prepare_image_url(source: str | bytes, api_key: str, im_base_url: str = DEFAULT_IM_BASE_URL) -> str:
    if isinstance(source, str) and source.startswith("https://"):
        logger.info("Using URL directly: %s", source[:50])
        return source

    if not api_key:
        raise RuntimeError("Local image upload requires IMA API key (--api-key)")

    if isinstance(source, str):
        if not os.path.isfile(source):
            raise RuntimeError(f"Image file not found: {source}")
        ext = Path(source).suffix.lstrip(".").lower() or "jpeg"
        with open(source, "rb") as handle:
            image_bytes = handle.read()
        content_type = mimetypes.guess_type(source)[0] or "image/jpeg"
    else:
        image_bytes = source
        ext = "jpeg"
        content_type = "image/jpeg"

    token_data = get_upload_token(api_key, ext, content_type, im_base_url)
    ful = token_data.get("ful")
    fdl = token_data.get("fdl")
    if not ful or not fdl:
        raise RuntimeError("Upload token missing 'ful' or 'fdl' field")
    upload_to_oss(image_bytes, content_type, ful)
    return fdl

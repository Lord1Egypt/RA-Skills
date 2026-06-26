from __future__ import annotations

import logging
import mimetypes
import os
from pathlib import Path

from ima_runtime.shared.client import get_upload_token, upload_to_oss
from ima_runtime.shared.config import DEFAULT_IM_BASE_URL
from ima_runtime.shared.media_utils import assert_public_https_url, detect_media_type
from ima_runtime.shared.types import MediaAsset


logger = logging.getLogger("ima_skills")


def flatten_input_images_args(raw_groups) -> list[str]:
    flattened: list[str] = []
    for group in raw_groups or []:
        if isinstance(group, list):
            flattened.extend([str(v) for v in group if str(v).strip()])
        elif group is not None and str(group).strip():
            flattened.append(str(group))
    return flattened


def flatten_media_args(raw_groups) -> list[str]:
    return flatten_input_images_args(raw_groups)


def build_cli_media_assets(
    task_type: str,
    *,
    input_images,
    reference_images,
    reference_videos,
    reference_audios,
) -> tuple[MediaAsset, ...]:
    input_sources = flatten_media_args(input_images)
    reference_image_sources = flatten_media_args(reference_images)
    reference_video_sources = flatten_media_args(reference_videos)
    reference_audio_sources = flatten_media_args(reference_audios)
    assets: list[MediaAsset] = []

    if task_type == "text_to_video":
        if input_sources or reference_image_sources or reference_video_sources or reference_audio_sources:
            raise ValueError("text_to_video does not accept media inputs")
        return ()

    if task_type == "image_to_video":
        if reference_image_sources or reference_video_sources or reference_audio_sources:
            raise ValueError("image_to_video does not accept reference media flags")
        if len(input_sources) != 1:
            raise ValueError("image_to_video requires exactly 1 input image")
        return (MediaAsset(source=input_sources[0], media_type="image", role="image_input"),)

    if task_type == "first_last_frame_to_video":
        if reference_image_sources or reference_video_sources or reference_audio_sources:
            raise ValueError("first_last_frame_to_video does not accept reference media flags")
        if len(input_sources) != 2:
            raise ValueError("first_last_frame_to_video requires exactly 2 input images")
        return (
            MediaAsset(source=input_sources[0], media_type="image", role="first_frame"),
            MediaAsset(source=input_sources[1], media_type="image", role="last_frame"),
        )

    if task_type == "reference_image_to_video":
        legacy_reference_sources = input_sources + reference_image_sources
        for source in legacy_reference_sources:
            media_type = detect_media_type(source)
            if media_type == "video":
                assets.append(MediaAsset(source=source, media_type="video", role="reference_video"))
            elif media_type == "audio":
                assets.append(MediaAsset(source=source, media_type="audio", role="reference_audio"))
            else:
                assets.append(MediaAsset(source=source, media_type="image", role="reference_image"))
        assets.extend(MediaAsset(source=source, media_type="video", role="reference_video") for source in reference_video_sources)
        assets.extend(MediaAsset(source=source, media_type="audio", role="reference_audio") for source in reference_audio_sources)
        if not assets:
            raise ValueError("reference_image_to_video requires at least 1 reference input")
        return tuple(assets)

    return tuple(assets)


def validate_and_filter_inputs(task_type: str, input_images: list[str]) -> list[str]:
    if task_type == "text_to_video":
        return []
    if task_type == "image_to_video" and len(input_images) != 1:
        raise ValueError("image_to_video requires exactly 1 input image")
    if task_type == "first_last_frame_to_video" and len(input_images) != 2:
        raise ValueError("first_last_frame_to_video requires exactly 2 input images")
    if task_type == "reference_image_to_video" and len(input_images) < 1:
        raise ValueError("reference_image_to_video requires at least 1 input image")
    return input_images


def validate_task_inputs(task_type: str, input_images: list[str], media_assets: tuple[MediaAsset, ...] = ()) -> list[str]:
    if not media_assets:
        return validate_and_filter_inputs(task_type, input_images)

    if task_type == "text_to_video":
        if media_assets:
            raise ValueError("text_to_video does not accept media inputs")
        return []
    if task_type == "image_to_video":
        if len(media_assets) != 1 or media_assets[0].media_type != "image":
            raise ValueError("image_to_video requires exactly 1 input image")
        return [media_assets[0].source]
    if task_type == "first_last_frame_to_video":
        if len(media_assets) != 2 or any(asset.media_type != "image" for asset in media_assets):
            raise ValueError("first_last_frame_to_video requires exactly 2 input images")
        return [asset.source for asset in media_assets]
    if task_type == "reference_image_to_video":
        if not media_assets:
            raise ValueError("reference_image_to_video requires at least 1 reference input")
        return [asset.source for asset in media_assets if asset.media_type == "image"]
    return input_images


def prepare_media_url(
    source: str | bytes,
    api_key: str,
    *,
    media_type: str = "image",
    im_base_url: str = DEFAULT_IM_BASE_URL,
) -> str:
    """
    Convert any supported media source to a public HTTPS CDN URL.

    - If source is already HTTPS URL → return as-is
    - If source is local file/bytes → upload to OSS first
    """
    if isinstance(source, str) and source.startswith("https://"):
        assert_public_https_url(source)
        logger.info(f"Using URL directly: {source[:50]}...")
        return source
    if isinstance(source, str) and source.startswith("http://"):
        raise RuntimeError(f"Only HTTPS remote media URLs are supported: {source}")

    if not api_key:
        raise RuntimeError(f"Local {media_type} upload requires IMA API key (--api-key)")

    if isinstance(source, str):
        if not os.path.isfile(source):
            raise RuntimeError(f"{media_type.capitalize()} file not found: {source}")

        default_ext = {"image": "jpeg", "video": "mp4", "audio": "mp3"}.get(media_type, "bin")
        ext = Path(source).suffix.lstrip(".").lower() or default_ext
        with open(source, "rb") as f:
            media_bytes = f.read()
        default_type = {
            "image": "image/jpeg",
            "video": "video/mp4",
            "audio": "audio/mpeg",
        }.get(media_type, "application/octet-stream")
        content_type = mimetypes.guess_type(source)[0] or default_type
        logger.info(f"Read local file: {source} ({len(media_bytes)} bytes)")
    else:
        media_bytes = source
        ext = {"image": "jpeg", "video": "mp4", "audio": "mp3"}.get(media_type, "bin")
        content_type = {
            "image": "image/jpeg",
            "video": "video/mp4",
            "audio": "audio/mpeg",
        }.get(media_type, "application/octet-stream")
        logger.info(f"Using raw bytes ({len(media_bytes)} bytes)")

    token_data = get_upload_token(api_key, ext, content_type, im_base_url)
    ful = token_data.get("ful")
    fdl = token_data.get("fdl")

    if not ful or not fdl:
        raise RuntimeError("Upload token missing 'ful' or 'fdl' field")

    upload_to_oss(media_bytes, content_type, ful)
    logger.info(f"{media_type.capitalize()} uploaded: {fdl[:50]}...")
    return fdl


def prepare_image_url(source: str | bytes, api_key: str,
                      im_base_url: str = DEFAULT_IM_BASE_URL) -> str:
    return prepare_media_url(source, api_key, media_type="image", im_base_url=im_base_url)

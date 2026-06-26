from __future__ import annotations

import mimetypes
import os
from pathlib import Path

from ima_runtime.shared.inputs import prepare_media_url
from ima_runtime.shared.media_utils import (
    detect_media_type,
    download_remote_media_to_temp,
    extract_video_cover_frame,
    get_audio_duration,
    get_image_dimensions,
    get_video_metadata,
    is_remote_url,
)
from ima_runtime.shared.reference_validation import AUDIO_MAX_BYTES, IMAGE_MAX_BYTES, REQUEST_MAX_BYTES, VIDEO_MAX_BYTES
from ima_runtime.shared.seedance_capabilities import is_seedance_model
from ima_runtime.shared.types import MediaAsset, MediaPayloadBundle, PreparedMediaAsset


REMOTE_DOWNLOAD_CAPS = {
    "image": IMAGE_MAX_BYTES,
    "video": VIDEO_MAX_BYTES,
    "audio": AUDIO_MAX_BYTES,
}


def infer_supported_media_types(task_type: str, model_info: dict) -> set[str]:
    if task_type in {"image_to_video", "first_last_frame_to_video"}:
        return {"image"}
    if task_type != "reference_image_to_video":
        return set()

    accept_types = model_info.get("files_accept_types") or []
    supported: set[str] = set()
    for item in accept_types:
        value = str(item).lower()
        if value.startswith("image/"):
            supported.add("image")
        elif value.startswith("video/"):
            supported.add("video")
        elif value.startswith("audio/"):
            supported.add("audio")
    return supported or {"image"}


def model_supports_media(task_type: str, model_info: dict, media_assets: tuple[MediaAsset, ...]) -> bool:
    supported = infer_supported_media_types(task_type, model_info)
    return all(asset.media_type in supported for asset in media_assets)


def filter_models_for_media_support(task_type: str, models: list[dict], media_assets: tuple[MediaAsset, ...]) -> list[dict]:
    if not media_assets:
        return models
    return [model for model in models if model_supports_media(task_type, model, media_assets)]


def validate_model_media_support(task_type: str, model_info: dict, media_assets: tuple[MediaAsset, ...]) -> None:
    if task_type in {"image_to_video", "first_last_frame_to_video"}:
        if any(asset.media_type != "image" for asset in media_assets):
            raise ValueError(f"{task_type} only supports image inputs.")
        return

    if task_type != "reference_image_to_video":
        return

    supported = infer_supported_media_types(task_type, model_info)
    unsupported = [asset.media_type for asset in media_assets if asset.media_type not in supported]
    if unsupported:
        model_id = model_info.get("model_id") or "<unknown-model>"
        raise ValueError(
            f"{model_id} does not support reference media types in reference_image_to_video: "
            f"{', '.join(sorted(set(unsupported)))}."
        )


def _download_and_probe_remote(source: str, media_type: str) -> tuple[str, int]:
    suffix = Path(source).suffix or {
        "image": ".jpg",
        "video": ".mp4",
        "audio": ".mp3",
    }.get(media_type, "")
    temp_path = download_remote_media_to_temp(
        source,
        suffix=suffix,
        max_bytes=REMOTE_DOWNLOAD_CAPS.get(media_type, REQUEST_MAX_BYTES),
    )
    size_bytes = os.path.getsize(temp_path)
    return temp_path, size_bytes


def _extract_metadata_for_path(path: str, media_type: str) -> dict:
    if media_type == "image":
        width, height = get_image_dimensions(path)
        return {"width": width, "height": height}
    if media_type == "video":
        return get_video_metadata(path)
    if media_type == "audio":
        return {"duration": get_audio_duration(path)}
    return {}


def _build_video_cover_url(path: str, api_key: str) -> str:
    try:
        cover_path = extract_video_cover_frame(path)
    except Exception:
        return ""
    try:
        return prepare_media_url(cover_path, api_key, media_type="image")
    finally:
        if os.path.exists(cover_path):
            os.unlink(cover_path)


def prepare_media_assets(media_assets: tuple[MediaAsset, ...], api_key: str) -> tuple[PreparedMediaAsset, ...]:
    prepared: list[PreparedMediaAsset] = []
    for asset in media_assets:
        temp_path = None
        try:
            if is_remote_url(asset.source):
                if asset.source.startswith("http://"):
                    raise RuntimeError(f"Only HTTPS remote media URLs are supported: {asset.source}")
                temp_path, size_bytes = _download_and_probe_remote(asset.source, asset.media_type)
                metadata = _extract_metadata_for_path(temp_path, asset.media_type)
                url = asset.source
                cover_url = _build_video_cover_url(temp_path, api_key) if asset.media_type == "video" else ""
            else:
                if not os.path.isfile(asset.source):
                    raise RuntimeError(f"{asset.media_type.capitalize()} file not found: {asset.source}")
                size_bytes = os.path.getsize(asset.source)
                metadata = _extract_metadata_for_path(asset.source, asset.media_type)
                url = prepare_media_url(asset.source, api_key, media_type=asset.media_type)
                cover_url = _build_video_cover_url(asset.source, api_key) if asset.media_type == "video" else ""

            prepared.append(
                PreparedMediaAsset(
                    source=asset.source,
                    media_type=asset.media_type,
                    role=asset.role,
                    url=url,
                    width=int(metadata.get("width", 0) or 0),
                    height=int(metadata.get("height", 0) or 0),
                    duration=float(metadata.get("duration", 0.0) or 0.0),
                    fps=float(metadata.get("fps", 0.0) or 0.0),
                    cover_url=cover_url,
                    size_bytes=size_bytes,
                )
            )
        finally:
            if temp_path and os.path.exists(temp_path):
                os.unlink(temp_path)
    return tuple(prepared)


def build_media_payload_bundle(task_type: str, model_id: str, prepared_assets: tuple[PreparedMediaAsset, ...]) -> MediaPayloadBundle:
    input_urls = tuple(asset.url for asset in prepared_assets)
    if task_type != "reference_image_to_video" or not is_seedance_model(model_id):
        return MediaPayloadBundle(input_images=input_urls)

    src_image = tuple(
        {
            "url": asset.url,
            "width": asset.width,
            "height": asset.height,
        }
        for asset in prepared_assets
        if asset.media_type == "image"
    )
    src_video = tuple(
        {
            "url": asset.url,
            "duration": int(asset.duration) if asset.duration else 0,
            "width": asset.width,
            "height": asset.height,
            "cover": asset.cover_url,
        }
        for asset in prepared_assets
        if asset.media_type == "video"
    )
    src_audio = tuple(
        {
            "url": asset.url,
            "duration": int(asset.duration) if asset.duration else 0,
        }
        for asset in prepared_assets
        if asset.media_type == "audio"
    )
    return MediaPayloadBundle(
        input_images=input_urls,
        src_image=src_image,
        src_video=src_video,
        src_audio=src_audio,
    )

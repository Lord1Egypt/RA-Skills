from __future__ import annotations

from ima_runtime.shared.types import PreparedMediaAsset


class ReferenceInputValidationError(RuntimeError):
    """Raised when Seedance reference media does not meet preflight requirements."""


IMAGE_MAX_BYTES = 30 * 1024 * 1024
VIDEO_MAX_BYTES = 50 * 1024 * 1024
AUDIO_MAX_BYTES = 15 * 1024 * 1024
REQUEST_MAX_BYTES = 64 * 1024 * 1024

VIDEO_MIN_DURATION = 2.0
VIDEO_MAX_DURATION = 15.0
AUDIO_MIN_DURATION = 2.0
AUDIO_MAX_DURATION = 15.0
VIDEO_MIN_DIMENSION = 300
VIDEO_MAX_DIMENSION = 6000
IMAGE_MIN_DIMENSION = 300
IMAGE_MAX_DIMENSION = 6000
MIN_ASPECT_RATIO = 0.4
MAX_ASPECT_RATIO = 2.5
VIDEO_MIN_PIXELS = 409600
VIDEO_MAX_PIXELS = 927408
VIDEO_MIN_FPS = 24.0
VIDEO_MAX_FPS = 60.0

IMAGE_EXTENSIONS = {"jpg", "jpeg", "png", "webp", "bmp", "tiff", "tif", "gif"}
VIDEO_EXTENSIONS = {"mp4", "mov"}
AUDIO_EXTENSIONS = {"wav", "mp3"}


def _format_bytes(num_bytes: int) -> str:
    units = ["B", "KB", "MB", "GB"]
    value = float(num_bytes)
    for unit in units:
        if value < 1024 or unit == units[-1]:
            return f"{value:.1f} {unit}"
        value /= 1024
    return f"{num_bytes} B"


def _build_issue(source: str, message: str, actual: str | None = None, allowed: str | None = None, fix: str | None = None) -> str:
    parts = [f"- {source}: {message}"]
    if actual is not None:
        parts.append(f"current={actual}")
    if allowed is not None:
        parts.append(f"allowed={allowed}")
    if fix is not None:
        parts.append(f"fix={fix}")
    return " | ".join(parts)


def _assert_range(source: str, label: str, value: float, minimum: float, maximum: float, issues: list[str], fix: str) -> None:
    if value < minimum or value > maximum:
        issues.append(
            _build_issue(source, f"{label} out of range", actual=str(value), allowed=f"[{minimum}, {maximum}]", fix=fix)
        )


def validate_seedance_reference_assets(media_items: tuple[PreparedMediaAsset, ...]) -> None:
    if not media_items:
        raise ReferenceInputValidationError(
            "reference_image_to_video requires at least 1 reference input (image, video, or audio)."
        )

    issues: list[str] = []
    images = [item for item in media_items if item.media_type == "image"]
    videos = [item for item in media_items if item.media_type == "video"]
    audios = [item for item in media_items if item.media_type == "audio"]

    if len(images) > 9:
        issues.append(f"reference images exceed limit | current={len(images)} | allowed=0~9")
    if len(videos) > 3:
        issues.append(f"reference videos exceed limit | current={len(videos)} | allowed=0~3")
    if len(audios) > 3:
        issues.append(f"reference audios exceed limit | current={len(audios)} | allowed=0~3")

    total_size = sum(item.size_bytes for item in media_items)
    if total_size > REQUEST_MAX_BYTES:
        issues.append(
            _build_issue("all reference assets", "total request size exceeds limit", _format_bytes(total_size), f"<= {_format_bytes(REQUEST_MAX_BYTES)}", "reduce file count or size")
        )

    total_video_duration = sum(item.duration for item in videos)
    if total_video_duration > VIDEO_MAX_DURATION:
        issues.append(_build_issue("all reference videos", "total video duration exceeds limit", f"{total_video_duration:.2f}s", f"<= {VIDEO_MAX_DURATION:.0f}s", "trim reference videos"))

    total_audio_duration = sum(item.duration for item in audios)
    if total_audio_duration > AUDIO_MAX_DURATION:
        issues.append(_build_issue("all reference audios", "total audio duration exceeds limit", f"{total_audio_duration:.2f}s", f"<= {AUDIO_MAX_DURATION:.0f}s", "trim reference audios"))

    for item in images:
        ext = item.source.rsplit(".", 1)[-1].lower() if "." in item.source else ""
        if ext and ext not in IMAGE_EXTENSIONS:
            issues.append(_build_issue(item.source, "unsupported image format", ext, "jpeg/png/webp/bmp/tiff/gif", "convert image format"))
        if item.size_bytes >= IMAGE_MAX_BYTES:
            issues.append(_build_issue(item.source, "image too large", _format_bytes(item.size_bytes), f"< {_format_bytes(IMAGE_MAX_BYTES)}", "compress image"))
        _assert_range(item.source, "image width", item.width, IMAGE_MIN_DIMENSION, IMAGE_MAX_DIMENSION, issues, "resize image width")
        _assert_range(item.source, "image height", item.height, IMAGE_MIN_DIMENSION, IMAGE_MAX_DIMENSION, issues, "resize image height")
        if item.width > 0 and item.height > 0:
            aspect_ratio = item.width / item.height
            _assert_range(item.source, "image aspect ratio", round(aspect_ratio, 4), MIN_ASPECT_RATIO, MAX_ASPECT_RATIO, issues, "crop image ratio")

    for item in videos:
        ext = item.source.rsplit(".", 1)[-1].lower() if "." in item.source else ""
        if ext and ext not in VIDEO_EXTENSIONS:
            issues.append(_build_issue(item.source, "unsupported video format", ext, "mp4/mov", "transcode video"))
        if item.size_bytes > VIDEO_MAX_BYTES:
            issues.append(_build_issue(item.source, "video too large", _format_bytes(item.size_bytes), f"<= {_format_bytes(VIDEO_MAX_BYTES)}", "compress video"))
        _assert_range(item.source, "video duration", round(item.duration, 3), VIDEO_MIN_DURATION, VIDEO_MAX_DURATION, issues, "trim video to 2~15s")
        _assert_range(item.source, "video width", item.width, VIDEO_MIN_DIMENSION, VIDEO_MAX_DIMENSION, issues, "resize video width")
        _assert_range(item.source, "video height", item.height, VIDEO_MIN_DIMENSION, VIDEO_MAX_DIMENSION, issues, "resize video height")
        if item.width > 0 and item.height > 0:
            aspect_ratio = item.width / item.height
            pixels = item.width * item.height
            _assert_range(item.source, "video aspect ratio", round(aspect_ratio, 4), MIN_ASPECT_RATIO, MAX_ASPECT_RATIO, issues, "crop video ratio")
            _assert_range(item.source, "video pixels", pixels, VIDEO_MIN_PIXELS, VIDEO_MAX_PIXELS, issues, "resize video resolution")
        _assert_range(item.source, "video fps", round(item.fps, 3), VIDEO_MIN_FPS, VIDEO_MAX_FPS, issues, "change video fps")

    for item in audios:
        ext = item.source.rsplit(".", 1)[-1].lower() if "." in item.source else ""
        if ext and ext not in AUDIO_EXTENSIONS:
            issues.append(_build_issue(item.source, "unsupported audio format", ext, "wav/mp3", "convert audio"))
        if item.size_bytes > AUDIO_MAX_BYTES:
            issues.append(_build_issue(item.source, "audio too large", _format_bytes(item.size_bytes), f"<= {_format_bytes(AUDIO_MAX_BYTES)}", "compress audio"))
        _assert_range(item.source, "audio duration", round(item.duration, 3), AUDIO_MIN_DURATION, AUDIO_MAX_DURATION, issues, "trim audio to 2~15s")

    if issues:
        raise ReferenceInputValidationError(
            "Reference inputs do not meet Seedance requirements:\n" + "\n".join(issues)
        )


def validate_seedance_image_assets(task_type: str, media_items: tuple[PreparedMediaAsset, ...]) -> None:
    expected_count = 1 if task_type == "image_to_video" else 2
    if len(media_items) != expected_count or any(item.media_type != "image" for item in media_items):
        raise ReferenceInputValidationError(f"{task_type} requires exactly {expected_count} image inputs for Seedance.")
    for item in media_items:
        if item.size_bytes >= IMAGE_MAX_BYTES:
            raise ReferenceInputValidationError(f"{item.source} exceeds the 30MB image limit.")
        if item.width < IMAGE_MIN_DIMENSION or item.width > IMAGE_MAX_DIMENSION:
            raise ReferenceInputValidationError(f"{item.source} image width is outside 300~6000 px.")
        if item.height < IMAGE_MIN_DIMENSION or item.height > IMAGE_MAX_DIMENSION:
            raise ReferenceInputValidationError(f"{item.source} image height is outside 300~6000 px.")
        if item.width > 0 and item.height > 0:
            aspect_ratio = item.width / item.height
            if aspect_ratio < MIN_ASPECT_RATIO or aspect_ratio > MAX_ASPECT_RATIO:
                raise ReferenceInputValidationError(f"{item.source} image aspect ratio is outside 0.4~2.5.")

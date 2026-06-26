"""
Reference media preflight validation for reference_image_to_video.
"""

import mimetypes
import os
import tempfile
from pathlib import Path
from typing import Optional
from urllib.parse import urlparse

import requests

from ima_media_upload import is_remote_url
from ima_media_utils import detect_media_type, extract_media_metadata


class ReferenceInputValidationError(RuntimeError):
    """Raised when reference media does not meet preflight requirements."""


IMAGE_EXTENSIONS = {"jpg", "jpeg", "png", "webp", "bmp", "tiff", "tif", "gif"}
VIDEO_EXTENSIONS = {"mp4", "mov"}
AUDIO_EXTENSIONS = {"wav", "mp3"}

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


def _format_bytes(num_bytes: int) -> str:
    units = ["B", "KB", "MB", "GB"]
    value = float(num_bytes)
    for unit in units:
        if value < 1024 or unit == units[-1]:
            return f"{value:.1f} {unit}"
        value /= 1024
    return f"{num_bytes} B"


def _format_source_label(source: str) -> str:
    return Path(urlparse(source).path).name or source


def _infer_extension(source: str, content_type: str | None = None) -> str:
    ext = Path(urlparse(source).path).suffix.lstrip(".").lower()
    if ext:
        return ext
    if content_type:
        guessed = mimetypes.guess_extension(content_type.split(";")[0].strip()) or ""
        return guessed.lstrip(".").lower()
    return ""


def _detect_media_type_from_extension(ext: str) -> str:
    if ext in IMAGE_EXTENSIONS:
        return "image"
    if ext in VIDEO_EXTENSIONS:
        return "video"
    if ext in AUDIO_EXTENSIONS:
        return "audio"
    return "unknown"


def _build_issue(source: str, message: str, actual: Optional[str] = None, allowed: Optional[str] = None, fix: Optional[str] = None) -> str:
    parts = [f"- {_format_source_label(source)}: {message}"]
    if actual is not None:
        parts.append(f"当前值: {actual}")
    if allowed is not None:
        parts.append(f"允许范围: {allowed}")
    if fix is not None:
        parts.append(f"建议调整: {fix}")
    return " | ".join(parts)


def _assert_range(source: str, label: str, value: float, minimum: float, maximum: float, issues: list[str], fix: str) -> None:
    if value < minimum or value > maximum:
        issues.append(
            _build_issue(
                source,
                f"{label} 不符合要求",
                actual=str(value),
                allowed=f"[{minimum}, {maximum}]",
                fix=fix,
            )
        )


def _download_remote_for_probe(url: str, max_bytes: int) -> tuple[str, int, str | None]:
    with requests.get(url, stream=True, timeout=30) as response:
        response.raise_for_status()
        content_type = response.headers.get("Content-Type")
        content_length = response.headers.get("Content-Length")
        if content_length and int(content_length) > max_bytes:
            raise ReferenceInputValidationError(
                _build_issue(
                    url,
                    "远程资源大小超限",
                    actual=_format_bytes(int(content_length)),
                    allowed=f"≤ {_format_bytes(max_bytes)}",
                    fix="压缩文件或改用更小的参考资源",
                )
            )

        suffix = _infer_extension(url, content_type)
        with tempfile.NamedTemporaryFile(delete=False, suffix=f".{suffix}" if suffix else "") as temp_file:
            total = 0
            for chunk in response.iter_content(chunk_size=1024 * 64):
                if not chunk:
                    continue
                total += len(chunk)
                if total > max_bytes:
                    temp_file.close()
                    os.unlink(temp_file.name)
                    raise ReferenceInputValidationError(
                        _build_issue(
                            url,
                            "远程资源大小超限",
                            actual=f">{_format_bytes(max_bytes)}",
                            allowed=f"≤ {_format_bytes(max_bytes)}",
                            fix="压缩文件或改用更小的参考资源",
                        )
                    )
                temp_file.write(chunk)
            return temp_file.name, total, content_type


def inspect_reference_source(source: str) -> dict:
    """
    Probe local or remote media and return normalized metadata for validation.
    """
    if is_remote_url(source):
        ext = _infer_extension(source)
        media_type = _detect_media_type_from_extension(ext)
        if media_type == "unknown":
            raise ReferenceInputValidationError(
                _build_issue(
                    source,
                    "无法从远程 URL 判断媒体类型",
                    fix="请提供带明确扩展名的直链，或改为本地文件再上传",
                )
            )
        max_bytes = {
            "image": IMAGE_MAX_BYTES,
            "video": VIDEO_MAX_BYTES,
            "audio": AUDIO_MAX_BYTES,
        }[media_type]
        temp_path, size_bytes, content_type = _download_remote_for_probe(source, max_bytes)
        try:
            ext = _infer_extension(source, content_type) or Path(temp_path).suffix.lstrip(".").lower()
            metadata = extract_media_metadata(temp_path, media_type, source)
        finally:
            if os.path.exists(temp_path):
                os.unlink(temp_path)
    else:
        if not os.path.isfile(source):
            raise ReferenceInputValidationError(
                _build_issue(
                    source,
                    "本地文件不存在",
                    fix="检查文件路径，或改用可访问的远程 URL",
                )
            )
        media_type = detect_media_type(source)
        ext = Path(source).suffix.lstrip(".").lower()
        size_bytes = os.path.getsize(source)
        metadata = extract_media_metadata(source, media_type, source)

    return {
        "source": source,
        "label": _format_source_label(source),
        "media_type": media_type,
        "extension": ext,
        "size_bytes": size_bytes,
        **metadata,
    }


def validate_reference_image_to_video_inputs(media_items: list[dict]) -> None:
    """
    Validate multimodal reference inputs before task creation.
    """
    if not media_items:
        raise ReferenceInputValidationError(
            "reference_image_to_video 至少需要 1 个参考输入（图片、视频或音频）。"
        )

    issues: list[str] = []
    images = [item for item in media_items if item["media_type"] == "image"]
    videos = [item for item in media_items if item["media_type"] == "video"]
    audios = [item for item in media_items if item["media_type"] == "audio"]
    unknowns = [item for item in media_items if item["media_type"] == "unknown"]

    if unknowns:
        for item in unknowns:
            issues.append(
                _build_issue(
                    item["source"],
                    "媒体类型无法识别",
                    fix="请改为支持的图片、视频或音频格式",
                )
            )

    if len(images) > 9:
        issues.append("参考图片数量超限 | 当前值: {} | 允许范围: 0~9 | 建议调整: 减少参考图片数量".format(len(images)))
    if len(videos) > 3:
        issues.append("参考视频数量超限 | 当前值: {} | 允许范围: 0~3 | 建议调整: 减少参考视频数量".format(len(videos)))
    if len(audios) > 3:
        issues.append("参考音频数量超限 | 当前值: {} | 允许范围: 0~3 | 建议调整: 减少参考音频数量".format(len(audios)))

    total_size = sum(item.get("size_bytes", 0) for item in media_items)
    if total_size > REQUEST_MAX_BYTES:
        issues.append(
            _build_issue(
                "全部参考资源",
                "总输入大小超限",
                actual=_format_bytes(total_size),
                allowed=f"≤ {_format_bytes(REQUEST_MAX_BYTES)}",
                fix="减少参考资源数量，或替换成更小的文件",
            )
        )

    total_video_duration = sum(float(item.get("duration", 0.0)) for item in videos)
    if total_video_duration > VIDEO_MAX_DURATION:
        issues.append(
            _build_issue(
                "全部参考视频",
                "参考视频总时长超限",
                actual=f"{total_video_duration:.2f}s",
                allowed=f"≤ {VIDEO_MAX_DURATION:.0f}s",
                fix="裁剪视频时长，确保所有参考视频总时长不超过 15 秒",
            )
        )

    total_audio_duration = sum(float(item.get("duration", 0.0)) for item in audios)
    if total_audio_duration > AUDIO_MAX_DURATION:
        issues.append(
            _build_issue(
                "全部参考音频",
                "参考音频总时长超限",
                actual=f"{total_audio_duration:.2f}s",
                allowed=f"≤ {AUDIO_MAX_DURATION:.0f}s",
                fix="裁剪音频时长，确保所有参考音频总时长不超过 15 秒",
            )
        )

    for item in images:
        ext = item["extension"]
        if ext not in IMAGE_EXTENSIONS:
            issues.append(
                _build_issue(
                    item["source"],
                    "图片格式不支持",
                    actual=ext or "<none>",
                    allowed="jpeg, png, webp, bmp, tiff, gif",
                    fix="转换为支持的图片格式",
                )
            )
        if item["size_bytes"] >= IMAGE_MAX_BYTES:
            issues.append(
                _build_issue(
                    item["source"],
                    "图片大小超限",
                    actual=_format_bytes(item["size_bytes"]),
                    allowed=f"< {_format_bytes(IMAGE_MAX_BYTES)}",
                    fix="压缩图片到 30MB 以下",
                )
            )
        width = int(item.get("width", 0))
        height = int(item.get("height", 0))
        _assert_range(item["source"], "图片宽度", width, IMAGE_MIN_DIMENSION, IMAGE_MAX_DIMENSION, issues, "调整图片宽度到 300~6000 px")
        _assert_range(item["source"], "图片高度", height, IMAGE_MIN_DIMENSION, IMAGE_MAX_DIMENSION, issues, "调整图片高度到 300~6000 px")
        if width > 0 and height > 0:
            aspect_ratio = width / height
            _assert_range(item["source"], "图片宽高比", round(aspect_ratio, 4), MIN_ASPECT_RATIO, MAX_ASPECT_RATIO, issues, "调整图片裁剪比例到 0.4~2.5")

    for item in videos:
        ext = item["extension"]
        if ext not in VIDEO_EXTENSIONS:
            issues.append(
                _build_issue(
                    item["source"],
                    "视频格式不支持",
                    actual=ext or "<none>",
                    allowed="mp4, mov",
                    fix="转码为 mp4 或 mov",
                )
            )
        if item["size_bytes"] > VIDEO_MAX_BYTES:
            issues.append(
                _build_issue(
                    item["source"],
                    "视频大小超限",
                    actual=_format_bytes(item["size_bytes"]),
                    allowed=f"≤ {_format_bytes(VIDEO_MAX_BYTES)}",
                    fix="压缩视频到 50MB 以下",
                )
            )
        duration = float(item.get("duration", 0.0))
        _assert_range(item["source"], "视频时长", round(duration, 3), VIDEO_MIN_DURATION, VIDEO_MAX_DURATION, issues, "裁剪视频到 2~15 秒")
        width = int(item.get("width", 0))
        height = int(item.get("height", 0))
        _assert_range(item["source"], "视频宽度", width, VIDEO_MIN_DIMENSION, VIDEO_MAX_DIMENSION, issues, "调整视频宽度到 300~6000 px")
        _assert_range(item["source"], "视频高度", height, VIDEO_MIN_DIMENSION, VIDEO_MAX_DIMENSION, issues, "调整视频高度到 300~6000 px")
        if width > 0 and height > 0:
            aspect_ratio = width / height
            pixels = width * height
            _assert_range(item["source"], "视频宽高比", round(aspect_ratio, 4), MIN_ASPECT_RATIO, MAX_ASPECT_RATIO, issues, "调整视频裁剪比例到 0.4~2.5")
            _assert_range(item["source"], "视频像素数", pixels, VIDEO_MIN_PIXELS, VIDEO_MAX_PIXELS, issues, "调整视频分辨率，使宽×高落在允许范围")
        fps = float(item.get("fps", 0.0))
        _assert_range(item["source"], "视频帧率", round(fps, 3), VIDEO_MIN_FPS, VIDEO_MAX_FPS, issues, "调整视频帧率到 24~60 FPS")

    for item in audios:
        ext = item["extension"]
        if ext not in AUDIO_EXTENSIONS:
            issues.append(
                _build_issue(
                    item["source"],
                    "音频格式不支持",
                    actual=ext or "<none>",
                    allowed="wav, mp3",
                    fix="转换为 wav 或 mp3",
                )
            )
        if item["size_bytes"] > AUDIO_MAX_BYTES:
            issues.append(
                _build_issue(
                    item["source"],
                    "音频大小超限",
                    actual=_format_bytes(item["size_bytes"]),
                    allowed=f"≤ {_format_bytes(AUDIO_MAX_BYTES)}",
                    fix="压缩音频到 15MB 以下",
                )
            )
        duration = float(item.get("duration", 0.0))
        _assert_range(item["source"], "音频时长", round(duration, 3), AUDIO_MIN_DURATION, AUDIO_MAX_DURATION, issues, "裁剪音频到 2~15 秒")

    if issues:
        raise ReferenceInputValidationError(
            "❌ 参考输入不符合 reference_image_to_video 要求，请先调整后再继续：\n"
            + "\n".join(issues)
        )

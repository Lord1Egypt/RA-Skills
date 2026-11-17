"""Ordered input-media validation shared by Skill and SDK.

The server owns rule definitions. Clients validate supplied inputs only;
At least one input is required, even with min_count=0; no count rule means one input.
Type hints select a primary URL only; the server validates content.
"""

import copy
import mimetypes
import os
from urllib.parse import urlsplit


class InputMediaValidationError(ValueError):
    """Supplied input media do not satisfy the published task limits."""


def normalize_input_media(value, selection):
    """Preserve input order and resolve types before upload or quota use.

    A scalar keeps the existing single-input API. Multiple inputs may be source
    strings or explicit {source, media_type, profile} objects when a URL has no
    recognizable suffix. Client type hints are not a substitute for server checks.
    """
    items = [] if value is None or (isinstance(value, str) and not value) else (list(value) if isinstance(value, (list, tuple)) else [value])
    if not items:
        raise InputMediaValidationError('至少需要提供一个输入素材')
    limits = selection.get("input_media")
    minimum = limits.get("min_count", 1) if limits is not None else 1
    maximum = limits.get("max_count", 1) if limits is not None else 1
    if len(items) < minimum or (maximum is not None and len(items) > maximum):
        raise InputMediaValidationError(
            f'输入素材数量 {len(items)} 必须介于 {minimum} 和 {maximum}'
        )
    result = []
    for index, item in enumerate(items):
        info = item if isinstance(item, dict) else {"source": item}
        source = info.get("source")
        if isinstance(source, os.PathLike):
            source = os.fspath(source)
        if source is None or (isinstance(source, str) and not source.strip()):
            raise InputMediaValidationError(f'输入素材 {index + 1}: 必须提供素材来源')
        raw_profile = info.get("profile")
        profile = copy.deepcopy(raw_profile) if raw_profile is not None else {}
        if not isinstance(profile, dict):
            raise InputMediaValidationError(f'输入素材 {index + 1}: profile 必须是对象')
        media_profile = profile.get("media_profiles", {})
        if not isinstance(media_profile, dict):
            raise InputMediaValidationError(f'输入素材 {index + 1}: media_profiles 必须是对象')
        declared = info.get("media_type") or media_profile.get("media_type")
        filename = source if isinstance(source, str) else getattr(source, "name", "")
        try:
            path = urlsplit(filename).path if isinstance(filename, str) else ""
            mime = mimetypes.guess_type(path)[0] or ""
        except ValueError:
            mime = ""  # Type discovery must not reject an otherwise usable source.
        inferred = mime.split("/", 1)[0] if mime else ""
        media_type = declared or inferred
        result.append({"source": source, "media_type": media_type, "profile": profile})
    return result


def primary_media_index(inputs):
    """Use the first video for consume, or the first input if there is no video."""
    return next((index for index, item in enumerate(inputs) if item["media_type"] == "video"), 0)


def uploaded_init_images(inputs, urls):
    """Build algorithm inputs in original order, keeping each input's own profile."""
    result = []
    for item, url in zip(inputs, urls):
        profile = copy.deepcopy(item["profile"])
        if item["media_type"]:
            profile.setdefault("media_profiles", {})["media_type"] = item["media_type"]
        media = {"url": url}
        if profile:
            media["profile"] = profile
        result.append(media)
    return result

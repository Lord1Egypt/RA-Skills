"""Input and import validation helpers used by MCP tools."""

import base64
import math
import mimetypes
import re
from datetime import datetime
from typing import Optional

from .portfolio_math import r2

DATA_SOURCE_MODES = {"source_a", "source_b", "huahua"}
LEGACY_DATA_SOURCE_MODES = {"b": "source_a", "c": "source_b"}
DATA_SOURCE_PREFERENCE_EPOCH = 1
MAX_IMAGE_SIZE = 10 * 1024 * 1024
MAX_UPLOAD_TOTAL_SIZE = 50 * 1024 * 1024
MAX_UPLOAD_FILES = 10


def detect_image_mime(content: bytes) -> Optional[str]:
    if content[:8] == b"\x89PNG\r\n\x1a\n":
        return "image/png"
    if content[:2] == b"\xff\xd8":
        return "image/jpeg"
    if content[:4] == b"RIFF" and content[8:12] == b"WEBP":
        return "image/webp"
    if content[:6] in (b"GIF87a", b"GIF89a"):
        return "image/gif"
    if content[:2] == b"BM":
        return "image/bmp"
    return None


def validate_image_file(filepath: str, content: bytes, mime: str) -> str:
    if len(content) > MAX_IMAGE_SIZE:
        raise ValueError(f"图片文件过大：{len(content) / 1024 / 1024:.1f}MB，最大允许 10MB")
    detected_mime = detect_image_mime(content)
    if not detected_mime:
        raise ValueError(f"不支持的图片格式：{mime or 'unknown'}，仅支持 JPEG/PNG/WebP/GIF/BMP")
    return detected_mime


def validate_fund_code(code: str) -> str:
    normalized = str(code or "").strip()
    if not re.fullmatch(r"\d{6}", normalized):
        raise ValueError(f"基金代码必须是 6 位数字，收到：{code}")
    return normalized


def normalize_data_source_mode(value) -> str:
    normalized = str(value or "source_a").strip().lower()
    if normalized in DATA_SOURCE_MODES:
        return normalized
    return LEGACY_DATA_SOURCE_MODES.get(normalized, "source_a")


def validate_amount(amount: float) -> float:
    if (
        isinstance(amount, bool)
        or not isinstance(amount, (int, float))
        or not math.isfinite(float(amount))
    ):
        raise ValueError(f"金额必须是数字，收到：{amount}")
    if amount <= 0:
        raise ValueError(f"金额必须大于 0，收到：{amount}")
    if amount > 100_000_000:
        raise ValueError(f"金额过大：{amount}，请确认是否正确")
    rounded = r2(float(amount))
    if rounded <= 0:
        raise ValueError("金额精确到分后必须至少为 0.01")
    return rounded


def validate_date(date_str: str) -> str:
    if not date_str:
        return ""
    if not re.fullmatch(r"\d{4}-\d{2}-\d{2}", date_str):
        raise ValueError(f"日期格式必须是 YYYY-MM-DD，收到：{date_str}")
    try:
        datetime.strptime(date_str, "%Y-%m-%d")
    except ValueError:
        raise ValueError(f"无效的日期：{date_str}") from None
    return date_str


def validate_data_cutoff(value: str) -> str:
    normalized = str(value or "").strip()
    if not normalized:
        raise ValueError("data_cutoff_at 不能为空")
    if re.fullmatch(r"\d{4}-\d{2}-\d{2}", normalized):
        return validate_date(normalized)
    if not re.fullmatch(r"\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z", normalized):
        raise ValueError("data_cutoff_at 必须是 YYYY-MM-DD 或 YYYY-MM-DDTHH:MM:SSZ")
    try:
        datetime.strptime(normalized, "%Y-%m-%dT%H:%M:%SZ")
    except ValueError:
        raise ValueError(f"无效的数据截止时间：{normalized}") from None
    return normalized


def normalize_upload_files(
    image_paths: Optional[list[str]] = None,
    images_base64: Optional[list[dict]] = None,
) -> list[tuple[str, bytes, str]]:
    files: list[tuple[str, bytes, str]] = []
    if image_paths:
        # Local file reads are disabled by default: an agent (or a
        # prompt-injected agent) could otherwise exfiltrate arbitrary files
        # (e.g. ~/.ssh/*, ~/.aws/*) to the backend screenshot service. Agents
        # must pass image content via images_base64 instead.
        raise ValueError(
            "image_paths 已禁用，请改用 images_base64 提供图片内容"
        )
    items = images_base64 or []
    if not isinstance(items, list):
        raise ValueError("images_base64 必须是数组")
    if len(items) > MAX_UPLOAD_FILES:
        raise ValueError(f"单次最多上传 {MAX_UPLOAD_FILES} 张截图")
    total_size = 0
    for index, item in enumerate(items):
        if not isinstance(item, dict):
            raise ValueError("images_base64 每项必须是对象")
        filename = re.split(r"[/\\]", str(item.get("filename") or f"image_{index + 1}.png"))[-1].strip()
        if not filename or len(filename) > 200 or any(ord(character) < 32 for character in filename):
            raise ValueError("图片文件名必须为 1-200 个不含控制字符的字符")
        mime = str(item.get("mime") or mimetypes.guess_type(filename)[0] or "image/png")
        raw_base64 = str(item.get("base64") or "")
        if "," in raw_base64 and raw_base64.strip().lower().startswith("data:"):
            raw_base64 = raw_base64.split(",", 1)[1]
        if not raw_base64:
            raise ValueError(f"{filename} 的 base64 内容为空")
        if len(raw_base64) > ((MAX_IMAGE_SIZE + 2) // 3) * 4 + 4:
            raise ValueError(f"{filename} 的编码内容超过单图 10MB 限制")
        try:
            content = base64.b64decode(raw_base64, validate=True)
        except Exception:
            raise ValueError(f"{filename} 的 base64 内容无效") from None
        mime = validate_image_file(filename, content, mime)
        total_size += len(content)
        if total_size > MAX_UPLOAD_TOTAL_SIZE:
            raise ValueError("单次上传图片总大小不能超过 50MB")
        files.append((filename, content, mime))
    if not files:
        raise ValueError("请提供 images_base64（image_paths 已禁用）")
    return files


def summarize_import_items(items: list[dict]) -> dict:
    total = len(items)
    exact = fuzzy = ambiguous = unmatched = skipped = 0
    for item in items:
        if item.get("skip"):
            skipped += 1
            continue
        status = item.get("match_status") or item.get("match_quality")
        matched = item.get("matched")
        code = item.get("code") or item.get("fund_code")
        if status == "exact" or (matched is True and status not in {"fuzzy", "ambiguous"}):
            exact += 1
        elif status in {"fuzzy", "manual"}:
            fuzzy += 1
        elif status == "ambiguous":
            ambiguous += 1
        elif matched is False or code in {None, "", "000000"}:
            unmatched += 1
    return {
        "total": total,
        "exact": exact,
        "fuzzy": fuzzy,
        "ambiguous": ambiguous,
        "unmatched": unmatched,
        "skipped": skipped,
    }

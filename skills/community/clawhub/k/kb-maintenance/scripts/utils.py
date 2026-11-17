import datetime as dt
import hashlib
import json
import re
from pathlib import PurePosixPath


def now():
    return dt.datetime.now(dt.timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def sha256_text(text):
    return hashlib.sha256((text or "").encode("utf-8")).hexdigest()


def clip(text, limit):
    text = "" if text is None else str(text)
    limit = max(0, int(limit or 0))
    if not limit or len(text) <= limit:
        return text
    return text[: max(0, limit - 3)].rstrip() + "..."


def unique(values):
    result = []
    seen = set()
    for value in values or []:
        if value in (None, ""):
            continue
        key = json.dumps(value, ensure_ascii=False, sort_keys=True) if isinstance(value, (dict, list)) else str(value)
        if key in seen:
            continue
        seen.add(key)
        result.append(value)
    return result


def safe_relpath(path):
    value = str(path or "").replace("\\", "/").strip()
    if not value:
        raise ValueError("empty path")
    if value.startswith("/") or value.startswith("\\"):
        raise ValueError(f"absolute paths are not allowed: {path}")
    normalized = str(PurePosixPath(value))
    if normalized in {"", "."}:
        raise ValueError("empty path")
    if normalized.startswith("../") or "/../" in normalized or normalized == "..":
        raise ValueError(f"path traversal is not allowed: {path}")
    return normalized.lstrip("./")


def strip_frontmatter(text):
    text = text or ""
    if not text.startswith("---"):
        return text.strip()
    match = re.match(r"(?s)^---\s*\n.*?\n---\s*\n?", text)
    if not match:
        return text.strip()
    return text[match.end():].strip()


def parse_frontmatter(text):
    text = text or ""
    if not text.startswith("---"):
        return {}
    match = re.match(r"(?s)^---\s*\n(.*?)\n---\s*\n?", text)
    if not match:
        return {}
    data = {}
    for raw_line in match.group(1).splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#") or ":" not in line:
            continue
        key, value = line.split(":", 1)
        key = key.strip()
        value = value.strip()
        try:
            data[key] = json.loads(value)
        except Exception:
            data[key] = value.strip("\"'")
    return data


def slugify(text, max_len=80):
    value = str(text or "").strip().lower()
    value = re.sub(r"[^a-z0-9\u4e00-\u9fff]+", "-", value)
    value = re.sub(r"-+", "-", value).strip("-")
    return (value or "page")[:max_len].strip("-") or "page"


def extract_keywords(text, limit=8):
    text = str(text or "")
    candidates = re.findall(r"[\u4e00-\u9fff]{2,12}|[A-Za-z][A-Za-z0-9_-]{2,30}", text)
    stop = {
        "overview", "source", "sources", "page", "pages", "markdown", "knowledge",
        "team", "research", "current", "updated", "this", "that", "with", "from",
    }
    result = []
    seen = set()
    for item in candidates:
        key = item.lower()
        if key in stop or key in seen:
            continue
        seen.add(key)
        result.append(item)
        if len(result) >= limit:
            break
    return result

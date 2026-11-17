import json
import datetime as dt
import hashlib
import re
from pathlib import Path


def now():
    return dt.datetime.now(dt.timezone.utc).replace(microsecond=0).isoformat()


def slugify(text, limit=80):
    value = str(text or "untitled").strip().lower()
    value = re.sub(r"[^\w\u4e00-\u9fff.-]+", "-", value)
    value = re.sub(r"-{2,}", "-", value).strip("-")
    return value[:limit] or "untitled"


def sha256_text(text):
    return hashlib.sha256(str(text or "").encode("utf-8")).hexdigest()


def unique(items):
    result = []
    seen = set()
    for item in items or []:
        if item in (None, ""):
            continue
        key = str(item)
        if key in seen:
            continue
        seen.add(key)
        result.append(item)
    return result


def safe_relpath(path):
    value = str(path or "").replace("\\", "/").strip()
    while value.startswith("/"):
        value = value[1:]
    parts = [part for part in value.split("/") if part not in ("", ".")]
    if any(part == ".." for part in parts):
        raise ValueError(f"Unsafe KB path: {path}")
    return "/".join(parts)


def parse_frontmatter(text):
    value = text or ""
    if not value.startswith("---"):
        return {}
    match = re.match(r"^---\s*\n([\s\S]*?)\n---\s*", value)
    if not match:
        return {}
    data = {}
    for line in match.group(1).splitlines():
        if not line.strip() or ":" not in line:
            continue
        key, raw_value = line.split(":", 1)
        key = key.strip()
        raw_value = raw_value.strip()
        if not key:
            continue
        if not raw_value:
            data[key] = ""
            continue
        try:
            data[key] = json.loads(raw_value)
        except json.JSONDecodeError:
            data[key] = raw_value.strip('"')
    return data


def strip_frontmatter(text):
    return re.sub(r"^---[\s\S]*?---\s*", "", text or "").strip()


def clip(text, max_chars):
    value = str(text or "")
    if len(value) <= max_chars:
        return value
    return value[:max_chars].rstrip() + "\n...[truncated]"


def query_tokens(text):
    raw = re.findall(r"[\u4e00-\u9fff]{2,}|[A-Za-z][A-Za-z0-9_+-]{2,}", text or "")
    tokens = set()
    for token in raw:
        lowered = token.lower()
        tokens.add(lowered)
        if re.fullmatch(r"[\u4e00-\u9fff]+", token) and len(token) > 3:
            for size in (2, 3, 4):
                for index in range(0, len(token) - size + 1):
                    tokens.add(token[index:index + size])
    return {token for token in tokens if token.strip()}


def score_text(text, tokens):
    haystack = str(text or "").lower()
    return sum(1 for token in tokens if token and token.lower() in haystack)


def read_text_limited(path, max_chars=12000):
    file_path = Path(path)
    if not file_path.exists() or not file_path.is_file():
        return ""
    if file_path.stat().st_size > 50 * 1024 * 1024:
        return ""
    return file_path.read_text(encoding="utf-8", errors="replace")[:max_chars]

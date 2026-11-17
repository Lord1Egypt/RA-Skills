import datetime as dt
import hashlib
import json
import re
from pathlib import Path


def now():
    return dt.datetime.now(dt.timezone.utc).replace(microsecond=0).isoformat()


def slugify(text, limit=80):
    text = str(text or "untitled").strip().lower()
    text = re.sub(r"[^\w\u4e00-\u9fff.-]+", "-", text)
    text = re.sub(r"-{2,}", "-", text).strip("-")
    return (text[:limit].strip("-") or "untitled")


def repo_slug(repo_url):
    value = str(repo_url or "repository").rstrip("/")
    value = value.rsplit("/", 1)[-1]
    if value.endswith(".git"):
        value = value[:-4]
    return slugify(value or repo_url or "repository")


def sha256_text(text):
    return hashlib.sha256(str(text or "").encode("utf-8")).hexdigest()


def read_json_file(path):
    raw = Path(path).read_bytes()
    if not raw.strip():
        return {}
    return json.loads(raw.decode("utf-8-sig", errors="replace"))


def write_json_file(path, data):
    target = Path(path)
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(json.dumps(data or {}, ensure_ascii=False, indent=2), encoding="utf-8")


def ensure_list(value):
    if value is None:
        return []
    if isinstance(value, list):
        return value
    return [value]


def unique(values):
    seen = set()
    result = []
    for value in values or []:
        if value in (None, ""):
            continue
        key = str(value)
        if key not in seen:
            result.append(value)
            seen.add(key)
    return result


def strip_frontmatter(text):
    return re.sub(r"^---\s*\n[\s\S]*?\n---\s*\n?", "", text or "").strip()


def extract_keywords(text, limit=16):
    tokens = re.findall(r"[\u4e00-\u9fff]{2,}|[A-Za-z][A-Za-z0-9_+.-]{2,}", text or "")
    return unique(tokens)[:limit]


def read_text_limited(path, max_chars=12000):
    candidate = Path(path)
    if not candidate.exists() or not candidate.is_file():
        return ""
    raw = candidate.read_bytes()
    if b"\x00" in raw[:4096]:
        return ""
    return raw.decode("utf-8-sig", errors="replace")[:max_chars]


def safe_relpath(path):
    value = str(path or "").replace("\\", "/").strip("/")
    if not value or value.startswith("../") or "/../" in value or value == "..":
        raise ValueError(f"Unsafe relative path: {path}")
    return value

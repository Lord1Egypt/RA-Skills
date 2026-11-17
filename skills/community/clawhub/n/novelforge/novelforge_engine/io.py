"""Small, dependency-free file primitives used by the Novel Skill gates."""

import hashlib
import json
import os
import tempfile
from contextlib import contextmanager
from pathlib import Path


def sha256_bytes(value):
    return hashlib.sha256(value).hexdigest()


def sha256_text(value):
    return sha256_bytes(value.encode("utf-8"))


def safe_id(value):
    """Return whether a user-controlled identifier is safe for one path segment."""
    return (
        isinstance(value, str)
        and value
        and "/" not in value
        and "\\" not in value
        and "\x00" not in value
        and not any(ord(character) < 32 for character in value)
        and value not in (".", "..")
    )


def sha256_file(path):
    return sha256_bytes(Path(path).read_bytes())


def write_bytes_atomic(path, data):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, temp_name = tempfile.mkstemp(prefix=".novelforge-", dir=str(path.parent))
    try:
        with os.fdopen(fd, "wb") as handle:
            handle.write(data)
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(temp_name, str(path))
    except Exception:
        try:
            os.unlink(temp_name)
        except OSError:
            pass
        raise


def write_json_atomic(path, value):
    data = json.dumps(value, ensure_ascii=False, sort_keys=True, indent=2).encode("utf-8")
    write_bytes_atomic(path, data + b"\n")


def read_json(path):
    with Path(path).open("r", encoding="utf-8") as handle:
        return json.load(handle)


def append_jsonl(path, value):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    line = json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")) + "\n"
    with path.open("a", encoding="utf-8") as handle:
        handle.write(line)
        handle.flush()
        os.fsync(handle.fileno())


@contextmanager
def file_lock(path):
    """Take an advisory process lock without introducing a runtime dependency."""
    import fcntl

    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a+", encoding="utf-8") as handle:
        fcntl.flock(handle.fileno(), fcntl.LOCK_EX)
        try:
            yield handle
        finally:
            fcntl.flock(handle.fileno(), fcntl.LOCK_UN)


try:
    import yaml
except ImportError:
    yaml = None


def parse_frontmatter(text):
    if not isinstance(text, str):
        raise ValueError("frontmatter input must be a string")
    text = text.lstrip("\ufeff")
    if not text.startswith("---"):
        return {}, text
    lines = text.splitlines(keepends=True)
    if not lines or lines[0].strip() != "---":
        return {}, text
    end_index = -1
    for idx in range(1, len(lines)):
        if lines[idx].strip() in ("---", "..."):
            end_index = idx
            break
    if end_index == -1:
        return {}, text
    frontmatter_raw = "".join(lines[1:end_index])
    body = "".join(lines[end_index + 1 :])
    metadata = {}
    if frontmatter_raw.strip():
        if yaml is not None:
            metadata = yaml.safe_load(frontmatter_raw) or {}
        else:
            try:
                metadata = json.loads(frontmatter_raw)
            except Exception:
                metadata = {}
    if not isinstance(metadata, dict):
        metadata = {}
    return metadata, body


def format_frontmatter(metadata, body=""):
    if not isinstance(metadata, dict):
        metadata = {}
    if yaml is not None:
        fm = yaml.safe_dump(metadata, allow_unicode=True, sort_keys=True)
    else:
        fm = json.dumps(metadata, ensure_ascii=False, indent=2, sort_keys=True)
    parts = ["---", fm.rstrip(), "---", ""]
    if body:
        parts.append(body.strip() + "\n")
    return "\n".join(parts)


def read_frontmatter(path):
    with Path(path).open("r", encoding="utf-8") as handle:
        return parse_frontmatter(handle.read())


def write_frontmatter_atomic(path, metadata, body=""):
    content = format_frontmatter(metadata, body)
    write_bytes_atomic(path, content.encode("utf-8"))

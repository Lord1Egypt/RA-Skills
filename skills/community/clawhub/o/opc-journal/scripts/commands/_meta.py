"""Minimal meta helpers for opc-journal commands."""
import fcntl
import json
import os
from pathlib import Path

from utils.storage import build_customer_dir
from utils.timezone import now_tz


def read_meta(customer_id: str) -> dict:
    try:
        path = os.path.expanduser(Path(build_customer_dir(customer_id)) / "journal_meta.json")
        if os.path.exists(path):
            with open(path, "r", encoding="utf-8") as f:
                fcntl.flock(f.fileno(), fcntl.LOCK_SH)
                try:
                    return json.load(f)
                finally:
                    fcntl.flock(f.fileno(), fcntl.LOCK_UN)
    except Exception:
        pass
    return {}


def get_language(customer_id: str) -> str:
    meta = read_meta(customer_id)
    lang = meta.get("language", "")
    if lang.startswith("zh"):
        return "zh"
    return "en"


def _has_chinese(texts: list) -> bool:
    combined = " ".join(str(t) for t in texts if t)
    return any("\u4e00" <= c <= "\u9fff" for c in combined)


def detect_language(texts: list) -> str:
    return "zh" if _has_chinese(texts) else "en"


def write_meta(customer_id: str, data: dict) -> bool:
    try:
        path = os.path.expanduser(Path(build_customer_dir(customer_id)) / "journal_meta.json")
        os.makedirs(os.path.dirname(path), exist_ok=True)
        
        # Ensure meta has timezone-aware timestamps
        if "last_updated" not in data:
            data["last_updated"] = now_tz().isoformat()
        
        with open(path, "w", encoding="utf-8") as f:
            fcntl.flock(f.fileno(), fcntl.LOCK_EX)
            try:
                json.dump(data, f, indent=2, ensure_ascii=False)
                f.flush()
                os.fsync(f.fileno())
            finally:
                fcntl.flock(f.fileno(), fcntl.LOCK_UN)
        return True
    except Exception:
        return False

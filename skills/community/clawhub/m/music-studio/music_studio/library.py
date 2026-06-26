"""输出记录管理模块（带类型标注）"""

import json
from datetime import datetime, timedelta
from pathlib import Path
from typing import Optional, Generator, Any

from music_studio import config


# 默认路径（会被 config.output_dir 覆盖）
_DEFAULT_OUTPUT: Path = Path(__file__).parent.parent / "output"


def OUTPUT_DIR() -> Path:
    """当前 output 目录（支持自定义配置）"""
    return config.get_output_dir()


def LIBRARY_FILE() -> Path:
    return OUTPUT_DIR() / "library.json"


def ensure_output_dir() -> None:
    OUTPUT_DIR().mkdir(parents=True, exist_ok=True)


def ensure_library() -> None:
    ensure_output_dir()
    if not LIBRARY_FILE().exists():
        write_library({"songs": []})


def write_library(data: dict[str, Any]) -> None:
    ensure_output_dir()
    with open(LIBRARY_FILE(), "w") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


def read_library() -> dict[str, Any]:
    ensure_library()
    with open(LIBRARY_FILE()) as f:
        return json.load(f)


def _now() -> str:
    return datetime.now().astimezone().isoformat(timespec="seconds")


def _expires(days: int = 30) -> str:
    t = datetime.now().astimezone() + timedelta(days=days)
    return t.isoformat(timespec="seconds")


def add_entry(entry: dict[str, Any]) -> None:
    lib = read_library()
    lib["songs"].append(entry)
    write_library(lib)


def list_entries(entry_type: Optional[str] = None) -> Generator[tuple[int, dict[str, Any]], None, None]:
    lib = read_library()
    songs = list(reversed(lib["songs"]))
    for idx, song in enumerate(songs, start=1):
        if entry_type and song.get("type") != entry_type:
            continue
        yield idx, song


def get_entry(entry_id: str) -> Optional[dict[str, Any]]:
    lib = read_library()
    for song in lib["songs"]:
        if song["id"] == entry_id:
            return song
    return None


def resolve_selector(selector: str) -> Optional[str]:
    lib = read_library()
    songs = list(reversed(lib["songs"]))

    if selector.isdigit():
        idx = int(selector) - 1
        if 0 <= idx < len(songs):
            return songs[idx]["id"]
        return None

    matches = [s["id"] for s in songs if s["id"].startswith(selector)]
    if len(matches) == 1:
        return matches[0]
    return None


def remove_expired() -> int:
    lib = read_library()
    before = len(lib["songs"])
    now_dt = datetime.now().astimezone()

    kept = []
    for s in lib["songs"]:
        expires = s.get("expires", "")
        if not expires:
            kept.append(s)
            continue
        try:
            exp_dt = datetime.fromisoformat(expires)
            if exp_dt >= now_dt:
                kept.append(s)
        except Exception:
            # 保守处理：解析失败就保留，避免误删
            kept.append(s)

    lib["songs"] = kept
    write_library(lib)
    return before - len(lib["songs"])


def purge_all() -> None:
    od = OUTPUT_DIR()
    lf = LIBRARY_FILE()
    if lf.exists():
        lf.unlink()
    for pattern in ("*.url", "*.txt", "*.hex", "*.mp3"):
        for f in od.glob(pattern):
            f.unlink()

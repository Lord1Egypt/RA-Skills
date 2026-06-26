#!/usr/bin/env python3
"""文件锁工具：安全的并发文件读写"""

import fcntl
import json
import time
from pathlib import Path
from contextlib import contextmanager
from typing import Any


@contextmanager
def file_lock(lock_path: str | Path, timeout: float = 5.0):
    """获取文件锁，超时抛异常"""
    lock_path = Path(lock_path)
    lock_path.parent.mkdir(parents=True, exist_ok=True)
    
    lock_file = None
    try:
        lock_file = open(lock_path, "w")
        start = time.time()
        while True:
            try:
                fcntl.flock(lock_file.fileno(), fcntl.LOCK_EX | fcntl.LOCK_NB)
                break
            except (IOError, OSError):
                if time.time() - start > timeout:
                    raise TimeoutError(f"无法获取锁: {lock_path}（超时 {timeout}s）")
                time.sleep(0.1)
        yield lock_file
    finally:
        if lock_file:
            try:
                fcntl.flock(lock_file.fileno(), fcntl.LOCK_UN)
            except (IOError, OSError):
                pass
            lock_file.close()


def safe_read(filepath: Path, encoding: str = "utf-8") -> str:
    """安全读取文件"""
    lock_path = filepath.parent / f".{filepath.stem}.lock"
    with file_lock(lock_path):
        if filepath.exists():
            return filepath.read_text(encoding=encoding)
        return ""


def safe_write(filepath: Path, content: str, encoding: str = "utf-8", append: bool = False):
    """安全写入文件"""
    filepath.parent.mkdir(parents=True, exist_ok=True)
    lock_path = filepath.parent / f".{filepath.stem}.lock"
    with file_lock(lock_path):
        if append:
            existing = filepath.read_text(encoding=encoding) if filepath.exists() else ""
            filepath.write_text(existing + content, encoding=encoding)
        else:
            filepath.write_text(content, encoding=encoding)


def safe_read_json(filepath: Path) -> Any:
    """安全读取 JSON"""
    content = safe_read(filepath)
    if content.strip():
        return json.loads(content)
    return {}


def safe_write_json(filepath: Path, data: Any, indent: int = 2):
    """安全写入 JSON"""
    safe_write(filepath, json.dumps(data, ensure_ascii=False, indent=indent))

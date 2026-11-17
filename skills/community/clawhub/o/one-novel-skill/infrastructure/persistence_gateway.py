"""
infrastructure/persistence_gateway.py — Atomic file I/O gateway

Provides atomic write (tmp → replace) for chapter files, tracker files,
and any other disk output. All file writes must go through this gateway.
"""
from __future__ import annotations

import logging
from pathlib import Path
from typing import Optional, List
from datetime import datetime

_log = logging.getLogger("persistence")


class AtomicFileWriter:
    """Write file atomically: data → .tmp → rename → confirm."""

    def __init__(self, target_path: Path):
        self.target = Path(target_path)
        self.tmp = self.target.with_suffix(self.target.suffix + '.tmp')
        self._written = False

    def write(self, content: str):
        """Write content to temp file."""
        self.target.parent.mkdir(parents=True, exist_ok=True)
        with open(self.tmp, 'w', encoding='utf-8') as f:
            f.write(content)
        self._written = True

    def write_bytes(self, content: bytes):
        """Write bytes to temp file."""
        self.target.parent.mkdir(parents=True, exist_ok=True)
        with open(self.tmp, 'wb') as f:
            f.write(content)
        self._written = True

    def commit(self):
        """Atomically replace target with temp file."""
        if not self._written:
            return
        self.tmp.replace(self.target)
        self._written = False

    def rollback(self):
        """Clean up temp file."""
        if self.tmp.exists():
            self.tmp.unlink(missing_ok=True)
        self._written = False


class PersistenceGateway:
    """
    Gateway for all file persistence operations.
    
    References:
    - book_dir/{number}章.txt — chapter text
    - book_dir/追踪/ — tracker files
    - book_dir/规格/ — chapter specs
    - book_dir/大纲/ — outlines
    """

    def __init__(self, book_dir: str):
        self.book_dir = Path(book_dir).resolve()
        self._backup_dir = self.book_dir / "_backup"

    # ─── Chapter writing ───

    def write_chapter(self, chapter: int, text: str) -> Path:
        """Atomically write a chapter file."""
        path = self.book_dir / f"正文" / f"第{chapter:03d}章.txt"
        writer = AtomicFileWriter(path)
        writer.write(text)
        writer.commit()
        _log.info(f"Chapter {chapter} written: {len(text)} chars")
        return path

    def read_chapter(self, chapter: int) -> Optional[str]:
        """Read a chapter file."""
        path = self.book_dir / f"正文" / f"第{chapter:03d}章.txt"
        if not path.exists():
            return None
        with open(path, 'r', encoding='utf-8') as f:
            return f.read()

    def backup_chapter(self, chapter: int):
        """Backup a chapter before overwriting."""
        src = self.book_dir / f"正文" / f"第{chapter:03d}章.txt"
        if not src.exists():
            return
        self._backup_dir.mkdir(parents=True, exist_ok=True)
        ts = datetime.now().strftime("%Y%m%d_%H%M%S")
        dst = self._backup_dir / f"第{chapter:03d}章_{ts}.txt"
        dst.write_text(src.read_text(encoding='utf-8'), encoding='utf-8')

    # ─── Spec writing ───

    def write_spec(self, chapter: int, spec_json: str):
        """Write chapter spec JSON."""
        path = self.book_dir / f"规格" / f"第{chapter:03d}章.json"
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(spec_json, encoding='utf-8')

    # ─── Tracker writing ───

    def append_tracker(self, rel_path: str, lines: List[str]):
        """
        Append lines to a tracker file (e.g., 追踪/角色状态.md).
        Uses idempotent append: checks if first line already exists.
        """
        path = self.book_dir / rel_path
        path.parent.mkdir(parents=True, exist_ok=True)
        
        if not lines:
            return
        
        first_line = lines[0]
        if path.exists():
            existing = path.read_text(encoding='utf-8')
            if first_line in existing:
                _log.debug(f"Tracker {rel_path}: line already exists, skipping")
                return
        
        with open(path, 'a', encoding='utf-8') as f:
            for line in lines:
                f.write(line + '\n')

    def write_tracker(self, rel_path: str, content: str):
        """Overwrite a tracker file."""
        path = self.book_dir / rel_path
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding='utf-8')

    # ─── Chapter existence ───

    def chapter_exists(self, chapter: int) -> bool:
        """Check if a chapter file exists."""
        path = self.book_dir / f"正文" / f"第{chapter:03d}章.txt"
        return path.exists()

    def chapter_count(self) -> int:
        """Count existing chapter files."""
        chap_dir = self.book_dir / "正文"
        if not chap_dir.exists():
            return 0
        return len(list(chap_dir.glob("第*章.txt")))

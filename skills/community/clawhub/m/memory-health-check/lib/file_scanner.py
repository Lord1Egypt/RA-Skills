#!/usr/bin/env python3
"""Reusable file system scanning utilities for memory-health-check."""
import logging
import re
import hashlib
from pathlib import Path
from datetime import datetime, timezone, timedelta
from typing import Optional

logger = logging.getLogger("memory-health-check.file_scanner")


class FileScanner:
    """Reusable file system scanner for memory directories."""
    
    TEMP_PATTERNS = {".DS_Store", "Thumbs.db", "desktop.ini", "~"}
    MAX_FILE_SIZE_MB = 500  # Skip files larger than this
    
    def __init__(self, base_dir: Path):
        """Initialize scanner for a base directory.
        
        Args:
            base_dir: Base directory to scan
        """
        self.base_dir = base_dir
    
    def get_dir_size(self, follow_symlinks: bool = False) -> int:
        """Recursively compute directory size in bytes.
        
        Args:
            follow_symlinks: Whether to follow symlinks
            
        Returns:
            Total bytes
        """
        total = 0
        try:
            for f in self.base_dir.rglob("*"):
                if f.is_file() and (follow_symlinks or not f.is_symlink()):
                    try:
                        total += f.stat().st_size
                    except OSError:
                        pass
        except Exception as e:
            logger.warning(f"Error computing dir size: {e}")
        return total
    
    def get_file_counts(self) -> dict[str, int]:
        """Count files by extension/type.
        
        Returns:
            Dict: {"total": int, "md": int, "sqlite": int, "json": int, "other": int}
        """
        counts = {"total": 0, "md": 0, "sqlite": 0, "json": 0, "other": 0}
        
        try:
            for f in self.base_dir.rglob("*"):
                if f.is_file():
                    counts["total"] += 1
                    ext = f.suffix.lower()
                    if ext == ".md":
                        counts["md"] += 1
                    elif ext == ".sqlite":
                        counts["sqlite"] += 1
                    elif ext == ".json":
                        counts["json"] += 1
                    else:
                        counts["other"] += 1
        except Exception as e:
            logger.warning(f"Error counting files: {e}")
        
        return counts
    
    def get_file_ages(self) -> list[tuple[Path, datetime]]:
        """Get modification times for all files.
        
        Returns:
            List of (file_path, mtime_datetime) tuples, sorted newest first
        """
        files_with_mtime = []
        
        try:
            for f in self.base_dir.rglob("*"):
                if f.is_file():
                    try:
                        mtime = datetime.fromtimestamp(f.stat().st_mtime, tz=timezone.utc)
                        files_with_mtime.append((f, mtime))
                    except OSError:
                        pass
        except Exception as e:
            logger.warning(f"Error getting file ages: {e}")
        
        files_with_mtime.sort(key=lambda x: x[1], reverse=True)
        return files_with_mtime
    
    def get_age_distribution(self, now: datetime = None) -> dict[str, int]:
        """Compute age distribution across categories.
        
        Args:
            now: Reference datetime (default: now)
            
        Returns:
            Dict: {"<7d": int, "7-30d": int, "30-90d": int, ">90d": int, "total": int}
        """
        if now is None:
            now = datetime.now(tz=timezone.utc)
        
        week_ago = now - timedelta(days=7)
        month_ago = now - timedelta(days=30)
        quarter_ago = now - timedelta(days=90)
        
        dist = {"<7d": 0, "7-30d": 0, "30-90d": 0, ">90d": 0, "total": 0}
        
        for _, mtime in self.get_file_ages():
            dist["total"] += 1
            if mtime >= week_ago:
                dist["<7d"] += 1
            elif mtime >= month_ago:
                dist["7-30d"] += 1
            elif mtime >= quarter_ago:
                dist["30-90d"] += 1
            else:
                dist[">90d"] += 1
        
        return dist
    
    def find_temp_files(self) -> list[Path]:
        """Find temporary files (.DS_Store, etc.).
        
        Returns:
            List of temp file paths
        """
        temp_files = []
        
        try:
            for f in self.base_dir.rglob("*"):
                if f.is_file() and f.name in self.TEMP_PATTERNS:
                    temp_files.append(f)
        except Exception as e:
            logger.warning(f"Error finding temp files: {e}")
        
        return temp_files
    
    def find_empty_files(self) -> list[Path]:
        """Find empty .md files.
        
        Returns:
            List of empty file paths
        """
        empty_files = []
        
        try:
            for f in self.base_dir.rglob("*.md"):
                if f.is_file():
                    try:
                        if f.stat().st_size == 0:
                            empty_files.append(f)
                    except OSError:
                        pass
        except Exception as e:
            logger.warning(f"Error finding empty files: {e}")
        
        return empty_files
    
    def compute_checksum(self, file_path: Path) -> Optional[str]:
        """Compute SHA256 checksum of a file.
        
        Args:
            file_path: Path to file
            
        Returns:
            Hex digest string, or None on error
        """
        try:
            h = hashlib.sha256()
            with open(file_path, "rb") as f:
                for chunk in iter(lambda: f.read(65536), b""):
                    h.update(chunk)
            return h.hexdigest()
        except Exception:
            return None
    
    def find_wikilinks(self, content: str) -> list[str]:
        """Extract Obsidian-style [[wikilinks]] from content.
        
        Args:
            content: Text content
            
        Returns:
            List of link targets
        """
        return re.findall(r"\[\[([^\]|]+)(?:\|[^\]]+)?\]]", content)
    
    def find_markdown_links(self, content: str) -> list[str]:
        """Extract Markdown [text](url) links from content.
        
        Args:
            content: Text content
            
        Returns:
            List of link targets
        """
        return re.findall(r"\[[^\]]+\]\(([^)]+)\)", content)


if __name__ == "__main__":
    scanner = FileScanner(Path.home() / ".openclaw" / "workspace" / "memory")
    print(f"Dir size: {scanner.get_dir_size()} bytes")
    print(f"File counts: {scanner.get_file_counts()}")
    print(f"Age dist: {scanner.get_age_distribution()}")

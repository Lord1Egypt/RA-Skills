"""
File scanner for image-works.
Scans file paths, directories, and glob patterns for image files.
"""
import os
import glob
import logging
from typing import List, Optional

logger = logging.getLogger(__name__)

# Supported image formats and their magic bytes
SUPPORTED_FORMATS = {"jpg", "jpeg", "png", "webp", "avif", "gif", "bmp", "tiff", "tif", "svg"}
SUPPORTED_EXTENSIONS = {f".{fmt}" for fmt in SUPPORTED_FORMATS}


def scan(paths: list, recursive: bool = False, max_files: int = 1000,
         file_types: Optional[list] = None) -> List[str]:
    """
    Scan for image files from mixed input (paths, dirs, globs).
    
    Args:
        paths: List of file paths, directories, or glob patterns.
        recursive: Whether to scan subdirectories.
        max_files: Maximum files to return.
        file_types: List of allowed extensions (e.g., ["jpg","png"]).
                    Default: all supported formats.
        
    Returns:
        List of absolute file paths matching the criteria.
    """
    if file_types:
        allowed_exts = {f".{ft.lstrip('.').lower()}" for ft in file_types}
    else:
        allowed_exts = SUPPORTED_EXTENSIONS
    
    found = []
    seen = set()
    
    for entry in paths:
        entry = os.path.expanduser(entry.strip())
        
        if not entry:
            continue
        
        # Glob pattern check (contains * or ?)
        if '*' in entry or '?' in entry:
            matched = glob.glob(entry, recursive=recursive)
            for m in matched:
                abs_path = os.path.abspath(m)
                if abs_path not in seen and _is_image(abs_path, allowed_exts):
                    seen.add(abs_path)
                    found.append(abs_path)
            continue
        
        # Directory
        if os.path.isdir(entry):
            if recursive:
                for root, _, files in os.walk(entry):
                    for fname in files:
                        fpath = os.path.join(root, fname)
                        if fpath not in seen and _is_image(fpath, allowed_exts):
                            seen.add(fpath)
                            found.append(fpath)
                            if len(found) >= max_files:
                                break
                    if len(found) >= max_files:
                        break
            else:
                for fname in os.listdir(entry):
                    fpath = os.path.join(entry, fname)
                    if os.path.isfile(fpath) and _is_image(fpath, allowed_exts):
                        if fpath not in seen:
                            seen.add(fpath)
                            found.append(fpath)
                            if len(found) >= max_files:
                                break
        # Single file
        elif os.path.isfile(entry):
            abs_path = os.path.abspath(entry)
            if _is_image(abs_path, allowed_exts):
                found.append(abs_path)
        
        if len(found) >= max_files:
            logger.info("Reached max_files limit (%d)", max_files)
            break
    
    return found[:max_files]


def _is_image(filepath: str, allowed_exts: set) -> bool:
    """Check if a file is an image based on extension and existence."""
    ext = os.path.splitext(filepath)[1].lower()
    if ext not in allowed_exts:
        return False
    return os.path.getsize(filepath) > 0


def check_large_files(paths: list, threshold_mb: int = 100) -> list:
    """Check for files larger than threshold_mb and return their paths."""
    large = []
    for path in paths:
        size_mb = os.path.getsize(path) / (1024 * 1024)
        if size_mb > threshold_mb:
            large.append({"path": path, "size_mb": round(size_mb, 1)})
    return large


def get_file_info(path: str) -> dict:
    """Get basic file info."""
    stat = os.stat(path)
    return {
        "path": path,
        "size_bytes": stat.st_size,
        "size_human": _format_size(stat.st_size),
        "modified": stat.st_mtime,
    }


def _format_size(size_bytes: int) -> str:
    """Format file size in human-readable format."""
    for unit in ("B", "KB", "MB", "GB"):
        if size_bytes < 1024:
            return f"{size_bytes:.1f} {unit}"
        size_bytes /= 1024
    return f"{size_bytes:.1f} TB"

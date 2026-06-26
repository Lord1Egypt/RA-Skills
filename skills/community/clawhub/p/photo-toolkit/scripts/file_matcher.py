#!/usr/bin/env python3
"""
Shared file matching utilities for cross-format photo file matching.

Used by grade.py and layout_preview.py to find original files
regardless of file extension differences.
"""

from pathlib import Path

# Supported extensions (must match grade.py and layout_preview.py)
RAW_EXTENSIONS = {
    ".nef",
    ".nrw",  # Nikon
    ".cr2",
    ".cr3",
    ".crw",  # Canon
    ".arw",
    ".srf",
    ".sr2",  # Sony
    ".raf",  # Fujifilm
    ".orf",  # Olympus / OM System
    ".rw2",  # Panasonic
    ".pef",  # Pentax
    ".srw",  # Samsung
    ".rwl",  # Leica
    ".dng",  # Adobe DNG
    ".3fr",
    ".fff",  # Hasselblad
    ".iiq",  # Phase One
    ".x3f",  # Sigma
}

JPG_EXTENSIONS = {".jpg", ".jpeg"}

HEIC_EXTENSIONS = {".heic", ".heif"}

SUPPORTED_EXTENSIONS = RAW_EXTENSIONS | JPG_EXTENSIONS | HEIC_EXTENSIONS


def find_raw_file(file_ref, raw_root=None, supported_extensions=None):
    """
    Find a RAW file by absolute path or by stem name under raw_root.

    Supports:
        - Absolute path that exists → use directly
        - Absolute path that doesn't exist → try different extensions
        - Relative filename → search under raw_root by stem

    Args:
        file_ref: Absolute path string, or filename/stem to search
        raw_root: Root directory to search in (used when file_ref is not absolute)
        supported_extensions: Set of supported extensions

    Returns:
        Path object if found, None otherwise
    """
    if supported_extensions is None:
        supported_extensions = SUPPORTED_EXTENSIONS

    file_ref_path = Path(file_ref)

    # If it's already an absolute path that exists, use it directly
    if file_ref_path.is_absolute() and file_ref_path.exists():
        return file_ref_path

    # If absolute but doesn't exist, try with different extensions
    if file_ref_path.is_absolute():
        return find_file_by_stem(file_ref_path.parent, file_ref_path.stem, supported_extensions)

    # Relative path: search under raw_root
    if raw_root:
        raw_root = Path(raw_root)
        # Try as relative path from raw_root
        candidate = raw_root / file_ref
        if candidate.exists():
            return candidate
        # Try stem matching (also searches subdirs if recursive needed)
        result = find_file_by_stem(raw_root, file_ref_path.stem, supported_extensions)
        if result:
            return result
        # Try recursive search in subdirectories
        for p in sorted(raw_root.rglob(f"{file_ref_path.stem}*")):
            if p.is_file() and p.suffix.lower() in supported_extensions:
                return p

    return None


def find_file_by_stem(directory, stem, supported_extensions=None):
    """
    Find a file by its stem name, trying multiple extensions and case variations.

    Args:
        directory: Directory to search in
        stem: File stem (name without extension)
        supported_extensions: Set of supported extensions (default: SUPPORTED_EXTENSIONS)

    Returns:
        Path object if found, None otherwise
    """
    if supported_extensions is None:
        supported_extensions = SUPPORTED_EXTENSIONS

    directory = Path(directory)
    if not directory.exists():
        return None

    # Try exact match first
    for ext in supported_extensions:
        for name in [f"{stem}{ext}", f"{stem.upper()}{ext}", f"{stem.lower()}{ext}", f"{stem}{ext.upper()}"]:
            candidate = directory / name
            if candidate.exists():
                return candidate

    # Try glob pattern matching
    matches = []
    for ext in supported_extensions:
        matches.extend(directory.glob(f"{stem}*{ext}"))
        matches.extend(directory.glob(f"{stem.upper()}*{ext}"))

    file_matches = [m for m in matches if m.suffix.lower() in supported_extensions]
    if file_matches:
        return file_matches[0]

    return None


def find_original_for_graded(graded_path, originals_dir, params_json=None, supported_extensions=None):
    """
    Find the corresponding original file for a graded image.

    Uses grading_params.json 'file' field for exact mapping, falls back to stem matching.

    Args:
        graded_path: Path to the graded image
        originals_dir: Directory containing original files
        params_json: Optional path to grading_params.json for exact mapping
        supported_extensions: Set of supported extensions (default: SUPPORTED_EXTENSIONS)

    Returns:
        Path object if found, None otherwise
    """
    if supported_extensions is None:
        supported_extensions = SUPPORTED_EXTENSIONS

    originals_dir = Path(originals_dir)
    if not originals_dir.exists():
        return None

    # Build index of originals
    orig_index = {}
    for p in originals_dir.iterdir():
        if p.is_file() and p.suffix.lower() in supported_extensions:
            orig_index[p.stem.lower()] = p

    # Try matching by stripping style suffix from graded filename
    # "DSC_0001_暖春丝滑.jpg" → try "DSC_0001"
    graded_stem = graded_path.stem.lower()

    # Try exact match first
    if graded_stem in orig_index:
        return orig_index[graded_stem]

    # Try progressively removing trailing "_xxx" suffixes
    parts = graded_stem.rsplit("_", 1)
    while len(parts) > 1:
        candidate = parts[0]
        if candidate in orig_index:
            return orig_index[candidate]
        parts = candidate.rsplit("_", 1)

    return None

from __future__ import annotations

import re
import shutil
import urllib.parse
import urllib.request
from collections.abc import Callable
from pathlib import Path
from typing import Any

from .image_fields import resolve_image_targets


_INVALID_FILENAME_CHARS = re.compile(r'[\\/:*?"<>|]')


def sanitize_filename(title: str, *, max_len: int = 120) -> str:
    cleaned = _INVALID_FILENAME_CHARS.sub("-", (title or "").strip())
    cleaned = re.sub(r"-{2,}", "-", cleaned)
    cleaned = re.sub(r"\s+", " ", cleaned)
    cleaned = cleaned.strip().rstrip(".")
    if not cleaned:
        cleaned = "Untitled"
    if len(cleaned) > max_len:
        cleaned = cleaned[:max_len].rstrip()
    return cleaned


def _escape_markdown_label(text: str) -> str:
    return (
        text.replace("\\", "\\\\")
        .replace("[", "\\[")
        .replace("]", "\\]")
        .replace("(", "\\(")
        .replace(")", "\\)")
    )


def _unique_path(path: Path) -> Path:
    if not path.exists():
        return path
    stem = path.stem
    suffix = path.suffix
    for idx in range(1, 1000):
        candidate = path.with_name(f"{stem}-{idx}{suffix}")
        if not candidate.exists():
            return candidate
    raise RuntimeError(f"Unable to find free filename for {path}")


def download_remote_image(url: str, destination: Path) -> None:
    destination.parent.mkdir(parents=True, exist_ok=True)
    with urllib.request.urlopen(url) as response, destination.open("wb") as handle:
        shutil.copyfileobj(response, handle)


def render_image_markdown(
    image: Any,
    *,
    vault_root: str | Path,
    note_title: str,
    download_image: Callable[[str, Path], None] | None = None,
) -> str | None:
    local_target, remote_target, label = resolve_image_targets(image)
    vault_root = Path(vault_root)
    note_dir = sanitize_filename(note_title)
    asset_dir = vault_root / "assets" / note_dir

    if local_target:
        source_path = Path(local_target).expanduser()
        if source_path.exists() and source_path.is_file():
            destination = _unique_path(asset_dir / source_path.name)
            destination.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(source_path, destination)
            rel_path = destination.relative_to(vault_root).as_posix()
            return f"![{_escape_markdown_label(label)}]({rel_path})"
        if _looks_remote(local_target):
            remote_target = local_target
        else:
            rel_path = Path(local_target).as_posix()
            return f"![{_escape_markdown_label(label)}]({rel_path})"

    if remote_target:
        filename = Path(urllib.parse.urlparse(remote_target).path).name or "image"
        if not Path(filename).suffix:
            filename = f"{Path(filename).stem or 'image'}.png"
        destination = _unique_path(asset_dir / filename)
        try:
            destination.parent.mkdir(parents=True, exist_ok=True)
            (download_image or download_remote_image)(remote_target, destination)
        except Exception:
            if destination.exists():
                try:
                    destination.unlink()
                except OSError:
                    pass
            for candidate in (destination.parent, asset_dir.parent):
                try:
                    if candidate.exists() and candidate.is_dir() and not any(candidate.iterdir()):
                        candidate.rmdir()
                except OSError:
                    pass
            return f"![{_escape_markdown_label(label)}](<{remote_target}>)"
        rel_path = destination.relative_to(vault_root).as_posix()
        return f"![{_escape_markdown_label(label)}]({rel_path})"

    return None

"""Output helpers for stdout + file export."""

from __future__ import annotations

from pathlib import Path


def export_rendered_output(content: str, output_path: str | None) -> None:
    if output_path is None:
        return
    target = Path(output_path)
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(content, encoding="utf-8")

#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from common import ensure_parent, slugify, utc_now_iso
from config import LibrarianSettings
from models import ArchitectOutput, SynthesizedContent


class VaultFileManager:
    def __init__(self, settings: LibrarianSettings) -> None:
        self.settings = settings

    def write_note(self, architect_output: ArchitectOutput, synthesized: SynthesizedContent) -> Path:
        category_dir = self.settings.vault_path / architect_output.category
        category_dir.mkdir(parents=True, exist_ok=True)

        base_slug = slugify(synthesized.title, fallback="captured-note")
        final_path = category_dir / f"{base_slug}.md"
        counter = 2
        while final_path.exists():
            final_path = category_dir / f"{base_slug}-{counter}.md"
            counter += 1

        frontmatter = dict(architect_output.frontmatter)
        frontmatter.setdefault("title", synthesized.title)
        frontmatter.setdefault("summary", synthesized.summary)
        frontmatter.setdefault("tags", [])
        frontmatter.setdefault("source", "manual paste")
        frontmatter["createdAt"] = utc_now_iso()
        frontmatter["updatedAt"] = frontmatter["createdAt"]

        note_text = self._render_frontmatter(frontmatter) + "\n" + architect_output.wikilinked_body.strip() + "\n"
        ensure_parent(final_path)
        final_path.write_text(note_text, encoding="utf-8")
        return final_path

    @staticmethod
    def remove_inbox_file(path: Path) -> None:
        try:
            path.unlink()
        except FileNotFoundError:
            return

    def _render_frontmatter(self, frontmatter: dict[str, Any]) -> str:
        lines = ["---"]
        for key in ("title", "summary", "source", "tags", "needs_review", "createdAt", "updatedAt"):
            if key not in frontmatter:
                continue
            value = frontmatter[key]
            lines.extend(self._render_yaml_item(key, value))
        lines.append("---")
        return "\n".join(lines)

    def _render_yaml_item(self, key: str, value: Any) -> list[str]:
        if isinstance(value, list):
            if not value:
                return [f"{key}: []"]
            lines = [f"{key}:"]
            for item in value:
                lines.append(f"  - {self._yaml_scalar(item)}")
            return lines
        return [f"{key}: {self._yaml_scalar(value)}"]

    @staticmethod
    def _yaml_scalar(value: Any) -> str:
        if isinstance(value, bool):
            return "true" if value else "false"
        if value is None:
            return "null"
        if isinstance(value, (int, float)):
            return str(value)
        return json.dumps(str(value), ensure_ascii=False)

#!/usr/bin/env python3
from __future__ import annotations

import re
from pathlib import Path


class VaultIndex:
    def __init__(self, vault_path: Path, inbox_folder: str = "_Inbox") -> None:
        self.vault_path = vault_path
        self.inbox_folder = inbox_folder
        self._concepts: dict[str, set[str]] = {}

    def build(self) -> "VaultIndex":
        self._concepts.clear()
        for path in self.vault_path.rglob("*.md"):
            if ".obsidian" in path.parts or self.inbox_folder in path.parts:
                continue
            title, aliases = self._extract_concepts_from_file(path)
            self.add_concept(title, aliases)
        return self

    def get_concepts_list(self) -> list[str]:
        return sorted(self._concepts.keys(), key=str.lower)

    def add_concept(self, name: str, aliases: list[str] | None = None) -> None:
        clean_name = name.strip()
        if not clean_name:
            return
        self._concepts.setdefault(clean_name, set())
        for alias in aliases or []:
            clean_alias = alias.strip()
            if clean_alias:
                self._concepts.setdefault(clean_alias, set()).add(clean_name)

    def _extract_concepts_from_file(self, path: Path) -> tuple[str, list[str]]:
        title = path.stem.replace("-", " ").strip()
        aliases: list[str] = []

        try:
            text = path.read_text(encoding="utf-8")
        except Exception:
            return title, aliases

        if not text.startswith("---"):
            return title, aliases

        parts = text.split("---", 2)
        if len(parts) < 3:
            return title, aliases
        frontmatter = parts[1]

        title_match = re.search(r"^title:\s*(.+)$", frontmatter, flags=re.MULTILINE)
        if title_match:
            title = self._strip_yaml_scalar(title_match.group(1)) or title

        aliases_match = re.search(r"^aliases:\s*\[(.*?)\]\s*$", frontmatter, flags=re.MULTILINE)
        if aliases_match:
            raw_aliases = [item.strip() for item in aliases_match.group(1).split(",") if item.strip()]
            aliases.extend(self._strip_yaml_scalar(item) for item in raw_aliases)
        else:
            lines = frontmatter.splitlines()
            collecting = False
            for line in lines:
                if line.startswith("aliases:"):
                    collecting = True
                    continue
                if collecting:
                    if re.match(r"^\s*-\s+", line):
                        alias = re.sub(r"^\s*-\s+", "", line)
                        aliases.append(self._strip_yaml_scalar(alias))
                    elif line.strip():
                        break

        aliases = [alias for alias in aliases if alias]
        return title, aliases

    @staticmethod
    def _strip_yaml_scalar(value: str) -> str:
        clean = value.strip()
        if clean.startswith(("'", '"')) and clean.endswith(("'", '"')) and len(clean) >= 2:
            clean = clean[1:-1]
        return clean.strip()

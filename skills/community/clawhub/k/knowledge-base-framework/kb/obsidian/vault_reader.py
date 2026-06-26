"""
Vault Reader - Read entries from Obsidian Vault
=================================================

Reads .md files from an Obsidian vault, parses YAML frontmatter,
and converts them to KB-compatible entry dictionaries.

Supports:
- YAML frontmatter parsing (--- delimiters)
- Fallback to filename-based titles
- Modified-since tracking for incremental sync
"""

from __future__ import annotations

import logging
import re
from datetime import datetime
from pathlib import Path
from typing import Optional

from .conflict import MalformedFrontmatterError

logger = logging.getLogger(__name__)

# Frontmatter delimiter pattern
FRONTMATTER_PATTERN = re.compile(
    r"^---\s*\n(.*?)\n---\s*\n?",
    re.DOTALL,
)


class VaultReader:
    """Read .md files from an Obsidian vault and convert to KB entries.

    Args:
        vault_path: Root path of the Obsidian vault.
    """

    def __init__(self, vault_path: Path):
        self.vault = Path(vault_path)

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def read_entry(self, path: Path) -> dict:
        """Read a .md file and parse it into a KB entry dict.

        Args:
            path: Path to the markdown file (absolute or relative to vault).

        Returns:
            Dict with keys: title, authors, year, tags, abstract, content,
            file_path, modified, frontmatter.

        Raises:
            MalformedFrontmatterError: If frontmatter cannot be parsed.
            FileNotFoundError: If the file does not exist.
        """
        path = Path(path)
        if not path.is_absolute():
            path = self.vault / path

        if not path.exists():
            raise FileNotFoundError(f"Vault file not found: {path}")

        content = path.read_text(encoding="utf-8")
        frontmatter, body = self._parse_frontmatter(content)

        return self._to_kb_entry(frontmatter, body, path)

    def list_entries(self) -> list[Path]:
        """List all .md files in the vault (excluding hidden dirs)."""
        return [
            p
            for p in self.vault.rglob("*.md")
            if not self._is_hidden(p)
        ]

    def get_modified_since(self, since: datetime) -> list[Path]:
        """Find vault entries modified after the given timestamp.

        Args:
            since: Cutoff datetime. Files with mtime after this are included.

        Returns:
            List of modified file paths.
        """
        modified = []
        for path in self.list_entries():
            try:
                mtime = datetime.fromtimestamp(path.stat().st_mtime)
                if mtime > since:
                    modified.append(path)
            except OSError:
                logger.debug(f"Cannot stat {path}, skipping")
        return modified

    # ------------------------------------------------------------------
    # Frontmatter Parsing
    # ------------------------------------------------------------------

    def _parse_frontmatter(self, content: str) -> tuple[dict, str]:
        """Parse YAML frontmatter from markdown content.

        Returns:
            Tuple of (frontmatter_dict, body_text).
            If no frontmatter is found, returns ({}, full_content).
        """
        match = FRONTMATTER_PATTERN.match(content)
        if not match:
            return {}, content

        yaml_str = match.group(1)
        body = content[match.end():]

        try:
            import yaml
            frontmatter = yaml.safe_load(yaml_str)
            if frontmatter is None:
                frontmatter = {}
            if not isinstance(frontmatter, dict):
                logger.warning(
                    f"Frontmatter is {type(frontmatter).__name__}, expected dict"
                )
                frontmatter = {}
        except yaml.YAMLError as e:
            raise MalformedFrontmatterError(
                f"Cannot parse frontmatter: {e}"
            ) from e

        return frontmatter, body

    # ------------------------------------------------------------------
    # Conversion
    # ------------------------------------------------------------------

    def _to_kb_entry(self, frontmatter: dict, body: str, path: Path) -> dict:
        """Convert parsed frontmatter + body to a KB entry dict.

        Maps standard YAML fields to KB entry keys. Missing fields
        get sensible defaults.
        """
        # Ensure tags is always a list
        tags = frontmatter.get("tags", [])
        if isinstance(tags, str):
            tags = [t.strip() for t in tags.split(",") if t.strip()]

        # Ensure authors is always a list
        authors = frontmatter.get("authors", [])
        if isinstance(authors, str):
            authors = [a.strip() for a in authors.split(";") if a.strip()]

        # Modified time from filesystem
        try:
            mtime = datetime.fromtimestamp(path.stat().st_mtime).isoformat()
        except OSError:
            mtime = None

        return {
            "title": frontmatter.get("title", path.stem),
            "authors": authors,
            "year": frontmatter.get("year"),
            "tags": tags,
            "abstract": frontmatter.get("abstract", body[:500].strip() if body else ""),
            "content": body.strip(),
            "file_path": str(path),
            "modified": mtime,
            "frontmatter": frontmatter,
        }

    # ------------------------------------------------------------------
    # Helpers
    # ------------------------------------------------------------------

    @staticmethod
    def _is_hidden(path: Path) -> bool:
        """Check if a path is inside a hidden directory (starts with .)."""
        for part in path.relative_to(Path("/")).parts:
            if part.startswith(".") and part not in (".", ".."):
                return True
        try:
            rel = path.relative_to(path.anchor)
            for part in rel.parts:
                if part.startswith("."):
                    return True
        except ValueError:
            pass
        # Simple check: any parent dir starting with .
        parts = path.parts
        for part in parts:
            if part.startswith(".") and part not in (".", ".."):
                return True
        return False
"""
Sync Manager - Bidirectional sync between KB and Obsidian Vault
================================================================

Orchestrates bidirectional synchronization between the KB SQLite
database and an Obsidian vault (directory of .md files).

Features:
- KB → Vault: Export entries as markdown with YAML frontmatter
- Vault → KB: Import/upserv vault notes as KB entries
- Bidirectional: Detect changes since last sync, resolve conflicts
- Dry-run mode: Preview changes without writing
- Incremental: Only sync entries modified since last sync

Architecture:
-------------
    SyncManager
    ├── VaultReader      (reads .md files from vault)
    ├── SyncState        (tracks last sync timestamps)
    ├── KBConnection     (reads/writes KB database)
    └── ConflictResolution (resolves sync conflicts)
"""

from __future__ import annotations

import json
import logging
from datetime import datetime
from pathlib import Path
from typing import Optional

import yaml

from .conflict import (
    ConflictResolution,
    VaultSyncError,
    FilePermissionError,
    SyncConflictError,
)
from .sync_state import SyncState
from .vault_reader import VaultReader

logger = logging.getLogger(__name__)


class SyncManager:
    """Manage bidirectional sync between KB and Obsidian vault.

    Args:
        kb_path: Path to the KB SQLite database.
        vault_path: Path to the Obsidian vault directory.
        strategy: Default conflict resolution strategy.
    """

    def __init__(
        self,
        kb_path: Path,
        vault_path: Path,
        strategy: ConflictResolution = ConflictResolution.KB_WINS,
    ):
        self.kb_path = Path(kb_path)
        self.vault_path = Path(vault_path)
        self.strategy = strategy

        self.reader = VaultReader(self.vault_path)
        self.state = SyncState.load(self.vault_path)

        # Ensure vault directory exists
        self.vault_path.mkdir(parents=True, exist_ok=True)

        # Conflicts directory (for MANUAL strategy)
        self.conflicts_dir = self.vault_path / "_conflicts"
        self.conflicts_dir.mkdir(exist_ok=True)

    # ------------------------------------------------------------------
    # KB → Vault
    # ------------------------------------------------------------------

    def sync_to_vault(
        self,
        entry_id: int,
        vault_path: Optional[Path] = None,
        dry_run: bool = False,
    ) -> Path:
        """Write a KB entry to the Obsidian vault as a .md file.

        Args:
            entry_id: ID of the KB entry to export.
            vault_path: Optional override for vault root.
            dry_run: If True, don't write files, just return the path.

        Returns:
            Path to the created/updated note.

        Raises:
            VaultSyncError: If the entry cannot be found or written.
        """
        vault_root = Path(vault_path) if vault_path else self.vault_path
        vault_root.mkdir(parents=True, exist_ok=True)

        # Read entry from KB database
        entry = self._get_kb_entry(entry_id)
        if entry is None:
            raise VaultSyncError(f"KB entry {entry_id} not found")

        # Generate filename: sanitize title
        filename = self._sanitize_filename(entry.get("title", f"entry_{entry_id}"))
        note_path = vault_root / f"{filename}.md"

        if dry_run:
            logger.info(f"[DRY RUN] Would write: {note_path}")
            return note_path

        # Build frontmatter
        frontmatter = self._entry_to_frontmatter(entry)

        # Build note content
        content = entry.get("content", entry.get("abstract", ""))
        note_content = self._build_note(frontmatter, content)

        # Write file
        try:
            note_path.write_text(note_content, encoding="utf-8")
        except OSError as e:
            raise FilePermissionError(f"Cannot write to {note_path}: {e}") from e

        logger.info(f"KB entry {entry_id} → {note_path}")
        self.state.mark_kb_sync()
        self.state.save(self.vault_path)

        return note_path

    # ------------------------------------------------------------------
    # Vault → KB
    # ------------------------------------------------------------------

    def sync_from_vault(
        self,
        path: Path,
        dry_run: bool = False,
    ) -> int:
        """Read a vault .md file and upsert it to the KB database.

        Args:
            path: Path to the vault note (relative or absolute).
            dry_run: If True, don't write to DB, just return parsed data.

        Returns:
            KB entry ID (or 0 for dry_run).

        Raises:
            VaultSyncError: If the entry cannot be parsed or written.
        """
        entry_data = self.reader.read_entry(path)

        if dry_run:
            logger.info(f"[DRY RUN] Would upsert: {entry_data.get('title', '?')}")
            return 0

        # Upsert to KB database
        entry_id = self._upsert_kb_entry(entry_data)

        logger.info(f"Vault {path} → KB entry {entry_id}")
        self.state.mark_vault_sync()
        self.state.save(self.vault_path)

        return entry_id

    # ------------------------------------------------------------------
    # Bidirectional Sync
    # ------------------------------------------------------------------

    def bidirectional_sync(
        self,
        strategy: Optional[ConflictResolution] = None,
        dry_run: bool = False,
    ) -> dict:
        """Full bidirectional sync with conflict resolution.

        1. Find vault entries modified since last sync → import to KB
        2. Find KB entries not in vault → export to vault
        3. Resolve conflicts using the chosen strategy

        Args:
            strategy: Override default conflict resolution strategy.
            dry_run: If True, don't write anything, just report.

        Returns:
            Dict with sync statistics.
        """
        strategy = strategy or self.strategy
        stats = {
            "vault_to_kb": 0,
            "kb_to_vault": 0,
            "conflicts": 0,
            "skipped": 0,
            "errors": 0,
        }

        # 1. Vault → KB: Import modified vault entries
        since = self.state.vault_last_sync_dt
        if since:
            modified = self.reader.get_modified_since(since)
        else:
            modified = self.reader.list_entries()

        logger.info(f"Vault → KB: {len(modified)} modified entries since {since}")

        for vault_path in modified:
            try:
                self._sync_single_from_vault(vault_path, strategy, dry_run, stats)
            except Exception as e:
                logger.warning(f"Error syncing {vault_path}: {e}")
                stats["errors"] += 1

        # 2. KB → Vault: Export KB entries not yet in vault
        kb_entries = self._get_all_kb_entries()
        for entry in kb_entries:
            title = entry.get("title", "")
            if not self._exists_in_vault(title):
                try:
                    if not dry_run:
                        self.sync_to_vault(entry["id"])
                    stats["kb_to_vault"] += 1
                except Exception as e:
                    logger.warning(f"Error exporting entry {entry.get('id')}: {e}")
                    stats["errors"] += 1

        # 3. Update sync state
        if not dry_run:
            self.state.mark_kb_sync()
            self.state.mark_vault_sync()
            self.state.save(self.vault_path)

        logger.info(
            f"Sync complete: vault→kb={stats['vault_to_kb']}, "
            f"kb→vault={stats['kb_to_vault']}, "
            f"conflicts={stats['conflicts']}, "
            f"errors={stats['errors']}"
        )

        return stats

    # ------------------------------------------------------------------
    # Internal: Single File Sync
    # ------------------------------------------------------------------

    def _sync_single_from_vault(
        self,
        vault_path: Path,
        strategy: ConflictResolution,
        dry_run: bool,
        stats: dict,
    ) -> None:
        """Sync a single vault file with conflict handling."""
        vault_entry = self.reader.read_entry(vault_path)
        kb_entry = self._find_kb_entry_by_title(vault_entry.get("title", ""))

        if kb_entry is None:
            # New entry from vault → insert
            if not dry_run:
                self._upsert_kb_entry(vault_entry)
            stats["vault_to_kb"] += 1
            return

        # Existing entry → check for conflict
        kb_modified = kb_entry.get("modified")
        vault_modified = vault_entry.get("modified")

        # Simple conflict detection: both modified since last sync
        is_conflict = False
        if kb_modified and vault_modified:
            try:
                kb_dt = datetime.fromisoformat(kb_modified) if isinstance(kb_modified, str) else kb_modified
                vault_dt = datetime.fromisoformat(vault_modified) if isinstance(vault_modified, str) else vault_modified
                last_sync = self.state.kb_last_sync_dt

                if last_sync and kb_dt > last_sync and vault_dt > last_sync:
                    is_conflict = True
            except (ValueError, TypeError):
                pass

        if not is_conflict:
            # No conflict → just update
            if not dry_run:
                vault_entry["id"] = kb_entry["id"]
                self._upsert_kb_entry(vault_entry)
            stats["vault_to_kb"] += 1
            return

        # Conflict resolution
        stats["conflicts"] += 1

        if strategy == ConflictResolution.VAULT_WINS:
            if not dry_run:
                vault_entry["id"] = kb_entry["id"]
                self._upsert_kb_entry(vault_entry)
            stats["vault_to_kb"] += 1

        elif strategy == ConflictResolution.KB_WINS:
            # KB wins → export KB entry to vault (overwrite vault file)
            if not dry_run:
                self.sync_to_vault(kb_entry["id"])
            stats["kb_to_vault"] += 1

        elif strategy == ConflictResolution.KEEP_BOTH:
            # Keep both → rename vault file with suffix
            if not dry_run:
                self._save_conflict_copy(vault_path, vault_entry, kb_entry)
            stats["skipped"] += 1

        elif strategy == ConflictResolution.MANUAL:
            # Flag for manual resolution
            if not dry_run:
                self._flag_conflict(vault_path, vault_entry, kb_entry)
            stats["skipped"] += 1

    # ------------------------------------------------------------------
    # Internal: KB Database Access
    # ------------------------------------------------------------------

    def _validate_kb_schema(self) -> bool:
        """Validate KB database has required schema."""
        with sqlite3.connect(str(self.kb_path)) as conn:
            cursor = conn.execute(
                "SELECT name FROM sqlite_master WHERE type='table' AND name='entries'"
            )
            if not cursor.fetchone():
                return False
            cursor = conn.execute("PRAGMA table_info(entries)")
            columns = {row[1] for row in cursor.fetchall()}
            required = {'id', 'title', 'authors', 'year', 'tags', 'content'}
            return required.issubset(columns)

    def _get_kb_entry(self, entry_id: int) -> Optional[dict]:
        """Read a single entry from the KB database."""
        import sqlite3

        try:
            with sqlite3.connect(str(self.kb_path)) as conn:
                conn.execute("PRAGMA foreign_keys=ON")
                conn.row_factory = sqlite3.Row
                cursor = conn.execute(
                    "SELECT * FROM entries WHERE id = ?",
                    (entry_id,),
                )
                row = cursor.fetchone()

            if row:
                return dict(row)
            return None
        except Exception as e:
            logger.warning(f"KB read error: {e}")
            return None

    def _get_all_kb_entries(self) -> list[dict]:
        """Read all entries from the KB database."""
        import sqlite3

        try:
            with sqlite3.connect(str(self.kb_path)) as conn:
                conn.execute("PRAGMA foreign_keys=ON")
                conn.row_factory = sqlite3.Row
                cursor = conn.execute("SELECT * FROM entries")
                rows = [dict(r) for r in cursor.fetchall()]
            return rows
        except Exception as e:
            logger.warning(f"KB read error: {e}")
            raise

    def _find_kb_entry_by_title(self, title: str) -> Optional[dict]:
        """Find a KB entry by title (case-insensitive)."""
        if not title:
            return None

        import sqlite3

        try:
            with sqlite3.connect(str(self.kb_path)) as conn:
                conn.execute("PRAGMA foreign_keys=ON")
                conn.row_factory = sqlite3.Row
                cursor = conn.execute(
                    "SELECT * FROM entries WHERE LOWER(title) = LOWER(?)",
                    (title,),
                )
                row = cursor.fetchone()

            if row:
                return dict(row)
            return None
        except Exception as e:
            logger.warning(f"KB lookup error: {e}")
            return None

    def _upsert_kb_entry(self, entry_data: dict) -> int:
        """Insert or update a KB entry from vault data.

        Returns the entry ID.
        """
        import sqlite3

        entry_id = entry_data.get("id")
        title = entry_data.get("title", "Untitled")
        authors = entry_data.get("authors", [])
        if isinstance(authors, list):
            authors = json.dumps(authors)
        year = entry_data.get("year")
        tags = entry_data.get("tags", [])
        if isinstance(tags, list):
            tags = json.dumps(tags)
        abstract = entry_data.get("abstract", "")
        content = entry_data.get("content", "")
        modified = entry_data.get("modified", datetime.now().isoformat())

        try:
            with sqlite3.connect(str(self.kb_path)) as conn:
                conn.execute("PRAGMA foreign_keys=ON")

                if entry_id:
                    conn.execute(
                        """UPDATE entries SET
                           title=?, authors=?, year=?, tags=?, abstract=?,
                           content=?, modified=?
                           WHERE id=?""",
                        (title, authors, year, tags, abstract, content, modified, entry_id),
                    )
                else:
                    cursor = conn.execute(
                        """INSERT INTO entries (title, authors, year, tags, abstract, content, modified)
                           VALUES (?, ?, ?, ?, ?, ?, ?)""",
                        (title, authors, year, tags, abstract, content, modified),
                    )
                    entry_id = cursor.lastrowid

                conn.commit()
            return entry_id or 0

        except Exception as e:
            logger.error(f"KB upsert error: {e}")
            raise VaultSyncError(f"Cannot upsert entry: {e}") from e

    # ------------------------------------------------------------------
    # Internal: Vault File Helpers
    # ------------------------------------------------------------------

    def _exists_in_vault(self, title: str) -> bool:
        """Check if a note with the given title exists in the vault."""
        filename = self._sanitize_filename(title) + ".md"
        return (self.vault_path / filename).exists()

    def _entry_to_frontmatter(self, entry: dict) -> dict:
        """Convert KB entry dict to YAML frontmatter dict."""
        fm = {}
        if entry.get("title"):
            fm["title"] = entry["title"]
        if entry.get("authors"):
            authors = entry["authors"]
            if isinstance(authors, str):
                try:
                    authors = json.loads(authors)
                except (json.JSONDecodeError, TypeError):
                    authors = [a.strip() for a in authors.split(";") if a.strip()]
            fm["authors"] = authors
        if entry.get("year"):
            fm["year"] = entry["year"]
        if entry.get("tags"):
            tags = entry["tags"]
            if isinstance(tags, str):
                try:
                    tags = json.loads(tags)
                except (json.JSONDecodeError, TypeError):
                    tags = [t.strip() for t in tags.split(",") if t.strip()]
            fm["tags"] = tags
        if entry.get("type"):
            fm["type"] = entry["type"]
        if entry.get("abstract"):
            fm["abstract"] = entry["abstract"]
        return fm

    @staticmethod
    def _build_note(frontmatter: dict, content: str) -> str:
        """Build a complete markdown note with frontmatter."""
        parts = []
        if frontmatter:
            parts.append("---")
            parts.append(yaml.dump(frontmatter, allow_unicode=True, default_flow_style=False).strip())
            parts.append("---")
            parts.append("")
        parts.append(content)
        return "\n".join(parts)

    @staticmethod
    def _sanitize_filename(title: str) -> str:
        """Convert a title to a safe filename (no special chars)."""
        # Replace problematic characters
        safe = title.strip()
        for char in ['/', '\\', ':', '*', '?', '"', '<', '>', '|', '#']:
            safe = safe.replace(char, '_')
        # Collapse multiple underscores/spaces
        safe = '_'.join(safe.split())
        return safe[:200]  # Limit length

    def _flag_conflict(self, vault_path: Path, vault_entry: dict, kb_entry: dict) -> None:
        """Save a conflict marker for manual resolution."""
        conflict_file = self.conflicts_dir / f"{vault_path.stem}_conflict.json"
        conflict_data = {
            "vault_file": str(vault_path),
            "vault_title": vault_entry.get("title"),
            "vault_modified": vault_entry.get("modified"),
            "kb_entry_id": kb_entry.get("id"),
            "kb_modified": kb_entry.get("modified"),
            "detected_at": datetime.now().isoformat(),
            "resolution": "pending",
        }
        conflict_file.write_text(
            json.dumps(conflict_data, indent=2, ensure_ascii=False),
            encoding="utf-8",
        )
        logger.warning(f"Conflict flagged: {conflict_file}")

    def _save_conflict_copy(self, vault_path: Path, vault_entry: dict, kb_entry: dict) -> None:
        """Save both versions when KEEP_BOTH strategy is used."""
        # Rename vault file with _vault suffix
        vault_stem = vault_path.stem
        vault_copy = vault_path.parent / f"{vault_stem}_vault.md"
        vault_path.rename(vault_copy)

        # Write KB version as the main file
        self.sync_to_vault(kb_entry["id"])

        logger.info(f"KEEP_BOTH: vault version → {vault_copy}, KB version → {vault_path}")

    # ------------------------------------------------------------------
    # Status
    # ------------------------------------------------------------------

    def get_status(self) -> dict:
        """Get current sync status and statistics."""
        return {
            "vault_path": str(self.vault_path),
            "kb_path": str(self.kb_path),
            "strategy": self.strategy.value,
            "kb_last_sync": self.state.kb_last_sync,
            "vault_last_sync": self.state.vault_last_sync,
            "conflicts": len(self.state.conflicts),
            "vault_entries": len(self.reader.list_entries()),
            "pending_conflicts": len(list(self.conflicts_dir.glob("*.json"))) if self.conflicts_dir.exists() else 0,
        }
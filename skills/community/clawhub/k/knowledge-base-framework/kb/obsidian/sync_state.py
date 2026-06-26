"""
KB-Obsidian Sync State Tracking
================================

Tracks the last sync timestamps and conflict resolution
strategy between the KB database and an Obsidian vault.

State is persisted as JSON in the vault directory.
"""

from __future__ import annotations

import json
import logging
from dataclasses import dataclass, field, asdict
from datetime import datetime
from pathlib import Path
from typing import Optional

logger = logging.getLogger(__name__)

DEFAULT_STATE_FILE = ".kb_sync_state.json"


@dataclass
class SyncState:
    """Tracks sync state between KB and Obsidian vault.

    Persisted as JSON alongside the vault for easy access.

    Attributes:
        kb_last_sync: Timestamp of last KB → Vault sync.
        vault_last_sync: Timestamp of last Vault → KB sync.
        conflict_resolution: Default conflict resolution strategy.
        last_sync_ids: Set of entry IDs synced in last run (for incremental sync).
        conflicts: List of unresolved conflict identifiers.
    """
    kb_last_sync: Optional[str] = None
    vault_last_sync: Optional[str] = None
    conflict_resolution: str = "kb_wins"  # 'kb_wins' | 'vault_wins' | 'manual' | 'keep_both'
    last_sync_ids: list = field(default_factory=list)
    conflicts: list = field(default_factory=list)

    # ------------------------------------------------------------------
    # Persistence
    # ------------------------------------------------------------------

    @classmethod
    def load(cls, vault_path: Path) -> "SyncState":
        """Load sync state from vault directory.

        Returns a default state if no state file exists.
        """
        state_file = vault_path / DEFAULT_STATE_FILE
        if state_file.exists():
            try:
                data = json.loads(state_file.read_text(encoding="utf-8"))
                return cls(**data)
            except (json.JSONDecodeError, TypeError) as e:
                logger.warning(f"Corrupt sync state file ({e}), using defaults")
        return cls()

    def save(self, vault_path: Path) -> None:
        """Persist sync state to vault directory."""
        state_file = vault_path / DEFAULT_STATE_FILE
        vault_path.mkdir(parents=True, exist_ok=True)
        state_file.write_text(
            json.dumps(asdict(self), indent=2, ensure_ascii=False),
            encoding="utf-8",
        )
        logger.debug(f"Sync state saved to {state_file}")

    # ------------------------------------------------------------------
    # Helpers
    # ------------------------------------------------------------------

    def mark_kb_sync(self) -> None:
        """Record a successful KB → Vault sync."""
        self.kb_last_sync = datetime.now().isoformat()

    def mark_vault_sync(self) -> None:
        """Record a successful Vault → KB sync."""
        self.vault_last_sync = datetime.now().isoformat()

    @property
    def kb_last_sync_dt(self) -> Optional[datetime]:
        if self.kb_last_sync:
            try:
                return datetime.fromisoformat(self.kb_last_sync)
            except ValueError:
                pass
        return None

    @property
    def vault_last_sync_dt(self) -> Optional[datetime]:
        if self.vault_last_sync:
            try:
                return datetime.fromisoformat(self.vault_last_sync)
            except ValueError:
                pass
        return None
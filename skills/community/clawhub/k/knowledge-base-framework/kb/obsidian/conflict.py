"""
KB-Obsidian Conflict Resolution
=================================

Defines conflict resolution strategies for bidirectional sync
between KB database and Obsidian vault.
"""

from __future__ import annotations

from enum import Enum


class ConflictResolution(Enum):
    """Strategy for resolving sync conflicts.

    Values:
        KB_WINS: KB database entry overwrites vault file.
        VAULT_WINS: Vault file overwrites KB entry.
        MANUAL: Conflict is flagged for manual resolution.
        KEEP_BOTH: Both versions are kept (vault file gets a suffix).
    """
    KB_WINS = "kb_wins"
    VAULT_WINS = "vault_wins"
    MANUAL = "manual"
    KEEP_BOTH = "keep_both"

    @classmethod
    def from_string(cls, value: str) -> "ConflictResolution":
        """Create from string value (case-insensitive)."""
        try:
            return cls(value.lower())
        except ValueError:
            raise ValueError(
                f"Invalid conflict resolution: '{value}'. "
                f"Valid options: {', '.join(m.value for m in cls)}"
            )


class VaultSyncError(Exception):
    """Base exception for vault sync operations."""
    pass


class FilePermissionError(VaultSyncError):
    """Cannot read from or write to vault directory."""
    pass


class MalformedFrontmatterError(VaultSyncError):
    """Frontmatter in markdown file cannot be parsed."""
    pass


class MissingRequiredFieldError(VaultSyncError):
    """A required field is missing from the entry."""
    pass


class SyncConflictError(VaultSyncError):
    """A sync conflict was detected and needs resolution."""
    pass
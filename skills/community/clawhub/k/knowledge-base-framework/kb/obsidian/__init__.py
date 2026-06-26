"""
Obsidian Integration Module for KB Framework.

Parses Obsidian vault files: WikiLinks, Tags, Frontmatter, Embeds.
Resolves wiki links to file paths using shortest-match algorithm.
"""

from .parser import (
    WIKILINK_PATTERN,
    EMBED_PATTERN,
    TAG_PATTERN,
    FRONTMATTER_PATTERN,
    parse_frontmatter,
    extract_wikilinks,
    extract_tags,
    extract_embeds,
)

from .vault import ObsidianVault

from .resolver import (
    PathResolver,
    resolve_wikilink,
)

from .writer import (
    VaultWriter,
    create_note,
    update_frontmatter,
)

from .sync_manager import SyncManager
from .vault_reader import VaultReader
from .sync_state import SyncState
from .conflict import (
    ConflictResolution,
    VaultSyncError,
    FilePermissionError,
    MalformedFrontmatterError,
    MissingRequiredFieldError,
    SyncConflictError,
)

__all__ = [
    # Parser
    'WIKILINK_PATTERN',
    'EMBED_PATTERN',
    'TAG_PATTERN',
    'FRONTMATTER_PATTERN',
    'parse_frontmatter',
    'extract_wikilinks',
    'extract_tags',
    'extract_embeds',
    # Resolver
    'PathResolver',
    'resolve_wikilink',
    # Writer
    'VaultWriter',
    'create_note',
    'update_frontmatter',
    # Vault
    'ObsidianVault',
    # Sync
    'SyncManager',
    'VaultReader',
    'SyncState',
    'ConflictResolution',
    'VaultSyncError',
    'FilePermissionError',
    'MalformedFrontmatterError',
    'MissingRequiredFieldError',
    'SyncConflictError',
]

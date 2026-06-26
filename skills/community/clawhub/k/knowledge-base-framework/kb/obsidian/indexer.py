"""
Obsidian Backlink Indexer - Build and query an inverted index of backlinks.

Obsidian does not pre-compute backlinks - this module builds an inverted index
that maps each note to all files that link TO it, along with context.
"""

import re
from pathlib import Path
from typing import Optional
import sys

# Import from Phase 1 and Phase 2
from .parser import extract_wikilinks, parse_frontmatter, extract_context
from .resolver import PathResolver


# =============================================================================
# BACKLINK INDEXER
# =============================================================================

class BacklinkIndexer:
    """
    Builds and maintains an inverted index of all backlinks.
    
    For each file, stores:
    - Which files link TO it
    - The context around the link
    - The link text (alias if present, otherwise target)
    
    The index is built incrementally:
        - index_vault(): Build complete index for vault
        - index_file(): Update index for single file
        - get_backlinks(): Query backlinks for a file
        - get_unlinked_mentions(): Find text mentions without wikilinks
    
    Example:
        >>> indexer = BacklinkIndexer("/path/to/vault")
        >>> indexer.index_vault()
        >>> backlinks = indexer.get_backlinks(Path("Note A.md"))
        >>> # Returns [{'source': Path("Note B.md"), 'context': '...', 'link_text': 'Note A'}, ...]
    """
    
    def __init__(self, vault_path: Path | str):
        """
        Initialize BacklinkIndexer.
        
        Args:
            vault_path: Root path of the Obsidian vault
        """
        self.vault_path = Path(vault_path)
        self.resolver = PathResolver(vault_path)
        
        # Inverted index: target_file -> list of backlink info
        # Key is the normalized note name (e.g., "Note A.md")
        # Value is list of dicts with source, context, link_text
        self._backlink_index: dict[str, list[dict]] = {}
        
        # Cache for normalized file names (for case-insensitive lookup)
        self._normalized_names: dict[Path, str] = {}
        
        # Context window size for backlink context
        self._context_chars = 100
    
    def index_vault(self, vault_path: Optional[Path] = None) -> dict[str, list[dict]]:
        """
        Index entire vault, building complete backlink graph.
        
        O(n) where n is total number of files in vault.
        
        Args:
            vault_path: Override vault path (uses instance vault_path if None)
        
        Returns:
            The complete backlink index dictionary
        """
        vault = vault_path or self.vault_path
        
        if not vault.exists():
            return self._backlink_index
        
        # Clear existing index
        self._backlink_index.clear()
        self._normalized_names.clear()
        
        # Build normalized name cache first
        self._build_name_cache(vault)
        
        # Process each markdown file
        for md_file in vault.rglob('*.md'):
            self._process_file(md_file)
        
        return self._backlink_index
    
    def index_file(self, file_path: Path) -> None:
        """
        Index single file, updating backlinks for all links in this file.
        
        This updates:
        1. All existing backlinks FROM this file are removed (in case content changed)
        2. All new backlinks FROM this file are added
        
        Args:
            file_path: Path to the markdown file to index
        """
        file_path = Path(file_path)
        
        if not file_path.exists():
            return
        
        # Remove all existing backlinks FROM this file (not TO it)
        self._remove_backlinks_from(file_path)
        
        # Ensure file is in name cache
        self._ensure_in_name_cache(file_path)
        
        # Process this file (extract links and add backlinks)
        self._process_file(file_path)
    
    def get_backlinks(self, file_path: Path) -> list[dict]:
        """
        Get all files that link to this file.
        
        Args:
            file_path: The target file to get backlinks for
        
        Returns:
            List of dictionaries with keys:
                - source: Path to the file containing the link
                - context: Text surrounding the link (normalized whitespace)
                - link_text: Display text of the link (alias or target)
                - link_target: The raw target from [[target]]
        """
        file_path = Path(file_path)
        
        # Get all possible keys for this file
        keys = self._get_all_index_keys(file_path)
        
        # Collect all backlinks
        all_backlinks = []
        seen = set()
        
        for key in keys:
            if key in self._backlink_index:
                for backlink in self._backlink_index[key]:
                    # Deduplicate by source + link_text
                    seen_key = (str(backlink['source']), backlink['link_text'])
                    if seen_key not in seen:
                        seen.add(seen_key)
                        all_backlinks.append(backlink)
        
        # Sort by source path
        all_backlinks.sort(key=lambda x: str(x['source']))
        return all_backlinks
    
    def get_unlinked_mentions(self, search_term: str, file_path: Optional[Path] = None) -> list[dict]:
        """
        Find mentions of a term that are not explicit links.
        
        This searches the raw text content for the term, excluding
        any matches that are part of [[wikilinks]].
        
        Args:
            search_term: Term to search for (case-insensitive)
            file_path: Optional - search only in this file, otherwise all files
        
        Returns:
            List of dicts with keys:
                - source: Path to the file
                - context: Text surrounding the mention
                - match: The matched text
        """
        search_lower = search_term.lower()
        mentions = []
        
        files_to_search = [file_path] if file_path else list(self.vault_path.rglob('*.md'))
        
        for md_file in files_to_search:
            if not md_file.exists():
                continue
            
            try:
                content = md_file.read_text(encoding='utf-8')
            except (UnicodeDecodeError, OSError):
                continue
            
            # Remove all wikilinks from a copy for searching
            content_without_links = re.sub(r'\[\[[^\]]+\]\]', '', content)
            
            # Find all mentions of search_term (case-insensitive)
            pattern = re.compile(re.escape(search_term), re.IGNORECASE)
            
            for match in pattern.finditer(content_without_links):
                # Calculate position in original content
                # Since we removed links, positions may differ - use context instead
                start = match.start()
                end = match.end()
                
                # Get context from original content
                ctx_start = max(0, start - self._context_chars)
                ctx_end = min(len(content), end + self._context_chars)
                context = content[ctx_start:ctx_end]
                
                # Normalize whitespace
                context = re.sub(r'\s+', ' ', context).strip()
                
                mentions.append({
                    'source': md_file,
                    'context': context,
                    'match': match.group()
                })
        
        return mentions
    
    def get_link_graph(self) -> dict[str, list[str]]:
        """
        Get the complete link graph as adjacency list.
        
        Returns:
            Dict mapping each note to list of notes it links TO
        """
        graph = {}
        
        for source_key, backlinks in self._backlink_index.items():
            for backlink in backlinks:
                source = backlink['source']
                target = backlink['link_text']
                if source not in graph:
                    graph[source] = []
                if target not in graph[source]:
                    graph[source].append(target)
        
        return graph
    
    def get_stats(self) -> dict:
        """
        Get statistics about the indexed vault.
        
        Returns:
            Dict with stats: total_files, total_links, total_backlinks, etc.
        """
        total_files = len(self._normalized_names)
        total_links = sum(len(links) for links in self._backlink_index.values())
        
        # Count backlinks (each entry in index is a backlink)
        total_backlinks = sum(len(links) for links in self._backlink_index.values())
        
        # Files with most backlinks
        most_linked = []
        for target, links in self._backlink_index.items():
            most_linked.append((target, len(links)))
        most_linked.sort(key=lambda x: -x[1])
        
        return {
            'total_files': total_files,
            'total_links': total_links,
            'total_backlinks': total_backlinks,
            'most_linked': most_linked[:10],
            'indexed_files': list(self._backlink_index.keys())
        }
    
    # =========================================================================
    # PRIVATE METHODS
    # =========================================================================
    
    def _build_name_cache(self, vault: Path) -> None:
        """Build cache of normalized file names for quick lookup."""
        self._normalized_names.clear()
        
        for md_file in vault.rglob('*.md'):
            self._ensure_in_name_cache(md_file)
    
    def _ensure_in_name_cache(self, file_path: Path) -> None:
        """Ensure file is in the name cache."""
        normalized = self._normalize_for_index(file_path)
        self._normalized_names[file_path] = normalized
    
    def _normalize_for_index(self, file_path: Path) -> str:
        """
        Normalize file path to index key.
        
        Key format: relative path from vault, always using forward slashes
        Examples:
            /vault/Notes/Test.md -> Notes/Test.md
            /vault/Test.md -> Test.md
        """
        try:
            relative = file_path.relative_to(self.vault_path)
            return str(relative).replace('\\', '/')
        except ValueError:
            # File is outside vault
            return file_path.name
    
    def _get_all_index_keys(self, file_path: Path) -> list[str]:
        """
        Get all possible index keys for a file path.
        
        This handles case variations and path formats.
        """
        keys = set()
        
        # Try relative path from vault
        try:
            relative = file_path.relative_to(self.vault_path)
            rel_str = str(relative).replace('\\', '/')
            keys.add(rel_str)
            keys.add(rel_str.lower())
        except ValueError:
            pass
        
        # Try just the filename
        keys.add(file_path.name)
        keys.add(file_path.name.lower())
        
        # Try with .md extension variations
        stem = file_path.stem
        keys.add(stem)
        keys.add(stem.lower())
        
        return list(keys)
    
    def _process_file(self, md_file: Path) -> None:
        """
        Process a single file, extracting links and updating backlink index.
        
        Args:
            md_file: Path to markdown file
        """
        if not md_file.exists() or md_file.suffix != '.md':
            return
        
        try:
            content = md_file.read_text(encoding='utf-8')
        except (UnicodeDecodeError, OSError):
            return
        
        # Extract all wikilinks from content
        wikilinks = extract_wikilinks(content)
        
        for link in wikilinks:
            target = link['target']
            link_text = link['alias'] if link['alias'] else target
            link_pos = link['start']
            
            # Resolve the link target to actual file path
            resolved = self.resolver.resolve_link(target)
            
            if resolved is None:
                continue
            
            # Only index links within the vault
            try:
                resolved.relative_to(self.vault_path)
            except ValueError:
                # Target is outside vault
                continue
            
            # Get context around the link
            context = extract_context(content, link_pos, self._context_chars)
            
            # Normalize target for index
            target_key = self._normalize_for_index(resolved)
            
            # Add to backlink index
            if target_key not in self._backlink_index:
                self._backlink_index[target_key] = []
            
            # Check for duplicate
            is_duplicate = any(
                b['source'] == md_file and b['link_text'] == link_text
                for b in self._backlink_index[target_key]
            )
            
            if not is_duplicate:
                self._backlink_index[target_key].append({
                    'source': md_file,
                    'context': context,
                    'link_text': link_text,
                    'link_target': target,
                    'heading': link.get('heading')
                })
    
    def _remove_backlinks_from(self, file_path: Path) -> None:
        """
        Remove all backlinks that originate FROM a file.
        
        When a file's content changes, we need to remove all the backlinks
        that this file creates (i.e., links FROM this file TO others).
        
        Args:
            file_path: The source file whose outgoing links should be removed
        """
        file_path = Path(file_path)
        
        for target_key, backlinks in list(self._backlink_index.items()):
            # Filter out backlinks that originate from our file
            remaining = [b for b in backlinks if b['source'] != file_path]
            
            if remaining:
                self._backlink_index[target_key] = remaining
            else:
                # Remove the key if no backlinks remain
                del self._backlink_index[target_key]


# =============================================================================
# STANDALONE FUNCTIONS
# =============================================================================

def index_vault(vault_path: Path | str) -> BacklinkIndexer:
    """
    Create and populate a BacklinkIndexer for a vault.
    
    Args:
        vault_path: Path to Obsidian vault
    
    Returns:
        Populated BacklinkIndexer instance
    """
    indexer = BacklinkIndexer(vault_path)
    indexer.index_vault()
    return indexer


def get_backlinks(file_path: Path, vault_path: Path | str) -> list[dict]:
    """
    Standalone function to get backlinks for a file.
    
    Args:
        file_path: Target file to get backlinks for
        vault_path: Path to Obsidian vault
    
    Returns:
        List of backlink dictionaries
    """
    indexer = BacklinkIndexer(vault_path)
    indexer.index_vault()
    return indexer.get_backlinks(file_path)

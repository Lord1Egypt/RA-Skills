"""
Obsidian Vault - High-Level API for Obsidian Vault Operations.

Combines parser, resolver, and indexer into a single unified interface
for working with Obsidian vaults.
"""

from pathlib import Path
from typing import Optional
import sys

from .parser import (
    parse_frontmatter,
    extract_wikilinks,
    extract_tags,
    extract_embeds,
    extract_context,
)
from .resolver import PathResolver
from .indexer import BacklinkIndexer
from .writer import VaultWriter


# =============================================================================
# OBSIDIAN VAULT
# =============================================================================

class ObsidianVault:
    """
    High-level API for Obsidian vault operations.
    
    Combines the functionality of parser, resolver, and indexer to provide
    a unified interface for working with Obsidian vaults.
    
    Features:
        - Parse markdown files (frontmatter, links, tags, embeds)
        - Resolve wiki links to actual file paths
        - Full-text search across the vault
        - Backlink discovery and querying
        - Graph data structure for visualization
    
    Example:
        >>> vault = ObsidianVault("/path/to/vault")
        >>> vault.search("machine learning")
        [{'file': PosixPath('Notes/AI.md'), 'context': '...', 'score': 0.85}]
        
        >>> vault.find_backlinks("Notes/AI.md")
        [{'source': Path('Notes/ML.md'), 'context': '...', 'link_text': 'AI'}]
        
        >>> graph = vault.get_graph()
        >>> # {'nodes': [...], 'edges': [...]}
    """
    
    def __init__(self, vault_path: str | Path):
        """
        Initialize vault with path.
        
        Args:
            vault_path: Root path of the Obsidian vault
        """
        self.vault_path = Path(vault_path)
        
        # Initialize components
        self.resolver = PathResolver(self.vault_path)
        self.indexer = BacklinkIndexer(self.vault_path)
        self.writer = VaultWriter(self.vault_path)
        
        # Index state
        self._is_indexed = False
        
        # Check if vault exists
        if not self.vault_path.exists():
            raise FileNotFoundError(f"Vault not found: {vault_path}")
    
    # =========================================================================
    # INDEXING
    # =========================================================================
    
    def index(self, force: bool = False) -> None:
        """
        Index the vault for fast querying.
        
        Builds the backlink index and file cache.
        Call this before using search() or find_backlinks() for better performance.
        
        Args:
            force: Rebuild index even if already indexed
        """
        if self._is_indexed and not force:
            return
        
        self.indexer.index_vault()
        self._is_indexed = True
    
    def index_file(self, file_path: Path | str) -> None:
        """
        Index a single file, updating backlinks.
        
        Args:
            file_path: Path to file to index
        """
        self.indexer.index_file(Path(file_path))
    
    # =========================================================================
    # SEARCH
    # =========================================================================
    
    def search(self, query: str, limit: int = 20) -> list[dict]:
        """
        Full-text search within the vault.
        
        Searches file names, content, and metadata.
        Results are sorted by relevance (simple word overlap scoring).
        
        Args:
            query: Search query string
            limit: Maximum number of results (default 20)
        
        Returns:
            List of dicts with keys:
                - file: Path to the matching file
                - context: Text context around the match
                - score: Relevance score (0-1)
                - match_type: 'name', 'content', or 'frontmatter'
        """
        query_lower = query.lower()
        query_words = set(query_lower.split())
        
        results = []
        
        # Get all markdown files
        for md_file in self.vault_path.rglob('*.md'):
            score = 0.0
            context = ""
            match_type = None
            
            # Check filename
            filename_lower = md_file.stem.lower()
            if query_lower in filename_lower:
                score = max(score, 0.8)
                match_type = 'name'
            
            # Check if query words appear in filename
            filename_words = set(filename_lower.replace('-', ' ').replace('_', ' ').split())
            word_overlap = query_words & filename_words
            if word_overlap:
                score = max(score, 0.6 + 0.1 * len(word_overlap))
                match_type = match_type or 'name'
            
            # Parse file for content and frontmatter search
            try:
                content = md_file.read_text(encoding='utf-8')
            except (UnicodeDecodeError, OSError):
                continue
            
            frontmatter_data = parse_frontmatter(content)
            body = frontmatter_data['body']
            metadata = frontmatter_data['metadata']
            
            # Check frontmatter
            metadata_text = ' '.join(str(v) for v in metadata.values())
            if query_lower in metadata_text.lower():
                score = max(score, 0.7)
                match_type = match_type or 'frontmatter'
            
            # Check content
            content_lower = body.lower()
            if query_lower in content_lower:
                # Find context position
                pos = content_lower.find(query_lower)
                context = extract_context(body, pos, 100)
                score = max(score, 0.5)
                match_type = match_type or 'content'
            
            # Check word overlap in content
            content_words = set(content_lower.split())
            content_overlap = query_words & content_words
            if content_overlap:
                score = max(score, 0.3 + 0.2 * len(content_overlap))
                if not match_type:
                    match_type = 'content'
            
            if score > 0:
                # Find best context
                if not context:
                    pos = content_lower.find(query_lower)
                    if pos >= 0:
                        context = extract_context(body, pos, 100)
                    else:
                        # Use beginning of content
                        context = extract_context(body, 0, 100)
                
                results.append({
                    'file': md_file,
                    'context': context,
                    'score': min(score, 1.0),
                    'match_type': match_type
                })
        
        # Sort by score descending
        results.sort(key=lambda x: -x['score'])
        
        return results[:limit]
    
    # =========================================================================
    # BACKLINKS
    # =========================================================================
    
    def find_backlinks(self, file_path: str | Path) -> list[dict]:
        """
        Get all files that link to this file.
        
        Args:
            file_path: Path to the target file (resolved relatively from vault)
        
        Returns:
            List of dicts with keys:
                - source: Path to the file containing the link
                - context: Text surrounding the link
                - link_text: Display text of the link (alias or target)
                - link_target: The raw target from [[target]]
        """
        # Ensure index is built
        if not self._is_indexed:
            self.index()
        
        target_path = Path(file_path)
        
        # Try to resolve to absolute path
        if not target_path.is_absolute():
            target_path = self.vault_path / target_path
        
        # Get backlinks
        backlinks = self.indexer.get_backlinks(target_path)
        
        return backlinks
    
    # =========================================================================
    # GRAPH
    # =========================================================================
    
    def get_graph(self) -> dict:
        """
        Get the full link graph of the vault.
        
        Returns:
            Dict with keys:
                - nodes: List of file nodes [{'path': Path, 'name': str, 'links': int}]
                - edges: List of links [{'source': Path, 'target': Path, 'target_name': str}]
        """
        # Ensure index is built
        if not self._is_indexed:
            self.index()
        
        # Get all markdown files as nodes
        nodes = []
        file_paths = set()
        
        for md_file in self.vault_path.rglob('*.md'):
            # Count outgoing links from this file
            try:
                content = md_file.read_text(encoding='utf-8')
                links = extract_wikilinks(content)
                out_links = len(links)
            except (UnicodeDecodeError, OSError):
                out_links = 0
            
            nodes.append({
                'path': md_file,
                'name': md_file.stem,
                'links': out_links
            })
            file_paths.add(md_file)
        
        # Get edges from backlink indexer
        edges = []
        backlink_graph = self.indexer.get_link_graph()
        
        for source, targets in backlink_graph.items():
            for target_name in targets:
                # Resolve target name to actual file path
                resolved = self.resolver.resolve_link(target_name)
                
                if resolved and resolved in file_paths:
                    edges.append({
                        'source': source,
                        'target': resolved,
                        'target_name': target_name
                    })
        
        return {'nodes': nodes, 'edges': edges}
    
    # =========================================================================
    # LINK RESOLUTION
    # =========================================================================
    
    def resolve_link(self, link: str) -> Path | None:
        """
        Resolve a wikilink to a file path.
        
        Args:
            link: Wiki link (e.g., "Note", "folder/Note", "Note#Heading")
        
        Returns:
            Resolved Path or None if not found
        """
        return self.resolver.resolve_link(link)
    
    def resolve_full_link(self, link: str) -> tuple[Path | None, str | None]:
        """
        Resolve a wiki link including heading to (file_path, heading_fragment).
        
        Args:
            link: Full wiki link (e.g., "Note#Heading" or "Note|Alias")
        
        Returns:
            Tuple of (resolved_file_path, heading_fragment or None)
        """
        return self.resolver.resolve_full_link(link)
    
    # =========================================================================
    # FILE PARSING
    # =========================================================================
    
    def parse_file(self, file_path: str | Path) -> dict:
        """
        Parse a markdown file and extract all structured data.
        
        Args:
            file_path: Path to the markdown file
        
        Returns:
            Dict with keys:
                - file_path: Absolute path to the file
                - frontmatter: Parsed YAML frontmatter (metadata dict)
                - body: Content after frontmatter
                - wikilinks: List of wikilinks [{'target', 'heading', 'alias', ...}]
                - tags: List of tags (without # prefix)
                - embeds: List of embedded file references
                - headings: List of headings found
        """
        file_path = Path(file_path)
        
        if not file_path.is_absolute():
            file_path = self.vault_path / file_path
        
        try:
            content = file_path.read_text(encoding='utf-8')
        except (UnicodeDecodeError, OSError):
            return {
                'file_path': file_path,
                'frontmatter': {},
                'body': '',
                'wikilinks': [],
                'tags': [],
                'embeds': [],
                'headings': [],
                'error': f'Could not read file'
            }
        
        # Parse frontmatter
        fm_data = parse_frontmatter(content)
        
        # Extract links, tags, embeds
        wikilinks = extract_wikilinks(fm_data['body'])
        tags = extract_tags(fm_data['body'])
        embeds = extract_embeds(fm_data['body'])
        
        # Extract headings
        headings = self._extract_headings(fm_data['body'])
        
        return {
            'file_path': file_path,
            'frontmatter': fm_data['metadata'],
            'body': fm_data['body'],
            'wikilinks': wikilinks,
            'tags': tags,
            'embeds': embeds,
            'headings': headings
        }
    
    def _extract_headings(self, content: str) -> list[dict]:
        """
        Extract all headings from markdown content.
        
        Args:
            content: Markdown body content
        
        Returns:
            List of dicts with 'level', 'text', and 'slug'
        """
        headings = []
        
        for line in content.split('\n'):
            line = line.strip()
            
            if line.startswith('#'):
                # Count heading level
                level = len(line) - len(line.lstrip('#'))
                text = line.lstrip('#').strip()
                
                # Create slug
                slug = text.lower().replace(' ', '-')
                slug = ''.join(c if c.isalnum() or c == '-' else '' for c in slug)
                slug = slug.strip('-')
                
                headings.append({
                    'level': level,
                    'text': text,
                    'slug': slug
                })
        
        return headings
    
    # =========================================================================
    # UTILITY
    # =========================================================================
    
    def get_file_info(self, file_path: str | Path) -> dict:
        """
        Get information about a file in the vault.
        
        Args:
            file_path: Path to file
        
        Returns:
            Dict with file metadata and stats
        """
        file_path = Path(file_path)
        
        if not file_path.is_absolute():
            file_path = self.vault_path / file_path
        
        if not file_path.exists():
            return {'error': 'File not found'}
        
        try:
            content = file_path.read_text(encoding='utf-8')
        except (UnicodeDecodeError, OSError):
            return {'error': 'Could not read file'}
        
        fm_data = parse_frontmatter(content)
        wikilinks = extract_wikilinks(fm_data['body'])
        tags = extract_tags(fm_data['body'])
        embeds = extract_embeds(fm_data['body'])
        
        # Get backlinks
        backlinks = self.indexer.get_backlinks(file_path)
        
        return {
            'path': file_path,
            'name': file_path.stem,
            'size': file_path.stat().st_size,
            'modified': file_path.stat().st_mtime,
            'frontmatter': fm_data['metadata'],
            'outgoing_links': len(wikilinks),
            'incoming_links': len(backlinks),
            'tags': tags,
            'embeds': embeds
        }
    
    def get_stats(self) -> dict:
        """
        Get vault statistics.
        
        Returns:
            Dict with vault stats
        """
        # Ensure index is built
        if not self._is_indexed:
            self.index()
        
        indexer_stats = self.indexer.get_stats()
        
        # Count total files
        total_files = len(list(self.vault_path.rglob('*.md')))
        
        return {
            'vault_path': str(self.vault_path),
            'total_files': total_files,
            'total_links': indexer_stats.get('total_links', 0),
            'total_backlinks': indexer_stats.get('total_backlinks', 0),
            'indexed': self._is_indexed
        }
    
    def invalidate_cache(self) -> None:
        """
        Clear all caches and force rebuild on next access.
        """
        self._is_indexed = False
        self.resolver.invalidate_cache()
    
    # =========================================================================
    # WRITE OPERATIONS (Delegated to VaultWriter)
    # =========================================================================
    
    def create_note(
        self,
        relative_path: str,
        content: str = "",
        frontmatter: dict = None
    ) -> Path:
        """
        Create a new note in the vault.
        
        Args:
            relative_path: Path relative to vault (e.g., "Notes/Test.md")
            content: Body content
            frontmatter: Metadata dict
        
        Returns:
            Absolute Path to created file
        """
        return self.writer.create_note(relative_path, content, frontmatter)
    
    def update_frontmatter(
        self,
        relative_path: str,
        updates: dict,
        merge: bool = True
    ) -> None:
        """
        Update frontmatter of a note.
        
        Args:
            relative_path: Path to the note
            updates: Fields to update
            merge: Merge with existing (True) or replace (False)
        """
        self.writer.update_frontmatter(relative_path, updates, merge)
    
    def add_wikilink(
        self,
        source_path: str,
        target: str,
        context: str = ""
    ) -> None:
        """
        Add a wikilink to a file.
        
        Args:
            source_path: Path to the file to add link to
            target: Link target
            context: Optional surrounding text
        """
        self.writer.add_wikilink(source_path, target, context)
    
    def remove_wikilink(
        self,
        source_path: str,
        target: str
    ) -> None:
        """
        Remove a wikilink from a file.
        
        Args:
            source_path: Path to the file
            target: Link target to remove
        """
        self.writer.remove_wikilink(source_path, target)
    
    def replace_wikilink(
        self,
        old_target: str,
        new_target: str,
        scope: str | Path | None = None
    ) -> int:
        """
        Replace wikilink target across vault.
        
        Args:
            old_target: Current link target
            new_target: New link target
            scope: Optional file/directory to limit to
        
        Returns:
            Number of links replaced
        """
        return self.writer.replace_wikilink(old_target, new_target, scope)
    
    def move_note(
        self,
        old_path: str | Path,
        new_path: str | Path,
        update_links: bool = True
    ) -> None:
        """
        Move/rename a note.
        
        Args:
            old_path: Current path
            new_path: New path
            update_links: Update backlinks (default True)
        """
        self.writer.move_note(old_path, new_path, update_links)
    
    def delete_note(
        self,
        relative_path: str,
        backup: bool = True
    ) -> None:
        """
        Delete a note.
        
        Args:
            relative_path: Path to the note
            backup: Move to .trash instead of deleting
        """
        self.writer.delete_note(relative_path, backup)
    
    def get_broken_links(self) -> list[dict]:
        """
        Find all broken links in the vault.
        
        Returns:
            List of dicts with file, target, context
        """
        return self.writer.get_broken_links()


# =============================================================================
# STANDALONE FUNCTIONS
# =============================================================================

def open_vault(vault_path: str | Path) -> ObsidianVault:
    """
    Open an Obsidian vault.
    
    Args:
        vault_path: Path to the vault
    
    Returns:
        ObsidianVault instance
    
    Example:
        >>> vault = open_vault("/path/to/vault")
        >>> vault.index()
        >>> vault.search("topic")
    """
    return ObsidianVault(vault_path)

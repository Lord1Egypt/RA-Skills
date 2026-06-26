"""
Obsidian Path Resolver - Resolve wiki links to actual file paths.

Uses shortest-match algorithm: finds the shortest possible path
that matches a wiki link target.
"""

import re
from pathlib import Path
from typing import Optional


# =============================================================================
# PATH RESOLVER
# =============================================================================

class PathResolver:
    """
    Resolves wiki links to actual file paths using Obsidian's shortest-match.
    
    Rules:
        1. [[Note]] → Note.md or Note/index.md
        2. [[folder/Note]] → folder/Note.md
        3. Case-insensitive matching
        4. Returns shortest path if multiple matches
    """
    
    def __init__(self, vault_path: Path | str):
        """
        Initialize resolver with vault path.
        
        Args:
            vault_path: Root path of the Obsidian vault
        """
        self.vault_path = Path(vault_path)
        self._file_index: Optional[dict[str, list[Path]]] = None
    
    def _build_file_index(self) -> dict[str, list[Path]]:
        """
        Build case-insensitive file index for the vault.
        
        Returns:
            Dictionary mapping lowercase paths to list of actual paths
        """
        if self._file_index is not None:
            return self._file_index
        
        self._file_index = {}
        
        if not self.vault_path.exists():
            return self._file_index
        
        for file_path in self.vault_path.rglob('*.md'):
            # Store with lowercase key for case-insensitive lookup
            relative = file_path.relative_to(self.vault_path)
            key = str(relative).lower()
            
            if key not in self._file_index:
                self._file_index[key] = []
            self._file_index[key].append(file_path)
        
        return self._file_index
    
    def invalidate_cache(self):
        """Clear the file index cache to force rebuild on next use."""
        self._file_index = None
    
    def resolve_link(self, link: str, vault_path: Optional[Path] = None) -> Optional[Path]:
        """
        Resolve [[target]] to actual file path.
        
        Args:
            link: Wiki link target (e.g., "Note" or "folder/Note")
            vault_path: Override vault path (uses instance vault_path if None)
        
        Returns:
            Resolved Path or None if not found
        
        Algorithm:
            1. Normalize link (strip anchors/aliases)
            2. Build case-insensitive index
            3. Try exact match first (case-insensitive)
            4. Try folder match: link/index.md
            5. Search for files ending with link
            6. Return shortest match
        """
        vault = vault_path or self.vault_path
        index = self._build_file_index()
        
        # Normalize: remove heading and alias parts
        # [[target#heading|alias]] → "target"
        target = self._normalize_target(link)
        
        if not target:
            return None
        
        target_lower = target.lower()
        
        # Strategy 1: Exact match using index (case-insensitive)
        # Check for target.md
        exact_key = f"{target_lower}.md"
        if exact_key in index:
            matches = index[exact_key]
            if matches:
                return min(matches, key=lambda p: len(str(p)))
        
        # Strategy 2: Folder match using index (target/index.md)
        folder_key = f"{target_lower}/index.md"
        if folder_key in index:
            matches = index[folder_key]
            if matches:
                return min(matches, key=lambda p: len(str(p)))
        
        # Strategy 3: Search for shortest match (case-insensitive suffix)
        # Collect all matches ending with target
        matches: list[Path] = []
        
        for key, paths in index.items():
            # Check if key ends with the target (with .md suffix)
            if key == target_lower or key.endswith(f"/{target_lower}"):
                for p in paths:
                    if p not in matches:
                        matches.append(p)
        
        if not matches:
            return None
        
        # Return shortest path
        return min(matches, key=lambda p: len(str(p)))
    
    def resolve_heading(self, file_path: Path, heading: str) -> Optional[str]:
        """
        Find heading anchor in file and return as wiki link fragment.
        
        Args:
            file_path: Path to the markdown file
            heading: Heading text to find (e.g., "My Heading")
        
        Returns:
            Slugified heading fragment for linking or None if not found
        """
        if not file_path.exists():
            return None
        
        try:
            content = file_path.read_text(encoding='utf-8')
        except (UnicodeDecodeError, OSError):
            return None
        
        # Search for heading (case-insensitive)
        heading_lower = heading.lower()
        
        for line in content.split('\n'):
            line = line.strip()
            
            # Check for ATX-style heading (# Heading)
            if line.startswith('#'):
                # Extract heading text (remove # prefix and whitespace)
                heading_text = line.lstrip('#').strip()
                
                # Compare case-insensitively
                if heading_text.lower() == heading_lower:
                    return self._slugify(heading_text)
            
            # Check for setex-style heading (Underline with === or ---)
            # This is handled differently - we'd need context
        
        return None
    
    def resolve_embed(self, embed: str, vault_path: Optional[Path] = None) -> Optional[Path]:
        """
        Resolve ![[embed]] to actual file path.
        
        Args:
            embed: Embed target (e.g., "image.png" or "folder/image.png")
            vault_path: Override vault path
        
        Returns:
            Resolved Path or None if not found
        """
        vault = vault_path or self.vault_path
        
        # Embeds can reference any file type, not just .md
        # Try direct path first
        direct = vault / embed
        if direct.exists() and direct.is_file():
            return direct
        
        # Try with various extensions
        embed_name = Path(embed).name
        embed_folder = str(Path(embed).parent)
        
        # If embed is just a filename, search in vault
        if '/' not in embed and '\\' not in embed:
            index = self._build_file_index()
            
            # Case-insensitive search
            embed_lower = embed.lower()
            matches = []
            
            for key, paths in index.items():
                if key.endswith(f"/{embed_lower}") or key == embed_lower:
                    matches.extend(paths)
            
            if matches:
                return min(matches, key=lambda p: len(str(p)))
        
        # Try folder/filename.md pattern
        md_embed = f"{embed}.md"
        md_path = vault / md_embed
        if md_path.exists() and md_path.is_file():
            return md_path
        
        return None
    
    # =========================================================================
    # HELPER METHODS
    # =========================================================================
    
    def _normalize_target(self, link: str) -> str:
        """
        Normalize wiki link target by removing heading and alias parts.
        
        Args:
            link: Raw wiki link (e.g., "Note#Heading|Alias")
        
        Returns:
            Clean target (e.g., "Note")
        """
        # Remove heading (#...)
        if '#' in link:
            link = link.split('#')[0]
        
        # Remove alias (|...)
        if '|' in link:
            link = link.split('|')[0]
        
        return link.strip()
    
    def _slugify(self, text: str) -> str:
        """
        Convert heading text to slug format for wiki links.
        
        Args:
            text: Heading text
        
        Returns:
            Slugified text (lowercase, spaces to dashes)
        """
        # Convert to lowercase
        slug = text.lower()
        
        # Replace spaces with dashes
        slug = slug.replace(' ', '-')
        
        # Remove characters that aren't alphanumeric or dashes
        slug = re.sub(r'[^a-z0-9\-]', '', slug)
        
        # Remove multiple consecutive dashes
        slug = re.sub(r'-+', '-', slug)
        
        # Strip leading/trailing dashes
        slug = slug.strip('-')
        
        return slug
    
    def resolve_full_link(self, link: str, vault_path: Optional[Path] = None) -> tuple[Optional[Path], Optional[str]]:
        """
        Resolve wiki link including heading to (file_path, heading_fragment).
        
        Args:
            link: Full wiki link (e.g., "Note#Heading" or "Note|Alias")
            vault_path: Override vault path
        
        Returns:
            Tuple of (resolved_file_path, heading_fragment or None)
        """
        # Split link and heading/alias
        heading = None
        raw_target = link
        
        if '#' in link:
            raw_target, heading = link.split('#', 1)
            # Remove alias if present
            if '|' in heading:
                heading = heading.split('|')[0]
        
        # Resolve the target
        file_path = self.resolve_link(raw_target, vault_path)
        
        if file_path and heading:
            # Try to find the heading fragment
            fragment = self.resolve_heading(file_path, heading)
            return file_path, fragment
        
        return file_path, None


# =============================================================================
# STANDALONE FUNCTIONS
# =============================================================================

def resolve_wikilink(link: str, vault_path: Path | str) -> Optional[Path]:
    """
    Standalone function to resolve a wiki link.
    
    Args:
        link: Wiki link target
        vault_path: Path to Obsidian vault
    
    Returns:
        Resolved Path or None
    """
    resolver = PathResolver(vault_path)
    return resolver.resolve_link(link)

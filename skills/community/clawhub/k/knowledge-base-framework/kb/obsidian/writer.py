"""
Obsidian Writer - Write Operations for Obsidian Vault

Provides write operations for creating, updating, and managing
Obsidian markdown files including frontmatter and wikilinks.
"""

import re
import yaml
import shutil
from pathlib import Path
from datetime import datetime
from typing import Optional

from .parser import parse_frontmatter, extract_wikilinks, WIKILINK_PATTERN


# =============================================================================
# VAULT WRITER
# =============================================================================

class VaultWriter:
    """
    Handles all write operations on an Obsidian vault.
    
    Provides atomic file operations with frontmatter management
    and wikilink manipulation.
    """
    
    def __init__(self, vault_path: Path | str):
        """
        Initialize writer with vault path.
        
        Args:
            vault_path: Root path of the Obsidian vault
        """
        self.vault_path = Path(vault_path)
    
    # =========================================================================
    # CORE FILE OPERATIONS
    # =========================================================================
    
    def create_note(
        self,
        file_path: str | Path,
        content: str = "",
        frontmatter: dict = None
    ) -> Path:
        """
        Create a new .md file with optional frontmatter.
        
        Args:
            file_path: Relative path within vault (e.g., "Notes/Test.md")
            content: Body content (without frontmatter - handled separately)
            frontmatter: Metadata dict (will be serialized as YAML)
        
        Returns:
            Absolute Path to the created file
        
        Raises:
            FileExistsError: If file already exists
            ValueError: If frontmatter is not a dict
        """
        file_path = Path(file_path)
        
        # Resolve to absolute path
        if not file_path.is_absolute():
            abs_path = self.vault_path / file_path
        else:
            abs_path = file_path
        
        # Check if file already exists
        if abs_path.exists():
            raise FileExistsError(f"File already exists: {abs_path}")
        
        # Validate frontmatter
        if frontmatter is not None and not isinstance(frontmatter, dict):
            raise ValueError("frontmatter must be a dict or None")
        
        # Ensure parent directory exists
        abs_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Build file content
        file_content = self._build_file_content(frontmatter, content)
        
        # Write atomically (temp file + rename)
        self._atomic_write(abs_path, file_content)
        
        return abs_path
    
    def update_frontmatter(
        self,
        file_path: str | Path,
        updates: dict,
        merge: bool = True
    ) -> None:
        """
        Update frontmatter of an existing file.
        
        Args:
            file_path: Path to the markdown file
            updates: Dictionary with fields to update
            merge: If True, merge with existing frontmatter; if False, replace
        
        Raises:
            FileNotFoundError: If file doesn't exist
            ValueError: If updates is not a dict
        """
        file_path = Path(file_path)
        
        if not file_path.is_absolute():
            file_path = self.vault_path / file_path
        
        if not file_path.exists():
            raise FileNotFoundError(f"File not found: {file_path}")
        
        if not isinstance(updates, dict):
            raise ValueError("updates must be a dict")
        
        # Read current content
        content = file_path.read_text(encoding='utf-8')
        
        # Parse existing frontmatter
        fm_data = parse_frontmatter(content)
        existing_fm = fm_data['metadata']
        body = fm_data['body']
        
        # Merge or replace frontmatter
        if merge:
            new_fm = {**existing_fm, **updates}
        else:
            new_fm = updates
        
        # Build new content
        new_content = self._build_file_content(new_fm, body)
        
        # Write atomically
        self._atomic_write(file_path, new_content)
    
    def append_content(
        self,
        file_path: str | Path,
        content: str,
        position: str = "end"
    ) -> None:
        """
        Append content to an existing file.
        
        Args:
            file_path: Path to the markdown file
            content: Content to append
            position: "end" (default), "start", or "after:<heading>"
        
        Raises:
            FileNotFoundError: If file doesn't exist
        """
        file_path = Path(file_path)
        
        if not file_path.is_absolute():
            file_path = self.vault_path / file_path
        
        if not file_path.exists():
            raise FileNotFoundError(f"File not found: {file_path}")
        
        # Read current content
        current_content = file_path.read_text(encoding='utf-8')
        
        # Determine insertion point
        if position == "end":
            new_content = current_content.rstrip('\n') + '\n\n' + content
        elif position == "start":
            new_content = content + '\n\n' + current_content
        elif position.startswith("after:"):
            heading = position[6:]  # Remove "after:" prefix
            new_content = self._insert_after_heading(current_content, heading, content)
        else:
            raise ValueError(f"Invalid position: {position}")
        
        # Write atomically
        self._atomic_write(file_path, new_content)
    
    def delete_note(
        self,
        file_path: str | Path,
        backup: bool = True
    ) -> None:
        """
        Delete a note, optionally moving to trash.
        
        Args:
            file_path: Path to the markdown file
            backup: If True, move to .trash folder instead of deleting
        
        Raises:
            FileNotFoundError: If file doesn't exist
        """
        file_path = Path(file_path)
        
        if not file_path.is_absolute():
            file_path = self.vault_path / file_path
        
        if not file_path.exists():
            raise FileNotFoundError(f"File not found: {file_path}")
        
        if backup:
            # Move to .trash directory
            trash_dir = self.vault_path / '.trash'
            trash_dir.mkdir(exist_ok=True)
            
            # Generate unique trash filename
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            trash_name = f"{file_path.stem}_{timestamp}{file_path.suffix}"
            trash_path = trash_dir / trash_name
            
            shutil.move(str(file_path), str(trash_path))
        else:
            file_path.unlink()
    
    def move_note(
        self,
        old_path: str | Path,
        new_path: str | Path,
        update_links: bool = True
    ) -> None:
        """
        Move/rename a note, optionally updating all backlinks.
        
        Args:
            old_path: Current path of the note
            new_path: New path for the note
            update_links: If True, update all backlinks pointing to old_path
        
        Raises:
            FileNotFoundError: If old_path doesn't exist
            FileExistsError: If new_path already exists
        """
        old_path = Path(old_path)
        new_path = Path(new_path)
        
        if not old_path.is_absolute():
            old_path = self.vault_path / old_path
        
        if not new_path.is_absolute():
            new_path = self.vault_path / new_path
        
        if not old_path.exists():
            raise FileNotFoundError(f"File not found: {old_path}")
        
        if new_path.exists():
            raise FileExistsError(f"Target already exists: {new_path}")
        
        # Get old and new link targets (stem for [[link]] format)
        old_target = old_path.stem
        new_target = new_path.stem
        
        # Create parent directories
        new_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Move the file
        shutil.move(str(old_path), str(new_path))
        
        # Update backlinks if requested
        if update_links and old_target != new_target:
            self.replace_wikilink(old_target, new_target)
    
    # =========================================================================
    # WIKILINK OPERATIONS
    # =========================================================================
    
    def add_wikilink(
        self,
        source_file: str | Path,
        target: str,
        context: str = ""
    ) -> None:
        """
        Add a wikilink to a file.
        
        Args:
            source_file: Path to the file to add link to
            target: Link target (e.g., "Target Note")
            context: Optional surrounding text for the link
        
        Raises:
            FileNotFoundError: If source file doesn't exist
        """
        source_file = Path(source_file)
        
        if not source_file.is_absolute():
            source_file = self.vault_path / source_file
        
        if not source_file.exists():
            raise FileNotFoundError(f"File not found: {source_file}")
        
        # Read content
        content = source_file.read_text(encoding='utf-8')
        
        # Build wikilink
        if context:
            wikilink = f"{context} [[{target}]]"
        else:
            wikilink = f"[[{target}]]"
        
        # Check if link already exists (handle [[target|alias]] format)
        import re
        link_pattern = re.compile(r'\s*\|[|\s]\s*'.join(re.escape(target.split('|')[0] if '|' in target else target)))
        if link_pattern.search(content) or wikilink in content:
            return  # Link already present
        
        # Append to end of file
        new_content = content.rstrip('\n') + '\n\n' + wikilink
        
        self._atomic_write(source_file, new_content)
    
    def remove_wikilink(
        self,
        source_file: str | Path,
        target: str
    ) -> None:
        """
        Remove a wikilink from a file.
        
        Args:
            source_file: Path to the file to remove link from
            target: Link target to remove
        
        Raises:
            FileNotFoundError: If source file doesn't exist
        """
        source_file = Path(source_file)
        
        if not source_file.is_absolute():
            source_file = self.vault_path / source_file
        
        if not source_file.exists():
            raise FileNotFoundError(f"File not found: {source_file}")
        
        # Read content
        content = source_file.read_text(encoding='utf-8')
        
        # Pattern for the specific wikilink target
        # Matches [[target]], [[target|alias]], [[target#heading]], [[target#heading|alias]]
        pattern = rf'\[\[{re.escape(target)}(?:#[^\]|]+)?(?:\|[^\]]+)?\]\]'
        
        # Remove the link (and surrounding context if it's just the link)
        new_content = re.sub(pattern, '', content)
        
        # Clean up extra whitespace
        new_content = re.sub(r'\n{3,}', '\n\n', new_content)
        
        self._atomic_write(source_file, new_content)
    
    def replace_wikilink(
        self,
        old_target: str,
        new_target: str,
        scope: str | Path | None = None
    ) -> int:
        """
        Replace wikilink target across files.
        
        Args:
            old_target: Current link target
            new_target: New link target
            scope: Optional file or directory to limit replacement to
        
        Returns:
            Number of links replaced
        """
        # Determine search scope
        if scope is None:
            search_path = self.vault_path
        else:
            scope = Path(scope)
            if not scope.is_absolute():
                scope = self.vault_path / scope
            search_path = scope
        
        # Pattern for old_target wikilink
        # Matches [[old_target]], [[old_target|alias]], [[old_target#heading]], etc.
        pattern = rf'\[\[{re.escape(old_target)}(?:#([^\]|]+))?(?:\|([^\]]+))?\]\]'
        
        count = 0
        
        # Find all markdown files in scope
        if search_path.is_file():
            files_to_process = [search_path]
        else:
            files_to_process = list(search_path.rglob('*.md'))
        
        for file_path in files_to_process:
            try:
                content = file_path.read_text(encoding='utf-8')
            except (UnicodeDecodeError, OSError):
                continue
            
            # Find all matches
            matches = list(re.finditer(pattern, content))
            
            if not matches:
                continue
            
            # Replace each match
            new_content = content
            offset = 0
            
            for match in matches:
                start = match.start() + offset
                end = match.end() + offset
                
                # Reconstruct the link with new target
                heading = match.group(1)  # Optional heading
                alias = match.group(2)  # Optional alias
                
                if heading:
                    if alias:
                        replacement = f"[[{new_target}#{heading}|{alias}]]"
                    else:
                        replacement = f"[[{new_target}#{heading}]]"
                elif alias:
                    replacement = f"[[{new_target}|{alias}]]"
                else:
                    replacement = f"[[{new_target}]]"
                
                new_content = new_content[:start] + replacement + new_content[end:]
                offset += len(replacement) - (match.end() - match.start())
                count += 1
            
            # Write updated content
            self._atomic_write(file_path, new_content)
        
        return count
    
    def get_broken_links(self) -> list[dict]:
        """
        Find all broken (orphaned) links in the vault.
        
        Returns:
            List of dicts with keys: file, target, context
        """
        broken = []
        
        for md_file in self.vault_path.rglob('*.md'):
            try:
                content = md_file.read_text(encoding='utf-8')
            except (UnicodeDecodeError, OSError):
                continue
            
            # Extract all wikilinks
            links = extract_wikilinks(content)
            
            for link in links:
                target = link['target']
                
                # Try to resolve the link
                resolved = self._resolve_target(target)
                
                if resolved is None or not resolved.exists():
                    # Find the link in content for context
                    link_str = f"[[{target}"
                    if link['heading']:
                        link_str += f"#{link['heading']}"
                    if link['alias']:
                        link_str += f"|{link['alias']}"
                    link_str += "]]"
                    
                    pos = content.find(link_str)
                    ctx = content[max(0, pos-50):min(len(content), pos+len(link_str)+50)]
                    
                    broken.append({
                        'file': md_file,
                        'target': target,
                        'context': ctx.strip()
                    })
        
        return broken
    
    # =========================================================================
    # SYNC OPERATIONS (with KB - future integration)
    # =========================================================================
    
    def sync_to_vault(
        self,
        kb_entry_id: int,
        vault_path: str | None = None
    ) -> Path:
        """
        Sync a KB entry to the vault.
        
        Delegates to SyncManager for bidirectional sync support.
        
        Args:
            kb_entry_id: ID of the KB entry
            vault_path: Optional vault path override
        
        Returns:
            Path to the created/updated note
        """
        from .sync_manager import SyncManager
        from .conflict import ConflictResolution
        
        target_vault = Path(vault_path) if vault_path else self.vault_path
        sm = SyncManager(
            kb_path=self._get_kb_path(),
            vault_path=target_vault,
        )
        return sm.sync_to_vault(kb_entry_id)
    
    def sync_from_vault(
        self,
        vault_path: str | Path
    ) -> int:
        """
        Sync a vault note back to KB.
        
        Delegates to SyncManager for bidirectional sync support.
        
        Args:
            vault_path: Path to the vault note
        
        Returns:
            KB entry ID
        """
        from .sync_manager import SyncManager
        
        sm = SyncManager(
            kb_path=self._get_kb_path(),
            vault_path=self.vault_path,
        )
        return sm.sync_from_vault(Path(vault_path))
    
    def _get_kb_path(self) -> Path:
        """Resolve the KB database path."""
        try:
            from kb.base.config import KBConfig
            return Path(KBConfig.get_instance().db_path)
        except (ImportError, Exception):
            # Fallback: look for biblio.db near the vault
            return self.vault_path.parent / "biblio.db"
    
    # =========================================================================
    # INTERNAL HELPERS
    # =========================================================================
    
    def _serialize_frontmatter(self, frontmatter: dict) -> str:
        """
        Serialize frontmatter dict to YAML string.
        
        Args:
            frontmatter: Metadata dictionary
        
        Returns:
            YAML-formatted string with --- markers
        """
        if not frontmatter:
            return "---\n---\n"
        
        # Use yaml.safe_dump for clean YAML output
        yaml_str = yaml.safe_dump(frontmatter, default_flow_style=False, sort_keys=False)
        
        return f"---\n{yaml_str}---\n"
    
    def _build_file_content(
        self,
        frontmatter: dict | None,
        body: str
    ) -> str:
        """
        Build complete file content from frontmatter and body.
        
        Args:
            frontmatter: Metadata dict or None
            body: Body content
        
        Returns:
            Complete file content
        """
        if frontmatter is not None:
            fm_str = self._serialize_frontmatter(frontmatter)
            return fm_str + body
        else:
            return body
    
    def _ensure_directory(self, file_path: Path) -> None:
        """
        Ensure parent directory exists for a file.
        
        Args:
            file_path: Path to the file
        """
        file_path.parent.mkdir(parents=True, exist_ok=True)
    
    def _atomic_write(self, file_path: Path, content: str) -> None:
        """
        Write content atomically using temp file + rename.
        
        Args:
            file_path: Target file path
            content: Content to write
        """
        # Create temp file in same directory
        temp_fd = None
        temp_path = None
        
        try:
            # Use mkstemp for secure temp file
            temp_fd, temp_path = self._create_temp_file(file_path.parent)
            
            # Write content
            import os
            os.write(temp_fd, content.encode('utf-8'))
            os.fsync(temp_fd)  # Ensure data is on disk
            
            # Close temp file
            os.close(temp_fd)
            temp_fd = None
            
            # Atomic rename
            shutil.move(temp_path, file_path)
            
        except Exception:
            # Clean up temp file on error
            if temp_fd is not None:
                import os
                try:
                    os.close(temp_fd)
                except OSError:
                    pass
            if temp_path is not None:
                import os
                try:
                    os.unlink(temp_path)
                except OSError:
                    pass
            raise
    
    def _create_temp_file(self, directory: Path):
        """
        Create a temporary file in the given directory.
        
        Args:
            directory: Directory to create temp file in
        
        Returns:
            Tuple of (file_descriptor, temp_path)
        """
        import os
        import tempfile
        
        # Create temp file with .tmp suffix
        fd, path = tempfile.mkstemp(suffix='.tmp', dir=str(directory))
        return fd, Path(path)
    
    def _insert_after_heading(
        self,
        content: str,
        heading: str,
        insert_text: str
    ) -> str:
        """
        Insert text after a specific heading.
        
        Args:
            content: Full markdown content
            heading: Heading text to find
            insert_text: Text to insert after the heading
        
        Returns:
            Modified content
        """
        lines = content.split('\n')
        insert_idx = None
        
        for i, line in enumerate(lines):
            # Check for ATX-style heading (# Heading)
            if line.strip().startswith('#'):
                heading_text = line.lstrip('#').strip()
                if heading_text.lower() == heading.lower():
                    # Insert after this heading (skip empty lines after)
                    insert_idx = i + 1
                    while insert_idx < len(lines) and not lines[insert_idx].strip():
                        insert_idx += 1
                    break
        
        if insert_idx is None:
            # Heading not found, append to end
            return content + '\n\n' + insert_text
        
        # Insert the text
        lines.insert(insert_idx, insert_text)
        return '\n'.join(lines)
    
    def _resolve_target(self, target: str) -> Path | None:
        """
        Resolve a wikilink target to a file path.
        
        Args:
            target: Wiki link target (e.g., "Note" or "folder/Note")
        
        Returns:
            Resolved Path or None if not found
        """
        # Try direct .md extension
        direct = self.vault_path / f"{target}.md"
        if direct.exists():
            return direct
        
        # Try folder/index.md pattern
        folder = self.vault_path / target / "index.md"
        if folder.exists():
            return folder
        
        # Case-insensitive search
        target_lower = target.lower()
        for md_file in self.vault_path.rglob('*.md'):
            relative = md_file.relative_to(self.vault_path)
            if relative.stem.lower() == target_lower:
                return md_file
        
        return None


# =============================================================================
# STANDALONE FUNCTIONS
# =============================================================================

def create_note(
    vault_path: str | Path,
    relative_path: str,
    content: str = "",
    frontmatter: dict = None
) -> Path:
    """
    Create a new note in the vault.
    
    Args:
        vault_path: Path to the vault
        relative_path: Relative path for the new note
        content: Body content
        frontmatter: Metadata dict
    
    Returns:
        Absolute Path to the created file
    """
    writer = VaultWriter(vault_path)
    return writer.create_note(relative_path, content, frontmatter)


def update_frontmatter(
    vault_path: str | Path,
    relative_path: str,
    updates: dict,
    merge: bool = True
) -> None:
    """
    Update frontmatter of a note.
    
    Args:
        vault_path: Path to the vault
        relative_path: Relative path to the note
        updates: Fields to update
        merge: Whether to merge with existing frontmatter
    """
    writer = VaultWriter(vault_path)
    writer.update_frontmatter(relative_path, updates, merge)

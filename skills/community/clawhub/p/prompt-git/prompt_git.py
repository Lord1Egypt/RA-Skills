#!/usr/bin/env python3
"""
PromptGit - Local Prompt Version Control
Main version control engine for prompts.

Author: Shadow Rose
License: MIT
"""

import json
import os
import hashlib
from datetime import datetime
from typing import List, Dict, Optional, Tuple
from dataclasses import dataclass, asdict
import difflib


@dataclass
class PromptVersion:
    """A single prompt version."""
    id: str  # SHA256 hash of content
    content: str
    timestamp: str  # ISO format
    note: str
    tags: List[str]
    category: str
    parent_id: Optional[str] = None


@dataclass
class PromptMetadata:
    """Metadata for a prompt line."""
    name: str
    category: str
    current_version: str
    created: str
    modified: str
    version_count: int
    tags: List[str]


class PromptRepository:
    """
    Local prompt version control repository.
    
    Storage structure:
    {storage_dir}/
        index.json          # Prompt metadata index
        prompts/
            {name}/
                versions.json   # Version history
                {version_id}.txt  # Version content
    """
    
    def __init__(self, storage_dir: str = None):
        """
        Initialize repository.
        
        Args:
            storage_dir: Directory for storing prompts (default: ~/.promptgit)
        """
        if storage_dir is None:
            storage_dir = os.path.join(os.path.expanduser('~'), '.promptgit')
        
        self.storage_dir = os.path.abspath(storage_dir)
        self.index_path = os.path.join(self.storage_dir, 'index.json')
        self.prompts_dir = os.path.join(self.storage_dir, 'prompts')
        
        self._ensure_storage()
    
    def _ensure_storage(self):
        """Ensure storage directories exist."""
        os.makedirs(self.storage_dir, exist_ok=True)
        os.makedirs(self.prompts_dir, exist_ok=True)
        
        if not os.path.exists(self.index_path):
            self._save_index({})
    
    def _load_index(self) -> Dict[str, Dict]:
        """Load the prompt index."""
        try:
            with open(self.index_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except (json.JSONDecodeError, FileNotFoundError):
            return {}
    
    def _save_index(self, index: Dict[str, Dict]):
        """Save the prompt index."""
        with open(self.index_path, 'w', encoding='utf-8') as f:
            json.dump(index, f, indent=2)
    
    def _sanitize_name(self, name: str) -> str:
        """
        Sanitize a prompt name to prevent path traversal.
        
        Raises ValueError if name contains illegal characters or patterns.
        Returns the sanitized name unchanged if safe.
        """
        if not name or not name.strip():
            raise ValueError("Prompt name cannot be empty.")
        # Reject path separators and traversal sequences
        illegal = ['..', '/', '\\', '\x00']
        for pattern in illegal:
            if pattern in name:
                raise ValueError(
                    f"Prompt name contains illegal character or sequence: {repr(pattern)}. "
                    f"Names must not contain '..', '/', '\\', or null bytes."
                )
        # Verify the resolved path stays inside prompts_dir (belt-and-suspenders)
        candidate = os.path.realpath(os.path.join(self.prompts_dir, name))
        if not candidate.startswith(os.path.realpath(self.prompts_dir) + os.sep):
            raise ValueError(
                f"Prompt name '{name}' resolves outside the repository directory."
            )
        return name

    def _get_prompt_dir(self, name: str) -> str:
        """Get directory path for a prompt (name is sanitized first)."""
        self._sanitize_name(name)
        return os.path.join(self.prompts_dir, name)
    
    def _get_versions_path(self, name: str) -> str:
        """Get versions.json path for a prompt."""
        return os.path.join(self._get_prompt_dir(name), 'versions.json')
    
    def _get_content_path(self, name: str, version_id: str) -> str:
        """Get content file path for a version."""
        return os.path.join(self._get_prompt_dir(name), f'{version_id}.txt')
    
    def _load_versions(self, name: str) -> List[PromptVersion]:
        """Load version history for a prompt."""
        versions_path = self._get_versions_path(name)
        
        if not os.path.exists(versions_path):
            return []
        
        try:
            with open(versions_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            return [PromptVersion(**v) for v in data]
        except (json.JSONDecodeError, FileNotFoundError):
            return []
    
    def _save_versions(self, name: str, versions: List[PromptVersion]):
        """Save version history for a prompt."""
        prompt_dir = self._get_prompt_dir(name)
        os.makedirs(prompt_dir, exist_ok=True)
        
        versions_path = self._get_versions_path(name)
        
        with open(versions_path, 'w', encoding='utf-8') as f:
            json.dump([asdict(v) for v in versions], f, indent=2)
    
    def _hash_content(self, content: str) -> str:
        """Generate SHA256 hash of content."""
        return hashlib.sha256(content.encode('utf-8')).hexdigest()[:16]
    
    def save(self, name: str, content: str, note: str = '', 
             category: str = 'general', tags: List[str] = None) -> str:
        """
        Save a new version of a prompt.
        
        Args:
            name: Prompt name
            content: Prompt content
            note: Version note/description
            category: Category (system, task, template, snippet)
            tags: List of tags
        
        Returns:
            Version ID
        """
        if tags is None:
            tags = []
        
        # Load existing versions
        versions = self._load_versions(name)
        
        # Generate version ID
        version_id = self._hash_content(content)
        timestamp = datetime.utcnow().isoformat()
        
        # Check if this exact content already exists
        if any(v.id == version_id for v in versions):
            raise ValueError(f"Version with identical content already exists: {version_id}")
        
        # Get parent (most recent version)
        parent_id = versions[-1].id if versions else None
        
        # Create new version
        version = PromptVersion(
            id=version_id,
            content=content,
            timestamp=timestamp,
            note=note,
            tags=tags,
            category=category,
            parent_id=parent_id
        )
        
        # Save content file
        content_path = self._get_content_path(name, version_id)
        with open(content_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        # Add version to history
        versions.append(version)
        self._save_versions(name, versions)
        
        # Update index
        index = self._load_index()
        
        if name not in index:
            # New prompt
            index[name] = {
                'name': name,
                'category': category,
                'current_version': version_id,
                'created': timestamp,
                'modified': timestamp,
                'version_count': 1,
                'tags': tags
            }
        else:
            # Update existing
            index[name]['current_version'] = version_id
            index[name]['modified'] = timestamp
            index[name]['version_count'] = len(versions)
            # Merge tags
            index[name]['tags'] = list(set(index[name]['tags'] + tags))
        
        self._save_index(index)
        
        return version_id
    
    def get_version(self, name: str, version_id: str = None) -> Optional[PromptVersion]:
        """
        Get a specific version of a prompt.
        
        Args:
            name: Prompt name
            version_id: Version ID (defaults to current)
        
        Returns:
            PromptVersion or None if not found
        """
        versions = self._load_versions(name)
        
        if not versions:
            return None
        
        if version_id is None:
            # Get current version
            index = self._load_index()
            if name not in index:
                return None
            version_id = index[name]['current_version']
        
        # Find version
        for v in versions:
            if v.id == version_id:
                # Load content
                content_path = self._get_content_path(name, v.id)
                try:
                    with open(content_path, 'r', encoding='utf-8') as f:
                        v.content = f.read()
                    return v
                except FileNotFoundError:
                    return None
        
        return None
    
    def list_prompts(self, category: str = None, tag: str = None) -> List[PromptMetadata]:
        """
        List all prompts, optionally filtered.
        
        Args:
            category: Filter by category
            tag: Filter by tag
        
        Returns:
            List of PromptMetadata
        """
        index = self._load_index()
        prompts = []
        
        for name, data in index.items():
            # Apply filters
            if category and data['category'] != category:
                continue
            if tag and tag not in data['tags']:
                continue
            
            prompts.append(PromptMetadata(**data))
        
        return prompts
    
    def list_versions(self, name: str) -> List[PromptVersion]:
        """
        List all versions of a prompt.
        
        Args:
            name: Prompt name
        
        Returns:
            List of PromptVersion (content not loaded)
        """
        return self._load_versions(name)
    
    def tag_version(self, name: str, version_id: str, tag: str):
        """
        Add a tag to a specific version.
        
        Args:
            name: Prompt name
            version_id: Version ID
            tag: Tag to add
        """
        versions = self._load_versions(name)
        
        for v in versions:
            if v.id == version_id:
                if tag not in v.tags:
                    v.tags.append(tag)
                break
        
        self._save_versions(name, versions)
    
    def rollback(self, name: str, version_id: str):
        """
        Rollback to a previous version (makes it current).
        
        Args:
            name: Prompt name
            version_id: Version ID to rollback to
        """
        # Verify version exists
        version = self.get_version(name, version_id)
        if not version:
            raise ValueError(f"Version not found: {version_id}")
        
        # Update index to make this the current version
        index = self._load_index()
        if name in index:
            index[name]['current_version'] = version_id
            index[name]['modified'] = datetime.utcnow().isoformat()
            self._save_index(index)
    
    def diff(self, name: str, version_a: str, version_b: str) -> str:
        """
        Generate diff between two versions.
        
        Args:
            name: Prompt name
            version_a: First version ID
            version_b: Second version ID
        
        Returns:
            Unified diff string
        """
        v_a = self.get_version(name, version_a)
        v_b = self.get_version(name, version_b)
        
        if not v_a or not v_b:
            raise ValueError("One or both versions not found")
        
        diff = difflib.unified_diff(
            v_a.content.splitlines(keepends=True),
            v_b.content.splitlines(keepends=True),
            fromfile=f'{name} ({version_a})',
            tofile=f'{name} ({version_b})',
            lineterm=''
        )
        
        return ''.join(diff)


def main():
    """CLI interface for PromptGit."""
    import argparse
    import sys
    
    parser = argparse.ArgumentParser(
        description='PromptGit - Local Prompt Version Control'
    )
    parser.add_argument(
        '--storage',
        help='Storage directory (default: ~/.promptgit)'
    )
    
    subparsers = parser.add_subparsers(dest='command', help='Commands')
    
    # Save command
    save_parser = subparsers.add_parser('save', help='Save a new version')
    save_parser.add_argument('name', help='Prompt name')
    save_parser.add_argument('--content', help='Content (or read from stdin)')
    save_parser.add_argument('--file', help='Read content from file')
    save_parser.add_argument('--note', default='', help='Version note')
    save_parser.add_argument('--category', default='general', help='Category')
    save_parser.add_argument('--tag', action='append', help='Add tag')
    
    # Get command
    get_parser = subparsers.add_parser('get', help='Get a version')
    get_parser.add_argument('name', help='Prompt name')
    get_parser.add_argument('--version', help='Version ID (default: current)')
    
    # List command
    list_parser = subparsers.add_parser('list', help='List prompts')
    list_parser.add_argument('--category', help='Filter by category')
    list_parser.add_argument('--tag', help='Filter by tag')
    
    # Versions command
    versions_parser = subparsers.add_parser('versions', help='List versions')
    versions_parser.add_argument('name', help='Prompt name')
    
    # Diff command
    diff_parser = subparsers.add_parser('diff', help='Show diff between versions')
    diff_parser.add_argument('name', help='Prompt name')
    diff_parser.add_argument('version_a', help='First version ID')
    diff_parser.add_argument('version_b', help='Second version ID')
    
    # Rollback command
    rollback_parser = subparsers.add_parser('rollback', help='Rollback to version')
    rollback_parser.add_argument('name', help='Prompt name')
    rollback_parser.add_argument('version', help='Version ID')
    
    # Tag command
    tag_parser = subparsers.add_parser('tag', help='Tag a version')
    tag_parser.add_argument('name', help='Prompt name')
    tag_parser.add_argument('version', help='Version ID')
    tag_parser.add_argument('tag', help='Tag to add')
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        sys.exit(1)
    
    # Initialize repository
    repo = PromptRepository(storage_dir=args.storage)
    
    try:
        if args.command == 'save':
            # Get content
            if args.file:
                with open(args.file, 'r', encoding='utf-8') as f:
                    content = f.read()
            elif args.content:
                content = args.content
            else:
                content = sys.stdin.read()
            
            tags = args.tag if args.tag else []
            
            version_id = repo.save(
                args.name,
                content,
                note=args.note,
                category=args.category,
                tags=tags
            )
            
            print(f"✅ Saved version: {version_id}")
        
        elif args.command == 'get':
            version = repo.get_version(args.name, args.version)
            if version:
                print(version.content)
            else:
                print(f"Error: Prompt not found: {args.name}", file=sys.stderr)
                sys.exit(1)
        
        elif args.command == 'list':
            prompts = repo.list_prompts(category=args.category, tag=args.tag)
            
            if not prompts:
                print("No prompts found")
            else:
                for p in prompts:
                    tags_str = ', '.join(p.tags) if p.tags else 'none'
                    print(f"{p.name} [{p.category}] — {p.version_count} versions — tags: {tags_str}")
        
        elif args.command == 'versions':
            versions = repo.list_versions(args.name)
            
            if not versions:
                print(f"No versions found for: {args.name}")
            else:
                index = repo._load_index()
                current = index.get(args.name, {}).get('current_version')
                
                for v in reversed(versions):
                    marker = '→ ' if v.id == current else '  '
                    tags_str = ', '.join(v.tags) if v.tags else ''
                    print(f"{marker}{v.id} — {v.timestamp} — {v.note} [{tags_str}]")
        
        elif args.command == 'diff':
            diff_output = repo.diff(args.name, args.version_a, args.version_b)
            print(diff_output)
        
        elif args.command == 'rollback':
            repo.rollback(args.name, args.version)
            print(f"✅ Rolled back to version: {args.version}")
        
        elif args.command == 'tag':
            repo.tag_version(args.name, args.version, args.tag)
            print(f"✅ Tagged version {args.version} with: {args.tag}")
    
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    main()

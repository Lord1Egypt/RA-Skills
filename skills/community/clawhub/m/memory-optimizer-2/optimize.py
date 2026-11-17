#!/usr/bin/env python3
"""
Agent Memory Optimizer - Optimizer v1.0.0
Applies recommended fixes: deduplication, re-indexing, stale entry handling.
Author: Peru 🇵🇪
"""

import os
import sys
import re
import json
import shutil
import argparse
from datetime import datetime, timedelta
from pathlib import Path
from difflib import SequenceMatcher
from collections import defaultdict

VERSION = "1.0.0"
STALE_DAYS = 30
SIMILARITY_THRESHOLD = 0.80


class MemoryOptimizer:
    def __init__(self, workspace_path, dry_run=True, backup=False):
        self.workspace = Path(workspace_path)
        self.dry_run = dry_run
        self.backup = backup
        self.changes = []
        self.files_modified = 0
        self.bytes_saved = 0

    def _backup_file(self, filepath):
        """Create .bak backup of a file."""
        if self.backup:
            bak = f"{filepath}.bak"
            shutil.copy2(filepath, bak)
            self.changes.append(f"Created backup: {bak}")

    def _read_file(self, filepath):
        """Read file content."""
        with open(filepath, 'r', encoding='utf-8', errors='replace') as f:
            return f.read()

    def _write_file(self, filepath, content):
        """Write file content (respects dry_run)."""
        if self.dry_run:
            self.changes.append(f"[DRY RUN] Would modify: {filepath}")
        else:
            self._backup_file(filepath)
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            self.files_modified += 1
            self.changes.append(f"Modified: {filepath}")

    def dedup(self):
        """Remove duplicate entries from memory files."""
        print("🔄 Running deduplication...")
        
        # Collect all entries across files
        all_entries = {}  # file -> list of (line_num, text)
        for filepath in self._find_md_files():
            content = self._read_file(filepath)
            lines = content.split('\n')
            entries = []
            for i, line in enumerate(lines):
                match = re.match(r'^([\s]*[-*+]\s+)(.+)', line)
                if match:
                    prefix = match.group(1)
                    text = match.group(2).strip()
                    entries.append((i, prefix, text, line))
            all_entries[filepath] = entries
        
        # Find duplicates across and within files
        # Use hash-based exact matching first, then fuzzy on short-hash buckets
        exact_seen = {}  # normalized_text -> (file, line)
        total_removed = 0
        
        for filepath, entries in all_entries.items():
            content = self._read_file(filepath)
            lines = content.split('\n')
            lines_to_remove = set()
            
            for line_num, prefix, text, original_line in entries:
                normalized = re.sub(r'\s+', ' ', text.lower().strip())
                if len(normalized) < 15:
                    continue
                
                # Phase 1: exact match (fast)
                found_dup = False
                if normalized in exact_seen:
                    seen_file, seen_line = exact_seen[normalized]
                    if 'MEMORY.md' not in filepath and 'MEMORY.md' in seen_file:
                        lines_to_remove.add(line_num)
                        found_dup = True
                    elif 'MEMORY.md' in filepath and 'MEMORY.md' not in seen_file:
                        pass  # Keep MEMORY.md version
                    elif filepath > seen_file:
                        lines_to_remove.add(line_num)
                        found_dup = True
                
                # Phase 2: fuzzy match only on first 40 chars bucket (bounded)
                if not found_dup:
                    bucket_key = normalized[:40]
                    for seen_text, (seen_file, seen_line) in list(exact_seen.items()):
                        if not seen_text.startswith(bucket_key[:20]):
                            continue
                        if abs(len(normalized) - len(seen_text)) > max(len(normalized), len(seen_text)) * 0.3:
                            continue
                        ratio = SequenceMatcher(None, normalized, seen_text).ratio()
                        if ratio >= SIMILARITY_THRESHOLD:
                            if 'MEMORY.md' not in filepath and 'MEMORY.md' in seen_file:
                                lines_to_remove.add(line_num)
                                found_dup = True
                            elif filepath > seen_file:
                                lines_to_remove.add(line_num)
                                found_dup = True
                            break
                
                if not found_dup:
                    exact_seen[normalized] = (filepath, line_num)
            
            if lines_to_remove:
                original_size = len(content.encode('utf-8'))
                new_lines = [l for i, l in enumerate(lines) if i not in lines_to_remove]
                # Also remove blank lines left by removals
                new_content = re.sub(r'\n{3,}', '\n\n', '\n'.join(new_lines))
                new_size = len(new_content.encode('utf-8'))
                
                self.bytes_saved += original_size - new_size
                total_removed += len(lines_to_remove)
                
                self.changes.append(f"  Removed {len(lines_to_remove)} duplicates from {os.path.basename(filepath)}")
                self._write_file(filepath, new_content)
        
        if total_removed == 0:
            print("  ✅ No duplicates to remove")
        else:
            print(f"  {'Would remove' if self.dry_run else 'Removed'} {total_removed} duplicate entries")

    def reindex(self):
        """Add or update table of contents for large files."""
        print("📑 Running re-indexing...")
        
        for filepath in self._find_md_files():
            content = self._read_file(filepath)
            lines = content.split('\n')
            
            if len(lines) < 80:
                continue
            
            # Extract headings
            headings = []
            for i, line in enumerate(lines):
                match = re.match(r'^(#{1,6})\s+(.+)', line)
                if match:
                    level = len(match.group(1))
                    title = match.group(2).strip()
                    headings.append((level, title))
            
            if len(headings) < 4:
                continue
            
            # Check if TOC already exists
            if re.search(r'(## Table of Contents|## TOC|## Index)', content, re.I):
                self.changes.append(f"  {os.path.basename(filepath)}: TOC already exists")
                continue
            
            # Generate TOC
            toc_lines = ['## Table of Contents', '']
            for level, title in headings:
                if level == 1:
                    continue  # Skip h1
                indent = '  ' * (level - 2)
                anchor = re.sub(r'[^\w\s-]', '', title.lower()).replace(' ', '-')
                toc_lines.append(f'{indent}- [{title}](#{anchor})')
            toc_lines.append('')
            
            # Insert after first heading
            first_heading_line = None
            for i, line in enumerate(lines):
                if re.match(r'^#\s+', line):
                    first_heading_line = i
                    break
            
            if first_heading_line is not None:
                insert_at = first_heading_line + 1
                # Skip any blank lines after first heading
                while insert_at < len(lines) and not lines[insert_at].strip():
                    insert_at += 1
                
                new_lines = lines[:insert_at] + [''] + toc_lines + lines[insert_at:]
                new_content = '\n'.join(new_lines)
                
                self.changes.append(f"  Added TOC to {os.path.basename(filepath)} ({len(headings)} sections)")
                self._write_file(filepath, new_content)

    def clean_stale(self):
        """Archive or flag stale entries."""
        print("🕐 Cleaning stale entries...")
        
        now = datetime.now()
        cutoff = now - timedelta(days=STALE_DAYS)
        stale_found = 0
        
        for filepath in self._find_md_files():
            content = self._read_file(filepath)
            
            # Check daily files that are old and have "current/active" markers
            filename = os.path.basename(filepath)
            date_match = re.match(r'(\d{4}-\d{2}-\d{2})', filename)
            if date_match:
                try:
                    file_date = datetime.strptime(date_match.group(1), '%Y-%m-%d')
                    if file_date < cutoff:
                        # Add "[ARCHIVED]" prefix to active items
                        new_content = re.sub(
                            r'(?m)^([-*+]\s+)((?:current|active|ongoing|in progress|TODO)\b.*)$',
                            r'\1[ARCHIVED] \2',
                            content,
                            flags=re.IGNORECASE
                        )
                        if new_content != content:
                            stale_found += content.count('\n') - new_content.count('\n')  # rough
                            stale_found += len(re.findall(r'\[ARCHIVED\]', new_content)) - len(re.findall(r'\[ARCHIVED\]', content))
                            self._write_file(filepath, new_content)
                            self.changes.append(f"  Archived stale entries in {filename}")
                except:
                    pass
        
        if stale_found == 0:
            print("  ✅ No stale entries to clean")
        else:
            print(f"  {'Would archive' if self.dry_run else 'Archived'} {stale_found} stale entries")

    def fix_structure(self):
        """Fix structural issues in markdown files."""
        print("🏗️ Fixing structure issues...")
        
        fixes = 0
        for filepath in self._find_md_files():
            content = self._read_file(filepath)
            original = content
            
            # Fix multiple consecutive blank lines
            content = re.sub(r'\n{4,}', '\n\n\n', content)
            
            # Fix trailing whitespace
            content = re.sub(r'[ \t]+$', '', content, flags=re.MULTILINE)
            
            # Ensure file ends with newline
            if content and not content.endswith('\n'):
                content += '\n'
            
            # Fix heading spacing (ensure blank line before headings)
            content = re.sub(r'([^\n])\n(#{1,6}\s)', r'\1\n\n\2', content)
            
            if content != original:
                self.bytes_saved += len(original.encode('utf-8')) - len(content.encode('utf-8'))
                fixes += 1
                self._write_file(filepath, content)
        
        if fixes == 0:
            print("  ✅ No structure issues to fix")
        else:
            print(f"  {'Would fix' if self.dry_run else 'Fixed'} {fixes} files")

    def _find_md_files(self):
        """Find all markdown files in workspace."""
        files = []
        for name in ['MEMORY.md', 'TOOLS.md', 'AGENTS.md']:
            p = self.workspace / name
            if p.exists():
                files.append(str(p))
        
        memory_dir = self.workspace / 'memory'
        if memory_dir.exists():
            files.extend(str(f) for f in sorted(memory_dir.glob('*.md')))
        
        return files

    def run(self, only=None):
        """Run optimization."""
        print(f"🧠 Agent Memory Optimizer v{VERSION}")
        print(f"Workspace: {self.workspace}")
        print(f"Mode: {'DRY RUN' if self.dry_run else '⚡ APPLYING CHANGES'}")
        print(f"Backup: {'Yes' if self.backup else 'No'}")
        print()
        
        operations = {
            'dedup': self.dedup,
            'reindex': self.reindex,
            'stale': self.clean_stale,
            'structure': self.fix_structure
        }
        
        if only and only in operations:
            operations[only]()
        else:
            for op in operations.values():
                op()
                print()
        
        # Summary
        print('=' * 50)
        print('Summary:')
        print(f'  Files modified: {self.files_modified}')
        print(f'  Bytes saved: {self.bytes_saved}')
        print(f'  Changes:')
        for c in self.changes:
            print(f'    {c}')
        
        if self.dry_run:
            print(f'\nThis was a dry run. Use --apply to make changes.')


def main():
    parser = argparse.ArgumentParser(description=f'Agent Memory Optimizer v{VERSION}')
    parser.add_argument('--path', default='.', help='Workspace directory')
    parser.add_argument('--apply', action='store_true', help='Apply fixes (default: dry run)')
    parser.add_argument('--only', choices=['dedup', 'reindex', 'stale', 'structure'],
                       help='Only apply specific fix type')
    parser.add_argument('--backup', action='store_true', help='Create .bak files before modifying')
    
    args = parser.parse_args()
    
    workspace = Path(args.path).resolve()
    if not workspace.exists():
        print(f"Error: workspace not found: {workspace}", file=sys.stderr)
        sys.exit(1)
    
    optimizer = MemoryOptimizer(workspace, dry_run=not args.apply, backup=args.backup)
    optimizer.run(only=args.only)


if __name__ == '__main__':
    main()

#!/usr/bin/env python3
"""
Refactoring - Rename Engine

Safely renames symbols (functions, classes, variables) across a codebase.
Uses AST for accurate parsing and transformation.
"""

import ast
import shutil
from dataclasses import dataclass, field
from pathlib import Path
from typing import Dict, List, Optional, Set, Tuple, Any
import re
from datetime import datetime


@dataclass
class RenameOccurrence:
    """A single occurrence of a symbol to rename"""
    file: str
    line: int
    column: int
    old_name: str
    new_name: str
    context: str  # Function, Class, Variable, etc.
    original_line: str


@dataclass
class RenamePlan:
    """Plan for a rename operation"""
    old_name: str
    new_name: str
    symbol_type: Optional[str]  # function, class, variable
    occurrences: List[RenameOccurrence] = field(default_factory=list)

    @property
    def affected_files(self) -> Set[str]:
        return set(occ.file for occ in self.occurrences)

    @property
    def total_changes(self) -> int:
        return len(self.occurrences)


class PythonRenameEngine:
    """Python-specific rename engine using AST"""

    def __init__(self, root_path: str):
        self.root = Path(root_path).resolve()
        self.backup_dir = self.root / '.refactoring' / 'backup'

    def find_occurrences(self, old_name: str, symbol_type: Optional[str] = None) -> RenamePlan:
        """Find all occurrences of a symbol"""
        plan = RenamePlan(
            old_name=old_name,
            new_name="",
            symbol_type=symbol_type
        )

        # Find all Python files
        py_files = list(self.root.rglob('*.py'))

        for filepath in py_files:
            if not filepath.is_file():
                continue

            try:
                content = filepath.read_text(encoding='utf-8')
                occurrences = self._find_in_file(filepath, content, old_name, symbol_type)
                plan.occurrences.extend(occurrences)
            except Exception as e:
                print(f"Warning: Could not parse {filepath}: {e}")

        return plan

    def _find_in_file(self, filepath: Path, content: str, old_name: str,
                     symbol_type: Optional[str]) -> List[RenameOccurrence]:
        """Find occurrences in a single file"""
        occurrences = []
        lines = content.split('\n')

        try:
            tree = ast.parse(content)
        except SyntaxError:
            # Fallback to text search for files with syntax errors
            return self._text_search(filepath, content, old_name)

        # Walk the AST
        for node in ast.walk(tree):
            # Function definitions
            if isinstance(node, ast.FunctionDef) and node.name == old_name:
                if symbol_type is None or symbol_type == 'function':
                    occ = RenameOccurrence(
                        file=str(filepath.relative_to(self.root)),
                        line=node.lineno,
                        column=node.col_offset,
                        old_name=old_name,
                        new_name="",
                        context='function',
                        original_line=lines[node.lineno - 1] if node.lineno <= len(lines) else ""
                    )
                    occurrences.append(occ)

            # Class definitions
            elif isinstance(node, ast.ClassDef) and node.name == old_name:
                if symbol_type is None or symbol_type == 'class':
                    occ = RenameOccurrence(
                        file=str(filepath.relative_to(self.root)),
                        line=node.lineno,
                        column=node.col_offset,
                        old_name=old_name,
                        new_name="",
                        context='class',
                        original_line=lines[node.lineno - 1] if node.lineno <= len(lines) else ""
                    )
                    occurrences.append(occ)

            # Variable assignments
            elif isinstance(node, ast.Name) and node.id == old_name:
                if symbol_type is None or symbol_type == 'variable':
                    occ = RenameOccurrence(
                        file=str(filepath.relative_to(self.root)),
                        line=node.lineno,
                        column=node.col_offset,
                        old_name=old_name,
                        new_name="",
                        context='variable',
                        original_line=lines[node.lineno - 1] if node.lineno <= len(lines) else ""
                    )
                    occurrences.append(occ)

            # Attribute access (method calls)
            elif isinstance(node, ast.Attribute) and node.attr == old_name:
                if symbol_type is None or symbol_type == 'method':
                    occ = RenameOccurrence(
                        file=str(filepath.relative_to(self.root)),
                        line=node.lineno,
                        column=node.col_offset,
                        old_name=old_name,
                        new_name="",
                        context='method',
                        original_line=lines[node.lineno - 1] if node.lineno <= len(lines) else ""
                    )
                    occurrences.append(occ)

        # Also do text search for strings, comments, etc.
        text_occurrences = self._text_search(filepath, content, old_name)

        # Merge AST and text results (avoid duplicates)
        existing_positions = {(occ.line, occ.column) for occ in occurrences}
        for occ in text_occurrences:
            if (occ.line, occ.column) not in existing_positions:
                occurrences.append(occ)

        return occurrences

    def _text_search(self, filepath: Path, content: str, old_name: str) -> List[RenameOccurrence]:
        """Fallback text-based search"""
        occurrences = []
        lines = content.split('\n')

        for i, line in enumerate(lines, 1):
            # Find all occurrences in this line
            for match in re.finditer(r'\b' + re.escape(old_name) + r'\b', line):
                occ = RenameOccurrence(
                    file=str(filepath.relative_to(self.root)),
                    line=i,
                    column=match.start(),
                    old_name=old_name,
                    new_name="",
                    context='text',
                    original_line=line
                )
                occurrences.append(occ)

        return occurrences

    def preview_rename(self, old_name: str, new_name: str,
                      symbol_type: Optional[str] = None) -> RenamePlan:
        """Preview a rename operation without executing"""
        plan = self.find_occurrences(old_name, symbol_type)
        plan.new_name = new_name

        # Update all occurrences with new name
        for occ in plan.occurrences:
            occ.new_name = new_name

        return plan

    def execute_rename(self, plan: RenamePlan, create_backup: bool = True) -> Dict[str, Any]:
        """Execute a rename plan"""
        if not plan.occurrences:
            return {'success': False, 'message': 'No occurrences found', 'changes': 0}

        # Create backup
        if create_backup:
            backup_id = datetime.now().strftime('%Y%m%d_%H%M%S')
            backup_path = self.backup_dir / backup_id
            backup_path.mkdir(parents=True, exist_ok=True)

        # Group occurrences by file
        by_file: Dict[str, List[RenameOccurrence]] = {}
        for occ in plan.occurrences:
            if occ.file not in by_file:
                by_file[occ.file] = []
            by_file[occ.file].append(occ)

        changes_made = 0
        files_modified = []

        for file_path_str, occurrences in by_file.items():
            file_path = self.root / file_path_str

            if not file_path.exists():
                continue

            # Create backup
            if create_backup:
                backup_file = backup_path / file_path_str
                backup_file.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(file_path, backup_file)

            # Read file
            content = file_path.read_text(encoding='utf-8')
            lines = content.split('\n')

            # Sort occurrences by line number (descending) to avoid offset issues
            sorted_occurrences = sorted(occurrences, key=lambda x: (x.line, x.column), reverse=True)

            # Apply changes
            for occ in sorted_occurrences:
                line_idx = occ.line - 1
                if 0 <= line_idx < len(lines):
                    line = lines[line_idx]
                    # Replace the old name with new name
                    # Use word boundaries to avoid partial matches
                    new_line = line[:occ.column] + occ.new_name + line[occ.column + len(occ.old_name):]
                    lines[line_idx] = new_line
                    changes_made += 1

            # Write file
            new_content = '\n'.join(lines)
            file_path.write_text(new_content, encoding='utf-8')
            files_modified.append(file_path_str)

        return {
            'success': True,
            'changes': changes_made,
            'files_modified': files_modified,
            'backup_id': backup_id if create_backup else None
        }

    def undo(self, backup_id: Optional[str] = None) -> Dict[str, Any]:
        """Undo a refactoring operation"""
        if backup_id is None:
            # Find most recent backup
            if not self.backup_dir.exists():
                return {'success': False, 'message': 'No backups found'}

            backups = sorted(self.backup_dir.iterdir(), key=lambda x: x.stat().st_mtime, reverse=True)
            if not backups:
                return {'success': False, 'message': 'No backups found'}

            backup_path = backups[0]
        else:
            backup_path = self.backup_dir / backup_id

        if not backup_path.exists():
            return {'success': False, 'message': f'Backup {backup_id} not found'}

        # Restore files from backup
        restored = 0
        for backup_file in backup_path.rglob('*'):
            if backup_file.is_file():
                rel_path = backup_file.relative_to(backup_path)
                target_path = self.root / rel_path
                target_path.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(backup_file, target_path)
                restored += 1

        return {
            'success': True,
            'message': f'Restored {restored} files from backup {backup_path.name}'
        }

    def list_backups(self) -> List[Dict[str, Any]]:
        """List available backups"""
        if not self.backup_dir.exists():
            return []

        backups = []
        for backup_path in sorted(self.backup_dir.iterdir(), key=lambda x: x.stat().st_mtime, reverse=True):
            if backup_path.is_dir():
                file_count = len(list(backup_path.rglob('*')))
                backups.append({
                    'id': backup_path.name,
                    'timestamp': datetime.fromtimestamp(backup_path.stat().st_mtime).isoformat(),
                    'files': file_count
                })

        return backups


def main():
    import argparse

    parser = argparse.ArgumentParser(description='Refactoring - Rename Engine')
    parser.add_argument('root', help='Project root directory')
    parser.add_argument('--old-name', '-o', required=True, help='Old symbol name')
    parser.add_argument('--new-name', '-n', required=True, help='New symbol name')
    parser.add_argument('--type', '-t', choices=['function', 'class', 'variable', 'method'],
                       help='Symbol type')
    parser.add_argument('--dry-run', '-d', action='store_true', help='Preview only')
    parser.add_argument('--no-backup', action='store_true', help='Skip backup creation')

    args = parser.parse_args()

    engine = PythonRenameEngine(args.root)
    plan = engine.preview_rename(args.old_name, args.new_name, args.type)

    print(f"\n🔍 Rename Plan: {args.old_name} → {args.new_name}")
    print(f"{'='*60}")
    print(f"Found {plan.total_changes} occurrence(s) in {len(plan.affected_files)} file(s)")
    print()

    # Group by file
    by_file: Dict[str, List[RenameOccurrence]] = {}
    for occ in plan.occurrences:
        if occ.file not in by_file:
            by_file[occ.file] = []
        by_file[occ.file].append(occ)

    for file_path, occurrences in by_file.items():
        print(f"📄 {file_path}")
        for occ in occurrences:
            print(f"   Line {occ.line}:{occ.column} ({occ.context})")
            print(f"   - {occ.original_line.strip()[:60]}")
        print()

    if args.dry_run:
        print("\n⏸️  Dry run mode - no changes made")
        print("   Remove --dry-run to execute")
    else:
        print("\n⚡ Executing rename...")
        result = engine.execute_rename(plan, create_backup=not args.no_backup)

        if result['success']:
            print(f"✅ Success! Made {result['changes']} change(s)")
            print(f"   Modified {len(result['files_modified'])} file(s)")
            if result.get('backup_id'):
                print(f"   Backup: {result['backup_id']}")
        else:
            print(f"❌ Error: {result['message']}")


if __name__ == '__main__':
    main()

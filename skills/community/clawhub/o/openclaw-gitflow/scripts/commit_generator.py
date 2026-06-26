#!/usr/bin/env python3
"""
Git Workflow - Commit Message Generator

Generates commit messages from staged changes.
"""

import subprocess
import re
from pathlib import Path
from typing import Dict, List, Optional, Tuple


class CommitGenerator:
    """Generates commit messages from git changes"""

    # Conventional commit types
    TYPES = {
        'feat': '✨',
        'fix': '🐛',
        'docs': '📚',
        'style': '💎',
        'refactor': '♻️',
        'test': '🧪',
        'chore': '🔧',
    }

    def __init__(self, root_path: str):
        self.root = Path(root_path).resolve()

    def generate(self, commit_type: Optional[str] = None) -> Dict[str, str]:
        """Generate commit message from staged changes"""
        # Get git diff of staged changes
        diff = self._get_staged_diff()
        if not diff:
            return {'error': 'No staged changes found'}

        # Parse changed files
        files = self._get_changed_files()

        # Determine commit type
        if not commit_type:
            commit_type = self._detect_type(files, diff)

        # Generate subject line
        subject = self._generate_subject(files, commit_type)

        # Generate body
        body = self._generate_body(files)

        # Generate full message
        emoji = self.TYPES.get(commit_type, '')
        full_message = f"{commit_type}: {subject}\n\n{body}"
        if emoji:
            full_message = f"{emoji} {full_message}"

        return {
            'type': commit_type,
            'subject': subject,
            'body': body,
            'full_message': full_message,
            'files': files,
        }

    def _get_staged_diff(self) -> str:
        """Get staged diff"""
        result = subprocess.run(
            ['git', 'diff', '--cached'],
            capture_output=True,
            text=True,
            cwd=self.root
        )
        return result.stdout

    def _get_changed_files(self) -> List[Dict[str, str]]:
        """Get list of changed files"""
        result = subprocess.run(
            ['git', 'diff', '--cached', '--name-status'],
            capture_output=True,
            text=True,
            cwd=self.root
        )

        files = []
        for line in result.stdout.strip().split('\n'):
            if not line:
                continue
            parts = line.split('\t')
            if len(parts) >= 2:
                status = parts[0]
                filepath = parts[1]
                files.append({
                    'path': filepath,
                    'status': self._interpret_status(status),
                })

        return files

    def _interpret_status(self, status: str) -> str:
        """Interpret git status code"""
        status_map = {
            'A': 'added',
            'M': 'modified',
            'D': 'deleted',
            'R': 'renamed',
            'C': 'copied',
        }
        return status_map.get(status[0], 'modified')

    def _detect_type(self, files: List[Dict[str, str]], diff: str) -> str:
        """Auto-detect commit type from changes"""
        file_paths = [f['path'] for f in files]

        # Check for test files
        if any('test' in p.lower() for p in file_paths):
            return 'test'

        # Check for documentation
        if any(p.endswith(('.md', '.rst', '.txt')) for p in file_paths):
            return 'docs'

        # Check for config/build files
        config_files = ['package.json', 'requirements.txt', 'Dockerfile', '.yml', '.yaml']
        if any(any(c in p for c in config_files) for p in file_paths):
            return 'chore'

        # Check if it's a fix (look for keywords in diff)
        fix_keywords = ['fix', 'bug', 'error', 'crash', 'broken']
        if any(kw in diff.lower() for kw in fix_keywords):
            return 'fix'

        # Default to feat
        return 'feat'

    def _generate_subject(self, files: List[Dict[str, str]], commit_type: str) -> str:
        """Generate subject line"""
        # Get primary scope (directory or file type)
        scopes = self._get_scopes(files)
        scope = scopes[0] if scopes else 'general'

        # Generate description based on changes
        descriptions = []

        for f in files:
            path = f['path']
            status = f['status']

            if status == 'added':
                descriptions.append(f"add {self._humanize_name(path)}")
            elif status == 'deleted':
                descriptions.append(f"remove {self._humanize_name(path)}")
            elif status == 'modified':
                descriptions.append(f"update {self._humanize_name(path)}")

        # Pick the most common action
        if descriptions:
            from collections import Counter
            action = Counter(descriptions).most_common(1)[0][0]
        else:
            action = "update code"

        return f"{action}"

    def _get_scopes(self, files: List[Dict[str, str]]) -> List[str]:
        """Extract scopes from file paths"""
        scopes = []
        for f in files:
            parts = f['path'].split('/')
            if len(parts) > 1:
                scopes.append(parts[0])

        # Return unique scopes
        return list(dict.fromkeys(scopes))  # Preserves order

    def _humanize_name(self, filepath: str) -> str:
        """Convert filepath to human-readable name"""
        # Remove extension
        name = Path(filepath).stem

        # Replace special characters
        name = name.replace('_', ' ').replace('-', ' ')

        # Convert camelCase to spaces
        name = re.sub(r'([a-z])([A-Z])', r'\1 \2', name)

        return name.lower()

    def _generate_body(self, files: List[Dict[str, str]]) -> str:
        """Generate commit body"""
        lines = []

        # List changed files
        if files:
            lines.append("Files changed:")
            for f in files:
                status_emoji = {
                    'added': '+',
                    'modified': '~',
                    'deleted': '-',
                }.get(f['status'], '~')
                lines.append(f"- {status_emoji} {f['path']}")
            lines.append("")

        return "\n".join(lines)


def main():
    import argparse

    parser = argparse.ArgumentParser(description='Commit Message Generator')
    parser.add_argument('--root', '-r', default='.', help='Project root')
    parser.add_argument('--type', '-t', choices=list(CommitGenerator.TYPES.keys()),
                       help='Commit type')

    args = parser.parse_args()

    generator = CommitGenerator(args.root)
    result = generator.generate(args.type)

    if 'error' in result:
        print(f"❌ {result['error']}")
        return

    print("\n📝 Suggested commit message:")
    print(f"{'='*60}")
    print(result['full_message'])
    print()
    print(f"Type: {result['type']}")
    print(f"Files: {len(result['files'])}")


if __name__ == '__main__':
    main()

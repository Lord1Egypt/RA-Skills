#!/usr/bin/env python3
"""
Project Anatomy Scanner
Generates a compact file index (.anatomy.md) for a project directory.
Inspired by OpenWolf's anatomy.md concept.

Usage:
    python3 anatomy_scan.py <project-path> [--output <path>] [--config <yaml>]
"""

import os
import sys
import argparse
import fnmatch
from pathlib import Path
from datetime import datetime

DEFAULT_EXCLUDES = [
    'node_modules', '.git', '__pycache__', '.venv', 'venv',
    '.wolf', '.anatomy.md', '*.pyc', '*.pyo', '.DS_Store',
    'dist', 'build', '.next', 'coverage', '.nyc_output',
    'target', 'vendor', '*.lock', 'package-lock.json',
]

DEFAULT_MAX_DEPTH = 5
DEFAULT_MAX_FILE_KB = 500
DEFAULT_DESC_CHARS = 120


def estimate_tokens(text: str) -> int:
    """Rough token estimate: ~4 chars per token for English, ~2 for CJK."""
    return max(1, len(text) // 4)


def estimate_file_tokens(filepath: Path) -> int:
    """Estimate tokens from file size."""
    try:
        size = filepath.stat().st_size
        return max(1, size // 4)
    except OSError:
        return 0


def extract_description(filepath: Path, max_chars: int = DEFAULT_DESC_CHARS) -> str:
    """Extract a one-line description from file content."""
    try:
        with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
            lines = []
            for i, line in enumerate(f):
                if i >= 30:  # only scan first 30 lines
                    break
                lines.append(line)
    except (OSError, UnicodeDecodeError):
        return ''

    text = ''.join(lines)
    desc = ''

    # Python docstring
    if filepath.suffix == '.py':
        for marker in ('"""', "'''"):
            idx = text.find(marker)
            if idx != -1:
                end = text.find(marker, idx + 3)
                if end != -1:
                    desc = text[idx+3:end].strip().split('\n')[0]
                    break

    # JS/TS first comment or export
    elif filepath.suffix in ('.js', '.ts', '.jsx', '.tsx', '.mjs'):
        for line in lines:
            stripped = line.strip()
            if stripped.startswith('//'):
                desc = stripped.lstrip('/ ').strip()
                break
            elif stripped.startswith('/**'):
                desc = stripped.lstrip('/* ').rstrip('* /').strip()
                break
            elif stripped.startswith('export'):
                desc = stripped[:max_chars]
                break

    # Markdown heading
    elif filepath.suffix in ('.md', '.mdx'):
        for line in lines:
            if line.startswith('#'):
                desc = line.lstrip('# ').strip()
                break

    # Shell script comment
    elif filepath.suffix in ('.sh', '.bash', '.zsh'):
        for line in lines:
            stripped = line.strip()
            if stripped.startswith('#') and not stripped.startswith('#!'):
                desc = stripped.lstrip('# ').strip()
                break

    # Generic: first non-empty line
    if not desc:
        for line in lines:
            stripped = line.strip()
            if stripped and not stripped.startswith('#!'):
                desc = stripped
                break

    return desc[:max_chars]


def should_exclude(path: str, excludes: list) -> bool:
    """Check if path matches any exclude pattern."""
    name = os.path.basename(path)
    for pattern in excludes:
        if fnmatch.fnmatch(name, pattern):
            return True
        if pattern in path.split(os.sep):
            return True
    return False


def is_binary(filepath: Path) -> bool:
    """Quick binary detection."""
    try:
        with open(filepath, 'rb') as f:
            chunk = f.read(1024)
            return b'\x00' in chunk
    except OSError:
        return True


def scan_directory(root: Path, excludes: list, max_depth: int, max_file_kb: int, desc_max: int) -> list:
    """Scan directory and collect file info."""
    entries = []
    root = root.resolve()

    for dirpath, dirnames, filenames in os.walk(root):
        # Calculate depth
        rel = os.path.relpath(dirpath, root)
        depth = 0 if rel == '.' else rel.count(os.sep) + 1
        if depth >= max_depth:
            dirnames.clear()
            continue

        # Filter excluded dirs in-place
        dirnames[:] = [d for d in dirnames if not should_exclude(d, excludes)]
        dirnames.sort()

        for fname in sorted(filenames):
            fpath = Path(dirpath) / fname
            if should_exclude(fname, excludes):
                continue

            # Skip large files
            try:
                size_kb = fpath.stat().st_size / 1024
                if size_kb > max_file_kb:
                    continue
            except OSError:
                continue

            # Skip binary
            if is_binary(fpath):
                continue

            rel_path = fpath.relative_to(root)
            tokens = estimate_file_tokens(fpath)
            desc = extract_description(fpath, desc_max)
            mtime = datetime.fromtimestamp(fpath.stat().st_mtime).strftime('%Y-%m-%d')

            entries.append({
                'path': str(rel_path),
                'tokens': tokens,
                'description': desc,
                'modified': mtime,
            })

    return entries


def generate_anatomy_md(entries: list, project_name: str, fmt: str = 'table') -> str:
    """Generate the anatomy markdown content.
    fmt: 'table' (default), 'compact' (list), 'summary' (by-directory)
    """
    total_tokens = sum(e['tokens'] for e in entries)
    header = [
        f'# Project Anatomy: {project_name}',
        '',
        f'> {len(entries)} files, ~{total_tokens:,} tokens total. (~4 chars/token estimate)',
        '',
    ]

    if fmt == 'compact':
        lines = header[:]
        for entry in entries:
            desc = f' — {entry["description"]}' if entry['description'] else ''
            lines.append(f'- `{entry["path"]}` (~{entry["tokens"]}t){desc}')
        lines.append('')

    elif fmt == 'summary':
        lines = header[:]
        # Group by top-level directory
        dirs = {}
        for entry in entries:
            parts = Path(entry['path']).parts
            top = parts[0] if len(parts) > 1 else '.'
            dirs.setdefault(top, []).append(entry)
        for dirname in sorted(dirs.keys()):
            dir_entries = dirs[dirname]
            dir_tokens = sum(e['tokens'] for e in dir_entries)
            lines.append(f'## {dirname}/ ({len(dir_entries)} files, ~{dir_tokens:,}t)')
            lines.append('')
            for entry in dir_entries:
                desc = f' — {entry["description"]}' if entry['description'] else ''
                lines.append(f'- `{Path(entry["path"]).name}` (~{entry["tokens"]}t){desc}')
            lines.append('')

    else:  # table
        lines = header[:]
        lines.append('| File | Tokens | Description | Modified |')
        lines.append('|------|--------|-------------|----------|')
        for entry in entries:
            desc = entry['description'].replace('|', '\\|')
            lines.append(
                f"| `{entry['path']}` | ~{entry['tokens']} | {desc} | {entry['modified']} |"
            )
        lines.append('')

    lines.append(f'**Total: {len(entries)} files, ~{total_tokens:,} estimated tokens**')
    lines.append('')
    return '\n'.join(lines)


def load_config(project_path: Path) -> dict:
    """Load .anatomy.yaml config if exists."""
    config_path = project_path / '.anatomy.yaml'
    config = {
        'exclude': DEFAULT_EXCLUDES,
        'max_depth': DEFAULT_MAX_DEPTH,
        'max_file_size_kb': DEFAULT_MAX_FILE_KB,
        'description_max_chars': DEFAULT_DESC_CHARS,
    }
    if config_path.exists():
        try:
            import yaml
            with open(config_path) as f:
                user_cfg = yaml.safe_load(f) or {}
            if 'exclude' in user_cfg:
                config['exclude'] = DEFAULT_EXCLUDES + user_cfg['exclude']
            for key in ('max_depth', 'max_file_size_kb', 'description_max_chars'):
                if key in user_cfg:
                    config[key] = user_cfg[key]
        except ImportError:
            pass  # yaml not available, use defaults
    return config


def load_previous_anatomy(output_path: Path) -> dict:
    """Load previous scan results for incremental update."""
    import json
    cache_path = output_path.with_suffix('.cache.json')
    if cache_path.exists():
        try:
            with open(cache_path) as f:
                return json.load(f)
        except (json.JSONDecodeError, OSError):
            pass
    return {}


def save_anatomy_cache(output_path: Path, entries: list):
    """Save scan cache for incremental updates."""
    import json
    cache_path = output_path.with_suffix('.cache.json')
    cache = {}
    for e in entries:
        cache[e['path']] = {
            'tokens': e['tokens'],
            'description': e['description'],
            'modified': e['modified'],
        }
    with open(cache_path, 'w') as f:
        json.dump(cache, f, ensure_ascii=False)


def main():
    parser = argparse.ArgumentParser(description='Generate project anatomy index')
    parser.add_argument('project_path', help='Path to project directory')
    parser.add_argument('--output', '-o', help='Output file path')
    parser.add_argument('--format', '-f', choices=['table', 'compact', 'summary'],
                        default='compact', help='Output format (default: compact)')
    parser.add_argument('--incremental', '-i', action='store_true',
                        help='Reuse cached descriptions for unchanged files')
    parser.add_argument('--max-depth', type=int, help='Max directory depth')
    parser.add_argument('--exclude', nargs='*', help='Additional exclude patterns')
    args = parser.parse_args()

    project_path = Path(args.project_path).resolve()
    if not project_path.is_dir():
        print(f"Error: {project_path} is not a directory", file=sys.stderr)
        sys.exit(1)

    config = load_config(project_path)
    if args.max_depth:
        config['max_depth'] = args.max_depth
    if args.exclude:
        config['exclude'] = config['exclude'] + args.exclude

    output_path = Path(args.output) if args.output else project_path / '.anatomy.md'

    # Incremental mode
    prev_cache = {}
    if args.incremental:
        prev_cache = load_previous_anatomy(output_path)
        if prev_cache:
            print(f"Incremental: {len(prev_cache)} cached entries")

    print(f"Scanning {project_path}...")
    entries = scan_directory(
        project_path,
        config['exclude'],
        config['max_depth'],
        config['max_file_size_kb'],
        config['description_max_chars'],
    )

    # Reuse cached descriptions for unchanged files
    if prev_cache:
        reused = 0
        for entry in entries:
            cached = prev_cache.get(entry['path'])
            if cached and cached['modified'] == entry['modified']:
                entry['description'] = cached['description']
                reused += 1
        print(f"Reused {reused}/{len(entries)} cached descriptions")

    project_name = project_path.name
    content = generate_anatomy_md(entries, project_name, fmt=args.format)

    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(content)

    save_anatomy_cache(output_path, entries)

    total_tokens = sum(e['tokens'] for e in entries)
    idx_tokens = estimate_tokens(content)
    pct = 100 * (total_tokens - idx_tokens) // max(1, total_tokens)
    print(f"Done! {len(entries)} files → {output_path}")
    print(f"Index: ~{idx_tokens}t | All files: ~{total_tokens:,}t | Savings: {pct}%")


if __name__ == '__main__':
    main()

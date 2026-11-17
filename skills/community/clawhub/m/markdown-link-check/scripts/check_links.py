#!/usr/bin/env python3
"""
Check markdown files for broken links.

Usage:
    python3 check_links.py <file-or-dir> [--timeout 10] [--verbose]

Outputs a report of broken links with their line numbers and reasons.
Exit code 0 = all links OK, 1 = broken links found.
"""

import argparse
import os
import re
import sys
import urllib.request
import urllib.error
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed

LINK_PATTERN = re.compile(r'\[([^\]]*)\]\(([^)]+)\)')
IMAGE_PATTERN = re.compile(r'!\[([^\]]*)\]\(([^)]+)\)')


def extract_links(content: str, base_dir: str):
    """Extract all links from markdown content, yield (url, line_num)."""
    lines = content.split('\n')
    for line_num, line in enumerate(lines, 1):
        # Skip image links (they're assets, not navigational)
        for match in LINK_PATTERN.finditer(line):
            url = match.group(2).strip()
            # Skip empty, anchor-only, or javascript: links
            if not url or url.startswith('#') or url.startswith('javascript:'):
                continue
            yield url, line_num


def check_remote_url(url: str, timeout: int) -> tuple[str, bool, str]:
    """Check if a remote URL is reachable."""
    try:
        req = urllib.request.Request(url, method='HEAD', headers={
            'User-Agent': 'Mozilla/5.0 (compatible; LinkChecker/1.0)'
        })
        urllib.request.urlopen(req, timeout=timeout)
        return url, True, 'OK'
    except urllib.error.HTTPError as e:
        return url, False, f'HTTP {e.code}'
    except urllib.error.URLError as e:
        return url, False, f'Connection failed: {e.reason}'
    except Exception as e:
        return url, False, str(e)


def check_local_link(url: str, base_dir: str) -> tuple[str, bool, str]:
    """Check if a local file link exists relative to base_dir."""
    # Strip anchor and query
    clean_url = url.split('#')[0].split('?')[0]
    if not clean_url:
        return url, True, 'OK (anchor)'

    target = Path(base_dir) / clean_url
    if target.exists():
        return url, True, 'OK'
    return url, False, f'File not found: {clean_url}'


def process_file(filepath: str, timeout: int, verbose: bool):
    """Process a single markdown file, return list of (url, line, status, reason)."""
    base_dir = str(Path(filepath).parent)
    results = []

    try:
        with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
    except Exception as e:
        return [(filepath, 0, False, f'Cannot read file: {e}')]

    for url, line_num in extract_links(content, base_dir):
        if url.startswith(('http://', 'https://')):
            results.append((url, line_num, *check_remote_url(url, timeout)))
        else:
            results.append((url, line_num, *check_local_link(url, base_dir)))

    return results


def main():
    parser = argparse.ArgumentParser(description='Check markdown links for broken URLs.')
    parser.add_argument('path', help='Markdown file or directory to scan')
    parser.add_argument('--timeout', type=int, default=10, help='HTTP timeout in seconds')
    parser.add_argument('--verbose', '-v', action='store_true', help='Show all links, not just broken ones')
    args = parser.parse_args()

    target = Path(args.path)
    md_files = []

    if target.is_file():
        md_files.append(str(target))
    elif target.is_dir():
        for root, dirs, files in os.walk(target):
            for fname in files:
                if fname.endswith('.md'):
                    md_files.append(os.path.join(root, fname))
    else:
        print(f"Error: {args.path} not found", file=sys.stderr)
        sys.exit(2)

    if not md_files:
        print("No markdown files found.")
        sys.exit(0)

    all_broken = []
    print(f"Checking {len(md_files)} markdown file(s)...\n")

    for filepath in sorted(md_files):
        results = process_file(filepath, args.timeout, args.verbose)
        broken = [r for r in results if not r[2]]

        if broken or args.verbose:
            print(f"📄 {filepath}")
            for url, line_num, ok, reason in broken:
                print(f"  ❌ Line {line_num}: {url}")
                print(f"     Reason: {reason}")
                all_broken.append((filepath, line_num, url, reason))
            if args.verbose and not broken:
                print(f"  ✅ All {len(results)} links OK")

    print(f"\n{'='*50}")
    if all_broken:
        print(f"❌ Found {len(all_broken)} broken link(s):")
        for fpath, ln, url, reason in all_broken:
            print(f"  - {fpath}:{ln} → {url} ({reason})")
        sys.exit(1)
    else:
        print("✅ All links verified successfully!")
        sys.exit(0)


if __name__ == '__main__':
    main()

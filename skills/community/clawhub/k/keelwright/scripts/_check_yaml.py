#!/usr/bin/env python3
# Copyright (c) 2026 ratingtesting — MIT-0 (see LICENSE). Free to use/modify/redistribute, no attribution required.
#!/usr/bin/env python3
# Copyright (c) 2026 ratingtesting — MIT-0 (see LICENSE). Free to use/modify/redistribute, no attribution required.
"""Validate the YAML frontmatter of a SKILL.md file.

Exists so the post-install check can run as a plain argument vector instead of
`python -c "<inline code>"` inside a shell. Inline -c strings had to be quote-escaped
through a shell, which made the install path part of a parsed command line — a command
injection vector. A real file takes the path as argv[1] and no shell is involved.

Usage:
    python _check_yaml.py <path-to-SKILL.md>

Exit codes: 0 = valid frontmatter, 1 = invalid/missing, 2 = usage error.
"""
import sys


def main() -> int:
    if len(sys.argv) != 2:
        print("Usage: _check_yaml.py <path-to-SKILL.md>")
        return 2

    path = sys.argv[1]
    try:
        import yaml
    except ImportError:
        print("SKIP: pyyaml not installed")
        return 0

    try:
        with open(path, encoding="utf-8") as fh:
            text = fh.read()
    except OSError as e:
        print(f"FAIL: cannot read {path}: {e}")
        return 1

    parts = text.split("---")
    if len(parts) < 2:
        print("FAIL: no YAML frontmatter delimited by ---")
        return 1

    try:
        data = yaml.safe_load(parts[1])
    except yaml.YAMLError as e:
        print(f"FAIL: invalid YAML: {str(e).splitlines()[0]}")
        return 1

    if not isinstance(data, dict) or "name" not in data:
        print("FAIL: frontmatter missing required 'name' field")
        return 1

    print(f"OK ({data.get('name')} v{data.get('version', '?')})")
    return 0


if __name__ == "__main__":
    sys.exit(main())

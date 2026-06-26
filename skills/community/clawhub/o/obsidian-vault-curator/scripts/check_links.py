#!/usr/bin/env python3
import argparse
import os
import re
from collections import defaultdict

# This script intentionally does not classify secrets or credentials.
# Any sensitive-content concern must be verified by the main agent against exact note text.

WIKILINK_RE = re.compile(r"\[\[([^\]|#]+)(?:#[^\]|]+)?(?:\|[^\]]+)?\]\]")


def iter_markdown_files(root: str):
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = [d for d in dirnames if d not in {".obsidian", ".git", ".trash", "node_modules"}]
        for filename in filenames:
            if filename.lower().endswith(".md"):
                yield os.path.join(dirpath, filename)


def main():
    parser = argparse.ArgumentParser(description="Check wikilinks in one vault slice.")
    parser.add_argument("target", help="Folder or note path to inspect")
    args = parser.parse_args()

    root = os.path.abspath(args.target)
    if not os.path.exists(root):
        raise SystemExit(f"Target not found: {root}")
    files = [root] if os.path.isfile(root) else sorted(iter_markdown_files(root))
    if not files:
        raise SystemExit(f"No markdown files found in target: {root}")
    known_titles = defaultdict(list)
    for path in files:
        title = os.path.splitext(os.path.basename(path))[0].lower()
        known_titles[title].append(path)

    unresolved = []
    ambiguous = []
    for path in files:
        with open(path, "r", encoding="utf-8") as handle:
            text = handle.read()
        for target in WIKILINK_RE.findall(text):
            matches = known_titles.get(target.strip().lower(), [])
            if not matches:
                unresolved.append((path, target))
            elif len(matches) > 1:
                ambiguous.append((path, target, matches))

    print(f"Scanned {len(files)} markdown files")
    print("Note: link resolution is limited to markdown files inside the provided slice")
    if unresolved:
        print("\nUnresolved wikilinks:")
        for path, target in unresolved:
            print(f"- {path} -> [[{target}]]")
    if ambiguous:
        print("\nAmbiguous wikilinks:")
        for path, target, matches in ambiguous:
            print(f"- {path} -> [[{target}]]")
            for match in matches:
                print(f"  - {match}")
    if not unresolved and not ambiguous:
        print("No unresolved or ambiguous wikilinks found in this slice")


if __name__ == "__main__":
    main()

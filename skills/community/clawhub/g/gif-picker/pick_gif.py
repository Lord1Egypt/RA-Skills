#!/usr/bin/env python3
"""
GIF Picker - Select a GIF from the local library by tag.

Usage:
    python3 pick_gif.py tag1 tag2 ...    # Best match by tags
    python3 pick_gif.py --list           # List all GIFs with tags
    python3 pick_gif.py --list-tags      # List all available tags
    python3 pick_gif.py --verify         # Verify all files exist
"""

import json, os, sys

INDEX_PATH = os.environ.get("GIF_LIBRARY_INDEX", 
    os.path.expanduser("~/.openclaw/workspace/gif-library/index.json"))
GIF_DIR = os.environ.get("GIF_LIBRARY_DIR", 
    os.path.expanduser("~/.openclaw/workspace/gif-library/gifs"))


def load_index():
    with open(INDEX_PATH) as f:
        return json.load(f)


def pick_by_tags(tags, index):
    """Find the best GIF match for given tags."""
    gifs = index["gifs"]
    best = None
    best_score = 0

    for name, info in gifs.items():
        score = sum(1 for t in tags if t in info["tags"])
        if score > best_score:
            best_score = score
            best = (name, info)

    if best is None or best_score == 0:
        # No tag match, return first
        name = next(iter(gifs))
        return name, gifs[name]

    return best


def verify_files(index):
    """Check all indexed GIFs exist and have content."""
    missing = []
    for name, info in index["gifs"].items():
        path = os.path.join(GIF_DIR, info["file"])
        if not os.path.exists(path):
            missing.append((name, info["file"], "MISSING"))
        elif os.path.getsize(path) < 100:
            missing.append((name, info["file"], "TOO SMALL"))
    return missing


def list_all(index):
    """Print all GIFs with tags."""
    for name, info in index["gifs"].items():
        tags_str = ", ".join(info["tags"])
        print(f"  {name:25s} | {info['file']:35s} | {tags_str}")


def list_tags(index):
    """Print all unique tags."""
    all_tags = set()
    for info in index["gifs"].values():
        all_tags.update(info["tags"])
    for t in sorted(all_tags):
        print(f"  {t}")


def print_media_line(name, info):
    """Print the MEDIA line for use in assistant output."""
    path = os.path.join(GIF_DIR, info["file"])
    abs_path = os.path.abspath(path)
    print(f"MEDIA:{abs_path}")
    print(f"// Selected: {name} — {info['description']}")


if __name__ == "__main__":
    args = sys.argv[1:]

    if not args or "--help" in args or "-h" in args:
        print("Usage:")
        print("  python3 pick_gif.py tag1 tag2 ...   → Match GIF by tags")
        print("  python3 pick_gif.py --list           → List all GIFs")
        print("  python3 pick_gif.py --list-tags      → List all tags")
        print("  python3 pick_gif.py --verify         → Verify files")
        sys.exit(0)

    index = load_index()

    if "--list" in args:
        list_all(index)
    elif "--list-tags" in args:
        list_tags(index)
    elif "--verify" in args:
        missing = verify_files(index)
        if missing:
            for name, fname, issue in missing:
                print(f"  ✗ {name} -> {fname}: {issue}")
            sys.exit(1)
        else:
            print(f"  ✓ All {len(index['gifs'])} GIFs verified")
    else:
        tags = [t.lower() for t in args if not t.startswith("--")]
        name, info = pick_by_tags(tags, index)
        print_media_line(name, info)

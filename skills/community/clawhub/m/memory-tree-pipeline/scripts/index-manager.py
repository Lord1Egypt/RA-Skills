#!/usr/bin/env python3
"""
Memory Tree Index Manager

CLI tool for managing the memory tree index and triggering sealing.

Usage:
    python3 index-manager.py status          — Show memory tree status
    python3 index-manager.py seal            — Run sealing worker on new files
    python3 index-manager.py reindex         — Rebuild index from scratch
    python3 index-manager.py verify          — Verify tree integrity
    python3 index-manager.py stats           — Detailed statistics
"""

import json
import os
import sys
from datetime import datetime, timezone
from pathlib import Path

# ── Configuration ──────────────────────────────────────────────────────────────

WORKSPACE = Path(os.environ.get("MEMORY_WORKSPACE", os.path.expanduser("~/.openclaw/workspace")))
MEMORY_ROOT = Path(os.environ.get("MEMORY_ROOT", str(WORKSPACE / "memory")))
SOURCE_DIR = MEMORY_ROOT / "source"
TOPIC_DIR = MEMORY_ROOT / "topic"
GLOBAL_DIR = MEMORY_ROOT / "global"
META_DIR = MEMORY_ROOT / "_meta"
INDEX_FILE = META_DIR / "index.json"
SEALING_LOG = META_DIR / "sealing-log.json"

TOKEN_RATIO = 4


def estimate_tokens(text: str) -> int:
    return max(1, len(text) // TOKEN_RATIO)


def load_json(path: Path, default=None):
    if not path.exists():
        return default if default is not None else {}
    try:
        with open(path) as f:
            return json.load(f)
    except (json.JSONDecodeError, OSError):
        return default if default is not None else {}


def save_json(path: Path, data):
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


def file_size_str(size_bytes: int) -> str:
    if size_bytes < 1024:
        return f"{size_bytes}B"
    elif size_bytes < 1024 * 1024:
        return f"{size_bytes / 1024:.1f}KB"
    else:
        return f"{size_bytes / (1024 * 1024):.1f}MB"


def cmd_status():
    """Show memory tree status."""
    index = load_json(INDEX_FILE, {})

    # Count files
    source_files = sorted(SOURCE_DIR.glob("*.md"))
    topic_files = sorted(TOPIC_DIR.glob("*.md"))
    global_files = sorted(GLOBAL_DIR.glob("*.md"))

    # Calculate sizes
    source_bytes = sum(f.stat().st_size for f in source_files)
    topic_bytes = sum(f.stat().st_size for f in topic_files)
    global_bytes = sum(f.stat().st_size for f in global_files)

    # Count unsealed
    sealed_files = {k: v for k, v in index.get("sources", {}).items() if v.get("sealed")}
    unsealed_count = len(source_files) - len(sealed_files)

    # Last seal time
    last_seal = index.get("last_seal", "Never")

    # Sealing log entries
    sealing_log = load_json(SEALING_LOG, [])
    recent_seals = sealing_log[-5:] if sealing_log else []

    print("=" * 60)
    print("Memory Tree Status")
    print("=" * 60)
    print()
    print(f"  Source files:  {len(source_files):>4}  ({file_size_str(source_bytes)})")
    print(f"  Topic files:   {len(topic_files):>4}  ({file_size_str(topic_bytes)})")
    print(f"  Global files:  {len(global_files):>4}  ({file_size_str(global_bytes)})")
    print()
    print(f"  Sealed:        {len(sealed_files):>4}")
    print(f"  Unsealed:      {unsealed_count:>4}")
    print(f"  Last seal:     {last_seal}")
    print()

    # Topic breakdown
    if index.get("topics"):
        print("  Topic Breakdown:")
        for topic, info in sorted(index["topics"].items()):
            tokens = info.get("tokens", 0)
            sources = len(info.get("sources", []))
            print(f"    {topic:<20} {sources:>3} sources  {tokens:>6} tokens")
        print()

    # Global breakdown
    if index.get("global"):
        print("  Global Knowledge:")
        for name, info in sorted(index["global"].items()):
            tokens = info.get("tokens", 0)
            topics = info.get("topics", [])
            print(f"    {name:<15} {tokens:>6} tokens  ← {', '.join(topics)}")
        print()

    # Recent sealing activity
    if recent_seals:
        print("  Recent Sealing Activity:")
        for entry in recent_seals:
            action = entry.get("action", "unknown")
            source = entry.get("source", "unknown")
            ts = entry.get("timestamp", "unknown")
            print(f"    {ts[:19]}  {action:<15} {source}")
        print()

    # Unsealed files
    if unsealed_count > 0:
        sealed_paths = set(index.get("sources", {}).keys())
        unsealed = [f for f in source_files if str(f.relative_to(MEMORY_ROOT)) not in sealed_paths]
        if unsealed:
            print(f"  ⚠️  {len(unsealed)} unsealed files:")
            for f in unsealed[:10]:
                print(f"    {f.name}")
            if len(unsealed) > 10:
                print(f"    ... and {len(unsealed) - 10} more")
            print()

    # Size warnings
    for gf in global_files:
        content = gf.read_text(encoding="utf-8", errors="replace")
        tokens = estimate_tokens(content)
        if tokens > 5000:
            print(f"  ⚠️  Global file {gf.name} exceeds 5000 tokens ({tokens})")

    return {
        "source_count": len(source_files),
        "topic_count": len(topic_files),
        "global_count": len(global_files),
        "sealed_count": len(sealed_files),
        "unsealed_count": unsealed_count,
    }


def cmd_seal():
    """Run sealing worker on new files."""
    # Import and run seal-worker
    sys.path.insert(0, str(Path(__file__).parent))
    from seal_worker import main as seal_main

    print("Running seal worker...")
    seal_main()


def cmd_reindex():
    """Rebuild the index from scratch by scanning all files."""
    print("Rebuilding index from scratch...")

    index = {
        "version": 1,
        "sources": {},
        "source_to_topic": {},
        "topics": {},
        "global": {},
        "last_seal": None,
        "reindexed_at": datetime.now(timezone.utc).isoformat(),
    }

    # Scan source files
    source_files = sorted(SOURCE_DIR.glob("*.md"))
    for f in source_files:
        rel = str(f.relative_to(MEMORY_ROOT))
        content = f.read_text(encoding="utf-8", errors="replace")
        index["sources"][rel] = {
            "sealed": False,
            "tokens": estimate_tokens(content),
            "size": f.stat().st_size,
            "reindexed": True,
        }
    print(f"  Indexed {len(source_files)} source files")

    # Scan topic files
    topic_files = sorted(TOPIC_DIR.glob("*.md"))
    for f in topic_files:
        topic_name = f.stem
        content = f.read_text(encoding="utf-8", errors="replace")
        index["topics"][topic_name] = {
            "file": str(f.relative_to(MEMORY_ROOT)),
            "tokens": estimate_tokens(content),
            "size": f.stat().st_size,
            "sources": [],
            "last_updated": datetime.now(timezone.utc).isoformat(),
        }
    print(f"  Indexed {len(topic_files)} topic files")

    # Scan global files
    global_files = sorted(GLOBAL_DIR.glob("*.md"))
    for f in global_files:
        name = f.stem
        content = f.read_text(encoding="utf-8", errors="replace")
        index["global"][name] = {
            "file": str(f.relative_to(MEMORY_ROOT)),
            "tokens": estimate_tokens(content),
            "size": f.stat().st_size,
            "last_updated": datetime.now(timezone.utc).isoformat(),
        }
    print(f"  Indexed {len(global_files)} global files")

    save_json(INDEX_FILE, index)
    print(f"\nIndex rebuilt: {INDEX_FILE}")
    print("Run `seal` command to generate topic summaries and update mappings.")


def cmd_verify():
    """Verify memory tree integrity."""
    index = load_json(INDEX_FILE, {})
    issues = []

    # Check directory structure
    for d in [SOURCE_DIR, TOPIC_DIR, GLOBAL_DIR, META_DIR]:
        if not d.exists():
            issues.append(f"Missing directory: {d.relative_to(WORKSPACE)}")

    # Check index file
    if not INDEX_FILE.exists():
        issues.append(f"Missing index file: {INDEX_FILE.relative_to(WORKSPACE)}")

    # Check source files referenced in index exist
    for rel, info in index.get("sources", {}).items():
        path = MEMORY_ROOT / rel
        if not path.exists():
            issues.append(f"Index references missing source: {rel}")

    # Check topic files referenced in index exist
    for topic, info in index.get("topics", {}).items():
        path = MEMORY_ROOT / info.get("file", "")
        if path and not path.exists():
            issues.append(f"Index references missing topic: {info['file']}")

    # Check global files referenced in index exist
    for name, info in index.get("global", {}).items():
        path = MEMORY_ROOT / info.get("file", "")
        if path and not path.exists():
            issues.append(f"Index references missing global: {info['file']}")

    # Check global file sizes
    for gf in GLOBAL_DIR.glob("*.md"):
        content = gf.read_text(encoding="utf-8", errors="replace")
        tokens = estimate_tokens(content)
        if tokens > 5000:
            issues.append(f"Global file exceeds 5000 tokens: {gf.name} ({tokens} tokens)")

    # Check topic file sizes
    for tf in TOPIC_DIR.glob("*.md"):
        content = tf.read_text(encoding="utf-8", errors="replace")
        tokens = estimate_tokens(content)
        if tokens > 2000:
            issues.append(f"Topic file exceeds 2000 tokens: {tf.name} ({tokens} tokens)")

    # Orphan check: source files not in index
    source_files = set(str(f.relative_to(MEMORY_ROOT)) for f in SOURCE_DIR.glob("*.md"))
    indexed_sources = set(index.get("sources", {}).keys())
    orphans = source_files - indexed_sources
    if orphans:
        issues.append(f"{len(orphans)} orphaned source files not in index")

    if issues:
        print("⚠️  Issues found:")
        for issue in issues:
            print(f"  - {issue}")
        return False
    else:
        print("✅ Memory tree integrity verified. No issues found.")
        return True


def cmd_stats():
    """Show detailed statistics."""
    index = load_json(INDEX_FILE, {})

    # Source stats
    source_files = sorted(SOURCE_DIR.glob("*.md"))
    source_tokens = []
    for f in source_files:
        content = f.read_text(encoding="utf-8", errors="replace")
        source_tokens.append(estimate_tokens(content))

    # Topic stats
    topic_files = sorted(TOPIC_DIR.glob("*.md"))
    topic_tokens = []
    for f in topic_files:
        content = f.read_text(encoding="utf-8", errors="replace")
        topic_tokens.append(estimate_tokens(content))

    # Global stats
    global_files = sorted(GLOBAL_DIR.glob("*.md"))
    global_tokens = []
    for f in global_files:
        content = f.read_text(encoding="utf-8", errors="replace")
        global_tokens.append(estimate_tokens(content))

    print("=" * 60)
    print("Memory Tree Statistics")
    print("=" * 60)
    print()

    print("Source Files:")
    if source_tokens:
        print(f"  Count:     {len(source_files)}")
        print(f"  Total tkns: {sum(source_tokens):,}")
        print(f"  Avg tkns:   {sum(source_tokens) // len(source_tokens):,}")
        print(f"  Min tkns:   {min(source_tokens):,}")
        print(f"  Max tkns:   {max(source_tokens):,}")
    else:
        print("  (none)")
    print()

    print("Topic Files:")
    if topic_tokens:
        print(f"  Count:     {len(topic_files)}")
        print(f"  Total tkns: {sum(topic_tokens):,}")
        print(f"  Avg tkns:   {sum(topic_tokens) // len(topic_tokens):,}")
        for tf, tkns in zip(topic_files, topic_tokens):
            print(f"    {tf.name:<25} {tkns:>6} tokens")
    else:
        print("  (none)")
    print()

    print("Global Knowledge:")
    if global_tokens:
        print(f"  Count:     {len(global_files)}")
        print(f"  Total tkns: {sum(global_tokens):,}")
        for gf, tkns in zip(global_files, global_tokens):
            status = "✅" if tkns <= 5000 else "⚠️ OVER"
            print(f"    {gf.name:<25} {tkns:>6} tokens  {status}")
    else:
        print("  (none)")
    print()

    print(f"Index version: {index.get('version', 'N/A')}")
    print(f"Last seal:     {index.get('last_seal', 'Never')}")
    print(f"Sealing log:   {len(load_json(SEALING_LOG, []))} entries")


# ── Main ────────────────────────────────────────────────────────────────────────

def main():
    if len(sys.argv) < 2:
        print("Usage: python3 index-manager.py <command>")
        print("Commands: status, seal, reindex, verify, stats")
        sys.exit(1)

    command = sys.argv[1].lower()

    if command == "status":
        cmd_status()
    elif command == "seal":
        cmd_seal()
    elif command == "reindex":
        cmd_reindex()
    elif command == "verify":
        cmd_verify()
    elif command == "stats":
        cmd_stats()
    else:
        print(f"Unknown command: {command}")
        print("Commands: status, seal, reindex, verify, stats")
        sys.exit(1)


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""
Memory Tree Tools

Python module providing structured access to the memory tree.
Can be imported as a module or run as CLI.

Module usage:
    from tools import MemoryTree
    mt = MemoryTree()
    mt.recall("security")
    mt.store("New information", source_type="conversation", topic_hint="security")
    mt.seal()
    mt.status()

CLI usage:
    python3 tools.py recall <query> [scope]
    python3 tools.py store <content> [topic_hint]
    python3 tools.py forget <topic> [--keep-source]
    python3 tools.py seal
    python3 tools.py status
"""

import json
import os
import re
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


class MemoryTree:
    """Structured access to the three-scope memory tree."""

    def __init__(self, root=None):
        self.root = Path(root) if root else MEMORY_ROOT
        self.source_dir = self.root / "source"
        self.topic_dir = self.root / "topic"
        self.global_dir = self.root / "global"
        self.meta_dir = self.root / "_meta"
        self.index_file = self.meta_dir / "index.json"

        # Ensure dirs exist
        for d in [self.source_dir, self.topic_dir, self.global_dir, self.meta_dir]:
            d.mkdir(parents=True, exist_ok=True)

    @property
    def index(self) -> dict:
        return load_json(self.index_file, {
            "version": 1,
            "sources": {},
            "source_to_topic": {},
            "topics": {},
            "global": {},
            "last_seal": None,
        })

    def _save_index(self, index: dict):
        save_json(self.index_file, index)

    # ── Recall ────────────────────────────────────────────────────────────────

    def recall(self, query: str, scope: str = "all") -> list[dict]:
        """
        Search across source, topic, and global files.

        Args:
            query: Search query (keyword or phrase)
            scope: "source", "topic", "global", or "all"

        Returns:
            List of {scope, file, relevance, snippet} dicts, sorted by relevance
        """
        query_lower = query.lower()
        query_words = set(query_lower.split())
        results = []

        search_dirs = {
            "source": self.source_dir,
            "topic": self.topic_dir,
            "global": self.global_dir,
        }

        for dir_scope, dir_path in search_dirs.items():
            if scope != "all" and scope != dir_scope:
                continue

            if not dir_path.exists():
                continue

            for md_file in sorted(dir_path.glob("*.md")):
                try:
                    content = md_file.read_text(encoding="utf-8", errors="replace")
                except OSError:
                    continue

                content_lower = content.lower()

                # Calculate relevance score
                score = 0
                for word in query_words:
                    # Title/filename match
                    if word in md_file.name.lower():
                        score += 10
                    # Heading match (## lines)
                    for line in content.split("\n"):
                        if line.strip().startswith("#") and word in line.lower():
                            score += 5
                    # Content frequency
                    score += content_lower.count(word)

                if score > 0:
                    # Extract snippet (first 200 chars around first match)
                    snippet = self._extract_snippet(content, query_words)

                    results.append({
                        "scope": dir_scope,
                        "file": md_file.name,
                        "path": str(md_file),
                        "relevance": score,
                        "tokens": estimate_tokens(content),
                        "snippet": snippet,
                    })

        # Sort by relevance descending
        results.sort(key=lambda r: r["relevance"], reverse=True)
        return results

    def _extract_snippet(self, content: str, query_words: set[str], max_len: int = 300) -> str:
        """Extract a snippet around the first match of query words."""
        content_lower = content.lower()
        best_pos = len(content)

        for word in query_words:
            pos = content_lower.find(word)
            if pos != -1 and pos < best_pos:
                best_pos = pos

        if best_pos == len(content):
            return content[:max_len] + ("..." if len(content) > max_len else "")

        # Expand around match
        start = max(0, best_pos - 100)
        end = min(len(content), best_pos + 200)
        snippet = content[start:end]
        if start > 0:
            snippet = "..." + snippet
        if end < len(content):
            snippet += "..."
        return snippet

    # ── Store ─────────────────────────────────────────────────────────────────

    def store(self, content: str, source_type: str = "conversation",
              topic_hint: str = None) -> str:
        """
        Save new content to source/ directory.

        Args:
            content: The content to store
            source_type: Type of source (conversation, research, tool-output, web-fetch)
            topic_hint: Optional topic hint for future sealing

        Returns:
            Path to the created source file
        """
        now = datetime.now(timezone.utc)
        date = now.strftime("%Y-%m-%d")
        timestamp = now.strftime("%Y-%m-%dT%H-%M-%S")

        # Build filename
        if topic_hint:
            slug = re.sub(r"[^a-z0-9]+", "-", topic_hint.lower()).strip("-")[:40]
            filename = f"{date}-{source_type}-{slug}.md"
        else:
            filename = f"{date}-{source_type}-{timestamp}.md"

        # Avoid collisions
        filepath = self.source_dir / filename
        counter = 1
        while filepath.exists():
            filename = f"{date}-{source_type}-{slug if topic_hint else timestamp}-{counter}.md"
            filepath = self.source_dir / filename
            counter += 1

        # Add frontmatter
        frontmatter = f"""---
type: {source_type}
date: {date}
topic_hint: {topic_hint or 'auto'}
created: {now.isoformat()}
---

"""
        full_content = frontmatter + content
        filepath.write_text(full_content, encoding="utf-8")

        # Update index
        index = self.index
        rel = str(filepath.relative_to(self.root))
        index.setdefault("sources", {})[rel] = {
            "sealed": False,
            "tokens": estimate_tokens(full_content),
            "type": source_type,
            "topic_hint": topic_hint,
            "created": now.isoformat(),
        }
        self._save_index(index)

        return str(filepath)

    # ── Forget ────────────────────────────────────────────────────────────────

    def forget(self, topic: str, keep_source: bool = True) -> dict:
        """
        Remove a topic summary and optionally its source files.

        Args:
            topic: Topic name to remove
            keep_source: If True, keep source files (only remove topic summary)

        Returns:
            Dict with removal details
        """
        topic_file = self.topic_dir / f"{topic}.md"
        result = {"topic": topic, "removed_topic": False, "removed_sources": 0}

        # Remove topic summary
        if topic_file.exists():
            topic_file.unlink()
            result["removed_topic"] = True

        # Remove source files (if not keeping)
        if not keep_source:
            index = self.index
            source_list = index.get("source_to_topic", {}).get(topic, [])
            for source_rel in source_list:
                source_path = self.root / source_rel
                if source_path.exists():
                    source_path.unlink()
                    result["removed_sources"] += 1

        # Update index
        index = self.index
        index.pop("source_to_topic", {}).pop(topic, None)
        index.get("topics", {}).pop(topic, None)
        # Mark related sources as unsealed
        for rel, info in index.get("sources", {}).items():
            if topic in info.get("topics", []):
                info["sealed"] = False
                info["topics"].remove(topic)
        self._save_index(index)

        return result

    # ── Seal ───────────────────────────────────────────────────────────────────

    def seal(self) -> dict:
        """
        Trigger sealing worker on new files.

        Returns:
            Dict with sealing results
        """
        sys.path.insert(0, str(Path(__file__).parent))
        from seal_worker import main as seal_main

        # Capture output
        import io
        from contextlib import redirect_stdout

        output = io.StringIO()
        with redirect_stdout(output):
            seal_main()

        return {
            "output": output.getvalue(),
            "status": "completed",
        }

    # ── Status ────────────────────────────────────────────────────────────────

    def status(self) -> dict:
        """
        Show memory tree status.

        Returns:
            Dict with file counts, sizes, and unsealed count
        """
        source_files = sorted(self.source_dir.glob("*.md"))
        topic_files = sorted(self.topic_dir.glob("*.md"))
        global_files = sorted(self.global_dir.glob("*.md"))

        index = self.index
        sealed = sum(1 for v in index.get("sources", {}).values() if v.get("sealed"))
        unsealed = len(source_files) - sealed

        source_bytes = sum(f.stat().st_size for f in source_files)
        topic_bytes = sum(f.stat().st_size for f in topic_files)
        global_bytes = sum(f.stat().st_size for f in global_files)

        return {
            "source": {"count": len(source_files), "bytes": source_bytes},
            "topic": {"count": len(topic_files), "bytes": topic_bytes},
            "global": {"count": len(global_files), "bytes": global_bytes},
            "sealed": sealed,
            "unsealed": unsealed,
            "last_seal": index.get("last_seal"),
        }


# ── CLI ─────────────────────────────────────────────────────────────────────────

def main():
    if len(sys.argv) < 2:
        print("Memory Tree Tools")
        print()
        print("Usage:")
        print("  python3 tools.py recall <query> [scope]  — Search memory")
        print("  python3 tools.py store <content> [topic] — Store new content")
        print("  python3 tools.py forget <topic> [keep]   — Remove topic")
        print("  python3 tools.py seal                    — Run sealing worker")
        print("  python3 tools.py status                  — Show status")
        print()
        print("Scopes: source, topic, global, all (default)")
        sys.exit(0)

    command = sys.argv[1].lower()
    mt = MemoryTree()

    if command == "recall":
        query = sys.argv[2] if len(sys.argv) > 2 else ""
        scope = sys.argv[3] if len(sys.argv) > 3 else "all"
        if not query:
            print("Usage: python3 tools.py recall <query> [scope]")
            sys.exit(1)
        results = mt.recall(query, scope)
        if results:
            print(f"Found {len(results)} results for '{query}':\n")
            for r in results[:20]:
                print(f"  [{r['scope']}] {r['file']} (relevance: {r['relevance']})")
                print(f"    {r['snippet'][:100]}...")
                print()
        else:
            print(f"No results for '{query}'")

    elif command == "store":
        content = sys.argv[2] if len(sys.argv) > 2 else ""
        topic = sys.argv[3] if len(sys.argv) > 3 else None
        if not content:
            print("Usage: python3 tools.py store <content> [topic_hint]")
            sys.exit(1)
        path = mt.store(content, source_type="manual", topic_hint=topic)
        print(f"Stored: {path}")

    elif command == "forget":
        topic = sys.argv[2] if len(sys.argv) > 2 else ""
        keep = "--keep-source" in sys.argv or len(sys.argv) <= 3
        if not topic:
            print("Usage: python3 tools.py forget <topic> [--keep-source]")
            sys.exit(1)
        result = mt.forget(topic, keep_source=keep)
        print(f"Forgot topic '{topic}': removed={result['removed_topic']}, sources_removed={result['removed_sources']}")

    elif command == "seal":
        result = mt.seal()
        print(result["output"])

    elif command == "status":
        status = mt.status()
        print("Memory Tree Status:")
        print(f"  Source files:  {status['source']['count']}  ({status['source']['bytes']} bytes)")
        print(f"  Topic files:   {status['topic']['count']}  ({status['topic']['bytes']} bytes)")
        print(f"  Global files:  {status['global']['count']}  ({status['global']['bytes']} bytes)")
        print(f"  Sealed:        {status['sealed']}")
        print(f"  Unsealed:      {status['unsealed']}")
        print(f"  Last seal:     {status['last_seal']}")

    else:
        print(f"Unknown command: {command}")
        print("Commands: recall, store, forget, seal, status")


if __name__ == "__main__":
    main()

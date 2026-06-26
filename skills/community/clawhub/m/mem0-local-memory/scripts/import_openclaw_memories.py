#!/usr/bin/env python3
"""
Import OpenClaw workspace memories into local mem0.
Reads MEMORY.md and TOOLS.md from each workspace, splits by Markdown sections,
and adds each section as a separate memory entry.

All memories use unified user_id="openclaw" (no agent isolation).
Source agent is tracked in metadata for traceability.
"""
import os
import re
import sys
import json
import time
import requests

MEM0_URL = os.environ.get("MEM0_URL", "http://127.0.0.1:8300")
UNIFIED_USER_ID = "openclaw"

WORKSPACES = {
    "main":     os.path.expanduser("~/.openclaw/workspace-main"),
    "claude":   os.path.expanduser("~/.openclaw/workspace-claude"),
    "claude2":  os.path.expanduser("~/.openclaw/workspace-claude2"),
    "chatgpt":  os.path.expanduser("~/.openclaw/workspace-chatgpt"),
    "qwen":     os.path.expanduser("~/.openclaw/workspace-qwen"),
}

FILES_TO_IMPORT = ["MEMORY.md", "TOOLS.md"]


def check_health():
    """Check mem0 server is running."""
    try:
        r = requests.get(f"{MEM0_URL}/api/health", timeout=5)
        data = r.json()
        if data.get("status") == "ok":
            print(f"✅ mem0 server healthy (memories: {data.get('total_memories', '?')})")
            return True
    except Exception as e:
        print(f"❌ mem0 server not reachable: {e}")
    return False


def split_by_sections(content: str) -> list[str]:
    """Split Markdown content by ## or ### headings into meaningful chunks."""
    sections = []
    current = []

    for line in content.split("\n"):
        if re.match(r'^#{1,3}\s+', line) and current:
            text = "\n".join(current).strip()
            if text and len(text) > 15:
                sections.append(text)
            current = [line]
        else:
            current.append(line)

    # Last section
    if current:
        text = "\n".join(current).strip()
        if text and len(text) > 15:
            sections.append(text)

    return sections


def add_memory(text: str, source_agent: str, source_file: str) -> bool:
    """Add a memory to mem0 with unified user_id and source metadata."""
    try:
        r = requests.post(
            f"{MEM0_URL}/api/memory/add",
            json={
                "text": text,
                "user_id": UNIFIED_USER_ID,
                "metadata": {
                    "source_agent": source_agent,
                    "source_file": source_file,
                }
            },
            headers={"Content-Type": "application/json"},
            timeout=30,
        )
        return r.status_code == 200
    except Exception as e:
        print(f"  ⚠️  Failed to add memory: {e}")
        return False


def import_workspace(agent_id: str, workspace_path: str):
    """Import MEMORY.md and TOOLS.md from a workspace."""
    total_added = 0
    total_skipped = 0

    for filename in FILES_TO_IMPORT:
        filepath = os.path.join(workspace_path, filename)
        if not os.path.exists(filepath):
            print(f"  ⏭️  {filename} not found, skipping")
            continue

        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read()

        if not content.strip():
            print(f"  ⏭️  {filename} is empty, skipping")
            continue

        sections = split_by_sections(content)
        print(f"  📄 {filename}: {len(sections)} sections")

        for i, section in enumerate(sections):
            # Skip pure title/header-only sections
            lines = [l for l in section.split("\n") if l.strip() and not l.startswith("#")]
            if not lines or len("\n".join(lines)) < 15:
                total_skipped += 1
                continue

            # Prefix with source info for context
            tagged = f"[source: {agent_id}/{filename}]\n{section}"

            if add_memory(tagged, agent_id, filename):
                total_added += 1
                print(f"    ✅ Section {i+1}/{len(sections)}")
            else:
                total_skipped += 1
                print(f"    ❌ Section {i+1}/{len(sections)} failed")

            # Small delay to avoid overwhelming the LLM
            time.sleep(1)

    return total_added, total_skipped


def main():
    print("=" * 60)
    print("OpenClaw → mem0 Memory Import (unified user_id)")
    print(f"All memories → user_id: {UNIFIED_USER_ID}")
    print("=" * 60)
    print()

    if not check_health():
        print("\nPlease start mem0 server first:")
        print("  cd ~/.openclaw/mem0-local && ./venv/bin/python3 mem0_server.py")
        sys.exit(1)

    print()
    grand_total = 0
    grand_skipped = 0

    for agent_id, workspace_path in WORKSPACES.items():
        print(f"📁 {agent_id} ({workspace_path})")

        if not os.path.exists(workspace_path):
            print(f"  ⏭️  Workspace not found, skipping")
            continue

        added, skipped = import_workspace(agent_id, workspace_path)
        grand_total += added
        grand_skipped += skipped
        print(f"  → Added: {added}, Skipped: {skipped}")
        print()

    print("=" * 60)
    print(f"Import complete! Total: {grand_total} memories added, {grand_skipped} skipped")
    print()

    # Final health check
    check_health()


if __name__ == "__main__":
    main()

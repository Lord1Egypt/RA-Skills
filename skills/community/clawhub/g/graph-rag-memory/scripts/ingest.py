#!/usr/bin/env python3
"""
ingest.py — Ingest content into the graph-rag memory system.

Usage:
    python3 ingest.py --file path/to/file.md
    python3 ingest.py --file path/to/file.md --domain project
    python3 ingest.py --text "Jebadiah decided to use FalkorDB because..."
    python3 ingest.py --text "..." --domain personal --group workspace
    python3 ingest.py --workspace /path/to/workspace  # ingest all memory/*.md files
"""

import asyncio
import sys
import os
import argparse
from pathlib import Path

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
WORKSPACE_ROOT = os.environ.get("OPENCLAW_WORKSPACE", "/home/node/.openclaw/workspace")
MEM_DIR = os.path.join(WORKSPACE_ROOT, "memory-upgrade")
sys.path.insert(0, MEM_DIR)

from setup_graphiti import init_graphiti
from write_path import ingest_memory, ingest_workspace_memories
from router import DomainRouter
from config import OLLAMA_URL


async def main():
    parser = argparse.ArgumentParser(description="Ingest content into graph-rag memory")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--file", help="Path to file to ingest")
    group.add_argument("--text", help="Text content to ingest directly")
    group.add_argument("--workspace", help="Path to workspace root (ingests all memory/*.md)")
    parser.add_argument("--domain", help="Force domain: personal/project/technical/research/episodic/meta")
    parser.add_argument("--graph", default="workspace", help="Target graph (default: workspace)")
    parser.add_argument("--group", default="workspace", help="Group ID (default: workspace)")
    args = parser.parse_args()

    print("Initializing Graphiti...")
    graphiti = await init_graphiti(args.graph)
    router = DomainRouter(ollama_base_url=OLLAMA_URL)
    print("✅ Ready\n")

    metadata = {}
    if args.domain:
        metadata["domain"] = args.domain

    if args.workspace:
        print(f"Ingesting workspace memory files from: {args.workspace}")
        await ingest_workspace_memories(graphiti, router, args.workspace, args.group)

    elif args.file:
        filepath = Path(args.file)
        if not filepath.exists():
            print(f"❌ File not found: {args.file}")
            sys.exit(1)
        content = filepath.read_text()
        metadata["file_path"] = str(filepath)
        print(f"Ingesting: {filepath.name} ({len(content)} chars)")
        routing = await ingest_memory(
            graphiti=graphiti,
            router=router,
            content=content,
            source_description=f"file:{filepath.name}",
            metadata=metadata,
            group_id=args.group,
            episode_name=filepath.stem,
        )
        print(f"✅ Ingested → domain: {routing.domain} ({routing.method})")

    elif args.text:
        content = args.text
        print(f"Ingesting text ({len(content)} chars)...")
        routing = await ingest_memory(
            graphiti=graphiti,
            router=router,
            content=content,
            source_description="inline_text",
            metadata=metadata,
            group_id=args.group,
        )
        print(f"✅ Ingested → domain: {routing.domain} ({routing.method})")

    await graphiti.close()


if __name__ == "__main__":
    asyncio.run(main())

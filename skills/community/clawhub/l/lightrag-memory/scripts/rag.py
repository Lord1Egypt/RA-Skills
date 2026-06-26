#!/usr/bin/env python3
"""
LightRAG memory management for AI agent skills.
Index, insert, and query semantic memory using vector embeddings + knowledge graph.
"""
import os
import sys
import argparse
import asyncio
import numpy as np
from pathlib import Path

from lightrag import LightRAG, QueryParam
from lightrag.llm.openai import openai_complete_if_cache
from lightrag.utils import EmbeddingFunc

# Storage directory
WORKING_DIR = os.environ.get(
    "LIGHTARG_WORKING_DIR",
    os.path.expanduser("~/.openclaw/workspace/lightrag_storage")
)
os.makedirs(WORKING_DIR, exist_ok=True)


async def _custom_embed(texts, model="text-embedding-3-small", base_url=None):
    """Embedding function with custom base_url support."""
    import openai

    api_key = os.getenv("OPENAI_API_KEY")
    if base_url is None:
        base_url = os.getenv("OPENAI_BASE_URL", "https://api.openai.com/v1")

    if not base_url.endswith("/v1"):
        base_url = base_url.rstrip("/") + "/v1"

    client = openai.AsyncOpenAI(api_key=api_key, base_url=base_url)
    response = await client.embeddings.create(
        model=model, input=texts, encoding_format="float"
    )
    return np.array([item.embedding for item in response.data])


def get_rag():
    """Create configured LightRAG instance."""
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        print("Error: OPENAI_API_KEY not set", file=sys.stderr)
        sys.exit(1)

    base_url = os.getenv("OPENAI_BASE_URL", "https://api.openai.com/v1")

    async def llm_func(prompt, system_prompt=None, history_messages=None, **kw):
        return await openai_complete_if_cache(
            model="gpt-4o-mini",
            prompt=prompt,
            system_prompt=system_prompt,
            history_messages=history_messages,
            base_url=base_url,
            api_key=api_key,
            **kw,
        )

    async def embed_func(texts):
        return await _custom_embed(texts, base_url=base_url)

    embedding = EmbeddingFunc(
        embedding_dim=1536,
        func=embed_func,
        max_token_size=8192,
    )

    return LightRAG(
        working_dir=WORKING_DIR,
        llm_model_func=llm_func,
        embedding_func=embedding,
        embedding_func_max_async=4,
        embedding_batch_num=8,
    )


async def insert_text(text, source=None):
    rag = get_rag()
    await rag.initialize_storages()
    await rag.ainsert(text)
    print(f"Inserted text from {source or 'stdin'}")


async def insert_file(filepath):
    with open(filepath, "r", encoding="utf-8") as f:
        text = f.read()
    await insert_text(text, source=filepath)


async def do_query(question, mode="hybrid"):
    rag = get_rag()
    await rag.initialize_storages()
    result = await rag.aquery(question, param=QueryParam(mode=mode))
    print(result)


async def index_memory_files(workspace=None):
    """Index MEMORY.md and memory/*.md from workspace."""
    if workspace is None:
        workspace = os.path.expanduser("~/.openclaw/workspace")

    files = []
    memory_md = os.path.join(workspace, "MEMORY.md")
    if os.path.exists(memory_md):
        files.append(memory_md)

    memory_dir = os.path.join(workspace, "memory")
    if os.path.isdir(memory_dir):
        files.extend(str(p) for p in Path(memory_dir).glob("*.md"))

    if not files:
        print("No memory files found to index.")
        return

    print(f"Indexing {len(files)} files...")
    rag = get_rag()
    await rag.initialize_storages()

    for fp in files:
        print(f"  - {fp}")
        try:
            with open(fp, "r", encoding="utf-8") as f:
                text = f.read()
            await rag.ainsert(text)
            print("    ✓ Done")
        except Exception as e:
            print(f"    ✗ Error: {e}")

    print("Indexing complete!")


def main():
    # Load .env from script directory if present
    script_dir = Path(__file__).parent
    env_file = script_dir.parent / ".env"
    if env_file.exists():
        try:
            from dotenv import load_dotenv
            load_dotenv(env_file)
        except ImportError:
            pass

    parser = argparse.ArgumentParser(description="LightRAG memory management")
    sub = parser.add_subparsers(dest="command")

    # insert
    ins = sub.add_parser("insert", help="Insert text into knowledge base")
    ins.add_argument("--file", help="File path to insert")
    ins.add_argument("--text", help="Text to insert")
    ins.add_argument("--source", help="Source identifier")

    # query
    qry = sub.add_parser("query", help="Query knowledge base")
    qry.add_argument("question", help="Question to ask")
    qry.add_argument(
        "--mode", default="hybrid",
        choices=["naive", "local", "global", "hybrid"],
    )

    # index
    idx = sub.add_parser("index", help="Index workspace memory files")
    idx.add_argument("--workspace", help="Workspace root path")

    args = parser.parse_args()

    if args.command == "insert":
        if args.file:
            asyncio.run(insert_file(args.file))
        elif args.text:
            asyncio.run(insert_text(args.text, source=args.source))
        else:
            asyncio.run(insert_text(sys.stdin.read(), source=args.source))
    elif args.command == "query":
        asyncio.run(do_query(args.question, mode=args.mode))
    elif args.command == "index":
        asyncio.run(index_memory_files(workspace=args.workspace))
    else:
        parser.print_help()


if __name__ == "__main__":
    main()

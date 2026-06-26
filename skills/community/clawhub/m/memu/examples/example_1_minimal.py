"""
Example 1: Minimal memU Integration (In-Memory Mode)
=====================================================
No PostgreSQL required. Memory lives in-process and resets on restart.
Good for testing and prototyping.

Requirements:
    pip install memu-py
    export OPENAI_API_KEY=sk-your-key

Usage:
    python example_1_minimal.py
"""

import asyncio
import os
from memu import MemoryService


async def main():
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        print("Error: Set OPENAI_API_KEY environment variable.")
        print("  export OPENAI_API_KEY=sk-your-key")
        return

    # Initialize memU with in-memory storage
    service = MemoryService(
        llm_profiles={
            "default": {
                "provider": "openai",
                "base_url": "https://api.openai.com/v1",
                "api_key": api_key,
                "chat_model": "gpt-4o-mini",
                "embed_model": "text-embedding-3-small",
            }
        }
    )

    # --- Memorize a conversation ---
    print("Memorizing conversation...")
    result = await service.memorize(
        resource_payload=[
            {"role": "user", "content": "I always deploy on Tuesdays after the 10am standup."},
            {"role": "assistant", "content": "Noted — I'll remind you about deployments on Tuesday mornings."},
            {"role": "user", "content": "Our staging database is PostgreSQL 15 on db-staging.internal."},
            {"role": "assistant", "content": "Got it, staging DB is PostgreSQL 15 at db-staging.internal."},
        ],
        modality="conversation",
    )
    print(f"  Extracted {len(result.memory_items)} memory items.")

    # --- Retrieve with embedding (fast) ---
    print("\nRetrieving with embedding mode...")
    memories = await service.retrieve(
        query=[{"role": "user", "content": "When do we usually deploy?"}],
        method="embedding",
    )
    for m in memories:
        print(f"  [{m.category}] {m.content}")

    # --- Retrieve with LLM (deeper reasoning) ---
    print("\nRetrieving with LLM mode...")
    memories = await service.retrieve(
        query=[{"role": "user", "content": "What should I prepare before deploying?"}],
        method="llm",
    )
    for m in memories:
        print(f"  [{m.category}] {m.content}")

    print("\nDone.")


if __name__ == "__main__":
    asyncio.run(main())

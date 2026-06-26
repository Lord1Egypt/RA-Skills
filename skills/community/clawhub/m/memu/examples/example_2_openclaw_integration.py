"""
Example 2: OpenClaw Agent Integration
======================================
Replaces OpenClaw's default flat-file memory with memU's hierarchical memory.
Uses PostgreSQL for persistent storage across agent restarts.

Requirements:
    pip install memu-py
    docker run -d --name memu-postgres \
      -e POSTGRES_USER=postgres -e POSTGRES_PASSWORD=postgres \
      -e POSTGRES_DB=memu -p 5432:5432 pgvector/pgvector:pg16
    export OPENAI_API_KEY=sk-your-key

Usage:
    python example_2_openclaw_integration.py
"""

import asyncio
import os
from memu import MemoryService


class OpenClawMemUAgent:
    """
    Drop-in memory replacement for an OpenClaw-style agent.
    Replaces flat Markdown + SQLite with memU's three-layer architecture.
    """

    def __init__(self):
        api_key = os.environ.get("OPENAI_API_KEY")
        if not api_key:
            raise EnvironmentError("Set OPENAI_API_KEY environment variable.")

        self.memory = MemoryService(
            llm_profiles={
                "default": {
                    "provider": "openai",
                    "base_url": "https://api.openai.com/v1",
                    "api_key": api_key,
                    "chat_model": "gpt-4o-mini",
                    "embed_model": "text-embedding-3-small",
                }
            },
            database_config={
                "provider": "postgresql",
                "url": "postgresql://postgres:postgres@localhost:5432/memu",
            },
        )
        self.conversation_buffer: list[dict] = []

    async def on_user_message(self, user_id: str, message: str) -> str:
        """
        Process a user message: retrieve relevant memory, generate response,
        and store the interaction.
        """
        # Step 1: Retrieve relevant memory BEFORE generating response
        memories = await self.memory.retrieve(
            query=[{"role": "user", "content": message}],
            method="embedding",
        )

        # Step 2: Format memory context for the LLM
        memory_lines = [f"- [{m.category}] {m.content}" for m in memories]
        memory_context = "\n".join(memory_lines) if memory_lines else "(no relevant memory)"

        # Step 3: Build prompt with memory (your LLM call goes here)
        system_prompt = (
            "You are a helpful assistant. Use the following memory context "
            "to provide informed, personalized responses.\n\n"
            f"Relevant memory:\n{memory_context}"
        )
        print(f"System prompt with {len(memories)} memory items injected.")
        print(f"Memory context:\n{memory_context}\n")

        # Placeholder: replace with your actual LLM call
        response = f"[Agent would respond using {len(memories)} memory items as context]"

        # Step 4: Buffer the conversation turn
        self.conversation_buffer.append({"role": "user", "content": message})
        self.conversation_buffer.append({"role": "assistant", "content": response})

        # Step 5: Memorize in batches (every 4 turns = 2 exchanges)
        if len(self.conversation_buffer) >= 4:
            await self.memory.memorize(
                resource_payload=self.conversation_buffer,
                modality="conversation",
                user={"user_id": user_id},
            )
            print(f"  Memorized {len(self.conversation_buffer)} turns.")
            self.conversation_buffer.clear()

        return response


async def main():
    agent = OpenClawMemUAgent()

    # Simulate a multi-turn conversation
    user_id = "user-alice"
    messages = [
        "I'm working on the payment service refactor. Using Go this time.",
        "Can you remind me what framework we used last time for the auth service?",
        "The staging deploy failed yesterday because of a missing env var.",
        "What are the common deployment issues we've seen?",
    ]

    for msg in messages:
        print(f"\nUser: {msg}")
        response = await agent.on_user_message(user_id, msg)
        print(f"Agent: {response}")


if __name__ == "__main__":
    asyncio.run(main())

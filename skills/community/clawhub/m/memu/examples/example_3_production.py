"""
Example 3: Production-Grade memU Integration
=============================================
Includes logging, error handling, retry logic, and performance monitoring.
Suitable for 24/7 agent deployments.

Requirements:
    pip install memu-py httpx
    PostgreSQL 16 with pgvector running
    export OPENAI_API_KEY=sk-your-key
    export MEMU_DB_URL=postgresql://user:pass@host:5432/memu

Usage:
    python example_3_production.py
"""

import asyncio
import logging
import os
import time
from dataclasses import dataclass, field

from memu import MemoryService

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
)
logger = logging.getLogger("memu-agent")


@dataclass
class MemUMetrics:
    """Simple in-process metrics for monitoring memU operations."""
    memorize_count: int = 0
    memorize_errors: int = 0
    memorize_total_ms: float = 0
    retrieve_count: int = 0
    retrieve_errors: int = 0
    retrieve_total_ms: float = 0

    def log_summary(self):
        avg_mem = (self.memorize_total_ms / self.memorize_count) if self.memorize_count else 0
        avg_ret = (self.retrieve_total_ms / self.retrieve_count) if self.retrieve_count else 0
        logger.info(
            "Metrics | memorize: %d ok / %d err / %.0fms avg | "
            "retrieve: %d ok / %d err / %.0fms avg",
            self.memorize_count, self.memorize_errors, avg_mem,
            self.retrieve_count, self.retrieve_errors, avg_ret,
        )


class ProductionMemUAgent:
    MAX_RETRIES = 3
    RETRY_DELAY_S = 1.0

    def __init__(self):
        db_url = os.environ.get("MEMU_DB_URL")
        api_key = os.environ.get("OPENAI_API_KEY")

        if not api_key:
            raise EnvironmentError("OPENAI_API_KEY is required.")
        if not db_url:
            logger.warning("MEMU_DB_URL not set; falling back to in-memory storage.")

        db_config = {"provider": "postgresql", "url": db_url} if db_url else None

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
            database_config=db_config,
        )
        self.metrics = MemUMetrics()

    async def _retry(self, operation: str, coro_factory):
        """Execute an async operation with retries and timing."""
        for attempt in range(1, self.MAX_RETRIES + 1):
            start = time.monotonic()
            try:
                result = await coro_factory()
                elapsed_ms = (time.monotonic() - start) * 1000

                if operation == "memorize":
                    self.metrics.memorize_count += 1
                    self.metrics.memorize_total_ms += elapsed_ms
                else:
                    self.metrics.retrieve_count += 1
                    self.metrics.retrieve_total_ms += elapsed_ms

                logger.debug("%s completed in %.0fms (attempt %d)", operation, elapsed_ms, attempt)
                return result

            except Exception as exc:
                elapsed_ms = (time.monotonic() - start) * 1000
                logger.warning(
                    "%s failed (attempt %d/%d, %.0fms): %s",
                    operation, attempt, self.MAX_RETRIES, elapsed_ms, exc,
                )
                if attempt == self.MAX_RETRIES:
                    if operation == "memorize":
                        self.metrics.memorize_errors += 1
                    else:
                        self.metrics.retrieve_errors += 1
                    logger.error("%s exhausted retries. Last error: %s", operation, exc)
                    return None
                await asyncio.sleep(self.RETRY_DELAY_S * attempt)

    async def memorize(self, payload: list[dict], user_id: str, modality: str = "conversation"):
        """Memorize with retries and error handling."""
        return await self._retry(
            "memorize",
            lambda: self.memory.memorize(
                resource_payload=payload,
                modality=modality,
                user={"user_id": user_id},
            ),
        )

    async def retrieve(self, query: str, method: str = "embedding"):
        """Retrieve with retries, falling back to embedding if LLM fails."""
        result = await self._retry(
            "retrieve",
            lambda: self.memory.retrieve(
                query=[{"role": "user", "content": query}],
                method=method,
            ),
        )
        if result is None and method == "llm":
            logger.info("LLM retrieval failed; falling back to embedding mode.")
            result = await self._retry(
                "retrieve",
                lambda: self.memory.retrieve(
                    query=[{"role": "user", "content": query}],
                    method="embedding",
                ),
            )
        return result or []


async def main():
    agent = ProductionMemUAgent()

    # Memorize some data
    await agent.memorize(
        payload=[
            {"role": "user", "content": "The payment service uses Stripe API v2023-10-16."},
            {"role": "assistant", "content": "Noted, I'll track that Stripe API version."},
        ],
        user_id="ops-team",
    )

    # Retrieve
    results = await agent.retrieve("What payment provider do we use?")
    for m in results:
        logger.info("Retrieved: [%s] %s", m.category, m.content)

    # Print metrics
    agent.metrics.log_summary()


if __name__ == "__main__":
    asyncio.run(main())

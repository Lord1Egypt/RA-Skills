"""
Consolidator — The "sleep cycle" that promotes memories to long-term storage.

Uses prediction error scores to decide what gets promoted to MEMORY.md.
Only high-surprise events reshape the world model.
"""

from __future__ import annotations

from datetime import datetime, date
from pathlib import Path

from .providers import LLMProvider
from .prediction_error import PredictionErrorEngine, PredictionResult


CONSOLIDATE_PROMPT = """You are a memory consolidation system performing a "sleep cycle."

Based on today's prediction errors (what surprised you), update the agent's 
long-term memory. Focus on:

1. NEW FACTS that change the world model (high prediction error)
2. RELATIONSHIP CHANGES between entities
3. LESSONS LEARNED from unexpected outcomes
4. STATUS UPDATES for tracked entities/projects

Do NOT include:
- Routine events (heartbeats, regular checks)
- Events already captured in MEMORY.md
- Low-surprise events (prediction_error < 0.4)

Output a markdown section to APPEND to MEMORY.md:

## Consolidated {date}
- **key insight or update**
- **key insight or update**

Keep it concise. 3-8 bullet points maximum.

CURRENT MEMORY.MD (world model):
{memory}

TODAY'S PREDICTION ERRORS:
{errors}

SUGGESTED MODEL UPDATES FROM PE ENGINE:
{updates}
"""


class Consolidator:
    """Promotes high-surprise events to long-term memory."""

    def __init__(self, llm: LLMProvider, memory_dir: Path, memory_file: Path):
        self.llm = llm
        self.memory_dir = memory_dir
        self.memory_file = memory_file
        self.pe_engine = PredictionErrorEngine(llm, memory_dir, memory_file)

    async def run(self, date_str: str | None = None) -> str:
        """
        Full consolidation cycle:
        1. Compute prediction errors
        2. Filter for high-surprise events
        3. Generate MEMORY.md update
        4. Append to MEMORY.md
        """
        if date_str is None:
            date_str = date.today().isoformat()

        # Stage 1: Compute prediction errors
        pe_result = await self.pe_engine.compute(date_str)

        if not pe_result.errors:
            return f"No events to consolidate for {date_str}"

        # Stage 2: Filter
        worth_consolidating = [e for e in pe_result.errors if e.should_consolidate(0.4)]
        if not worth_consolidating:
            return f"No surprising events for {date_str} (mean PE: {pe_result.mean_surprise:.2f})"

        # Stage 3: Generate update
        memory = self.memory_file.read_text()[:4000] if self.memory_file.exists() else ""
        errors_text = "\n".join(
            f"- [{e.prediction_error:.1f}] {e.event} — {e.reason}"
            for e in worth_consolidating
        )
        updates_text = "\n".join(f"- {u}" for u in pe_result.model_updates)

        prompt = CONSOLIDATE_PROMPT.format(
            date=date_str,
            memory=memory,
            errors=errors_text,
            updates=updates_text
        )
        result = self.llm.generate_json_sync(prompt)

        # If LLM returned JSON, format it. Otherwise use raw text.
        if isinstance(result, dict) and "content" in result:
            update_text = result["content"]
        else:
            # The prompt asks for markdown, so the LLM might not return JSON
            # Fall back to generating markdown directly
            update_text = self._generate_markdown_update(pe_result, date_str)

        # Stage 4: Append to MEMORY.md
        if update_text:
            with open(self.memory_file, "a") as f:
                f.write(f"\n\n{update_text}\n")
            return f"Consolidated {len(worth_consolidating)} events for {date_str}"

        return f"Nothing to consolidate for {date_str}"

    def _generate_markdown_update(self, result: PredictionResult, date_str: str) -> str:
        """Fallback: generate markdown update directly from PE scores."""
        lines = [f"## Consolidated {date_str}"]
        
        for e in result.high_surprise:
            lines.append(f"- 🔴 **{e.event}** (PE: {e.prediction_error:.1f})")
        
        for e in result.medium_surprise:
            lines.append(f"- 🟡 {e.event} (PE: {e.prediction_error:.1f})")

        if result.model_updates:
            lines.append("")
            lines.append("### World Model Updates")
            for u in result.model_updates:
                lines.append(f"- {u}")

        return "\n".join(lines)

    def run_sync(self, date_str: str | None = None) -> str:
        """Synchronous wrapper."""
        import asyncio
        return asyncio.run(self.run(date_str))

"""
mindclaw.context — Context window builder for LLM agents.

Turns a recall query into a formatted, token-aware context block
ready to be injected into an LLM system prompt or user message.

Also provides conflict detection and cluster summarization utilities.
"""

from __future__ import annotations

import time
from dataclasses import dataclass
from typing import Any, Optional

from .search import SearchEngine
from .store import Memory, MemoryStore


# ---------------------------------------------------------------------------
# Token estimation (rough: 1 token ≈ 4 chars for English)
# ---------------------------------------------------------------------------

def _estimate_tokens(text: str) -> int:
    return max(1, len(text) // 4)


# ---------------------------------------------------------------------------
# ContextBuilder
# ---------------------------------------------------------------------------

@dataclass
class ContextBlock:
    """A ready-to-inject context block for an LLM prompt."""
    text: str
    memories_used: int
    estimated_tokens: int
    truncated: bool


class ContextBuilder:
    """
    Retrieves relevant memories and formats them as a context block
    for injection into an LLM prompt.

    Usage:
        builder = ContextBuilder(store)
        block = builder.build("What do we know about the database stack?")
        # inject block.text into your system prompt
    """

    HEADER = "## Relevant memories\n"
    FOOTER = "\n## End of memories\n"
    MEMORY_TEMPLATE = (
        "[{id}] ({category}, importance={importance:.2f}{pinned_marker}) {content}"
    )
    RELATION_TEMPLATE = "  → linked to [{target_id}] via {relation}"

    def __init__(self, store: MemoryStore):
        self.store = store
        self._engine = SearchEngine(store)

    def build(
        self,
        query: str,
        *,
        max_tokens: int = 2000,
        top_k: int = 20,
        agent_id: Optional[str] = None,
        include_relations: bool = True,
        format: str = "markdown",   # "markdown" | "plain" | "xml"
    ) -> ContextBlock:
        """
        Build a token-limited context block from the most relevant memories.

        Args:
            query: What the agent is about to do / needs context for.
            max_tokens: Hard token cap for the returned block.
            top_k: Max candidate memories to consider before capping.
            agent_id: Restrict to a specific agent namespace.
            include_relations: Append direct graph links for each memory.
            format: Output format for the block.

        Returns:
            ContextBlock with formatted text and metadata.
        """
        self._engine.rebuild()
        # Pass agent_id directly to the search engine so the BM25 + Ollama
        # merge respects the namespace filter before scoring, not after.
        candidates = self._engine.search(
            query,
            top_k=top_k,
            agent_id=agent_id,
        )

        lines: list[str] = []
        tokens_used = _estimate_tokens(self.HEADER + self.FOOTER)
        memories_included = 0
        truncated = False

        for result in candidates:
            mem: Memory = result["memory"]
            pinned_marker = ", PINNED" if mem.pinned else ""
            conf_marker = f", confirmed×{mem.confirmed_count}" if mem.confirmed_count > 0 else ""
            line = self.MEMORY_TEMPLATE.format(
                id=mem.id,
                category=mem.category,
                importance=mem.importance,
                pinned_marker=pinned_marker + conf_marker,
                content=mem.content,
            )
            if mem.tags:
                line += f"  [tags: {', '.join(mem.tags)}]"

            relation_lines: list[str] = []
            if include_relations:
                edges = self.store.get_edges(mem.id, direction="out")
                for edge in edges[:3]:  # max 3 relations per memory
                    relation_lines.append(
                        self.RELATION_TEMPLATE.format(
                            target_id=edge["target_id"],
                            relation=edge["relation"],
                        )
                    )

            block_text = line + ("\n" + "\n".join(relation_lines) if relation_lines else "")
            block_tokens = _estimate_tokens(block_text + "\n")

            if tokens_used + block_tokens > max_tokens:
                truncated = True
                break

            lines.append(block_text)
            tokens_used += block_tokens
            memories_included += 1

        if format == "xml":
            body = "\n".join(f"  <memory>{l}</memory>" for l in lines)
            full_text = f"<memories>\n{body}\n</memories>"
        elif format == "plain":
            full_text = "MEMORIES:\n" + "\n".join(f"- {l}" for l in lines)
        else:  # markdown
            full_text = self.HEADER + "\n".join(f"- {l}" for l in lines) + self.FOOTER

        return ContextBlock(
            text=full_text,
            memories_used=memories_included,
            estimated_tokens=_estimate_tokens(full_text),
            truncated=truncated,
        )

    def build_system_prompt(
        self,
        base_prompt: str,
        query: str,
        *,
        max_memory_tokens: int = 1500,
        agent_id: Optional[str] = None,
    ) -> str:
        """
        Inject memory context into a base system prompt string.
        Places the memory block just before the end of the prompt.
        """
        block = self.build(query, max_tokens=max_memory_tokens, agent_id=agent_id)
        if block.memories_used == 0:
            return base_prompt
        return base_prompt.rstrip() + "\n\n" + block.text


# ---------------------------------------------------------------------------
# Conflict reporter
# ---------------------------------------------------------------------------

@dataclass
class ConflictReport:
    """Describes a potential memory conflict."""
    new_content: str
    conflicting_memory: Memory
    similarity: float
    suggestion: str


def check_conflicts(
    new_content: str,
    store: MemoryStore,
    *,
    agent_id: Optional[str] = None,
    threshold: float = 0.20,
) -> list[ConflictReport]:
    """
    Before storing a new memory, check if it contradicts existing ones.
    Returns a list of ConflictReport objects (empty = no conflicts).
    """
    conflicts = store.find_conflicts(new_content, agent_id=agent_id, threshold=threshold)
    reports: list[ConflictReport] = []
    for mem in conflicts:
        words_new = set(new_content.lower().split())
        words_existing = set(mem.content.lower().split())
        union = words_new | words_existing
        sim = len(words_new & words_existing) / len(union) if union else 0
        reports.append(ConflictReport(
            new_content=new_content,
            conflicting_memory=mem,
            similarity=round(sim, 3),
            suggestion=(
                f"Consider confirming [{mem.id}] if this reinforces it, "
                f"or use 'forget {mem.id}' to replace it."
            ),
        ))
    return reports


# ---------------------------------------------------------------------------
# Cluster summarizer
# ---------------------------------------------------------------------------

def summarize_cluster(
    memories: list[Memory],
    *,
    max_chars: int = 500,
) -> str:
    """
    Produce a plain-text summary of a cluster of related memories.
    No LLM required — extracts key sentences by importance rank.

    For richer summarization, pass the output to your LLM.
    """
    if not memories:
        return ""

    # Sort by importance descending, prefer pinned and confirmed
    ranked = sorted(
        memories,
        key=lambda m: m.importance + m.confirmed_count * 0.05 + (0.2 if m.pinned else 0),
        reverse=True,
    )

    parts: list[str] = []
    char_count = 0
    for mem in ranked:
        sentence = mem.summary if mem.summary and mem.summary != mem.content else mem.content
        sentence = sentence[:200]
        if char_count + len(sentence) > max_chars:
            break
        parts.append(f"[{mem.category}] {sentence}")
        char_count += len(sentence)

    categories = list({m.category for m in memories})
    header = f"Cluster of {len(memories)} memories ({', '.join(categories)}):\n"
    return header + "\n".join(f"• {p}" for p in parts)

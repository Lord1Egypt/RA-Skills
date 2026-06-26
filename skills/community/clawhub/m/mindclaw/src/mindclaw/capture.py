"""
mindclaw.capture — Auto-capture engine.

Analyzes text from conversations/sessions and automatically
extracts important facts, decisions, errors, and preferences.
"""

from __future__ import annotations

import re
import time
from dataclasses import dataclass
from typing import Optional

from .graph import KnowledgeGraph
from .store import Memory, MemoryStore


# ---------------------------------------------------------------------------
# Pattern-based importance detection
# ---------------------------------------------------------------------------

@dataclass
class CaptureRule:
    """Rule for detecting capturable information."""
    name: str
    pattern: re.Pattern
    category: str
    importance: float
    extract_group: int = 0


# Default rules — detect common patterns in conversations
DEFAULT_RULES: list[CaptureRule] = [
    CaptureRule(
        name="decision",
        pattern=re.compile(
            r"(?:we decided|decision:|let'?s go with|agreed to|chose to|"
            r"the plan is|we'?ll|going with)\s+(.+)",
            re.IGNORECASE,
        ),
        category="decision",
        importance=0.85,
        extract_group=1,
    ),
    CaptureRule(
        name="error_learned",
        pattern=re.compile(
            r"(?:error:|bug:|issue:|problem:|fix:|fixed:|resolved:)\s+(.+)",
            re.IGNORECASE,
        ),
        category="error",
        importance=0.8,
        extract_group=1,
    ),
    CaptureRule(
        name="preference",
        pattern=re.compile(
            r"(?:i prefer|i like|i always|i never|i want|please always|"
            r"please never|don'?t ever|always use|never use)\s+(.+)",
            re.IGNORECASE,
        ),
        category="preference",
        importance=0.75,
        extract_group=1,
    ),
    CaptureRule(
        name="fact",
        pattern=re.compile(
            r"(?:note:|remember:|important:|fyi:|btw:|fact:)\s+(.+)",
            re.IGNORECASE,
        ),
        category="fact",
        importance=0.7,
        extract_group=1,
    ),
    CaptureRule(
        name="credential",
        pattern=re.compile(
            r"(?:api.?key|token|password|secret|credential).{0,10}(?:is|=|:)\s*(\S+)",
            re.IGNORECASE,
        ),
        category="credential",
        importance=0.9,
        extract_group=0,  # capture full match for context, NOT the secret
    ),
    CaptureRule(
        name="url_resource",
        pattern=re.compile(
            r"(?:docs?(?:umentation)?|reference|link|url|endpoint)(?:\s+(?:is|at|:))?\s+"
            r"(https?://\S+)",
            re.IGNORECASE,
        ),
        category="resource",
        importance=0.6,
        extract_group=1,
    ),
    CaptureRule(
        name="todo",
        pattern=re.compile(
            r"(?:todo|to.do|task|action.item|follow.up):\s+(.+)",
            re.IGNORECASE,
        ),
        category="todo",
        importance=0.8,
        extract_group=1,
    ),
]


# ---------------------------------------------------------------------------
# Capture Result
# ---------------------------------------------------------------------------

@dataclass
class CaptureResult:
    """Result of auto-capture analysis."""
    memory: Memory
    rule_name: str
    matched_text: str
    confidence: float


# ---------------------------------------------------------------------------
# AutoCapture Engine
# ---------------------------------------------------------------------------

class AutoCapture:
    """
    Analyzes input text and automatically extracts memorable information.

    Usage:
        capture = AutoCapture(store)
        results = capture.process("We decided to use PostgreSQL for the backend")
    """

    def __init__(
        self,
        store: MemoryStore,
        graph: Optional[KnowledgeGraph] = None,
        rules: Optional[list[CaptureRule]] = None,
    ):
        self.store = store
        self.graph = graph or KnowledgeGraph(store)
        self.rules = rules or DEFAULT_RULES

    def process(
        self,
        text: str,
        *,
        source: str = "auto-capture",
        dry_run: bool = False,
    ) -> list[CaptureResult]:
        """
        Process a block of text and extract memories.

        Args:
            text: The text to analyze (conversation, log, etc.)
            source: Label for where this text came from
            dry_run: If True, detect but don't save

        Returns:
            List of CaptureResult objects for each detected memory.
        """
        results: list[CaptureResult] = []
        seen_contents: set[str] = set()

        # Process line by line for better granularity
        lines = text.split("\n")

        for line in lines:
            line = line.strip()
            if len(line) < 5:
                continue

            for rule in self.rules:
                match = rule.pattern.search(line)
                if match is None:
                    continue

                # Extract the relevant content
                try:
                    content = match.group(rule.extract_group).strip()
                except IndexError:
                    content = match.group(0).strip()

                # Skip duplicates in this batch
                if content in seen_contents:
                    continue
                seen_contents.add(content)

                # Redact credentials — store the context, not the secret
                if rule.category == "credential":
                    content = _redact_sensitive(line)

                # Check for duplicate in existing store
                if self._is_duplicate(content):
                    continue

                memory = Memory(
                    content=content,
                    summary=f"Auto-captured {rule.category}: {content[:100]}",
                    category=rule.category,
                    tags=[rule.category, "auto-captured"],
                    source=source,
                    importance=rule.importance,
                )

                confidence = _compute_confidence(line, rule)

                if not dry_run:
                    self.store.add(memory)

                results.append(CaptureResult(
                    memory=memory,
                    rule_name=rule.name,
                    matched_text=match.group(0)[:200],
                    confidence=confidence,
                ))

        # Auto-link related captures
        if not dry_run and len(results) > 1:
            self._auto_link(results)

        return results

    def process_conversation(
        self,
        messages: list[dict[str, str]],
        *,
        source: str = "conversation",
    ) -> list[CaptureResult]:
        """
        Process a list of conversation messages.
        Each message should have 'role' and 'content' keys.
        """
        all_results: list[CaptureResult] = []
        for msg in messages:
            role = msg.get("role", "unknown")
            content = msg.get("content", "")
            results = self.process(
                content,
                source=f"{source}:{role}",
            )
            all_results.extend(results)
        return all_results

    def _is_duplicate(self, content: str, threshold: float = 0.9) -> bool:
        """Check if similar content already exists."""
        # Simple check: exact or near-exact match
        existing = self.store.search_text(content[:50], limit=5)
        for mem in existing:
            if _text_similarity(content, mem.content) > threshold:
                return True
        return False

    def _auto_link(self, results: list[CaptureResult]) -> None:
        """Create edges between captures from the same batch."""
        ids = [r.memory.id for r in results]
        for i, r1 in enumerate(results):
            for r2 in results[i + 1:]:
                self.graph.link(
                    r1.memory.id,
                    r2.memory.id,
                    "co_captured",
                    bidirectional=True,
                )


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _redact_sensitive(text: str) -> str:
    """Replace potential secrets with [REDACTED]."""
    # Redact anything that looks like a key/token value
    redacted = re.sub(
        r'((?:key|token|password|secret|credential)\s*[:=]\s*)(\S+)',
        r'\1[REDACTED]',
        text,
        flags=re.IGNORECASE,
    )
    return redacted


def _compute_confidence(text: str, rule: CaptureRule) -> float:
    """Estimate confidence of the capture (0.0 – 1.0)."""
    base = 0.6
    # Longer text = more context = higher confidence
    if len(text) > 50:
        base += 0.1
    if len(text) > 100:
        base += 0.1
    # Multiple pattern keywords boost confidence
    keywords = rule.pattern.pattern.split("|")
    matches = sum(1 for k in keywords if k.lower() in text.lower())
    base += min(matches * 0.05, 0.15)
    return min(base, 1.0)


def _text_similarity(a: str, b: str) -> float:
    """Simple Jaccard similarity between two texts."""
    words_a = set(a.lower().split())
    words_b = set(b.lower().split())
    if not words_a or not words_b:
        return 0.0
    intersection = words_a & words_b
    union = words_a | words_b
    return len(intersection) / len(union)

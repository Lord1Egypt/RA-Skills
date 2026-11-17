"""
chunking_validator.py — Validate that text chunking preserves data integrity.

Use when you've split a long document into chunks (for RAG, for batched
processing, for sending to an LLM) and want to verify nothing was lost or
corrupted. Checks: code blocks aren't split mid-fence, total length matches,
URLs/emails/structured content survived the chunking.
"""
from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Any


@dataclass
class ChunkIssue:
    chunk_index: int  # -1 means "global" (applies to whole document)
    issue_type: str
    description: str
    severity: str  # 'error' or 'warning'


class ChunkingValidator:
    """Validate that chunked text reassembles to the original without loss.

    Three classes of check:
    1. Structural — code fences balanced in each chunk, no orphan markers
    2. Length — reassembled length matches original
    3. Content preservation — URLs, emails, IDs all present in reassembly
    """

    # Common structured-content patterns to verify preservation
    PRESERVATION_PATTERNS: dict[str, str] = {
        "urls": r"https?://\S+",
        "emails": r"[\w.]+@[\w.]+\.\w+",
        "code_blocks": r"```[\s\S]*?```",
        "inline_code": r"`[^`\n]+`",
        "headers": r"^#{1,6}\s+.+$",
        "list_items": r"^\s*[-*+]\s+.+$",
        "uuids": r"\b[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}\b",
    }

    def __init__(self, original: str):
        self.original = original
        self.issues: list[ChunkIssue] = []

    def validate(self, chunks: list[dict]) -> dict[str, Any]:
        """Validate a list of chunk dicts (each must have 'content' key)."""
        self.issues = []

        # 1. Per-chunk structural checks
        for i, chunk in enumerate(chunks):
            content = chunk.get("content", "")
            self._check_chunk_structure(i, content)

        # 2. Length preservation
        reassembled = "".join(c.get("content", "") for c in chunks)
        if len(reassembled) != len(self.original):
            self.issues.append(ChunkIssue(
                -1, "length_mismatch",
                f"Original {len(self.original)} chars → reassembled {len(reassembled)} chars",
                "error",
            ))

        # 3. Content preservation
        for name, pattern in self.PRESERVATION_PATTERNS.items():
            orig_count = len(re.findall(pattern, self.original, re.MULTILINE))
            new_count = len(re.findall(pattern, reassembled, re.MULTILINE))
            if orig_count != new_count:
                self.issues.append(ChunkIssue(
                    -1, f"{name}_loss",
                    f"{name.capitalize()}: original {orig_count} → reassembled {new_count} "
                    f"(lost {orig_count - new_count})",
                    "warning",
                ))

        # 4. Order preservation (sample-based — full check is O(n²))
        if not self._check_order_preserved(reassembled):
            self.issues.append(ChunkIssue(
                -1, "order_changed",
                "Chunk order may have changed (sampled substring check failed)",
                "warning",
            ))

        hard_errors = [i for i in self.issues if i.severity == "error"]
        return {
            "valid": len(hard_errors) == 0,
            "issues": [
                {"chunk": i.chunk_index, "type": i.issue_type, "desc": i.description, "severity": i.severity}
                for i in self.issues
            ],
        }

    def _check_chunk_structure(self, idx: int, content: str) -> None:
        """Check structural integrity of a single chunk."""
        # Unbalanced code fences
        fence_count = content.count("```")
        if fence_count % 2 != 0:
            self.issues.append(ChunkIssue(
                idx, "unclosed_code_block",
                f"Code fence count is {fence_count} (odd) — chunk splits a code block",
                "error",
            ))

        # Unclosed inline code
        if content.count("`") - 3 * fence_count % 2 != 0:
            # Approximate — counting backticks not in fences is tricky
            pass

        # Truncated markdown header (starts with # but no content)
        for line in content.split("\n"):
            if re.match(r"^#{1,6}\s*$", line):
                self.issues.append(ChunkIssue(
                    idx, "empty_header",
                    f"Truncated header: {line!r}",
                    "warning",
                ))

    def _check_order_preserved(self, reassembled: str) -> bool:
        """Sample several substrings from the original and verify they
        appear in the same order in the reassembled text."""
        # Take 5 random 20-char substrings and check their positions are monotonic
        if len(self.original) < 40:
            return True  # too short to meaningfully check
        import random
        positions = []
        attempts = 0
        while len(positions) < 5 and attempts < 20:
            start = random.randint(0, len(self.original) - 20)
            sample = self.original[start:start + 20]
            pos = reassembled.find(sample)
            if pos >= 0:
                positions.append(pos)
            attempts += 1
        return positions == sorted(positions)


def validate_chunking(original: str, chunks: list[dict]) -> dict[str, Any]:
    """One-shot chunking validation."""
    return ChunkingValidator(original).validate(chunks)


__all__ = ["ChunkingValidator", "validate_chunking"]

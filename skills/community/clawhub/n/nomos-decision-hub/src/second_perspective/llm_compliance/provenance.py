"""Provenance tracking — every LLM output carries its origin.

Invariant L-3: all LLM output must be accompanied by provenance that records
the model, timestamp, and prompt fingerprint, so any downstream consumer
can verify where the output came from and reproduce it (to the extent the
model is deterministic).
"""

from __future__ import annotations

import hashlib
import time
from dataclasses import dataclass, field


def make_prompt_fingerprint(prompt_text: str) -> str:
    """Deterministic SHA-256 fingerprint of a prompt string.

    Used in provenance to link output to the exact prompt that produced it.
    Normalizes line endings before hashing for cross-platform stability.
    """
    normalized = prompt_text.replace("\r\n", "\n").replace("\r", "\n")
    return hashlib.sha256(normalized.encode("utf-8")).hexdigest()


@dataclass(frozen=True)
class Provenance:
    """Origin record for a piece of LLM-generated content.

    Fields
    ------
    model : str
        Model identifier, e.g. "gpt-4o-2024-05-13" or "qwen2.5-72b-instruct".
    timestamp : float
        Unix timestamp (seconds) of when the call was made.
    prompt_fingerprint : str
        SHA-256 hex digest of the prompt text (see make_prompt_fingerprint).
    endpoint : str
        Optional: which API endpoint or provider was used.
    call_id : str
        Optional: opaque identifier for tracing the specific API call.
    """

    model: str
    timestamp: float = field(default_factory=time.time)
    prompt_fingerprint: str = ""
    endpoint: str = ""
    call_id: str = ""

    def __post_init__(self) -> None:
        if not self.model:
            raise ValueError("Provenance.model must not be empty")

    @property
    def short_fingerprint(self) -> str:
        """First 12 hex chars of the prompt fingerprint for display."""
        return self.prompt_fingerprint[:12] if self.prompt_fingerprint else ""

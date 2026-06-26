"""
NIMA Core Type Definitions
============================
Typed dataclasses for memory nodes, LLM config, and precognition results.

Author: Lilu
Date: 2026-03-20
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Optional, Dict, Any, List


@dataclass
class MemoryNode:
    """
    Represents a memory node in LadybugDB or SQLite.

    Used in: ladybug_store.py, darwinism.py, precognition.py
    """

    id: int
    timestamp: int
    layer: str  # 'input', 'contemplation', 'output'
    text: str
    summary: str
    who: str
    affect_json: str
    session_key: str
    conversation_id: str
    turn_id: str
    fe_score: float

    # Optional fields (not always present)
    embedding: Optional[bytes] = None
    strength: Optional[float] = None
    themes: Optional[str] = None  # JSON string
    is_ghost: bool = False
    last_accessed: Optional[int] = None

    @classmethod
    def from_dict(cls, d: Dict[str, Any]) -> "MemoryNode":
        """
        Create MemoryNode from dict, for backward compatibility.

        Args:
            d: Dict with memory node fields

        Returns:
            MemoryNode instance
        """
        return cls(
            id=d.get("id", 0),
            timestamp=d.get("timestamp", 0),
            layer=d.get("layer", ""),
            text=d.get("text", ""),
            summary=d.get("summary", ""),
            who=d.get("who", "unknown"),
            affect_json=d.get("affect_json", "{}"),
            session_key=d.get("session_key", ""),
            conversation_id=d.get("conversation_id", ""),
            turn_id=d.get("turn_id", ""),
            fe_score=d.get("fe_score", 0.5),
            embedding=d.get("embedding"),
            strength=d.get("strength"),
            themes=d.get("themes"),
            is_ghost=d.get("is_ghost", False),
            last_accessed=d.get("last_accessed"),
        )


@dataclass
class LLMConfig:
    """
    LLM provider configuration from llm_client.py get_llm_config().

    Used in: llm_client.py, darwinism.py, precognition.py
    """

    provider: str  # 'openai-compatible', 'anthropic', 'openai'
    base_url: str
    model: str
    key: str
    headers: Dict[str, str]
    endpoint: str
    response_path: List[str]  # Path to navigate JSON response

    def __repr__(self) -> str:
        return (
            f"LLMConfig(provider={self.provider!r}, model={self.model!r}, "
            f"key='***', base_url={self.base_url!r})"
        )

    @classmethod
    def from_dict(cls, d: Dict[str, Any]) -> "LLMConfig":
        """
        Create LLMConfig from dict, for backward compatibility.

        Args:
            d: Dict with LLM config fields

        Returns:
            LLMConfig instance
        """
        return cls(
            provider=d.get("provider", ""),
            base_url=d.get("base_url", ""),
            model=d.get("model", ""),
            key=d.get("key", ""),
            headers=d.get("headers") or {},
            endpoint=d.get("endpoint", ""),
            response_path=d.get("response_path", []),
        )


@dataclass
class PrecognitionResult:
    """
    Precognition/prediction result from pattern mining.

    Used in: precognition.py mine_patterns() and generate_precognitions()
    """

    # From pattern mining
    bucket: Optional[str] = None  # e.g. "Monday_14"
    frequency: Optional[int] = None
    common_who: List[str] = field(default_factory=list)
    common_themes: List[str] = field(default_factory=list)
    sample_memories: List[str] = field(default_factory=list)
    confidence: float = 0.5

    # From LLM prediction generation
    what: Optional[str] = None
    who: Optional[str] = None
    when_predicted: Optional[str] = None  # ISO timestamp
    predicted_affect: Dict[str, Any] = field(default_factory=dict)
    source_pattern: Optional[str] = None

    # From storage
    id: Optional[int] = None
    pattern_hash: Optional[str] = None
    status: str = "pending"
    matched_memory_id: Optional[int] = None
    similarity_score: Optional[float] = None
    generated_at: Optional[str] = None
    expires_at: Optional[str] = None
    embedding: Optional[bytes] = None

    @classmethod
    def from_dict(cls, d: Dict[str, Any]) -> "PrecognitionResult":
        """
        Create PrecognitionResult from dict, for backward compatibility.

        Args:
            d: Dict with precognition fields

        Returns:
            PrecognitionResult instance
        """
        return cls(
            bucket=d.get("bucket"),
            frequency=d.get("frequency"),
            common_who=d.get("common_who", []),
            common_themes=d.get("common_themes", []),
            sample_memories=d.get("sample_memories", []),
            confidence=d.get("confidence", 0.5),
            what=d.get("what"),
            who=d.get("who"),
            when_predicted=d.get("when_predicted"),
            predicted_affect=d.get("predicted_affect", {}),
            source_pattern=d.get("source_pattern"),
            id=d.get("id"),
            pattern_hash=d.get("pattern_hash"),
            status=d.get("status", "pending"),
            matched_memory_id=d.get("matched_memory_id"),
            similarity_score=d.get("similarity_score"),
            generated_at=d.get("generated_at"),
            expires_at=d.get("expires_at"),
            embedding=d.get("embedding"),
        )


__all__ = [
    "LLMConfig",
    "MemoryNode",
    "PrecognitionResult",
]

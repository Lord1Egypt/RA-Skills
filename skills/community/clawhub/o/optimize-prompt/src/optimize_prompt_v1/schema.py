from __future__ import annotations

from dataclasses import asdict, dataclass, field
from typing import Any, Literal

Mode = Literal["passthrough", "optimized", "conservative"]
ScoreStatus = Literal["scored", "not_scored", "invalid"]
ConfidenceStatus = Literal["valid", "invalid", "not_available"]


@dataclass
class PromptIR:
    """Audit ledger only. Items should be grounded in the original prompt."""

    actions: list[str] = field(default_factory=list)
    entities: list[str] = field(default_factory=list)
    constraints: list[str] = field(default_factory=list)
    outputs: list[str] = field(default_factory=list)
    ambiguities: list[str] = field(default_factory=list)
    risk_flags: list[str] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass
class ValidationReport:
    valid: bool
    missing_literals: list[str] = field(default_factory=list)
    unsupported_additions: list[str] = field(default_factory=list)
    ir_untraceable_items: list[str] = field(default_factory=list)
    prompt_ir_mismatches: list[str] = field(default_factory=list)
    negation_scope_mismatches: list[str] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass
class OptimizationResult:
    version: str
    mode: Mode
    optimized_prompt: str
    prompt_ir: dict[str, Any]
    confidence: float
    confidence_status: ConfidenceStatus
    original_prompt_score: int | None
    score_status: ScoreStatus
    score_reasons: list[str]
    score_feedback: dict[str, list[str]]
    score_unavailable_reason: str
    validation_failed: bool
    validation: dict[str, Any]
    warnings: list[str]
    original_tokens: int
    optimized_tokens: int
    compression_ratio: float
    gate_reason: str = ""
    fallback_reason: str = ""
    conservative_reason: str = ""

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)

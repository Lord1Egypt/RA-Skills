from __future__ import annotations

from collections import Counter
from dataclasses import dataclass, field

from .schema import OptimizationResult


@dataclass
class MetricsCollector:
    requests: int = 0
    original_tokens: int = 0
    optimized_tokens: int = 0
    compression_ratio_sum: float = 0.0
    confidence_sum: float = 0.0
    score_sum: int = 0
    scored_requests: int = 0
    mode_counts: Counter = field(default_factory=Counter)
    validation_failures: int = 0
    fallbacks: int = 0

    def record(self, result: OptimizationResult) -> None:
        self.requests += 1
        self.original_tokens += result.original_tokens
        self.optimized_tokens += result.optimized_tokens
        self.compression_ratio_sum += result.compression_ratio
        self.confidence_sum += result.confidence
        if result.original_prompt_score is not None:
            self.score_sum += result.original_prompt_score
            self.scored_requests += 1
        self.mode_counts[result.mode] += 1
        self.validation_failures += int(result.validation_failed)
        self.fallbacks += int(bool(result.fallback_reason))

    def snapshot(self) -> dict:
        return {
            "original_tokens": self.original_tokens,
            "optimized_tokens": self.optimized_tokens,
            "mode_distribution": dict(self.mode_counts),
            "average_compression_ratio": self.compression_ratio_sum / self.requests if self.requests else 0,
            "average_confidence": self.confidence_sum / self.requests if self.requests else 0,
            "average_original_prompt_score": self.score_sum / self.scored_requests if self.scored_requests else None,
            "validation_failure_rate": self.validation_failures / self.requests if self.requests else 0,
            "fallback_rate": self.fallbacks / self.requests if self.requests else 0,
        }

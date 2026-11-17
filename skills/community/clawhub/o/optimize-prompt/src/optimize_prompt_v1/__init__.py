from __future__ import annotations

from .metrics import MetricsCollector
from .model import InvalidModelResponse, ModelOptimization, RetryableModelError
from .optimizer import ApproximateTokenCounter, OptimizerConfig, PromptOptimizer, TokenCounter
from .schema import OptimizationResult, PromptIR, ValidationReport
from .validator import DeterministicValidator


def optimize_prompt_v1(prompt: str, *, config: OptimizerConfig | None = None, model=None, metrics: MetricsCollector | None = None) -> dict:
    """Optimize a user prompt into an auditable downstream-agent instruction."""
    return PromptOptimizer(config=config, model=model, metrics=metrics).optimize(prompt).to_dict()


__all__ = ["ApproximateTokenCounter", "DeterministicValidator", "InvalidModelResponse", "MetricsCollector", "ModelOptimization", "OptimizationResult", "OptimizerConfig", "PromptIR", "PromptOptimizer", "RetryableModelError", "TokenCounter", "ValidationReport", "optimize_prompt_v1"]

from __future__ import annotations

from dataclasses import dataclass
from typing import Protocol

from .schema import Mode, PromptIR


class RetryableModelError(RuntimeError):
    """Timeout, rate limit, or transient transport failure."""


class InvalidModelResponse(ValueError):
    """Non-retryable model response contract violation."""


@dataclass
class ModelOptimization:
    mode: Mode
    optimized_prompt: str
    prompt_ir: PromptIR
    confidence: float
    original_prompt_score: int | None = None
    score_reasons: list[str] | None = None
    score_strengths: list[str] | None = None
    score_improvements: list[str] | None = None


class ModelAdapter(Protocol):
    """Low-cost, vendor-neutral one-shot optimizer."""

    def optimize(self, prompt: str) -> ModelOptimization:
        """Route, rewrite, and create the audit IR in one model call."""
        ...


OPTIMIZER_SYSTEM_PROMPT = """You are a lossless prompt optimization gateway.
Return mode, optimized_prompt, prompt_ir, confidence, original_prompt_score,
score_strengths, and score_improvements as structured output.
Modes: passthrough, optimized, conservative.
Never infer missing parameters or strengthen tentative language.
Score the original prompt from 0 to 100 for expression quality only: clarity,
constraint completeness, and conciseness. The score is not a safety rating or
execution permission. Give up to 3 short strengths and up to 3 actionable
improvements grounded in the input. These fields are educational UI feedback.
Every IR item must be a verbatim or directly traceable fragment of the original.
Every execution-affecting atom in optimized_prompt must be represented in IR.
Preserve negations, permissions, numbers, dates, amounts, percentages, URLs,
file/function names, output format/language, attachment references, and risk limits.
Use conservative when ambiguity, conflict, or risky execution could mislead.
IR schema: actions, entities, constraints, outputs, ambiguities, risk_flags.
Prompt IR is an audit ledger; optimized_prompt is the downstream instruction."""

from __future__ import annotations

import json
import re
import time
from dataclasses import dataclass
from typing import Protocol

from .metrics import MetricsCollector
from .model import InvalidModelResponse, ModelAdapter, RetryableModelError
from .schema import OptimizationResult, PromptIR, ValidationReport
from .validator import DeterministicValidator


class TokenCounter(Protocol):
    def count(self, text: str) -> int: ...


class ApproximateTokenCounter:
    """Replace with the provider tokenizer in production for exact accounting."""

    def count(self, text: str) -> int:
        return max(1, len(re.findall(r"[\u4e00-\u9fff]|[A-Za-z0-9_.-]+|[^\s]", text)))


@dataclass(frozen=True)
class OptimizerConfig:
    min_chars_for_model: int = 20
    min_tokens_for_model: int = 12
    base64_min_length: int = 256
    code_block_min_chars: int = 200
    code_block_dominance_ratio: float = 0.7
    structured_xml_tags: tuple[str, ...] = (
        "context",
        "user_query",
        "tool_call",
        "tool_result",
        "function_call",
        "arguments",
        "mcp_context",
        "resource",
    )
    machine_instruction_prefixes: tuple[str, ...] = ("tool:", "function:", "mcp:", "/")
    max_model_attempts: int = 3
    retry_backoff_seconds: float = 0.0


class PromptOptimizer:
    def __init__(self, config: OptimizerConfig | None = None, model: ModelAdapter | None = None, metrics: MetricsCollector | None = None, tokenizer: TokenCounter | None = None, validator: DeterministicValidator | None = None):
        self.config = config or OptimizerConfig()
        self.model = model
        self.metrics = metrics or MetricsCollector()
        self.tokenizer = tokenizer or ApproximateTokenCounter()
        self.validator = validator or DeterministicValidator()

    def optimize(self, prompt: str) -> OptimizationResult:
        if not isinstance(prompt, str) or not prompt.strip():
            raise ValueError("prompt must be a non-empty string")
        original = prompt.strip()
        original_tokens = self.tokenizer.count(original)
        gate_reason = self._gate_reason(original, original_tokens)
        if gate_reason or self.model is None:
            reason = gate_reason or "model_unavailable"
            result = self._result(original, "passthrough", original, PromptIR(), 1.0, "not_available", None, [], {"strengths": [], "improvements": []}, self._score_unavailable_reason(reason), ValidationReport(True), reason, "", "", [])
            self.metrics.record(result)
            return result

        try:
            response = self._call_model(original)
            self._validate_model_response(response)
        except InvalidModelResponse as exc:
            return self._fallback_from_model_error(original, "invalid_model_response", str(exc))
        except Exception as exc:
            return self._fallback_from_model_error(original, "model_error", str(exc))
        candidate = response.optimized_prompt.strip()
        report = self.validator.validate(original, candidate, response.prompt_ir)
        warnings: list[str] = []
        score, score_reasons = self._normalize_score(response.original_prompt_score, response.score_reasons)
        score_feedback = self._normalize_feedback(response.score_strengths, response.score_improvements)
        confidence, confidence_status = self._normalize_confidence(response.confidence)
        if confidence_status == "invalid":
            warnings.append("invalid confidence: expected a number from 0 to 1")
        if response.original_prompt_score is not None and score is None:
            warnings.append("invalid original_prompt_score: expected an integer from 0 to 100")
        if not report.valid:
            warnings.append("validation_failed: optimized prompt was rejected and original prompt restored")
            result = self._result(original, "conservative", original, response.prompt_ir, min(confidence, 0.5), confidence_status, score, score_reasons, score_feedback, "", report, "", "validation_failed", self._conservative_reason(response.prompt_ir), warnings)
        elif response.mode == "conservative":
            # Conservative is a downstream safety contract, not merely a label:
            # no model rewrite is allowed to reach the executing agent.
            result = self._result(original, "conservative", original, response.prompt_ir, confidence, confidence_status, score, score_reasons, score_feedback, "", report, "", "", self._conservative_reason(response.prompt_ir), warnings)
        else:
            result = self._result(original, response.mode, candidate, response.prompt_ir, confidence, confidence_status, score, score_reasons, score_feedback, "", report, "", "", "", warnings)
        self.metrics.record(result)
        return result

    def _gate_reason(self, prompt: str, tokens: int) -> str:
        if self._is_json(prompt):
            return "json_input"
        lowered = prompt.lstrip().lower()
        if lowered.startswith(self.config.machine_instruction_prefixes) or self._is_tool_call(prompt):
            return "machine_instruction"
        if self._contains_base64_data(prompt):
            return "contains_base64_data"
        if self._is_code_block_dominant(prompt):
            return "code_block_dominant"
        if self._contains_structured_xml(prompt):
            return "structured_xml_tags"
        if len(prompt) < self.config.min_chars_for_model or tokens < self.config.min_tokens_for_model:
            return "too_short"
        return ""

    @staticmethod
    def _is_json(prompt: str) -> bool:
        try:
            return isinstance(json.loads(prompt), (dict, list))
        except (ValueError, TypeError):
            return False

    @staticmethod
    def _is_tool_call(prompt: str) -> bool:
        return bool(re.fullmatch(r"[A-Za-z_]\w*\s*\(.*\)\s*", prompt, re.S))

    def _contains_base64_data(self, prompt: str) -> bool:
        minimum = self.config.base64_min_length
        data_uri = re.compile(
            rf"data:[\w.+-]+/[\w.+-]+(?:;[\w.+-]+=[^;,\s]+)*;base64,[A-Za-z0-9+/\s]{{{minimum},}}={{0,2}}",
            re.I,
        )
        if data_uri.search(prompt):
            return True
        bare_base64 = re.compile(rf"(?<![A-Za-z0-9+/])[A-Za-z0-9+/]{{{minimum},}}={{0,2}}(?![A-Za-z0-9+/=])")
        return bool(bare_base64.search(prompt))

    def _is_code_block_dominant(self, prompt: str) -> bool:
        blocks = re.findall(r"```[^\n`]*\n([\s\S]*?)```", prompt)
        # Treat a long unclosed final fence as pasted code too.
        if prompt.count("```") % 2:
            tail = prompt.rsplit("```", 1)[-1]
            tail = tail.split("\n", 1)[-1] if "\n" in tail else ""
            blocks.append(tail)
        code_chars = sum(len(block) for block in blocks)
        return (
            code_chars >= self.config.code_block_min_chars
            and code_chars / max(1, len(prompt)) >= self.config.code_block_dominance_ratio
        )

    def _contains_structured_xml(self, prompt: str) -> bool:
        for tag in self.config.structured_xml_tags:
            escaped = re.escape(tag)
            if re.search(rf"<{escaped}(?:\s[^>]*)?>[\s\S]*?</{escaped}\s*>", prompt, re.I):
                return True
        return False

    @staticmethod
    def _normalize_score(score: int | None, reasons: list[str] | None) -> tuple[int | None, list[str]]:
        valid_score = isinstance(score, int) and not isinstance(score, bool) and 0 <= score <= 100
        clean_reasons = [reason.strip() for reason in (reasons or []) if isinstance(reason, str) and reason.strip()][:3]
        return (score if valid_score else None), clean_reasons

    @staticmethod
    def _normalize_feedback(strengths, improvements) -> dict[str, list[str]]:
        clean = lambda values: [x.strip() for x in (values or []) if isinstance(x, str) and x.strip()][:3]
        return {"strengths": clean(strengths), "improvements": clean(improvements)}

    @staticmethod
    def _normalize_confidence(value) -> tuple[float, str]:
        if isinstance(value, (int, float)) and not isinstance(value, bool) and 0 <= value <= 1:
            return float(value), "valid"
        return 0.0, "invalid"

    def _call_model(self, original: str):
        last_error = None
        for attempt in range(max(1, self.config.max_model_attempts)):
            try:
                return self.model.optimize(original)
            except RetryableModelError as exc:
                last_error = exc
                if attempt + 1 < max(1, self.config.max_model_attempts) and self.config.retry_backoff_seconds > 0:
                    time.sleep(self.config.retry_backoff_seconds * (2 ** attempt))
        raise last_error or RetryableModelError("model retry exhausted")

    @staticmethod
    def _validate_model_response(response) -> None:
        if response is None or response.mode not in ("passthrough", "optimized", "conservative"):
            raise InvalidModelResponse("unsupported or missing mode")
        if not isinstance(response.optimized_prompt, str) or not response.optimized_prompt.strip():
            raise InvalidModelResponse("optimized_prompt must be non-empty")
        if not isinstance(response.prompt_ir, PromptIR):
            raise InvalidModelResponse("prompt_ir must be PromptIR")

    def _fallback_from_model_error(self, original: str, reason: str, detail: str) -> OptimizationResult:
        result = self._result(original, "passthrough", original, PromptIR(), 0.0, "not_available", None, [], {"strengths": [], "improvements": []}, "model_unavailable", ValidationReport(True), "", reason, "", [f"{reason}: {detail}"])
        self.metrics.record(result)
        return result

    @staticmethod
    def _score_unavailable_reason(gate_reason: str) -> str:
        if gate_reason == "too_short": return "content_too_short"
        if gate_reason in ("json_input", "machine_instruction", "structured_xml_tags"): return "machine_or_structured_input"
        if gate_reason in ("contains_base64_data", "code_block_dominant"): return "data_or_code_dominant"
        return "model_unavailable"

    @staticmethod
    def _conservative_reason(ir: PromptIR) -> str:
        if ir.risk_flags: return "risk"
        if ir.ambiguities: return "ambiguity"
        return "conflict"

    def _result(self, original: str, mode: str, optimized: str, ir: PromptIR, confidence: float, confidence_status: str, score: int | None, score_reasons: list[str], score_feedback: dict[str, list[str]], score_unavailable_reason: str, validation: ValidationReport, gate_reason: str, fallback_reason: str, conservative_reason: str, warnings: list[str]) -> OptimizationResult:
        original_tokens = self.tokenizer.count(original)
        optimized_tokens = self.tokenizer.count(optimized)
        return OptimizationResult(
            version="v1",
            mode=mode,  # type: ignore[arg-type]
            optimized_prompt=optimized,
            prompt_ir=ir.to_dict(),
            confidence=confidence,
            confidence_status=confidence_status,
            original_prompt_score=score,
            score_status="not_scored" if gate_reason else ("scored" if score is not None else "invalid"),
            score_reasons=score_reasons,
            score_feedback=score_feedback,
            score_unavailable_reason=score_unavailable_reason,
            validation_failed=not validation.valid,
            validation=validation.to_dict(),
            warnings=warnings,
            original_tokens=original_tokens,
            optimized_tokens=optimized_tokens,
            compression_ratio=max(0.0, round((original_tokens - optimized_tokens) / original_tokens, 4)),
            gate_reason=gate_reason,
            fallback_reason=fallback_reason,
            conservative_reason=conservative_reason,
        )

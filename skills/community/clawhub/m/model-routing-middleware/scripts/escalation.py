"""
Escalation Engine — Confidence detection and retry logic

Detects low-confidence responses and automatically retries
with progressively stronger models.

Escalation chain:
    Level 0: qwen3-14b (default)
    Level 1: deepseek-r1 (reasoning upgrade)
    Level 2: glm-5-1-cloud (cloud upgrade, final)

Max retries: 2


"""

from __future__ import annotations

import logging
import os
import re
from dataclasses import dataclass, field
from enum import Enum
from typing import Optional

import yaml

from router.classifiers import TaskType
from router.models import ModelRegistry, ModelInfo

logger = logging.getLogger("router.escalation")


class EscalationLevel(Enum):
    """Escalation levels for retry chain."""
    LEVEL_0 = 0  # Default model (from routing)
    LEVEL_1 = 1  # Reasoning upgrade
    LEVEL_2 = 2  # Cloud upgrade (final)


@dataclass
class EscalationResult:
    """Result of an escalation check."""
    should_escalate: bool                # Whether to retry with a stronger model
    confidence: float                    # Detected confidence (0.0 - 1.0)
    matched_patterns: list[str]         # Low-confidence patterns found
    escalation_level: EscalationLevel   # Current escalation level
    next_model_key: Optional[str]       # Model key to retry with (None if max reached)
    next_model_id: Optional[str]        # Model ID to retry with
    next_think: bool                     # Whether to enable think mode on retry
    reason: str = ""                     # Human-readable reason

    def __str__(self) -> str:
        if self.should_escalate:
            return (
                f"EscalationResult(ESCALATE level={self.escalation_level.value} → "
                f"model={self.next_model_key}, confidence={self.confidence:.2f})"
            )
        return f"EscalationResult(OK confidence={self.confidence:.2f})"


class EscalationEngine:
    """
    Detects low-confidence responses and manages retry escalation.

    Checks for low-confidence keywords in responses and escalates
    to progressively stronger models.
    """

    def __init__(self, config_path: Optional[str] = None):
        """
        Initialize escalation engine with configuration.

        Args:
            config_path: Path to config.yaml. Defaults to ./config.yaml.
        """
        if config_path is None:
            config_path = os.path.join(os.path.dirname(__file__), "config.yaml")

        self.config_path = config_path
        with open(config_path, 'r') as f:
            self.config = yaml.safe_load(f)

        self.registry = ModelRegistry(self.config)
        escalation_config = self.config.get("escalation", {})

        self.confidence_threshold = escalation_config.get("confidence_threshold", 0.7)
        self.max_retries = escalation_config.get("max_retries", 2)
        self.low_confidence_keywords = escalation_config.get("low_confidence_keywords", [])
        self.escalation_chain = escalation_config.get("escalation_chain", [])

        # Compile keyword patterns for efficient matching
        self._compiled_patterns = [
            re.compile(re.escape(kw), re.IGNORECASE)
            for kw in self.low_confidence_keywords
        ]

    def check_response(
        self,
        response_text: str,
        current_model_key: str,
        current_escalation_level: int = 0,
        task_type: Optional[TaskType] = None,
    ) -> EscalationResult:
        """
        Check if a response indicates low confidence and should be escalated.

        Args:
            response_text: The model's response text.
            current_model_key: Config key of the model that produced this response.
            current_escalation_level: Current escalation level (0, 1, or 2).
            task_type: The task type of the original request.

        Returns:
            EscalationResult with escalation decision and next model.
        """
        # Step 1: Detect low-confidence patterns
        matched_patterns = []
        response_lower = response_text.lower() if response_text else ""

        for pattern in self._compiled_patterns:
            if pattern.search(response_lower):
                # Find the original keyword that matched
                for kw in self.low_confidence_keywords:
                    if kw.lower() in response_lower:
                        matched_patterns.append(kw)

        # Deduplicate
        matched_patterns = list(dict.fromkeys(matched_patterns))

        # Step 2: Calculate confidence score
        # More patterns matched = lower confidence
        num_patterns = len(matched_patterns)
        if num_patterns == 0:
            confidence = 1.0
        elif num_patterns == 1:
            confidence = 0.5
        elif num_patterns == 2:
            confidence = 0.3
        else:
            confidence = 0.1

        # Step 3: Determine if escalation is needed
        should_escalate = (
            confidence < self.confidence_threshold
            and current_escalation_level < self.max_retries
        )

        # Step 4: Get next model in escalation chain
        next_model_key = None
        next_model_id = None
        next_think = False

        if should_escalate:
            next_level = current_escalation_level + 1
            if next_level < len(self.escalation_chain):
                next_model_key = self.escalation_chain[next_level]
                model_info = self.registry.get_model(next_model_key)
                if model_info:
                    next_model_id = model_info.model_id
                    next_think = model_info.supports_think
                else:
                    # Model not in registry, try to use key as-is
                    next_model_id = next_model_key
                    next_think = True  # Default to think mode on escalation

        # Step 5: Build reason
        reason = self._build_reason(
            should_escalate, confidence, matched_patterns,
            current_escalation_level, next_model_key,
        )

        result = EscalationResult(
            should_escalate=should_escalate,
            confidence=confidence,
            matched_patterns=matched_patterns,
            escalation_level=EscalationLevel(current_escalation_level),
            next_model_key=next_model_key,
            next_model_id=next_model_id,
            next_think=next_think,
            reason=reason,
        )

        if should_escalate:
            logger.info(
                f"ESCALATE | level={current_escalation_level} → {next_level} | "
                f"confidence={confidence:.2f} | patterns={matched_patterns} | "
                f"next_model={next_model_key}"
            )
        else:
            logger.debug(
                f"NO ESCALATE | confidence={confidence:.2f} | "
                f"level={current_escalation_level} | patterns={matched_patterns}"
            )

        return result

    def _build_reason(
        self,
        should_escalate: bool,
        confidence: float,
        matched_patterns: list[str],
        current_level: int,
        next_model: Optional[str],
    ) -> str:
        """Build a human-readable reason for the escalation decision."""
        if not should_escalate:
            if confidence >= self.confidence_threshold:
                return f"Confidence {confidence:.2f} >= threshold {self.confidence_threshold}. No escalation needed."
            else:
                return f"Confidence {confidence:.2f} < threshold {self.confidence_threshold}, but max escalation level ({self.max_retries}) reached. No further escalation."

        return (
            f"Confidence {confidence:.2f} < threshold {self.confidence_threshold}. "
            f"Low-confidence patterns: {matched_patterns}. "
            f"Escalating from level {current_level} to model '{next_model}'."
        )


def check_escalation(
    response_text: str,
    current_model_key: str = "qwen3-14b",
    current_level: int = 0,
    config_path: Optional[str] = None,
) -> EscalationResult:
    """
    Convenience function to check if a response should be escalated.

    Args:
        response_text: The model's response text.
        current_model_key: Config key of the model that produced this response.
        current_level: Current escalation level (0, 1, or 2).
        config_path: Path to config.yaml.

    Returns:
        EscalationResult with escalation decision.
    """
    engine = EscalationEngine(config_path=config_path)
    return engine.check_response(response_text, current_model_key, current_level)
#!/usr/bin/env python3
"""Dependency-free temperature scaling for Jev-compatible distributions.

This module deliberately works on the typed probabilities already returned by a
provider. It does not pretend to recover hidden logits. Use a calibration split
from the same provider/model and keep the resulting profile tied to that
deployment. Applying a profile fitted on another model or domain is not valid.
"""

from __future__ import annotations

import copy
import json
import math
from pathlib import Path
from typing import Any, Iterable


PROFILE_SCHEMA = "jev-calibration-v1"
EPSILON = 1e-12


class CalibrationError(ValueError):
    """A malformed calibration profile or an impossible fit input."""


def _finite(value: Any, label: str) -> float:
    if isinstance(value, bool) or not isinstance(value, (int, float)) or not math.isfinite(float(value)):
        raise CalibrationError(f"{label} must be a finite number")
    return float(value)


def _positive_temperature(value: Any, label: str = "temperature") -> float:
    temperature = _finite(value, label)
    if temperature <= 0:
        raise CalibrationError(f"{label} must be greater than zero")
    return temperature


def _logit(probability: float) -> float:
    clipped = min(1.0 - EPSILON, max(EPSILON, probability))
    return math.log(clipped / (1.0 - clipped))


def _sigmoid(value: float) -> float:
    if value >= 0:
        inverse = math.exp(-value)
        return 1.0 / (1.0 + inverse)
    exponential = math.exp(value)
    return exponential / (1.0 + exponential)


def scale_binary_probability(probability: Any, temperature: Any) -> float:
    """Apply binary temperature scaling to a probability in ``[0, 1]``."""

    value = _finite(probability, "probability")
    if not 0 <= value <= 1:
        raise CalibrationError("probability must be between 0 and 1")
    temp = _positive_temperature(temperature)
    return _sigmoid(_logit(value) / temp)


def scale_distribution(probabilities: dict[str, Any], temperature: Any) -> dict[str, float]:
    """Apply multiclass temperature scaling and renormalize the distribution."""

    if not isinstance(probabilities, dict) or not probabilities:
        raise CalibrationError("probabilities must be a non-empty object")
    temp = _positive_temperature(temperature)
    values = {str(key): _finite(value, f"probability {key!r}") for key, value in probabilities.items()}
    if any(value < 0 for value in values.values()):
        raise CalibrationError("probabilities cannot be negative")
    total = math.fsum(values.values())
    if not math.isfinite(total) or total <= 0:
        raise CalibrationError("probabilities must have a positive finite sum")

    # Work in log space so a very small temperature cannot overflow p ** (1/T).
    log_weights = {
        key: (math.log(max(EPSILON, value / total)) / temp)
        for key, value in values.items()
    }
    maximum = max(log_weights.values())
    weights = {key: math.exp(value - maximum) for key, value in log_weights.items()}
    weight_total = math.fsum(weights.values())
    if not math.isfinite(weight_total) or weight_total <= 0:
        raise CalibrationError("temperature scaling produced an invalid distribution")
    return {key: weight / weight_total for key, weight in weights.items()}


def _sample_nll(sample: dict[str, Any], temperature: float) -> float:
    kind = sample.get("kind")
    if kind == "binary":
        probability = scale_binary_probability(sample["probability"], temperature)
        label = bool(sample["label"])
        return -math.log(max(EPSILON, probability if label else 1.0 - probability))
    if kind == "categorical":
        distribution = scale_distribution(sample["probabilities"], temperature)
        label = str(sample["label"])
        if label not in distribution:
            raise CalibrationError(f"categorical label {label!r} is not in the probability support")
        return -math.log(max(EPSILON, distribution[label]))
    raise CalibrationError(f"unknown calibration sample kind {kind!r}")


def negative_log_likelihood(samples: Iterable[dict[str, Any]], temperature: Any) -> float:
    """Return mean NLL for binary or categorical calibration samples."""

    rows = list(samples)
    if not rows:
        raise CalibrationError("at least one calibration sample is required")
    temp = _positive_temperature(temperature)
    losses = [_sample_nll(row, temp) for row in rows]
    return math.fsum(losses) / len(losses)


def fit_temperature(
    samples: Iterable[dict[str, Any]],
    *,
    minimum: float = 0.05,
    maximum: float = 20.0,
    iterations: int = 80,
) -> float:
    """Fit one temperature by deterministic golden-section search in log space."""

    rows = list(samples)
    if not rows:
        raise CalibrationError("at least one calibration sample is required")
    minimum = _positive_temperature(minimum, "minimum")
    maximum = _positive_temperature(maximum, "maximum")
    if maximum <= minimum:
        raise CalibrationError("maximum temperature must be greater than minimum")
    if iterations < 1:
        raise CalibrationError("iterations must be positive")

    lower = math.log(minimum)
    upper = math.log(maximum)
    golden = (math.sqrt(5.0) - 1.0) / 2.0

    def objective(log_temperature: float) -> float:
        return negative_log_likelihood(rows, math.exp(log_temperature))

    left = upper - golden * (upper - lower)
    right = lower + golden * (upper - lower)
    left_value = objective(left)
    right_value = objective(right)
    for _ in range(iterations):
        if left_value < right_value:
            upper, right, right_value = right, left, left_value
            left = upper - golden * (upper - lower)
            left_value = objective(left)
        else:
            lower, left, left_value = left, right, right_value
            right = lower + golden * (upper - lower)
            right_value = objective(right)
    fitted = math.exp((lower + upper) / 2.0)
    # Keep profile output stable and avoid tiny optimizer noise in git/CI.
    return round(fitted, 8)


def validate_profile(profile: Any) -> dict[str, Any]:
    """Validate and copy a calibration profile before it touches a response."""

    if not isinstance(profile, dict):
        raise CalibrationError("calibration profile must be an object")
    if profile.get("schema_version") != PROFILE_SCHEMA:
        raise CalibrationError(f"calibration profile schema_version must be {PROFILE_SCHEMA!r}")
    temperatures = profile.get("temperatures", {})
    if not isinstance(temperatures, dict):
        raise CalibrationError("calibration profile temperatures must be an object")
    normalized = copy.deepcopy(profile)
    normalized["temperatures"] = {
        str(key): _positive_temperature(value, f"temperature for {key!r}")
        for key, value in temperatures.items()
    }
    by_question = profile.get("by_question", {})
    if by_question is not None:
        if not isinstance(by_question, dict):
            raise CalibrationError("calibration profile by_question must be an object")
        normalized["by_question"] = {}
        for question_id, question_profile in by_question.items():
            if not isinstance(question_profile, dict):
                raise CalibrationError(f"calibration profile for {question_id!r} must be an object")
            normalized["by_question"][str(question_id)] = {
                str(key): _positive_temperature(value, f"temperature for {question_id!r}/{key!r}")
                for key, value in question_profile.items()
            }
    else:
        normalized["by_question"] = {}
    return normalized


def _temperature_for(profile: dict[str, Any], question_id: str, question_type: str) -> float | None:
    question_profile = profile.get("by_question", {}).get(question_id, {})
    if isinstance(question_profile, dict) and question_type in question_profile:
        return float(question_profile[question_type])
    value = profile.get("temperatures", {}).get(question_type)
    return float(value) if value is not None else None


def apply_calibration_profile(
    response: dict[str, Any],
    questions: dict[str, dict[str, Any]],
    profile: dict[str, Any],
) -> tuple[dict[str, Any], list[str]]:
    """Return a calibrated response and warnings describing applied scalers."""

    checked = validate_profile(profile)
    calibrated = copy.deepcopy(response)
    answers = calibrated.get("answers")
    if not isinstance(answers, dict):
        raise CalibrationError("response is missing answers")
    applied: dict[str, float] = {}
    for question_id, question in questions.items():
        temperature = _temperature_for(checked, question_id, question["type"])
        if temperature is None or abs(temperature - 1.0) < 1e-10:
            continue
        answer = answers.get(question_id)
        if not isinstance(answer, dict):
            raise CalibrationError(f"response answer {question_id!r} is not an object")
        if question["type"] == "noul":
            answer["noul"] = scale_binary_probability(answer.get("noul"), temperature)
        elif question["type"] in {"choice", "score"}:
            answer["probabilities"] = scale_distribution(answer.get("probabilities"), temperature)
            if question["type"] == "choice":
                keys = list(question["criteria"])
                answer["choice"] = max(keys, key=lambda key: (answer["probabilities"][key], -keys.index(key)))
                answer["confidence"] = max(answer["probabilities"].values())
            else:
                answer["score"] = sum(float(key) * answer["probabilities"][key] for key in answer["probabilities"])
                answer["confidence"] = max(answer["probabilities"].values())
        applied[question_id] = temperature
    if applied:
        calibrated["calibration"] = {
            "schema_version": PROFILE_SCHEMA,
            "applied": applied,
            "profile_id": checked.get("profile_id"),
        }
    return calibrated, [
        f"temperature scaling applied to {len(applied)} question(s)"
    ] if applied else []


def load_profile(path: Path) -> dict[str, Any]:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError as exc:
        raise CalibrationError(f"calibration profile not found: {path}") from exc
    except json.JSONDecodeError as exc:
        raise CalibrationError(f"invalid calibration profile JSON: {exc}") from exc
    return validate_profile(value)

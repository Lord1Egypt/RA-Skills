#!/usr/bin/env python3
"""Dependency-free control-plane policies for consuming Jev answers.

The model supplies typed evidence; these functions turn that evidence into a
reviewable application decision. They never call a model, execute a tool, or
grant authorization. Keep authorization, allowlists, and side-effect policy
in the caller.
"""

from __future__ import annotations

import math
from typing import Any, Mapping


CONTROL_VERSION = "1.0.0"
DEFAULT_ROUTE_CONFIDENCE = 0.80
DEFAULT_ROUTE_MARGIN = 0.10
DEFAULT_RISK_THRESHOLD = 0.50
DEFAULT_JUDGE_ACCEPT_THRESHOLD = 0.80
DEFAULT_JUDGE_REVIEW_THRESHOLD = 0.50


class ControlInputError(ValueError):
    """Raised when a typed answer or policy definition is unsafe to consume."""


def _finite_probability(value: Any, label: str) -> float:
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise ControlInputError(f"{label} must be a number between 0 and 1")
    numeric = float(value)
    if not math.isfinite(numeric) or not 0.0 <= numeric <= 1.0:
        raise ControlInputError(f"{label} must be a number between 0 and 1")
    return numeric


def _threshold(value: Any, label: str) -> float:
    return _finite_probability(value, label)


def _answer(response_or_answer: Mapping[str, Any], question_id: str | None) -> Mapping[str, Any]:
    if not isinstance(response_or_answer, Mapping):
        raise ControlInputError("typed response must be an object")
    if question_id is None:
        answer = response_or_answer
    else:
        answers = response_or_answer.get("answers")
        if not isinstance(answers, Mapping) or question_id not in answers:
            raise ControlInputError(f"typed response is missing answer {question_id!r}")
        answer = answers[question_id]
    if not isinstance(answer, Mapping):
        raise ControlInputError("typed answer must be an object")
    return answer


def _probabilities(answer: Mapping[str, Any], label: str) -> dict[str, float]:
    raw = answer.get("probabilities")
    if not isinstance(raw, Mapping) or not raw:
        raise ControlInputError(f"{label}.probabilities must be a non-empty object")
    probabilities = {str(key): _finite_probability(value, f"{label}.probabilities[{key!r}]") for key, value in raw.items()}
    total = sum(probabilities.values())
    if not math.isclose(total, 1.0, rel_tol=1e-6, abs_tol=1e-6):
        raise ControlInputError(f"{label}.probabilities must sum to 1 (got {total:.6f})")
    return probabilities


def route_choice(
    response_or_answer: Mapping[str, Any],
    routes: Mapping[str, str],
    *,
    question_id: str | None = None,
    min_confidence: float = DEFAULT_ROUTE_CONFIDENCE,
    min_margin: float = DEFAULT_ROUTE_MARGIN,
    fallback: str = "review",
) -> dict[str, Any]:
    """Choose a route only when the Choice distribution clears two gates.

    The decision uses the probability distribution, not a self-reported
    ``confidence`` field. A high top probability with a close runner-up is
    treated as ambiguous and sent to ``fallback``.
    """

    min_confidence = _threshold(min_confidence, "min_confidence")
    min_margin = _threshold(min_margin, "min_margin")
    if not isinstance(routes, Mapping) or not routes or any(not isinstance(key, str) or not key.strip() for key in routes):
        raise ControlInputError("routes must be a non-empty mapping with string keys")
    if not isinstance(fallback, str) or not fallback.strip():
        raise ControlInputError("fallback must be a non-empty string")
    answer = _answer(response_or_answer, question_id)
    if answer.get("type") != "choice":
        raise ControlInputError("routing requires a Choice answer")
    choice = answer.get("choice")
    if not isinstance(choice, str) or not choice.strip():
        raise ControlInputError("Choice answer must include a non-empty choice")
    probabilities = _probabilities(answer, "choice")
    if choice not in probabilities:
        raise ControlInputError("Choice answer is not present in its probability distribution")
    ranked = sorted(probabilities.items(), key=lambda item: (-item[1], item[0]))
    top_choice, top_probability = ranked[0]
    runner_up = ranked[1][1] if len(ranked) > 1 else 0.0
    margin = top_probability - runner_up
    reasons: list[str] = []
    if top_choice != choice:
        reasons.append("selected choice is not the most probable option")
    if top_probability < min_confidence:
        reasons.append(f"top probability {top_probability:.3f} is below {min_confidence:.3f}")
    if margin < min_margin:
        reasons.append(f"probability margin {margin:.3f} is below {min_margin:.3f}")
    if choice not in routes:
        reasons.append("selected choice has no application route")
    accepted = not reasons
    return {
        "status": "route" if accepted else "review",
        "route": routes[choice] if accepted else fallback,
        "choice": choice,
        "top_choice": top_choice,
        "confidence": round(top_probability, 6),
        "margin": round(margin, 6),
        "thresholds": {"min_confidence": min_confidence, "min_margin": min_margin},
        "reasons": reasons or ["choice cleared confidence and margin gates"],
    }


def assess_tool_call(
    tool_name: str,
    response_or_answer: Mapping[str, Any] | None,
    *,
    protected_tools: set[str] | list[str] | tuple[str, ...],
    authorized: bool = False,
    question_id: str | None = None,
    risk_threshold: float = DEFAULT_RISK_THRESHOLD,
    unlisted_policy: str = "review",
    classifier_error: str | None = None,
) -> dict[str, Any]:
    """Return a fail-closed risk recommendation for a proposed tool call.

    ``authorized`` must come from deterministic application policy. A low Jev
    risk probability is never authorization. Unknown/unlisted tools default to
    review, while classifier errors on protected tools default to block.
    """

    if not isinstance(tool_name, str) or not tool_name.strip():
        raise ControlInputError("tool_name must be a non-empty string")
    if not isinstance(protected_tools, (set, list, tuple)):
        raise ControlInputError("protected_tools must be a set, list, or tuple")
    protected = tool_name in protected_tools
    risk_threshold = _threshold(risk_threshold, "risk_threshold")
    if unlisted_policy not in {"allow", "review", "block"}:
        raise ControlInputError("unlisted_policy must be allow, review, or block")

    base = {
        "tool": tool_name,
        "protected": protected,
        "risk_threshold": risk_threshold,
        "authorized": bool(authorized),
        "risk_probability": None,
    }
    if not protected:
        decision = unlisted_policy
        if decision == "allow" and not authorized:
            decision = "review"
        return {**base, "decision": decision, "reason": "tool is not in the protected-tool policy"}
    if classifier_error:
        return {
            **base,
            "decision": "block",
            "reason": "protected tool blocked because the classifier failed",
            "error": str(classifier_error),
        }
    try:
        answer = _answer(response_or_answer or {}, question_id)
        if answer.get("type") != "noul":
            raise ControlInputError("tool-risk assessment requires a Noul answer")
        risk_probability = _finite_probability(answer.get("noul"), "risk answer.noul")
    except (ControlInputError, TypeError, AttributeError) as exc:
        return {
            **base,
            "decision": "block",
            "reason": "protected tool blocked because the risk answer was invalid",
            "error": str(exc),
        }
    base["risk_probability"] = round(risk_probability, 6)
    if risk_probability >= risk_threshold:
        return {**base, "decision": "block", "reason": "risk probability meets or exceeds the block threshold"}
    if not authorized:
        return {**base, "decision": "review", "reason": "risk is below threshold but deterministic authorization is missing"}
    return {**base, "decision": "allow", "reason": "risk is below threshold and deterministic authorization is present"}


def _criterion_result(
    question_id: str,
    answer: Mapping[str, Any],
    rubric: Mapping[str, Any],
) -> dict[str, Any]:
    question_type = rubric.get("type", answer.get("type"))
    threshold = _threshold(rubric.get("threshold", 0.8), f"rubric[{question_id!r}].threshold")
    weight = rubric.get("weight", 1.0)
    if isinstance(weight, bool) or not isinstance(weight, (int, float)) or not math.isfinite(float(weight)) or float(weight) <= 0:
        raise ControlInputError(f"rubric[{question_id!r}].weight must be a positive number")
    weight = float(weight)
    if answer.get("type") != question_type:
        raise ControlInputError(f"answer {question_id!r} type does not match its rubric")

    if question_type == "noul":
        score = _finite_probability(answer.get("noul"), f"answer[{question_id!r}].noul")
        passed = score >= threshold
        reason = f"yes probability {score:.3f} {'meets' if passed else 'misses'} threshold {threshold:.3f}"
    elif question_type == "choice":
        expected = rubric.get("expected")
        if not isinstance(expected, str) or not expected:
            raise ControlInputError(f"rubric[{question_id!r}] choice criteria needs an expected option")
        probabilities = _probabilities(answer, f"answer[{question_id!r}]")
        if expected not in probabilities:
            raise ControlInputError(f"rubric[{question_id!r}] expected option is absent from probabilities")
        score = probabilities[expected]
        passed = answer.get("choice") == expected and score >= threshold
        reason = f"expected option probability {score:.3f} {'meets' if passed else 'misses'} threshold {threshold:.3f}"
    elif question_type == "score":
        actual = answer.get("score")
        if isinstance(actual, bool) or not isinstance(actual, (int, float)) or not math.isfinite(float(actual)):
            raise ControlInputError(f"answer[{question_id!r}].score must be a finite number")
        actual = float(actual)
        if "min_score" in rubric:
            minimum = rubric["min_score"]
            if isinstance(minimum, bool) or not isinstance(minimum, (int, float)) or not math.isfinite(float(minimum)):
                raise ControlInputError(f"rubric[{question_id!r}].min_score must be a finite number")
            passed = actual >= float(minimum)
            score = 1.0 if passed else 0.0
            reason = f"score {actual:.3f} {'meets' if passed else 'misses'} minimum {float(minimum):.3f}"
        else:
            expected = rubric.get("expected")
            if isinstance(expected, Mapping):
                expected = expected.get("level")
            if isinstance(expected, bool) or not isinstance(expected, (int, float)) or not math.isfinite(float(expected)):
                raise ControlInputError(f"rubric[{question_id!r}] score criteria needs expected or min_score")
            tolerance = rubric.get("tolerance", 0.5)
            if (
                isinstance(tolerance, bool)
                or not isinstance(tolerance, (int, float))
                or not math.isfinite(float(tolerance))
                or float(tolerance) < 0
            ):
                raise ControlInputError(f"rubric[{question_id!r}].tolerance must be a non-negative number")
            error = abs(actual - float(expected))
            passed = error <= float(tolerance)
            score = 1.0 if passed else 0.0
            reason = f"score error {error:.3f} {'is' if passed else 'exceeds'} tolerance {float(tolerance):.3f}"
    else:
        raise ControlInputError(f"rubric[{question_id!r}] has unsupported type {question_type!r}")
    return {
        "id": question_id,
        "type": question_type,
        "score": round(score, 6),
        "passed": passed,
        "weight": weight,
        "threshold": threshold,
        "reason": reason,
    }


def judge_typed_answers(
    response_or_answers: Mapping[str, Any],
    rubric: Mapping[str, Mapping[str, Any]],
    *,
    accept_threshold: float = DEFAULT_JUDGE_ACCEPT_THRESHOLD,
    review_threshold: float = DEFAULT_JUDGE_REVIEW_THRESHOLD,
) -> dict[str, Any]:
    """Aggregate typed rubric judgments into accept/review/reject.

    Rubrics are explicit application policy. A common online-eval rubric is a
    set of Noul questions such as ``correct``, ``grounded``, and ``cited``;
    Choice and Score criteria are supported for stricter contracts.
    """

    if not isinstance(rubric, Mapping) or not rubric:
        raise ControlInputError("rubric must be a non-empty mapping")
    accept_threshold = _threshold(accept_threshold, "accept_threshold")
    review_threshold = _threshold(review_threshold, "review_threshold")
    if review_threshold > accept_threshold:
        raise ControlInputError("review_threshold cannot exceed accept_threshold")
    if not isinstance(response_or_answers, Mapping):
        raise ControlInputError("typed response must be an object")
    answers = response_or_answers.get("answers", response_or_answers)
    if not isinstance(answers, Mapping):
        raise ControlInputError("typed response answers must be an object")

    criteria: list[dict[str, Any]] = []
    for question_id, definition in rubric.items():
        if not isinstance(question_id, str) or not question_id.strip():
            raise ControlInputError("rubric question IDs must be non-empty strings")
        if not isinstance(definition, Mapping):
            raise ControlInputError(f"rubric[{question_id!r}] must be an object")
        if question_id not in answers or not isinstance(answers[question_id], Mapping):
            raise ControlInputError(f"typed response is missing rubric answer {question_id!r}")
        criteria.append(_criterion_result(question_id, answers[question_id], definition))
    total_weight = sum(item["weight"] for item in criteria)
    weighted_score = sum(item["score"] * item["weight"] for item in criteria) / total_weight
    if weighted_score >= accept_threshold:
        decision = "accept"
    elif weighted_score >= review_threshold:
        decision = "review"
    else:
        decision = "reject"
    return {
        "decision": decision,
        "score": round(weighted_score, 6),
        "passed": sum(item["passed"] for item in criteria),
        "total": len(criteria),
        "thresholds": {"accept": accept_threshold, "review": review_threshold},
        "criteria": criteria,
    }

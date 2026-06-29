from __future__ import annotations

import math
import re
from collections.abc import Mapping


ALLOWED_BUCKETS = {"strong_review", "review", "weak_review", "manual_review"}
ALLOWED_SCORE_BASIS = {"resume_quality_only", "resume_plus_jd_company"}
FINAL_DECISION_LABEL_RE = re.compile(
    r"\b(hire|reject|pass|fail|eliminate|admit)\b",
    re.IGNORECASE,
)
FINAL_DECISION_CJK_LABELS = (
    "\u5f55\u7528",
    "\u6dd8\u6c70",
    "\u901a\u8fc7",
    "\u4e0d\u901a\u8fc7",
)


class ValidationError(ValueError):
    pass


def validate_evaluation(data, evaluation_config=None):
    evaluation_config = evaluation_config or {}
    _require_keys(
        data,
        (
            "candidate_id",
            "inferred_profile",
            "scores",
            "evidence",
            "deductions",
            "strengths",
            "concerns",
            "interview_validation_points",
            "compliance",
            "recommendation",
        ),
        "evaluation",
    )
    _require_list_fields(
        data,
        ("evidence", "deductions", "strengths", "concerns", "interview_validation_points"),
        "evaluation",
    )
    _validate_profile(data["inferred_profile"])
    _validate_scores(data["scores"], evaluation_config)
    _validate_compliance(data["compliance"])
    _validate_recommendation(data["recommendation"])

    return data


def _require_keys(data, keys, label):
    if not isinstance(data, Mapping):
        raise ValidationError(f"{label} must be an object")

    for key in keys:
        if key not in data:
            raise ValidationError(f"{label} missing required key: {key}")


def _require_list_fields(data, keys, label):
    for key in keys:
        if not isinstance(data[key], list):
            raise ValidationError(f"{label}.{key} must be a list")


def _validate_profile(profile):
    _require_keys(profile, ("role_family", "seniority", "domain_context", "confidence"), "inferred_profile")
    _number(profile["confidence"], "inferred_profile.confidence", 0, 1)


def _validate_recommendation(recommendation):
    _require_keys(recommendation, ("screening_bucket", "summary", "next_steps"), "recommendation")

    bucket = recommendation["screening_bucket"]
    if bucket not in ALLOWED_BUCKETS:
        raise ValidationError("recommendation.screening_bucket is not allowed")

    summary = recommendation["summary"]
    if not isinstance(summary, str):
        raise ValidationError("recommendation.summary must be text")

    if not isinstance(recommendation["next_steps"], list):
        raise ValidationError("recommendation.next_steps must be a list")
    for item in recommendation["next_steps"]:
        if not isinstance(item, str):
            raise ValidationError("recommendation.next_steps items must be text")

    _reject_final_decision_labels("recommendation.summary", (summary,))
    _reject_final_decision_labels("recommendation.next_steps", recommendation["next_steps"])


def _reject_final_decision_labels(label, values):
    for value in values:
        if FINAL_DECISION_LABEL_RE.search(value) or any(
            prohibited in value for prohibited in FINAL_DECISION_CJK_LABELS
        ):
            raise ValidationError(f"{label} contains prohibited final decision label")


def _validate_scores(scores, evaluation_config):
    _require_keys(
        scores,
        ("score_basis", "overall", "resume_quality", "jd_company_match", "dimensions"),
        "scores",
    )

    basis = scores["score_basis"]
    if basis not in ALLOWED_SCORE_BASIS:
        raise ValidationError("scores.score_basis is not allowed")

    overall = _number(scores["overall"], "scores.overall", 0, 100)
    resume_quality = _number(scores["resume_quality"], "scores.resume_quality", 0, 60)

    if basis == "resume_plus_jd_company":
        jd_company_match = _number(scores["jd_company_match"], "scores.jd_company_match", 0, 40)
        expected_overall = round(resume_quality + jd_company_match, 2)
        if overall != expected_overall:
            raise ValidationError("scores.overall must equal resume_quality plus jd_company_match")
    else:
        if scores["jd_company_match"] is not None:
            raise ValidationError("scores.jd_company_match must be None for resume_quality_only")
        expected_overall = round(resume_quality / 60 * 100, 2)
        if overall != expected_overall:
            raise ValidationError("scores.overall must equal resume_quality normalized to 100")

    dimensions = scores["dimensions"]
    if not isinstance(dimensions, list) or not dimensions:
        raise ValidationError("scores.dimensions must be a non-empty list")

    for dimension in dimensions:
        if not isinstance(dimension, Mapping):
            raise ValidationError("scores.dimensions item must be an object")
        _require_keys(dimension, ("name", "score", "max_score", "evidence", "deductions"), "dimension")

        max_score = _number(dimension["max_score"], "dimension.max_score", 0, math.inf)
        if max_score <= 0:
            raise ValidationError("dimension.max_score must be positive")
        _number(dimension["score"], "dimension.score", 0, max_score)

        if not isinstance(dimension["evidence"], list):
            raise ValidationError("dimension.evidence must be a list")
        if not isinstance(dimension["deductions"], list):
            raise ValidationError("dimension.deductions must be a list")
        if not dimension["evidence"] and not dimension["deductions"]:
            raise ValidationError("dimension evidence or deductions required")

    weights = evaluation_config.get("weights")
    if weights:
        _validate_weighted_dimensions(scores, weights)


def _validate_weighted_dimensions(scores, weights):
    if not isinstance(weights, Mapping):
        raise ValidationError("weights must be an object")

    resume_weights = _dimension_weights(weights, "resume_quality")
    jd_weights = _dimension_weights(weights, "jd_company_match")
    basis = scores["score_basis"]

    expected_groups = [("resume_quality", resume_weights)]
    if basis == "resume_plus_jd_company":
        expected_groups.append(("jd_company_match", jd_weights))

    expected_weights = {}
    for _, group_weights in expected_groups:
        expected_weights.update(group_weights)

    dimensions = scores["dimensions"]
    by_name = {}
    for dimension in dimensions:
        name = dimension["name"]
        if name in by_name:
            raise ValidationError(f"duplicate dimension: {name}")
        by_name[name] = dimension
        if name not in expected_weights:
            raise ValidationError(f"unexpected dimension: {name}")
        if dimension["max_score"] != expected_weights[name]:
            raise ValidationError(f"dimension.max_score does not match configured weight: {name}")

    missing = [name for name in expected_weights if name not in by_name]
    if missing:
        raise ValidationError(f"missing configured dimension: {missing[0]}")

    resume_score = _sum_dimension_scores(by_name, resume_weights)
    if resume_score != scores["resume_quality"]:
        raise ValidationError("scores.resume_quality must equal configured resume dimension scores")

    if basis == "resume_plus_jd_company":
        jd_score = _sum_dimension_scores(by_name, jd_weights)
        if jd_score != scores["jd_company_match"]:
            raise ValidationError("scores.jd_company_match must equal configured JD/company dimension scores")


def _dimension_weights(weights, group):
    group_weights = weights.get(group)
    if not isinstance(group_weights, Mapping) or not group_weights:
        raise ValidationError(f"weights.{group} must be a non-empty object")
    for name, value in group_weights.items():
        _number(value, f"weights.{group}.{name}", 0, math.inf)
        if value <= 0:
            raise ValidationError(f"weights.{group}.{name} must be positive")
    return group_weights


def _sum_dimension_scores(by_name, weights):
    return round(sum(by_name[name]["score"] for name in weights), 2)


def _validate_compliance(compliance):
    _require_keys(
        compliance,
        (
            "sensitive_or_irrelevant_information",
            "must_not_use_for_screening",
            "manual_review_required",
            "no_auto_reject_reasons",
        ),
        "compliance",
    )
    _require_list_fields(
        compliance,
        (
            "sensitive_or_irrelevant_information",
            "must_not_use_for_screening",
            "manual_review_required",
            "no_auto_reject_reasons",
        ),
        "compliance",
    )


def _number(value, label, minimum, maximum):
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise ValidationError(f"{label} must be numeric")
    if not math.isfinite(value):
        raise ValidationError(f"{label} must be a finite number")
    if value < minimum or value > maximum:
        raise ValidationError(f"{label} must be between {minimum} and {maximum}")
    return value

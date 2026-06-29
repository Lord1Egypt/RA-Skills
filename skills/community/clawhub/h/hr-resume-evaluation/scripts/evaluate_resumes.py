from __future__ import annotations

import argparse
import copy
import json
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Callable

import yaml

if __package__ in {None, ""}:
    project_root = Path(__file__).resolve().parents[1]
    if str(project_root) not in sys.path:
        sys.path.insert(0, str(project_root))

from scripts.llm_client import ModelConfig, build_messages, evaluate_with_model, load_model_config
from scripts.parse_documents import ParsedDocument, discover_resumes, parse_document
from scripts.render_reports import (
    render_candidate_report,
    render_csv_summary,
    render_raw_json_result,
    render_summary_report,
)
from scripts.validate_results import ValidationError, validate_evaluation


KNOWN_PARSE_ERRORS = {"empty_text", "unsupported_extension"}
TOP_LEVEL_RESULT_KEYS = (
    "candidate_id",
    "file_name",
    "inferred_profile",
    "scores",
    "evidence",
    "deductions",
    "strengths",
    "concerns",
    "interview_validation_points",
    "compliance",
    "recommendation",
    "audit",
)

Evaluator = Callable[
    [ParsedDocument, str | None, str | None, dict[str, Any], ModelConfig | None],
    dict[str, Any],
]


def run_batch(
    *,
    resumes_dir: str | Path,
    output_dir: str | Path,
    evaluation_config_path: str | Path,
    evaluator: Evaluator,
    jd_path: str | Path | None = None,
    company_path: str | Path | None = None,
    model_config_path: str | Path | None = None,
) -> dict[str, int]:
    output_dir = Path(output_dir)
    evaluation_config = _load_yaml(evaluation_config_path)
    max_model_retries = _max_model_retries(evaluation_config)
    include_raw_json = bool(evaluation_config.get("include_raw_json", False))
    model_config = load_model_config(model_config_path) if model_config_path is not None else None
    jd_text = _read_optional_text(jd_path)
    company_text = _read_optional_text(company_path)

    results: list[dict[str, Any]] = []
    failures: list[dict[str, str]] = []

    for resume_path in discover_resumes(Path(resumes_dir)):
        parsed = parse_document(resume_path)
        if not parsed.ok:
            failures.append(
                {
                    "candidate_id": parsed.candidate_id,
                    "file_name": parsed.file_name,
                    "error": _parse_error_code(parsed.error),
                }
            )
            continue

        try:
            validated = _evaluate_and_validate(
                parsed,
                jd_text,
                company_text,
                evaluation_config,
                model_config,
                evaluator,
                max_model_retries,
            )
            render_candidate_report(validated, output_dir)
            if include_raw_json:
                render_raw_json_result(validated, output_dir)
            results.append(validated)
        except Exception as exc:
            failures.append(_failure_record(parsed.file_name, parsed.candidate_id, exc))

    render_summary_report(results, failures, output_dir)
    render_csv_summary(results, output_dir)
    return {"successful": len(results), "failed": len(failures)}


def _evaluate_and_validate(
    parsed: ParsedDocument,
    jd_text: str | None,
    company_text: str | None,
    evaluation_config: dict[str, Any],
    model_config: ModelConfig | None,
    evaluator: Evaluator,
    max_model_retries: int,
) -> dict[str, Any]:
    for attempt in range(max_model_retries + 1):
        raw = evaluator(parsed, jd_text, company_text, evaluation_config, model_config)
        try:
            if not isinstance(raw, dict):
                return validate_evaluation(raw, evaluation_config)
            prepared = _prepare_for_validation(raw, parsed, jd_text, company_text, evaluation_config)
            return _sanitize_evaluation(validate_evaluation(prepared, evaluation_config))
        except ValidationError:
            if attempt >= max_model_retries:
                raise

    raise ValidationError("evaluation validation failed")


def _prepare_for_validation(
    raw: dict[str, Any],
    parsed: ParsedDocument,
    jd_text: str | None,
    company_text: str | None,
    evaluation_config: dict[str, Any],
) -> dict[str, Any]:
    prepared = copy.deepcopy(raw)
    prepared["candidate_id"] = parsed.candidate_id
    prepared["file_name"] = parsed.file_name

    profile = prepared.get("inferred_profile")
    if isinstance(profile, dict):
        role_family_override = evaluation_config.get("role_family_override")
        seniority_override = evaluation_config.get("seniority_override")
        if role_family_override is not None:
            profile["role_family"] = role_family_override
        if seniority_override is not None:
            profile["seniority"] = seniority_override

    prepared["audit"] = {
        "evaluation_time": datetime.now(timezone.utc).replace(microsecond=0).isoformat(),
        "jd_company_context_used": bool(jd_text or company_text),
    }
    return prepared


def _sanitize_evaluation(result: dict[str, Any]) -> dict[str, Any]:
    sanitized = {key: copy.deepcopy(result[key]) for key in TOP_LEVEL_RESULT_KEYS if key in result}
    sanitized["inferred_profile"] = {
        key: sanitized["inferred_profile"][key]
        for key in ("role_family", "seniority", "domain_context", "confidence")
    }
    sanitized["scores"] = {
        "score_basis": sanitized["scores"]["score_basis"],
        "overall": sanitized["scores"]["overall"],
        "resume_quality": sanitized["scores"]["resume_quality"],
        "jd_company_match": sanitized["scores"]["jd_company_match"],
        "dimensions": [
            {
                "name": dimension["name"],
                "score": dimension["score"],
                "max_score": dimension["max_score"],
                "evidence": copy.deepcopy(dimension["evidence"]),
                "deductions": copy.deepcopy(dimension["deductions"]),
            }
            for dimension in sanitized["scores"]["dimensions"]
        ],
    }
    sanitized["compliance"] = {
        key: copy.deepcopy(sanitized["compliance"][key])
        for key in (
            "sensitive_or_irrelevant_information",
            "must_not_use_for_screening",
            "manual_review_required",
            "no_auto_reject_reasons",
        )
    }
    sanitized["recommendation"] = {
        "screening_bucket": sanitized["recommendation"]["screening_bucket"],
        "summary": sanitized["recommendation"]["summary"],
        "next_steps": copy.deepcopy(sanitized["recommendation"]["next_steps"]),
    }
    if "audit" in sanitized:
        sanitized["audit"] = {
            "evaluation_time": sanitized["audit"]["evaluation_time"],
            "jd_company_context_used": bool(sanitized["audit"]["jd_company_context_used"]),
        }
    return sanitized


def _failure_record(file_name: str, candidate_id: str, exc: Exception) -> dict[str, str]:
    return {
        "candidate_id": candidate_id,
        "file_name": file_name,
        "error": f"evaluation_error:{exc.__class__.__name__}",
    }


def _parse_error_code(error: str | None) -> str:
    if error in KNOWN_PARSE_ERRORS:
        return error
    return "parse_error"


def _model_evaluator(
    parsed: ParsedDocument,
    jd_text: str | None,
    company_text: str | None,
    evaluation_config: dict[str, Any],
    model_config: ModelConfig | None,
) -> dict[str, Any]:
    if model_config is None:
        raise ValueError("model_config is required")

    messages = build_messages(
        candidate_id=parsed.candidate_id,
        resume_text=parsed.text,
        jd_text=jd_text or "",
        company_text=company_text or "",
        evaluation_config=evaluation_config,
    )
    return evaluate_with_model(
        model_config,
        messages,
        max_response_retries=_max_model_retries(evaluation_config),
    )


def _read_optional_text(path: str | Path | None) -> str | None:
    if path is None:
        return None
    return Path(path).read_text(encoding="utf-8-sig")


def _load_yaml(path: str | Path) -> dict[str, Any]:
    return yaml.safe_load(Path(path).read_text(encoding="utf-8-sig")) or {}


def _max_model_retries(evaluation_config: dict[str, Any]) -> int:
    return max(0, int(evaluation_config.get("max_model_retries", 0) or 0))


def _exit_code(summary: dict[str, int]) -> int:
    return 1 if summary["failed"] > 0 else 0


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Evaluate resumes and render batch reports.")
    parser.add_argument("--resumes", required=True, type=Path)
    parser.add_argument("--jd", type=Path)
    parser.add_argument("--company", type=Path)
    parser.add_argument("--output", required=True, type=Path)
    parser.add_argument("--config", type=Path, default=Path("config/evaluation.yaml"))
    parser.add_argument("--model-config", type=Path, default=Path("config/model.yaml"))
    return parser


def main(argv: list[str] | None = None) -> int:
    args = _parser().parse_args(argv)
    summary = run_batch(
        resumes_dir=args.resumes,
        output_dir=args.output,
        evaluation_config_path=args.config,
        evaluator=_model_evaluator,
        jd_path=args.jd,
        company_path=args.company,
        model_config_path=args.model_config,
    )
    print(json.dumps(summary, ensure_ascii=False))
    return _exit_code(summary)


if __name__ == "__main__":
    raise SystemExit(main())

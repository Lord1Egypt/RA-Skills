from dataclasses import dataclass
from pathlib import Path
from typing import Any
import json
import os
import time

import requests
import yaml


class MissingApiKey(RuntimeError):
    pass


class ModelResponseError(RuntimeError):
    pass


@dataclass(frozen=True)
class ModelConfig:
    base_url: str
    chat_completions_path: str
    model: str
    api_key_env: str
    timeout_seconds: int
    max_retries: int
    temperature: float

    def api_key(self) -> str:
        value = os.environ.get(self.api_key_env)
        if not value:
            raise MissingApiKey(f"Missing API key environment variable: {self.api_key_env}")
        return value

    @property
    def endpoint(self) -> str:
        return f"{self.base_url.rstrip('/')}/{self.chat_completions_path.lstrip('/')}"


def load_model_config(path: str | Path) -> ModelConfig:
    data = yaml.safe_load(Path(path).read_text(encoding="utf-8")) or {}
    return ModelConfig(
        base_url=data["base_url"],
        chat_completions_path=data.get("chat_completions_path", "/chat/completions"),
        model=data["model"],
        api_key_env=data["api_key_env"],
        timeout_seconds=data.get("timeout_seconds", 120),
        max_retries=data.get("max_retries", 2),
        temperature=data.get("temperature", 0.1),
    )


def build_messages(
    *,
    candidate_id: str,
    resume_text: str,
    jd_text: str,
    company_text: str,
    evaluation_config: dict[str, Any],
) -> list[dict[str, str]]:
    user_payload = {
        "candidate_id": candidate_id,
        "candidate_id_instruction": "Return exactly this candidate_id in the top-level candidate_id field.",
        "output_language": evaluation_config.get("output_language"),
        "role_family_override": evaluation_config.get("role_family_override"),
        "seniority_override": evaluation_config.get("seniority_override"),
        "scoring_weights": evaluation_config.get("weights"),
        "enterprise_hiring_calibration": [
            "Score for enterprise recruiting judgment, not academic ranking or resume polish alone.",
            "Education is important, and papers or competitions can support technical depth, but they should not outweigh concrete project delivery evidence when the project is technically plausible and has visible real-world effects.",
            "For projects, weigh scenario constraints, personal ownership, implementation details, production/pilot/customer delivery status, measurable impact, scale, cost, quality, efficiency, reliability, and post-launch iteration.",
            "When no JD is provided, still distinguish landed enterprise projects, pilot delivery, PoC, academic research, coursework, and vague claims; use holistic judgment without rigid caps.",
            "When JD is provided, prioritize JD-relevant landed projects and technology fit over impressive but unrelated academic or competition signals.",
            "Do not infer missing facts; use deductions and interview validation points when delivery status, personal contribution, or metrics are unclear.",
        ],
        "resume_text": resume_text,
        "jd_text": jd_text,
        "company_text": company_text,
        "required_json_contract": {
            "candidate_id": f"must equal {candidate_id!r}",
            "inferred_profile": {
                "role_family": "string",
                "seniority": "string",
                "domain_context": "string",
                "confidence": "number from 0 to 1",
            },
            "scores": {
                "score_basis": "resume_quality_only or resume_plus_jd_company",
                "overall": "number from 0 to 100",
                "resume_quality": "number from 0 to 60",
                "jd_company_match": "number from 0 to 40, or null for resume_quality_only",
                "score_formulas": {
                    "resume_plus_jd_company": "overall = resume_quality + jd_company_match",
                    "resume_quality_only": "overall = round(resume_quality / 60 * 100, 2); jd_company_match = null",
                },
                "dimensions": [
                    {
                        "name": "string",
                        "score": "number",
                        "max_score": "positive number",
                        "evidence": "array of resume, JD, or company facts",
                        "deductions": "array of evidence-based limitations",
                    }
                ],
            },
            "evidence": "array",
            "deductions": "array",
            "strengths": "array",
            "concerns": "array",
            "interview_validation_points": "array",
            "compliance": {
                "sensitive_or_irrelevant_information": "array",
                "must_not_use_for_screening": "array",
                "manual_review_required": "array",
                "no_auto_reject_reasons": "array",
            },
            "recommendation": {
                "screening_bucket": "strong_review, review, weak_review, or manual_review",
                "summary": "string",
                "next_steps": "array",
            },
            "rules": [
                "Return exactly the provided candidate_id; do not infer or rewrite it.",
                "Every score dimension must include evidence, deductions, or both.",
                "Evidence and deductions must cite only resume, JD, or company facts.",
                "Use the enterprise_hiring_calibration guidance to make holistic tradeoffs; do not apply hidden hard caps.",
            ],
        },
    }
    return [
        {
            "role": "system",
            "content": (
                "You are a recruiter-side resume evaluation assistant. "
                "Calibrate scores for enterprise hiring: prioritize concrete, technically plausible "
                "project delivery and JD-relevant implementation evidence while treating education, "
                "papers, and competitions as supporting signals. "
                "Return only valid JSON. Do not make hiring, rejection, pass, fail, "
                "admission, or elimination decisions. Do not score protected traits "
                "or job-irrelevant personal traits."
            ),
        },
        {
            "role": "user",
            "content": json.dumps(user_payload, ensure_ascii=False, indent=2),
        },
    ]


def _http_status_code(exc: requests.HTTPError) -> int | None:
    response = getattr(exc, "response", None)
    return getattr(response, "status_code", None)


def _is_retryable_status(status_code: int | None) -> bool:
    return status_code == 429 or (status_code is not None and 500 <= status_code <= 599)


def _raise_model_error(prefix: str, exc: BaseException, attempts: int, status_code: int | None = None) -> None:
    status = f" status={status_code}" if status_code is not None else ""
    raise ModelResponseError(f"{prefix} after {attempts} attempt(s): {exc.__class__.__name__}{status}") from None


def _parse_model_response(response: requests.Response, attempts: int) -> dict[str, Any]:
    try:
        content = response.json()["choices"][0]["message"]["content"]
        return json.loads(content)
    except (KeyError, IndexError, TypeError, ValueError) as exc:
        _raise_model_error("Model response invalid", exc, attempts)


def evaluate_with_model(
    config: ModelConfig,
    messages: list[dict[str, str]],
    *,
    max_response_retries: int | None = None,
) -> dict[str, Any]:
    response_retries = config.max_retries if max_response_retries is None else max_response_retries
    http_failures = 0
    response_failures = 0
    max_attempts = config.max_retries + response_retries + 1
    payload = {
        "model": config.model,
        "messages": messages,
        "temperature": config.temperature,
        "response_format": {"type": "json_object"},
    }
    headers = {
        "Authorization": f"Bearer {config.api_key()}",
        "Content-Type": "application/json",
    }

    for attempt in range(max_attempts):
        attempts = attempt + 1
        try:
            response = requests.post(
                config.endpoint,
                headers=headers,
                json=payload,
                timeout=config.timeout_seconds,
            )
            response.raise_for_status()
        except requests.HTTPError as exc:
            status_code = _http_status_code(exc)
            if _is_retryable_status(status_code) and http_failures < config.max_retries:
                http_failures += 1
                time.sleep(1 + attempt)
                continue
            _raise_model_error("Model request failed", exc, attempts, status_code)
        except requests.RequestException as exc:
            if http_failures < config.max_retries:
                http_failures += 1
                time.sleep(1 + attempt)
                continue
            _raise_model_error("Model request failed", exc, attempts)

        try:
            return _parse_model_response(response, attempts)
        except ModelResponseError:
            if response_failures < response_retries:
                response_failures += 1
                time.sleep(1 + attempt)
                continue
            raise

    raise ModelResponseError("Model request failed")

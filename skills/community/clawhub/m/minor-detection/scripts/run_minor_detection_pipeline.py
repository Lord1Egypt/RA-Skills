#!/usr/bin/env python3
# 模块说明：
# - bundled skill 内部总控脚本。
# - Mode A 和 Mode B 最终真正执行的就是它。

from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
import tempfile
from pathlib import Path
from typing import Any, Dict, List, Tuple

import requests

SCRIPT_DIR = Path(__file__).resolve().parent
SKILL_DIR = SCRIPT_DIR.parent
REFERENCES_DIR = SKILL_DIR / "references"

if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

from _classifier_client import ClassifierAPIError, call_chat_completion
from _payload_normalizer import normalize_payload
from _profile_merge import merge_output
from _schema_repair import repair_output, validate_output
from _skill_retrieval_utils import build_query_retrieval_text
from config import (
    CLASSIFIER_API_KEY,
    CLASSIFIER_BASE_URL,
    CLASSIFIER_MAX_RETRIES,
    CLASSIFIER_MODEL,
    CLASSIFIER_RETRY_BACKOFF_SEC,
    CLASSIFIER_TIMEOUT_SEC,
    PIPELINE_TIMEZONE,
    RETRIEVAL_TOP_K,
    classifier_runtime_snapshot,
    embedding_runtime_snapshot,
    export_embedding_env,
)


PIPELINE_SCRIPT_NAME = "run_minor_detection_pipeline.py"
TIME_SCRIPT_NAME = "extract_time_features.py"
RETRIEVE_SCRIPT_NAME = "retrieve_cases.py"
OBSERVABILITY_PREFIX = "[MINOR_PIPELINE_OBSERVABILITY]"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run the minor-detection end-to-end pipeline.")
    parser.add_argument("--payload-file", help="Path to a JSON payload file.")
    parser.add_argument("--payload-json", help="Inline JSON payload.")
    return parser.parse_args()


def _load_payload(args: argparse.Namespace) -> Dict[str, Any]:
    if args.payload_file:
        return json.loads(Path(args.payload_file).read_text(encoding="utf-8"))
    if args.payload_json:
        return json.loads(args.payload_json)
    return json.load(sys.stdin)


def _load_reference(name: str) -> str:
    return (REFERENCES_DIR / name).read_text(encoding="utf-8")


def _render_template(template: str, variables: Dict[str, Any]) -> str:
    rendered = template
    for key, value in variables.items():
        rendered = rendered.replace(f"{{{{{key}}}}}", str(value))
    return rendered


def _safe_text(value: Any) -> str:
    return str(value or "").strip()


def _conversation_user_text(conversation: List[Dict[str, Any]]) -> str:
    parts: List[str] = []
    for turn in conversation:
        if not isinstance(turn, dict):
            continue
        if _safe_text(turn.get("role")) == "assistant":
            continue
        content = _safe_text(turn.get("content"))
        if content:
            parts.append(content)
    return "\n".join(parts)


def _script_path(script_name: str) -> Path:
    return SCRIPT_DIR / script_name


def _run_json_script(script_name: str, args: List[str], observability: Dict[str, Any]) -> Dict[str, Any]:
    command = [sys.executable, str(_script_path(script_name)), *args]
    env = dict(os.environ)
    env.update(export_embedding_env())
    completed = subprocess.run(
        command,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
        check=False,
        env=env,
    )
    output_text = (completed.stdout or "").strip()
    parsed_output: Dict[str, Any] = {}
    if output_text:
        try:
            parsed_output = json.loads(output_text.splitlines()[-1])
        except Exception:
            parsed_output = {}

    observability["script_calls"].append(
        {
            "script_name": script_name,
            "status": "completed" if completed.returncode == 0 else "failed",
            "exit_code": completed.returncode,
            "failed": completed.returncode != 0,
            "command": " ".join(command),
            "output_json": parsed_output or None,
        }
    )
    if completed.returncode != 0:
        raise RuntimeError((completed.stderr or output_text or f"{script_name} failed").strip())
    return parsed_output


def _extract_time_features(normalized_payload: Dict[str, Any], observability: Dict[str, Any]) -> Tuple[Dict[str, Any], str]:
    time_processing = observability["time_processing"]
    existing = normalized_payload["context"].get("time_features") or {}
    if existing:
        time_processing.update({"attempted": True, "successful": True, "mode": "provided"})
        return dict(existing), normalized_payload["timestamp_candidate"]

    raw_time_hint = normalized_payload["timestamp_candidate"]
    if not raw_time_hint:
        time_processing.update({"attempted": False, "successful": False, "mode": "none"})
        return {}, ""

    time_processing["attempted"] = True
    payload = _run_json_script(
        TIME_SCRIPT_NAME,
        ["--timestamp", raw_time_hint, "--timezone", PIPELINE_TIMEZONE],
        observability,
    )
    time_processing.update({"successful": True, "mode": "script"})
    return payload if isinstance(payload, dict) else {}, raw_time_hint


def _compose_retrieval_query(
    normalized_payload: Dict[str, Any],
    time_features: Dict[str, Any],
    raw_time_hint: str,
    template_text: str,
) -> str:
    base_query = build_query_retrieval_text(
        normalized_payload["conversation"],
        raw_time_hint=raw_time_hint,
        time_features=time_features,
    )
    return _render_template(
        template_text,
        {
            "MODE": normalized_payload["mode"],
            "CONVERSATION_TEXT": normalized_payload["conversation_text"],
            "USER_TEXT": _conversation_user_text(normalized_payload["conversation"]),
            "TIME_HINT": raw_time_hint,
            "TIME_FEATURES_JSON": json.dumps(time_features, ensure_ascii=False, indent=2),
            "IDENTITY_HINTS": "；".join(normalized_payload["identity_hints"]) or "无",
            "BASE_QUERY": base_query,
        },
    ).strip()


def _retrieve_cases(
    normalized_payload: Dict[str, Any],
    raw_time_hint: str,
    time_features: Dict[str, Any],
    retrieval_query: str,
    observability: Dict[str, Any],
) -> List[Dict[str, Any]]:
    retrieval = observability["retrieval"]
    existing = normalized_payload["context"].get("retrieved_cases") or []
    if existing:
        retrieval.update(
            {
                "attempted": False,
                "successful": True,
                "mode": "external_rag",
                "used_fallback": False,
                "retrieved_count": len(existing),
            }
        )
        return list(existing)

    retrieval["attempted"] = True
    with tempfile.NamedTemporaryFile("w", suffix=".json", delete=False, encoding="utf-8") as handle:
        json.dump(time_features, handle, ensure_ascii=False)
        temp_path = Path(handle.name)
    try:
        payload = _run_json_script(
            RETRIEVE_SCRIPT_NAME,
            [
                "--query",
                retrieval_query,
                "--top-k",
                str(RETRIEVAL_TOP_K),
                "--raw-time-hint",
                raw_time_hint,
                "--time-features-json",
                temp_path.read_text(encoding="utf-8"),
            ],
            observability,
        )
    finally:
        temp_path.unlink(missing_ok=True)

    if payload.get("status") != "ok":
        raise RuntimeError(_safe_text(payload.get("message")) or "retrieve_cases.py returned non-ok status")

    mode = _safe_text(payload.get("mode")) or "unknown"
    message = _safe_text(payload.get("message"))
    retrieval.update(
        {
            "successful": True,
            "mode": mode,
            "used_fallback": mode.startswith("fallback:"),
            "retrieved_count": int(payload.get("count", 0) or 0),
            "message": message or None,
            "fallback_reason": mode.split(":", 1)[1] if mode.startswith("fallback:") else None,
            "quoting_failure_detected": False,
            "network_error_detected": any(token in mode.lower() or token in message.lower() for token in ("connect", "network", "socket")),
        }
    )
    if retrieval["used_fallback"]:
        observability["issues"].append("retrieval_fallback")
    if retrieval["network_error_detected"]:
        observability["issues"].append("retrieval_network_blocked")
    return payload.get("retrieved_cases") or []


def _build_evidence_package(
    normalized_payload: Dict[str, Any],
    *,
    raw_time_hint: str,
    time_features: Dict[str, Any],
    retrieved_cases: List[Dict[str, Any]],
    evidence_rules_text: str,
    icbo_guidelines_text: str,
    output_schema_text: str,
) -> Dict[str, Any]:
    return {
        "mode": normalized_payload["mode"],
        "request_id": normalized_payload["meta"]["request_id"],
        "sample_id": normalized_payload["meta"]["sample_id"],
        "user_id": normalized_payload["meta"]["user_id"],
        "conversation": normalized_payload["conversation"],
        "conversation_text": normalized_payload["conversation_text"],
        "raw_time_hint": raw_time_hint,
        "time_features": time_features,
        "prior_profile": normalized_payload["context"].get("prior_profile") or {},
        "retrieved_cases": retrieved_cases,
        "identity_hints": normalized_payload["identity_hints"],
        "evidence_rules": evidence_rules_text,
        "icbo_guidelines": icbo_guidelines_text,
        "output_schema": output_schema_text,
        "runtime": {
            "classifier": classifier_runtime_snapshot(),
            "embedding": embedding_runtime_snapshot(),
        },
    }


def _retrieval_evidence_lines(retrieved_cases: List[Dict[str, Any]]) -> List[str]:
    lines: List[str] = []
    for item in retrieved_cases:
        if not isinstance(item, dict):
            continue
        sample_id = _safe_text(item.get("sample_id")) or "unknown"
        label = _safe_text(item.get("label")) or "unknown"
        score = item.get("score")
        summary = _safe_text(item.get("summary"))
        lines.append(f"sample_id={sample_id}; label={label}; score={score}; summary={summary}")
    return lines


def _post_process_output(output: Dict[str, Any], normalized_payload: Dict[str, Any], retrieved_cases: List[Dict[str, Any]], raw_time_hint: str, time_features: Dict[str, Any]) -> Dict[str, Any]:
    output = merge_output(output, normalized_payload)
    evidence = output.setdefault("evidence", {})
    evidence.setdefault("retrieval_evidence", [])
    if not evidence["retrieval_evidence"]:
        evidence["retrieval_evidence"] = _retrieval_evidence_lines(retrieved_cases)
    evidence.setdefault("time_evidence", [])
    if raw_time_hint and not evidence["time_evidence"]:
        evidence["time_evidence"] = [raw_time_hint]
    icbo = output.setdefault("icbo_features", {})
    if raw_time_hint and _safe_text(icbo.get("opportunity_time")) in {"", "未明确"}:
        time_tags = []
        for key in ("weekday", "time_bucket", "holiday_label"):
            value = _safe_text(time_features.get(key))
            if value:
                time_tags.append(f"{key}={value}")
        suffix = f"；{'；'.join(time_tags)}" if time_tags else ""
        icbo["opportunity_time"] = f"{raw_time_hint}{suffix}"
    return output


def _emit_observability(observability: Dict[str, Any]) -> None:
    print(f"{OBSERVABILITY_PREFIX} {json.dumps(observability, ensure_ascii=False)}", file=sys.stderr)


def run_pipeline(raw_payload: Dict[str, Any]) -> Dict[str, Any]:
    normalized_payload = normalize_payload(raw_payload)
    observability: Dict[str, Any] = {
        "summary": {"script_call_count": 0, "failed_script_calls": 0, "stderr_non_empty": False},
        "time_processing": {"attempted": False, "successful": False, "failure_count": 0, "mode": None},
        "retrieval": {
            "attempted": False,
            "successful": False,
            "mode": None,
            "used_fallback": False,
            "fallback_reason": None,
            "retrieved_count": 0,
            "failure_count": 0,
            "quoting_failure_detected": False,
            "network_error_detected": False,
            "message": None,
        },
        "issues": [],
        "script_calls": [
            {
                "script_name": PIPELINE_SCRIPT_NAME,
                "status": "completed",
                "exit_code": 0,
                "failed": False,
                "command": PIPELINE_SCRIPT_NAME,
                "output_json": None,
            }
        ],
        "classifier_runtime": classifier_runtime_snapshot(),
        "embedding_runtime": embedding_runtime_snapshot(),
    }

    raw_time_hint = ""
    time_features: Dict[str, Any] = {}
    retrieved_cases: List[Dict[str, Any]] = []
    raw_classifier_output = ""
    try:
        retrieval_query_template = _load_reference("retrieval-query-template.md")
        classifier_system_text = _load_reference("classifier-system.md")
        classifier_user_template = _load_reference("classifier-user-template.md")
        evidence_rules_text = _load_reference("evidence-rules.md")
        icbo_guidelines_text = _load_reference("icbo-guidelines.md")
        output_schema_text = _load_reference("output-schema.md")
        schema_repair_template = _load_reference("schema-repair-template.md")

        time_features, raw_time_hint = _extract_time_features(normalized_payload, observability)
        retrieval_query = _compose_retrieval_query(
            normalized_payload,
            time_features,
            raw_time_hint,
            retrieval_query_template,
        )
        retrieved_cases = _retrieve_cases(
            normalized_payload,
            raw_time_hint,
            time_features,
            retrieval_query,
            observability,
        )
        evidence_package = _build_evidence_package(
            normalized_payload,
            raw_time_hint=raw_time_hint,
            time_features=time_features,
            retrieved_cases=retrieved_cases,
            evidence_rules_text=evidence_rules_text,
            icbo_guidelines_text=icbo_guidelines_text,
            output_schema_text=output_schema_text,
        )
        classifier_prompt = _render_template(
            classifier_user_template,
            {
                "EVIDENCE_PACKAGE_JSON": json.dumps(evidence_package, ensure_ascii=False, indent=2),
                "OUTPUT_SCHEMA": output_schema_text,
            },
        )
        output, raw_classifier_output = call_chat_completion(
            base_url=CLASSIFIER_BASE_URL,
            api_key=CLASSIFIER_API_KEY,
            model=CLASSIFIER_MODEL,
            timeout_sec=CLASSIFIER_TIMEOUT_SEC,
            max_retries=CLASSIFIER_MAX_RETRIES,
            retry_backoff_sec=CLASSIFIER_RETRY_BACKOFF_SEC,
            messages=[
                {"role": "system", "content": classifier_system_text},
                {"role": "user", "content": classifier_prompt},
            ],
            temperature=0.0,
        )
        output = _post_process_output(output, normalized_payload, retrieved_cases, raw_time_hint, time_features)
        if validate_output(output):
            output = repair_output(
                candidate=output,
                raw_response_text=raw_classifier_output,
                normalized_payload=normalized_payload,
                output_schema_text=output_schema_text,
                repair_template_text=schema_repair_template,
                classifier_base_url=CLASSIFIER_BASE_URL,
                classifier_api_key=CLASSIFIER_API_KEY,
                classifier_model=CLASSIFIER_MODEL,
                classifier_timeout_sec=CLASSIFIER_TIMEOUT_SEC,
                classifier_max_retries=CLASSIFIER_MAX_RETRIES,
                classifier_retry_backoff_sec=CLASSIFIER_RETRY_BACKOFF_SEC,
            )
            output = _post_process_output(output, normalized_payload, retrieved_cases, raw_time_hint, time_features)
        return output
    finally:
        observability["summary"]["script_call_count"] = len(observability["script_calls"])
        observability["summary"]["failed_script_calls"] = sum(1 for item in observability["script_calls"] if item.get("failed"))
        observability["issues"] = sorted(set(observability["issues"]))
        _emit_observability(observability)


def main() -> None:
    args = parse_args()
    try:
        payload = _load_payload(args)
        result = run_pipeline(payload)
        print(json.dumps(result, ensure_ascii=False))
    except requests.HTTPError as exc:
        print(f"classifier api http error: {exc}", file=sys.stderr)
        raise SystemExit(1)
    except ClassifierAPIError as exc:
        print(str(exc), file=sys.stderr)
        raise SystemExit(1)
    except Exception as exc:
        print(str(exc), file=sys.stderr)
        raise SystemExit(1)


if __name__ == "__main__":
    main()

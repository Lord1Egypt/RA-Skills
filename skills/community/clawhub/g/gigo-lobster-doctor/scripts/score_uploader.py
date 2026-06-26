from __future__ import annotations

import json
import re
import socket
import time
import urllib.error
import urllib.request

DEFAULT_UPLOAD_NAMES = {"zh": "未命名龙虾", "en": "Unnamed Lobster"}
UPLOAD_NAME_MAX_LENGTH = 50
UPLOAD_NAME_SANITIZER = re.compile(r"[^\w\s-]", re.UNICODE)


def sanitize_lobster_name(name: str, lang: str = "zh") -> str:
    cleaned = UPLOAD_NAME_SANITIZER.sub(" ", (name or "").strip())
    cleaned = re.sub(r"\s+", " ", cleaned).strip(" _-")
    if len(cleaned) > UPLOAD_NAME_MAX_LENGTH:
        cleaned = cleaned[:UPLOAD_NAME_MAX_LENGTH].rstrip(" _-")
    return cleaned or DEFAULT_UPLOAD_NAMES.get(lang, DEFAULT_UPLOAD_NAMES["en"])


def _http_error_detail(error: urllib.error.HTTPError) -> str:
    try:
        body = error.read().decode("utf-8", errors="replace").strip()
    except Exception:
        body = ""

    if body:
        try:
            payload = json.loads(body)
        except json.JSONDecodeError:
            payload = None
        if isinstance(payload, dict):
            message = payload.get("message") or payload.get("error")
            if message:
                return str(message)
        return body

    return str(error.reason or error.msg or "Request failed")


def _post_json(url: str, payload: dict, headers: dict[str, str] | None = None, timeout: int = 20) -> dict:
    request_headers = {"Content-Type": "application/json"}
    if headers:
        request_headers.update(headers)
    request = urllib.request.Request(
        url,
        data=json.dumps(payload).encode("utf-8"),
        headers=request_headers,
        method="POST",
    )
    try:
        with urllib.request.urlopen(request, timeout=timeout) as response:
            return json.loads(response.read().decode("utf-8"))
    except urllib.error.HTTPError as error:
        detail = _http_error_detail(error)
        raise RuntimeError(f"HTTP {error.code} {error.reason}: {detail}") from error
    except urllib.error.URLError as error:
        detail = getattr(error, "reason", None) or "Unknown network error"
        raise RuntimeError(f"Network error while contacting {url}: {detail}") from error
    except (TimeoutError, socket.timeout) as error:
        raise RuntimeError(f"Network timeout while contacting {url}: {error}") from error


def _get_json(url: str, headers: dict[str, str] | None = None) -> dict:
    request = urllib.request.Request(url, headers=headers or {}, method="GET")
    try:
        with urllib.request.urlopen(request, timeout=8) as response:
            return json.loads(response.read().decode("utf-8"))
    except urllib.error.HTTPError as error:
        detail = _http_error_detail(error)
        raise RuntimeError(f"HTTP {error.code} {error.reason}: {detail}") from error
    except urllib.error.URLError as error:
        detail = getattr(error, "reason", None) or "Unknown network error"
        raise RuntimeError(f"Network error while contacting {url}: {detail}") from error


def _base_payload(scores, ref_code: str | None) -> dict:
    payload = {
        "lobster_name": sanitize_lobster_name(scores.lobster_name, scores.lang),
        "anonymous": scores.anonymous,
        "total_score": scores.total_score,
        "tier": scores.tier,
        "dimensions": scores.dimensions,
        "lang": scores.lang,
        "timestamp": scores.timestamp,
    }
    if ref_code:
        payload["ref_code"] = ref_code
    return payload


def _session_payload(config: dict) -> dict:
    session = config.get("task_session") or {}
    session_id = session.get("session_id")
    ticket = session.get("ticket")
    if not session_id or not ticket:
        raise RuntimeError("Missing task session credentials for cloud scoring")
    return {"session_id": session_id, "ticket": ticket}


def upload_submission_batch(raw_results, config: dict) -> dict:
    session_payload = _session_payload(config)
    payload = {
        **session_payload,
        "results": [
            {
                "task_id": result.task_id,
                "response": result.response,
                "status": result.status,
                "error": result.error,
                "elapsed_ms": int(result.elapsed_ms),
                "usage": {
                    "prompt_tokens": int(result.usage.get("prompt_tokens", 0)),
                    "completion_tokens": int(result.usage.get("completion_tokens", 0)),
                },
                "artifact_refs": [],
            }
            for result in raw_results
        ],
    }
    return _post_json(f"{config['api_base'].rstrip('/')}/api/submissions/batch", payload)


def finalize_cloud_evaluation(scores, upload_mode: str, config: dict) -> dict:
    payload = {
        **_session_payload(config),
        "lobster_name": sanitize_lobster_name(scores.lobster_name, scores.lang),
        "anonymous": bool(scores.anonymous),
        "upload_mode": upload_mode,
        "timestamp": scores.timestamp,
    }
    return _post_json(f"{config['api_base'].rstrip('/')}/api/session/finalize", payload)


def fetch_cloud_evaluation(config: dict) -> dict:
    session = _session_payload(config)
    return _get_json(
        f"{config['api_base'].rstrip('/')}/api/evaluations/{session['session_id']}",
        headers={"X-GIGO-Session-Ticket": session["ticket"]},
    )


def submit_for_cloud_scoring(scores, raw_results, upload_mode: str, config: dict) -> dict:
    if str(config.get("runtime_mode") or "") == "v2":
        from .v2_run_report import build_run_report

        payload = build_run_report(scores, raw_results, config, upload_mode)
        try:
            return _post_json(
                f"{config['api_base'].rstrip('/')}/api/v2/runs/report",
                payload,
                timeout=int(config.get("v2_report_timeout_seconds") or 75),
            )
        except RuntimeError as error:
            if "timed out" not in str(error).lower() and "timeout" not in str(error).lower():
                raise
            time.sleep(2)
            try:
                return fetch_cloud_evaluation(config)
            except Exception:
                raise error
    upload_submission_batch(raw_results, config)
    return finalize_cloud_evaluation(scores, upload_mode, config)


def apply_cloud_evaluation(scores, raw_results, evaluation: dict) -> None:
    if not evaluation or not evaluation.get("success"):
        return

    if "total_score" in evaluation:
        scores.total_score = int(evaluation["total_score"])
    if "tier" in evaluation:
        scores.tier = str(evaluation["tier"])
    if "tier_name" in evaluation:
        scores.tier_name = str(evaluation["tier_name"])
    if "dimensions" in evaluation and isinstance(evaluation["dimensions"], dict):
        scores.dimensions = {key: int(value) for key, value in evaluation["dimensions"].items()}
    if "summary_comment" in evaluation:
        scores.summary_comment = str(evaluation["summary_comment"])
    if "judge_model" in evaluation:
        scores.judge_model = str(evaluation["judge_model"])
    if "partial" in evaluation:
        scores.partial = bool(evaluation["partial"])

    task_map = {item.task_id: item for item in raw_results}
    task_payloads = evaluation.get("task_scores") or evaluation.get("task_results") or []
    for task_score in task_payloads:
        task_id = task_score.get("task_id")
        if not task_id or task_id not in task_map:
            continue
        result = task_map[task_id]
        if "total_score" in task_score:
            result.total_score = int(task_score["total_score"])
        elif "task_score" in task_score:
            result.total_score = int(task_score["task_score"])
        if isinstance(task_score.get("rule_scores"), dict):
            result.rule_scores = {key: int(value) for key, value in task_score["rule_scores"].items()}
        if isinstance(task_score.get("ai_scores"), dict):
            result.ai_scores = {key: int(value) for key, value in task_score["ai_scores"].items()}
        if isinstance(task_score.get("scores"), dict):
            result.task_scores = {key: int(value) for key, value in task_score["scores"].items()}
        if isinstance(task_score.get("details"), dict):
            result.details = dict(task_score["details"])
        if isinstance(task_score.get("violations"), list):
            result.violations = [str(item) for item in task_score["violations"]]
        if "reasoning" in task_score:
            result.reasoning = str(task_score["reasoning"] or "")


def upload_score(scores, ref_code: str, config: dict) -> dict:
    payload = _base_payload(scores, ref_code)
    payload["task_version"] = config.get("task_bundle_version") or config.get("skill_version") or "1.0.0"
    return _post_json(f"{config['api_base'].rstrip('/')}/api/score", payload)


def register_ref(scores, ref_code: str | None, config: dict) -> dict:
    payload = _base_payload(scores, ref_code)
    headers = {}
    token = str(config.get("ref_register_token") or "").strip()
    if token:
        headers["X-GIGO-Ref-Register-Token"] = token
    response = _post_json(f"{config['api_base'].rstrip('/')}/api/ref/register", payload, headers=headers or None)
    if response.get("ref_code"):
        response.setdefault("success", True)
        response.setdefault("registered_only", True)
    return response

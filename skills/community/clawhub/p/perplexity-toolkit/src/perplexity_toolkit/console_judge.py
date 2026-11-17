"""Optional Jev judge layer for the resident console.

Design adapted from browser-use/jev-ultrafast (MIT, 2026-09-18):
- one batched TypeSafe request for several atomic questions (parallel pass);
- defensive response validation — a choice answer must be in the offered set,
  carry finite probabilities for exactly that set summing to ~1, and its
  ``choice`` must be the arg-max — otherwise the judgment is discarded;
- fail-open: any network/contract problem yields an "unavailable" judgment and
  the console pipeline continues unchanged;
- advisory output only: judgments are recorded in results / error hints and
  never alter pipeline behaviour.

Enable per call (``--judge``) or via ``PERPLEXITY_CONSOLE_JUDGE=1``. The API
key is read from ``TYPESAFE_API_KEY`` / ``JEV_API_KEY`` (environment first,
then ``~/.hermes/.env``; override the file with ``HERMES_ENV_FILE``).
"""

from __future__ import annotations

import json
import math
import os
import time
import urllib.request
from typing import Any, Callable, Optional

JEV_URL = "https://api.typesafe.ai/v1/systemone"
JEV_MODEL_DEFAULT = "jev-latest"
JEV_TIMEOUT = 12.0
_TRUTHY = {"1", "on", "true", "yes", "enabled"}

_ROUTE_OPTIONS = {
    "retry-step": "run the same step again as-is (the transient condition may be gone)",
    "reload-and-retry": "reload the page, then run the step again",
    "wait-longer": "wait, then retry (the page or the model may still be progressing)",
    "escalate": "stop and report to the human with the evidence",
}


def resolve_judge(flag: Optional[bool] = None) -> bool:
    """True when judging is enabled: explicit flag wins, else the env var."""
    if flag is not None:
        return bool(flag)
    return str(os.environ.get("PERPLEXITY_CONSOLE_JUDGE", "")).strip().lower() in _TRUTHY


def _api_key() -> Optional[str]:
    for name in ("TYPESAFE_API_KEY", "JEV_API_KEY"):
        value = os.environ.get(name)
        if value:
            return value.strip()
    env_path = os.path.expanduser(os.environ.get("HERMES_ENV_FILE", "~/.hermes/.env"))
    try:
        with open(env_path, encoding="utf-8") as fh:
            for line in fh:
                line = line.strip()
                if not line or line.startswith("#") or "=" not in line:
                    continue
                key, _, value = line.partition("=")
                if key.strip() in ("TYPESAFE_API_KEY", "JEV_API_KEY"):
                    value = value.strip().strip('"').strip("'")
                    if value:
                        return value
    except OSError:
        pass
    return None


def _valid_prob(value: Any) -> bool:
    return (isinstance(value, (int, float)) and not isinstance(value, bool)
            and math.isfinite(float(value)) and 0.0 <= float(value) <= 1.0)


def _validate_noul(answer: Any) -> bool:
    return isinstance(answer, dict) and _valid_prob(answer.get("noul"))


def _validate_choice(answer: Any, ids: set) -> bool:
    """Adapted from jev-ultrafast's validate_choice (MIT)."""
    try:
        probabilities = answer["probabilities"]
        numbers = [*probabilities.values(), answer["confidence"]]
        valid = (
            answer["choice"] in ids
            and set(probabilities) == set(ids)
            and all(_valid_prob(n) for n in numbers)
            and abs(sum(float(n) for n in probabilities.values()) - 1) < 0.02
            and float(probabilities[answer["choice"]]) >= max(float(n) for n in probabilities.values()) - 1e-6
        )
    except (KeyError, TypeError, ValueError):
        valid = False
    return valid


def _post_http(url: str, key: str, body: dict, timeout: float) -> dict:
    request = urllib.request.Request(
        url, data=json.dumps(body).encode("utf-8"),
        headers={"Authorization": f"Bearer {key}", "Content-Type": "application/json"},
        method="POST")
    with urllib.request.urlopen(request, timeout=timeout) as response:
        return json.loads(response.read().decode("utf-8"))


def jev_ask(state: str, questions: dict, *, key: Optional[str] = None,
            timeout: float = JEV_TIMEOUT,
            post: Optional[Callable[[str, str, dict, float], dict]] = None) -> dict:
    """One batched TypeSafe request with defensive validation.

    Returns ``{"ok": True, answers, model, latency_ms, usage}`` or
    ``{"ok": False, reason}`` — never raises.
    """
    api_key = key or _api_key()
    if not api_key:
        return {"ok": False, "reason": "no-api-key"}
    body = {
        "model": os.environ.get("PERPLEXITY_CONSOLE_JEV_MODEL", JEV_MODEL_DEFAULT),
        "state": state,
        "questions": questions,
    }
    started = time.monotonic()
    try:
        result = (post or _post_http)(JEV_URL, api_key, body, timeout)
    except Exception as exc:  # noqa: BLE001 — fail-open by design
        return {"ok": False, "reason": f"request-failed: {type(exc).__name__}: {str(exc)[:160]}"}
    answers = result.get("answers") if isinstance(result, dict) else None
    if not isinstance(answers, dict):
        return {"ok": False, "reason": "invalid-response: no answers"}
    for name, spec in questions.items():
        answer = answers.get(name)
        qtype = (spec or {}).get("type")
        if qtype == "noul":
            if not _validate_noul(answer):
                return {"ok": False, "reason": f"invalid-response: {name}"}
        elif qtype == "choice":
            ids = set((spec or {}).get("criteria") or {})
            if not _validate_choice(answer, ids):
                return {"ok": False, "reason": f"invalid-response: {name}"}
        else:
            return {"ok": False, "reason": f"invalid-response: unknown type {qtype!r}"}
    return {
        "ok": True,
        "answers": answers,
        "model": result.get("model") or "",
        "latency_ms": round((time.monotonic() - started) * 1000),
        "usage": result.get("usage") or {},
    }


def judge_extraction(query: str, answer: str, *,
                     client: Optional[Callable[..., dict]] = None,
                     flag: Optional[bool] = None) -> dict:
    """Advisory judgment on an extracted answer (question match + completeness)."""
    if not resolve_judge(flag):
        return {"enabled": False}
    if not query or not answer:
        return {"enabled": True, "status": "skipped", "reason": "no query/answer to judge"}
    state = json.dumps({"question": query[:6000], "answer": answer[:24000]}, ensure_ascii=False)
    questions = {
        "answers_question": {
            "type": "noul",
            "instructions": ("Does the extracted answer correctly answer the stated question, "
                             "without evasion? Judge the content only, not the style."),
        },
        "complete": {
            "type": "noul",
            "instructions": ("Does the answer appear complete and self-contained — not truncated "
                             "mid-sentence and not cut off by a stream that never finished?"),
        },
    }
    result = (client or jev_ask)(state, questions)
    if not result.get("ok"):
        return {"enabled": True, "status": "unavailable", "reason": result.get("reason")}
    answers = result["answers"]
    aq = float(answers["answers_question"]["noul"])
    cp = float(answers["complete"]["noul"])
    status = "ok" if min(aq, cp) >= 0.6 else ("review" if min(aq, cp) >= 0.4 else "concern")
    return {
        "enabled": True,
        "status": status,
        "answers_question": aq,
        "complete": cp,
        "model": result.get("model"),
        "latency_ms": result.get("latency_ms"),
    }


def route_hint(gate: Optional[str], code: Optional[str], message: str, *,
               client: Optional[Callable[..., dict]] = None,
               flag: Optional[bool] = None) -> dict:
    """Advisory recovery hint for a failed step (one Choice over the ladder)."""
    if not resolve_judge(flag):
        return {"enabled": False}
    if (code or "").startswith("pending."):
        # The recovery for these is deterministic and already stated in the
        # error message ("run console fill/submit first") — no judgment needed.
        return {"enabled": True, "status": "skipped",
                "reason": "deterministic pending guidance is already in the error message"}
    state = json.dumps({
        "context": ("Perplexity console (browser automation) step failure; the pipeline "
                    "already applied its built-in bounded recovery."),
        "gate": gate or "",
        "error_code": code or "",
        "error": (message or "")[:2000],
    }, ensure_ascii=False)
    questions = {
        "route": {
            "type": "choice",
            "instructions": "What should the operator do next for this failed step?",
            "criteria": dict(_ROUTE_OPTIONS),
        },
    }
    result = (client or jev_ask)(state, questions)
    if not result.get("ok"):
        return {"enabled": True, "status": "unavailable", "reason": result.get("reason")}
    answer = result["answers"]["route"]
    return {
        "enabled": True,
        "status": "ok",
        "route": answer["choice"],
        "confidence": float(answer["confidence"]),
        "probabilities": {k: float(v) for k, v in answer["probabilities"].items()},
        "model": result.get("model"),
        "latency_ms": result.get("latency_ms"),
    }

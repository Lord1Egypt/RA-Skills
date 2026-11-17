# Copyright (c) 2026 Ming Fang — MIT (vendored from perplexity-skill
# src/perplexity_toolkit/console_judge.py; design adapted from
# browser-use/jev-ultrafast, MIT, 2026-09-18)
"""Vendored TypeSafe Jev client helpers (console_judge.py, MIT).

Design adapted from browser-use/jev-ultrafast (MIT, 2026-09-18):
- one batched TypeSafe request for several atomic questions (parallel pass);
- defensive response validation — a choice answer must be in the offered set,
  carry finite probabilities for exactly that set summing to ~1, and its
  ``choice`` must be the arg-max — otherwise the judgment is discarded;
- fail-open: any network/contract problem surfaces as an error the caller
  maps to ``JevUnavailable``.

The API key is read from ``TYPESAFE_API_KEY`` / ``JEV_API_KEY`` (environment
first, then an optional env file pointed to by ``JEV_ENV_FILE``).

TypeSafe MCA §2.3(b): Jev outputs are never training labels.
"""

from __future__ import annotations

import json
import math
import os
import time
import urllib.request
from collections.abc import Callable
from typing import Any

JEV_URL = "https://api.typesafe.ai/v1/systemone"
JEV_MODEL_DEFAULT = "jev-latest"
JEV_TIMEOUT = 12.0


def _api_key() -> str | None:
    for name in ("TYPESAFE_API_KEY", "JEV_API_KEY"):
        value = os.environ.get(name)
        if value:
            return value.strip()
    env_path = os.environ.get("JEV_ENV_FILE")
    if not env_path:
        return None
    try:
        with open(os.path.expanduser(env_path), encoding="utf-8") as fh:
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
            and float(probabilities[answer["choice"]]) >= max(
                float(n) for n in probabilities.values()) - 1e-6
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


def jev_ask(state: str, questions: dict, *, key: str | None = None,
            timeout: float = JEV_TIMEOUT,
            post: Callable[[str, str, dict, float], dict] | None = None,
            url: str = JEV_URL) -> dict:
    """One batched TypeSafe request with defensive validation.

    Returns ``{"ok": True, answers, model, latency_ms, usage}`` or
    ``{"ok": False, reason}`` — never raises. (Adapted from console_judge.py:
    only the endpoint became a parameter so callers can override it.)
    """
    api_key = key or _api_key()
    if not api_key:
        return {"ok": False, "reason": "no-api-key"}
    body = {
        "model": os.environ.get("JEV_MODEL", JEV_MODEL_DEFAULT),
        "state": state,
        "questions": questions,
    }
    started = time.monotonic()
    try:
        result = (post or _post_http)(url, api_key, body, timeout)
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


def jev_ask_adapter(questions: list[dict], api_key: str | None = None,
                    endpoint: str | None = None) -> list[dict]:
    """Expose the vendored helpers as ``_jev_ask(questions, api_key, endpoint)``.

    The wrapper (policy.py) owns question construction, so ``state`` carries the
    questions' instructions (the decision context: goal + state signature).
    The endpoint URL and payload shape — ``{model, state, questions}`` POSTed to
    ``JEV_URL`` with Bearer auth — are taken verbatim from console_judge.jev_ask;
    questions are keyed ``q0, q1, ...`` because that API takes a dict.
    Returns the validated answers as a list in question order; raises on any
    network/contract problem (policy.JevClient maps it to JevUnavailable).
    """
    names = [f"q{i}" for i in range(len(questions))]
    spec = dict(zip(names, questions))
    state = "\n".join(str(q.get("instructions", "")) for q in questions)
    result = jev_ask(state, spec, key=api_key, url=endpoint or JEV_URL)
    if not result.get("ok"):
        raise RuntimeError(f"jev unavailable: {result.get('reason')}")
    answers = result["answers"]
    return [answers[name] for name in names]

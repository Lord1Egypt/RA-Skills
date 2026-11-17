#!/usr/bin/env python3
"""
llm_resolution — single source of truth for the LLM model used across the
memory toolkit.

Why this module exists
----------------------
Every script used to carry its own copy of a `PREFERRED_MODELS` tuple plus a
`resolve_llm_model()` function. That duplication broke production *twice*:

  * a bare `glm-5.2` was hard-coded while the daemon served `glm-5.2:cloud`
    -> Ollama answered 404 -> conflict arbitration died **silently**;
  * after the Ollama catalogue rotated, each script had to be patched by hand
    (v3.6.1, v3.6.2) to follow the operator's real default.

A list copied into N files re-breaks on every model swap. This module ends the
class of bug, not just its instance: the model comes from ONE place — the
gateway config (`agents.defaults.model.primary`).

Resolution order (highest precedence first)
-------------------------------------------
  1. Explicit override   — the caller's env var (`OLLAMA_MODEL`, `*_LLM_MODEL`)
                           or an `explicit=` argument. Kept visible and logged
                           (decision #2: these saved v3.6.0/v3.6.1).
  2. Gateway config      — `agents.defaults.model.primary` from openclaw.json.
  3. Configured fallback — `agents.defaults.model.fallbacks[0]`.
  4. Local safety net    — `qwen2.5:7b` (loopback, free). LAST resort only.

The safety net is validated for *presence* before it is handed out (see
`fallback_model()`), so a missing local model raises a clear error instead of
triggering a multi-GB synchronous Ollama pull that would hang the run
(spec V4 section 6.1).

Configuration source — scope of v4.0
------------------------------------
This module reads `~/.openclaw/openclaw.json` directly. It does NOT resolve
`$include` directives. Verified 2026-10-10: this deployment has no `$include`
and `agents.defaults.model` is inline. If the field cannot be found, the module
reports `source=missing` and falls through — it never invents a model. Resolving
`$include` is deferred until/unless the config is actually externalised.

Caching
-------
The config read is cached per process (`@lru_cache`), so a run that resolves the
model many times reads openclaw.json exactly once. Separate runs are separate
processes, so the cache never goes stale across runs.
"""

from __future__ import annotations

import json
import os
import sys
import urllib.parse
import urllib.request
from functools import lru_cache
from pathlib import Path

# ─── Constants ────────────────────────────────────────────────────────────────

# The local safety net. Loopback only, free, always the last link in the chain.
LOCAL_SAFETY_MODEL = "qwen2.5:7b"

# Loopback allowlist — same guard as hybrid_search.py / conflict_resolver.py /
# auto_capture.py / consolidate_advisor.py. A remote OLLAMA_URL would let memory
# content be POSTed off-machine, so it is refused at import time.
ALLOWED_OLLAMA_HOSTS = {"localhost", "127.0.0.1", "::1"}


def get_safe_ollama_url(env_var: str, default: str) -> str:
    """Validate and return an OLLAMA URL, restricting it to loopback only.

    Mirrors the guard in the other toolkit modules: the destination is fixed to
    localhost at import time, so a remote endpoint cannot receive memory content.
    """
    raw_url = os.environ.get(env_var, default)
    parsed = urllib.parse.urlparse(raw_url)
    if parsed.scheme not in ("http", "https"):
        raise ValueError(f"Invalid scheme for {env_var}: {parsed.scheme}")
    hostname = parsed.hostname or ""
    if hostname not in ALLOWED_OLLAMA_HOSTS:
        raise ValueError(
            f"Host '{hostname}' not allowed for {env_var}. Only localhost is permitted."
        )
    return raw_url


# Local Ollama endpoint. Loopback-only, enforced by the same guard the other
# modules use; never a remote host.
OLLAMA_LOCAL_URL = get_safe_ollama_url(
    "OLLAMA_URL", "http://127.0.0.1:11434"
).rstrip("/")

# Gateway config path (override with OPENCLAW_CONFIG for tests).
CONFIG_PATH = Path(
    os.environ.get("OPENCLAW_CONFIG", str(Path.home() / ".openclaw" / "openclaw.json"))
)

# Explicit overrides, checked in this order. Each is the historical env var the
# owning script understands, so callers keep working unchanged.
_OVERRIDE_ENV_ORDER = (
    "OLLAMA_MODEL",
    "TRACE_LLM_MODEL",
    "CONFLICT_LLM_MODEL",
    "AUTO_CAPTURE_MODEL",
)


# ─── Gateway config read (cached per process) ─────────────────────────────────


@lru_cache(maxsize=1)
def _read_gateway_config() -> dict:
    """Read openclaw.json once per process. Returns {} on any failure.

    Deliberately does NOT resolve `$include`: out of scope for v4.0 (see module
    docstring). A missing/unreadable file yields {}, which makes every downstream
    lookup report `source=missing` rather than crash.
    """
    try:
        return json.loads(CONFIG_PATH.read_text())
    except Exception:
        return {}


def _gateway_model_field(field: str):
    """Return `agents.defaults.model.<field>` from the config, or None."""
    try:
        return (
            _read_gateway_config()
            .get("agents", {})
            .get("defaults", {})
            .get("model", {})
            .get(field)
        )
    except Exception:
        return None


def _strip_provider(model: str) -> str:
    """`ollama/deepseek-v4.1-flash:cloud` -> `deepseek-v4.1-flash:cloud`.

    Scripts talk to the Ollama daemon directly (no OpenClaw provider routing),
    so the provider prefix must be removed before a model name is sent.
    """
    if not model:
        return model
    if "/" in model:
        return model.split("/", 1)[1]
    return model


# ─── Local model presence ─────────────────────────────────────────────────────


@lru_cache(maxsize=1)
def _served_models() -> frozenset:
    """Names the local Ollama daemon currently serves. Empty set if unreachable."""
    try:
        url = OLLAMA_LOCAL_URL + "/api/tags"
        with urllib.request.urlopen(url, timeout=5) as resp:
            data = json.loads(resp.read())
        return frozenset(m.get("name", "") for m in data.get("models", []))
    except Exception:
        return frozenset()


def is_locally_served(model: str) -> bool:
    """True when the daemon serves this exact model name."""
    return model in _served_models()


# ─── Public API ───────────────────────────────────────────────────────────────


def resolve_llm_model(explicit: str | None = None,
                      override_env: str | None = None,
                      require_local_presence: bool = False) -> str:
    """Resolve the model to use, following the documented precedence.

    Args:
        explicit: caller-supplied model. Highest precedence; returned as-is
            (provider prefix stripped) even if the daemon does not serve it —
            an explicit choice is the operator's, not ours.
        override_env: name of the env var this caller treats as its explicit
            override (e.g. "CONFLICT_LLM_MODEL"). Checked before the generic
            override chain, preserving each script's historical behaviour.
        require_local_presence: when True, a local model is only returned if the
            daemon actually serves it; otherwise raise RuntimeError instead of
            handing out a name that would trigger a synchronous pull.

    Returns:
        A model name with no provider prefix.

    Raises:
        RuntimeError: only when `require_local_presence=True` and the resolved
            local model is not served (spec v4 section 6.1 — no silent hang).
    """
    # 1. Caller-specific override env, then the generic override chain.
    env_names = ([override_env] if override_env else []) + list(_OVERRIDE_ENV_ORDER)
    for name in env_names:
        val = (os.environ.get(name) or "").strip()
        if val:
            return _strip_provider(val)

    # 2. Gateway default.
    primary = _gateway_model_field("primary")
    if primary:
        return _strip_provider(primary)

    # 3. Configured fallback.
    fallbacks = _gateway_model_field("fallbacks") or []
    if isinstance(fallbacks, list) and fallbacks:
        return _strip_provider(fallbacks[0])

    # 4. Local safety net.
    return fallback_model(require_presence=require_local_presence)


def fallback_model(require_presence: bool = True) -> str:
    """Return the local safety-net model, validating it is really available.

    With `require_presence=True` (the default for the *last* link of the chain),
    a missing local model raises RuntimeError with an actionable message rather
    than letting Ollama start a multi-GB synchronous pull that would hang the
    run and violate the no-silent-failure invariant.
    """
    if require_presence and not is_locally_served(LOCAL_SAFETY_MODEL):
        raise RuntimeError(
            f"Local fallback model '{LOCAL_SAFETY_MODEL}' is not served by "
            f"{OLLAMA_LOCAL_URL}. Ollama would attempt a synchronous multi-GB "
            f"pull, hanging this run. Fix: `ollama pull {LOCAL_SAFETY_MODEL}`, "
            f"or set an explicit override (OLLAMA_MODEL / *_LLM_MODEL)."
        )
    return LOCAL_SAFETY_MODEL


def explain_resolution(explicit: str | None = None,
                       override_env: str | None = None) -> dict:
    """Return WHY a model was chosen — for logs and tests.

    Shape: {model, source, candidates, config_path, local_served}
      source ∈ {explicit, override_env:<NAME>, gateway:primary,
                gateway:fallback, local_safety, error}
    """
    info = {
        "config_path": str(CONFIG_PATH),
        "local_served": is_locally_served(LOCAL_SAFETY_MODEL),
    }
    if explicit:
        info.update(model=_strip_provider(explicit), source="explicit")
        return info

    env_names = ([override_env] if override_env else []) + list(_OVERRIDE_ENV_ORDER)
    for name in env_names:
        val = (os.environ.get(name) or "").strip()
        if val:
            info.update(model=_strip_provider(val), source=f"override_env:{name}")
            return info

    primary = _gateway_model_field("primary")
    if primary:
        info.update(model=_strip_provider(primary), source="gateway:primary")
        return info

    fallbacks = _gateway_model_field("fallbacks") or []
    if isinstance(fallbacks, list) and fallbacks:
        info.update(model=_strip_provider(fallbacks[0]), source="gateway:fallback")
        return info

    info.update(model=LOCAL_SAFETY_MODEL, source="local_safety")
    if not info["local_served"]:
        info["source"] = "error"
        info["hint"] = (
            f"local safety model '{LOCAL_SAFETY_MODEL}' is not served — "
            f"`ollama pull {LOCAL_SAFETY_MODEL}`"
        )
    return info


def log_resolution(prefix: str = "[memory-toolkit]", explicit: str | None = None,
                   override_env: str | None = None) -> str:
    """Log the resolved model + its source to stderr. Returns the model name."""
    info = explain_resolution(explicit=explicit, override_env=override_env)
    print(f"{prefix} resolved model = {info['model']} (source={info['source']})",
          file=sys.stderr)
    if info["source"] == "error":
        print(f"{prefix} WARNING: {info.get('hint', '')}", file=sys.stderr)
    return info["model"]


if __name__ == "__main__":  # pragma: no cover - manual inspection helper
    print(json.dumps(explain_resolution(), indent=2, ensure_ascii=False))

"""
models.py — OpenRouter model registry.

Public API
----------
get_ranked_free_models(api_key, refresh=False) -> list[dict]
    Returns free models sorted best-first, using a 6-hour cache.

cache_summary() -> str
    Human-readable cache age / model count.

is_rate_limited(model_id) -> bool
mark_rate_limited(model_id)
clear_rate_limits()
expire_stale_rate_limits() -> list[str]   # returns expired IDs
"""

import json
import time
from datetime import datetime, timedelta
from pathlib import Path
from typing import Optional

import requests


# ── OpenRouter endpoint ────────────────────────────────────────────────────────
MODELS_URL = "https://openrouter.ai/api/v1/models"

# ── Local state directory ──────────────────────────────────────────────────────
_DIR          = Path.home() / ".infinity-router"
_CACHE_FILE   = _DIR / "model-cache.json"
_RL_FILE      = _DIR / "rate-limits.json"
CACHE_TTL_H   = 6
COOLDOWN_MIN  = 30

# ── Ranking weights (must sum to 1.0) ─────────────────────────────────────────
_W_TOOLS    = 0.35   # tool/function calling support (critical for coding agents)
_W_CONTEXT  = 0.30   # context window length
_W_RECENCY  = 0.20   # model freshness
_W_PROVIDER = 0.10   # provider trust
_W_CAPS     = 0.05   # other supported parameters

# ── Trusted providers (index 0 = most trusted) ────────────────────────────────
_PROVIDERS = [
    "meta-llama", "mistralai", "deepseek",
    "nvidia", "qwen", "microsoft", "google", "allenai", "arcee-ai",
]

# ── Model families known to NOT support tool/function calling ─────────────────
# These models may claim "tools" in supported_parameters but fail at runtime.
_NO_TOOL_FAMILIES = (
    "gemma",    # Google Gemma series — no real function calling
    "gemma-2",
    "gemma-3",
)


def _has_real_tool_support(model: dict) -> bool:
    """
    Return False for model families known to fake or lack tool support
    even when listed in supported_parameters.
    """
    mid = model.get("id", "").lower()
    return not any(fam in mid for fam in _NO_TOOL_FAMILIES)


# ──────────────────────────────────────────────────────────────────────────────
# Fetch & filter
# ──────────────────────────────────────────────────────────────────────────────

def _fetch(api_key: str) -> list[dict]:
    try:
        r = requests.get(
            MODELS_URL,
            headers={"Authorization": f"Bearer {api_key}"},
            timeout=30,
        )
        r.raise_for_status()
        return r.json().get("data", [])
    except requests.RequestException as exc:
        raise ConnectionError(f"OpenRouter API unreachable: {exc}") from exc


# ── Model IDs / name fragments that are NOT chat/text models ──────────────────
# (audio generation, image generation, video generation, embedding-only, etc.)
_NON_CHAT_PATTERNS = (
    "lyria", "imagen", "veo", "dall-e", "stable-diffusion",
    "sdxl", "musicgen", "audiogen", "whisper", "tts",
    "text-embedding", "embedding",
)


def _is_chat_model(model: dict) -> bool:
    """
    Return True only for text-in / text-out chat models.
    Rejects audio, image, video, and embedding models.

    Strategy (in order):
    1. Check architecture.modality — must produce text output.
    2. Fall back to name-based heuristic if modality is absent.
    """
    model_id = model.get("id", "").lower()

    # Name-based fast reject
    if any(pat in model_id for pat in _NON_CHAT_PATTERNS):
        return False

    # Modality check — OpenRouter reports e.g. "text->text", "text+image->text",
    # "audio->audio", "text->image".  We require "->text" in the output side.
    arch     = model.get("architecture") or {}
    modality = arch.get("modality", "")
    if modality:
        output = modality.split("->")[-1].strip().lower()
        return "text" in output

    # No modality info — assume it's a chat model (conservative default)
    return True


def _is_free(model: dict) -> bool:
    if ":free" in model.get("id", ""):
        return True
    try:
        return float(model.get("pricing", {}).get("prompt", 1)) == 0
    except (TypeError, ValueError):
        return False


# ──────────────────────────────────────────────────────────────────────────────
# Scoring
# ──────────────────────────────────────────────────────────────────────────────

def score_model(model: dict) -> float:
    """Produce a 0.0–1.0 quality score."""
    s    = 0.0
    caps = model.get("supported_parameters") or []

    # Tool / function calling support — highest weight (coding agents need this)
    # OpenRouter reports "tools" or "tool_choice" in supported_parameters,
    # but some model families (e.g. Gemma) claim tools yet fail at runtime.
    has_tools = (
        any(p in caps for p in ("tools", "tool_choice"))
        and _has_real_tool_support(model)
    )
    s += (1.0 if has_tools else 0.0) * _W_TOOLS

    # Context length — ceiling at 1 M tokens
    s += min(model.get("context_length", 0) / 1_000_000, 1.0) * _W_CONTEXT

    # Recency — linear decay over 365 days
    created = model.get("created", 0)
    if created:
        age = (time.time() - created) / 86_400
        s += max(0.0, 1.0 - age / 365) * _W_RECENCY

    # Provider trust
    provider = (model.get("id", "").split("/") or [""])[0]
    if provider in _PROVIDERS:
        s += (1.0 - _PROVIDERS.index(provider) / len(_PROVIDERS)) * _W_PROVIDER

    # Other capabilities (minor bonus)
    s += min(len(caps) / 10, 1.0) * _W_CAPS

    return round(s, 4)


# ──────────────────────────────────────────────────────────────────────────────
# Cache
# ──────────────────────────────────────────────────────────────────────────────

def _load_cache() -> Optional[list[dict]]:
    if not _CACHE_FILE.exists():
        return None
    try:
        data = json.loads(_CACHE_FILE.read_text())
        ts   = datetime.fromisoformat(data["cached_at"])
        if datetime.now() - ts < timedelta(hours=CACHE_TTL_H):
            return data["models"]
    except (KeyError, ValueError, json.JSONDecodeError):
        pass
    return None


def _save_cache(models: list[dict]) -> None:
    _DIR.mkdir(parents=True, exist_ok=True)
    _CACHE_FILE.write_text(json.dumps(
        {"cached_at": datetime.now().isoformat(), "models": models},
        indent=2,
    ))


def cache_summary() -> str:
    if not _CACHE_FILE.exists():
        return "no cache"
    try:
        data = json.loads(_CACHE_FILE.read_text())
        ts   = datetime.fromisoformat(data["cached_at"])
        diff = datetime.now() - ts
        h    = diff.seconds // 3600
        m    = (diff.seconds % 3600) // 60
        n    = len(data.get("models", []))
        return f"{n} models, updated {h}h {m}m ago"
    except Exception:
        return "invalid cache"


# ──────────────────────────────────────────────────────────────────────────────
# Public model API
# ──────────────────────────────────────────────────────────────────────────────

def get_ranked_free_models(api_key: str, refresh: bool = False) -> list[dict]:
    """Return free models sorted best-first. Uses cache unless refresh=True."""
    if not refresh:
        cached = _load_cache()
        if cached is not None:
            return cached

    raw    = _fetch(api_key)
    free   = [m for m in raw if _is_free(m) and _is_chat_model(m)]
    ranked = sorted(free, key=score_model, reverse=True)
    ranked = [{**m, "_score": score_model(m)} for m in ranked]

    _save_cache(ranked)
    return ranked


# ──────────────────────────────────────────────────────────────────────────────
# Rate-limit state
# ──────────────────────────────────────────────────────────────────────────────

def _load_rl() -> dict:
    if _RL_FILE.exists():
        try:
            return json.loads(_RL_FILE.read_text())
        except json.JSONDecodeError:
            pass
    return {}


def _save_rl(rl: dict) -> None:
    _DIR.mkdir(parents=True, exist_ok=True)
    _RL_FILE.write_text(json.dumps(rl, indent=2))


def is_rate_limited(model_id: str) -> bool:
    ts_str = _load_rl().get(model_id)
    if not ts_str:
        return False
    try:
        return datetime.now() - datetime.fromisoformat(ts_str) < timedelta(minutes=COOLDOWN_MIN)
    except ValueError:
        return False


def mark_rate_limited(model_id: str) -> None:
    rl = _load_rl()
    rl[model_id] = datetime.now().isoformat()
    _save_rl(rl)


def clear_rate_limits() -> None:
    _save_rl({})


def expire_stale_rate_limits() -> list[str]:
    """Remove expired entries. Returns the list of expired model IDs."""
    rl      = _load_rl()
    now     = datetime.now()
    expired = [
        k for k, v in rl.items()
        if now - datetime.fromisoformat(v) >= timedelta(minutes=COOLDOWN_MIN)
    ]
    for k in expired:
        del rl[k]
    if expired:
        _save_rl(rl)
    return expired

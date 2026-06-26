"""
targets.py — Config-target writers for Infinity-Router.

A "target" is any AI coding tool whose model config we can read and write.

Supported targets
-----------------
openclaw     ~/.openclaw/openclaw.json   primary + fallback chain
claude-code  ~/.claude/settings.json    primary model only

Public API
----------
get_target(name="openclaw") -> BaseTarget
detect_target()             -> BaseTarget   (first found, or openclaw)
list_targets()              -> list of (name, BaseTarget)
fmt_primary(model_id)       -> OpenClaw "openrouter/…" primary format
fmt_list(model_id)          -> OpenClaw allowlist format (no routing prefix)
FREE_ROUTER                 -> "openrouter/free" smart-router placeholder
"""

import json
from abc import ABC, abstractmethod
from pathlib import Path
from typing import Optional


FREE_ROUTER = "openrouter/free"


# ──────────────────────────────────────────────────────────────────────────────
# ID formatting helpers (OpenClaw convention)
# ──────────────────────────────────────────────────────────────────────────────

def fmt_primary(model_id: str) -> str:
    """
    Format for openclaw agents.defaults.model.primary.
    Always has the 'openrouter/' routing prefix.
    """
    if model_id in (FREE_ROUTER, f"{FREE_ROUTER}:free"):
        return "openrouter/openrouter/free"
    base = model_id.removeprefix("openrouter/")
    return f"openrouter/{base}"


def fmt_list(model_id: str) -> str:
    """
    Format for openclaw agents.defaults.models allowlist.
    No routing prefix — just the raw API model ID.
    """
    if model_id in (FREE_ROUTER, f"{FREE_ROUTER}:free"):
        return FREE_ROUTER
    return model_id.removeprefix("openrouter/")


# ──────────────────────────────────────────────────────────────────────────────
# Abstract base
# ──────────────────────────────────────────────────────────────────────────────

class BaseTarget(ABC):
    name: str    # short identifier used on the CLI
    label: str   # human-readable name for output

    @abstractmethod
    def exists(self) -> bool:
        """Return True if the target config file is present."""

    @abstractmethod
    def read_primary(self) -> Optional[str]:
        """Return the currently active primary model ID, or None."""

    @abstractmethod
    def write_primary(self, model_id: str) -> None:
        """Set model_id as the primary model."""

    def read_fallbacks(self) -> list[str]:
        return []

    def write_fallbacks(self, model_ids: list[str]) -> None:
        pass   # not all targets support fallback lists


# ──────────────────────────────────────────────────────────────────────────────
# OpenClaw
# ──────────────────────────────────────────────────────────────────────────────

_OPENCLAW_PATH = Path.home() / ".openclaw" / "openclaw.json"


def _oc_load() -> dict:
    if _OPENCLAW_PATH.exists():
        try:
            return json.loads(_OPENCLAW_PATH.read_text())
        except json.JSONDecodeError:
            pass
    return {}


def _oc_save(cfg: dict) -> None:
    _OPENCLAW_PATH.parent.mkdir(parents=True, exist_ok=True)
    _OPENCLAW_PATH.write_text(json.dumps(cfg, indent=2))


def _oc_ensure(cfg: dict) -> dict:
    """Guarantee the nested keys exist and are the correct types.
    Overwrites any key that exists but holds the wrong type (e.g. a bare string).
    """
    if not isinstance(cfg.get("agents"), dict):
        cfg["agents"] = {}
    if not isinstance(cfg["agents"].get("defaults"), dict):
        cfg["agents"]["defaults"] = {}
    if not isinstance(cfg["agents"]["defaults"].get("model"), dict):
        cfg["agents"]["defaults"]["model"] = {}
    if not isinstance(cfg["agents"]["defaults"].get("models"), dict):
        cfg["agents"]["defaults"]["models"] = {}
    return cfg


class OpenClawTarget(BaseTarget):
    name  = "openclaw"
    label = "OpenClaw"

    def exists(self) -> bool:
        return _OPENCLAW_PATH.exists()

    def _model_section(self) -> dict:
        """Return agents.defaults.model as a dict, guarding against non-dict values."""
        cfg      = _oc_load()
        agents   = cfg.get("agents")
        if not isinstance(agents, dict):
            return {}
        defaults = agents.get("defaults")
        if not isinstance(defaults, dict):
            return {}
        model    = defaults.get("model")
        return model if isinstance(model, dict) else {}

    def read_primary(self) -> Optional[str]:
        return self._model_section().get("primary")

    def read_fallbacks(self) -> list[str]:
        fbs = self._model_section().get("fallbacks", [])
        return fbs if isinstance(fbs, list) else []

    def write_primary(self, model_id: str) -> None:
        cfg = _oc_ensure(_oc_load())
        cfg["agents"]["defaults"]["model"]["primary"] = fmt_primary(model_id)
        cfg["agents"]["defaults"]["models"][fmt_list(model_id)] = {}
        _oc_save(cfg)

    def write_fallbacks(self, model_ids: list[str]) -> None:
        cfg = _oc_ensure(_oc_load())
        fallbacks = []
        for mid in model_ids:
            entry = fmt_list(mid)
            fallbacks.append(entry)
            cfg["agents"]["defaults"]["models"][entry] = {}
        cfg["agents"]["defaults"]["model"]["fallbacks"] = fallbacks
        _oc_save(cfg)

    def ensure_auth_profile(self) -> None:
        """Insert openrouter:default auth profile if absent."""
        cfg = _oc_load()
        cfg.setdefault("auth", {})
        cfg["auth"].setdefault("profiles", {})
        if "openrouter:default" not in cfg["auth"]["profiles"]:
            cfg["auth"]["profiles"]["openrouter:default"] = {
                "provider": "openrouter",
                "mode": "api_key",
            }
            _oc_save(cfg)
            print("  [openclaw] Added openrouter:default auth profile.")

    def clear_model_config(self) -> None:
        cfg = _oc_ensure(_oc_load())
        cfg["agents"]["defaults"]["model"]  = {}
        cfg["agents"]["defaults"]["models"] = {}
        _oc_save(cfg)


# ──────────────────────────────────────────────────────────────────────────────
# Claude Code
# ──────────────────────────────────────────────────────────────────────────────

_CLAUDE_PATH = Path.home() / ".claude" / "settings.json"


class ClaudeCodeTarget(BaseTarget):
    """
    Writes the model key to ~/.claude/settings.json.
    Fallback lists are not supported here.
    Note: Claude Code uses Anthropic model IDs, not OpenRouter IDs.
    """
    name  = "claude-code"
    label = "Claude Code"

    def exists(self) -> bool:
        return _CLAUDE_PATH.exists()

    def _load(self) -> dict:
        if _CLAUDE_PATH.exists():
            try:
                return json.loads(_CLAUDE_PATH.read_text())
            except json.JSONDecodeError:
                pass
        return {}

    def _save(self, cfg: dict) -> None:
        _CLAUDE_PATH.parent.mkdir(parents=True, exist_ok=True)
        _CLAUDE_PATH.write_text(json.dumps(cfg, indent=2))

    def read_primary(self) -> Optional[str]:
        return self._load().get("model")

    def write_primary(self, model_id: str) -> None:
        cfg = self._load()
        cfg["model"] = model_id
        self._save(cfg)

    def clear_model_config(self) -> None:
        cfg = self._load()
        cfg.pop("model", None)
        self._save(cfg)


# ──────────────────────────────────────────────────────────────────────────────
# Registry
# ──────────────────────────────────────────────────────────────────────────────

_REGISTRY: dict[str, BaseTarget] = {
    "openclaw":    OpenClawTarget(),
    "claude-code": ClaudeCodeTarget(),
}


def get_target(name: str = "openclaw") -> BaseTarget:
    t = _REGISTRY.get(name)
    if t is None:
        valid = ", ".join(_REGISTRY)
        raise ValueError(f"Unknown target '{name}'. Valid options: {valid}")
    return t


def detect_target() -> BaseTarget:
    """Return the first target whose config file exists, else OpenClaw."""
    for t in _REGISTRY.values():
        if t.exists():
            return t
    return _REGISTRY["openclaw"]


def list_targets() -> list[tuple[str, BaseTarget]]:
    return list(_REGISTRY.items())

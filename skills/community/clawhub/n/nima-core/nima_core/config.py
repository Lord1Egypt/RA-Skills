"""
nima_core.config
~~~~~~~~~~~~~~~~
Single source of truth for all environment variables.

Replaces scattered os.environ.get() calls across the codebase.
All modules should import from here instead of reading env vars directly.

Deprecated aliases (still read for backward compat, emit no warnings):
  NIMA_DB        -> use NIMA_DB_PATH
  NIMA_SQLITE_DB -> use NIMA_DB_PATH
  LILU_WORKSPACE -> use OPENCLAW_WORKSPACE
"""
import os
from pathlib import Path


# ── Safe env-var helpers ──────────────────────────────────────────────────────

def _get_env_int(key: str, default: int) -> int:
    """Return *key* from the environment as ``int``, falling back to *default* on missing/invalid values."""
    try:
        return int(os.environ.get(key, default))
    except (ValueError, TypeError):
        return default


def _get_env_float(key: str, default: float) -> float:
    """Return *key* from the environment as ``float``, falling back to *default* on missing/invalid values."""
    try:
        return float(os.environ.get(key, default))
    except (ValueError, TypeError):
        return default


# ── Core paths ────────────────────────────────────────────────────────────────
NIMA_HOME: Path = Path(
    os.path.expanduser(os.environ.get("NIMA_HOME", "~/.nima"))
)

# Canonical DB path (consolidates NIMA_DB, NIMA_SQLITE_DB, NIMA_DB_PATH)
NIMA_DB_PATH: Path = Path(
    os.path.expanduser(
        os.environ.get(
            "NIMA_DB_PATH",
            os.environ.get(
                "NIMA_DB",
                os.environ.get(
                    "NIMA_SQLITE_DB",
                    str(NIMA_HOME / "memory" / "graph.sqlite"),
                ),
            ),
        )
    )
)

NIMA_MEMORY_DIR: Path = Path(
    os.path.expanduser(os.environ.get("NIMA_MEMORY_DIR", str(NIMA_HOME / "memory")))
)

NIMA_DATA_DIR: Path = Path(
    os.path.expanduser(os.environ.get("NIMA_DATA_DIR", str(NIMA_HOME / "memory")))
)

NIMA_DREAMS_DIR: Path = Path(
    os.path.expanduser(os.environ.get("NIMA_DREAMS_DIR", str(NIMA_HOME / "dreams")))
)

# ── OpenClaw paths ────────────────────────────────────────────────────────────
# Canonical workspace path (consolidates OPENCLAW_WORKSPACE and LILU_WORKSPACE)
OPENCLAW_WORKSPACE: Path = Path(
    os.path.expanduser(
        os.environ.get(
            "OPENCLAW_WORKSPACE",
            os.environ.get(
                "LILU_WORKSPACE",
                "~/.openclaw/workspace",
            ),
        )
    )
)

OPENCLAW_CONFIG: Path = Path(
    os.path.expanduser(os.environ.get("OPENCLAW_CONFIG", "~/.openclaw/openclaw.json"))
)

# ── LLM config ────────────────────────────────────────────────────────────────
NIMA_LLM_PROVIDER: str = os.environ.get("NIMA_LLM_PROVIDER", "")
NIMA_LLM_API_KEY: str = os.environ.get("NIMA_LLM_API_KEY", os.environ.get("NIMA_LLM_KEY", ""))
NIMA_LLM_BASE_URL: str = os.environ.get("NIMA_LLM_BASE_URL", os.environ.get("NIMA_LLM_BASE", ""))
NIMA_LLM_MODEL: str = os.environ.get("NIMA_LLM_MODEL", "qwen3.5:cloud")
NIMA_DISTILL_MODEL: str = os.environ.get("NIMA_DISTILL_MODEL", "claude-haiku-4-5")
NIMA_BOT_NAME: str = os.environ.get("NIMA_BOT_NAME", "bot")

# Backward-compatible aliases for legacy imports
NIMA_LLM_BASE: str = NIMA_LLM_BASE_URL
NIMA_LLM_KEY: str = NIMA_LLM_API_KEY

# ── API keys ──────────────────────────────────────────────────────────────────
OPENAI_API_KEY: str = os.environ.get("OPENAI_API_KEY", "")
ANTHROPIC_API_KEY: str = os.environ.get("ANTHROPIC_API_KEY", "")
ANTHROPIC_BASE_URL: str = os.environ.get("ANTHROPIC_BASE_URL", "https://api.anthropic.com")
OPENAI_BASE_URL: str = os.environ.get("OPENAI_BASE_URL", "https://api.openai.com/v1")
VOYAGE_API_KEY: str = os.environ.get("VOYAGE_API_KEY", "")
NIMA_HMAC_KEY: str = os.environ.get("NIMA_HMAC_KEY", "")

# ── Logging ───────────────────────────────────────────────────────────────────
NIMA_LOG_LEVEL: str = os.environ.get("NIMA_LOG_LEVEL", "INFO").upper()

# ── Darwin / Darwinism ────────────────────────────────────────────────────────
DARWIN_THRESHOLD: float = _get_env_float("DARWIN_THRESHOLD", 0.85)
DARWIN_MAX_CLUSTER: int = _get_env_int("DARWIN_MAX_CLUSTER", 5)
DARWIN_MIN_TEXT: int = _get_env_int("DARWIN_MIN_TEXT", 20)
DARWIN_LLM_ENDPOINT: str = os.environ.get(
    "DARWIN_LLM_ENDPOINT", "https://ollama.com/v1/chat/completions"
)
DARWIN_LLM_MODEL: str = os.environ.get("DARWIN_LLM_MODEL", "gemini-3-flash-preview")

# ── Dream subsystem ───────────────────────────────────────────────────────────
NIMA_MAX_INSIGHTS: int = _get_env_int("NIMA_MAX_INSIGHTS", 500)
NIMA_MAX_PATTERNS: int = _get_env_int("NIMA_MAX_PATTERNS", 200)
NIMA_MAX_DREAM_LOG: int = _get_env_int("NIMA_MAX_DREAM_LOG", 100)
NIMA_DREAM_HOURS: int = _get_env_int("NIMA_DREAM_HOURS", 24)
NIMA_DREAM_MAX_MEMORIES: int = _get_env_int("NIMA_DREAM_MAX_MEMORIES", 500)

# ── Memory pruner ─────────────────────────────────────────────────────────────
NIMA_CAPTURE_CLI: str = os.environ.get("NIMA_CAPTURE_CLI", "")
NIMA_TRACKED_FILES: str = os.environ.get("NIMA_TRACKED_FILES", "MEMORY.md,LILU_STATUS.md")

# ── Storage backend ───────────────────────────────────────────────────────────
# Canonical var: NIMA_DB_BACKEND (values: "sqlite" | "ladybug")
# Deprecated aliases (read for backward compat, no warnings emitted):
#   NIMA_STORE            — previous canonical name
#   NIMA_LADYBUG_ENABLED  — Knox legacy; "true" maps to "ladybug"
def _resolve_db_backend() -> str:
    """Resolve NIMA_DB_BACKEND with fallback chain for deprecated aliases."""
    val = os.environ.get("NIMA_DB_BACKEND", "").lower().strip()
    if val in ("sqlite", "ladybug"):
        return val
    # Fallback 1: NIMA_STORE
    val = os.environ.get("NIMA_STORE", "").lower().strip()
    if val in ("sqlite", "ladybug"):
        return val
    # Fallback 2: NIMA_LADYBUG_ENABLED (Knox legacy)
    if os.environ.get("NIMA_LADYBUG_ENABLED", "").lower().strip() == "true":
        return "ladybug"
    return "sqlite"

NIMA_DB_BACKEND: str = _resolve_db_backend()
NIMA_USE_LADYBUG: bool = NIMA_DB_BACKEND == "ladybug"

# LadybugDB path (used when NIMA_DB_BACKEND=ladybug)
NIMA_LADYBUG_DB: Path = Path(
    os.path.expanduser(
        os.environ.get("NIMA_LADYBUG_DB", str(NIMA_HOME / "memory" / "ladybug.lbug"))
    )
)


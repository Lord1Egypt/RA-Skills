import os
import re
from datetime import datetime, timezone
from pathlib import Path

TRADING_DAYS_PER_YEAR: int = 252

DEFAULT_ASSETS: list[str] = [
    "XLC", "XLY", "XLP", "XLE", "XLF", "XLV", "XLI", "XLB",
    "XLRE", "XLK", "XLU", "GLD", "DBC", "TLT",
]


def get_project_root() -> Path:
    override = os.environ.get("MPT_PROJECT_ROOT")
    if override:
        return Path(override).resolve()
    # Walk up from this file looking for a known project marker rather than
    # assuming a fixed directory depth — the package may be installed or
    # mounted in varying structures (e.g. OpenClaw workspaces).
    _markers = ("config/default.yaml", "pyproject.toml")
    candidate = Path(__file__).resolve().parent.parent
    for _ in range(5):
        if any((candidate / m).exists() for m in _markers):
            return candidate
        candidate = candidate.parent
    return Path(__file__).resolve().parent.parent


def get_portfolios_dir() -> Path:
    d = get_project_root() / "portfolios"
    d.mkdir(exist_ok=True)
    return d


def get_portfolio_dir(name: str) -> Path:
    d = get_portfolios_dir() / name
    if not d.exists():
        raise FileNotFoundError(f"Portfolio '{name}' not found at {d}")
    return d


def get_portfolio_reports_dir(name: str) -> Path:
    d = get_portfolio_dir(name) / "reports"
    d.mkdir(exist_ok=True)
    return d


def validate_portfolio_name(name: str) -> str:
    if not re.match(r"^[a-zA-Z0-9][a-zA-Z0-9_-]*$", name):
        raise ValueError(
            f"Invalid portfolio name '{name}'. "
            "Use alphanumeric characters, hyphens, and underscores only. "
            "Must start with a letter or digit."
        )
    return name


def timestamp_str() -> str:
    return datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")


def resolve_env_vars(value: str) -> str:
    """Resolve ${VAR_NAME} patterns from environment variables."""
    if not isinstance(value, str):
        return value
    pattern = re.compile(r"\$\{([^}]+)\}")
    def replacer(match: re.Match) -> str:
        var_name = match.group(1)
        env_val = os.environ.get(var_name)
        if env_val is None:
            raise ValueError(f"Environment variable '{var_name}' not set")
        return env_val
    return pattern.sub(replacer, value)

"""Configuration management for git-log-tracker."""

import fnmatch
import json
from pathlib import Path

DEFAULT_CONFIG_DIR = Path.home() / ".commit-logs"
DEFAULT_CONFIG_PATH = DEFAULT_CONFIG_DIR / "config.toml"
DEFAULT_LABELS_PATH = DEFAULT_CONFIG_DIR / "labels.json"


def read_config(config_path: Path | None = None) -> dict:
    """Read configuration from TOML file."""
    if config_path is None:
        config_path = DEFAULT_CONFIG_PATH

    if not config_path.exists():
        return {"hooks": {"exclude": []}, "database": {"path": "index.db"}}

    try:
        import tomllib
    except ImportError:
        import tomli as tomllib

    with open(config_path, "rb") as f:
        return tomllib.load(f)


def is_excluded_repo(repo_path: str, config: dict) -> bool:
    """Check if repo_path matches any exclude pattern."""
    excludes = config.get("hooks", {}).get("exclude", [])
    normalized = repo_path.replace("\\", "/")
    for pattern in excludes:
        if fnmatch.fnmatch(normalized, pattern):
            return True
    return False


def get_default_config_content() -> str:
    """Return default config.toml content."""
    return """\
[hooks]
# Exclude patterns (fnmatch syntax)
# Supports exact repo paths and wildcard prefixes
exclude = [
    "/tmp/*",
]

[database]
# Relative to ~/.commit-logs/ or absolute path
path = "index.db"
"""


def ensure_config_exists() -> Path:
    """Ensure config directory and file exist, return config path."""
    DEFAULT_CONFIG_DIR.mkdir(parents=True, exist_ok=True)
    if not DEFAULT_CONFIG_PATH.exists():
        DEFAULT_CONFIG_PATH.write_text(get_default_config_content(), encoding="utf-8")
    return DEFAULT_CONFIG_PATH


# =============================================================================
# Repo-level labels (labels.json)
# =============================================================================

def _normalize_path(p: str) -> str:
    """Normalize a repo path to a stable key (resolved, forward slashes)."""
    return str(Path(p).resolve()).replace("\\", "/")


def read_labels() -> dict:
    """Read labels mapping. Returns {} if missing or unparseable."""
    if not DEFAULT_LABELS_PATH.exists():
        return {}
    try:
        with open(DEFAULT_LABELS_PATH, "r", encoding="utf-8") as f:
            data = json.load(f)
        if not isinstance(data, dict):
            return {}
        return data
    except (json.JSONDecodeError, OSError):
        return {}


def write_labels(data: dict) -> None:
    """Write labels mapping to labels.json."""
    DEFAULT_CONFIG_DIR.mkdir(parents=True, exist_ok=True)
    with open(DEFAULT_LABELS_PATH, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


def add_label(repo_path: str, label: str) -> None:
    """Add a label to a repo (ordered dedup)."""
    data = read_labels()
    key = _normalize_path(repo_path)
    labels = data.get(key, [])
    if label not in labels:
        labels.append(label)
    data[key] = labels
    write_labels(data)


def remove_label(repo_path: str, label: str) -> bool:
    """Remove a label from a repo. Returns True if it was present."""
    data = read_labels()
    key = _normalize_path(repo_path)
    labels = data.get(key, [])
    if label not in labels:
        return False
    labels = [x for x in labels if x != label]
    if labels:
        data[key] = labels
    else:
        del data[key]
    write_labels(data)
    return True


def paths_for_label(label: str) -> list[str]:
    """Return all normalized repo paths carrying the given label."""
    data = read_labels()
    return [path for path, labels in data.items() if label in labels]


def labels_for_path(repo_path: str) -> list[str]:
    """Return the labels for a single repo path."""
    data = read_labels()
    return data.get(_normalize_path(repo_path), [])
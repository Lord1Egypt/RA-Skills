"""Configuration loading for memory consolidation.

Loads from config.yaml (optional, PyYAML optional),
then overlays config.json from structured/ directory.
Identity is auto-detected from IDENTITY.md + USER.md in the workspace.
"""

from __future__ import annotations

import json
import os
import re
from pathlib import Path
from typing import Any, Dict, List, Optional

# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------
WORKSPACE = Path(os.environ.get("OPENCLAW_WORKSPACE", str(Path.home() / ".openclaw" / "workspace"))).resolve()
DAILY_DIR = WORKSPACE / "memory"
STRUCT_DIR = WORKSPACE / "memory" / "structured"
CONFIG_JSON_PATH = STRUCT_DIR / "config.json"
STATE_PATH = STRUCT_DIR / "state.json"
SNAPSHOT_PATH = WORKSPACE / "MEMORY_SNAPSHOT.md"
SNAPSHOT_RULE_PATH = WORKSPACE / "MEMORY_SNAPSHOT.rule.md"
SNAPSHOT_SEMANTIC_PATH = WORKSPACE / "MEMORY_SNAPSHOT.semantic.md"
CANDIDATES_DIR = STRUCT_DIR / "candidates"
CANDIDATE_LATEST_PATH = CANDIDATES_DIR / "latest.json"
SEMANTIC_DIR = STRUCT_DIR / "semantic"
SEMANTIC_LATEST_PATH = SEMANTIC_DIR / "latest.json"
SEMANTIC_PIPELINE_STATUS_PATH = SEMANTIC_DIR / "pipeline_status.json"

FACTS_PATH = STRUCT_DIR / "facts.jsonl"
BELIEFS_PATH = STRUCT_DIR / "beliefs.jsonl"
SUMMARIES_PATH = STRUCT_DIR / "summaries.jsonl"
EVENTS_PATH = STRUCT_DIR / "events.jsonl"
HEALTH_PATH = STRUCT_DIR / "health.json"

ARCHIVE_DIR = STRUCT_DIR / "archive"
ARCHIVE_FACTS_PATH = ARCHIVE_DIR / "facts.jsonl"
ARCHIVE_BELIEFS_PATH = ARCHIVE_DIR / "beliefs.jsonl"
ARCHIVE_SUMMARIES_PATH = ARCHIVE_DIR / "summaries.jsonl"
ARCHIVE_EVENTS_PATH = ARCHIVE_DIR / "events.jsonl"

# CRON_RUNS_PATH is no longer used (health_history.jsonl replaced cron log parsing)
CRON_RUNS_PATH: Path = Path("/dev/null")

_YAML_CONFIG_PATH = Path(__file__).resolve().parent / "config.yaml"

# ---------------------------------------------------------------------------
# Default config (engine-level)
# ---------------------------------------------------------------------------
DEFAULT_CONFIG: Dict[str, Any] = {
    "decay_rates": {
        "fact": 0.008,
        "belief": 0.07,
        "summary": 0.025,
        "event": 0.02,
    },
    "thresholds": {
        "archive": 0.05,
        "archive_temperature": 0.3,
        "summary_trigger": 3,
    },
    "temperature": {
        "w_age": 0.5,
        "w_ref": 0.3,
        "w_pri": 0.2,
        "age_lambda": 0.07,
        "reference_days": 7,
        "ref_cap": 3,
        "max_reference_lines": 5000,
        "hot_threshold": 0.7,
        "warm_threshold": 0.35,
    },
    "reinforcement": {
        "enabled": True,
        "cooldown_hours": 18,
        "boost_per_ref": 0.03,
        "max_boost": 0.12,
    },
    "snapshot": {
        "max_chars": 12000,
        "recent_days": 3,
        "top_facts": 8,
        "top_beliefs": 6,
        "top_summaries": 6,
        "top_decisions": 6,
        "top_issues": 5,
        "top_solutions": 5,
        "top_artifacts": 8,
    },
    "ingest": {
        "session_logs": True,
        "session_hours": 24,
        "agent_ids": "main",
    },
}

# Fallback identity (used only if IDENTITY.md / USER.md are missing)
DEFAULT_IDENTITY: Dict[str, Any] = {
    "assistant_name": "Assistant",
    "owner_name": "User",
    "owner_language": "English",
    "owner_timezone": "UTC",
}

# Generic tag rules (non-project-specific)
DEFAULT_GENERIC_TAG_RULES: Dict[str, List[str]] = {
    "docs": ["docs/", "README.md", "PROGRESS.md", "DECISIONS.md", "TASKS.md"],
    "deploy": ["systemctl", "build", "部署", "重启"],
    "git": ["git", "commit", "push"],
}


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _load_json_file(path: Path, default: Any) -> Any:
    try:
        return json.loads(path.read_text("utf-8"))
    except (FileNotFoundError, json.JSONDecodeError):
        return default


def merge_dict(base: Dict[str, Any], override: Dict[str, Any]) -> Dict[str, Any]:
    merged: Dict[str, Any] = dict(base)
    for k, v in override.items():
        if isinstance(v, dict) and isinstance(base.get(k), dict):
            merged[k] = merge_dict(base[k], v)
        else:
            merged[k] = v
    return merged


def _load_yaml_config() -> Dict[str, Any]:
    if not _YAML_CONFIG_PATH.exists():
        return {}
    raw = _YAML_CONFIG_PATH.read_text("utf-8")
    try:
        import yaml  # type: ignore
        return yaml.safe_load(raw) or {}
    except ImportError:
        pass
    try:
        return json.loads(raw) or {}
    except (json.JSONDecodeError, ValueError):
        return {}


# ---------------------------------------------------------------------------
# Identity parsing from IDENTITY.md + USER.md
# ---------------------------------------------------------------------------
_MD_KV_RE = re.compile(r'^\s*-\s*\*\*(.+?)[:：]\*\*\s*(.+)$')


def _parse_md_fields(path: Path) -> Dict[str, str]:
    fields: Dict[str, str] = {}
    if not path.exists():
        return fields
    try:
        for line in path.read_text("utf-8", errors="ignore").splitlines():
            m = _MD_KV_RE.match(line)
            if m:
                fields[m.group(1).strip()] = m.group(2).strip()
    except Exception:
        pass
    return fields


def _infer_language(notes: str) -> Optional[str]:
    if not notes:
        return None
    lower = notes.lower()
    if "中文" in notes or "chinese" in lower:
        return "Chinese"
    if "english" in lower or "英文" in notes:
        return "English"
    if "日本語" in notes or "japanese" in lower:
        return "Japanese"
    return None


def load_identity(workspace: Optional[Path] = None) -> Dict[str, Any]:
    """Load identity from IDENTITY.md + USER.md, fall back to yaml then defaults."""
    ws = workspace or WORKSPACE
    result: Dict[str, Any] = dict(DEFAULT_IDENTITY)

    _ensure_loaded()
    yaml_identity = _loaded_yaml.get("identity")
    if isinstance(yaml_identity, dict):
        result = merge_dict(result, yaml_identity)

    # IDENTITY.md → assistant_name
    id_fields = _parse_md_fields(ws / "IDENTITY.md")
    if id_fields.get("Name"):
        result["assistant_name"] = id_fields["Name"]

    # USER.md → owner_name, owner_timezone, owner_language
    user_fields = _parse_md_fields(ws / "USER.md")
    if user_fields.get("Name"):
        result["owner_name"] = user_fields["Name"]
    if user_fields.get("Timezone"):
        result["owner_timezone"] = user_fields["Timezone"]
    if user_fields.get("What to call them"):
        result["owner_display_name"] = user_fields["What to call them"]
    lang = _infer_language(user_fields.get("Notes", ""))
    if lang:
        result["owner_language"] = lang

    return result


# ---------------------------------------------------------------------------
# Loaded config singleton
# ---------------------------------------------------------------------------
_loaded_yaml: Dict[str, Any] = {}
_loaded_config: Dict[str, Any] = {}
_config_loaded = False


def _ensure_loaded() -> None:
    global _loaded_yaml, _loaded_config, _config_loaded, CRON_RUNS_PATH
    if _config_loaded:
        return
    _loaded_yaml = _load_yaml_config()

    cfg = dict(DEFAULT_CONFIG)
    for key in DEFAULT_CONFIG:
        if key in _loaded_yaml:
            if isinstance(cfg.get(key), dict) and isinstance(_loaded_yaml[key], dict):
                cfg[key] = merge_dict(cfg[key], _loaded_yaml[key])
            else:
                cfg[key] = _loaded_yaml[key]
    json_cfg = _load_json_file(CONFIG_JSON_PATH, {})
    if isinstance(json_cfg, dict):
        cfg = merge_dict(cfg, json_cfg)
    _loaded_config = cfg

    cron_path = _loaded_yaml.get("cron_runs_path")
    if cron_path:
        CRON_RUNS_PATH = Path(cron_path)

    _config_loaded = True


def load_config() -> Dict[str, Any]:
    _ensure_loaded()
    return dict(_loaded_config)


def get_tag_rules() -> Dict[str, List[str]]:
    """Return generic tag rules merged with yaml overrides."""
    _ensure_loaded()
    base: Dict[str, List[str]] = dict(DEFAULT_GENERIC_TAG_RULES)
    yaml_rules = _loaded_yaml.get("tag_rules")
    if isinstance(yaml_rules, dict):
        for k, v in yaml_rules.items():
            if isinstance(v, list):
                base[k] = v
    return base

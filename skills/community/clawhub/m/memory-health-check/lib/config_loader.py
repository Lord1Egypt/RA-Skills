#!/usr/bin/env python3
"""YAML configuration loader for memory-health-check."""
import yaml
import logging
from pathlib import Path
from typing import Any

logger = logging.getLogger("memory-health-check.config")


# ─────────────────────────────────────────────────────────────────────────────
# Default Thresholds
# ─────────────────────────────────────────────────────────────────────────────

DEFAULT_THRESHOLDS = {
    "integrity": {"healthy": 100, "warning": 80, "critical": 50},
    "freshness_rate": {"healthy": 0.70, "warning": 0.40, "critical": 0.20},
    "bloat_mb": {"healthy": 500, "warning": 2000, "critical": 5000},
    "orphan_rate": {"healthy": 0.01, "warning": 0.05, "critical": 0.10},
    "dedup_rate": {"healthy": 0.02, "warning": 0.10, "critical": 0.20},
    "coverage_rate": {"healthy": 0.80, "warning": 0.50, "critical": 0.20},
}

DEFAULT_WEIGHTS = {
    "integrity": 0.30,
    "freshness": 0.20,
    "bloat": 0.15,
    "orphans": 0.15,
    "dedup": 0.10,
    "coverage": 0.10,
}

DEFAULT_CONFIG = {
    "version": "1.0.0",
    "thresholds": DEFAULT_THRESHOLDS,
    "weights": DEFAULT_WEIGHTS,
    "scan": {
        "max_db_size_mb": 5000,
        "max_file_count": 100000,
        "timeout_seconds": 300,
        "db_sample_size": 10000,
    },
    "auto_repair": {
        "enabled": False,
        "require_confirmation": True,
        "remove_ds_store": True,
        "remove_empty_files": True,
        "remove_orphans": False,
        "min_file_age_days": 7,
        "max_archive_age_days": 90,
    },
    "reporting": {
        "summary_dir": "health-reports",
        "max_reports_stored": 30,
        "include_recommendations": True,
        "include_auto_repair_plan": True,
    },
    "knowledge_domains": [
        "技术", "商业", "创意", "人际关系", "个人成长", "日常",
    ],
    "coverage_keywords": {
        "技术": ["Python", "JavaScript", "API", "数据库", "代码", "架构", "部署", "skill", "agent", "tool"],
        "商业": ["客户", "合同", "报价", "商业", "合作", "BD", "销售", "收入", "business", "deal"],
        "创意": ["创意", "设计", "想法", "灵感", "创新", "creative", "idea", "design"],
        "人际关系": ["团队", "沟通", "合作", "家人", "朋友", "会议", "team", "meeting"],
        "个人成长": ["学习", "目标", "计划", "反思", "成长", "learning", "goal", "plan"],
        "日常": ["今天", "明天", "会议", "日程", "任务", "today", "tomorrow", "schedule"],
    },
}


def get_default_thresholds() -> dict:
    """Return the default thresholds dictionary."""
    import copy
    return copy.deepcopy(DEFAULT_THRESHOLDS)


def get_default_weights() -> dict:
    """Return the default weights dictionary."""
    import copy
    return copy.deepcopy(DEFAULT_WEIGHTS)


def load_config(config_path: Path = None) -> dict:
    """Load configuration from YAML file with fallback to defaults.
    
    Args:
        config_path: Path to config YAML.
                     Defaults to: memory-health-check/config/thresholds.yaml
        
    Returns:
        dict: Configuration dictionary (merged with defaults)
    """
    if config_path is None:
        config_path = (
            Path.home()
            / ".openclaw"
            / "workspace"
            / "skills"
            / "memory-health-check"
            / "config"
            / "thresholds.yaml"
        )
    
    config = _deep_copy(DEFAULT_CONFIG)
    
    if not config_path.exists():
        logger.info(f"Config not found at {config_path}, using defaults")
        return config
    
    try:
        with open(config_path, "r", encoding="utf-8") as f:
            user_config = yaml.safe_load(f) or {}
        config = _deep_merge(config, user_config)
        logger.info(f"Loaded config from {config_path}")
    except Exception as e:
        logger.warning(f"Failed to load config: {e}, using defaults")
    
    return config


def _deep_merge(base: dict, override: dict) -> dict:
    """Deep merge override dict into base dict."""
    for key, value in override.items():
        if key in base and isinstance(base[key], dict) and isinstance(value, dict):
            base[key] = _deep_merge(base[key], value)
        else:
            base[key] = value
    return base


def _deep_copy(d: dict) -> dict:
    """Deep copy a dict."""
    import copy
    return copy.deepcopy(d)


# ─────────────────────────────────────────────────────────────────────────────
# Threshold Evaluation Helpers
# ─────────────────────────────────────────────────────────────────────────────

def eval_threshold(value: float, thresholds: dict, invert: bool = False) -> tuple[str, int]:
    """Evaluate a value against healthy/warning/critical thresholds.
    
    Args:
        value: The measured value
        thresholds: Dict with keys: healthy, warning, critical
        invert: If True, lower is better (e.g., for orphan rate)
        
    Returns:
        (status_str, score_int): ("healthy"|"warning"|"critical", 0-100)
    """
    h = thresholds.get("healthy", 100)
    w = thresholds.get("warning", 50)
    c = thresholds.get("critical", 20)
    
    if invert:
        # Lower is better (e.g., orphan rate: 0% is best)
        if value <= h:
            return "healthy", 100
        elif value <= w:
            return "warning", 70
        elif value <= c:
            return "warning", 60
        else:
            return "critical", 20
    else:
        # Higher is better (e.g., freshness: high % is best)
        if value >= h:
            return "healthy", 100
        elif value >= w:
            return "warning", 70
        elif value >= c:
            return "warning", 60
        else:
            return "critical", 20


if __name__ == "__main__":
    import json
    cfg = load_config()
    print(json.dumps(cfg, indent=2, ensure_ascii=False))

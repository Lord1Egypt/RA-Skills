"""配置加载：从 config.yaml 读取全部配置，与默认值深度合并，并提供点路径访问。

零第三方依赖（复用 yamlmini）。代码中不允许出现硬编码业务参数（P0-6 / 设计约束 1）。
"""

from . import paths, yamlmini

DEFAULTS = {
    "general": {
        "timezone": "Asia/Shanghai",
        "language": "zh-CN",
        "expected_run_interval_minutes": 30,
        "scheduler_grace_multiplier": 3,
    },
    "news_sources": [],
    "cache": {
        "ttl_seconds": 300,
        "dir": "cache",
        "price_series_max_points": 2000,
    },
    "alerts": {
        "threshold_pct": 1.0,
        "min_threshold_pct": 0.5,
        "max_threshold_pct": 3.0,
        "volatility_multiplier": 1.5,
        "lookback_days": 7,
        "benchmarks": {
            "prev_close": True,
            "last_fetch": True,
            "ema": False,
            "ema_window": 20,
            "trend": True,
            "trend_consecutive_n": 3,
        },
        "cooldown_minutes": 30,
        "max_alerts_per_day": 10,
        "max_alerts_per_direction_per_day": 1,
        "auto_resolve_minutes": 1440,
        "retention_days": 30,
    },
    "output": {
        "max_push_bytes": 2000,
        "min_factors_per_analysis": 2,
        "max_factors_per_analysis": 6,
        "constraints": {
            "allowed_impacts": [
                "利多", "利空", "偏多", "偏空", "中性", "多空交织",
            ],
            "required_factor_fields": ["factor", "impact", "reasoning", "sources"],
            "sources": {
                "must_be_http_url": True,
                "must_be_in_fetch_log": True,
                "min_count_per_factor": 1,
                "min_unique_domains": 2,
            },
            "forbidden_phrases": [
                "根据经验", "众所周知", "一般来说", "通常情况下",
                "据了解", "据业内人士", "显而易见",
            ],
            "no_data_marker": "no_data",
        },
    },
    "validation": {
        "gold_price_min": 1000.0,
        "gold_price_max": 10000.0,
    },
    "archive": {
        "retention_days": 365,
        "index_enabled": True,
        "auto_archive_hour": 23,
    },
    "notification": {
        "enabled": True,
        "dedup_max_fingerprints": 100,
        "default_timeout_seconds": 90,
        "default_retry_count": 2,
        "retry_backoff_seconds": 10,
        "send_summary": True,
    },
    "paths": {
        "logs": "logs",
        "archive": "archive",
        "alerts": "alerts",
        "cache": "cache",
        "state": "state.json",
        "notifications": "notifications",
    },
}


def _copy(obj):
    if isinstance(obj, dict):
        return {k: _copy(v) for k, v in obj.items()}
    if isinstance(obj, list):
        return [_copy(v) for v in obj]
    return obj


def _deep_merge(base, override):
    for k, v in override.items():
        if isinstance(v, dict) and isinstance(base.get(k), dict):
            base[k] = _deep_merge(base[k], v)
        else:
            base[k] = v
    return base


def load(path=None):
    path = paths.resolve(path or "config.yaml")
    data = {}
    if path.exists():
        parsed = yamlmini.load(path.read_text(encoding="utf-8"))
        if isinstance(parsed, dict):
            data = parsed
    return _deep_merge(_copy(DEFAULTS), data)


def dig(cfg, dotted, default=None):
    """点路径取值，如 dig(cfg, "alerts.benchmarks.trend", False)。"""
    node = cfg
    for part in dotted.split("."):
        if not isinstance(node, dict) or part not in node:
            return default
        node = node[part]
    return node

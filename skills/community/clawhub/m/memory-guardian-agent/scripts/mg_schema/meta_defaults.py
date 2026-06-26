"""Canonical schema defaults for memory-guardian v0.4.6.

All scripts MUST import defaults from here. Do NOT duplicate these dicts
in individual scripts — that leads to drift and silent bugs.
"""

# ── Single source of truth for version ──────────────────────────────────
SCHEMA_VERSION = "0.4.6"  # meta.json schema version (migration target)
PRODUCT_VERSION = "v0.4.6"  # product/release version for docs & display

# Per-memory v0.4.5 field defaults.
# Applied by bootstrap, migrate_retag, _ensure_schema_compliance, and
# any code path that creates a new memory entry.
MEMORY_DEFAULTS = {
    "tags_locked": False,
    "classification_confidence": None,
    "classification_context": None,
    "inbox_reason": None,
    "signal_level": None,
    "reactivation_count": 0,
    "last_reactivated": None,
    "trigger_words": [],
    "needs_review": False,
    "needs_review_since": None,
    "needs_review_timeout": "7d",
    "review_result": None,
    "reviewed_at": None,
    "version": 0,
    "access_signals": [],
}

DEFAULT_DECAY_CONFIG = {
    "alpha": 2.0,
    "beta_cap": 3.0,
    "l2_queue_cap": 20,
    "l2_timeout_minutes": 30,
    "l2_early_recovery_m": 5,
    "signal_weights": {
        "access_log_weight": 1.0,
        "infer_weight": 0.5,
        "implicit_access_weight": 0.3,
    },
    "signal_stale_threshold_hours": 24,
    "signal_stale_threshold_deploy_hours": 2,
    "quiet_degradation": {
        "min_sample": 5,
        "median_discount": 0.7,
        "iqr_multiplier": 1.5,
        "trigger_exemption": 5,
    },
    "provenance": {
        "authoritative_base": 0.6,
        "authoritative_multiplier": 1.0,
        "non_authoritative_base": 0.4,
        "non_authoritative_multiplier": 0.7,
        "verification_step": 0.1,
        "verification_cap": 0.3,
    },
}

DEFAULT_QUALITY_GATE_STATE = {
    "state": "NORMAL",
    "anomaly_count": 0,
    "consecutive_clean": 0,
    "total_writes": 0,
    "total_failures": 0,
    "failure_rate": 0.0,
    "history": [],
    "check_history": [],
    "intervention_log": [],
}

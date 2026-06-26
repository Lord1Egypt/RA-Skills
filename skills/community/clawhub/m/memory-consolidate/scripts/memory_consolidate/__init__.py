from .main import main

# Backward-compat exports for legacy helper scripts that still do:
#   import memory_consolidate as mc
from .config import (
    FACTS_PATH,
    SUMMARIES_PATH,
    EVENTS_PATH,
    SNAPSHOT_PATH,
    SNAPSHOT_RULE_PATH,
    SNAPSHOT_SEMANTIC_PATH,
    CANDIDATES_DIR,
    CANDIDATE_LATEST_PATH,
    SEMANTIC_DIR,
    SEMANTIC_LATEST_PATH,
    load_config,
)
from .core import (
    make_id,
    merge_rows_by_identity,
    normalize_content,
    normalize_for_match,
    read_jsonl,
    render_row_content,
    utc_now_iso,
    is_path_like_text,
)
from .ingest import (
    apply_pattern_metadata,
    collect_recent_lines,
    is_display_noise_issue_line,
    is_low_signal_line,
    is_non_issue_progress_line,
    is_questionish_line,
    is_request_or_discussion_line,
    list_daily_logs,
    prune_noisy_facts,
    prune_noisy_issue_events,
)
from .snapshot import top_events

__all__ = [
    "main",
    "FACTS_PATH",
    "SUMMARIES_PATH",
    "EVENTS_PATH",
    "SNAPSHOT_PATH",
    "SNAPSHOT_RULE_PATH",
    "SNAPSHOT_SEMANTIC_PATH",
    "CANDIDATES_DIR",
    "CANDIDATE_LATEST_PATH",
    "SEMANTIC_DIR",
    "SEMANTIC_LATEST_PATH",
    "load_config",
    "make_id",
    "merge_rows_by_identity",
    "normalize_content",
    "normalize_for_match",
    "read_jsonl",
    "render_row_content",
    "utc_now_iso",
    "is_path_like_text",
    "apply_pattern_metadata",
    "collect_recent_lines",
    "is_display_noise_issue_line",
    "is_low_signal_line",
    "is_non_issue_progress_line",
    "is_questionish_line",
    "is_request_or_discussion_line",
    "list_daily_logs",
    "prune_noisy_facts",
    "prune_noisy_issue_events",
    "top_events",
]

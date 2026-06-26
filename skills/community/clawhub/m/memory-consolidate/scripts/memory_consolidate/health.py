"""Memory health metrics computation."""

from __future__ import annotations

from typing import Any, Dict, List, Optional


def compute_memory_health(
    active_rows: List[Dict[str, Any]],
    archived_rows: List[Dict[str, Any]],
    processed_lines: int,
    skipped_low_signal: int,
    reinforced_count: int,
    distilled_count: int,
    previous_health: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    active_total = len(active_rows)
    archived_total = len(archived_rows)
    total = active_total + archived_total
    archive_ratio = (archived_total / total) if total > 0 else 0.0

    hot = sum(1 for r in active_rows if str(r.get("temperature_bucket") or "") == "hot")
    warm = sum(1 for r in active_rows if str(r.get("temperature_bucket") or "") == "warm")
    cold = max(0, active_total - hot - warm)

    issue_count = sum(1 for r in active_rows if str(r.get("kind") or "") == "event" and str(r.get("event_type") or "") == "issue")
    solution_count = sum(1 for r in active_rows if str(r.get("kind") or "") == "event" and str(r.get("event_type") or "") == "solution")
    decision_count = sum(1 for r in active_rows if str(r.get("kind") or "") == "event" and str(r.get("event_type") or "") == "decision")
    correction_count = sum(1 for r in active_rows if "correction" in (r.get("tags") or []) or str(r.get("source_type") or "") == "correction")
    pattern_summary_count = sum(1 for r in active_rows if str(r.get("kind") or "") == "summary" and (r.get("pattern_key") or "working_pattern" in (r.get("tags") or [])))

    # SNR v2: percentage of high-signal items among active items
    high_signal = hot + reinforced_count + decision_count + solution_count + pattern_summary_count
    high_signal = min(high_signal, active_total)
    snr = (high_signal / max(1, active_total)) * 100.0

    return {
        "active_total": active_total,
        "archived_total": archived_total,
        "archive_ratio": round(archive_ratio, 4),
        "hot": hot,
        "warm": warm,
        "cold": cold,
        "reinforced_count": reinforced_count,
        "distilled_count": distilled_count,
        "signal_noise_ratio": round(snr, 3),
        "issue_count": issue_count,
        "solution_count": solution_count,
        "correction_count": correction_count,
        "pattern_summary_count": pattern_summary_count,
    }

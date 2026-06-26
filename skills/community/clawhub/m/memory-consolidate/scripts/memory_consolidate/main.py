"""Main consolidation pipeline: orchestrates all sub-modules."""

from __future__ import annotations

import datetime as dt
from typing import Any, Dict, List

from .config import (
    STRUCT_DIR,
    ARCHIVE_DIR,
    CANDIDATES_DIR,
    SEMANTIC_DIR,
    FACTS_PATH,
    BELIEFS_PATH,
    SUMMARIES_PATH,
    EVENTS_PATH,
    HEALTH_PATH,
    ARCHIVE_FACTS_PATH,
    ARCHIVE_BELIEFS_PATH,
    ARCHIVE_SUMMARIES_PATH,
    ARCHIVE_EVENTS_PATH,
    SNAPSHOT_PATH,
    SNAPSHOT_RULE_PATH,
    SNAPSHOT_SEMANTIC_PATH,
    STATE_PATH,
    load_config,
    load_identity,
)
from .core import (
    load_json,
    save_json,
    read_jsonl,
    write_jsonl,
    utc_now_iso,
    make_id,
    upsert,
    merge_rows_by_identity,
    normalize_event_content,
    normalize_content,
)
from .ingest import (
    list_daily_logs,
    list_reflection_logs,
    is_reflection_log,
    read_new_lines,
    extract_candidate_line,
    classify_event_type,
    infer_tags,
    build_learning_items,
    apply_pattern_metadata,
    prune_noisy_facts,
    prune_noisy_issue_events,
    collect_recent_lines,
    collect_reference_corpus,
    classify_line,
    is_low_signal_line,
)
from .temperature import (
    apply_decay,
    apply_temperature,
    apply_usage_reinforcement,
)
from .archive import (
    partition_archive_rows,
    merge_archive_rows,
    distill_archived_rows,
    purge_low_value_facts,
)
from .snapshot import generate_snapshot
from .health import compute_memory_health
from .pipeline import run_semantic_v2_lite_pipeline

HEALTH_HISTORY_PATH = STRUCT_DIR / "health_history.jsonl"


def _append_health_history(health: Dict[str, Any], now_iso: str) -> None:
    """Append current health metrics to health_history.jsonl."""
    import json
    record = dict(health)
    record["run_at"] = now_iso
    HEALTH_HISTORY_PATH.parent.mkdir(parents=True, exist_ok=True)
    with HEALTH_HISTORY_PATH.open("a", encoding="utf-8") as f:
        f.write(json.dumps(record, ensure_ascii=True, separators=(",", ":")) + "\n")



def main() -> int:
    cfg = load_config()
    snap_cfg = cfg.get("snapshot") or {}
    decay_cfg = cfg.get("decay_rates") or {}
    thresholds = cfg.get("thresholds") or {}
    temp_cfg = cfg.get("temperature") or {}
    reinforce_cfg = cfg.get("reinforcement") or {}

    STRUCT_DIR.mkdir(parents=True, exist_ok=True)
    ARCHIVE_DIR.mkdir(parents=True, exist_ok=True)
    CANDIDATES_DIR.mkdir(parents=True, exist_ok=True)
    SEMANTIC_DIR.mkdir(parents=True, exist_ok=True)
    FACTS_PATH.touch(exist_ok=True)
    BELIEFS_PATH.touch(exist_ok=True)
    SUMMARIES_PATH.touch(exist_ok=True)
    EVENTS_PATH.touch(exist_ok=True)
    ARCHIVE_FACTS_PATH.touch(exist_ok=True)
    ARCHIVE_BELIEFS_PATH.touch(exist_ok=True)
    ARCHIVE_SUMMARIES_PATH.touch(exist_ok=True)
    ARCHIVE_EVENTS_PATH.touch(exist_ok=True)

    now = dt.datetime.now(dt.timezone.utc)
    now_iso = utc_now_iso()

    facts = merge_rows_by_identity(read_jsonl(FACTS_PATH))
    beliefs = merge_rows_by_identity(read_jsonl(BELIEFS_PATH))
    summaries = merge_rows_by_identity(read_jsonl(SUMMARIES_PATH))
    events = merge_rows_by_identity(read_jsonl(EVENTS_PATH))

    facts = [apply_decay(it, float(decay_cfg.get("fact", 0.008)), now) for it in facts]
    beliefs = [apply_decay(it, float(decay_cfg.get("belief", 0.07)), now) for it in beliefs]
    summaries = [apply_decay(it, float(decay_cfg.get("summary", 0.025)), now) for it in summaries]
    events = [apply_decay(it, float(decay_cfg.get("event", 0.02)), now) for it in events]

    state = load_json(STATE_PATH, {})
    previous_health = dict((state.get("stats") or {}).get("memory_health") or {})
    cursors: Dict[str, int] = dict(state.get("file_cursors") or {})

    all_logs = list_daily_logs()
    reflection_logs = list_reflection_logs()
    all_input_logs = sorted([*all_logs, *reflection_logs], key=lambda p: p.name)

    recent_days = int(snap_cfg.get("recent_days", 3))
    if not cursors:
        files_to_process = sorted(
            [*all_logs[-recent_days:], *reflection_logs[-recent_days:]],
            key=lambda p: p.name,
        )
    else:
        files_to_process = all_input_logs

    processed_lines = 0
    skipped_low_signal = 0
    new_events = 0

    for p in files_to_process:
        from_reflection = is_reflection_log(p)
        cursor = int(cursors.get(p.name, 0))
        rows, new_cursor = read_new_lines(p, cursor)
        for lineno, raw in rows:
            line = extract_candidate_line(raw)
            if not line:
                continue

            normalized = normalize_content(line)
            if is_low_signal_line(normalized):
                skipped_low_signal += 1
                continue

            processed_lines += 1

            row_source = f"{p.name}:{lineno}"
            source_type = "reflection" if from_reflection else "daily_memory"

            event_type = classify_event_type(normalized)
            if event_type:
                normalized_event = normalize_event_content(normalized, event_type)
                ev = {
                    "id": make_id("event", f"{event_type}:{normalized_event}"),
                    "kind": "event",
                    "event_type": event_type,
                    "content": normalized_event,
                    "confidence": 0.9,
                    "importance": 0.75 if event_type in {"decision", "progress", "artifact"} else 0.65,
                    "weight": 1.0,
                    "created_at": now_iso,
                    "updated_at": now_iso,
                    "last_seen_at": now_iso,
                    "source": row_source,
                    "source_type": source_type,
                    "tags": [
                        *infer_tags(normalized_event),
                        *( ["clauder", "reflection"] if from_reflection else [] ),
                    ],
                }
                before = len(events)
                events = upsert(events, ev)
                if len(events) > before:
                    new_events += 1

            learning_items, skip_default_fact_belief = build_learning_items(normalized, now_iso, row_source, from_reflection=from_reflection)
            for item in learning_items:
                if item["kind"] == "fact":
                    facts = upsert(facts, item)
                elif item["kind"] == "belief":
                    beliefs = upsert(beliefs, item)
                elif item["kind"] == "summary":
                    summaries = upsert(summaries, item)

            if not from_reflection and not skip_default_fact_belief:
                kind, conf, imp = classify_line(normalized)
                item = {
                    "id": make_id(kind, normalized),
                    "kind": kind,
                    "content": normalized,
                    "confidence": float(conf),
                    "importance": float(imp),
                    "weight": 1.0,
                    "created_at": now_iso,
                    "updated_at": now_iso,
                    "last_seen_at": now_iso,
                    "source": row_source,
                    "source_type": source_type,
                    "tags": infer_tags(normalized),
                }
                if kind == "fact":
                    facts = upsert(facts, item)
                elif kind == "belief":
                    beliefs = upsert(beliefs, item)

        cursors[p.name] = new_cursor

    trig = int(thresholds.get("summary_trigger", 3))
    buckets: Dict[str, int] = {}
    for ev in events:
        ev_type = str(ev.get("event_type") or "")
        if ev_type not in {"decision", "progress", "artifact"}:
            continue
        content = str(ev.get("content") or "")
        key = None
        for kw in ["OpenClaw", "事件驱动", "统一", "部署", "build", "git", "deploy", "refactor"]:
            if kw in content:
                key = kw
                break
        if not key:
            continue
        buckets[key] = buckets.get(key, 0) + 1

    for k, count in buckets.items():
        if count < trig:
            continue
        s = f"近期关键决策/进展聚焦在 {k}（提及 {count} 次）。"
        summaries = upsert(
            summaries,
            {
                "id": make_id("summary", f"focus:{k}"),
                "kind": "summary",
                "content": s,
                "confidence": 1.0,
                "importance": 0.8,
                "weight": 1.0,
                "created_at": now_iso,
                "updated_at": now_iso,
                "last_seen_at": now_iso,
                "source": "auto",
                "tags": [k],
            },
        )

    facts = prune_noisy_facts(apply_pattern_metadata(merge_rows_by_identity(facts)))
    beliefs = apply_pattern_metadata(merge_rows_by_identity(beliefs))
    summaries = apply_pattern_metadata(merge_rows_by_identity(summaries))
    events = prune_noisy_issue_events(apply_pattern_metadata(merge_rows_by_identity(events)))

    ref_days = max(1, int(temp_cfg.get("reference_days", 7)))
    reference_files = sorted(
        [*all_logs[-ref_days:], *reflection_logs[-ref_days:]],
        key=lambda p: p.name,
    )
    reference_corpus = collect_reference_corpus(
        reference_files,
        max_lines=max(500, int(temp_cfg.get("max_reference_lines", 5000))),
    )

    facts = apply_temperature(facts, now, reference_corpus, temp_cfg)
    beliefs = apply_temperature(beliefs, now, reference_corpus, temp_cfg)
    summaries = apply_temperature(summaries, now, reference_corpus, temp_cfg)
    events = apply_temperature(events, now, reference_corpus, temp_cfg)

    facts, facts_reinforced = apply_usage_reinforcement(facts, now, reinforce_cfg)
    beliefs, beliefs_reinforced = apply_usage_reinforcement(beliefs, now, reinforce_cfg)
    summaries, summaries_reinforced = apply_usage_reinforcement(summaries, now, reinforce_cfg)
    events, events_reinforced = apply_usage_reinforcement(events, now, reinforce_cfg)
    reinforced_count = facts_reinforced + beliefs_reinforced + summaries_reinforced + events_reinforced

    facts_before_purge = len(facts)
    facts = purge_low_value_facts(facts)
    purged_facts_count = facts_before_purge - len(facts)

    legacy_archive = float(thresholds.get("archive", 0.05))
    cold_threshold = float(
        thresholds.get("archive_temperature", 0.3 if legacy_archive <= 0.1 else legacy_archive)
    )

    facts, facts_cold = partition_archive_rows(facts, cold_threshold)
    beliefs, beliefs_cold = partition_archive_rows(beliefs, cold_threshold)
    summaries, summaries_cold = partition_archive_rows(summaries, cold_threshold)
    events, events_cold = partition_archive_rows(events, cold_threshold)

    distilled_count = 0
    for label_name, cold_rows in [
        ("fact", facts_cold),
        ("belief", beliefs_cold),
        ("summary", summaries_cold),
        ("event", events_cold),
    ]:
        distilled = distill_archived_rows(cold_rows, label_name, now_iso)
        if not distilled:
            continue
        before = len(summaries)
        summaries = upsert(summaries, distilled)
        if len(summaries) > before:
            distilled_count += 1

    facts_archive = merge_archive_rows(read_jsonl(ARCHIVE_FACTS_PATH), facts_cold)
    beliefs_archive = merge_archive_rows(read_jsonl(ARCHIVE_BELIEFS_PATH), beliefs_cold)
    summaries_archive = merge_archive_rows(read_jsonl(ARCHIVE_SUMMARIES_PATH), summaries_cold)
    events_archive = merge_archive_rows(read_jsonl(ARCHIVE_EVENTS_PATH), events_cold)

    write_jsonl(FACTS_PATH, facts)
    write_jsonl(BELIEFS_PATH, beliefs)
    write_jsonl(SUMMARIES_PATH, summaries)
    write_jsonl(EVENTS_PATH, events)
    write_jsonl(ARCHIVE_FACTS_PATH, facts_archive)
    write_jsonl(ARCHIVE_BELIEFS_PATH, beliefs_archive)
    write_jsonl(ARCHIVE_SUMMARIES_PATH, summaries_archive)
    write_jsonl(ARCHIVE_EVENTS_PATH, events_archive)

    recent_files_for_snapshot = all_logs[-recent_days:] if all_logs else []
    recent_reflection_files = reflection_logs[-recent_days:] if reflection_logs else []
    recent_lines = collect_recent_lines(recent_files_for_snapshot, max_lines=18)

    active_rows = [*facts, *beliefs, *summaries, *events]
    archived_rows = [*facts_archive, *beliefs_archive, *summaries_archive, *events_archive]
    memory_health = compute_memory_health(
        active_rows=active_rows,
        archived_rows=archived_rows,
        processed_lines=processed_lines,
        skipped_low_signal=skipped_low_signal,
        reinforced_count=reinforced_count,
        distilled_count=distilled_count,
        previous_health=previous_health,
    )

    # Add per-type counts to health for history
    health_with_counts = dict(memory_health)
    health_with_counts["facts"] = len(facts)
    health_with_counts["beliefs"] = len(beliefs)
    health_with_counts["summaries"] = len(summaries)
    health_with_counts["events"] = len(events)

    identity = load_identity()

    rule_snapshot = generate_snapshot(
        facts=facts,
        beliefs=beliefs,
        summaries=summaries,
        events=events,
        recent_lines=recent_lines,
        max_chars=int(snap_cfg.get("max_chars", 12000)),
        limits={
            "top_facts": int(snap_cfg.get("top_facts", 8)),
            "top_beliefs": int(snap_cfg.get("top_beliefs", 6)),
            "top_summaries": int(snap_cfg.get("top_summaries", 6)),
            "top_decisions": int(snap_cfg.get("top_decisions", 6)),
            "top_issues": int(snap_cfg.get("top_issues", 5)),
            "top_solutions": int(snap_cfg.get("top_solutions", 5)),
            "top_artifacts": int(snap_cfg.get("top_artifacts", 8)),
        },
        identity=identity,
        memory_health=memory_health,
    )
    SNAPSHOT_RULE_PATH.write_text(rule_snapshot, "utf-8")
    SNAPSHOT_PATH.write_text(rule_snapshot, "utf-8")
    save_json(HEALTH_PATH, memory_health)

    # Append health metrics to history
    _append_health_history(health_with_counts, now_iso)

    semantic_status = run_semantic_v2_lite_pipeline(now_iso)
    semantic_ready = semantic_status.get("status") == "ok" and SNAPSHOT_SEMANTIC_PATH.exists()
    if semantic_ready:
        SNAPSHOT_PATH.write_text(SNAPSHOT_SEMANTIC_PATH.read_text("utf-8"), "utf-8")
        semantic_status["default_source"] = "semantic"
    else:
        SNAPSHOT_PATH.write_text(rule_snapshot, "utf-8")
        semantic_status["default_source"] = "rule_fallback"

    semantic_status["default_ready"] = SNAPSHOT_PATH.exists()
    semantic_status["rule_ready"] = SNAPSHOT_RULE_PATH.exists()
    semantic_status["semantic_ready"] = SNAPSHOT_SEMANTIC_PATH.exists()
    from .config import SEMANTIC_PIPELINE_STATUS_PATH, SEMANTIC_LATEST_PATH
    save_json(SEMANTIC_PIPELINE_STATUS_PATH, semantic_status)

    # User traits extraction disabled (low practical value for now)

    state["last_run_at"] = now_iso
    state["recent_files"] = [p.name for p in recent_files_for_snapshot]
    state["recent_reflection_files"] = [p.name for p in recent_reflection_files]
    state["file_cursors"] = cursors
    state["stats"] = {
        "processed_lines": processed_lines,
        "skipped_low_signal": skipped_low_signal,
        "new_events": new_events,
        "reinforced_count": reinforced_count,
        "distilled_count": distilled_count,
        "purged_facts": purged_facts_count,
        "reference_corpus_lines": len(reference_corpus),
        "cold_threshold": cold_threshold,
        "facts": len(facts),
        "beliefs": len(beliefs),
        "summaries": len(summaries),
        "events": len(events),
        "archived_facts": len(facts_archive),
        "archived_beliefs": len(beliefs_archive),
        "archived_summaries": len(summaries_archive),
        "archived_events": len(events_archive),
        "semantic_candidates_ready": CANDIDATES_DIR.joinpath("latest.json").exists(),
        "snapshot_default_ready": SNAPSHOT_PATH.exists(),
        "snapshot_rule_ready": SNAPSHOT_RULE_PATH.exists(),
        "semantic_snapshot_ready": SNAPSHOT_SEMANTIC_PATH.exists(),
        "snapshot_default_source": semantic_status.get("default_source"),
        "memory_health": memory_health,
    }
    save_json(STATE_PATH, state)

    return 0

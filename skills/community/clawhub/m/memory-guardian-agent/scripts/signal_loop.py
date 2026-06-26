#!/usr/bin/env python3
"""memory-guardian: Signal loop — dual-layer access signal collection (v0.4.6).

Phase 1 of v0.4.6: Provides real access signals for the decay engine.

Two signal layers:
  Layer 1 (real-time, low noise): access_log.jsonl
    - Agent appends {file, ts, context, tags} after memory_get
    - Weight: 1.0 (configurable)
  Layer 2 (periodic inference, noisy): cron keyword matching
    - run_batch scans daily_notes for keyword matches against meta.json tags
    - Weight: 0.5 (configurable)

Signal health check:
  - run_batch checks access_log.jsonl mtime
  - If stale > threshold → degrade to Layer 2 only + WARNING
  - Auto-recovery when new entries appear

Design principle: "Observable but not brittle"
  - Signal break → degrade gracefully (not crash)
  - WARNING logged but run_batch continues
  - Weights configurable in decay_config.signal_weights

Usage:
  python3 signal_loop.py [--workspace <path>] [--meta <path>] [--dry-run]

MCP integration:
  append_access_log(file, context, tags)  — call after memory_get
  merge_signals(meta_path, workspace)      — call at run_batch start
  check_signal_health(workspace)           — call at run_batch start
"""

import json
import math
import os
import re
import argparse
import sys
from datetime import datetime, timedelta

# Add scripts dir to path for imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from mg_utils import CST, load_meta, save_meta

# ── Constants ──────────────────────────────────────────────────────────────

ACCESS_LOG_FILENAME = "access_log.jsonl"
SIGNAL_WEIGHTS_DEFAULT = {
    "access_log_weight": 1.0,
    "infer_weight": 0.5,
    "implicit_access_weight": 0.3,
}
SIGNAL_STALE_THRESHOLD_HOURS = 24
SIGNAL_STALE_THRESHOLD_DEPLOY_HOURS = 2
DEPLOYMENT_AGE_THRESHOLD_DAYS = 7  # After this many days, use stable threshold

# ── Layer 1: access_log.jsonl ──────────────────────────────────────────────

def get_access_log_path(workspace):
    """Get the path to access_log.jsonl in the workspace."""
    return os.path.join(workspace, ACCESS_LOG_FILENAME)


def append_access_log(workspace, file_path, context="", tags=None):
    """Append an entry to access_log.jsonl (Layer 1 signal).

    Called by agent after memory_get reads a memory file.

    Args:
        workspace: Path to the memory workspace.
        file_path: Relative path of the memory file that was read.
        context: Brief description of why the file was accessed.
        tags: Optional list of tags related to the access.
    """
    log_path = get_access_log_path(workspace)
    entry = {
        "file": file_path,
        "ts": datetime.now(CST).isoformat(),
        "context": context[:200] if context else "",
        "tags": tags or [],
    }

    # Append to log file (create if not exists)
    with open(log_path, "a", encoding="utf-8") as f:
        f.write(json.dumps(entry, ensure_ascii=False) + "\n")


def read_access_log(workspace, since_ts=None):
    """Read entries from access_log.jsonl, optionally filtered by timestamp.

    Args:
        workspace: Path to the memory workspace.
        since_ts: Only return entries after this ISO timestamp.

    Returns:
        list[dict]: Log entries, newest last.
    """
    log_path = get_access_log_path(workspace)
    if not os.path.exists(log_path):
        return []

    entries = []
    with open(log_path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                entry = json.loads(line)
                if since_ts and entry.get("ts", "") < since_ts:
                    continue
                entries.append(entry)
            except json.JSONDecodeError:
                continue

    return entries


def _contains_cjk(text):
    """Check if text contains CJK characters."""
    return bool(re.search(r'[\u4e00-\u9fff]', text))


def count_access_log_hits(log_entries, meta_memories):
    """Count how many times each memory file appears in the access log.

    Matching strategy: extract source file name from memory content prefix
    (e.g. '[2026-04-12.md ...]' or '[MEMORY.md ...]') and match against
    access_log file paths. Falls back to file_path field if no prefix match.

    Args:
        log_entries: List of access_log entries.
        meta_memories: List of memory dicts from meta.json.

    Returns:
        dict: {memory_id: log_count}
    """
    import re

    # Build source_file → [memory_ids] mapping
    source_to_ids = {}
    for mem in meta_memories:
        mid = mem.get("id", "")
        if not mid:
            continue
        # Priority 1: explicit source_file field (set by memory_sync)
        sf = mem.get("source_file", "")
        if sf:
            source_to_ids.setdefault(sf, []).append(mid)
            continue
        # Priority 2: extract from content prefix
        content = mem.get("content", "")
        m = re.match(r'^\[([^\]]+\.md)\b', content)
        if m:
            source_file = m.group(1)
            # Normalize: ensure it's a relative path
            if not source_file.startswith("memory/") and source_file != "MEMORY.md":
                source_file = "memory/" + source_file
            source_to_ids.setdefault(source_file, []).append(mid)
        # Also try file_path as fallback (classification dir path)
        fp = mem.get("file_path", "")
        if fp:
            source_to_ids.setdefault(fp, []).append(mid)

    counts = {}
    for entry in log_entries:
        f = entry.get("file", "")
        if not f:
            continue
        # Exact match
        ids = source_to_ids.get(f, [])
        if not ids:
            # Try with memory/ prefix
            ids = source_to_ids.get("memory/" + f if not f.startswith("memory/") else f, [])
        for mid in ids:
            counts[mid] = counts.get(mid, 0) + 1

    return counts


# ── Layer 2: cron inference ────────────────────────────────────────────────

def cron_infer_access(workspace, meta_path, memories=None):
    """Infer access counts from daily_notes keywords and file mtime changes.

    Called at run_batch start. Scans daily_notes for keyword matches
    against memory tags/titles, and checks file modification times.

    Args:
        workspace: Path to the memory workspace.
        meta_path: Path to meta.json.
        memories: Optional pre-loaded memories list (avoids double I/O).

    Returns:
        dict: {memory_id: infer_count}
    """
    if memories is None:
        meta = load_meta(meta_path)
        memories = meta.get("memories", [])
    infer_counts = {}

    # 1. Check file mtime changes (last_modified > last_accessed → active use)
    for mem in memories:
        if mem.get("status", "active") != "active":
            continue

        mid = mem.get("id", "")
        if not mid:
            continue

        # Use source_file (set by memory_sync) or file_path as fallback
        f = mem.get("source_file", "") or mem.get("file_path", "")
        if not f:
            continue

        file_path = os.path.join(workspace, f)
        if not os.path.exists(file_path):
            continue

        try:
            mtime = os.path.getmtime(file_path)
            last_accessed_str = mem.get("last_accessed", mem.get("created_at", ""))
            if last_accessed_str:
                # Parse ISO timestamp to compare
                last_ts = datetime.fromisoformat(last_accessed_str).timestamp()
                if mtime > last_ts:
                    infer_counts[mid] = infer_counts.get(mid, 0) + 1
        except (ValueError, OSError):
            continue

    # 2. Keyword matching from recent daily notes
    memory_dir = os.path.join(workspace, "memory")
    if os.path.isdir(memory_dir):
        # Get keywords from all active memories
        mem_keywords = {}
        for mem in memories:
            if mem.get("status", "active") != "active":
                continue
            mid = mem.get("id", "")
            tags = mem.get("tags", [])
            title = mem.get("title", "")
            keywords = set()
            for tag in tags:
                if len(tag) >= 2:
                    keywords.add(tag.lower())
            if title:
                # Add title words as keywords (skip short ones)
                for word in title.split():
                    if len(word) >= 3:
                        keywords.add(word.lower())
            if keywords:
                mem_keywords[mid] = keywords

        # Scan recent daily notes (last 3 days)
        now = datetime.now(CST)
        for day_offset in range(3):
            day = now.replace(hour=0, minute=0, second=0, microsecond=0) - timedelta(days=day_offset)
            day_str = day.strftime("%Y-%m-%d")
            note_path = os.path.join(memory_dir, f"{day_str}.md")
            if not os.path.exists(note_path):
                continue

            try:
                with open(note_path, "r", encoding="utf-8") as f:
                    content = f.read().lower()
            except OSError:
                continue

            # Match keywords — use bigram for CJK tags, exact word for ASCII
            for mid, keywords in mem_keywords.items():
                for kw in keywords:
                    matched = False
                    if _contains_cjk(kw):
                        # CJK: check if any bigram of kw appears in content
                        for bi in range(len(kw) - 1):
                            if kw[bi:bi+2] in content:
                                matched = True
                                break
                    else:
                        matched = kw in content
                    if matched:
                        infer_counts[mid] = infer_counts.get(mid, 0) + 1
                        break  # One match per memory per day is enough

    return infer_counts


# ── Signal health check ────────────────────────────────────────────────────

def check_signal_health(workspace, decay_config=None, meta_path=None):
    """Check if Layer 1 (access_log) signal is healthy.

    Args:
        workspace: Path to the memory workspace.
        decay_config: Optional decay_config dict for custom threshold.
        meta_path: Optional path to meta.json for deployment age detection.

    Returns:
        dict: {
            "layer1_active": bool,
            "layer2_active": True,  # Layer 2 is always active
            "stale_hours": float or None,
            "threshold_hours": float,
            "degraded": bool,
        }
    """
    log_path = get_access_log_path(workspace)

    # Determine threshold based on deployment age
    config = decay_config or {}
    stable_hours = config.get("signal_stale_threshold_hours", SIGNAL_STALE_THRESHOLD_HOURS)
    deploy_hours = config.get("signal_stale_threshold_deploy_hours", SIGNAL_STALE_THRESHOLD_DEPLOY_HOURS)
    deploy_days = config.get("deployment_age_days", DEPLOYMENT_AGE_THRESHOLD_DAYS)

    # Check if we're in deployment period (meta.json created < N days ago)
    # meta.json is in workspace/memory/meta.json
    if meta_path:
        actual_meta = meta_path
    else:
        actual_meta = os.path.join(workspace, "memory", "meta.json")
    in_deploy_period = False
    if os.path.exists(actual_meta):
        try:
            created = os.path.getctime(actual_meta)
            age_days = (datetime.now(CST).timestamp() - created) / 86400
            in_deploy_period = age_days < deploy_days
        except OSError:
            pass

    threshold_hours = deploy_hours if in_deploy_period else stable_hours

    if not os.path.exists(log_path):
        return {
            "layer1_active": False,
            "layer2_active": True,
            "stale_hours": None,
            "threshold_hours": threshold_hours,
            "degraded": True,
            "reason": "access_log.jsonl does not exist",
        }

    try:
        mtime = os.path.getmtime(log_path)
        stale_hours = (datetime.now(CST).timestamp() - mtime) / 3600
    except OSError:
        return {
            "layer1_active": False,
            "layer2_active": True,
            "stale_hours": None,
            "threshold_hours": threshold_hours,
            "degraded": True,
            "reason": "cannot read access_log.jsonl mtime",
        }

    layer1_active = stale_hours <= threshold_hours

    result = {
        "layer1_active": layer1_active,
        "layer2_active": True,
        "stale_hours": round(stale_hours, 1),
        "threshold_hours": threshold_hours,
        "degraded": not layer1_active,
    }

    if not layer1_active:
        result["reason"] = f"signal_layer_1_stale: no new access_log entries for {stale_hours:.1f}h (threshold: {threshold_hours}h), degraded to layer_2_only"

    return result


# ── Signal merging ─────────────────────────────────────────────────────────

def merge_signals(meta_path, workspace, decay_config=None, dry_run=False):
    """Merge Layer 1 and Layer 2 signals into meta.json access_count fields.

    Called at run_batch start. Combines both layers according to configurable
    weights, then updates each memory's access_count.

    Formula:
        effective_access = log_count × w1 + infer_count × w2

    If Layer 1 is degraded (health check fails), only Layer 2 is used.

    Args:
        meta_path: Path to meta.json.
        workspace: Path to the memory workspace.
        decay_config: Optional decay_config dict.
        dry_run: If True, don't write changes.

    Returns:
        dict: Summary of signal merge results.
    """
    config = decay_config or {}
    weights = config.get("signal_weights", SIGNAL_WEIGHTS_DEFAULT)
    w1 = weights.get("access_log_weight", 1.0)
    w2 = weights.get("infer_weight", 0.5)

    # Health check
    health = check_signal_health(workspace, config, meta_path=meta_path)
    layer1_active = health["layer1_active"]

    meta = load_meta(meta_path)
    memories = meta.get("memories", [])

    # Layer 1: count access_log hits
    log_counts = {}
    if layer1_active:
        # Read entries since last run (use last_accessed of newest memory as cutoff)
        cutoff = meta.get("last_signal_merge", "")
        log_entries = read_access_log(workspace, since_ts=cutoff if cutoff else None)
        log_counts = count_access_log_hits(log_entries, memories)

    # Layer 2: cron inference (with dedup — skip if already inferred today)
    infer_counts = {}
    last_merge = meta.get("last_signal_merge", "")
    today_str = datetime.now(CST).strftime("%Y-%m-%d")
    should_infer = not last_merge or not last_merge.startswith(today_str)
    if should_infer:
        infer_counts = cron_infer_access(workspace, meta_path, memories=memories)

    # Merge and update
    updated = 0
    total_signal = 0
    for mem in memories:
        if mem.get("status", "active") != "active":
            continue

        mid = mem.get("id", "")
        lc = log_counts.get(mid, 0)
        ic = infer_counts.get(mid, 0)

        # Merge formula
        effective = 0
        if layer1_active:
            effective = lc * w1 + ic * w2
        else:
            effective = ic * w2

        if effective > 0:
            old_count = mem.get("access_count", 0)
            mem["access_count"] = old_count + int(math.ceil(effective))
            mem["last_accessed"] = datetime.now(CST).isoformat()
            updated += 1
            total_signal += effective

    # Update signal_source in meta
    meta["signal_source"] = "dual" if layer1_active else "proxy_only"
    meta["signal_health"] = health
    meta["last_signal_merge"] = datetime.now(CST).isoformat()

    if not dry_run:
        save_meta(meta_path, meta)
        # Truncate access_log to keep last 30 days
        _truncate_access_log(workspace, keep_days=30)

    result = {
        "layer1_active": layer1_active,
        "layer1_hits": sum(log_counts.values()),
        "layer2_inferences": sum(infer_counts.values()),
        "memories_updated": updated,
        "total_signal": round(total_signal, 2),
        "signal_source": meta["signal_source"],
        "health": health,
        "degraded": health.get("degraded", False),
    }
    if health.get("degraded"):
        result["warning"] = health.get("reason", "Layer 1 signal degraded")

    return result


# ── Access log maintenance ─────────────────────────────────────────────────

def _truncate_access_log(workspace, keep_days=30):
    """Remove access_log entries older than keep_days.

    Called after merge_signals to prevent unbounded growth.
    """
    log_path = get_access_log_path(workspace)
    if not os.path.exists(log_path):
        return

    cutoff = (datetime.now(CST) - timedelta(days=keep_days)).isoformat()
    kept = []
    total_lines = 0
    with open(log_path, "r", encoding="utf-8") as f:
        for line in f:
            total_lines += 1
            line = line.strip()
            if not line:
                continue
            try:
                entry = json.loads(line)
                if entry.get("ts", "") > cutoff:
                    kept.append(line)
            except json.JSONDecodeError:
                continue

    if len(kept) < total_lines:
        with open(log_path, "w", encoding="utf-8") as f:
            for line in kept:
                f.write(line + "\n")


# ── CLI entry point ────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description="Signal loop: dual-layer access signals")
    parser.add_argument("--workspace", default=".", help="Memory workspace path")
    parser.add_argument("--meta", default=None, help="Path to meta.json")
    parser.add_argument("--dry-run", action="store_true", help="Don't write changes")
    parser.add_argument("--health-only", action="store_true", help="Only check signal health")
    args = parser.parse_args()

    workspace = os.path.abspath(args.workspace)
    meta_path = args.meta or os.path.join(workspace, "memory", "meta.json")

    if args.health_only:
        result = check_signal_health(workspace)
        print(json.dumps(result, indent=2, ensure_ascii=False))
        return

    result = merge_signals(meta_path, workspace, dry_run=args.dry_run)
    print(json.dumps(result, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()

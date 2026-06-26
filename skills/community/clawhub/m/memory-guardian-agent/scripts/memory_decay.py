#!/usr/bin/env python3
"""memory-guardian: Five-track Bayesian decay engine (v0.4.6).

Computes decay_score for all memories based on five tracks:
  1. importance_track  — base importance × cost signal modifier
  2. network_track     — access + trigger + cooling + dual-layer signals (v0.4.5)
  3. context_track     — recency × access pattern
  4. cooling_track     — 24h high-frequency detection
  5. beta_track        — log-smooth idle decay (v0.4.1) + scar maturity (v0.4)
                        + reactivation_count slowdown (v0.4.5)

v0.4.5 additions:
  - Dual-layer signals: file_loaded=1.0 / search_hit=0.5 / content_modified=1.5
  - reactivation_count: effective_decay = base × (1 / (1 + reactivation_count × 0.3))
  - Signal recording: record_signal() for external callers (MCP tools, router)
  - access_signals log: rolling buffer of recent signals

Formula:
  final = (0.35 × importance_factor + 0.35 × network_factor + 0.30 × context_factor) × β_effective

Usage:
  python3 memory_decay.py [--meta <path>] [--lambda <float>] [--dry-run]
"""
import json, math, argparse, os, sys
from datetime import datetime
from mg_utils import (
    CASE_TTL,
    COOLING_THRESHOLD,
    CST,
    MEMORY_TYPE_ALPHA_DEFAULTS,
    MEMORY_TYPE_BETA_CAP_DEFAULTS,
    _now_iso,
    get_effective_importance,
    get_memory_type_decay_profile,
    is_protected_memory,
    load_meta,
    save_meta,
)


# ─── Tunable Parameters ──────────────────────────────────────
IMPORTANCE_WEIGHT = 0.35
NETWORK_WEIGHT = 0.35
CONTEXT_WEIGHT = 0.30

COOLING_NETWORK_CAP = 0.3    # network_factor cap during cooling
COOLING_WINDOW_HOURS = 24    # window for frequency detection

# v0.4.1 Log-smooth β parameters (leozhang)
# BETA_ALPHA is configurable via meta.json decay_config.alpha (default: 2.0)
BETA_ALPHA_DEFAULT = 2.0      # default sensitivity for log-smooth decay
BETA_BASE_DAYS_CONSTANT = 7   # base_days = 7 + importance × 23
BETA_BASE_DAYS_SCALE = 23
BETA_IMPORTANCE_CAP = 1.0     # cap importance to prevent infinite base_days
BETA_CAP = 3.0                # β upper cap — above this, mark for archive review
BETA_ARCHIVE_MARK = 3.0       # mark as archive candidate when β exceeds this

# Wakeup weighting (leozhang)
WAKEUP_PASSIVE_BOOST = 1.0    # passive wakeup (external trigger) adds to effective idle
WAKEUP_ACTIVE_BOOST = 0.3     # active wakeup (cron/heartbeat) adds less
ZOMBIE_THRESHOLD_DAYS = 30    # if only active wakeups for 30d → accelerate
ZOMBIE_ACCELERATION = 1.5     # β multiplier for zombie memories

TTL_GRACE_DAYS = 7           # extend TTL if matched within this window

# v0.4.2 P2: Per-type decay parameters (ovea)
# static memories (bootstrap/core): minimal decay
# derive memories (induced): moderate decay
# absorb memories (external): aggressive decay
TYPE_ALPHA = dict(MEMORY_TYPE_ALPHA_DEFAULTS)
TYPE_BETA_CAP = dict(MEMORY_TYPE_BETA_CAP_DEFAULTS)
DEFAULT_MEMORY_TYPE = "derive"  # fallback for memories without type field

# v0.4.2 P2: Quiet degradation parameters (neuro)
QUIET_DEGRADATION = {
    "min_sample": 5,            # min trigger_count for degradation checks
    "median_discount": 0.7,     # discount factor for median comparison
    "iqr_multiplier": 1.5,      # IQR threshold for outlier detection
    "trigger_exemption": 5,     # trigger_count < this → exempt from degradation
}

# Legacy v0.4 parameters (fallback)
BETA_INITIAL = 1.0
FAILURE_REBOUND = 0.05       # +0.05 beta per failure_count (learning from mistakes)
FAILURE_BOOST_CAP = 2.0      # max failure_boost multiplier (prevents runaway β)
BETA_DECAY = 0.02            # beta decays slowly toward 1.0 over time

COST_IMPORTANCE_MODIFIER = {
    "write": 0.0,
    "verify": 0.05,
    "human": 0.10,
    "transfer": 0.05,
}

# Status that skip archive/delete decisions
PROTECTED_STATUSES = {"draft", "observing", "suspended"}

# ─── v0.4.5: Dual-layer signal weights ─────────────────────
SIGNAL_WEIGHTS = {
    "file_loaded": 1.0,
    "search_hit": 0.5,
    "content_modified": 1.5,
}
REACTIVATION_FACTOR = 0.3          # decay slowdown per reactivation
REACTIVATION_MIN_MULTIPLIER = 0.2  # minimum effective decay (floor)
ACCESS_SIGNALS_MAX = 10            # rolling buffer size




# ─── v0.4.5: Signal recording ────────────────────────────────

def record_signal(mem, signal_type, session_id=None):
    """Record an access signal on a memory entry.

    Args:
        mem: Memory dict (modified in place).
        signal_type: One of "file_loaded", "search_hit", "content_modified".
        session_id: Optional session identifier.

    Returns:
        dict: Updated signal info.
    """
    now = _now_iso()

    # Update signal_level
    mem["signal_level"] = signal_type

    # Update reactivation count
    if signal_type == "search_hit":
        mem["reactivation_count"] = mem.get("reactivation_count", 0) + 1
        mem["last_reactivated"] = now

    # Append to access_signals rolling buffer
    signals = mem.get("access_signals", [])
    signals.append({
        "type": signal_type,
        "at": now,
        "session_id": session_id,
    })
    # Keep only last N signals
    if len(signals) > ACCESS_SIGNALS_MAX:
        mem["access_signals"] = signals[-ACCESS_SIGNALS_MAX:]
    else:
        mem["access_signals"] = signals

    return {
        "signal_type": signal_type,
        "reactivation_count": mem.get("reactivation_count", 0),
        "signal_level": signal_type,
    }


def compute_signal_boost(mem, now):
    """Compute boost from recent access signals.

    Looks at signals within the last 24h and applies weights.

    Returns:
        float: Signal boost value (0.0 to 0.3).
    """
    signals = mem.get("access_signals", [])
    if not signals:
        return 0.0

    now_ts = now.timestamp() if hasattr(now, 'timestamp') else datetime.timestamp(now)
    boost = 0.0

    for sig in signals:
        sig_type = sig.get("type", "")
        weight = SIGNAL_WEIGHTS.get(sig_type, 0.0)
        if weight <= 0:
            continue

        sig_at = sig.get("at", "")
        if not sig_at:
            continue
        try:
            sig_dt = datetime.fromisoformat(sig_at)
            sig_ts = sig_dt.timestamp() if hasattr(sig_dt, 'timestamp') else datetime.timestamp(sig_dt)
            hours_ago = (now_ts - sig_ts) / 3600
            if hours_ago < 0:
                hours_ago = 0
            if hours_ago < 24:
                # Linear decay within 24h window
                recency = 1.0 - (hours_ago / 24)
                boost += weight * recency * 0.05  # Scale to max ~0.05 per signal
        except (ValueError, TypeError):
            continue

    return min(boost, 0.3)  # Cap at 0.3


def compute_reactivation_multiplier(mem):
    """Compute decay slowdown from reactivation_count.

    More reactivations → slower decay (memory proven valuable on re-access).

    Returns:
        float: Multiplier in [REACTIVATION_MIN_MULTIPLIER, 1.0]
    """
    count = mem.get("reactivation_count", 0)
    if count <= 0:
        return 1.0
    multiplier = 1.0 / (1.0 + count * REACTIVATION_FACTOR)
    return max(multiplier, REACTIVATION_MIN_MULTIPLIER)



def compute_importance_factor(mem):
    """Track 1: importance × cost signal modifier (L0/L1 threshold)."""
    base = get_effective_importance(mem)

    # Cost signal modifier (L1 only)
    cost_factors = mem.get("cost_factors", {})
    modifier = 0.0
    modifier += cost_factors.get("write_cost", 0) * COST_IMPORTANCE_MODIFIER["write"]
    modifier += cost_factors.get("verify_cost", 0) * COST_IMPORTANCE_MODIFIER["verify"]
    modifier += cost_factors.get("human_cost", 0) * COST_IMPORTANCE_MODIFIER["human"]
    modifier += cost_factors.get("transfer_cost", 0) * COST_IMPORTANCE_MODIFIER["transfer"]

    return min(base + modifier, 1.0)


def compute_network_factor(mem, now):
    """Track 2: access + trigger + cooling + dual-layer signals (v0.4.5).

    Combines access_count and trigger_count with cooling mechanism.
    High-frequency same-source access (>threshold in 24h) caps network_factor.
    v0.4.5: Adds signal_boost from recent access_signals.
    """
    access_count = mem.get("access_count", 0)
    trigger_count = mem.get("trigger_count", 0)

    # Combined interaction score
    ref_max = 100
    raw_access = math.log(1 + access_count) / math.log(1 + ref_max)
    raw_trigger = math.log(1 + trigger_count) / math.log(1 + ref_max)
    raw_combined = min(raw_access + raw_trigger * 0.5, 1.0)

    network = 0.3 + 0.7 * raw_combined  # range [0.3, 1.0]

    # v0.4 case template bonus: has action_conclusion → +10% stability
    if mem.get("action_conclusion"):
        network = min(network * 1.1, 1.0)

    # Confidence bonus: higher confidence → higher network
    confidence = mem.get("confidence", 0.5)
    if confidence > 0.7:
        network = min(network * (1 + 0.05 * (confidence - 0.7)), 1.0)

    # v0.4.5: Dual-layer signal boost
    signal_boost = compute_signal_boost(mem, now)
    if signal_boost > 0:
        network = min(network + signal_boost, 1.0)

    # Cooling check
    cooldown_active = mem.get("cooldown_active", False)
    cooldown_until = mem.get("cooldown_until")

    if cooldown_active:
        if cooldown_until:
            try:
                cd_end = datetime.fromisoformat(cooldown_until)
                if now < cd_end:
                    # Active cooling — cap network_factor
                    network = min(network, COOLING_NETWORK_CAP)
                else:
                    # Cooling expired
                    cooldown_active = False
            except (ValueError, TypeError):
                cooldown_active = False

    return network, cooldown_active


def compute_context_factor(mem, lam, now):
    """Track 3: recency × access pattern.

    Standard exponential decay with access pattern normalization.
    """
    base = float(mem.get("importance", 0.5))
    created = datetime.fromisoformat(mem.get("created_at", _now_iso()))
    days = max((now - created).total_seconds() / 86400, 0)
    recency = math.exp(-lam * days)

    # Access pattern: recently accessed memories get a boost
    last_accessed = mem.get("last_accessed")
    access_boost = 0.0
    if last_accessed:
        try:
            la = datetime.fromisoformat(last_accessed)
            hours_since = max((now - la).total_seconds() / 3600, 0)
            if hours_since < 24:
                access_boost = 0.1 * (1 - hours_since / 24)
            elif hours_since < 72:
                access_boost = 0.03 * (1 - (hours_since - 24) / 48)
        except (ValueError, TypeError):
            pass

    return min(recency * (base / max(base, 0.1)) + access_boost, 1.0)


def _type_decay_profile(mem, decay_config):
    """Resolve type-based alpha and importance for beta decay.

    Returns:
        dict with keys: memory_type, alpha, importance, type_beta_cap, beta
    """
    mem_type = mem.get("memory_type", DEFAULT_MEMORY_TYPE)
    type_profile = get_memory_type_decay_profile(mem_type, decay_config)
    alpha = type_profile["alpha"]

    # Reduce α for low-importance memories
    importance = min(max(get_effective_importance(mem), 0.01), BETA_IMPORTANCE_CAP)
    if importance < 0.1:
        alpha = 1.0  # gentle decay for near-zero importance

    return {
        "memory_type": type_profile["memory_type"],
        "alpha": alpha,
        "importance": importance,
        "type_beta_cap": type_profile["beta_cap"],
        "beta": mem.get("beta", BETA_INITIAL),
    }


def _compute_idle_days(mem, now, days_since_creation):
    """Compute effective idle days from last_accessed or creation time."""
    last_accessed = mem.get("last_accessed")
    if last_accessed:
        try:
            la = datetime.fromisoformat(last_accessed)
            return max((now - la).total_seconds() / 86400, 0)
        except (ValueError, TypeError):
            return days_since_creation
    return days_since_creation


def _quiet_degradation_discount(mem, qd_config, _precomputed_betas, meta, beta_log_smooth):
    """Apply IQR-adaptive median discount for quiet degradation (neuro).

    Returns:
        float: The (possibly discounted) beta_log_smooth value.
    """
    trigger_count = mem.get("trigger_count", 0)
    qd_min_sample = qd_config.get("min_sample", QUIET_DEGRADATION["min_sample"])
    qd_median_discount = qd_config.get("median_discount", QUIET_DEGRADATION["median_discount"])
    trigger_exempt = trigger_count < qd_config.get("trigger_exemption",
                                                    QUIET_DEGRADATION["trigger_exemption"])

    if trigger_exempt or not meta:
        return beta_log_smooth

    qd_iqr_mult = qd_config.get("iqr_multiplier", QUIET_DEGRADATION["iqr_multiplier"])
    all_betas = _precomputed_betas if _precomputed_betas is not None else []
    if not all_betas:
        for m in (meta.get("memories", []) if isinstance(meta, dict) else []):
            if m.get("status", "active") == "active" and m.get("id") != mem.get("id"):
                all_betas.append(m.get("beta", BETA_INITIAL))
    if len(all_betas) < qd_min_sample:
        return beta_log_smooth

    all_betas.sort()
    n = len(all_betas)
    median_beta = all_betas[n // 2]
    q1_idx = max(0, n // 4)
    q3_idx = min(n - 1, 3 * n // 4)
    iqr = all_betas[q3_idx] - all_betas[q1_idx]
    iqr_threshold = median_beta + qd_iqr_mult * iqr
    if beta_log_smooth > iqr_threshold:
        discount = qd_median_discount
        beta_log_smooth = beta_log_smooth * discount + median_beta * (1 - discount)
    return beta_log_smooth


def _zombie_detection(mem, idle_days, beta_log_smooth):
    """Detect zombie memories and apply acceleration.

    Returns:
        tuple: (is_zombie, adjusted_beta_log_smooth)
    """
    wakeup_streak = mem.get("passive_wakeup_streak", 0)
    is_zombie = (wakeup_streak == 0 and idle_days > ZOMBIE_THRESHOLD_DAYS)
    if is_zombie:
        beta_log_smooth *= ZOMBIE_ACCELERATION
    return is_zombie, beta_log_smooth


def _failure_rebound(mem, days_since_creation):
    """Compute failure rebound boost and time decay for scar memory.

    Returns:
        dict with keys: failure_boost, time_decay
    """
    failure_count = mem.get("failure_count", 0)
    failure_boost = min(failure_count * FAILURE_REBOUND, FAILURE_BOOST_CAP)
    time_decay = max(0, BETA_DECAY * (days_since_creation / 30))
    return {"failure_boost": failure_boost, "time_decay": time_decay}


def compute_beta_recovery(mem, now, meta=None, _precomputed_betas=None):
    """Track 5: log-smooth idle decay (v0.4.1) + scar maturity (v0.4).

    v0.4.1: β_multiplier = max(1, 1 + α × ln(idle_days / base_days))
      where base_days = 7 + importance × 23
      α is configurable via meta.json decay_config.alpha (default: 2.0)

    Combined with v0.4 failure rebound:
      β_effective = β_log_smooth × (1 + failure_boost) - time_decay

    Backward compatible: if no last_accessed, falls back to v0.4 fixed β + failure.

    Args:
        _precomputed_betas: Optional pre-sorted list of all active beta values.
    """
    decay_config = meta.get("decay_config", {}) if isinstance(meta, dict) else {}

    # 1. Type-based alpha & importance
    tp = _type_decay_profile(mem, decay_config)

    # 2. Compute idle days
    created = datetime.fromisoformat(mem.get("created_at", _now_iso()))
    days_since_creation = max((now - created).total_seconds() / 86400, 0)
    idle_days = _compute_idle_days(mem, now, days_since_creation)

    # 3. Log-smooth decay
    base_days = BETA_BASE_DAYS_CONSTANT + tp["importance"] * BETA_BASE_DAYS_SCALE
    if idle_days >= base_days and idle_days > 0:
        beta_log_smooth = 1.0 + tp["alpha"] * math.log(idle_days / base_days)
    else:
        beta_log_smooth = 1.0

    # 4. Quiet degradation IQR discount
    qd_config = (meta.get("decay_config", {}).get("quiet_degradation", {})
                 if meta else {})
    beta_log_smooth = _quiet_degradation_discount(
        mem, qd_config, _precomputed_betas, meta, beta_log_smooth)

    # 5. Zombie detection
    is_zombie, beta_log_smooth = _zombie_detection(mem, idle_days, beta_log_smooth)

    # 6. Per-type cap
    beta_log_smooth = min(beta_log_smooth, tp["type_beta_cap"])

    # 7. Reactivation slowdown
    reactivation_mult = compute_reactivation_multiplier(mem)
    beta_log_smooth *= reactivation_mult

    # 8. Failure rebound & time decay
    fr = _failure_rebound(mem, days_since_creation)
    effective_beta = beta_log_smooth * (1 + fr["failure_boost"]) - fr["time_decay"]
    effective_beta = max(effective_beta, 0.1)  # minimum floor

    return round(effective_beta, 4), effective_beta >= BETA_ARCHIVE_MARK, is_zombie


def check_ttl(mem, now):
    """v0.4.1: Check if memory has exceeded its case-type TTL.

    Returns: (ttl_expired, ttl_days_remaining)
    Only applies to case records with a case_origin field.
    """
    case_origin = mem.get("case_origin", "")
    if not case_origin or case_origin not in CASE_TTL:
        return False, None  # Non-case or unknown origin: no TTL

    ttl_days = CASE_TTL[case_origin]
    ttl_start = mem.get("ttl_start_time") or mem.get("created_at")

    if not ttl_start:
        return False, None

    try:
        start = datetime.fromisoformat(ttl_start)
        elapsed = (now - start).total_seconds() / 86400
        remaining = ttl_days - elapsed

        # Grace extension: if recently matched, extend TTL
        last_triggered = mem.get("last_triggered")
        if last_triggered and remaining < TTL_GRACE_DAYS:
            try:
                lt = datetime.fromisoformat(last_triggered)
                if (now - lt).total_seconds() / 86400 < TTL_GRACE_DAYS:
                    remaining = TTL_GRACE_DAYS  # extend by grace period
            except (ValueError, TypeError):
                pass

        return remaining <= 0, round(remaining, 1)
    except (ValueError, TypeError):
        return False, None


def compute_decay(mem, lam, now, meta=None, _precomputed_betas=None):
    """Compute full five-track decay score.

    Args:
        _precomputed_betas: Optional pre-sorted list of all active beta values
            to avoid O(N²) recollection in quiet degradation.
    """
    importance_f = compute_importance_factor(mem)
    network_f, cooldown_active = compute_network_factor(mem, now)
    context_f = compute_context_factor(mem, lam, now)
    beta_r, archive_mark, is_zombie = compute_beta_recovery(
        mem, now, meta=meta, _precomputed_betas=_precomputed_betas)

    # Weighted combination
    weighted = (IMPORTANCE_WEIGHT * importance_f +
                NETWORK_WEIGHT * network_f +
                CONTEXT_WEIGHT * context_f)

    final = weighted * beta_r

    # Failure conditions penalty: active failures reduce score
    failure_conditions = mem.get("failure_conditions", [])
    if failure_conditions:
        total_failures = sum(fc.get("count", 0) for fc in failure_conditions)
        penalty = min(total_failures * 0.03, 0.15)  # max 15% penalty
        final = final * (1 - penalty)

    # v0.4.1 TTL check
    ttl_expired, ttl_remaining = check_ttl(mem, now)
    if ttl_expired:
        final = final * 0.5  # halve score when TTL expired (soft archive)

    return {
        "new_score": round(min(max(final, 0.0), 1.0), 4),
        "cooldown_active": cooldown_active,
        "archive_mark": archive_mark,
        "is_zombie": is_zombie,
        "beta_recovery": beta_r,
        "importance_factor": importance_f,
        "network_factor": network_f,
        "context_factor": context_f,
    }


def run(meta_path, lam, dry_run):
    meta = load_meta(meta_path)
    now = datetime.now(CST)
    changes = []
    to_archive = []
    to_delete = []
    archive_candidates = []  # v0.4.1: β > cap

    # Precompute all active betas once (O(N)) instead of per-memory (O(N²))
    all_active_betas = sorted([
        m.get("beta", BETA_INITIAL)
        for m in meta.get("memories", [])
        if m.get("status", "active") == "active"
    ])

    for mem in meta.get("memories", []):
        status = mem.get("status", "active")
        protected_memory = is_protected_memory(mem)

        if protected_memory and status == "archived":
            status = "active"
            if not dry_run:
                mem["status"] = "active"
                mem["pinned"] = True

        # Protected statuses skip archive/delete
        if status in PROTECTED_STATUSES:
            continue

        old_score = float(mem.get("decay_score", mem.get("importance", 0.5)))
        result = compute_decay(mem, lam, now, meta=meta, _precomputed_betas=all_active_betas)
        new_score = result["new_score"]
        cooldown_active = result["cooldown_active"]
        archive_mark = result["archive_mark"]
        is_zombie = result["is_zombie"]
        beta_r = result["beta_recovery"]
        importance_f = result["importance_factor"]
        network_f = result["network_factor"]
        context_f = result["context_factor"]
        changes.append({
            "id": mem.get("id", "?"),
            "content": mem.get("content", "")[:60],
            "old_score": old_score,
            "new_score": new_score,
            "importance_f": round(importance_f, 3),
            "network_f": round(network_f, 3),
            "context_f": round(context_f, 3),
            "beta": round(beta_r, 3),
            "cooling": cooldown_active,
            "archive_mark": archive_mark,
            "zombie": is_zombie,
        })

        if not dry_run:
            mem["decay_score"] = new_score
            mem["cooldown_active"] = cooldown_active
            if protected_memory:
                mem["status"] = "active"
                mem["pinned"] = True
            # Fix missing last_accessed: if accessed before but field missing,
            # backfill from created_at to prevent inaccurate idle_days calculation
            if not mem.get("last_accessed") and mem.get("access_count", 0) > 0:
                mem["last_accessed"] = mem.get("created_at", "")
            if archive_mark:
                mem.setdefault("quality_gate", {})
                mem["quality_gate"]["beta_archive_candidate"] = True
                mem["quality_gate"]["beta_value"] = round(beta_r, 3)

        if protected_memory:
            continue
        if new_score < 0.05:
            to_delete.append(mem)
            if not dry_run:
                mem["status"] = "deleted"
        elif new_score < 0.2 and status == "active":
            to_archive.append(mem)
            if not dry_run:
                mem["status"] = "archived"

        if archive_mark and status == "active":
            archive_candidates.append(mem)

    if dry_run:
        print("=== DRY RUN (Five-Track Decay v0.4.1) ===")
    else:
        save_meta(meta_path, meta)

    print(f"Processed {len(changes)} memories (lambda={lam})")
    print(f"Weights: importance={IMPORTANCE_WEIGHT} network={NETWORK_WEIGHT} context={CONTEXT_WEIGHT}")
    print(f"  To archive (score < 0.2): {len(to_archive)}")
    print(f"  To delete  (score < 0.05): {len(to_delete)}")
    print(f"  Archive candidates (beta >= {BETA_ARCHIVE_MARK}): {len(archive_candidates)}")
    print()

    # Show top movers
    changes.sort(key=lambda x: x["new_score"] - x["old_score"], reverse=True)
    for c in changes[:8]:
        delta = c["new_score"] - c["old_score"]
        arrow = "up" if delta > 0.01 else ("down" if delta < -0.01 else "same")
        cool = " [cooling]" if c["cooling"] else ""
        zombie = " [zombie]" if c["zombie"] else ""
        mark = " [review]" if c["archive_mark"] else ""
        print(f"  [{c['id']}] {arrow} {c['old_score']:.3f} -> {c['new_score']:.3f}"
              f" (imp={c['importance_f']} net={c['network_f']} ctx={c['context_f']} beta={c['beta']}){cool}{zombie}{mark}")
        print(f"      {c['content']}")
    if len(changes) > 8:
        print(f"  ... and {len(changes) - 8} more")

    # Cooling summary
    cooling_count = sum(1 for c in changes if c["cooling"])
    zombie_count = sum(1 for c in changes if c["zombie"])
    if cooling_count or zombie_count:
        print(f"\nCooling: {cooling_count} | Zombies: {zombie_count}")
    if archive_candidates:
        print(f"Review: {len(archive_candidates)} memories flagged as archive candidates (beta >= {BETA_ARCHIVE_MARK})")
        for m in archive_candidates[:5]:
            print(f"    - [{m.get('id','?')}] beta={m.get('quality_gate',{}).get('beta_value','?')}")

    return {
        "changes": changes,
        "to_archive": len(to_archive),
        "to_delete": len(to_delete),
        "cooling_count": cooling_count,
        "zombie_count": zombie_count,
        "archive_candidates": len(archive_candidates),
    }


if __name__ == "__main__":
    p = argparse.ArgumentParser(description="memory-guardian five-track decay engine (v0.4)")
    p.add_argument("--workspace", default=None, help="Workspace root path")
    p.add_argument("--meta", default=None, help="Path to meta.json")
    p.add_argument("--lambda", type=float, default=0.01, help="Decay rate λ (default: 0.01)")
    p.add_argument("--dry-run", action="store_true", help="Show results without writing")
    args = p.parse_args()

    workspace = args.workspace or os.environ.get(
        "OPENCLAW_WORKSPACE", os.path.expanduser("~/workspace/agent/workspace")
    )
    meta_path = args.meta or os.path.join(workspace, "memory", "meta.json")
    run(meta_path, args.__dict__["lambda"], args.dry_run)

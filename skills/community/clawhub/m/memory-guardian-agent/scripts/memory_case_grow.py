#!/usr/bin/env python3
"""memory-guardian: Case self-growth engine (v0.4.1).

Implements the full case lifecycle with v0.4.1 additions:
  - observing → active promotion (trigger_count ≥ 3 + feedback)
  - v0.4.1: Temporary observation pool (neuro/leozhang)
  - v0.4.1: Quadrant TTL (chaonengnono)
  - v0.4.1: Result feedback tracking (ovea)
  - v0.4.1: Post-stress review (SimonClaw) — authority context marking + pressure-free re-evaluation
  - v0.4.1: Tag penalty scheme A — ×1.3 multiplier for context deviation
  - Dynamic confidence discount for observing cases
  - Split logic A (systemic inconsistency, N=5) / B (insufficient granularity)
  - Merge logic (triple condition: behavior N=5 + tag Jaccard>0.8 + consequence direction)
  - Confidence asymmetric adjustment (+0.1 / -0.3)
  - Failure conditions dedup via intent clustering

Usage:
  python3 memory_case_grow.py status [--workspace <path>]
  python3 memory_case_grow.py grow [--workspace <path>] [--dry-run]
  python3 memory_case_grow.py merge [--workspace <path>] [--dry-run]
  python3 memory_case_grow.py conflict [--workspace <path>] [--dry-run]
  python3 memory_case_grow.py pool [--workspace <path>]  (v0.4.1)
"""
import json, os, argparse, re, uuid, copy
from datetime import datetime, timezone, timedelta
from collections import Counter
from mg_utils import _now_iso, CST, tokenize as _tokenize, load_meta, save_meta, safe_print
from mg_events.telemetry import record_module_run

print = safe_print

# ─── Growth Parameters ──────────────────────────────────────
OBSERVING_PROMOTE_N = 3        # trigger_count to promote observing → active
SUSPEND_CONFIRM_N = 2          # suspended entries confirmed after N triggers
SPLIT_SYSTEMIC_N = 5           # inconsistencies before systemic split
SPLIT_SCENARIO_N = 5           # inconsistencies before scenario split
MERGE_BEHAVIOR_N = 5           # consistent behaviors for merge
MERGE_JACCARD_THRESHOLD = 0.8  # tag overlap threshold for merge
CONFIDENCE_BOOST = 0.1         # +0.1 on consistent trigger
CONFIDENCE_PENALTY = 0.3       # -0.3 on inconsistent trigger
CONFIDENCE_FLOOR = 0.1         # minimum confidence
CONFIDENCE_MERGE_INIT = 0.7    # confidence after merge (probation)
CONFIDENCE_SPLIT_INIT = 0.5    # confidence after split
MAX_FAILURE_CONDITIONS = 20    # cap on failure conditions per case

# v0.4.1: Temporary observation pool (neuro/leozhang)
POOL_OBSERVATION_HOURS = 72    # max hours in observation pool
POOL_OBSERVATION_TRIGGERS = 5  # max triggers before forced evaluation
POOL_RISK_TAG_REQUIRED = 1     # min risk tags to be a valid case
POOL_POSITIVE_FEEDBACK_REQUIRED = 1  # min positive feedbacks for promotion (v0.4.1)

# v0.4.1: Quadrant TTL (chaonengnono) — canonical definition in mg_utils
from mg_utils import CASE_TTL

# v0.4.1: Adaptive thresholds
DEFAULT_ABSORB_THRESHOLD = 0.8
DEFAULT_DERIVE_THRESHOLD = 0.5
DEFAULT_NEW_TYPE_THRESHOLD = 0.3


class SceneGroup:
    def __init__(self, group_id, tag_prefix=""):
        self.group_id = group_id
        self.tag_prefix = tag_prefix
        self.case_ids = []
        self.N = 0
        self.adaptive_threshold = None
    
    def update(self, case_ids):
        self.case_ids = case_ids
        self.N = len(case_ids)
        self._compute_threshold()
    
    def _compute_threshold(self):
        # N < 20: fixed thresholds (0.8/0.5/0.3)
        # N >= 20: linear scaling
        if self.N < 20:
            self.adaptive_threshold = None  # use defaults
        elif self.N < 50:
            delta = 0.05  # max adjustment
            factor = (self.N - 20) / 30
            self.adaptive_threshold = {
                "absorb": 0.8 + factor * delta,
                "derive": 0.5 - factor * delta * 0.5,
                "new_type": 0.3 + factor * delta * 0.3,
            }
        else:
            self.adaptive_threshold = {
                "absorb": 0.85,
                "derive": 0.45,
                "new_type": 0.35,
            }


# v0.4.1: Post-stress review (SimonClaw: authority context + pressure-free re-evaluation)
AUTHORITY_TAG_KEYWORDS = ["权威", "老板", "manager", "boss", "领导", "上级", "审批", "review",
                         "authority", "hierarchy", "performance_review", "考核"]
POST_STRESS_COOLDOWN_HOURS = 24  # default cooldown before re-evaluation
POST_STRESS_CONFIDENCE_MATCH_BONUS = 0.1
POST_STRESS_CONFIDENCE_MISMATCH_PENALTY = -0.3  # downgrade to L1 notify
# CONFIDENCE_FLOOR already defined above (L38), not redefined here
CONFIDENCE_SUSPEND_THRESHOLD = 0.1

# v0.4.1: Tag penalty scheme A — context deviation multiplier
TAG_PENALTY_MULTIPLIER = 1.3
TAG_PENALTY_APPLICABLE_ACTIONS = {"delete", "modify", "remove"}

# v0.4.2 P2: Context burrs (velvet_claw) — preserve 3 types of "noise" in case.context
# Types: situation_context (情境上下文), failure_case (失败案例), dispute_record (争议记录)
CONTEXT_BURR_TYPES = ["situation_context", "failure_case", "dispute_record"]
CONTEXT_BURR_MAX_ITEMS = 10   # max items per burr type
CONTEXT_BURR_MAX_TOTAL = 30  # max total burrs across all types


def mark_authority_context(mem_entry):
    """Check if a memory entry was created in an authority/high-pressure context.

    Criteria (SimonClaw):
    - Provenance is L1 (human direct input)
    - Tags or situation contain authority-related keywords

    Args:
        mem_entry: dict, a memory/case entry

    Returns:
        bool: True if this entry should be flagged as authority_context
    """
    # Only L1 provenance (human direct) is eligible
    if mem_entry.get("provenance_level") != "L1":
        return False

    situation = (mem_entry.get("situation") or "").lower()
    tags = [t.lower() for t in mem_entry.get("tags", [])]
    for keyword in AUTHORITY_TAG_KEYWORDS:
        if keyword.lower() in situation or any(keyword.lower() in t for t in tags):
            return True

    return False


def schedule_post_stress_review(mem_entry, cooldown_hours=None):
    """Schedule a post-stress review for an authority-context case.

    Sets review_at_pressure_free to a future timestamp when re-evaluation
    should occur (after pressure has likely subsided).

    Args:
        mem_entry: dict, a memory/case entry (modified in-place)
        cooldown_hours: int or None, hours before review (default: POST_STRESS_COOLDOWN_HOURS)
    """
    if cooldown_hours is None:
        cooldown_hours = POST_STRESS_COOLDOWN_HOURS

    created = mem_entry.get("created_at")
    if created:
        try:
            from datetime import datetime, timedelta
            if isinstance(created, str):
                created_dt = datetime.fromisoformat(created.replace("Z", "+00:00"))
            else:
                created_dt = created
            review_time = created_dt + timedelta(hours=cooldown_hours)
            mem_entry["review_at_pressure_free"] = review_time.isoformat()
        except (ValueError, TypeError):
            # Fallback: set relative timestamp
            import time
            mem_entry["review_at_pressure_free"] = time.strftime(
                "%Y-%m-%dT%H:%M:%S+00:00",
                time.gmtime(time.time() + cooldown_hours * 3600)
            )
    else:
        import time
        mem_entry["review_at_pressure_free"] = time.strftime(
            "%Y-%m-%dT%H:%M:%S+00:00",
            time.gmtime(time.time() + cooldown_hours * 3600)
        )

    mem_entry["authority_context"] = True
    mem_entry["post_stress_review_status"] = "pending"  # pending → reviewed → resolved


def rescan_authority_context(meta_path):
    """Rescan all cases for authority context eligibility.

    Called when tags are modified on existing cases. Cases that newly
    qualify for authority_context get a post-stress review scheduled.

    Returns:
        dict: {"newly_flagged": int, "total_flagged": int}
    """
    meta = load_meta(meta_path)
    newly_flagged = 0
    total_flagged = 0

    for mem in meta.get("memories", []):
        if mem.get("status") not in ("active", "observing"):
            continue

        was_flagged = mem.get("authority_context") is True
        should_flag = mark_authority_context(mem)

        if should_flag and not was_flagged:
            schedule_post_stress_review(mem)
            newly_flagged += 1
        if should_flag:
            total_flagged += 1

    if newly_flagged > 0:
        save_meta(meta_path, meta)

    return {"newly_flagged": newly_flagged, "total_flagged": total_flagged}


def apply_tag_penalty(base_confidence, action_type):
    """Apply scheme A tag penalty (×1.3 multiplier) for high-risk actions.

    SimonClaw: scheme A is lighter weight than formal context_tags[] field.
    Penalty applies to distance calculation, not directly to confidence.
    Effectively raises the threshold for absorb by ×1.3.

    Args:
        base_confidence: float, the computed similarity/distance score
        action_type: str, the action being considered

    Returns:
        float: adjusted confidence score (penalized if applicable)
    """
    if action_type in TAG_PENALTY_APPLICABLE_ACTIONS:
        # Apply ×1.3 to the "distance from absorb threshold"
        # If base is 0.85 and absorb threshold is 0.8, distance is 0.05
        # Penalized: 0.8 - 0.05 * 1.3 = 0.735
        # This makes it harder to absorb when context deviates
        return max(0.0, base_confidence / TAG_PENALTY_MULTIPLIER)
    return base_confidence


# ─── v0.4.2 P2: Context Burrs (velvet_claw) ──────────────────

def add_context_burr(mem_entry, burr_type, burr_data):
    """Add a context burr to a case entry.

    Context burrs preserve "noise" that's actually valuable for case matching:
    - situation_context: Contextual situations where this case was relevant
    - failure_case: Instances where this case failed or was misapplied
    - dispute_record: Times when this case was controversial or contested

    Args:
        mem_entry: dict, a case entry (modified in-place)
        burr_type: str, one of CONTEXT_BURR_TYPES
        burr_data: dict, the burr data (any structure)

    Returns:
        bool: True if added, False if rejected (invalid type or at capacity)
    """
    if burr_type not in CONTEXT_BURR_TYPES:
        return False

    mem_entry.setdefault("context_burrs", {})
    burrs = mem_entry["context_burrs"]

    # Check type-level cap
    type_burrs = burrs.setdefault(burr_type, [])
    if len(type_burrs) >= CONTEXT_BURR_MAX_ITEMS:
        # Evict oldest
        type_burrs.pop(0)

    # Check total cap
    total = sum(len(v) for v in burrs.values())
    if total >= CONTEXT_BURR_MAX_TOTAL:
        return False

    burr_entry = {
        "data": burr_data,
        "added_at": _now_iso(),
    }
    type_burrs.append(burr_entry)
    return True


def get_context_burrs(mem_entry, burr_type=None):
    """Get context burrs from a case entry.

    Args:
        mem_entry: dict
        burr_type: str or None, filter by type (None = all)

    Returns:
        dict: {type: [items]} or empty dict
    """
    burrs = mem_entry.get("context_burrs", {})
    if burr_type:
        return burrs.get(burr_type, [])
    return burrs


def prune_context_burrs(meta_path, max_age_days=90):
    """Remove context burrs older than max_age_days.

    Args:
        meta_path: str
        max_age_days: int

    Returns:
        int: number of burrs pruned
    """
    import math
    now = datetime.now(CST)
    pruned = 0

    meta = load_meta(meta_path)
    for mem in meta.get("memories", []):
        burrs = mem.get("context_burrs", {})
        if not burrs:
            continue
        for btype in list(burrs.keys()):
            items = burrs[btype]
            new_items = []
            for item in items:
                try:
                    added = datetime.fromisoformat(item.get("added_at", ""))
                    age_days = (now - added).total_seconds() / 86400
                    if age_days < max_age_days:
                        new_items.append(item)
                    else:
                        pruned += 1
                except (ValueError, TypeError):
                    new_items.append(item)  # keep if unparseable
            burrs[btype] = new_items
            if not new_items:
                del burrs[btype]

    save_meta(meta_path, meta)
    return pruned


def run_post_stress_reviews(meta, dry_run=False):
    """Execute post-stress reviews for authority-context cases.

    Finds cases with authority_context=true and review_at_pressure_free in the past,
    and marks them for human re-evaluation.

    This should be called by cron periodically.

    Args:
        meta: dict, meta.json content
        dry_run: bool, if True, don't modify meta

    Returns:
        dict: {"due": [...], "reviewed": [...], "stats": {...}}
    """
    from datetime import datetime, timezone

    now = datetime.now(timezone.utc)
    results = {"due": [], "reviewed": [], "stats": {"total_authority": 0, "due_count": 0, "reviewed_count": 0}}

    # Find all authority-context cases
    authority_cases = [
        mem for mem in meta.get("memories", [])
        if mem.get("authority_context") is True
    ]
    results["stats"]["total_authority"] = len(authority_cases)

    for case in authority_cases:
        review_time_str = case.get("review_at_pressure_free")
        status = case.get("post_stress_review_status", "unknown")

        if status == "resolved":
            continue  # Already reviewed and confirmed

        if not review_time_str:
            continue

        try:
            review_time = datetime.fromisoformat(review_time_str.replace("Z", "+00:00"))
        except (ValueError, TypeError):
            continue

        if review_time <= now:
            results["due"].append({
                "id": case.get("id"),
                "content_preview": (case.get("content") or "")[:80],
                "status": status,
                "confidence": case.get("confidence", case.get("decay_score", "?")),
                "review_due_since": str(review_time),
            })
            results["stats"]["due_count"] += 1

            if not dry_run and status == "pending":
                # Mark as "needs_review" — intervention L1 will pick this up
                case["post_stress_review_status"] = "needs_review"
                results["reviewed"].append(case.get("id"))
                results["stats"]["reviewed_count"] += 1

    return results


def cmd_post_stress(meta_path, workspace, dry_run=False):
    """Show and process post-stress reviews."""
    meta = load_meta(meta_path)
    results = run_post_stress_reviews(meta, dry_run)

    print(f"🔍 Post-Stress Review (SimonClaw: authority context re-evaluation)")
    print(f"  Total authority-context cases: {results['stats']['total_authority']}")
    print(f"  Due for review: {results['stats']['due_count']}")
    print(f"  Newly flagged: {results['stats']['reviewed_count']}")
    print()

    if results["due"]:
        for r in results["due"]:
            icon = "🟡" if r["status"] == "needs_review" else "⏳"
            print(f"  {icon} [{r['id']}] conf={r['confidence']} (due: {r['review_due_since'][:10]})")
            print(f"     {r['content_preview']}")
    else:
        print(f"  ✅ No cases due for review")

    if not dry_run and results["reviewed"]:
        save_meta(meta_path, meta)
        print(f"\n✅ Saved: {len(results['reviewed'])} cases flagged for review")

    return results


def build_scene_groups(meta):
    """Build scene groups from active/observing cases.

    Args:
        meta: dict, meta.json content

    Returns:
        dict: {group_id: SceneGroup}
    """
    groups = {}
    cases = [mem for mem in meta.get("memories", [])
             if mem.get("status") in ("active", "observing") and mem.get("case_type") == "case"]
    
    for case in cases:
        tags = case.get("tags", [])
        if not tags:
            group_id = "_default"
            tag_prefix = ""
        else:
            first_tag = tags[0]
            if ":" in first_tag:
                tag_prefix = first_tag.split(":")[0]
                group_id = f"tag:{tag_prefix}"
            else:
                tag_prefix = first_tag
                group_id = f"tag:{tag_prefix}"
        
        if group_id not in groups:
            groups[group_id] = SceneGroup(group_id, tag_prefix)
        groups[group_id].case_ids.append(case.get("id"))
    
    # Update group stats
    for group in groups.values():
        group.update(group.case_ids)
    
    return groups


def get_adaptive_threshold(scene_groups, tag):
    """Get adaptive threshold for a given tag.

    Args:
        scene_groups: dict from build_scene_groups()
        tag: str, case tag

    Returns:
        dict: adaptive thresholds (always returns a valid dict, never None)
    """
    if not tag or not scene_groups:
        return _default_thresholds()

    # Find group for tag
    tag_prefix = tag.split(":")[0] if ":" in tag else tag
    group_id = f"tag:{tag_prefix}"
    group = scene_groups.get(group_id)

    if not group or group.N < 20:
        return _default_thresholds()

    return group.adaptive_threshold


def _default_thresholds():
    """Return default (fixed) thresholds when adaptive is not available."""
    return {
        "absorb": DEFAULT_ABSORB_THRESHOLD,
        "derive": DEFAULT_DERIVE_THRESHOLD,
        "new_type": DEFAULT_NEW_TYPE_THRESHOLD,
        "source": "fixed_default",
        "reason": "N < 20 or group not found",
    }


def jaccard(set_a, set_b):
    """Jaccard similarity (0-1). Protected against empty sets."""
    if not set_a and not set_b:
        return 0.0
    union = len(set_a | set_b)
    if union == 0:
        return 0.0
    return len(set_a & set_b) / union


def tag_jaccard(tags_a, tags_b):
    """Jaccard similarity on tag sets."""
    return jaccard(set(t.lower() for t in tags_a), set(t.lower() for t in tags_b))


def consequence_direction(consequence):
    """Extract consequence direction: positive / negative / neutral."""
    if not consequence:
        return "neutral"
    text = consequence.lower()
    positive_kw = ["成功", "正确", "有效", "解决", "改善", "good", "success", "fix", "resolved"]
    negative_kw = ["失败", "错误", "问题", "冲突", "不一致", "fail", "error", "wrong", "conflict"]
    pos = sum(1 for kw in positive_kw if kw in text)
    neg = sum(1 for kw in negative_kw if kw in text)
    if pos > neg:
        return "positive"
    elif neg > pos:
        return "negative"
    return "neutral"


def add_failure_condition(mem, intent, context=""):
    """Add a failure condition with intent-based dedup."""
    conditions = mem.get("failure_conditions", [])
    if len(conditions) >= MAX_FAILURE_CONDITIONS:
        return  # cap reached

    # Intent clustering: check if similar intent already exists
    intent_tokens = set(_tokenize(intent))
    for cond in conditions:
        cond_tokens = set(_tokenize(cond.get("intent", "")))
        sim = jaccard(intent_tokens, cond_tokens)
        if sim > 0.8:
            # Similar intent exists — increment count
            cond["count"] = cond.get("count", 1) + 1
            cond["last_seen"] = _now_iso()
            return

    # New failure condition
    conditions.append({
        "intent": intent,
        "count": 1,
        "context": context[:200] if context else "",
        "first_seen": _now_iso(),
        "last_seen": _now_iso(),
    })
    mem["failure_conditions"] = conditions
    mem["failure_count"] = len(conditions)


def adjust_confidence(mem, consistent=True):
    """Asymmetric confidence adjustment."""
    current = mem.get("confidence", 0.5)
    if consistent:
        new = min(current + CONFIDENCE_BOOST, 1.0)
    else:
        new = max(current - CONFIDENCE_PENALTY, CONFIDENCE_FLOOR)
    mem["confidence"] = round(new, 3)


# ─── Commands ────────────────────────────────────────────────

def cmd_status(meta_path, workspace):
    """Show case lifecycle overview."""
    meta = load_meta(meta_path)
    memories = meta.get("memories", [])

    status_counts = Counter()
    case_stats = {"total": 0, "high_confidence": 0, "has_failures": 0,
                  "avg_confidence": 0, "avg_triggers": 0, "suspended_pending": 0}

    for mem in memories:
        status = mem.get("status", "active")
        status_counts[status] += 1

        if mem.get("id", "").startswith("case_") or mem.get("case_type") == "case":
            case_stats["total"] += 1
            conf = mem.get("confidence", 0.5)
            triggers = mem.get("trigger_count", 0)
            case_stats["avg_confidence"] += conf
            case_stats["avg_triggers"] += triggers
            if conf >= 0.7:
                case_stats["high_confidence"] += 1
            if mem.get("failure_conditions"):
                case_stats["has_failures"] += 1
            if status == "suspended":
                case_stats["suspended_pending"] += 1

    n_cases = max(case_stats["total"], 1)
    case_stats["avg_confidence"] = round(case_stats["avg_confidence"] / n_cases, 3)
    case_stats["avg_triggers"] = round(case_stats["avg_triggers"] / n_cases, 1)

    print("=" * 50)
    print("Case Self-Growth Status")
    print("=" * 50)
    print(f"\n📋 All memories by status:")
    for s, c in sorted(status_counts.items()):
        icon = {"active": "🟢", "archived": "📦", "deleted": "🗑️",
                "draft": "📝", "observing": "👁️", "suspended": "⏸️"}.get(s, "❓")
        print(f"  {icon} {s}: {c}")

    print(f"\n📊 Case statistics:")
    print(f"  Total cases: {case_stats['total']}")
    print(f"  High confidence (≥0.7): {case_stats['high_confidence']}")
    print(f"  Has failures: {case_stats['has_failures']}")
    print(f"  Avg confidence: {case_stats['avg_confidence']}")
    print(f"  Avg triggers: {case_stats['avg_triggers']}")
    print(f"  Suspended pending: {case_stats['suspended_pending']}")

    # Show observing cases ready for promotion
    observing = [m for m in memories if m.get("status") == "observing"]
    promotable = [m for m in observing if m.get("trigger_count", 0) >= OBSERVING_PROMOTE_N]
    if promotable:
        print(f"\n🚀 Ready for promotion (trigger_count ≥ {OBSERVING_PROMOTE_N}):")
        for m in promotable:
            print(f"  [{m['id']}] triggers={m.get('trigger_count', 0)} conf={m.get('confidence', 0.5)}")
            print(f"    {m.get('content', '')[:80]}")

    # Show suspended cases
    suspended = [m for m in memories if m.get("status") == "suspended"]
    if suspended:
        print(f"\n⏸️ Suspended cases:")
        for m in suspended:
            pending = m.get("suspended_pending_count", 0)
            print(f"  [{m['id']}] pending={pending}/{SUSPEND_CONFIRM_N}")
            print(f"    {m.get('content', '')[:80]}")

    # Show conflicts
    conflicts = meta.get("conflicts", [])
    if conflicts:
        print(f"\n⚡ Conflicts: {len(conflicts)}")
        for c in conflicts[:5]:
            print(f"  [{c.get('id', '?')}] type={c.get('type', '?')} status={c.get('status', '?')}")
            print(f"    case_a={c.get('case_a_id')} case_b={c.get('case_b_id')}")

    return case_stats


def record_trigger(meta_path, case_id):
    """Increment trigger_count for a case and update last_accessed.

    This is the unified API for recording that a case was triggered/matched.
    Should be called by memory_guardian or any external trigger source.

    Args:
        meta_path: str, path to meta.json
        case_id: str, the case ID to record a trigger for

    Returns:
        dict: {"updated": bool, "trigger_count": int, "case_id": str}
    """
    meta = load_meta(meta_path)
    now = _now_iso()

    for mem in meta.get("memories", []):
        if mem.get("id") == case_id:
            mem["trigger_count"] = mem.get("trigger_count", 0) + 1
            mem["last_accessed"] = now
            mem["access_count"] = mem.get("access_count", 0) + 1
            save_meta(meta_path, meta)
            return {
                "updated": True,
                "trigger_count": mem["trigger_count"],
                "case_id": case_id,
            }

    return {"updated": False, "trigger_count": 0, "case_id": case_id}


def cmd_record_trigger(meta_path, workspace, case_id):
    """CLI: Record a trigger for a case."""
    if not case_id:
        print("Usage: memory_case_grow.py record-trigger --id <case_id>")
        return

    result = record_trigger(meta_path, case_id)
    if result["updated"]:
        print(f"✅ Trigger recorded for {case_id}")
        print(f"  trigger_count: {result['trigger_count']}")
    else:
        print(f"❌ Case not found: {case_id}")


def cmd_grow(meta_path, workspace, dry_run):
    """Run growth cycle: promote observing, check suspended, adjust confidence.

    v0.4.1 additions:
    - Pool evaluation: check observation pool for promotion/archive
    - Feedback-aware promotion: positive feedback required
    - TTL-based expiry check
    """
    meta = load_meta(meta_path)
    now = _now_iso()
    now_dt = datetime.now(CST)
    promoted = 0
    suspended_confirmed = 0
    confidence_adjusted = 0
    pool_graduated = 0
    pool_demoted = 0

    for mem in meta.get("memories", []):
        status = mem.get("status", "active")
        case_pool = mem.get("case_pool", "matching")  # v0.4.1

        # 0. v0.4.1: Pool evaluation (observation pool)
        if case_pool == "observation" and status == "observing":
            obs_start = mem.get("obs_start_time")
            triggers = mem.get("trigger_count", 0)
            positive_feedback = mem.get("positive_feedback_count", 0)

            # Exit conditions: max(hours, triggers)
            should_evaluate = False
            exit_reason = ""

            if obs_start:
                try:
                    obs_dt = datetime.fromisoformat(obs_start)
                    hours = (now_dt - obs_dt).total_seconds() / 3600
                    if hours >= POOL_OBSERVATION_HOURS:
                        should_evaluate = True
                        exit_reason = f"timeout ({hours:.0f}h ≥ {POOL_OBSERVATION_HOURS}h)"
                except (ValueError, TypeError):
                    pass

            if triggers >= POOL_OBSERVATION_TRIGGERS:
                should_evaluate = True
                exit_reason = f"trigger count ({triggers} ≥ {POOL_OBSERVATION_TRIGGERS})"

            if should_evaluate:
                # Evaluate: promote if criteria met, else archive
                risk_tags = len([t for t in mem.get("tags", []) if t in
                    ("delete", "overwrite", "external_send", "permission_expand")])
                has_feedback = positive_feedback >= POOL_POSITIVE_FEEDBACK_REQUIRED

                if risk_tags >= POOL_RISK_TAG_REQUIRED and has_feedback and triggers >= OBSERVING_PROMOTE_N:
                    # Promote to matching pool (active)
                    if not dry_run:
                        mem["case_pool"] = "matching"
                        mem["status"] = "active"
                        mem["promoted_at"] = now
                        mem["pool_graduated_at"] = now
                        mem["confidence"] = min(mem.get("confidence", 0.5) + 0.1, 1.0)
                    pool_graduated += 1
                    promoted += 1
                else:
                    # v0.4.2 prep (neuro): demote to draft instead of archive
                    # if evaluation triggered but criteria not met
                    if not dry_run:
                        mem["status"] = "draft"
                        mem["pool_exit_reason"] = exit_reason
                        mem["pool_demoted_at"] = now
                    pool_demoted += 1

        # 1. Promote observing → active (matching pool only)
        if status == "observing" and case_pool != "observation":
            triggers = mem.get("trigger_count", 0)
            positive_feedback = mem.get("positive_feedback_count", 0)
            # v0.4.1: require positive feedback + risk tags for promotion (same as cmd_pool)
            risk_tags = len([t for t in mem.get("tags", []) if t in
                ("delete", "overwrite", "external_send", "permission_expand")])
            if (triggers >= OBSERVING_PROMOTE_N and
                positive_feedback >= POOL_POSITIVE_FEEDBACK_REQUIRED and
                risk_tags >= POOL_RISK_TAG_REQUIRED):
                if not dry_run:
                    mem["status"] = "active"
                    mem["promoted_at"] = now
                    mem["confidence"] = min(mem.get("confidence", 0.5) + 0.1, 1.0)
                promoted += 1

        # 2. Check suspended → confirm or expire
        elif status == "suspended":
            pending = mem.get("suspended_pending_count", 0)
            if pending >= SUSPEND_CONFIRM_N:
                if not dry_run:
                    mem["status"] = "observing"
                    mem["observing_since"] = now
                    mem["suspended_pending_count"] = 0
                suspended_confirmed += 1

        # 3. Adjust confidence based on trigger patterns
        if status in ("active", "observing"):
            triggers = mem.get("trigger_count", 0)
            failures = len(mem.get("failure_conditions", []))
            if triggers > 0 and failures > 0:
                failure_ratio = failures / triggers
                if failure_ratio > 0.5:
                    if not dry_run:
                        adjust_confidence(mem, consistent=False)
                    confidence_adjusted += 1

    if not dry_run:
        save_meta(meta_path, meta)

    print(f"Growth cycle complete:")
    print(f"  🚀 Promoted observing→active: {promoted}")
    print(f"  ✅ Confirmed suspended→observing: {suspended_confirmed}")
    print(f"  📉 Confidence adjusted (high failure ratio): {confidence_adjusted}")
    print(f"  🏊 Pool graduated → matching: {pool_graduated}")
    print(f"  📝 Pool demoted → draft: {pool_demoted}")
    if dry_run:
        print("  (dry-run: no changes written)")

    return {"promoted": promoted, "confirmed": suspended_confirmed,
            "adjusted": confidence_adjusted, "pool_graduated": pool_graduated,
            "pool_demoted": pool_demoted}


def cmd_pool(meta_path, workspace):
    """v0.4.1: Show temporary observation pool status."""
    meta = load_meta(meta_path)
    now = datetime.now(CST)

    observation = [m for m in meta.get("memories", [])
                   if m.get("case_pool") == "observation" and m.get("status") == "observing"]

    print("=" * 50)
    print(f"🏊 Temporary Observation Pool ({len(observation)} entries)")
    print(f"   Max: {POOL_OBSERVATION_HOURS}h or {POOL_OBSERVATION_TRIGGERS} triggers")
    print("=" * 50)

    for mem in observation:
        obs_start = mem.get("obs_start_time", mem.get("created_at"))
        triggers = mem.get("trigger_count", 0)
        feedback = mem.get("positive_feedback_count", 0)
        confidence = mem.get("confidence", 0.5)
        risk_tags = [t for t in mem.get("tags", []) if t in
                     ("delete", "overwrite", "external_send", "permission_expand")]

        hours = 0
        if obs_start:
            try:
                obs_dt = datetime.fromisoformat(obs_start)
                hours = (now - obs_dt).total_seconds() / 3600
            except (ValueError, TypeError):
                pass

        progress_h = min(hours / POOL_OBSERVATION_HOURS * 100, 100)
        progress_t = min(triggers / POOL_OBSERVATION_TRIGGERS * 100, 100)
        progress = max(progress_h, progress_t)

        # Status indicators
        can_promote = (len(risk_tags) >= POOL_RISK_TAG_REQUIRED and
                       feedback >= POOL_POSITIVE_FEEDBACK_REQUIRED and
                       triggers >= OBSERVING_PROMOTE_N)

        status_icon = "🚀" if can_promote else "⏳"
        if progress >= 100:
            status_icon = "⚠️"  # ready for evaluation

        print(f"\n  {status_icon} [{mem['id']}] conf={confidence:.2f} triggers={triggers} feedback={feedback}")
        print(f"     Time: {hours:.0f}h / {POOL_OBSERVATION_HOURS}h ({progress_h:.0f}%)")
        print(f"     Triggers: {triggers} / {POOL_OBSERVATION_TRIGGERS} ({progress_t:.0f}%)")
        print(f"     Risk tags: {risk_tags or '(none)'}")
        print(f"     Content: {mem.get('content', '')[:80]}")
        if can_promote:
            print(f"     ✅ Meets promotion criteria!")
        elif progress >= 100:
            print(f"     ⚠️ Ready for evaluation — will demote to draft if criteria not met")

    if not observation:
        print("\n  (empty — no entries in observation pool)")

    return {"count": len(observation)}


def cmd_merge(meta_path, workspace, dry_run):
    """Check for merge candidates (triple condition)."""
    meta = load_meta(meta_path)
    now = _now_iso()
    active_cases = [m for m in meta.get("memories", [])
                    if m.get("status") in ("active", "observing") and
                    m.get("action_conclusion")]

    if len(active_cases) < 2:
        print("Not enough active cases with action_conclusion for merge check.")
        return {"merges": []}

    merge_candidates = []
    for i in range(len(active_cases)):
        for j in range(i + 1, len(active_cases)):
            a = active_cases[i]
            b = active_cases[j]

            # Condition 1: behavior consistency (trigger_count as proxy)
            a_triggers = a.get("trigger_count", 0)
            b_triggers = b.get("trigger_count", 0)
            if a_triggers < MERGE_BEHAVIOR_N or b_triggers < MERGE_BEHAVIOR_N:
                continue

            # Condition 2: tag Jaccard > 0.8
            tags_a = a.get("tags", [])
            tags_b = b.get("tags", [])
            tag_sim = tag_jaccard(tags_a, tags_b)
            if tag_sim < MERGE_JACCARD_THRESHOLD:
                continue

            # Condition 3: consequence direction consistency
            dir_a = consequence_direction(a.get("consequence", ""))
            dir_b = consequence_direction(b.get("consequence", ""))
            if dir_a != dir_b or dir_a == "neutral":
                continue

            # All three conditions met — merge candidate
            similarity = tag_sim  # primary signal
            merge_candidates.append({
                "case_a": a.get("id"),
                "case_b": b.get("id"),
                "content_a": a.get("content", "")[:60],
                "content_b": b.get("content", "")[:60],
                "tag_sim": round(tag_sim, 3),
                "direction": dir_a,
                "score": round(similarity, 3),
            })

    merge_candidates.sort(key=lambda x: x["score"], reverse=True)

    print(f"Merge analysis: {len(active_cases)} cases checked, {len(merge_candidates)} candidates")
    for c in merge_candidates[:10]:
        print(f"  [{c['case_a']}] ↔ [{c['case_b']}] sim={c['tag_sim']:.3f} dir={c['direction']}")
        print(f"    A: {c['content_a']}")
        print(f"    B: {c['content_b']}")

    # Apply merges in non-dry-run
    if not dry_run and merge_candidates:
        applied = 0
        for c in merge_candidates:
            # Merge B into A
            keeper_id = c["case_a"]
            absorbed_id = c["case_b"]
            keeper = None
            absorbed = None
            for mem in meta["memories"]:
                if mem.get("id") == keeper_id:
                    keeper = mem
                elif mem.get("id") == absorbed_id:
                    absorbed = mem
            if not keeper or not absorbed:
                continue
            # Bug fix: skip if either case was archived by a prior merge in this loop
            if keeper.get("status") == "archived" or absorbed.get("status") == "archived":
                continue

            # Merge tags
            keeper["tags"] = list(set(keeper.get("tags", []) + absorbed.get("tags", [])))
            # Set probation confidence
            keeper["confidence"] = CONFIDENCE_MERGE_INIT

            # v0.4.1: Version the keeper before merge modification
            version_group = keeper.get("version_group", keeper.get("id"))
            old_version = keeper.get("version", 1)

            # Create a snapshot of the pre-merge keeper as a deprecated version
            snapshot_id = f"case_{uuid.uuid4().hex[:8]}"
            snapshot = dict(keeper)
            snapshot["id"] = snapshot_id
            snapshot["version"] = old_version
            snapshot["version_group"] = version_group
            snapshot["deprecated"] = True
            snapshot["deprecated_at"] = now
            snapshot["deprecated_reason"] = f"pre-merge snapshot before absorbing {absorbed_id}"
            snapshot["status"] = "archived"
            snapshot["failure_signals"] = copy.deepcopy(keeper.get("failure_signals", {}))
            meta["memories"].append(snapshot)

            # Update keeper version
            keeper["version"] = old_version + 1
            keeper["prev_version"] = snapshot_id
            keeper["version_group"] = version_group

            # Record merge
            keeper.setdefault("merge_history", []).append({
                "absorbed": absorbed_id,
                "at": now,
                "reason": f"merge: tag_sim={c['tag_sim']:.3f} dir={c['direction']}",
            })
            keeper.setdefault("version_log", []).append({
                "action": "merge_promote",
                "from_version": old_version,
                "to_version": old_version + 1,
                "timestamp": now,
                "reason": f"merged {absorbed_id}",
            })
            # Archive absorbed
            absorbed["status"] = "archived"
            absorbed["merged_into"] = keeper_id
            absorbed["archived_at"] = now
            # Update conflict refs
            keeper.setdefault("conflict_refs", [])
            keeper["conflict_refs"].append(absorbed_id)
            applied += 1

        if applied:
            save_meta(meta_path, meta)
            print(f"\n✅ Applied: {applied} merges executed")

    return {"merges": merge_candidates}


def cmd_conflict(meta_path, workspace, dry_run):
    """Detect key conflicts between cases (v0.4: string comparison)."""
    meta = load_meta(meta_path)
    now = _now_iso()
    active_cases = [m for m in meta.get("memories", [])
                    if m.get("status") in ("active", "observing") and
                    m.get("judgment")]

    conflicts = []
    seen_pairs = set()

    for i in range(len(active_cases)):
        for j in range(i + 1, len(active_cases)):
            a = active_cases[i]
            b = active_cases[j]

            # Key conflict: check if judgment contradicts
            j_a = a.get("judgment", "").lower()
            j_b = b.get("judgment", "").lower()

            # Check for negation patterns
            negation_pairs = [
                ("拒绝", "接受"), ("接受", "拒绝"),
                ("不允许", "允许"), ("允许", "不允许"),
                ("不要", "要"), ("禁止", "可以"),
                # English negation pairs
                ("reject", "accept"), ("accept", "reject"),
                ("refuse", "allow"), ("allow", "refuse"),
                ("don't", "do"), ("do", "don't"),
                ("never", "always"), ("always", "never"),
                ("should not", "should"), ("should", "should not"),
                ("must not", "must"), ("must", "must not"),
                ("no", "yes"), ("yes", "no"),
            ]

            has_conflict = False
            for neg, pos in negation_pairs:
                if (neg in j_a and pos in j_b) or (pos in j_a and neg in j_b):
                    # Verify overlap in situation (similar context)
                    s_a = a.get("situation", "").lower()
                    s_b = b.get("situation", "").lower()
                    tokens_a = set(_tokenize(s_a))
                    tokens_b = set(_tokenize(s_b))
                    if tokens_a and tokens_b:
                        overlap = len(tokens_a & tokens_b) / max(len(tokens_a | tokens_b), 1)
                        if overlap > 0.3:  # similar context
                            has_conflict = True
                            break

            if has_conflict:
                pair_key = tuple(sorted([a.get("id"), b.get("id")]))
                if pair_key not in seen_pairs:
                    seen_pairs.add(pair_key)
                    conflicts.append({
                        "case_a_id": a.get("id"),
                        "case_b_id": b.get("id"),
                        "judgment_a": a.get("judgment", "")[:80],
                        "judgment_b": b.get("judgment", "")[:80],
                        "type": "key_conflict",
                        "status": "detected",
                        "detected_at": now,
                    })

    print(f"Conflict detection: {len(active_cases)} cases checked, {len(conflicts)} conflicts")
    for c in conflicts:
        print(f"  ⚡ [{c['case_a_id']}] ↔ [{c['case_b_id']}]")
        print(f"    A: {c['judgment_a']}")
        print(f"    B: {c['judgment_b']}")

    # Store conflicts
    if not dry_run and conflicts:
        meta.setdefault("conflicts", [])
        existing_ids = {f"{c['case_a_id']}:{c['case_b_id']}" for c in meta["conflicts"]}
        new_count = 0
        for c in conflicts:
            key = f"{c['case_a_id']}:{c['case_b_id']}"
            if key not in existing_ids:
                c["id"] = f"conflict_{os.urandom(4).hex()}"
                meta["conflicts"].append(c)
                new_count += 1
        if new_count:
            save_meta(meta_path, meta)
            print(f"\n✅ Stored: {new_count} new conflicts")

    return {"conflicts": conflicts}


def cmd_scenes(meta_path, workspace):
    """Show all scene groups and their adaptive thresholds."""
    meta = load_meta(meta_path)
    groups = build_scene_groups(meta)

    print(f"📊 Scene Groups (PID Adaptive Cold Start)")
    print(f"  Total groups: {len(groups)}")
    total_cases = sum(g.N for g in groups.values())
    print(f"  Total cases: {total_cases}")
    print()

    for gid in sorted(groups.keys()):
        g = groups[gid]
        icon = "🟢" if g.N >= 20 else "⚪"
        print(f"  {icon} {gid}: N={g.N}")
        if g.adaptive_threshold:
            t = g.adaptive_threshold
            print(f"     absorb={t['absorb']:.2f}  derive={t['derive']:.2f}  new_type={t['new_type']:.2f}")
        else:
            print(f"     (using defaults: absorb=0.80  derive=0.50  new_type=0.30)")
        print(f"     Cases: {g.case_ids[:5]}{'...' if len(g.case_ids) > 5 else ''}")
        print()

    # Summary
    adaptive_count = sum(1 for g in groups.values() if g.adaptive_threshold is not None)
    if adaptive_count == 0:
        print(f"  💡 All groups have N < 20, using fixed thresholds.")
        print(f"     Adaptive thresholds activate when N ≥ 20.")


if __name__ == "__main__":
    p = argparse.ArgumentParser(description="memory-guardian case self-growth engine (v0.4.1)")
    p.add_argument("command", choices=["status", "grow", "merge", "conflict", "pool", "scenes", "post-stress", "record-trigger", "rescan-authority"],
                   help="Growth command")
    p.add_argument("--workspace", default=None, help="Workspace root path")
    p.add_argument("--meta", default=None, help="Path to meta.json")
    p.add_argument("--dry-run", action="store_true", help="Show results without applying")
    p.add_argument("--id", default=None, help="Case ID (for record-trigger command)")
    args = p.parse_args()

    workspace = args.workspace or os.environ.get(
        "OPENCLAW_WORKSPACE", os.path.expanduser("~/workspace/agent/workspace")
    )
    meta_path = args.meta or os.path.join(workspace, "memory", "meta.json")
    telemetry_meta = load_meta(meta_path) if os.path.exists(meta_path) else {"memories": []}
    telemetry_input_count = sum(
        1
        for mem in telemetry_meta.get("memories", [])
        if mem.get("id", "").startswith("case_") or mem.get("case_type") == "case"
    )

    if args.command == "status":
        cmd_status(meta_path, workspace)
    elif args.command == "grow":
        cmd_grow(meta_path, workspace, args.dry_run)
    elif args.command == "merge":
        cmd_merge(meta_path, workspace, args.dry_run)
    elif args.command == "conflict":
        cmd_conflict(meta_path, workspace, args.dry_run)
    elif args.command == "pool":
        cmd_pool(meta_path, workspace)
    elif args.command == "scenes":
        cmd_scenes(meta_path, workspace)
    elif args.command == "post-stress":
        cmd_post_stress(meta_path, workspace, args.dry_run)
    elif args.command == "record-trigger":
        cmd_record_trigger(meta_path, workspace, args.id)
    elif args.command == "rescan-authority":
        result = rescan_authority_context(meta_path)
        print(f"🔍 Authority Context Rescan")
        print(f"  Newly flagged: {result['newly_flagged']}")
        print(f"  Total flagged: {result['total_flagged']}")

    record_module_run(
        workspace,
        "case_grow",
        input_count=telemetry_input_count,
        output_count=telemetry_input_count,
    )

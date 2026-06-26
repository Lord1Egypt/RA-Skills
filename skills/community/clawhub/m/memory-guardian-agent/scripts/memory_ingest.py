#!/usr/bin/env python3
"""memory-guardian: Memory ingest — add/update a memory/case entry in meta.json.

v0.4 changes:
  - Supports 11-field case template (situation/judgment/consequence/action_conclusion)
  - Draft state machine: new ingest → draft → observing → active
  - Reversibility four-level (0-3)
  - Cost signal four-dimension auto-evaluation
  - L0/L1 importance threshold
  - Security layer pre-check
  - confidence/trigger_count/failure_conditions support

v0.4.5 changes:
  - Classification: rule-based tag assignment + confidence scoring
  - Three-step write: classify → confidence gate → write to category dir
  - memory_id + file_path + classification fields on every new memory
  - tags_locked=True on ingest (prevents reclassification)
  - _inbox routing for low-confidence memories

Usage:
  python3 memory_ingest.py --content "..." [--importance <0-1>] [--tags tag1,tag2]
  python3 memory_ingest.py --situation "..." --judgment "..." --consequence "..."  # case mode
  echo "content from stdin" | python3 memory_ingest.py --stdin
"""
import argparse
import importlib.util
import os
import re
import sys
import uuid
from collections.abc import Mapping
from types import ModuleType

from mg_events.telemetry import record_module_run
from mg_utils import (
    COOLING_THRESHOLD,
    _now_iso,
    compute_provenance_confidence as _compute_provenance_confidence_from_config,
    save_meta as _save_meta,
    tokenize as _tokenize,
    generate_memory_id,
    derive_file_path,
    resolve_primary_tag,
    classify_confidence_level,
)


# ─── v0.4 Constants ──────────────────────────────────────────
L0_IMPORTANCE_THRESHOLD = 0.3  # L0: all memories; L1: importance >= this
DEFAULT_REVERSIBILITY = 1       # 1 = low-cost reversible
DEFAULT_CONFIDENCE = 0.5


def _load_module_from_path(module_name, module_path) -> ModuleType | None:
    """Load a sibling module defensively for optional integrations."""
    spec = importlib.util.spec_from_file_location(module_name, module_path)
    if spec is None or spec.loader is None:
        return None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def _format_quality_bypass_reason(layer_results) -> str | None:
    """Collapse failed layer reasons into one human-readable string."""
    if not isinstance(layer_results, Mapping):
        return None

    reasons = []
    for layer, result in layer_results.items():
        if not isinstance(layer, str) or not isinstance(result, Mapping):
            continue
        if result.get("passed") is not False:
            continue
        reason = result.get("reason")
        if isinstance(reason, str) and reason:
            reasons.append(f"{layer}:{reason}")

    return "; ".join(reasons) or None


def save_meta(*args, **kwargs):
    """Backward-compatible save helper exported for legacy callers."""
    return _save_meta(*args, **kwargs)


def quick_dedup_check(content, memories, threshold=0.85, inverted_index=None):
    """Token-overlap dedup check with bigram support for CJK.

    If an inverted_index (from mg_utils.build_inverted_index) is provided,
    only candidates sharing tokens with the input are examined, reducing
    O(N×M) to O(K) where K is the candidate set size.
    """
    words_a = set(_tokenize(content))
    if not words_a:
        return None

    # Build lookup set of candidate memory IDs via inverted index
    candidate_ids = None
    if inverted_index is not None:
        candidate_ids = set()
        for token in words_a:
            ids = inverted_index.get(token)
            if ids:
                candidate_ids.update(ids)
        if not candidate_ids:
            return None

    # Build a quick ID→memory map for lookup
    if candidate_ids is not None:
        mem_map = {}
        for mem in memories:
            mid = mem.get("memory_id", mem.get("id", ""))
            if mid in candidate_ids:
                mem_map[mid] = mem
    else:
        mem_map = {mem.get("memory_id", mem.get("id", "")): mem for mem in memories}

    for mem in mem_map.values():
        if mem.get("status", "active") not in ("active", "observing"):
            continue
        words_b = set(_tokenize(mem.get("content", "")))
        if not words_b:
            continue
        overlap = len(words_a & words_b)
        union = len(words_a | words_b)
        if union > 0 and overlap / union > threshold:
            return mem
    return None


def extract_entities(content):
    """Extract basic entities using regex patterns (7 types)."""
    entities = []
    seen = set()

    for m in re.finditer(r"(ou_[a-f0-9]+)", content):
        if m.group(1) not in seen:
            entities.append({"type": "feishu_open_id", "value": m.group(1)})
            seen.add(m.group(1))
    for m in re.finditer(r"(oc_[a-f0-9]+)", content):
        if m.group(1) not in seen:
            entities.append({"type": "feishu_chat_id", "value": m.group(1)})
            seen.add(m.group(1))
    for m in re.finditer(r"(mem_[a-f0-9]+|case_[a-f0-9]+)", content):
        if m.group(1) not in seen:
            entities.append({"type": "memory_id", "value": m.group(1)})
            seen.add(m.group(1))
    for m in re.finditer(r"(?<![a-f0-9])([a-f0-9]{8})(?![a-f0-9])", content):
        val = m.group(1)
        if val not in seen:
            entities.append({"type": "hex_id", "value": val})
            seen.add(val)

    CODE_KEYWORDS = {
        "parent_id", "full_uuid", "target_type", "target_id",
        "recipient_username", "thread_id", "retry_after_seconds",
        "reply_to_current", "access_count", "memory_search",
        "decay_score", "network_factor", "gitcode_token",
        "memory_guardian", "memory_diff", "skill_id",
        "thread_ids", "memory_id", "post_id", "chat_id",
        "message_id", "file_key", "image_key", "open_id",
        "user_id", "union_id", "app_token", "table_id",
        "field_name", "record_id", "view_id", "event_id",
        "calendar_id", "folder_token", "page_token",
        "action_conclusion", "cooling_threshold", "suspended_pending_count",
        "failure_count", "trigger_count", "confidence", "reversibility",
    }
    for m in re.finditer(r"(?<![a-zA-Z_])([a-z][a-z0-9]*(?:_[a-z0-9]+){1,4})(?![a-zA-Z_])", content):
        val = m.group(1)
        if val.startswith("sk_") or val.startswith("sk_inst_"):
            continue
        if val not in seen and len(val) >= 5 and val not in CODE_KEYWORDS:
            entities.append({"type": "username", "value": val})
            seen.add(val)

    for m in re.finditer(r"(v\d+\.\d+(?:\.\d+)?(?:-[a-z]+)?)", content):
        if m.group(1) not in seen:
            entities.append({"type": "version", "value": m.group(1)})
            seen.add(m.group(1))

    for m in re.finditer(r"(https?://[^\s\])>\"]+)", content):
        url = m.group(1)
        if len(url) > 120:
            url = url[:120] + "..."
        if url not in seen:
            entities.append({"type": "url", "value": url})
            seen.add(url)

    return entities


def check_security(content, workspace):
    """Run security layer check. Returns violations list."""
    if not workspace:
        return []

    try:
        security_path = os.path.join(os.path.dirname(__file__), "security_layer.py")
        if not os.path.exists(security_path):
            return []

        security_mod = _load_module_from_path("security_layer", security_path)
        if security_mod is None:
            return []

        meta_path = os.path.join(workspace, "memory", "meta.json")
        meta = security_mod.load_meta(meta_path)
        rules = meta.get("security_rules", []) if isinstance(meta, Mapping) else []
        if not rules:
            return []
        return security_mod.check_content(content, rules)
    except Exception as e:
        import logging
        logging.warning("security check failed for content: %s", e)
        return []


def evaluate_cost_signals(content, situation=None, judgment=None):
    """Auto-evaluate four-dimension cost signals.

    Returns {write_cost, verify_cost, human_cost, transfer_cost} (0-3 each).
    L1 threshold: only records with transfer_cost>0 OR human_cost>0 get cost signal tracking.
    """
    text = " ".join(filter(None, [content, situation, judgment])).lower()
    costs = {"write_cost": 0, "verify_cost": 0, "human_cost": 0, "transfer_cost": 0}

    # write_cost: how much effort to write this memory
    if len(text) > 500:
        costs["write_cost"] = 2
    elif len(text) > 200:
        costs["write_cost"] = 1

    # verify_cost: how hard to verify correctness
    verify_keywords = ["测试", "验证", "确认", "check", "verify", "test", "debug", "排查"]
    costs["verify_cost"] = min(sum(1 for kw in verify_keywords if kw in text), 3)

    # human_cost: involves human interaction/impact
    human_keywords = ["用户", "通知", "回复", "human", "user", "reply", "dm", "群聊", "私聊"]
    costs["human_cost"] = min(sum(1 for kw in human_keywords if kw in text), 3)

    # transfer_cost: could be shared/transferred to other agents
    transfer_keywords = ["社区", "分享", "发布", "帖", "share", "publish", "post", "community"]
    costs["transfer_cost"] = min(sum(1 for kw in transfer_keywords if kw in text), 3)

    return costs


def build_importance_explain(importance, cost_factors):
    """Generate human-readable importance explanation."""
    if isinstance(importance, str) and importance == "auto":
        return None
    importance = float(importance)
    parts = []
    main_factor = "base"

    if cost_factors.get("human_cost", 0) > 0:
        parts.append("human")
    if cost_factors.get("transfer_cost", 0) > 0:
        parts.append("transfer")
    if cost_factors.get("verify_cost", 0) > 0:
        parts.append("verify")
    if cost_factors.get("write_cost", 0) > 0:
        parts.append("write")

    if parts:
        main_factor = "/".join(parts[:2])

    return f"{importance:.2f} main:{main_factor}"


def _determine_provenance(content, situation, is_case, source=None):
    """Determine provenance level and source.

    Args:
        content: str, memory content
        situation: str or None, case situation field
        is_case: bool, whether this is a case entry
        source: str or None, "human"/"system"/"external"

    Returns:
        tuple: (level_str, source_str)
    """
    content_text = content or ""
    content_lower = content_text.lower()

    if source == "human":
        return "L1", "human_direct"
    if source == "external":
        return "L3", "external"
    if source == "system":
        return "L2", "system_induction"

    # L1: Human direct input
    if (
        "记住" in content_lower
        or "note" in content_lower
        or "todo" in content_lower
        or "TODO" in content_text
        or "NOTE" in content_text
    ):
        return "L1", "human_direct"

    # L3: External reference
    if "外部引用" in content_lower or "external reference" in content_lower:
        return "L3", "external"

    # L2: Default (experience induction)
    return "L2", "system_induction"


def _compute_provenance_confidence(provenance_level, verification_count=0, decay_config=None):
    """v0.4.2 P2: Compute confidence using multiplicative model (SimonClaw).

    confidence = base × auth_mult × verification_mult
    where verification_mult = 1.0 + min(0.3, count × 0.1)

    This replaces the fixed DEFAULT_CONFIDENCE = 0.5.
    """
    return _compute_provenance_confidence_from_config(
        provenance_level,
        verification_count=verification_count,
        decay_config=decay_config,
    )


def _assign_memory_type(provenance_level, case_origin, tags):
    """v0.4.2 P2: Assign memory_type based on provenance and case origin (ovea).

    - static: Human direct (L1) + core/bootstrap tags
    - derive: System induction (L2) + standard cases
    - absorb: External references (L3) + any external source + absorb case_origin
    """
    tags_set = set(t.lower() for t in (tags or []))

    # L3 (external) → absorb
    if provenance_level == "L3":
        return "absorb"

    # Check case_origin for absorb hints
    if case_origin:
        origin_lower = case_origin.lower()
        if any(kw in origin_lower for kw in ["外部", "external", "社区", "community", "论坛", "forum"]):
            return "absorb"

    # L1 + bootstrap/core tags → static
    if provenance_level == "L1":
        if "bootstrap" in tags_set or "core" in tags_set or "pinned" in tags_set:
            return "static"
        return "derive"  # Human input but not core → derive

    # L2 (system induction) → derive by default
    return "derive"


def _security_precheck(content, workspace):
    """Run security layer check. Returns violations or None.

    Returns None if no blocking violations, list of violations if blocked.
    """
    if not workspace:
        return None
    violations = check_security(content, workspace)
    critical = [v for v in violations if v.get("action") == "BLOCK"]
    if critical:
        print("[BLOCKED] Security violation detected:")
        for v in critical:
            print(f"  🚫 [{v['rule_id']}] {v['description']}")
        return critical
    return None


# ─── v0.4.5: Classification ──────────────────────────────────

# Classification rules: (tag, [keywords], weight)
# Higher weight = more specific match. First match at highest weight wins.
_CLASSIFICATION_RULES = [
    # project
    ("project", ["项目", "project", "开发", "编码", "版本", "release", "v0.", "v1.", "里程碑", "milestone", "迭代", "sprint"], 3),
    ("project", ["memory-guardian", "skill", "skill-creator", "skill设计"], 2),
    # tech
    ("tech", ["架构", "设计模式", "算法", "api", "schema", "数据结构", "缓存", "索引", "路由", "框架", "framework", "design", "architecture"], 3),
    ("tech", ["测试", "test", "debug", "bug", "性能优化", "performance", "重构", "refactor"], 2),
    # social
    ("social", ["社区", "帖子", "评论", "回复", "推广", "讨论", "论坛", "instreet", "虾评", "小组帖", "广场帖"], 3),
    ("social", ["neuro", "SimonClaw", "jarvis", "byteclaw", "smartlobster", "小虾米", "guoxiaoxin", "skilly_wang"], 2),
    # personal
    ("personal", ["偏好", "习惯", "日常", "个人", "风清", "owner", "偏好设置", "作息"], 3),
]

# Confidence modifiers
_CONFIDENCE_BOOST_EXPLICIT_TAG = 0.2     # User explicitly provided matching tag
_CONFIDENCE_BOOST_STRONG_KEYWORD = 0.15  # 3+ keyword hits
_CONFIDENCE_BOOST_MEDIUM_KEYWORD = 0.08  # 1-2 keyword hits
_CONFIDENCE_BASE_RULE = 0.7              # Base confidence for rule match
_CONFIDENCE_BASE_FALLBACK = 0.3          # Base confidence for content-only match
_CONFIDENCE_BOOST_CASE_FIELDS = 0.1      # Case with situation+judgment


def _classify(content, tags_hint=None, is_case=False, situation=None, judgment=None):
    """Classify a memory into tags with confidence score.

    Uses rule-based keyword matching with tag hints.

    Args:
        content: Memory content string.
        tags_hint: Optional user-provided tags list.
        is_case: Whether this is a case entry.
        situation: Case situation field (adds context).
        judgment: Case judgment field (adds context).

    Returns:
        dict: {
            "tags": [str],
            "confidence": float,
            "classification_context": str,
            "primary_tag": str,
        }
    """
    content_lower = (content or "").lower()
    # Include case fields in matching text
    match_text = content_lower
    if situation:
        match_text += " " + situation.lower()
    if judgment:
        match_text += " " + judgment.lower()

    tags_hint = tags_hint or []
    hint_set = set(t.lower() for t in tags_hint)

    # Phase 1: Check hint tags against known directories
    for tag in tags_hint:
        mapped = resolve_primary_tag([tag])
        if mapped != "misc":
            confidence = _CONFIDENCE_BASE_RULE + _CONFIDENCE_BOOST_EXPLICIT_TAG
            if is_case and situation and judgment:
                confidence += _CONFIDENCE_BOOST_CASE_FIELDS
            return {
                "tags": tags_hint,
                "confidence": min(confidence, 1.0),
                "classification_context": f"explicit tag '{tag}' mapped to {mapped}",
                "primary_tag": mapped,
            }

    # Phase 2: Rule-based keyword matching
    best_match = None
    best_score = 0
    best_hits = 0

    for tag, keywords, weight in _CLASSIFICATION_RULES:
        hits = sum(1 for kw in keywords if kw.lower() in match_text)
        if hits > 0:
            score = hits * weight
            if score > best_score:
                best_score = score
                best_match = tag
                best_hits = hits

    if best_match:
        confidence = _CONFIDENCE_BASE_RULE
        if best_hits >= 3:
            confidence += _CONFIDENCE_BOOST_STRONG_KEYWORD
        elif best_hits >= 1:
            confidence += _CONFIDENCE_BOOST_MEDIUM_KEYWORD
        if is_case and situation and judgment:
            confidence += _CONFIDENCE_BOOST_CASE_FIELDS
        confidence = min(confidence, 1.0)

        final_tags = list(set(tags_hint + [best_match])) if tags_hint else [best_match]
        return {
            "tags": final_tags,
            "confidence": confidence,
            "classification_context": f"rule match: '{best_match}' ({best_hits} keywords, weight={_get_rule_weight(best_match, best_hits)})",
            "primary_tag": best_match,
        }

    # Phase 3: Fallback — content keyword scan via resolve_primary_tag
    primary = resolve_primary_tag([], content)
    confidence = _CONFIDENCE_BASE_FALLBACK
    if is_case and situation and judgment:
        confidence += _CONFIDENCE_BOOST_CASE_FIELDS

    final_tags = list(set(tags_hint + [primary])) if tags_hint else [primary]
    return {
        "tags": final_tags,
        "confidence": confidence,
        "classification_context": f"content fallback: '{primary}' (no strong keyword match)",
        "primary_tag": primary,
    }


def _get_rule_weight(tag, hits):
    """Get the weight used for a matched rule (for logging)."""
    for t, kws, w in _CLASSIFICATION_RULES:
        if t == tag:
            return w
    return 0


def _write_memory_file(memory_id, content, file_path, workspace=None):
    """Write memory content to its category directory file.

    Args:
        memory_id: Memory ID string.
        content: Memory content.
        file_path: Relative file path (e.g. "memory/project/mem_xxx.md").
        workspace: Workspace root (for absolute path).

    Returns:
        str: Absolute file path written, or None if skipped.
    """
    if not workspace or not file_path:
        return None

    abs_path = os.path.join(workspace, file_path)
    dir_name = os.path.dirname(abs_path)
    os.makedirs(dir_name, exist_ok=True)

    import tempfile
    tmp = tempfile.NamedTemporaryFile(
        mode='w', dir=dir_name, delete=False, encoding='utf-8'
    )
    try:
        tmp.write(content or "")
        tmp.close()
        os.replace(tmp.name, abs_path)
    except BaseException:
        tmp.close()
        try:
            os.unlink(tmp.name)
        except OSError:
            pass
        raise
    return abs_path


def _build_content_from_case_fields(situation, judgment, consequence, action_conclusion, content):
    """Build content string from case fields if no content provided.

    Returns (content, is_case) tuple.
    """
    is_case = any([situation, judgment, consequence, action_conclusion])
    if is_case and not content:
        parts = []
        if situation:
            parts.append(f"情境：{situation}")
        if judgment:
            parts.append(f"判断：{judgment}")
        if consequence:
            parts.append(f"后果：{consequence}")
        if action_conclusion:
            parts.append(f"修正：{action_conclusion}")
        content = "\n".join(parts)
    return content, is_case


def _build_new_memory(content, importance, tags, situation, judgment, consequence,
                      action_conclusion, reversibility, boundary_words, alternatives,
                      provenance_source, is_case, decay_config=None,
                      classification=None, existing_ids=None):
    """Build a new memory dict (without saving).

    Args:
        classification: Optional dict from _classify(). If None, runs _classify internally.
        existing_ids: Optional set of existing memory_ids for uniqueness guarantee.

    Returns (mem_dict, cost_factors, is_l1, importance_explain).
    """
    now = _now_iso()
    entities = extract_entities(content)
    cost_factors = evaluate_cost_signals(content, situation, judgment)
    is_l1 = cost_factors.get("transfer_cost", 0) > 0 or cost_factors.get("human_cost", 0) > 0
    importance_explain = build_importance_explain(importance, cost_factors) if is_l1 else None

    initial_status = "draft" if is_case else "active"
    id_prefix = "case" if is_case else "mem"
    mem_id = f"{id_prefix}_{uuid.uuid4().hex[:8]}"

    provenance_level, prov_source = _determine_provenance(content, situation, is_case, provenance_source)

    # v0.4.2 P2: Provenance multiplicative confidence (SimonClaw)
    confidence = _compute_provenance_confidence(
        provenance_level,
        decay_config=decay_config,
    )

    # v0.4.2 P2: Assign memory_type for per-type decay (ovea)
    case_origin = situation if is_case else None
    mem_type = _assign_memory_type(provenance_level, case_origin, tags)

    # v0.4.5: Classification
    if classification is None:
        classification = _classify(content, tags_hint=tags, is_case=is_case,
                                  situation=situation, judgment=judgment)
    class_tags = classification.get("tags", tags or [])
    class_confidence = classification.get("confidence", 0.5)
    class_context = classification.get("classification_context", "auto")
    primary_tag = classification.get("primary_tag", "misc")

    # v0.4.5: memory_id (new format) + file_path
    _existing = existing_ids if existing_ids is not None else set()
    new_memory_id = generate_memory_id(content, existing_ids=_existing)
    file_path = derive_file_path(new_memory_id, class_tags, content)

    # v0.4.5: Confidence-based routing
    action, label = classify_confidence_level(class_confidence)
    inbox_reason = None
    needs_review = False
    if action == "inbox":
        inbox_reason = "uncertain" if class_confidence < 0.5 else None
        # Override file_path to _inbox
        file_path = f"memory/_inbox/uncertain/{new_memory_id}.md"
    elif action == "review":
        needs_review = True

    mem = {
        "id": mem_id,
        "content": content,
        "importance": importance,
        "entities": entities,
        "tags": class_tags,
        "created_at": now,
        "last_accessed": now,
        "access_count": 0,
        "decay_score": importance,
        "status": initial_status,
        "case_type": "case" if is_case else "memory",
        "situation": situation or None,
        "judgment": judgment or None,
        "consequence": consequence or None,
        "action_conclusion": action_conclusion or None,
        "confidence": confidence,
        "reversibility": reversibility if reversibility is not None else DEFAULT_REVERSIBILITY,
        "beta": 1.0,
        "trigger_count": 0,
        "last_triggered": None,
        "cooling_threshold": COOLING_THRESHOLD,
        "boundary_words": boundary_words or [],
        "conflict_refs": [],
        "failure_conditions": [],
        "failure_count": 0,
        "last_failure_trigger": None,
        "last_failure_fix": None,
        "source_case_id": None,
        "alternatives_considered": alternatives or [],
        "cost_factors": cost_factors,
        "quality_gate": {
            "confidence": confidence,
            "gate_mode": "normal",
            "bypass_reason": None,
        },
        "importance_explain": importance_explain,
        "security_version": 1,
        "cooldown_active": False,
        "cooldown_until": None,
        "observing_since": None,
        "suspended_pending_count": 0,
        "provenance_level": provenance_level,
        "provenance_source": prov_source,
        "citations": [],
        "memory_type": mem_type,
        # v0.4.5 fields
        "memory_id": new_memory_id,
        "file_path": file_path,
        "tags_locked": True,
        "classification": classification,
        "classification_confidence": class_confidence,
        "classification_context": class_context,
        "inbox_reason": inbox_reason,
        "signal_level": None,
        "reactivation_count": 0,
        "last_reactivated": None,
        "trigger_words": [],
        "needs_review": needs_review,
        "needs_review_since": _now_iso() if needs_review else None,
        "needs_review_timeout": "7d",
        "review_result": None,
        "reviewed_at": None,
        "version": 0,
        "access_signals": [],
    }

    # Post-stress review (SimonClaw) — auto-mark authority context
    try:
        from memory_case_grow import mark_authority_context, schedule_post_stress_review
        if mark_authority_context(mem):
            schedule_post_stress_review(mem)
    except ImportError:
        pass

    # Auto-promote draft → observing if case has all core fields
    if is_case and situation and judgment:
        mem["status"] = "observing"
        mem["observing_since"] = now

    return mem, cost_factors, is_l1, importance_explain


def _run_quality_gate(mem, content, meta, meta_path, situation, judgment,
                      consequence, action_conclusion, tags):
    """Run quality gate check on a new memory.

    Returns (intervention_level, queue_result_or_None).
    queue_result is set when L2_PAUSE queues the write.
    """
    try:
        qg_path = os.path.join(os.path.dirname(__file__), "quality_gate.py")
        if not os.path.exists(qg_path):
            return None, None

        qg_mod = _load_module_from_path("quality_gate", qg_path)
        if qg_mod is None:
            return None, None

        all_passed, layer_results, _ = qg_mod.check_all_layers(content, meta)
        gate_state = qg_mod.get_gate_state(meta)
        intervention_level, _, _ = qg_mod.compute_intervention_level(
            gate_state,
            "ingest",
            meta,
        )

        mem["quality_gate"] = {
            "confidence": mem.get("confidence", DEFAULT_CONFIDENCE),
            "gate_mode": gate_state.get("state", "normal"),
            "bypass_reason": None if all_passed else _format_quality_bypass_reason(layer_results),
            "intervention_level": intervention_level,
        }

        trigger = "clean" if all_passed else "anomaly"
        new_state, _, _ = qg_mod.transition_state(gate_state, trigger, reason="ingest_check")
        qg_mod.save_gate_state(meta_path, meta, new_state)
        qg_mod.record_result(meta_path, meta, all_passed)

        if intervention_level == qg_mod.INTERVENTION_L2_PAUSE:
            queue_result = qg_mod.enqueue_write(
                meta_path,
                {
                    "action": "ingest",
                    "fields": {
                        "content": content,
                        "id": mem["id"],
                        "importance": mem["importance"],
                        "tags": tags or [],
                        "status": mem.get("status", "active"),
                        "situation": situation,
                        "judgment": judgment,
                        "consequence": consequence,
                        "action_conclusion": action_conclusion,
                        "reversibility": mem.get("reversibility", 1),
                        "case_type": mem.get("case_type"),
                        "provenance_level": mem.get("provenance_level"),
                        "provenance_source": mem.get("provenance_source"),
                    },
                },
                queue_reason=f"L2_PAUSE: state={gate_state.get('state')}",
            )
            return intervention_level, queue_result

        return intervention_level, None
    except (ImportError, ModuleNotFoundError):
        return None, None
    except Exception:
        import logging
        logging.warning("quality_gate module raised an unexpected error", exc_info=True)
        return None, None


def _print_ingest_result(mem, content, tags, is_case, is_l1, cost_factors, importance_explain):
    """Print ingest result to stdout."""
    print(f"[OK] Memory created: {mem['id']} (status: {mem['status']})")
    print(f"  Content: {content[:100]}")
    print(f"  Importance: {mem['importance']}")
    print(f"  Tags: {tags or []}")
    print(f"  Entities: {len(mem['entities'])} extracted")
    if is_case:
        filled = []
        if mem.get("situation"):
            filled.append("情境✓")
        if mem.get("judgment"):
            filled.append("判断✓")
        if mem.get("consequence"):
            filled.append("后果✓")
        if mem.get("action_conclusion"):
            filled.append("修正✓")
        print(f"  Case template: {', '.join(filled)}")
        print(f"  Reversibility: {mem['reversibility']} (0=零成本 1=低成本 2=高成本 3=不可逆)")
    if is_l1:
        print(f"  Cost signals (L1): {cost_factors}")
        print(f"  Importance explain: {importance_explain}")
    if mem.get("provenance_level"):
        print(f"  Provenance level: {mem['provenance_level']} (source: {mem['provenance_source']})")


def run(content, importance, tags, meta_path, workspace=None,
        update_id=None, situation=None, judgment=None, consequence=None,
        action_conclusion=None, reversibility=None, boundary_words=None,
        alternatives=None, skip_security=False, provenance_source=None):
    """Main ingest logic — now delegated to the app/repo layers."""
    from mg_app.ingest_service import IngestService
    from mg_repo.meta_json_repository import MetaJsonRepository

    resolved_content, is_case = _build_content_from_case_fields(
        situation,
        judgment,
        consequence,
        action_conclusion,
        content,
    )

    repo = MetaJsonRepository(meta_path, workspace=workspace)
    service = IngestService(repo)
    result = service.ingest(
        content=resolved_content,
        importance=importance,
        tags=tags,
        workspace=workspace,
        update_id=update_id,
        situation=situation,
        judgment=judgment,
        consequence=consequence,
        action_conclusion=action_conclusion,
        reversibility=reversibility,
        boundary_words=boundary_words,
        alternatives=alternatives,
        skip_security=skip_security,
        provenance_source=provenance_source,
    )

    if result.get("action") == "created":
        mem = result["memory"]
        _print_ingest_result(
            mem,
            resolved_content or "",
            tags,
            is_case,
            result.get("is_l1", False),
            result.get("cost_factors", {}),
            result.get("importance_explain"),
        )
    elif result.get("action") == "queued":
        print(f"[L2_QUEUED] Memory queued: {result['id']} (gate state: CRITICAL)")
        queue_result = result.get("queue_result")
        queue_size = queue_result.get("queue_size", "?") if isinstance(queue_result, Mapping) else "?"
        print(f"  Queue size: {queue_size}")
    elif result.get("action") == "dedup_found":
        meta = repo.load_meta(persist=False)
        memories = meta.get("memories", []) if isinstance(meta, Mapping) else []
        dup = quick_dedup_check(resolved_content or "", memories)
        if dup:
            print(f"[DEDUP] Similar memory found: [{dup.get('id')}] {dup.get('content', '')[:80]}")
            print(f"  Consider using --update {dup.get('id')} instead of creating new entry.")
    elif result.get("action") == "updated":
        print(f"[OK] Memory updated: {result['id']}")

    return result


if __name__ == "__main__":
    p = argparse.ArgumentParser(description="memory-guardian ingest (v0.4)")
    p.add_argument("--content", default=None, help="Memory content text")
    p.add_argument("--importance", type=float, default=0.5, help="Importance 0-1")
    p.add_argument("--tags", default="", help="Comma-separated tags")
    p.add_argument("--workspace", default=None, help="Workspace root path")
    p.add_argument("--meta", default=None, help="Path to meta.json")
    p.add_argument("--stdin", action="store_true", help="Read content from stdin")
    p.add_argument("--update", default=None, help="Memory ID to update")
    # v0.4 case fields
    p.add_argument("--situation", default=None, help="情境·触发条件+背景")
    p.add_argument("--judgment", default=None, help="判断·执行意图")
    p.add_argument("--consequence", default=None, help="后果·验证结果")
    p.add_argument("--action-conclusion", default=None, help="修正·行动结论")
    p.add_argument("--reversibility", type=int, default=None, choices=[0, 1, 2, 3],
                   help="可逆性: 0(零成本) 1(低成本) 2(高成本) 3(不可逆)")
    p.add_argument("--boundary-words", default=None, help="Comma-separated boundary/anchor words")
    p.add_argument("--alternatives", default=None, help="Comma-separated alternatives considered")
    p.add_argument("--skip-security", action="store_true", help="Skip security check")
    # v0.4.1: Provenance source
    p.add_argument("--provenance-source", choices=["human", "system", "external"],
                   help="Provenance source for memory")
    args = p.parse_args()

    content = args.content
    if args.stdin:
        content = sys.stdin.read().strip()
    if not content and not any([args.situation, args.judgment, args.consequence, args.action_conclusion]):
        print("Error: Provide --content or case fields (--situation/--judgment/etc)")
        sys.exit(1)

    tags = [t.strip() for t in args.tags.split(",") if t.strip()] if args.tags else []
    workspace = args.workspace or os.environ.get(
        "OPENCLAW_WORKSPACE", os.path.expanduser("~/workspace/agent/workspace")
    )
    meta_path = args.meta or os.path.join(workspace, "memory", "meta.json")
    boundary_words = [w.strip() for w in args.boundary_words.split(",") if w.strip()] if args.boundary_words else []
    alternatives = [a.strip() for a in args.alternatives.split(",") if a.strip()] if args.alternatives else []

    result = run(
        content=content,
        importance=args.importance,
        tags=tags,
        meta_path=meta_path,
        workspace=workspace,
        update_id=args.update,
        situation=args.situation,
        judgment=args.judgment,
        consequence=args.consequence,
        action_conclusion=args.action_conclusion,
        reversibility=args.reversibility,
        boundary_words=boundary_words,
        alternatives=alternatives,
        skip_security=args.skip_security,
        provenance_source=args.provenance_source,
    )
    record_module_run(
        workspace,
        "memory_ingest",
        input_count=1,
        output_count=1 if result.get("action") in {"created", "queued", "updated"} else 0,
    )

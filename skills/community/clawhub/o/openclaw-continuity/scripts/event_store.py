#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Event Store — V2 event tracking layer.

Events represent "what happened" with causal context and lifecycle.
Hooks represent "what to do next" with scheduling and dispatch.

Event → Hook is one-way: events may spawn hooks, hooks reference events.

Usage (CLI):
  python3 event_store.py create --type defer --title "先放著的話題" --cause "使用者說晚點再聊"
  python3 event_store.py list [--status active|parked|due]
  python3 event_store.py get --id EVT-xxx
  python3 event_store.py update --id EVT-xxx --status parked
  python3 event_store.py due [--limit 3]
  python3 event_store.py close --id EVT-xxx --reason completed
  python3 event_store.py context [--limit 5]    # For runtime-context injection
  python3 event_store.py gc [--days 30]          # Garbage-collect old closed events

Usage (Python import):
  from event_store import EventStore
  store = EventStore("/path/to/events.json")
  evt = store.create(event_type="defer", title="...", cause_summary="...")
"""

import json
import os
import sys
import uuid
from datetime import datetime, timedelta, timezone
from typing import Optional, List, Dict, Any

__version__ = "1.1.0"

DEFAULT_OPENCLAW_STATE_DIR = os.path.expanduser("~/.openclaw")

# ── Host Semantic Config (lazy-loaded) ──

_semantic_categories = None   # List[SemanticCategory] | None
_policy_overrides = None      # Dict[str, str] | None


def _load_host_semantics():
    """Lazy-load host semantic config. Safe to call multiple times."""
    global _semantic_categories, _policy_overrides
    if _semantic_categories is not None:
        return
    try:
        from semantic_config import load_semantic_config, parse_categories, get_policy_overrides
        cfg = load_semantic_config()
        _semantic_categories = parse_categories(cfg)
        _policy_overrides = get_policy_overrides(cfg)
    except Exception:
        _semantic_categories = []
        _policy_overrides = {}


def get_host_categories():
    """Return parsed host semantic categories (lazy-loaded)."""
    _load_host_semantics()
    return _semantic_categories or []


def get_policy_override(event_type: str) -> Optional[str]:
    """Return host policy override for an event type, or None."""
    _load_host_semantics()
    if _policy_overrides:
        return _policy_overrides.get(event_type)
    return None


def _is_host_event_type(event_type: str) -> bool:
    """Check if event_type is defined by a host semantic category."""
    for cat in get_host_categories():
        if cat.event_type == event_type:
            return True
    return False


# ── Schema ──

EVENT_TYPES = [
    "defer",               # 「先放著 / 晚點再說」
    "wake_followup",       # 「我醒來再聊 / 起床後提醒我」
    "checkin",             # 「之後問我 / 過一陣子確認」
    "reminder_intent",     # 「提醒我做X」
    "unresolved_topic",    # 對話中未結束的議題
    "health_event",        # 健康事件（跌倒、住院、生病）
    "emotional_event",     # 情緒事件（壓力、難過、焦慮）
    "work_event",          # 工作事件（deadline、專案、壓力）
    "relationship_event",  # 關係事件（吵架、想念、紀念日）
    "task_progress",       # 進行中的任務/項目
    "incident",            # 突發事件
    "custom",              # 自定義
]

EVENT_STATUSES = [
    "active",       # 正在追蹤
    "parked",       # 暫停追蹤（使用者說先放著）
    "due",          # 該追問了（next_check_at 到期）
    "completed",    # 已結束
    "cancelled",    # 取消
    "superseded",   # 被新事件取代
    "suggested",    # AI 建議建立，等使用者確認
]

EVENT_PRIORITIES = ["low", "medium", "high", "critical"]
IMMEDIATE_HOOK_EVENT_TYPES = {"health_event", "emotional_event", "wake_followup"}
SCHEDULED_EVENT_DEFAULT_MINUTES = {
    "defer": 120,
    "checkin": 180,
    "reminder_intent": 60,
    "task_progress": 180,
    "unresolved_topic": 180,
}

# ── Helpers ──

def _now_iso() -> str:
    return datetime.now().astimezone().isoformat(timespec="seconds")

def _make_event_id() -> str:
    ts = datetime.now().strftime("%Y%m%d-%H%M%S")
    short = uuid.uuid4().hex[:6]
    return f"EVT-{ts}-{short}"

def _parse_dt(s: Optional[str]) -> Optional[datetime]:
    if not s:
        return None
    try:
        return datetime.fromisoformat(s)
    except (ValueError, TypeError):
        return None


def _default_next_check_at(event_type: str, now_dt: Optional[datetime] = None, base_dt: Optional[datetime] = None) -> str:
    minutes = SCHEDULED_EVENT_DEFAULT_MINUTES.get(event_type)
    if not minutes:
        return ""
    anchor = base_dt or now_dt or datetime.now().astimezone()
    if anchor.tzinfo is None:
        anchor = anchor.replace(tzinfo=datetime.now().astimezone().tzinfo)
    return (anchor + timedelta(minutes=minutes)).isoformat(timespec="seconds")


# ── Event Store ──

class EventStore:
    """File-backed event store with JSON persistence."""

    def __init__(self, path: str):
        self.path = path
        self._data = self._load()

    def _load(self) -> dict:
        if os.path.exists(self.path):
            try:
                with open(self.path) as f:
                    return json.load(f)
            except (json.JSONDecodeError, IOError):
                pass
        return {"version": 1, "updated_at": _now_iso(), "events": []}

    def _save(self):
        self._data["updated_at"] = _now_iso()
        os.makedirs(os.path.dirname(self.path) or ".", exist_ok=True)
        with open(self.path, "w") as f:
            json.dump(self._data, f, indent=2, ensure_ascii=False)

    @property
    def events(self) -> List[dict]:
        return self._data.get("events", [])

    # ── CRUD ──

    def create(
        self,
        event_type: str,
        title: str,
        cause_summary: str = "",
        desired_followup: str = "",
        priority: str = "medium",
        owner: str = "system",
        source_session: str = "",
        source_channel: str = "",
        source_turn_range: str = "",
        next_check_at: Optional[str] = None,
        linked_hook_ids: Optional[List[str]] = None,
        linked_memory_refs: Optional[List[str]] = None,
        metadata: Optional[Dict[str, Any]] = None,
    ) -> dict:
        """Create a new event. Returns the created event dict."""
        now = _now_iso()
        evt = {
            "event_id": _make_event_id(),
            "event_type": event_type if (event_type in EVENT_TYPES or _is_host_event_type(event_type)) else "custom",
            "title": title,
            "status": "active",
            "priority": priority if priority in EVENT_PRIORITIES else "medium",
            "owner": owner,
            "cause_summary": cause_summary,
            "desired_followup": desired_followup,
            "source_session": source_session,
            "source_channel": source_channel,
            "source_turn_range": source_turn_range,
            "created_at": now,
            "last_update_at": now,
            "next_check_at": next_check_at or "",
            "linked_hook_ids": linked_hook_ids or [],
            "linked_memory_refs": linked_memory_refs or [],
            "closure_reason": "",
            "metadata": metadata or {},
        }
        self._data["events"].append(evt)
        self._save()
        return evt

    def get(self, event_id: str) -> Optional[dict]:
        for evt in self.events:
            if evt.get("event_id") == event_id:
                return evt
        return None

    def update(self, event_id: str, **fields) -> Optional[dict]:
        """Update specific fields of an event. Returns updated event or None."""
        for evt in self.events:
            if evt.get("event_id") == event_id:
                allowed = {
                    "status", "title", "priority", "cause_summary",
                    "desired_followup", "next_check_at", "owner",
                    "linked_hook_ids", "linked_memory_refs",
                    "closure_reason", "metadata",
                }
                for k, v in fields.items():
                    if k in allowed:
                        evt[k] = v
                evt["last_update_at"] = _now_iso()
                self._save()
                return evt
        return None

    def close(self, event_id: str, reason: str = "completed", status: str = "completed") -> Optional[dict]:
        """Close an event with a reason."""
        if status not in ("completed", "cancelled", "superseded"):
            status = "completed"
        return self.update(event_id, status=status, closure_reason=reason)

    def link_hook(self, event_id: str, hook_id: str) -> Optional[dict]:
        """Link a hook to an event."""
        evt = self.get(event_id)
        if evt:
            ids = evt.get("linked_hook_ids", [])
            if hook_id not in ids:
                ids.append(hook_id)
            return self.update(event_id, linked_hook_ids=ids)
        return None

    def link_memory(self, event_id: str, memory_ref: str) -> Optional[dict]:
        """Link a memory reference to an event."""
        evt = self.get(event_id)
        if evt:
            refs = evt.get("linked_memory_refs", [])
            if memory_ref not in refs:
                refs.append(memory_ref)
            return self.update(event_id, linked_memory_refs=refs)
        return None

    # ── Queries ──

    def list_by_status(self, statuses: Optional[List[str]] = None) -> List[dict]:
        """List events by status. None = all non-closed."""
        if statuses is None:
            statuses = ["active", "parked", "due"]
        return [e for e in self.events if e.get("status") in statuses]

    def list_due(self, now_dt: Optional[datetime] = None, limit: int = 5) -> List[dict]:
        """List events whose next_check_at has arrived, or status is 'due'."""
        if now_dt is None:
            now_dt = datetime.now().astimezone()
        result = []
        for evt in self.events:
            if evt.get("status") in ("completed", "cancelled", "superseded"):
                continue
            # Explicit due status
            if evt.get("status") == "due":
                result.append(evt)
                continue
            if evt.get("status") in ("active", "parked") and not evt.get("next_check_at"):
                derived = _default_next_check_at(
                    evt.get("event_type", ""),
                    now_dt=now_dt,
                    base_dt=_parse_dt(evt.get("last_update_at")) or _parse_dt(evt.get("created_at")),
                )
                if derived:
                    evt["next_check_at"] = derived
                    evt["last_update_at"] = _now_iso()
            # next_check_at has passed
            nca = _parse_dt(evt.get("next_check_at"))
            if nca and nca <= now_dt and evt.get("status") in ("active", "parked"):
                evt["status"] = "due"
                evt["last_update_at"] = _now_iso()
                result.append(evt)
        if result:
            self._save()  # persist status changes
        # Sort by priority (critical first) then created_at
        priority_order = {"critical": 0, "high": 1, "medium": 2, "low": 3}
        result.sort(key=lambda e: (priority_order.get(e.get("priority", "medium"), 2), e.get("created_at", "")))
        return result[:limit]

    def list_active_summary(self, limit: int = 5, staleness_hours: int = 72) -> List[dict]:
        """Return active/parked/due events for runtime-context injection.

        Applies four filters:
        1. Staleness: transient event types have type-specific max age.
        2. Universal max age: all events capped at 168h (7 days).
        3. Recursive: events whose cause_summary is structured event display are excluded.
        4. Priority sort (recency-weighted within same priority) + limit.
        """
        now_dt = datetime.now().astimezone()
        # Type-specific staleness: shorter windows for transient event types
        _type_staleness_hours = {
            "emotional_event": staleness_hours,       # 72h
            "wake_followup": 24,                      # wake events are transient
            "health_followup": staleness_hours,       # 72h
        }
        universal_max_hours = 168  # 7 days absolute cap for any event
        universal_cutoff = now_dt - timedelta(hours=universal_max_hours)
        live = []
        for e in self.events:
            if e.get("status") not in ("active", "parked", "due"):
                continue
            # Filter recursive events (cause_summary is structured display format)
            cause = str(e.get("cause_summary") or "")
            if cause.startswith("- 🔵") or cause.startswith("- ❓") or "[emotional_event/" in cause or "[health_event/" in cause:
                continue
            created = _parse_dt(e.get("created_at"))
            # Universal max age
            if created and created < universal_cutoff:
                continue
            # Type-specific staleness filter
            etype = e.get("event_type", "")
            if etype in _type_staleness_hours:
                type_cutoff = now_dt - timedelta(hours=_type_staleness_hours[etype])
                if created and created < type_cutoff:
                    continue
            live.append(e)
        priority_order = {"critical": 0, "high": 1, "medium": 2, "low": 3}
        # Sort by priority first, then by recency (newest first within same priority)
        live.sort(key=lambda e: (priority_order.get(e.get("priority", "medium"), 2), -((_parse_dt(e.get("created_at")) or now_dt).timestamp())))
        return live[:limit]

    def gc(self, days: int = 30) -> int:
        """Remove closed events older than N days. Returns count removed."""
        cutoff = datetime.now().astimezone() - timedelta(days=days)
        before = len(self.events)
        self._data["events"] = [
            e for e in self.events
            if e.get("status") not in ("completed", "cancelled", "superseded")
            or (_parse_dt(e.get("last_update_at")) or datetime.now().astimezone()) > cutoff
        ]
        after = len(self.events)
        if before != after:
            self._save()
        return before - after

    # ── Context Building ──

    def list_suggested(self, limit: int = 3) -> List[dict]:
        """Return events with status=suggested, most recent first."""
        suggested = [e for e in self.events if e.get("status") == "suggested"]
        suggested.sort(key=lambda e: e.get("created_at", ""), reverse=True)
        return suggested[:limit]

    def build_event_context_prompt(self, now_dt: Optional[datetime] = None, limit: int = 5) -> str:
        """Build a prompt section for active events, for runtime-context injection."""
        if now_dt is None:
            now_dt = datetime.now().astimezone()

        live = self.list_active_summary(limit)
        suggested = self.list_suggested(1)
        if not live and not suggested:
            return ""

        lines = [
            "## Active tracked events (trusted structured state)",
            "These are events you are currently tracking. Use them to maintain continuity.",
            "When relevant, reference the event and its cause — do not invent new context.",
            "",
        ]

        for evt in live:
            status_icon = {"active": "🔵", "parked": "⏸️", "due": "🔴"}.get(evt.get("status", ""), "❓")
            title = evt.get("title", "untitled")
            etype = evt.get("event_type", "unknown")
            priority = evt.get("priority", "medium")
            cause = evt.get("cause_summary", "")
            followup = evt.get("desired_followup", "")
            created = evt.get("created_at", "")[:16]
            nca = evt.get("next_check_at", "")
            status = evt.get("status", "?")

            line = f"- {status_icon} **{title}** [{etype}/{priority}] (status: {status})"
            if cause:
                line += f"\n  cause: {cause[:120]}"
            if followup:
                line += f"\n  followup: {followup[:120]}"
            if nca:
                line += f"\n  next_check: {nca[:16]}"
            line += f"\n  created: {created}"

            lines.append(line)

        # Pending suggestions — model should ask user to confirm
        if suggested:
            lines.append("")
            lines.append("### Pending event suggestions")
            lines.append("These events were detected but need user confirmation. Ask briefly: 「這件事要我幫你記著追嗎？」")
            lines.append("If user says yes/好/對, confirm it. If no/不用/算了, drop it. Do NOT auto-confirm.")
            for evt in suggested:
                title = evt.get("title", "untitled")
                cause = evt.get("cause_summary", "")
                lines.append(f"- ❓ **{title}** — {cause[:100]}")

        return "\n".join(lines)

    def build_new_session_carryover(self, limit: int = 3) -> str:
        """Build a carryover section for new sessions — top unresolved events."""
        live = self.list_active_summary(limit)
        if not live:
            return ""

        lines = [
            "## Unresolved events from previous sessions (trusted structured state)",
            "These events are still being tracked. Continue from where you left off.",
            "",
        ]

        for evt in live:
            title = evt.get("title", "untitled")
            cause = evt.get("cause_summary", "")
            followup = evt.get("desired_followup", "")
            status = evt.get("status", "?")

            line = f"- **{title}** (status: {status})"
            if cause:
                line += f" — {cause[:100]}"
            if followup:
                line += f" → {followup[:100]}"

            lines.append(line)

        return "\n".join(lines)


# ── Event → Hook Helpers ──

def should_auto_generate_hook(event: dict) -> Optional[dict]:
    """Decide if an event should auto-generate a hook.
    Returns hook params dict if yes, None if no.
    """
    etype = event.get("event_type", "")
    status = event.get("status", "")
    nca = event.get("next_check_at", "")

    # Only active/parked events with next_check_at should generate hooks
    if status not in ("active", "parked", "due"):
        return None

    # Types that auto-generate hooks
    auto_types = {
        "defer": "progress_followup",
        "wake_followup": "care_message",
        "checkin": "progress_followup",
        "reminder_intent": "progress_followup",
        "health_event": "health_followup",
        "emotional_event": "emotional_followup",
        "task_progress": "progress_followup",
    }

    hook_type = auto_types.get(etype)

    # Host-defined event types: map to progress_followup by default
    if not hook_type and _is_host_event_type(etype):
        hook_type = "progress_followup"

    if not hook_type:
        return None

    # health/emotional/wake generate hooks immediately (no next_check_at needed)
    if etype not in IMMEDIATE_HOOK_EVENT_TYPES and not nca:
        return None

    return {
        "hook_type": hook_type,
        "trigger_at": nca or "",
        "source_summary": event.get("cause_summary", event.get("title", "")),
        "normalized_seed_summary": event.get("title", ""),
        "event_id": event.get("event_id", ""),
        "event_type": etype,
        "priority": event.get("priority", "medium"),
    }


# ── Natural Language → Event Detection ──

DEFER_SIGNALS = [
    "先放著", "晚點再說", "等一下再", "之後再", "先不說", "先跳過",
    "先這樣", "明天再", "回來再", "醒來再", "下次再", "改天",
    "先忙", "等等再", "待會再", "過一陣子",
]

WAKE_SIGNALS = [
    "醒來", "起床", "起來再", "睡醒",
]

CHECKIN_SIGNALS = [
    "提醒我", "之後問我", "記得問", "幫我記", "別忘了問",
    "過幾天問", "追蹤", "follow up", "跟進",
]

HEALTH_SIGNALS = [
    "跌倒", "受傷", "住院", "生病", "發燒", "頭痛", "不舒服",
    "看醫生", "急診", "開刀", "手術",
]

EMOTIONAL_SIGNALS = [
    "壓力", "焦慮", "難過", "沮喪", "心情不好", "煩", "累",
    "想哭", "撐不住", "崩潰",
]

NEGATION_PREFIXES = ["沒", "不", "沒有", "不是", "不會", "沒在", "不再", "無"]

def _is_negated(text: str, signal: str) -> bool:
    """Check if a signal match is negated (e.g., '沒頭痛' should not trigger health_event)."""
    idx = text.find(signal)
    if idx <= 0:
        return False
    # Check 1-3 chars before the signal for negation
    before = text[max(0, idx - 3):idx]
    return any(before.endswith(neg) for neg in NEGATION_PREFIXES)


def detect_event_from_text(text: str, context: str = "") -> Optional[dict]:
    """Detect if user text implies an event that should be tracked.
    Returns a partial event dict or None.

    Detection order: high-priority signals first (health > emotional > checkin > wake > defer).
    """
    results = []

    # Health (high priority)
    for sig in HEALTH_SIGNALS:
        if sig in text and not _is_negated(text, sig):
            results.append({
                "event_type": "health_event",
                "title": f"健康事件：{sig}",
                "cause_summary": text[:200],
                "desired_followup": "主動關心身體狀況",
                "priority": "high",
                "_rank": 0,
            })
            break

    # Emotional (high priority)
    for sig in EMOTIONAL_SIGNALS:
        if sig in text and not _is_negated(text, sig):
            results.append({
                "event_type": "emotional_event",
                "title": f"情緒狀態：{sig}",
                "cause_summary": text[:200],
                "desired_followup": "適時關心情緒",
                "priority": "high",
                "_rank": 1,
            })
            break

    # Checkin
    for sig in CHECKIN_SIGNALS:
        if sig in text:
            results.append({
                "event_type": "checkin",
                "title": _extract_topic(text, sig),
                "cause_summary": text[:200],
                "desired_followup": "按使用者要求追問",
                "priority": "medium",
                "_rank": 2,
            })
            break

    # Wake followup
    for sig in WAKE_SIGNALS:
        if sig in text:
            results.append({
                "event_type": "wake_followup",
                "title": _extract_topic(text, sig),
                "cause_summary": text[:200],
                "desired_followup": "使用者醒來後主動接回這個話題",
                "priority": "medium",
                "_rank": 3,
            })
            break

    # Defer (lowest priority signal)
    for sig in DEFER_SIGNALS:
        if sig in text:
            results.append({
                "event_type": "defer",
                "title": _extract_topic(text, sig),
                "cause_summary": text[:200],
                "desired_followup": "使用者說先放著，適時主動接回",
                "priority": "medium",
                "_rank": 4,
            })
            break

    # ── Host semantic categories (additive) ──
    for cat in get_host_categories():
        for sig in cat.signals:
            if sig in text:
                if cat.negation_aware and _is_negated(text, sig):
                    continue
                results.append({
                    "event_type": cat.event_type,
                    "title": cat.format_title(sig),
                    "cause_summary": text[:200],
                    "desired_followup": cat.desired_followup,
                    "priority": cat.priority,
                    "_rank": cat.rank,
                    "_host_policy": cat.policy,  # carried through for process_event_entry
                })
                break  # one match per category

    if not results:
        return None

    # Return highest priority (lowest rank)
    winner = min(results, key=lambda r: r["_rank"])
    winner.pop("_rank", None)
    return winner


def _extract_topic(text: str, signal: str) -> str:
    """Try to extract a meaningful topic from text around the signal."""
    # Simple: take up to 60 chars, trimming the signal keyword
    idx = text.find(signal)
    if idx > 0:
        before = text[max(0, idx - 40):idx].strip()
        if before:
            return before[:60]
    after = text[idx + len(signal):].strip()
    if after:
        return after[:60]
    return text[:60]


# ── Event Entry Layer ──
# Three entry modes: manual (user explicitly asks), suggest (AI asks first), auto (high confidence)

# Manual create — user explicitly asks to track something
MANUAL_CREATE_SIGNALS = [
    "幫我記住", "幫我記", "記住這", "追蹤這", "追這件事",
    "提醒我", "之後提醒", "晚點提醒", "記得提醒",
    "之後問我", "晚點問我", "記得問我", "幫我追",
    "keep track", "remind me", "follow up on",
]

# CRUD — view / complete / cancel / park
VIEW_SIGNALS = [
    "現在追蹤什麼", "在追什麼", "有什麼事在追", "追蹤中",
    "我的事件", "事件列表", "有什麼待追", "追蹤清單",
    "what are you tracking", "my events",
]
COMPLETE_SIGNALS = [
    "完成了", "搞定了", "解決了", "做完了", "處理好了",
    "結束了", "已經好了", "OK了", "done",
]
CANCEL_SIGNALS = [
    "取消追蹤", "不追了", "不用追了", "取消那個", "刪掉那個事件",
    "stop tracking", "cancel that",
]
PARK_SIGNALS = [
    "暫停追蹤", "先擱著", "先暫停那個",
    "pause tracking",
]

# Confirmation / denial for suggest mode
CONFIRM_SIGNALS = [
    "好", "對", "幫我記", "記吧", "追吧", "要", "嗯",
    "ok", "OK", "是", "幫我追", "記一下", "好啊", "可以",
]
DENY_SIGNALS = [
    "不用", "不要", "算了", "沒關係", "不必", "跳過", "pass",
]

# Auto create types — high confidence, no need to ask
AUTO_CREATE_TYPES = {
    "defer",            # 使用者主動暫緩 = 明確意圖
    "wake_followup",    # 使用者說醒來再聊 = 明確意圖
    "reminder_intent",  # 使用者說提醒我 = 明確意圖
    "health_event",     # 關鍵字精準（頭痛/住院/跌倒） = 高信心
    "emotional_event",  # 關鍵字精準（壓力/難過/崩潰） = 高信心
}

# Suggest create types — ask user first
SUGGEST_CREATE_TYPES = {
    "checkin",              # 可能是隨口一提
    "unresolved_topic",     # 模糊
    "work_event",           # 不確定是否要追
    "relationship_event",   # 私密，應先問
    "task_progress",        # 可能只是聊天
    "incident",             # 視情況
    "custom",               # 不確定
}


def _matches_any(text: str, signals: List[str]) -> bool:
    """Check if text contains any of the signal phrases."""
    t = text.strip().lower() if text else ""
    for sig in signals:
        if sig.lower() in t:
            return True
    return False


def _find_best_matching_event(events: List[dict], text: str) -> Optional[dict]:
    """Find the event most likely referenced by user text.
    Strategy: keyword overlap between text and event title/cause.
    Fallback: most recent active event.
    """
    active = [e for e in events if e.get("status") in ("active", "parked", "due")]
    if not active:
        return None
    if len(active) == 1:
        return active[0]
    # Score by keyword overlap
    text_chars = set(text)
    best, best_score = None, -1
    for evt in active:
        title = evt.get("title", "")
        cause = evt.get("cause_summary", "")
        combined = title + cause
        score = sum(1 for c in combined if c in text_chars and c.strip())
        if score > best_score:
            best, best_score = evt, score
    return best


def process_event_entry(
    event_store: "EventStore",
    text: str,
    session_key: str = "",
    channel: str = "direct",
    now_dt: Optional[datetime] = None,
) -> dict:
    """Process user text through the event entry layer.

    Returns dict with:
      action: 'manual_create' | 'auto_create' | 'suggest_create' |
              'confirm_suggest' | 'deny_suggest' |
              'view' | 'complete' | 'cancel' | 'park' | 'none'
      event: the event dict (if created/modified) or None
      entry_mode: 'manual' | 'auto' | 'suggest' | 'crud' | 'none'
      frontend_prompt: short prompt for the model to show user ('' if silent)
    """
    if not text or not text.strip():
        return {"action": "none", "event": None, "entry_mode": "none", "frontend_prompt": ""}

    text = text.strip()
    residue_markers = (
        "## Active tracked events",
        "## Pending follow-up topics",
        "## New-session carryover",
        "## Night-owl schedule context",
        "## Household schedule awareness",
        "## Recent dispatch awareness",
        "trusted structured state",
    )
    if any(marker in text for marker in residue_markers):
        return {"action": "none", "event": None, "entry_mode": "none", "frontend_prompt": ""}

    # ── 0. Check pending suggestions first ──
    suggested = event_store.list_suggested(1)
    if suggested:
        if _matches_any(text, CONFIRM_SIGNALS) and len(text) < 20:
            evt = suggested[0]
            event_store.update(evt["event_id"], status="active", owner="user")
            return {
                "action": "confirm_suggest",
                "event": evt,
                "entry_mode": "suggest",
                "frontend_prompt": f"✅ 已開始追蹤：{evt.get('title', '')}",
            }
        if _matches_any(text, DENY_SIGNALS) and len(text) < 20:
            evt = suggested[0]
            event_store.update(evt["event_id"], status="cancelled", closure_reason="使用者拒絕建議")
            return {
                "action": "deny_suggest",
                "event": evt,
                "entry_mode": "suggest",
                "frontend_prompt": "",
            }

    # ── 1. CRUD: view ──
    if _matches_any(text, VIEW_SIGNALS):
        active = [e for e in event_store.events if e.get("status") in ("active", "parked", "due")]
        if not active:
            return {
                "action": "view",
                "event": None,
                "entry_mode": "crud",
                "frontend_prompt": "目前沒有追蹤中的事件。",
            }
        items = []
        for e in active[:8]:
            icon = {"active": "🔵", "parked": "⏸️", "due": "🔴"}.get(e.get("status"), "")
            items.append(f"{icon} {e.get('title', '?')}（{e.get('event_type', '?')}）")
        prompt = "追蹤中：\n" + "\n".join(f"- {it}" for it in items)
        return {
            "action": "view",
            "event": None,
            "entry_mode": "crud",
            "frontend_prompt": prompt,
        }

    # ── 2. CRUD: complete ──
    if _matches_any(text, COMPLETE_SIGNALS):
        target = _find_best_matching_event(event_store.events, text)
        if target:
            event_store.close(target["event_id"], reason="使用者確認完成", status="completed")
            return {
                "action": "complete",
                "event": target,
                "entry_mode": "crud",
                "frontend_prompt": f"✅ 已完成：{target.get('title', '')}",
            }

    # ── 3. CRUD: cancel ──
    if _matches_any(text, CANCEL_SIGNALS):
        target = _find_best_matching_event(event_store.events, text)
        if target:
            event_store.close(target["event_id"], reason="使用者取消", status="cancelled")
            return {
                "action": "cancel",
                "event": target,
                "entry_mode": "crud",
                "frontend_prompt": f"已取消追蹤：{target.get('title', '')}",
            }

    # ── 4. CRUD: park ──
    if _matches_any(text, PARK_SIGNALS):
        target = _find_best_matching_event(event_store.events, text)
        if target:
            event_store.update(target["event_id"], status="parked")
            return {
                "action": "park",
                "event": target,
                "entry_mode": "crud",
                "frontend_prompt": f"⏸️ 已暫停：{target.get('title', '')}",
            }

    # ── 5. Manual create — user explicitly asks ──
    if _matches_any(text, MANUAL_CREATE_SIGNALS):
        # Extract topic from text
        topic = text
        for sig in MANUAL_CREATE_SIGNALS:
            if sig.lower() in text.lower():
                idx = text.lower().find(sig.lower())
                after = text[idx + len(sig):].strip()
                if after:
                    topic = after[:100]
                break
        evt = event_store.create(
            event_type="checkin",
            title=topic[:60],
            cause_summary=text[:200],
            desired_followup="使用者要求追蹤",
            priority="medium",
            owner="user",
            source_session=session_key,
            source_channel=channel,
            next_check_at=_default_next_check_at("checkin", now_dt=now_dt),
        )
        return {
            "action": "manual_create",
            "event": evt,
            "entry_mode": "manual",
            "frontend_prompt": f"✅ 已記住：{topic[:60]}",
        }

    # ── 6. Auto-detect + classify entry mode ──
    detected = detect_event_from_text(text)
    if detected and detected.get("event_type"):
        etype = detected["event_type"]

        # Resolve effective policy: host override > host_policy from detection > built-in sets
        host_override = get_policy_override(etype)
        host_policy = detected.pop("_host_policy", None)
        if host_override:
            effective_policy = host_override
        elif host_policy:
            effective_policy = host_policy
        elif etype in AUTO_CREATE_TYPES:
            effective_policy = "auto"
        elif etype in SUGGEST_CREATE_TYPES:
            effective_policy = "suggest"
        else:
            effective_policy = "suggest"

        if effective_policy == "auto":
            auto_next_check = detected.get("next_check_at") or _default_next_check_at(etype, now_dt=now_dt)
            evt = event_store.create(
                event_type=etype,
                title=detected.get("title", ""),
                cause_summary=detected.get("cause_summary", ""),
                desired_followup=detected.get("desired_followup", ""),
                priority=detected.get("priority", "medium"),
                owner="system",
                source_session=session_key,
                source_channel=channel,
                next_check_at=auto_next_check,
            )
            return {
                "action": "auto_create",
                "event": evt,
                "entry_mode": "auto",
                "frontend_prompt": "",  # silent — auto events don't need frontend noise
            }

        if effective_policy == "suggest":
            suggest_next_check = detected.get("next_check_at") or _default_next_check_at(etype, now_dt=now_dt)
            evt = event_store.create(
                event_type=etype,
                title=detected.get("title", ""),
                cause_summary=detected.get("cause_summary", ""),
                desired_followup=detected.get("desired_followup", ""),
                priority=detected.get("priority", "medium"),
                owner="agent",
                source_session=session_key,
                source_channel=channel,
                next_check_at=suggest_next_check,
            )
            # Override status to suggested
            event_store.update(evt["event_id"], status="suggested")
            return {
                "action": "suggest_create",
                "event": evt,
                "entry_mode": "suggest",
                "frontend_prompt": "",  # model will ask via context prompt
            }

        # policy == "manual" → skip auto-detection, let user explicitly create
        # (falls through to "none")

    # ── 7. Nothing detected ──
    return {"action": "none", "event": None, "entry_mode": "none", "frontend_prompt": ""}


# ── Event ↔ Memory Linkage ──

_MEMORY_HEADING = "V2 event-store"

EVENT_KIND_LABELS = {
    "defer": "暫緩主題",
    "wake_followup": "起床接回",
    "checkin": "追蹤確認",
    "reminder_intent": "提醒事項",
    "unresolved_topic": "未結議題",
    "health_event": "健康事件",
    "emotional_event": "情緒事件",
    "work_event": "工作事件",
    "relationship_event": "關係事件",
    "task_progress": "任務進度",
    "incident": "突發事件",
    "life_context_event": "生活情境",
    "identity_event": "身份資訊",
    "custom": "自定義事件",
}


def _resolve_memory_dir() -> str:
    state_dir = os.environ.get("OPENCLAW_STATE_DIR")
    if not state_dir:
        here = os.path.realpath(__file__)
        marker = os.sep + "workspace" + os.sep + "skills" + os.sep
        if marker in here:
            state_dir = here.split(marker, 1)[0]
        else:
            state_dir = DEFAULT_OPENCLAW_STATE_DIR
    return os.path.join(state_dir, "workspace/memory")


def _daily_memory_path(now_dt: Optional[datetime] = None) -> str:
    if now_dt is None:
        now_dt = datetime.now().astimezone()
    d = now_dt.date().isoformat()
    return os.path.join(_resolve_memory_dir(), f"{d}.md")


def _append_memory_note_once(path: str, heading: str, note: str) -> bool:
    """Append a note under heading in a daily memory markdown file. Returns True if new."""
    import re as _re
    os.makedirs(os.path.dirname(path) or ".", exist_ok=True)
    existing = ""
    if os.path.isfile(path):
        with open(path, "r", encoding="utf-8") as f:
            existing = f.read()
    if note in existing:
        return False
    if heading not in existing:
        stem = os.path.splitext(os.path.basename(path))[0]
        prefix = existing.rstrip()
        body = f"{prefix}\n\n## {heading}\n- {note}\n" if prefix else f"# {stem}\n\n## {heading}\n- {note}\n"
    else:
        body = _re.sub(
            rf"(## {_re.escape(heading)}\n)",
            rf"\1- {note}\n",
            existing,
            count=1,
        )
    with open(path, "w", encoding="utf-8") as f:
        f.write(body)
    return True


def _make_memory_ref(event_id: str, action: str, path: str) -> str:
    """Build a memory ref string: daily-memory path + event_id + action."""
    return f"{path}#{event_id}:{action}"


def _kind_label(event_type: str) -> str:
    return EVENT_KIND_LABELS.get(event_type, event_type)


def write_event_memory_trace(
    event_store: "EventStore",
    event: dict,
    action: str,
    now_dt: Optional[datetime] = None,
) -> Optional[str]:
    """Write a daily memory note for an event lifecycle action and link it.

    Actions: 'created', 'confirmed', 'completed', 'cancelled', 'followup'

    Returns the memory_ref string, or None if deduped.
    """
    if not event:
        return None
    if now_dt is None:
        now_dt = datetime.now().astimezone()

    event_id = event.get("event_id", "?")
    event_type = event.get("event_type", "custom")
    title = event.get("title", "")[:72]
    kind = _kind_label(event_type)

    if action == "created":
        note = f"[{event_id}] 新建追蹤（{kind}）：{title}"
    elif action == "confirmed":
        note = f"[{event_id}] 使用者確認追蹤（{kind}）：{title}"
    elif action == "completed":
        reason = event.get("closure_reason", "")
        note = f"[{event_id}] 完成（{kind}）：{title}" + (f"（{reason[:40]}）" if reason else "")
    elif action == "cancelled":
        reason = event.get("closure_reason", "")
        note = f"[{event_id}] 取消（{kind}）：{title}" + (f"（{reason[:40]}）" if reason else "")
    elif action == "followup":
        note = f"[{event_id}] 後續追蹤（{kind}）：{title}"
    else:
        note = f"[{event_id}] {action}（{kind}）：{title}"

    path = _daily_memory_path(now_dt)
    written = _append_memory_note_once(path, _MEMORY_HEADING, note)
    if not written:
        return None

    ref = _make_memory_ref(event_id, action, path)
    event_store.link_memory(event_id, ref)
    return ref


def process_event_entry_with_memory(
    event_store: "EventStore",
    text: str,
    session_key: str = "",
    channel: str = "direct",
    now_dt: Optional[datetime] = None,
) -> dict:
    """Wrapper around process_event_entry that also writes memory traces.

    Returns the same dict as process_event_entry, with added 'memory_ref' key.
    """
    result = process_event_entry(event_store, text, session_key, channel, now_dt)
    action = result.get("action", "none")
    event = result.get("event")
    memory_ref = None

    if event:
        if action in ("manual_create", "auto_create"):
            memory_ref = write_event_memory_trace(event_store, event, "created", now_dt)
        elif action == "suggest_create":
            pass  # Don't write memory for suggestions — wait for confirm
        elif action == "confirm_suggest":
            memory_ref = write_event_memory_trace(event_store, event, "confirmed", now_dt)
        elif action == "complete":
            memory_ref = write_event_memory_trace(event_store, event, "completed", now_dt)
        elif action == "cancel":
            memory_ref = write_event_memory_trace(event_store, event, "cancelled", now_dt)

    result["memory_ref"] = memory_ref
    return result


# ── CLI ──

def _get_store_path() -> str:
    """Resolve events.json path from environment or default."""
    state_dir = os.environ.get("OPENCLAW_STATE_DIR", DEFAULT_OPENCLAW_STATE_DIR)
    return os.path.join(state_dir, "workspace/personal-hooks/events.json")


def main():
    args = sys.argv[1:]
    if not args:
        print(json.dumps({"error": "usage: event_store.py <command> [args]"}, ensure_ascii=False))
        sys.exit(1)

    cmd = args[0]
    store = EventStore(_get_store_path())

    if cmd == "create":
        params = _parse_kv_args(args[1:])
        evt = store.create(
            event_type=params.get("type", "custom"),
            title=params.get("title", "untitled"),
            cause_summary=params.get("cause", ""),
            desired_followup=params.get("followup", ""),
            priority=params.get("priority", "medium"),
            owner=params.get("owner", "system"),
            source_session=params.get("session", ""),
            source_channel=params.get("channel", ""),
            next_check_at=params.get("next_check", ""),
        )
        print(json.dumps(evt, ensure_ascii=False, indent=2))

    elif cmd == "list":
        statuses = None
        for i, a in enumerate(args[1:], 1):
            if a == "--status" and i + 1 < len(args):
                statuses = args[i + 1].split(",")
        events = store.list_by_status(statuses)
        print(json.dumps({"count": len(events), "events": events}, ensure_ascii=False, indent=2))

    elif cmd == "get":
        eid = _get_flag(args, "--id")
        evt = store.get(eid) if eid else None
        if evt:
            print(json.dumps(evt, ensure_ascii=False, indent=2))
        else:
            print(json.dumps({"error": f"event not found: {eid}"}, ensure_ascii=False))
            sys.exit(1)

    elif cmd == "update":
        eid = _get_flag(args, "--id")
        params = _parse_kv_args(args[1:])
        params.pop("id", None)
        if eid:
            evt = store.update(eid, **params)
            if evt:
                print(json.dumps(evt, ensure_ascii=False, indent=2))
            else:
                print(json.dumps({"error": f"event not found: {eid}"}, ensure_ascii=False))
                sys.exit(1)

    elif cmd == "close":
        eid = _get_flag(args, "--id")
        reason = _get_flag(args, "--reason") or "completed"
        status = _get_flag(args, "--status") or "completed"
        if eid:
            evt = store.close(eid, reason=reason, status=status)
            if evt:
                print(json.dumps(evt, ensure_ascii=False, indent=2))
            else:
                print(json.dumps({"error": f"event not found: {eid}"}, ensure_ascii=False))
                sys.exit(1)

    elif cmd == "due":
        limit = int(_get_flag(args, "--limit") or "5")
        events = store.list_due(limit=limit)
        print(json.dumps({"count": len(events), "events": events}, ensure_ascii=False, indent=2))

    elif cmd == "context":
        limit = int(_get_flag(args, "--limit") or "5")
        prompt = store.build_event_context_prompt(limit=limit)
        print(prompt if prompt else "(no active events)")

    elif cmd == "carryover":
        limit = int(_get_flag(args, "--limit") or "3")
        prompt = store.build_new_session_carryover(limit=limit)
        print(prompt if prompt else "(no unresolved events)")

    elif cmd == "detect":
        text = _get_flag(args, "--text") or ""
        result = detect_event_from_text(text)
        if result:
            print(json.dumps(result, ensure_ascii=False, indent=2))
        else:
            print(json.dumps({"detected": False}, ensure_ascii=False))

    elif cmd == "gc":
        days = int(_get_flag(args, "--days") or "30")
        removed = store.gc(days)
        print(json.dumps({"removed": removed, "remaining": len(store.events)}, ensure_ascii=False))

    elif cmd == "entry":
        text = _get_flag(args, "--text") or ""
        session = _get_flag(args, "--session") or ""
        channel = _get_flag(args, "--channel") or "direct-channel"
        result = process_event_entry(store, text, session_key=session, channel=channel)
        print(json.dumps(result, ensure_ascii=False, indent=2))

    else:
        print(json.dumps({"error": f"unknown command: {cmd}"}, ensure_ascii=False))
        sys.exit(1)


def _get_flag(args: list, flag: str) -> Optional[str]:
    for i, a in enumerate(args):
        if a == flag and i + 1 < len(args):
            return args[i + 1]
    return None


def _parse_kv_args(args: list) -> dict:
    result = {}
    i = 0
    while i < len(args):
        if args[i].startswith("--") and i + 1 < len(args):
            key = args[i][2:].replace("-", "_")
            result[key] = args[i + 1]
            i += 2
        else:
            i += 1
    return result


if __name__ == "__main__":
    main()

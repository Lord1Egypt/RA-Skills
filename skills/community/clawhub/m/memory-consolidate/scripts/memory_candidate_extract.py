#!/usr/bin/env python3
"""Extract V2-lite semantic candidates from rule-processed memory state."""

from __future__ import annotations

import json
import re
from typing import Any, Dict, List, Optional

import memory_consolidate as mc


ACTIVE_ISSUE_SPEC_PREFIXES = [
    "问题：支持",
    "问题：每",
    "问题：hover",
    "问题：删除逻辑",
    "问题：任务最终状态",
    "问题：三种触发场景",
    "问题：三类能力",
    "问题：默认只显示",
    "问题：变更为",
    "问题：deploy 失败策略",
    "问题：自动补齐",
    "问题：display_name",
    "问题：`任意",
]

ACTIVE_ISSUE_DROP_MARKERS = [
    "用户纠正",
    "apply_patch",
    "outside session root",
    "session.delete({ sessionkey })",
    "sessions.delete({ key })",
    "cleanuptasksessions(taskid)",
    "for...of sessionkeys",
    "静态渲染错误",
    "export const dynamic",
    "绿色圆中的白色 dot",
    "dot 看起来偏上",
    "流光",
    "半透明红色线",
    "pulse",
    "title 展示",
    "按模型 + 小时聚合",
    "24 格状态条",
    "hours 参数",
]

ACTIVE_ISSUE_NEGATIVE_MARKERS = [
    "失败",
    "错误",
    "异常",
    "超时",
    "timeout",
    "timed out",
    "报错",
    "无法",
    "不能",
    "消失",
    "抖动",
    "偏上",
    "污染",
    "冲突",
    "抓取失败",
    "internal error",
    "acp_turn_failed",
    "not found",
    "missing",
    "unknown method",
    "null",
    "不兼容",
]

WORKING_PATTERN_DROP_MARKERS = [
    "signals_",
    "工作日 17:30",
    "batch_download.py",
    "daily_scanner.py",
    "deploy 类型 subtask",
    "三类能力",
    "默认只显示 active 项目",
    "workspace_skills",
    "workspace/[slug]/page.tsx",
    "livefeed",
    "继承 openclaw 默认模型",
    "已按中文提交并 push",
    "配置默认模型",
    "覆盖默认模型",
    "同步默认 main workspace",
    "gateways",
    "parallel_group",
    "running 子任务",
    "hours 参数",
    "outside session root",
    "apply_patch",
    "signals_2026-03-04.csv",
    "图片解析默认走",
]

WORKING_PATTERN_KEEP_MARKERS = [
    "先看需求",
    "读代码",
    "最小改动",
    "build",
    "重启验证",
    "乐观规划",
    "异步假设确认",
    "异步确认",
    "重新规划",
    "里程碑验收",
    "阶段都做 build",
    "主聊天",
    "重任务",
    "后台",
    "先 `search --unseen --recent 24h`",
    "fetch <uid>",
    "日报邮件",
    "营销性质邮件",
    "应该先查看项目内的代码",
]

TOP_FACT_ALLOWED_BUCKETS = {"durable_fact", "durable_preference", "stable_rule"}
TOP_FACT_IMPLEMENTATION_MARKERS = [
    "docs/",
    "src/",
    "route.ts",
    "page.tsx",
    "curl ",
    "commit ",
    "api/",
    "workspace_skills",
    "数据库表名",
    "session:",
    "codex session",
    "需求文档",
    "review 保留",
    "创建任务表单",
    "tab 标题",
    "promptly",
    "soUL.md".lower(),
    "memory_consolidate.py",
    "active_total",
    "archive_ratio",
    "signal_noise_ratio",
    "issue_count",
]
TOP_FACT_ONE_OFF_MARKERS = [
    "本轮手动收敛",
    "当前判断",
    "后续追加",
    "原需求",
    "修正（",
    "创建任务表单",
    "review 保留",
    "浏览器 tab 标题",
]
TOP_FACT_PREFERENCE_MARKERS = [
    "标题偏好",
    "标题统一使用中文",
    "更适合给",
    "更适合用",
    "优先使用",
    "沟通偏好",
]
TOP_FACT_RULE_MARKERS = [
    "明确要求",
    "不要让他来提醒",
    "长任务结束后",
    "术语统一",
    "英文统一用 capability",
    "中文用\"能力\"",
    "中文用“能力”",
]
TOP_FACT_DURABLE_MARKERS = [
    "跑两天再评估",
    "已安装技能",
]

SOLUTION_DROP_MARKERS = [
    "已在 `src/",
    "修复文件：",
    "page.tsx",
    "route.ts",
    "executionflow",
    "按钮",
    "颜色",
    "样式",
    "suspense",
    "type assertion",
    "build 错误",
    "build + deploy",
    "服务已重启",
    "手动触发",
    "手动重置状态",
    "现在是 running",
    "codex 已经在修了",
    "先深入看一下",
    "你的需求是",
    "promptly",
    "tab 标题",
]
SOLUTION_STRATEGY_PRIORITY = {
    "memory_denoise": 90,
    "replan_cleanup": 80,
    "deliverables_normalization": 72,
    "deliverables_render": 70,
    "skill_over_type": 62,
    "calendar_explicit_date": 58,
    "calendar_scope_consistency": 56,
}

RECENT_DROP_MARKERS = [
    "文档变更:",
    "需求文档：",
    "修复文件：",
    "文件：",
    "任务清单位置：",
    "commit ",
    "curl ",
    "openclaw ",
    "python ",
    "python3 ",
    "node ",
    "npm ",
    "systemctl ",
    "build + deploy",
    "构建",
    "部署",
    "docs/",
    "src/",
    "route.ts",
    "page.tsx",
    "signals_",
    "工作日 17:30",
    "batch_download.py",
    "daily_scanner.py",
]
RECENT_KIND_PRIORITY = {
    "key_fix": 90,
    "confirmed_problem": 82,
    "rule_change": 74,
    "system_status": 66,
}


def _row_time(row: Dict[str, Any]) -> str:
    return str(row.get("last_seen_at") or row.get("updated_at") or "")


def _row_weight(row: Dict[str, Any]) -> float:
    return float(row.get("temperature") or row.get("weight") or 0.0)


def _row_occ(row: Dict[str, Any]) -> int:
    return int(row.get("occurrences") or 1)


def _copy_row(row: Dict[str, Any], **updates: Any) -> Dict[str, Any]:
    copied = dict(row)
    copied.update(updates)
    return copied


def _norm_key(text: str) -> str:
    return mc.normalize_for_match(mc.normalize_content(text))


def _item_from_row(section: str, rank: int, row: Dict[str, Any]) -> Dict[str, Any]:
    item = {
        "candidate_id": f"{section}:{row.get('id') or mc.make_id('fact', str(row.get('content') or ''))}",
        "section": section,
        "rank": rank,
        "text": mc.render_row_content(row) or mc.normalize_content(str(row.get("content") or "")),
        "source_kind": row.get("kind"),
        "source_id": row.get("id"),
        "event_type": row.get("event_type"),
        "source_type": row.get("source_type"),
        "pattern_key": row.get("pattern_key"),
        "temperature": row.get("temperature"),
        "temperature_bucket": row.get("temperature_bucket"),
        "importance": row.get("importance"),
        "priority_score": row.get("priority_score"),
        "occurrences": row.get("occurrences"),
        "recent_refs": row.get("recent_refs"),
        "last_seen_at": row.get("last_seen_at"),
        "updated_at": row.get("updated_at"),
        "tags": row.get("tags") or [],
        "sources": row.get("sources") or ([row.get("source")] if row.get("source") else []),
    }
    for extra_key in ["top_fact_bucket", "solution_strategy", "recent_kind"]:
        if row.get(extra_key) is not None:
            item[extra_key] = row.get(extra_key)
    return item


def _item_from_text(section: str, rank: int, text: str, *, extra: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    normalized = mc.normalize_content(text)
    item = {
        "candidate_id": f"{section}:{mc.make_id('fact', normalized)}",
        "section": section,
        "rank": rank,
        "text": normalized,
        "source_kind": "recent_line",
        "source_id": None,
        "event_type": None,
        "source_type": "recent_line",
        "pattern_key": None,
        "temperature": None,
        "temperature_bucket": None,
        "importance": None,
        "priority_score": None,
        "occurrences": 1,
        "recent_refs": 0,
        "last_seen_at": None,
        "updated_at": None,
        "tags": [],
        "sources": [],
    }
    if extra:
        item.update(extra)
    return item


def _issue_sort_key(row: Dict[str, Any]) -> tuple:
    return (
        int(row.get("occurrences") or 1),
        int(row.get("recent_refs") or 0),
        float(row.get("temperature") or row.get("weight") or 0.0),
        str(row.get("last_seen_at") or row.get("updated_at") or ""),
        float(row.get("importance") or 0.0),
    )


def _pattern_sort_key(row: Dict[str, Any]) -> tuple:
    text = mc.normalize_content(str(row.get("content") or ""))
    return (
        int(any(marker in text for marker in ["先看需求", "乐观规划", "异步确认", "build", "主聊天", "后台"])),
        int(row.get("occurrences") or 1),
        int(row.get("recent_refs") or 0),
        float(row.get("temperature") or row.get("weight") or 0.0),
        str(row.get("last_seen_at") or row.get("updated_at") or ""),
        float(row.get("importance") or 0.0),
    )


def _top_fact_user_signal(text: str) -> int:
    return int(any(marker in text for marker in ["标题偏好", "长任务结束后", "capability", "沟通偏好", "明确要求"]))


def _classify_top_fact_bucket(text: str) -> Optional[str]:
    s = mc.normalize_content(text)
    lower = s.lower()
    if not s or mc.is_low_signal_line(s) or mc.is_request_or_discussion_line(s):
        return None
    if len(s) < 14:
        return None
    if s.endswith(("：", ":")):
        return None
    if "跑两天再评估" in s or "memory consolidation" in lower:
        return "durable_fact"
    if "已安装技能" in s and "humanizer-zh" in lower:
        return "durable_fact"
    if any(marker in s for marker in TOP_FACT_PREFERENCE_MARKERS):
        return "durable_preference"
    if any(marker in s for marker in TOP_FACT_RULE_MARKERS):
        return "stable_rule"
    if mc.is_path_like_text(s):
        return "implementation_detail"
    if s.startswith(("问题：", "方案：", "工作模式：", "需求文档：", "修复文件：", "文件：", "包含", "原需求：", "后续追加：")):
        return "implementation_detail"
    if re.match(r"^\d+[.)、]\s*", s):
        return "one_off_request"
    if any(marker in lower for marker in TOP_FACT_IMPLEMENTATION_MARKERS):
        return "implementation_detail"
    if any(marker in s for marker in TOP_FACT_ONE_OFF_MARKERS):
        return "one_off_request"
    if any(marker in s for marker in TOP_FACT_DURABLE_MARKERS):
        return "durable_fact"
    return None


def _top_fact_sort_key(row: Dict[str, Any]) -> tuple:
    bucket = str(row.get("top_fact_bucket") or "")
    bucket_priority = {"durable_preference": 3, "stable_rule": 2, "durable_fact": 1}.get(bucket, 0)
    text = mc.normalize_content(str(row.get("content") or row.get("text") or ""))
    return (
        bucket_priority,
        _top_fact_user_signal(text),
        int(row.get("recent_refs") or 0),
        _row_occ(row),
        _row_weight(row),
        _row_time(row),
    )


def _select_top_fact_candidates(facts: List[Dict[str, Any]], events: List[Dict[str, Any]], limit: int) -> List[Dict[str, Any]]:
    pool: List[Dict[str, Any]] = []
    for row in facts:
        text = mc.normalize_content(str(row.get("content") or ""))
        bucket = _classify_top_fact_bucket(text)
        if bucket in TOP_FACT_ALLOWED_BUCKETS:
            pool.append(_copy_row(row, top_fact_bucket=bucket))
    for row in events:
        if str(row.get("event_type") or "") != "decision":
            continue
        text = mc.normalize_content(str(row.get("content") or ""))
        bucket = _classify_top_fact_bucket(text)
        if bucket in TOP_FACT_ALLOWED_BUCKETS:
            pool.append(_copy_row(row, top_fact_bucket=bucket))

    pool = sorted(pool, key=_top_fact_sort_key, reverse=True)

    seen: set[str] = set()
    out: List[Dict[str, Any]] = []
    for row in pool:
        key = _norm_key(str(row.get("content") or row.get("text") or ""))
        if not key or key in seen:
            continue
        seen.add(key)
        out.append(row)
        if len(out) >= limit:
            break
    return out


def _classify_solution_strategy(text: str) -> Optional[str]:
    s = mc.normalize_content(text)
    lower = s.lower()
    if not s or mc.is_request_or_discussion_line(s):
        return None
    if mc.is_path_like_text(s):
        return None
    if any(marker in lower for marker in SOLUTION_DROP_MARKERS):
        return None
    if any(k in lower for k in ["goals / facts / issues", "signal_noise_ratio", "施工日志", "伪 issue"]):
        return "memory_denoise"
    if any(k in lower for k in ["running/in_progress/dispatched/pending", "subtask_runs", "cleanupTaskSessions".lower()]):
        return "replan_cleanup"
    if "保留已完成" in s and "subtasks" in lower:
        return "replan_cleanup"
    if "deliverables" in lower and any(k in lower for k in ["对象数组", "react 子节点", "name 或 path", "可显示字段"]):
        return "deliverables_render"
    if "deliverables" in lower and any(k in lower for k in ["路径补全", "绝对路径去重", "upsert", "相对路径"]):
        return "deliverables_normalization"
    if "日历" in s and "date" in lower:
        return "calendar_explicit_date"
    if "scope" in lower and "calendar" in lower:
        return "calendar_scope_consistency"
    if "项目级 skill" in s or "不拆多个 type" in s:
        return "skill_over_type"
    return None


def _solution_sort_key(row: Dict[str, Any]) -> tuple:
    strategy = str(row.get("solution_strategy") or "")
    return (
        SOLUTION_STRATEGY_PRIORITY.get(strategy, 0),
        _row_time(row),
        _row_occ(row),
        _row_weight(row),
    )


def _select_chosen_solution_candidates(events: List[Dict[str, Any]], limit: int) -> List[Dict[str, Any]]:
    pool: List[Dict[str, Any]] = []
    for row in mc.top_events(events, "solution", max(80, limit * 20)):
        text = mc.normalize_content(str(row.get("content") or ""))
        strategy = _classify_solution_strategy(text)
        if not strategy:
            continue
        pool.append(_copy_row(row, solution_strategy=strategy))

    pool = sorted(pool, key=_solution_sort_key, reverse=True)

    seen: set[str] = set()
    out: List[Dict[str, Any]] = []
    for row in pool:
        key = _norm_key(str(row.get("content") or row.get("text") or ""))
        if not key or key in seen:
            continue
        seen.add(key)
        out.append(row)
        if len(out) >= limit:
            break
    return out


def _is_probably_real_issue(row: Dict[str, Any]) -> bool:
    text = mc.normalize_content(str(row.get("content") or ""))
    lower = text.lower()
    if not text or str(row.get("event_type") or "") != "issue":
        return False
    if mc.is_questionish_line(text) or mc.is_request_or_discussion_line(text) or mc.is_non_issue_progress_line(text):
        return False
    if mc.is_display_noise_issue_line(text):
        return False
    if any(text.startswith(prefix) for prefix in ACTIVE_ISSUE_SPEC_PREFIXES):
        return False
    if any(marker in lower for marker in ACTIVE_ISSUE_DROP_MARKERS):
        return False
    if any(marker in text for marker in ["问题：但发现问题", "问题：优化错误信息", "问题：改进错误处理"]):
        return False
    if int(row.get("occurrences") or 1) >= 2:
        return True
    return any(marker in lower for marker in ACTIVE_ISSUE_NEGATIVE_MARKERS)


def _select_active_issue_candidates(events: List[Dict[str, Any]], limit: int) -> List[Dict[str, Any]]:
    rows = [row for row in events if _is_probably_real_issue(row)]
    rows = sorted(rows, key=_issue_sort_key, reverse=True)

    seen: set[str] = set()
    out: List[Dict[str, Any]] = []
    for row in rows:
        text = mc.normalize_content(str(row.get("content") or ""))
        key = mc.normalize_for_match(text)
        if not key or key in seen:
            continue
        seen.add(key)
        out.append(row)
        if len(out) >= limit:
            break
    return out


def _is_working_pattern_candidate(text: str) -> bool:
    normalized = mc.normalize_content(text)
    lower = normalized.lower()
    if not normalized:
        return False
    if normalized.startswith("工作模式：实现完整："):
        return False
    if any(marker in lower for marker in WORKING_PATTERN_DROP_MARKERS):
        return False
    if mc.is_path_like_text(normalized):
        return False
    return any(marker in normalized for marker in WORKING_PATTERN_KEEP_MARKERS)


def _select_working_pattern_candidates(
    summaries: List[Dict[str, Any]],
    events: List[Dict[str, Any]],
    recent_lines: List[str],
    limit: int,
) -> List[Dict[str, Any]]:
    rows: List[Dict[str, Any]] = []
    for row in summaries:
        tags = set(row.get("tags") or [])
        if not ({"working_pattern", "best_practice", "correction"} & tags):
            continue
        text = mc.normalize_content(str(row.get("content") or ""))
        if _is_working_pattern_candidate(text):
            rows.append(row)

    for row in events:
        if str(row.get("event_type") or "") not in {"decision", "progress"}:
            continue
        text = mc.normalize_content(str(row.get("content") or ""))
        if _is_working_pattern_candidate(text):
            rows.append(row)

    rows = sorted(rows, key=_pattern_sort_key, reverse=True)

    seen: set[str] = set()
    out: List[Dict[str, Any]] = []
    for row in rows:
        text = mc.normalize_content(str(row.get("content") or ""))
        key = mc.normalize_for_match(text)
        if not key or key in seen:
            continue
        seen.add(key)
        out.append(row)
        if len(out) >= max(0, limit - 2):
            break

    for text in recent_lines:
        normalized = mc.normalize_content(text)
        if not _is_working_pattern_candidate(normalized):
            continue
        key = mc.normalize_for_match(normalized)
        if not key or key in seen:
            continue
        seen.add(key)
        out.append({"kind": "recent_line", "content": normalized})
        if len(out) >= limit:
            break

    return out[:limit]


def _is_recent_noise_text(text: str) -> bool:
    s = mc.normalize_content(text)
    lower = s.lower()
    if not s:
        return True
    if mc.is_path_like_text(s):
        return True
    if any(marker in lower for marker in RECENT_DROP_MARKERS):
        return True
    return False


def _classify_recent_event_kind(row: Dict[str, Any]) -> Optional[str]:
    text = mc.normalize_content(str(row.get("content") or ""))
    lower = text.lower()
    if _is_recent_noise_text(text):
        return None

    event_type = str(row.get("event_type") or "")
    strategy = _classify_solution_strategy(text)

    if event_type == "solution" and strategy in {"memory_denoise", "replan_cleanup"}:
        return "key_fix"
    if event_type == "issue" and _is_probably_real_issue(row):
        if any(marker in lower for marker in ["gateway timeout", "acp_turn_failed", "internal error", "timeout=7200", "进程消失"]):
            return "confirmed_problem"
        return None
    if event_type == "decision" and any(marker in text for marker in ["主聊天", "普通频道", "后台"]):
        return "rule_change"
    if event_type == "progress":
        if text.startswith("系统状态:") or "可以测试" in text or ("热重载" in text and "gateway" in lower):
            return "system_status"
        if any(marker in text for marker in ["失败摘要", "保留已完成"]):
            return "key_fix"
    return None


def _classify_recent_line_kind(text: str) -> Optional[str]:
    s = mc.normalize_content(text)
    lower = s.lower()
    if _is_recent_noise_text(s):
        return None
    if any(marker in s for marker in ["根因", "定位到根因", "保留已完成", "失败摘要"]):
        return "key_fix"
    if any(marker in s for marker in ["主聊天", "普通频道", "后台"]):
        return "rule_change"
    if "可以测试" in s or ("热重载" in s and "gateway" in lower) or "无需重启 gateway" in lower:
        return "system_status"
    if any(marker in s for marker in ["确认", "问题", "超时", "报错"]) and "需求" not in s:
        return "confirmed_problem"
    return None


def _recent_sort_key(row: Dict[str, Any]) -> tuple:
    kind = str(row.get("recent_kind") or "")
    return (
        RECENT_KIND_PRIORITY.get(kind, 0),
        _row_time(row),
        _row_occ(row),
        _row_weight(row),
    )


def _select_recent_candidates(events: List[Dict[str, Any]], recent_lines: List[str], limit: int) -> List[Dict[str, Any]]:
    event_pool: List[Dict[str, Any]] = []
    for row in events:
        kind = _classify_recent_event_kind(row)
        if not kind:
            continue
        strategy = _classify_solution_strategy(mc.normalize_content(str(row.get("content") or "")))
        event_pool.append(_copy_row(row, recent_kind=kind, solution_strategy=strategy))

    event_pool = sorted(event_pool, key=_recent_sort_key, reverse=True)

    seen: set[str] = set()
    out: List[Dict[str, Any]] = []
    event_cap = 3
    for row in event_pool:
        text = mc.normalize_content(str(row.get("content") or ""))
        key = _norm_key(text)
        if not key or key in seen:
            continue
        seen.add(key)
        out.append(row)
        if len(out) >= min(event_cap, limit):
            break

    for text in reversed(recent_lines):
        kind = _classify_recent_line_kind(text)
        if not kind:
            continue
        normalized = mc.normalize_content(text)
        key = _norm_key(normalized)
        if not key or key in seen:
            continue
        seen.add(key)
        out.append({"kind": "recent_line", "content": normalized, "recent_kind": kind})
        if len(out) >= limit:
            break

    return out[:limit]


def build_candidate_payload() -> Dict[str, Any]:
    cfg = mc.load_config()
    snap_cfg = cfg.get("snapshot") or {}
    recent_days = int(snap_cfg.get("recent_days", 3))

    facts = mc.prune_noisy_facts(mc.apply_pattern_metadata(mc.merge_rows_by_identity(mc.read_jsonl(mc.FACTS_PATH))))
    summaries = mc.apply_pattern_metadata(mc.merge_rows_by_identity(mc.read_jsonl(mc.SUMMARIES_PATH)))
    events = mc.prune_noisy_issue_events(mc.apply_pattern_metadata(mc.merge_rows_by_identity(mc.read_jsonl(mc.EVENTS_PATH))))
    all_logs = mc.list_daily_logs()
    recent_lines = mc.collect_recent_lines(all_logs[-recent_days:] if all_logs else [], max_lines=18)

    top_facts = _select_top_fact_candidates(facts, events, limit=14)
    chosen_solutions = _select_chosen_solution_candidates(events, limit=14)
    recent = _select_recent_candidates(events, recent_lines, limit=12)
    active_issues = _select_active_issue_candidates(events, limit=14)
    working_patterns = _select_working_pattern_candidates(summaries, events, recent_lines, limit=14)

    payload: Dict[str, Any] = {
        "schema": "memory.candidates.v2-lite",
        "generated_at": mc.utc_now_iso(),
        "source_layer": "rule-engine",
        "inputs": {
            "facts": str(mc.FACTS_PATH),
            "summaries": str(mc.SUMMARIES_PATH),
            "events": str(mc.EVENTS_PATH),
            "snapshot": str(mc.SNAPSHOT_PATH),
        },
        "sections": {
            "top_facts": [_item_from_row("top_facts", idx + 1, row) for idx, row in enumerate(top_facts)],
            "chosen_solutions": [_item_from_row("chosen_solutions", idx + 1, row) for idx, row in enumerate(chosen_solutions)],
            "recent": [
                _item_from_text("recent", idx + 1, str(row.get("content") or ""), extra={"recent_kind": row.get("recent_kind")})
                if str(row.get("kind") or "") == "recent_line"
                else _item_from_row("recent", idx + 1, row)
                for idx, row in enumerate(recent)
            ],
            "active_issues": [_item_from_row("active_issues", idx + 1, row) for idx, row in enumerate(active_issues)],
            "working_patterns": [
                _item_from_text("working_patterns", idx + 1, str(row.get("content") or ""))
                if str(row.get("kind") or "") == "recent_line"
                else _item_from_row("working_patterns", idx + 1, row)
                for idx, row in enumerate(working_patterns)
            ],
        },
        "counts": {
            "top_facts": len(top_facts),
            "chosen_solutions": len(chosen_solutions),
            "recent": len(recent),
            "active_issues": len(active_issues),
            "working_patterns": len(working_patterns),
        },
    }
    return payload


def main() -> int:
    payload = build_candidate_payload()
    mc.CANDIDATES_DIR.mkdir(parents=True, exist_ok=True)

    latest_path = mc.CANDIDATE_LATEST_PATH
    stamp = payload["generated_at"].replace(":", "").replace("-", "")
    history_path = mc.CANDIDATES_DIR / f"candidates-{stamp}.json"

    text = json.dumps(payload, ensure_ascii=False, indent=2) + "\n"
    latest_path.write_text(text, "utf-8")
    history_path.write_text(text, "utf-8")

    print(str(latest_path))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

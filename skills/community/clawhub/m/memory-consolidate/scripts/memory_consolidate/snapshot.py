"""Snapshot generation: select, filter, and render MEMORY_SNAPSHOT.md."""

from __future__ import annotations

import re
from typing import Any, Dict, List, Optional

from .core import (
    normalize_content,
    normalize_for_match,
    is_path_like_text,
    render_row_content,
)
from .ingest import (
    is_low_signal_line,
    is_questionish_line,
    is_non_issue_progress_line,
    is_request_or_discussion_line,
    STRONG_ISSUE_KEYWORDS,
)


def top_n(rows: List[Dict[str, Any]], n: int) -> List[Dict[str, Any]]:
    return sorted(rows, key=lambda r: float(r.get("weight") or 0.0), reverse=True)[:n]


def top_events(events: List[Dict[str, Any]], event_type: str, n: int) -> List[Dict[str, Any]]:
    rows = [e for e in events if str(e.get("event_type") or "") == event_type]
    return top_n(rows, n)


def is_display_noise_issue_line(text: str) -> bool:
    s = normalize_content(text)
    lower = s.lower()
    if not s:
        return True
    if s.startswith(("问题：✅", "问题：🔄", "问题：实现完整：")):
        return True
    if re.match(r"^问题：\d+[.)、]\s*", s):
        return True
    if re.match(r"^问题：[A-Za-z_][A-Za-z0-9_]*:\s*", s):
        return True
    noisy_markers = [
        "commit ", "单元测试", "让codex实现", "hover只显示", "ppt", "商业计划书", "worker两类agent",
        "现在的任务流程", "哪些环节", "加一页内容", "写一篇架构演化", "追加的刚才的codex",
        "提出并关注", "落地要点", "结构化 trace", "灰度发布", "自动回滚", "原生方案框架",
        "看一下问题所在", "分析一下", "最终结果", "总耗时", "同一任务超时时间已从",
        "建议：", "重跑时设置更长超时", "执行完成", "验证通过", "已将对应 cron", "timeoutseconds=",
        "route.ts", "subtask completed 后统计 pending/completed/total", "deliverable split:", "超时时间:",
        "优化错误处理", "runtimeoutseconds:", "增加超时时间", "**原因**:",
    ]
    return any(m in lower for m in noisy_markers)


def select_real_issues(events: List[Dict[str, Any]], n: int) -> List[Dict[str, Any]]:
    rows = [
        e for e in events
        if str(e.get("event_type") or "") == "issue"
        and not is_questionish_line(str(e.get("content") or ""))
        and not is_non_issue_progress_line(str(e.get("content") or ""))
        and not is_request_or_discussion_line(str(e.get("content") or ""))
        and not is_display_noise_issue_line(str(e.get("content") or ""))
        and (
            bool(e.get("pattern_key"))
            or any(k in str(e.get("content") or "").lower() for k in STRONG_ISSUE_KEYWORDS)
        )
    ]
    return top_n(rows, n) if rows else []


def select_recurring_problems(events: List[Dict[str, Any]], n: int) -> List[Dict[str, Any]]:
    rows = [
        e for e in select_real_issues(events, max(50, n * 10))
        if (
            int(e.get("occurrences") or 1) >= 2
            or int(e.get("recent_refs") or 0) >= 2
            or bool(e.get("pattern_key"))
        )
    ]
    return top_n(rows, n) if rows else []


def select_working_patterns(summaries: List[Dict[str, Any]], n: int) -> List[Dict[str, Any]]:
    rows = [
        s for s in summaries
        if (
            bool(s.get("pattern_key"))
            or "working_pattern" in (s.get("tags") or [])
            or "best_practice" in (s.get("tags") or [])
            or "correction" in (s.get("tags") or [])
        )
        and not normalize_content(str(s.get("content") or "")).startswith("工作模式：实现完整：")
    ]
    return top_n(rows, n) if rows else []


def is_goal_noise_line(text: str) -> bool:
    s = normalize_content(text)
    lower = s.lower()
    if not s:
        return True
    if s.startswith(("工作模式：", "修正：", "需求文档：", "文件：", "任务清单位置：", "今日文档变更:")):
        return True
    noisy_markers = [
        "我验证一下", "然后提交", "search --unseen", "fetch <uid>", "默认过滤", "systemctl", "npm run build",
        "docs/", "src/", "route.ts", "page.tsx",
    ]
    return any(m.lower() in lower for m in noisy_markers)


def select_goal_summaries(summaries: List[Dict[str, Any]], n: int) -> List[Dict[str, Any]]:
    rows = []
    for s in top_n(summaries, max(12, n * 3)):
        content = normalize_content(str(s.get("content") or ""))
        tags = set(s.get("tags") or [])
        if not content or is_goal_noise_line(content):
            continue
        if "working_pattern" in tags or "best_practice" in tags or "correction" in tags:
            continue
        rows.append(s)
        if len(rows) >= n:
            break
    return rows


def is_solution_noise_line(text: str) -> bool:
    s = normalize_content(text)
    lower = s.lower()
    if not s:
        return True
    if s in {"方案：", "修复：", "解决："}:
        return True
    if s.startswith(("方案：bug：", "方案：需求文档：", "方案：文件：", "方案：修复文件：")):
        return True
    noisy_markers = [
        "docs/", "src/", "route.ts", "page.tsx", "追加的刚才的codex", "看一下问题所在", "是什么 一个",
        "分析一下", "你的需求是", "已经在修了", "先深入看一下", "推荐）", "两个设计", "三种设计",
        "手动重置状态", "现在是 running", "之前的 pending 是因为",
    ]
    return any(m.lower() in lower for m in noisy_markers)


def is_concrete_solution_line(text: str) -> bool:
    s = normalize_content(text)
    return any(
        marker in s
        for marker in [
            "改为", "改成", "新增", "增加", "修复", "清理", "取消", "统一", "补上", "拆成",
            "先查并", "保留已完成", "重置为", "落地", "触发", "补齐", "切到", "移到",
        ]
    )


def select_real_solutions(events: List[Dict[str, Any]], n: int) -> List[Dict[str, Any]]:
    rows = []
    for e in top_events(events, "solution", max(30, n * 6)):
        content = normalize_content(str(e.get("content") or ""))
        if not content or is_solution_noise_line(content):
            continue
        if not is_concrete_solution_line(content):
            continue
        rows.append(e)
        if len(rows) >= n:
            break
    return rows


def is_high_level_fact_line(text: str) -> bool:
    c = normalize_content(text)
    lower = c.lower()
    if not c or is_low_signal_line(c) or is_path_like_text(c):
        return False
    if c.startswith(("问题：", "方案：", "工作模式：", "需求文档：", "修复文件：", "文件：", "包含", "原需求：", "后续追加：", "保持绝对路径")):
        return False
    if is_request_or_discussion_line(c):
        return False
    if len(c) < 16:
        return False
    if "`" in c and "标题偏好" not in c:
        return False
    if any(sym in c for sym in ["{", "}", "=>"]):
        return False

    exclude_kw = [
        "构建成功", "已 build", "systemctl", "重启", "commit", "push", "src/components", "route.ts", "page.tsx",
        "openclaw agents add", "参考项目", "参考:", "检测", "stopreason", "workspace-scoped", "work:",
        "mission control (next.js)", "openclaw gateway", "文件：", "需求文档：", "修复文件：", "今日文档变更:",
        "任务清单位置:", "callback/", "task_deliverables", "subtasks.deliverables", "finaldeliverables", "upsert",
        "requestid", "running/in_progress/dispatched/pending", "当前为 `in_progress`", "绝对路径去重", "runtime:",
        "agentid:", "thread:", "cwd:", "本地绑定路径", "clone 仓库到", "worker via codex", "git@", "路径基准",
        "相对路径补全逻辑", "memory_consolidate.py", "archive", "deliverable", "google_calendar_device_auth.py",
        "包含", "原需求", "后续追加", "ops 模型监控", "tab风格", "gateway按钮", "执行引擎改进",
    ]
    if any(k in lower for k in exclude_kw):
        return False
    if any(k in c for k in ["按文档", "按需求文档", "已按需求文档", "已完成需求文档", "依据 `docs/", "依据 docs/"]):
        return False

    include_kw = [
        "偏好", "要求", "默认", "统一", "命名", "策略", "架构", "能力", "模型", "时区", "定时任务",
        "执行顺序", "工作日", "目标", "流程", "分流", "中文", "标题", "Docker", "内存限制", "跑两天再评估",
    ]
    return any(k in c for k in include_kw)


def select_strategic_facts(facts: List[Dict[str, Any]], n: int) -> List[Dict[str, Any]]:
    ranked = sorted(facts, key=lambda r: float(r.get("weight") or 0.0), reverse=True)
    selected: List[Dict[str, Any]] = []
    seen_norm: set = set()

    def norm(text: str) -> str:
        return re.sub(r"[^\w\u4e00-\u9fff]+", "", text.lower())

    for row in ranked:
        c = str(row.get("content") or "").strip()
        if not is_high_level_fact_line(c):
            continue
        key = norm(c)
        if not key or key in seen_norm:
            continue
        seen_norm.add(key)
        selected.append(row)
        if len(selected) >= n:
            break

    return selected[:n]


def bullets_from_rows(rows: List[Dict[str, Any]], *, allow_path_like: bool = True) -> str:
    out: List[str] = []
    seen: set = set()
    for r in rows:
        c = render_row_content(r)
        if not c:
            continue
        if is_low_signal_line(c):
            continue
        if re.match(r"^\d+\.\s", c):
            continue
        if c.startswith("```"):
            continue
        if (not allow_path_like) and is_path_like_text(c):
            continue
        key = normalize_for_match(c)
        if not key or key in seen:
            continue
        seen.add(key)
        out.append(f"- {c}")
    return "\n".join(out) if out else "-"


def bullets_from_text(items: List[str], *, allow_path_like: bool = True) -> str:
    out: List[str] = []
    seen: set = set()
    for raw in items:
        text = normalize_content(str(raw or ""))
        if not text:
            continue
        if (not allow_path_like) and is_path_like_text(text):
            continue
        key = normalize_for_match(text)
        if not key or key in seen:
            continue
        seen.add(key)
        out.append(f"- {text}")
    return "\n".join(out) if out else "-"


def generate_snapshot(
    facts: List[Dict[str, Any]],
    beliefs: List[Dict[str, Any]],
    summaries: List[Dict[str, Any]],
    events: List[Dict[str, Any]],
    recent_lines: List[str],
    max_chars: int,
    limits: Dict[str, int],
    identity: Optional[Dict[str, Any]] = None,
    memory_health: Optional[Dict[str, Any]] = None,
) -> str:
    top_f = select_strategic_facts(facts, min(int(limits.get("top_facts", 8)), 8))
    top_b = top_n(beliefs, limits.get("top_beliefs", 6))
    top_s = top_n(summaries, limits.get("top_summaries", 6))
    top_d = top_events(events, "decision", limits.get("top_decisions", 6))
    top_i = select_real_issues(events, limits.get("top_issues", 5))
    top_sol = select_real_solutions(events, limits.get("top_solutions", 5))
    top_art = top_events(events, "artifact", limits.get("top_artifacts", 8))
    recurring_problems = select_recurring_problems(events, min(5, limits.get("top_issues", 5)))
    working_patterns = select_working_patterns(summaries, min(5, limits.get("top_summaries", 6)))
    goal_summaries = select_goal_summaries(summaries, 3)

    goals: List[str] = []
    for s in goal_summaries:
        c = str(s.get("content") or "").strip()
        if c:
            goals.append(c)

    mh = memory_health or {}
    memory_health_lines = [
        f"活跃条目: {int(mh.get('active_total', 0))} | 归档条目: {int(mh.get('archived_total', 0))} | 归档率: {round(float(mh.get('archive_ratio', 0.0)) * 100, 1)}%",
        f"温度分布: hot {int(mh.get('hot', 0))} / warm {int(mh.get('warm', 0))} / cold {int(mh.get('cold', 0))}",
        f"本轮强化: {int(mh.get('reinforced_count', 0))} 条 | 归档回流: {int(mh.get('distilled_count', 0))} 条",
        f"信噪比(有效/噪声): {round(float(mh.get('signal_noise_ratio', 0.0)), 3)}",
        f"问题/方案/修正/模式: {int(mh.get('issue_count', 0))} / {int(mh.get('solution_count', 0))} / {int(mh.get('correction_count', 0))} / {int(mh.get('pattern_summary_count', 0))}",
    ]

    # Identity from config (not hardcoded)
    id_info = identity or {}
    assistant_name = str(id_info.get("assistant_name") or "Assistant")
    owner_name = str(id_info.get("owner_name") or "User")
    owner_display = str(id_info.get("owner_display_name") or owner_name)
    owner_lang = str(id_info.get("owner_language") or "")
    owner_tz = str(id_info.get("owner_timezone") or "")

    owner_lines = [f"- User: {owner_display}"]
    if owner_lang:
        owner_lines.append(f"- Prefers: {owner_lang}")
    if owner_tz:
        owner_lines.append(f"- Timezone: {owner_tz}")

    text = (
        "# MEMORY_SNAPSHOT.md\n\n"
        "This is the injected working-memory snapshot. Keep it short and high-signal.\n\n"
        "## Identity\n"
        f"- Assistant: {assistant_name}\n\n"
        "## Owner\n"
        + "\n".join(owner_lines) + "\n\n"
        "## Current Goals\n"
        f"{bullets_from_text(goals)}\n\n"
        "## Key Decisions\n"
        f"{bullets_from_rows(top_d)}\n\n"
        "## Active Issues\n"
        f"{bullets_from_rows(top_i)}\n\n"
        "## Recurring Problems\n"
        f"{bullets_from_rows(recurring_problems)}\n\n"
        "## Chosen Solutions\n"
        f"{bullets_from_rows(top_sol)}\n\n"
        "## Working Patterns\n"
        f"{bullets_from_rows(working_patterns, allow_path_like=False)}\n\n"
        "## Artifact Index\n"
        f"{bullets_from_rows(top_art)}\n\n"
        "## Memory Health\n"
        f"{bullets_from_text(memory_health_lines)}\n\n"
        "## Top Facts\n"
        f"{bullets_from_rows(top_f, allow_path_like=False)}\n\n"
        "## Beliefs (uncertain)\n"
        f"{bullets_from_rows(top_b)}\n\n"
        "## Recent\n"
        f"{bullets_from_text(recent_lines[-8:])}\n"
    )

    if len(text) > max_chars:
        text = text[: max_chars - 20] + "\n\n(truncated)\n"
    return text

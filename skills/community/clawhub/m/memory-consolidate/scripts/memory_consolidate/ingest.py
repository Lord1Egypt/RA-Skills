"""Log parsing: extract lines, classify events, build learning items.

All pattern lists live here. Bilingual (Chinese + English).
"""

from __future__ import annotations

import re
from typing import Any, Dict, List, Optional, Tuple

from . import core
from .config import get_tag_rules

# ---------------------------------------------------------------------------
# Noise markers (bilingual)
# ---------------------------------------------------------------------------
NOISE_MARKERS = [
    "429", "too many requests", "high traffic",
    # Chinese
    "继续", "看看", "嗨", "test", "构建成功", "修复已完成", "测试构建", "早上好", "没问题", "ok", "heartbeart_ok",
    # English
    "continue", "let me see", "hi", "build succeeded", "fix completed", "test build",
    "good morning", "no problem", "sounds good",
]

# ---------------------------------------------------------------------------
# Issue patterns (bilingual)
# ---------------------------------------------------------------------------
ISSUE_PREFIX_PATTERNS = [
    # Chinese
    r"^问题[:：]", r"^报错[:：]", r"^错误[:：]", r"^失败[:：]", r"^异常[:：]",
    r"^超时[:：]", r"^卡死[:：]", r"^阻塞[:：]", r"^首次.*失败[:：]", r"^网关超时[:：]",
    r"^无法", r"^不能",
    # English
    r"^issue[:：]", r"^error[:：]", r"^bug[:：]", r"^failed[:：]", r"^timeout[:：]",
    r"^blocked[:：]", r"^cannot ", r"^unable to ",
]

ISSUE_KEYWORDS = [
    # Chinese
    "问题", "失败", "错误", "异常", "报错", "超时", "卡死", "阻塞", "不匹配", "冲突", "无法", "不能", "不支持",
    # English (some already present in original)
    "timeout", "timed out", "stuck", "invalid", "failed", "exception", "traceback",
    "not found", "no such", "unknown method", "no such column", "permission denied",
    "lane wait exceeded", "slow listener", "listener", "websocket connection closed", "missing",
]

STRONG_ISSUE_KEYWORDS = [
    # Chinese
    "失败", "错误", "异常", "报错", "超时", "卡死", "阻塞", "不匹配", "冲突",
    # English
    "timeout", "timed out", "stuck", "invalid", "failed", "exception", "traceback",
    "not found", "no such", "unknown method", "no such column", "permission denied",
    "lane wait exceeded", "slow listener", "websocket connection closed", "missing",
]

# ---------------------------------------------------------------------------
# Solution patterns (bilingual)
# ---------------------------------------------------------------------------
SOLUTION_PREFIX_PATTERNS = [
    # Chinese
    r"^方案[:：]", r"^解决[:：]", r"^修复[:：]", r"^修复方法[:：]", r"^解决办法[:：]",
    r"^处理办法[:：]", r"^workaround[:：]", r"^止血方案[:：]", r"^临时方案[:：]",
    r"^最终做法[:：]", r"^改成", r"^改为",
    # English
    r"^fix[:：]", r"^solution[:：]", r"^resolved[:：]", r"^workaround[:：]",
    r"^fixed by ", r"^changed to ", r"^switched to ",
]

SOLUTION_KEYWORDS = [
    # Chinese
    "解决", "修复", "修正", "改成", "改为", "切换", "回退", "绕过", "workaround", "止血",
    "临时方案", "解决办法", "修复方法", "处理办法", "最终做法", "补救", "恢复", "重试",
    "验证通过", "恢复正常",
    # English
    "fix", "fixed", "resolved", "switched", "changed to", "reverted", "bypassed",
    "retry", "verified", "recovered",
]

# ---------------------------------------------------------------------------
# Decision patterns (bilingual)
# ---------------------------------------------------------------------------
DECISION_PREFIX_PATTERNS = [
    # Chinese
    r"^决策[:：]", r"^决定[:：]", r"^最终决定", r"^统一[:：]", r"^采用", r"^选用",
    # English
    r"^decision[:：]", r"^decided[:：]", r"^chose ", r"^adopted ", r"^unified[:：]",
]

DECISION_KEYWORDS = [
    # Chinese
    "决定", "采用", "统一", "选用", "最终确定", "定为", "定成", "策略改为", "架构改为",
    # English
    "decided", "adopted", "unified", "chose", "finalized", "set to", "strategy changed",
]

# ---------------------------------------------------------------------------
# Question / request / progress patterns (bilingual)
# ---------------------------------------------------------------------------
QUESTIONISH_PATTERNS = [
    # Chinese
    r"[？?]$", r"^如何", r"^怎么", r"^为什么", r"^是不是", r"^能不能", r"^能否",
    r"^要不要", r"^需不需要", r"^可不可以", r"^有没有", r"^帮我", r"^我想",
    r"^我们打算", r"^查看", r"^分析一下", r"^实现完整[:：]", r"^写一篇", r"^加一页",
    # English
    r"[?]$", r"^how to ", r"^why ", r"^is it ", r"^can we ", r"^should we ", r"^what if ",
]

NON_ISSUE_PROGRESS_PATTERNS = [
    r"^下一阶段[:：]", r"^当前阶段[:：]", r"^系统状态[:：]", r"^任务状态[:：]",
    r"^需求文档[:：]", r"^实现完整[:：]", r"^最终结果[:：]", r"^手动更新最终结果[:：]",
    r"^验证[:：]",
]

# ---------------------------------------------------------------------------
# Correction / best-practice patterns (bilingual)
# ---------------------------------------------------------------------------
CORRECTION_PATTERNS = [
    # Chinese
    r"不是这个意思", r"你错了", r"应该是", r"应该改为", r"不用这样", r"不需要这样",
    r"这个不用", r"这个不用改", r"不用改这个", r"先别", r"不对路", r"不是重点",
    r"重点不是", r"不是这个问题", r"不是.+而是",
    # English
    r"that's not what I meant", r"you're wrong", r"it should be", r"no need for",
    r"not the point", r"the point is",
]

BEST_PRACTICE_PATTERNS = [
    # Chinese
    r"最稳的做法是", r"正确方向是", r"建议路线是", r"先.+再.+", r"不要.+应该",
    r"V1", r"一句话[:：]", r"默认", r"一律", r"短期.+长期", r"默认.*后台",
    r"走后台", r"后台处理", r"主链路不要", r"不要在主链路",
    # English
    r"the safest approach is", r"the right direction is", r"recommended approach",
    r"always .+ before", r"never .+ without", r"default to",
]

FACT_CORRECTION_HINTS = ["时区", "路径", "目录", "仓库", "端口", "频道", "channel", "vault", "token", "scope", "版本", "model", "id"]
METHOD_CORRECTION_HINTS = ["做法", "处理", "规则", "分流", "后台", "主链路", "执行", "配置", "prompt", "cron", "skill", "hook", "异步", "同步"]

# Explicit fact regex (bilingual)
_EXPLICIT_FACT = re.compile(r"\b(用户|我|user|owner|I)[:：].+")


# ---------------------------------------------------------------------------
# Core classification functions
# ---------------------------------------------------------------------------

def _matches_any(patterns: List[str], text: str) -> bool:
    return any(re.search(p, text, re.I) for p in patterns)


def is_noise_line(line: str) -> bool:
    lower = line.lower()
    return any(m.lower() in lower for m in NOISE_MARKERS)


def is_low_signal_line(line: str) -> bool:
    s = line.strip()
    if not s:
        return True
    if is_noise_line(s):
        return True
    if s.startswith("```") or s.endswith("```"):
        return True
    if re.match(r'^[{}\[\]":,\s]+$', s):
        return True
    if s.startswith(("Conversation info", "Sender (untrusted metadata)", "System:")):
        return True
    if s.startswith(("http://", "https://")) and len(s) > 120:
        return True
    # Command prefixes (bilingual)
    if s.startswith(("openclaw ", "python ", "python3 ", "npm ", "curl ", "rg ", "grep ",
                      "docker ", "git ", "cd ", "cat ", "ls ")):
        return True
    if s.startswith(("参考", "命令:", "执行:", "输出:", "检测")):
        return True
    return False


def extract_candidate_line(raw: str) -> Optional[str]:
    s = raw.strip()
    if not s:
        return None
    if s.startswith("#"):
        return None
    if s in {"HEARTBEAT_OK"}:
        return None
    if s.startswith("-"):
        s = s[1:].strip()
    if len(s) < 6:
        return None
    return re.sub(r"\s+", " ", s).strip()


def classify_line(line: str) -> Tuple[str, float, float]:
    """Classify a line as fact or belief with confidence and importance."""
    importance = 0.5
    if any(k in line for k in ["偏好", "时区", "路径", "仓库", "部署", "端口"]):
        importance = 0.8
    if any(k in line for k in ["token", "密钥", "密码", "apiKey"]):
        importance = 0.2
    if "记住" in line or "长期" in line:
        importance = min(1.0, importance + 0.3)

    if _EXPLICIT_FACT.search(line):
        return ("fact", 1.0, min(1.0, importance))
    # Hedging words (bilingual)
    if any(k in line for k in ["可能", "大概", "也许", "似乎",
                                 "maybe", "perhaps", "probably", "seems like", "might be"]):
        return ("belief", 0.6, min(1.0, importance))
    return ("fact", 0.9, min(1.0, importance))


def is_questionish_line(text: str) -> bool:
    s = core.normalize_content(text)
    if not s:
        return False
    if _matches_any(QUESTIONISH_PATTERNS, s):
        return True
    if any(x in s for x in ["怎么办", "怎么做", "如何做", "能否做", "可否", "是什么"]):
        return True
    return False


def is_non_issue_progress_line(text: str) -> bool:
    s = core.normalize_content(text)
    if not s:
        return False
    return _matches_any(NON_ISSUE_PROGRESS_PATTERNS, s)


def is_request_or_discussion_line(text: str) -> bool:
    s = core.normalize_content(text)
    lower = s.lower()
    if not s:
        return False
    if is_questionish_line(s):
        return True
    markers = [
        "帮我", "让codex", "写一篇", "加一页", "实现", "分析", "查看", "我想", "我们打算",
        "哪些环节", "能否", "如何", "怎么", "是什么", "hover", "ppt", "需求",
    ]
    return any(m in s for m in markers) or any(m in lower for m in ["codex", "ppt", "hover"])


def classify_event_type(line: str) -> Optional[str]:
    if is_low_signal_line(line):
        return None

    lower = line.lower()
    artifact_kw = ["docs/", ".md", "TASKS.md", "PROGRESS.md", "DECISIONS.md", "README.md"]
    progress_kw = ["phase", "阶段", "进度", "完成度", "系统状态", "下一阶段", "最终结果",
                   "success", "failed", "总耗时", "执行完成", "验证通过"]

    if any(k in line for k in artifact_kw):
        return "artifact"
    if is_non_issue_progress_line(line) or any(k.lower() in lower for k in progress_kw):
        return "progress"

    if _matches_any(SOLUTION_PREFIX_PATTERNS, line):
        return "solution"
    if _matches_any(DECISION_PREFIX_PATTERNS, line):
        return "decision"
    if _matches_any(ISSUE_PREFIX_PATTERNS, line) and not is_questionish_line(line):
        return "issue"

    has_issue = any(k in lower for k in ISSUE_KEYWORDS)
    has_strong_issue = any(k in lower for k in STRONG_ISSUE_KEYWORDS)
    has_solution = any(k in lower for k in SOLUTION_KEYWORDS)
    has_decision = any(k in lower for k in DECISION_KEYWORDS)
    questionish = is_questionish_line(line)
    requestish = is_request_or_discussion_line(line)

    if has_solution and not has_decision:
        return "solution"
    if has_issue and has_solution:
        if re.search(r"(改成|改为|修复|解决|workaround|止血|恢复|重试)", line, re.I):
            return "solution"
        return None if (questionish or requestish or not has_strong_issue) else "issue"
    if has_issue and not has_solution:
        return None if (questionish or requestish or not has_strong_issue) else "issue"
    if has_decision:
        return "decision"
    return None


def infer_tags(line: str) -> List[str]:
    tags: List[str] = []
    lower = line.lower()
    tag_map = get_tag_rules()
    for tag, kws in tag_map.items():
        if any(kw in line for kw in kws):
            tags.append(tag)
    if any(k in lower for k in ["timeout", "timed out", "超时", "卡死", "stuck", "阻塞",
                                  "slow listener", "lane wait exceeded"]):
        tags.append("stability")
    if any(k in lower for k in ["error", "failed", "异常", "报错", "错误", "失败",
                                  "traceback", "exception", "invalid"]):
        tags.append("error")
    if any(k in lower for k in ["修复", "解决", "workaround", "止血", "恢复", "改为", "改成",
                                  "fix", "fixed", "resolved"]):
        tags.append("fix")
    return list(dict.fromkeys(tags))

# ---------------------------------------------------------------------------
# Pattern key inference
# ---------------------------------------------------------------------------

def infer_pattern_key(content: str, *, kind: str = "", event_type: str = "",
                      tags: Optional[List[str]] = None) -> Optional[str]:
    lower = content.lower()
    tags = tags or []
    if any(k in lower for k in [".sync.lock", "ob sync", "obsidian"]) and "lock" in lower:
        return "obsidian.sync.lock"
    if any(k in lower for k in ["bigmodel", "asr", "ogg_to_text"]) and any(k in lower for k in ["timeout", "超时", "卡死", "阻塞"]):
        return "asr.sync_timeout"
    if "discord" in lower and any(k in lower for k in ["message_create", "listener", "lane wait", "主链路", "后台", "卡死", "阻塞"]):
        return "discord.heavy_task.blocking"
    if any(k in lower for k in ["routing-rules", "分流"]) or ("后台" in content and "主" in content and "链路" in content):
        return "routing.background_required"
    if "requiremention" in lower or "require mention" in lower:
        return "discord.require_mention"
    if event_type == "issue" and any(k in lower for k in ["timeout", "timed out", "超时", "卡死"]):
        return "stability.timeout"
    if kind == "summary" and any(tag in tags for tag in ["best_practice", "correction"]):
        return f"pattern.{next((t for t in tags if t not in ['best_practice','correction','working_pattern','fix','error','stability']), 'general')}"
    return None


def build_learning_items(line: str, now_iso: str, source: str, *,
                         from_reflection: bool) -> Tuple[List[Dict[str, Any]], bool]:
    items: List[Dict[str, Any]] = []
    normalized = core.normalize_content(line)
    tags = infer_tags(normalized)
    source_type = "reflection" if from_reflection else "daily_memory"

    is_correction = any(re.search(p, normalized) for p in CORRECTION_PATTERNS)
    is_best_practice = any(re.search(p, normalized) for p in BEST_PRACTICE_PATTERNS)

    if is_correction:
        if any(k in normalized for k in FACT_CORRECTION_HINTS):
            content = normalized
            item = {
                "id": core.make_id("fact", content),
                "kind": "fact",
                "content": content,
                "confidence": 0.98,
                "importance": 0.85,
                "weight": 1.0,
                "created_at": now_iso,
                "updated_at": now_iso,
                "last_seen_at": now_iso,
                "source": source,
                "source_type": "correction",
                "tags": list(dict.fromkeys([*tags, "correction"])),
            }
            pk = infer_pattern_key(content, kind="fact", tags=item["tags"])
            if pk:
                item["pattern_key"] = pk
            items.append(item)
        else:
            content = normalized if normalized.startswith("修正：") else f"修正：{normalized}"
            item = {
                "id": core.make_id("summary", content),
                "kind": "summary",
                "content": content,
                "confidence": 0.95,
                "importance": 0.82 if any(k in normalized for k in METHOD_CORRECTION_HINTS) else 0.76,
                "weight": 1.0,
                "created_at": now_iso,
                "updated_at": now_iso,
                "last_seen_at": now_iso,
                "source": source,
                "source_type": "correction",
                "tags": list(dict.fromkeys([*tags, "correction"])),
            }
            pk = infer_pattern_key(content, kind="summary", tags=item["tags"])
            if pk:
                item["pattern_key"] = pk
            items.append(item)

    if is_best_practice:
        content = normalized
        if not content.startswith(("工作模式：", "最佳实践：", "原则：")):
            content = f"工作模式：{content}"
        item = {
            "id": core.make_id("summary", content),
            "kind": "summary",
            "content": content,
            "confidence": 0.93,
            "importance": 0.88,
            "weight": 1.0,
            "created_at": now_iso,
            "updated_at": now_iso,
            "last_seen_at": now_iso,
            "source": source,
            "source_type": "best_practice",
            "tags": list(dict.fromkeys([*tags, "best_practice", "working_pattern"])),
        }
        pk = infer_pattern_key(content, kind="summary", tags=item["tags"])
        if pk:
            item["pattern_key"] = pk
        items.append(item)

    return items, bool(items)


def apply_pattern_metadata(rows: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    out: List[Dict[str, Any]] = []
    for row in rows:
        row = dict(row)
        content = str(row.get("content") or "")
        tags = list(row.get("tags") or [])
        pk = infer_pattern_key(content, kind=str(row.get("kind") or ""),
                               event_type=str(row.get("event_type") or ""), tags=tags)
        if pk and not row.get("pattern_key"):
            row["pattern_key"] = pk
        if row.get("pattern_key") and row.get("kind") == "summary" and "working_pattern" not in tags:
            row["tags"] = [*tags, "working_pattern"]
        out.append(row)
    return out


# ---------------------------------------------------------------------------
# Noise detection for facts / issues / recent lines
# ---------------------------------------------------------------------------

def is_noisy_fact_row(row: Dict[str, Any]) -> bool:
    content = core.normalize_content(str(row.get("content") or ""))
    lower = content.lower()
    if not content:
        return True
    if content.endswith(("：", ":")):
        return True
    if content.startswith(("问题：", "方案：", "工作模式：", "需求文档：", "修复文件：", "文件：", "今日文档变更:", "任务清单位置:")):
        return True
    noisy_markers = [
        "按需求文档", "已按需求文档", "已完成需求文档", "依据 `docs/", "依据 docs/", "docs/clauder-task/",
        "src/", "route.ts", "page.tsx", "systemctl", "npm run build", "curl http://127.0.0.1:3000",
        "状态改为", "错误信息 `重规划：已取消旧执行`", "先查并取消", "取消对应 `subtask_runs`", "await cleanuptasksessions",
        "已更新 cron 任务", "jobid:",
    ]
    return any(m.lower() in lower for m in noisy_markers)


def prune_noisy_facts(rows: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    return [row for row in rows if not is_noisy_fact_row(row)]


def is_noisy_issue_row(row: Dict[str, Any]) -> bool:
    if str(row.get("event_type") or "") != "issue":
        return False
    return is_display_noise_issue_line(str(row.get("content") or ""))


def prune_noisy_issue_events(rows: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    return [row for row in rows if not is_noisy_issue_row(row)]


def is_display_noise_issue_line(text: str) -> bool:
    s = core.normalize_content(text)
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


def is_recent_noise_line(text: str) -> bool:
    s = core.normalize_content(text)
    lower = s.lower()
    if not s:
        return True
    if s.startswith(("需求文档：", "修复文件：", "文件：", "命令：", "执行：", "输出：", "验证：",
                     "今日文档变更:", "任务清单位置:", "任务：", "调用 ", "读取当日 ", "包含",
                     "原需求：", "后续追加：", "交付物", "OPS ", "已完成代码修改：", "保持绝对路径",
                     "Bug ", "API ", "文档记录", "验证与部署：", "示例模式更新：")):
        return True
    if "`" in s or "/" in s or ".py" in lower or ".ts" in lower or ".md" in lower:
        return True
    noisy_markers = [
        "npm run build", "systemctl", "curl http://", "curl https://", "src/", "route.ts", "page.tsx", "/api/",
        "await ", "running/in_progress/dispatched/pending", "subtask_runs", "tasksessions", "task_deliverables",
        "callback/", "in_progress", "cancelled", "error:", "requestid", "upsert", "绝对路径去重",
        "jobid", "payload", "process.kill", "cron payload", "主动", "wrapper 脚本", "signals_", "scan_errors_",
    ]
    return any(m in lower for m in noisy_markers)


# ---------------------------------------------------------------------------
# File reading utilities
# ---------------------------------------------------------------------------

def read_new_lines(path: "Path", cursor: int) -> Tuple[List[Tuple[int, str]], int]:
    from pathlib import Path as _P
    lines = path.read_text("utf-8", errors="ignore").splitlines()
    total = len(lines)
    start = max(0, cursor)
    new_rows: List[Tuple[int, str]] = []
    for i in range(start, total):
        new_rows.append((i + 1, lines[i]))
    return new_rows, total


def list_daily_logs() -> "List[Path]":
    from .config import DAILY_DIR
    return sorted([p for p in DAILY_DIR.glob("????-??-??.md") if p.is_file()])


def list_reflection_logs() -> "List[Path]":
    from .config import DAILY_DIR
    return sorted([p for p in DAILY_DIR.glob("????-??-??-clauder-reflection.md") if p.is_file()])


def is_reflection_log(path: "Path") -> bool:
    return path.name.endswith("-clauder-reflection.md")


def collect_recent_lines(files: "List[Path]", max_lines: int = 18) -> List[str]:
    out: List[str] = []
    seen: set = set()
    for p in files:
        txt = p.read_text("utf-8", errors="ignore")
        for raw in txt.splitlines():
            line = extract_candidate_line(raw)
            if not line:
                continue
            line = core.normalize_content(line)
            if is_low_signal_line(line) or is_recent_noise_line(line) or re.match(r"^\d+\.\s", line):
                continue
            key = core.normalize_for_match(line)
            if not key or key in seen:
                continue
            seen.add(key)
            out.append(line)
    return out[-max_lines:]


def collect_reference_corpus(files: "List[Path]", max_lines: int = 5000) -> List[str]:
    out: List[str] = []
    for p in files:
        txt = p.read_text("utf-8", errors="ignore")
        for raw in txt.splitlines():
            line = extract_candidate_line(raw)
            if not line:
                continue
            normalized = core.normalize_for_match(line)
            if normalized:
                out.append(normalized)
    return out[-max_lines:]


# ---------------------------------------------------------------------------
# Session log ingestion
# ---------------------------------------------------------------------------
_HEARTBEAT_SKIP = {"HEARTBEAT_OK", "NO_REPLY"}
_HEARTBEAT_MARKER = "HEARTBEAT"


def list_session_logs(workspace: "Path", hours: int = 24,
                      agent_ids: "Any" = "main") -> "List[Path]":
    """List recent session JSONL files for the given agent(s).

    agent_ids can be a string (single agent) or a list of strings.
    """
    import time
    from pathlib import Path as _P

    # Normalize to list
    if isinstance(agent_ids, str):
        ids = [agent_ids]
    elif isinstance(agent_ids, list):
        ids = agent_ids
    else:
        ids = ["main"]

    cutoff = time.time() - hours * 3600
    result = []
    for aid in ids:
        sessions_dir = workspace.parent / "agents" / aid / "sessions"
        if not sessions_dir.is_dir():
            continue
        for p in sessions_dir.iterdir():
            if not p.name.endswith(".jsonl"):
                continue
            if ".deleted." in p.name or ".reset." in p.name:
                continue
            try:
                if p.stat().st_mtime >= cutoff:
                    result.append(p)
            except OSError:
                continue
    return sorted(result, key=lambda p: p.name)


def extract_session_lines(path: "Path") -> List[Tuple[int, str]]:
    """Extract user/assistant text lines from a session JSONL file."""
    import json as _json

    result: List[Tuple[int, str]] = []
    try:
        raw_lines = path.read_text("utf-8", errors="ignore").splitlines()
    except Exception:
        return result

    for lineno, raw in enumerate(raw_lines, 1):
        raw = raw.strip()
        if not raw:
            continue
        try:
            obj = _json.loads(raw)
        except _json.JSONDecodeError:
            continue

        if obj.get("type") != "message":
            continue
        msg = obj.get("message") or {}
        role = msg.get("role")
        if role not in ("user", "assistant"):
            continue

        content_parts = msg.get("content")
        if not isinstance(content_parts, list):
            continue

        for part in content_parts:
            if not isinstance(part, dict):
                continue
            # Only extract text parts; skip thinking, toolCall, toolResult, etc.
            if part.get("type") != "text":
                continue
            text = str(part.get("text") or "").strip()
            if not text:
                continue
            # Skip heartbeat / no-reply markers
            if text in _HEARTBEAT_SKIP:
                continue
            if _HEARTBEAT_MARKER in text and len(text) < 200:
                continue

            # Session messages can be multi-line; split and yield each line
            for sub_line in text.splitlines():
                sub = sub_line.strip()
                if sub and len(sub) >= 6:
                    result.append((lineno, sub))

    return result

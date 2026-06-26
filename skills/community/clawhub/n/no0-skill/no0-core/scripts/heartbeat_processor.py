#!/usr/bin/env python3
"""
Heartbeat processor: classifies unlabeled change events using local rule-based analysis,
then reconciles records between active log and labeled archive.
"""
import json
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional, Sequence, Tuple

from event_logger import _build_markdown_block, update_change_log_label
from event_emitter import emit_tamper_event

BASE_DIR = Path(__file__).resolve().parent.parent
CHANGE_LOG_JSON = BASE_DIR / "change_log.json"
CHANGE_LOG_MD = BASE_DIR / "change_log.md"
ARCHIVE_JSON = BASE_DIR / "change_log_labeled.json"
ARCHIVE_MD = BASE_DIR / "change_log_labeled.md"

CORE_FILES = {
    "soul.md",
    "user.md",
    "heartbeat.md",
    "memory.md",
    "tools.md",
    "agents.md",
}

CONTROL_FILES = {
    "monitor.py",
    "skill_launcher.py",
    "heartbeat_processor.py",
    "reconcile_daemon.py",
}

HIGH_RISK_RULES: Dict[str, Sequence[str]] = {
    "安全机制绕过": [
        "绕过", "bypass", "disable security", "skip check",
        "ignore confirmation", "无人工确认", "忽略确认",
        "monitor blind", "权限自动放行", "allow all", "trust all",
    ],
    "自动执行外部命令": [
        "自动执行外部命令", "os.system(", "subprocess.run(",
        "shell=true", "invoke-expression", "eval(", "exec(",
        "curl ", "wget ", "powershell -command",
    ],
    "敏感信息外发": [
        "token", "secret", "api_key", "private_key",
        "upload", "exfil", "send to", "外发", "上报外部",
    ],
    "破坏性清理与覆盖": [
        "rm -rf", "shutil.rmtree", "delete backup", "truncate",
        "wipe", "unlink(", "覆盖核心文件", "删除备份",
    ],
}

MEDIUM_RISK_RULES: Dict[str, Sequence[str]] = {
    "权限与身份边界": [
        "权限", "鉴权", "admin", "root", "sudo", "grant", "身份",
    ],
    "回滚与备份策略": [
        "回滚限制", "rollback", "backup", "restore", "版本", "备份策略",
    ],
    "外部来源与路由": [
        "外部来源策略", "工具路由改写", "source", "router", "endpoint", "url",
    ],
    "定时与进程控制": [
        "reconcile", "timer", "interval", "cron", "pid", "terminate", "kill",
    ],
}

LOW_RISK_HINTS: Dict[str, Sequence[str]] = {
    "注释和文案": [
        "维护注记", "注释", "comment", "readme", "文案", "描述",
    ],
    "格式化与排版": [
        "format", "formatter", "whitespace", "空行", "markdown", "typo", "拼写",
    ],
}

PARSE_ERROR_REASON = "Heartbeat returned invalid JSON"


def now_text() -> str:
    return datetime.now().astimezone().isoformat(timespec="seconds")


def is_pending(level: Any) -> bool:
    if level is None:
        return True
    raw = str(level).strip().lower()
    return raw == "" or raw == "null"


def resolve_record_level(row: Dict[str, Any]) -> Any:
    return row.get("level")


def load_records() -> List[Dict[str, Any]]:
    if not CHANGE_LOG_JSON.exists():
        return []
    try:
        data = json.loads(CHANGE_LOG_JSON.read_text(encoding="utf-8"))
        if isinstance(data, list):
            return [x for x in data if isinstance(x, dict)]
    except Exception:
        pass
    return []


def parse_event(record: Dict[str, Any]) -> Tuple[Dict[str, Any], bool]:
    """Extract the event payload directly from the record."""
    event_payload = record.get("event_payload", {})
    if isinstance(event_payload, dict) and event_payload:
        return event_payload, True
    return {}, False


def safe_int(value: Any) -> int:
    try:
        return int(value or 0)
    except Exception:
        return 0


def collect_text_blob(event: Dict[str, Any]) -> Tuple[str, int, int, str]:
    diff = event.get("diff", {}) if isinstance(event, dict) else {}
    diff = diff if isinstance(diff, dict) else {}
    stats = diff.get("stats", {}) if isinstance(diff, dict) else {}
    stats = stats if isinstance(stats, dict) else {}

    added = safe_int(stats.get("added_line_count", 0))
    removed = safe_int(stats.get("removed_line_count", 0))

    file_name = str(event.get("file_name", "")).strip()
    source = str(event.get("source", "")).strip()
    trigger_type = str(event.get("trigger_type", "")).strip()
    unified = str(diff.get("unified_diff", ""))
    before_content = str(event.get("before_content", ""))
    after_content = str(event.get("after_content", ""))

    blob = "\n".join([file_name, source, trigger_type, unified, before_content, after_content]).lower()
    return blob, added, removed, file_name.lower()


def match_rule_groups(text: str, rule_groups: Dict[str, Sequence[str]]) -> List[Tuple[str, str]]:
    matches: List[Tuple[str, str]] = []
    for group, keywords in rule_groups.items():
        for keyword in keywords:
            token = keyword.lower().strip()
            if token and token in text:
                matches.append((group, keyword))
                break
    return matches


def compact_match_labels(matches: List[Tuple[str, str]]) -> str:
    labels = [name for name, _ in matches]
    if not labels:
        return ""
    return "、".join(labels)


def classify(event: Dict[str, Any]) -> Tuple[Optional[int], str]:
    text, added, removed, file_name = collect_text_blob(event)
    churn = added + removed

    high_hits = match_rule_groups(text, HIGH_RISK_RULES)
    medium_hits = match_rule_groups(text, MEDIUM_RISK_RULES)
    low_hits = match_rule_groups(text, LOW_RISK_HINTS)

    score = 0
    evidence: List[str] = []

    if high_hits:
        score += 8 + len(high_hits)
        evidence.append(f"命中高危规则：{compact_match_labels(high_hits)}")

    if medium_hits:
        score += 3 + len(medium_hits)
        evidence.append(f"命中中危规则：{compact_match_labels(medium_hits)}")

    if file_name in CORE_FILES and churn > 0:
        score += 2
        evidence.append("涉及核心认知文件")

    if file_name in CONTROL_FILES and churn > 0:
        score += 2
        evidence.append("涉及监控/调度控制脚本")

    if churn >= 200:
        score += 4
        evidence.append("变更规模极大")
    elif churn >= 80:
        score += 3
        evidence.append("变更规模较大")
    elif churn >= 30:
        score += 2
        evidence.append("变更规模中等")
    elif churn >= 10:
        score += 1

    if low_hits and not high_hits and not medium_hits:
        score -= min(2, len(low_hits))
        evidence.append(f"命中低风险信号：{compact_match_labels(low_hits)}")
    elif churn <= 3 and not high_hits:
        score -= 1

    has_critical_group = {name for name, _ in high_hits} & {
        "安全机制绕过", "自动执行外部命令", "敏感信息外发", "破坏性清理与覆盖",
    }

    if has_critical_group:
        level = 5
    elif score >= 11:
        level = 5
    elif score >= 7:
        level = 4
    elif score >= 4:
        level = 3
    elif score >= 2:
        level = 2
    else:
        level = 1

    if not evidence:
        evidence.append("未命中显著风险关键词")

    reason = (
        f"{'; '.join(evidence[:3])}；"
        f"变更规模 added={added}, removed={removed}，综合评分={score}，判定 Level {level}。"
    )
    return level, reason


def load_json_list(path: Path) -> List[Dict[str, Any]]:
    if not path.exists():
        return []
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
        if isinstance(data, list):
            return [x for x in data if isinstance(x, dict)]
    except Exception:
        pass
    return []


def save_json_list(path: Path, rows: List[Dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(rows, ensure_ascii=False, indent=2), encoding="utf-8")


def reconcile_json() -> Tuple[int, int]:
    rows = load_json_list(CHANGE_LOG_JSON)
    if not rows:
        return 0, 0

    pending: List[Dict[str, Any]] = []
    labeled_new: List[Dict[str, Any]] = []
    for row in rows:
        level = resolve_record_level(row)
        if is_pending(level):
            pending.append(row)
        else:
            row.setdefault("archived_record_time", now_text())
            labeled_new.append(row)

    existing = load_json_list(ARCHIVE_JSON)
    seen = {str(x.get("event_id", "")).strip() for x in existing}
    for row in labeled_new:
        eid = str(row.get("event_id", "")).strip()
        if eid and eid not in seen:
            existing.append(row)
            seen.add(eid)

    save_json_list(CHANGE_LOG_JSON, pending)
    save_json_list(ARCHIVE_JSON, existing)
    return len(labeled_new), len(pending)


def render_markdown_rows(rows: List[Dict[str, Any]], default_record_type: str) -> str:
    blocks: List[str] = []
    fallback_time = now_text()

    for row in rows:
        if not isinstance(row, dict):
            continue

        event_payload = row.get("event_payload", {})
        if not isinstance(event_payload, dict):
            event_payload = {}

        file_name = str(row.get("file_name", "")).strip() or str(event_payload.get("file_name", "")).strip()
        level = resolve_record_level(row)
        reason = str(row.get("reason", ""))
        record_type = str(row.get("record_type", "")).strip() or default_record_type

        if default_record_type == "labeled":
            record_time = (
                str(row.get("labeled_record_time", "")).strip()
                or str(row.get("archived_record_time", "")).strip()
                or str(row.get("record_time", "")).strip()
                or fallback_time
            )
        else:
            record_time = str(row.get("record_time", "")).strip() or fallback_time

        block = _build_markdown_block(
            record_time=record_time,
            file_name=file_name,
            event_payload=event_payload,
            level=level,
            reason=reason,
            record_type=record_type,
        ).strip()
        if block:
            blocks.append(block)

    text = "\n\n".join(blocks).strip()
    return text + ("\n" if text else "")


def reconcile_md() -> Tuple[int, int]:
    pending_rows = [x for x in load_json_list(CHANGE_LOG_JSON) if isinstance(x, dict)]
    labeled_rows = [x for x in load_json_list(ARCHIVE_JSON) if isinstance(x, dict)]

    CHANGE_LOG_MD.write_text(render_markdown_rows(pending_rows, "detected"), encoding="utf-8")
    ARCHIVE_MD.write_text(render_markdown_rows(labeled_rows, "labeled"), encoding="utf-8")

    pending_count = sum(1 for row in pending_rows if is_pending(resolve_record_level(row)))
    labeled_count = sum(1 for row in labeled_rows if not is_pending(resolve_record_level(row)))
    return labeled_count, pending_count


def summarize_json_state() -> Dict[str, int]:
    active_rows = [x for x in load_json_list(CHANGE_LOG_JSON) if isinstance(x, dict)]
    archived_rows = [x for x in load_json_list(ARCHIVE_JSON) if isinstance(x, dict)]
    all_rows = active_rows + archived_rows
    labeled_count = sum(1 for row in all_rows if not is_pending(resolve_record_level(row)))
    total_count = len(all_rows)
    return {
        "total": total_count,
        "labeled": labeled_count,
        "unlabeled": max(0, total_count - labeled_count),
    }


def reconcile_labeled_records() -> Dict[str, int]:
    j_labeled, j_pending = reconcile_json()
    m_labeled, m_pending = reconcile_md()
    return {
        "json_archived": j_labeled,
        "json_pending": j_pending,
        "md_archived": m_labeled,
        "md_pending": m_pending,
    }


def process_once() -> Dict[str, int]:
    records = load_records()
    pending = [r for r in records if is_pending(resolve_record_level(r))]
    updated = 0
    parse_error = 0
    now = now_text()

    for row in pending:
        event_id = str(row.get("event_id", "")).strip()
        if not event_id:
            continue

        event, parsed_ok = parse_event(row)
        if not parsed_ok:
            ok = update_change_log_label(
                event_id=event_id,
                level="parse_error",
                reason=PARSE_ERROR_REASON,
                json_file_path=CHANGE_LOG_JSON,
                md_file_path=CHANGE_LOG_MD,
                labeled_record_time=now,
            )
            if ok:
                parse_error += 1
            continue

        try:
            level, reason = classify(event)
            if level is None:
                raise ValueError("invalid level")
            ok = update_change_log_label(
                event_id=event_id,
                level=level,
                reason=reason,
                json_file_path=CHANGE_LOG_JSON,
                md_file_path=CHANGE_LOG_MD,
                labeled_record_time=now,
            )
            if ok:
                updated += 1
                if isinstance(level, int) and level >= 4:
                    blob, added, removed, _ = collect_text_blob(event)
                    rule_hits = [group for group, _ in match_rule_groups(blob, HIGH_RISK_RULES)]
                    emit_tamper_event(
                        event_payload=event,
                        level=level,
                        reason=reason,
                        rule_hits=rule_hits,
                        added=added,
                        removed=removed,
                        target_path=str(event.get("source", "")) or None,
                    )
        except Exception:
            ok = update_change_log_label(
                event_id=event_id,
                level="parse_error",
                reason=PARSE_ERROR_REASON,
                json_file_path=CHANGE_LOG_JSON,
                md_file_path=CHANGE_LOG_MD,
                labeled_record_time=now,
            )
            if ok:
                parse_error += 1

    reconcile_stats = reconcile_labeled_records()
    reconcile_stats["heartbeat_processed"] = updated
    reconcile_stats["parse_error"] = parse_error
    return reconcile_stats


def main() -> int:
    stats = process_once()
    json_state = summarize_json_state()
    print(
        f"heartbeat_processed={stats['heartbeat_processed']} parse_error={stats['parse_error']} | "
        f"json moved={stats['json_archived']} pending_in_log={stats['json_pending']} total={json_state['total']} "
        f"labeled={json_state['labeled']} unlabeled={json_state['unlabeled']} | "
        f"md total={json_state['total']} labeled={stats['md_archived']} unlabeled={stats['md_pending']}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

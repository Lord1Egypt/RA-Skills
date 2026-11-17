#!/usr/bin/env python3
"""Priority Coach weekly report generator.

优先读取 sessions.json（最小会话摘要），生成：
- Markdown 周报
- JSON 结构化摘要
- 给 AI 审核的 prompt

默认兼容：
- ~/.openclaw/data/priority-coach/sessions.json
- ~/.workbuddy/priority-coach/sessions.json
"""

from __future__ import annotations

import argparse
import datetime as dt
import json
import os
from collections import Counter
from pathlib import Path
from typing import Any


OPENCLAW_HOME = Path(os.environ.get("OPENCLAW_HOME", "~/.openclaw")).expanduser()
DEFAULT_INPUT = OPENCLAW_HOME / "data" / "priority-coach" / "sessions.json"
LEGACY_INPUT = Path("~/.workbuddy/priority-coach/sessions.json").expanduser()

HELPFUL_OUTCOMES = {
    "clarified_priority",
    "defined_next_step",
    "reduced_pressure",
}


def detect_input_path(explicit: str | None) -> Path:
    if explicit:
        return Path(explicit).expanduser()
    if DEFAULT_INPUT.exists():
        return DEFAULT_INPUT
    return LEGACY_INPUT


def load_store(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {"schemaVersion": 0, "sessions": []}
    with path.open("r", encoding="utf-8") as f:
        data = json.load(f)
    if not isinstance(data, dict):
        return {"schemaVersion": 0, "sessions": []}
    sessions = data.get("sessions")
    if not isinstance(sessions, list):
        data["sessions"] = []
    return data


def normalize_string(value: Any) -> str:
    if value is None:
        return ""
    return str(value).strip()


def normalize_bool(value: Any, default: bool = False) -> bool:
    if isinstance(value, bool):
        return value
    if value in (1, "1", "true", "True", "yes", "YES"):
        return True
    if value in (0, "0", "false", "False", "no", "NO"):
        return False
    return default


def normalize_list(value: Any) -> list[str]:
    if value is None:
        return []
    if isinstance(value, list):
        return [normalize_string(x) for x in value if normalize_string(x)]
    if isinstance(value, str):
        text = normalize_string(value)
        return [text] if text else []
    text = normalize_string(value)
    return [text] if text else []


def default_session_summary() -> dict[str, Any]:
    return {
        "schemaVersion": 1,
        "sessionId": "",
        "date": "",
        "startedAt": "",
        "endedAt": "",
        "enteredState": "",
        "endedState": "",
        "completed": False,
        "resultType": "",
        "savedResult": False,
        "feedbackOutcome": "",
        "feedbackFailureReason": "",
        "failureTags": [],
        "routeConfidence": "",
        "dropoffRisk": "",
        "nextStepChosen": "",
    }


def normalize_session_summary(raw: Any) -> dict[str, Any] | None:
    if not isinstance(raw, dict):
        return None

    base = default_session_summary()
    now = dt.datetime.now().isoformat(timespec="seconds")
    base["sessionId"] = normalize_string(raw.get("sessionId"))
    base["date"] = normalize_string(raw.get("date")) or dt.date.today().isoformat()
    base["startedAt"] = normalize_string(raw.get("startedAt")) or now
    base["endedAt"] = normalize_string(raw.get("endedAt")) or now
    base["enteredState"] = normalize_string(raw.get("enteredState"))
    base["endedState"] = normalize_string(raw.get("endedState"))
    base["completed"] = normalize_bool(raw.get("completed"), False)
    base["resultType"] = normalize_string(raw.get("resultType"))
    base["savedResult"] = normalize_bool(raw.get("savedResult"), False)
    base["feedbackOutcome"] = normalize_string(raw.get("feedbackOutcome"))
    base["feedbackFailureReason"] = normalize_string(raw.get("feedbackFailureReason"))
    base["failureTags"] = normalize_list(raw.get("failureTags"))[:2]
    base["routeConfidence"] = normalize_string(raw.get("routeConfidence"))
    base["dropoffRisk"] = normalize_string(raw.get("dropoffRisk"))
    base["nextStepChosen"] = normalize_string(raw.get("nextStepChosen"))
    return base


def filter_sessions(
    sessions: list[dict[str, Any]],
    *,
    days: int = 7,
    limit: int | None = None,
) -> list[dict[str, Any]]:
    cutoff = dt.date.today() - dt.timedelta(days=days)
    filtered: list[dict[str, Any]] = []

    for session in sessions:
        date_str = session.get("date", "")
        try:
            session_date = dt.date.fromisoformat(date_str)
        except Exception:
            continue
        if session_date >= cutoff:
            filtered.append(session)

    filtered.sort(key=lambda x: x.get("date", ""), reverse=True)

    if limit is not None:
        filtered = filtered[:limit]
    return filtered


def pct(numerator: int, denominator: int) -> float:
    if denominator <= 0:
        return 0.0
    return round(numerator / denominator, 4)


def summarize(sessions: list[dict[str, Any]]) -> dict[str, Any]:
    total = len(sessions)

    entered_counter: Counter[str] = Counter()
    ended_counter: Counter[str] = Counter()
    feedback_counter: Counter[str] = Counter()
    failure_reason_counter: Counter[str] = Counter()
    failure_tag_counter: Counter[str] = Counter()
    next_step_counter: Counter[str] = Counter()
    route_confidence_counter: Counter[str] = Counter()
    dropoff_risk_counter: Counter[str] = Counter()
    result_type_counter: Counter[str] = Counter()

    completed_count = 0
    saved_count = 0
    helpful_count = 0
    overwhelmed_count = 0

    for session in sessions:
        entered_state = normalize_string(session.get("enteredState"))
        ended_state = normalize_string(session.get("endedState"))
        feedback_outcome = normalize_string(session.get("feedbackOutcome"))
        failure_reason = normalize_string(session.get("feedbackFailureReason"))
        next_step = normalize_string(session.get("nextStepChosen"))
        route_confidence = normalize_string(session.get("routeConfidence"))
        dropoff_risk = normalize_string(session.get("dropoffRisk"))
        result_type = normalize_string(session.get("resultType"))
        failure_tags = normalize_list(session.get("failureTags"))

        if entered_state:
            entered_counter[entered_state] += 1
        if ended_state:
            ended_counter[ended_state] += 1
        if feedback_outcome:
            feedback_counter[feedback_outcome] += 1
        if failure_reason:
            failure_reason_counter[failure_reason] += 1
        if next_step:
            next_step_counter[next_step] += 1
        if route_confidence:
            route_confidence_counter[route_confidence] += 1
        if dropoff_risk:
            dropoff_risk_counter[dropoff_risk] += 1
        if result_type:
            result_type_counter[result_type] += 1

        for tag in failure_tags:
            failure_tag_counter[tag] += 1

        if normalize_bool(session.get("completed"), False):
            completed_count += 1
        if normalize_bool(session.get("savedResult"), False):
            saved_count += 1
        if feedback_outcome in HELPFUL_OUTCOMES:
            helpful_count += 1
        if entered_state == "overwhelmed_mode":
            overwhelmed_count += 1

    insights = derive_insights(
        total=total,
        entered_counter=entered_counter,
        feedback_counter=feedback_counter,
        failure_reason_counter=failure_reason_counter,
        failure_tag_counter=failure_tag_counter,
        completed_count=completed_count,
        helpful_count=helpful_count,
        overwhelmed_count=overwhelmed_count,
    )

    recommendations = derive_recommendations(
        failure_reason_counter=failure_reason_counter,
        failure_tag_counter=failure_tag_counter,
        entered_counter=entered_counter,
        feedback_counter=feedback_counter,
        total=total,
        overwhelmed_count=overwhelmed_count,
    )

    version_bump, suggested_next_version = suggest_version_bump(
        total=total,
        failure_reason_counter=failure_reason_counter,
        failure_tag_counter=failure_tag_counter,
        helpful_rate=pct(helpful_count, total),
    )

    return {
        "generatedAt": dt.datetime.now().isoformat(timespec="seconds"),
        "windowDays": None,
        "totalSessions": total,
        "completionRate": pct(completed_count, total),
        "saveRate": pct(saved_count, total),
        "helpfulRate": pct(helpful_count, total),
        "overwhelmedRate": pct(overwhelmed_count, total),
        "stateDistribution": dict(entered_counter),
        "endedStateDistribution": dict(ended_counter),
        "feedbackOutcomeDistribution": dict(feedback_counter),
        "failureReasonDistribution": dict(failure_reason_counter),
        "failureTagDistribution": dict(failure_tag_counter),
        "nextStepDistribution": dict(next_step_counter),
        "routeConfidenceDistribution": dict(route_confidence_counter),
        "dropoffRiskDistribution": dict(dropoff_risk_counter),
        "resultTypeDistribution": dict(result_type_counter),
        "topInsights": insights,
        "recommendedFocus": recommendations,
        "recommendedVersionBump": version_bump,
        "suggestedNextVersion": suggested_next_version,
    }


def derive_insights(
    *,
    total: int,
    entered_counter: Counter[str],
    feedback_counter: Counter[str],
    failure_reason_counter: Counter[str],
    failure_tag_counter: Counter[str],
    completed_count: int,
    helpful_count: int,
    overwhelmed_count: int,
) -> list[str]:
    insights: list[str] = []

    if total == 0:
        return insights

    if entered_counter:
        top_state, top_count = entered_counter.most_common(1)[0]
        insights.append(f"{top_state} 占比最高（{top_count}/{total}），说明这是当前最主要的入口。")

    if overwhelmed_count / total >= 0.2:
        insights.append("overwhelmed_mode 命中率偏高，说明低能量 / 过载场景比较明显。")

    if failure_reason_counter:
        reason, count = failure_reason_counter.most_common(1)[0]
        insights.append(f"最常见失败原因是 {reason}（{count} 次），适合优先修这一类问题。")

    if failure_tag_counter:
        tag, count = failure_tag_counter.most_common(1)[0]
        insights.append(f"最常见失败标签是 {tag}（{count} 次），说明问题模式已经开始集中。")

    clarified = feedback_counter.get("clarified_priority", 0)
    next_step = feedback_counter.get("defined_next_step", 0)
    reduced_pressure = feedback_counter.get("reduced_pressure", 0)

    if clarified > next_step:
        insights.append("“看清重点”多于“定下第一步”，说明洞察强于行动转化。")
    elif next_step > clarified:
        insights.append("“定下第一步”多于“看清重点”，说明行动转化正在增强。")

    if reduced_pressure > 0:
        insights.append("有一部分用户明确反馈“被减负了”，说明减负能力已经形成价值。")

    if completed_count / total < 0.6:
        insights.append("完成率偏低，建议优先排查中途掉线或动作过重的问题。")
    elif helpful_count / total >= 0.6:
        insights.append("有帮助率已经不错，下一步更适合做小步 patch，而不是大改结构。")

    return insights[:5]


def derive_recommendations(
    *,
    failure_reason_counter: Counter[str],
    failure_tag_counter: Counter[str],
    entered_counter: Counter[str],
    feedback_counter: Counter[str],
    total: int,
    overwhelmed_count: int,
) -> list[str]:
    recs: list[str] = []

    top_reason = failure_reason_counter.most_common(1)
    if top_reason:
        reason = top_reason[0][0]
        if reason == "too_many_questions":
            recs.append("压缩 cold_start 的问题密度，尽早转为候选项选择。")
        elif reason == "wrong_route":
            recs.append("优先优化 router，降低误路由到冷启动或错误 flow 的概率。")
        elif reason == "not_actionable":
            recs.append("优先优化 today_plan，把最小动作缩小到更容易开始的粒度。")
        elif reason == "too_heavy":
            recs.append("降低动作负担，增加 5 分钟版本和更轻的 fallback。")
        elif reason == "too_abstract":
            recs.append("加强具体化表达，让输出更快落到现实动作。")

    top_tag = failure_tag_counter.most_common(1)
    if top_tag:
        tag = top_tag[0][0]
        if tag == "low_energy_dropoff":
            recs.append("优化低能量场景的收束方式，减少追问，优先减负。")

    if total > 0 and overwhelmed_count / total >= 0.2:
        recs.append("给 overwhelmed_mode 再加一层极低负担兜底。")

    clarified = feedback_counter.get("clarified_priority", 0)
    next_step = feedback_counter.get("defined_next_step", 0)
    if clarified > next_step:
        recs.append("优先补强从“看清”到“行动”的转化，重点改 today_plan。")

    if entered_counter and entered_counter.get("cold_start", 0) >= max(entered_counter.values() or [0]):
        recs.append("持续优化 cold_start，因为它仍是最主要入口。")

    deduped: list[str] = []
    for item in recs:
        if item not in deduped:
            deduped.append(item)
    return deduped[:3]


def suggest_version_bump(
    *,
    total: int,
    failure_reason_counter: Counter[str],
    failure_tag_counter: Counter[str],
    helpful_rate: float,
) -> tuple[str, str]:
    if total == 0:
        return "none", "0.2.1"

    top_failure_count = failure_reason_counter.most_common(1)[0][1] if failure_reason_counter else 0
    top_tag_count = failure_tag_counter.most_common(1)[0][1] if failure_tag_counter else 0

    if helpful_rate >= 0.6 and top_failure_count < 5 and top_tag_count < 5:
        return "none", "0.2.1"

    if top_failure_count >= 3 or top_tag_count >= 3:
        return "patch", "0.2.2"

    return "patch", "0.2.2"


def build_changelog(summary: dict[str, Any]) -> str:
    version = summary.get("suggestedNextVersion", "0.2.2")
    focus = summary.get("recommendedFocus", [])
    if not focus:
        return f"{version}: maintenance improvements based on weekly review."
    short = "; ".join(focus[:3])
    return f"{version}: {short}"


def render_markdown_report(summary: dict[str, Any]) -> str:
    def render_counter_block(title: str, data: dict[str, int]) -> str:
        lines = [f"## {title}"]
        if not data:
            lines.append("- 暂无数据")
            return "\n".join(lines)
        for key, value in sorted(data.items(), key=lambda x: x[1], reverse=True):
            lines.append(f"- {key}: {value}")
        return "\n".join(lines)

    lines = [
        "# Priority Coach Weekly Review",
        "",
        f"时间范围：最近 {summary['windowDays']} 天",
        f"生成时间：{summary['generatedAt']}",
        "",
        "## 1. 本周概览",
        f"- 总会话数：{summary['totalSessions']}",
        f"- 完成率：{summary['completionRate']:.0%}",
        f"- 保存结果率：{summary['saveRate']:.0%}",
        f"- 有帮助率：{summary['helpfulRate']:.0%}",
        f"- overwhelmed 命中率：{summary['overwhelmedRate']:.0%}",
        "",
        render_counter_block("2. 状态分布", summary["stateDistribution"]),
        "",
        render_counter_block("3. 反馈结果", summary["feedbackOutcomeDistribution"]),
        "",
        render_counter_block("4. 失败原因", summary["failureReasonDistribution"]),
        "",
        render_counter_block("5. 失败标签", summary["failureTagDistribution"]),
        "",
        render_counter_block("6. 结果类型", summary["resultTypeDistribution"]),
        "",
        "## 7. 本周观察",
    ]

    insights = summary.get("topInsights", [])
    if insights:
        for item in insights:
            lines.append(f"- {item}")
    else:
        lines.append("- 暂无明显观察")

    lines.extend(["", "## 8. 建议优先修复点"])
    recs = summary.get("recommendedFocus", [])
    if recs:
        for idx, item in enumerate(recs, start=1):
            lines.append(f"{idx}. {item}")
    else:
        lines.append("- 暂无明确建议")

    lines.extend([
        "",
        "## 9. AI 建议",
        f"- 建议是否发版：{summary['recommendedVersionBump']}",
        f"- 建议版本号：{summary['suggestedNextVersion']}",
        "",
        "## 10. changelog 草稿",
        build_changelog(summary),
        "",
    ])

    return "\n".join(lines)


def render_review_prompt(summary: dict[str, Any]) -> str:
    payload = json.dumps(summary, ensure_ascii=False, indent=2)
    return f"""你是 priority-coach 的维护助手。请基于下面这份周报数据，给出：

1. 本周最重要的 3 个问题
2. 这些问题更像出在 router / states / daily-flows / copy-tone / record 哪一层
3. 建议是否发版（不发 / patch / minor）
4. 如果发版，建议修改哪些文件
5. 给出一版 changelog 草稿

要求：
- 不要泛泛而谈
- 优先改最影响主流程的问题
- 一次最多建议改 1–3 个点
- 不要建议大而全的新功能，除非数据明确支持

下面是数据：
{payload}
"""


def ensure_parent(path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)


def write_text(path: Path | None, content: str) -> None:
    if path is None:
        return
    ensure_parent(path)
    path.write_text(content, encoding="utf-8")


def write_json(path: Path | None, data: dict[str, Any]) -> None:
    if path is None:
        return
    ensure_parent(path)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Priority Coach weekly report generator")
    parser.add_argument("--input", help="sessions.json path")
    parser.add_argument("--days", type=int, default=7, help="look back N days (default: 7)")
    parser.add_argument("--limit", type=int, help="max number of sessions after filtering")
    parser.add_argument("--output", help="markdown report output path")
    parser.add_argument("--json-output", help="json summary output path")
    parser.add_argument("--prompt-output", help="AI review prompt output path")
    parser.add_argument("--stdout", action="store_true", help="print markdown report to stdout")
    return parser


def main() -> int:
    args = build_parser().parse_args()

    input_path = detect_input_path(args.input)
    store = load_store(input_path)
    normalized_sessions = [
        session for session in (normalize_session_summary(item) for item in store.get("sessions", [])) if session is not None
    ]
    sessions = filter_sessions(normalized_sessions, days=args.days, limit=args.limit)

    summary = summarize(sessions)
    summary["windowDays"] = args.days
    summary["inputPath"] = str(input_path)

    markdown = render_markdown_report(summary)
    prompt = render_review_prompt(summary)

    output_path = Path(args.output).expanduser() if args.output else None
    json_output_path = Path(args.json_output).expanduser() if args.json_output else None
    prompt_output_path = Path(args.prompt_output).expanduser() if args.prompt_output else None

    write_text(output_path, markdown)
    write_json(json_output_path, summary)
    write_text(prompt_output_path, prompt)

    if args.stdout or not any([output_path, json_output_path, prompt_output_path]):
        print(markdown)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())

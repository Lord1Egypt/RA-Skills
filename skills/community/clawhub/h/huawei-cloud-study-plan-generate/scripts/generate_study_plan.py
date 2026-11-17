#!/usr/bin/env python3
"""Generate a random, constraint-respecting study-practice plan.

This is a self-contained generator built on the Python 3 standard library only.
It lays out a plan as ``day x time slot`` cells, assigns a study topic and a
practice item to every cell, keeps a topic from repeating until the topic pool is
exhausted, keeps a day's slots non-overlapping in time, and prints the result as
a Markdown table (or plain text / JSON). A ``--seed`` value makes any run
reproducible.

It does not call the Huawei Cloud CLI, any Huawei Cloud SDK, or any REST API, and
it touches no cloud resource.
"""
import argparse
import datetime as _dt
import json
import random
import sys
from pathlib import Path

DEFAULT_TOPICS_FILE = Path(__file__).resolve().parent / "topics.json"

# Nominal length of one study session, in minutes (``--session-minutes`` default).
DEFAULT_SESSION_MINUTES = 45
# Random variation applied around the nominal session length so durations vary
# inside a bounded, reasonable interval.
SESSION_JITTER_MINUTES = 10
# Hard bounds for a single session length; the upper bound is kept below the
# smallest gap between two slot start times so slots never overlap.
MIN_MINUTES = 15
MAX_MINUTES = 110
MINUTE_STEP = 5

# Ordered slot templates: (label, start time). The first ``--slots-per-day``
# entries are used and then rendered in chronological order. Every pair of start
# times is at least 120 minutes apart, which is greater than MAX_MINUTES, so a
# day's slots never overlap in time.
SLOT_TEMPLATES = [
    ("上午", "09:00"),
    ("下午", "13:00"),
    ("晚上", "19:00"),
    ("早读", "07:00"),
    ("午间", "11:00"),
    ("傍晚", "17:00"),
    ("夜读", "21:00"),
]


def _start_minutes(start):
    hh, mm = (int(x) for x in start.split(":"))
    return hh * 60 + mm

_GENERIC_PRACTICE_TEMPLATES = [
    "围绕《{topic}》完成一次动手练习",
    "整理《{topic}》的要点笔记并复述",
    "用《{topic}》解决一个小问题",
]

_WEEKDAY_NAMES = ["周一", "周二", "周三", "周四", "周五", "周六", "周日"]


def load_topics(override=None):
    """Return a list of ``{"topic": str, "practices": [str, ...]}`` dicts.

    ``override`` may be:
      * ``None`` -> the built-in topic pool shipped as ``scripts/topics.json``;
      * a path to a JSON file -> that file (either ``{"topics": [...]}`` or a
        bare list);
      * a comma separated string of topic names -> a pool built on the fly with
        generic practice items.
    """
    if override is None:
        with open(DEFAULT_TOPICS_FILE, encoding="utf-8") as fh:
            data = json.load(fh)
        raw = data.get("topics", data) if isinstance(data, dict) else data
        return _normalize_pool(raw)

    candidate = Path(override)
    if candidate.is_file() and candidate.suffix.lower() == ".json":
        with open(candidate, encoding="utf-8") as fh:
            data = json.load(fh)
        raw = data.get("topics", data) if isinstance(data, dict) else data
        pool = _normalize_pool(raw)
        if not pool:
            raise ValueError(f"主题池为空: {override}")
        return pool

    names = [name.strip() for name in override.split(",") if name.strip()]
    if not names:
        raise ValueError("--topics 未提供任何主题")
    return [
        {
            "topic": name,
            "practices": [t.format(topic=name) for t in _GENERIC_PRACTICE_TEMPLATES],
        }
        for name in names
    ]


def _normalize_pool(raw):
    pool = []
    for item in raw or []:
        if isinstance(item, str):
            topic, practices = item, [_t.format(topic=item) for _t in _GENERIC_PRACTICE_TEMPLATES]
        else:
            topic = str(item.get("topic", "")).strip()
            practices = [str(p) for p in item.get("practices", []) if str(p).strip()]
            if not practices:
                practices = [t.format(topic=topic) for t in _GENERIC_PRACTICE_TEMPLATES]
        if topic:
            pool.append({"topic": topic, "practices": practices})
    return pool


def _rand_minutes(rng, base):
    lo = max(MIN_MINUTES, base - SESSION_JITTER_MINUTES)
    hi = min(MAX_MINUTES, base + SESSION_JITTER_MINUTES)
    if hi < lo:
        hi = lo
    raw = rng.randint(lo, hi)
    rounded = int(round(raw / float(MINUTE_STEP))) * MINUTE_STEP
    return max(MIN_MINUTES, min(MAX_MINUTES, rounded))


def build_plan(seed, days, slots_per_day, topics_pool, session_minutes,
               start_date=None):
    """Build the plan as a list of day dicts.

    Each day is ``{"date": "YYYY-MM-DD", "weekday": "周一", "slots": [...]}`` and
    each slot is ``{"slot": label, "start": "HH:MM", "topic": ..., "practice":
    ..., "minutes": int}``. Topics are drawn without repetition until the pool is
    exhausted, then the pool is reshuffled and reused.
    """
    rng = random.Random(seed)
    if not topics_pool:
        raise ValueError("主题池为空，无法生成计划")
    if days <= 0:
        raise ValueError("--days 必须为正整数")
    if slots_per_day <= 0:
        raise ValueError("--slots-per-day 必须为正整数")
    if slots_per_day > len(SLOT_TEMPLATES):
        raise ValueError(f"--slots-per-day 最大为 {len(SLOT_TEMPLATES)}")
    if session_minutes < MIN_MINUTES:
        raise ValueError(f"--session-minutes 不能小于 {MIN_MINUTES}")

    if start_date is None:
        start_date = _dt.date.today()
    elif isinstance(start_date, str):
        start_date = _dt.date.fromisoformat(start_date)

    slot_templates = sorted(SLOT_TEMPLATES[:slots_per_day],
                            key=lambda item: _start_minutes(item[1]))
    cycle = []

    def next_topic():
        if not cycle:
            cycle.extend(rng.sample(topics_pool, len(topics_pool)))
        return cycle.pop()

    plan = []
    for offset in range(days):
        current = start_date + _dt.timedelta(days=offset)
        day = {
            "date": current.isoformat(),
            "weekday": _WEEKDAY_NAMES[current.weekday()],
            "slots": [],
        }
        for label, start in slot_templates:
            entry = next_topic()
            day["slots"].append({
                "slot": label,
                "start": start,
                "topic": entry["topic"],
                "practice": rng.choice(entry["practices"]),
                "minutes": _rand_minutes(rng, session_minutes),
            })
        plan.append(day)
    return plan


def render_markdown(plan, seed=None):
    lines = ["# 学习实践表", ""]
    if seed is not None:
        lines.append(f"> 随机种子（seed）：{seed}")
        lines.append("")
    lines.append("| 日期 | 时段 | 学习主题 | 实践内容 | 时长(分钟) |")
    lines.append("|------|------|----------|----------|------------|")
    for day in plan:
        for slot in day["slots"]:
            date_cell = f"{day['date']}（{day['weekday']}）"
            slot_cell = f"{slot['slot']} {slot['start']}"
            lines.append(
                f"| {date_cell} | {slot_cell} | {slot['topic']} | "
                f"{slot['practice']} | {slot['minutes']} |"
            )
    return "\n".join(lines) + "\n"


def render_text(plan, seed=None):
    lines = ["学习实践表"]
    if seed is not None:
        lines.append(f"随机种子（seed）：{seed}")
    for day in plan:
        lines.append("")
        lines.append(f"{day['date']}（{day['weekday']}）")
        for slot in day["slots"]:
            lines.append(
                f"  [{slot['slot']} {slot['start']}] {slot['topic']} | "
                f"{slot['practice']} | {slot['minutes']} 分钟"
            )
    return "\n".join(lines) + "\n"


def render_json(plan, seed=None):
    payload = {"seed": seed, "plan": plan}
    return json.dumps(payload, ensure_ascii=False, indent=2) + "\n"


def _build_parser():
    parser = argparse.ArgumentParser(
        prog="generate_study_plan.py",
        description="随机生成结构化的学习实践表（Markdown 表格 / 文本 / JSON）。",
    )
    parser.add_argument("--days", type=int, default=7, help="学习天数（默认 7）")
    parser.add_argument("--slots-per-day", type=int, default=3,
                        help="每日时段数，最大 7（默认 3）")
    parser.add_argument("--topics", default=None,
                        help="主题池覆盖：逗号分隔的主题名，或一个 JSON 文件路径（默认内置主题池）")
    parser.add_argument("--session-minutes", type=int, default=DEFAULT_SESSION_MINUTES,
                        help=f"单时段名义时长（分钟），实际在 ±{SESSION_JITTER_MINUTES} 区间内随机（默认 "
                             f"{DEFAULT_SESSION_MINUTES}）")
    parser.add_argument("--start-date", default=None,
                        help="起始日期 YYYY-MM-DD（默认今天）")
    parser.add_argument("--seed", type=int, default=None,
                        help="随机种子；省略时随机取一个并打印，便于复现")
    parser.add_argument("--format", choices=["markdown", "text", "json"],
                        default="markdown", help="输出格式（默认 markdown）")
    parser.add_argument("--output", default=None, help="写入文件（默认输出到标准输出）")
    return parser


def main(argv=None):
    parser = _build_parser()
    args = parser.parse_args(argv)

    seed = args.seed if args.seed is not None else random.SystemRandom().randint(0, 2 ** 31 - 1)

    try:
        topics_pool = load_topics(args.topics)
        plan = build_plan(
            seed=seed,
            days=args.days,
            slots_per_day=args.slots_per_day,
            topics_pool=topics_pool,
            session_minutes=args.session_minutes,
            start_date=args.start_date,
        )
    except (ValueError, OSError, json.JSONDecodeError) as exc:
        print(f"错误: {exc}", file=sys.stderr)
        return 2

    show_seed = seed if args.seed is None else args.seed
    if args.format == "markdown":
        out = render_markdown(plan, seed=show_seed)
    elif args.format == "text":
        out = render_text(plan, seed=show_seed)
    else:
        out = render_json(plan, seed=show_seed)

    if args.output:
        Path(args.output).write_text(out, encoding="utf-8")
    else:
        sys.stdout.write(out)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
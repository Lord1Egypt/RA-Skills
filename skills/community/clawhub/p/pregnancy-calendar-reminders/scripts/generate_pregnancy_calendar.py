#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import re
from dataclasses import dataclass
from datetime import date, datetime, time, timedelta, timezone
from pathlib import Path


TZID = "Asia/Shanghai"
LOCAL_OFFSET = timezone(timedelta(hours=8))
DEFAULT_DAILY_TIME = "20:30"
DEFAULT_KEY_TIME = "09:00"
UID_DOMAIN = "pregnancy-calendar-reminders.codex.local"


@dataclass(frozen=True)
class WindowSpec:
    name: str
    start_week: int
    start_day: int
    end_week: int
    end_day: int
    medical: str
    family: str
    short: str


WINDOW_SPECS = [
    WindowSpec(
        "早孕确认期",
        5,
        0,
        8,
        0,
        "预约产科门诊；按医生安排早孕超声，确认宫内妊娠及胚胎发育；有出血或腹痛及时就诊。",
        "叶酸、用药核对、避免烟酒；收集既往检查报告。",
        "早孕确认",
    ),
    WindowSpec(
        "首次系统产检/建档",
        6,
        0,
        13,
        6,
        "13周+6前完成建档、首次产检、风险评估和医院要求的基础化验。",
        "确定长期产检医院，记录血压、体重和既往史。",
        "建档/首检",
    ),
    WindowSpec(
        "NT筛查窗口",
        11,
        0,
        13,
        6,
        "按预约完成NT超声；结合医生建议选择后续产前筛查或诊断路径。",
        "不要把NT与无创DNA视为同一项检查。",
        "NT",
    ),
    WindowSpec(
        "无创DNA可适用窗口",
        12,
        0,
        22,
        6,
        "NIPT需经正规机构、知情同意后进行，用于常见染色体非整倍体风险评估。",
        "是否做、何时做由产科结合年龄、筛查结果及意愿决定。",
        "NIPT",
    ),
    WindowSpec(
        "孕中期随访",
        14,
        0,
        19,
        6,
        "按医生方案常规产检、血清学筛查或相关评估。",
        "保持均衡饮食和适量活动。",
        "中期随访",
    ),
    WindowSpec(
        "胎儿系统超声",
        20,
        0,
        24,
        0,
        "完成胎儿结构筛查超声，评估重要器官结构与发育。",
        "关键预约项目，建议提前挂号。",
        "系统超声",
    ),
    WindowSpec(
        "妊娠期糖尿病筛查",
        24,
        0,
        28,
        0,
        "通常安排75 g OGTT，并结合医嘱复查血常规、尿常规等。",
        "按医院要求准备，不擅自节食“控结果”。",
        "糖耐/OGTT",
    ),
    WindowSpec(
        "生长评估期",
        29,
        0,
        32,
        0,
        "常规产检；医生根据情况安排胎儿生长、胎位、羊水等评估。",
        "明确分娩医院、陪护安排和待产物资清单。",
        "生长评估",
    ),
    WindowSpec(
        "孕晚期准备",
        33,
        0,
        36,
        6,
        "监测胎动、血压与临产风险；GBS筛查、胎心监护等按医院或个人风险安排。",
        "准备证件、住院包和就医路线。",
        "晚孕准备",
    ),
    WindowSpec(
        "足月待产",
        37,
        0,
        41,
        0,
        "按产科频率复诊，评估胎动、宫缩、胎心及分娩时机；超过预产期听从医生安排。",
        "规律宫缩、破水、出血或胎动明显减少，及时就医。",
        "足月待产",
    ),
]


@dataclass(frozen=True)
class Window:
    name: str
    start: date
    end: date
    medical: str
    family: str
    short: str


def parse_date(value: str) -> date:
    try:
        return date.fromisoformat(value)
    except ValueError as exc:
        raise argparse.ArgumentTypeError(f"Invalid date '{value}', expected YYYY-MM-DD") from exc


def parse_clock(value: str) -> time:
    if not re.fullmatch(r"\d{2}:\d{2}", value):
        raise argparse.ArgumentTypeError(f"Invalid time '{value}', expected HH:MM")
    hour, minute = [int(part) for part in value.split(":")]
    if not (0 <= hour <= 23 and 0 <= minute <= 59):
        raise argparse.ArgumentTypeError(f"Invalid time '{value}', expected HH:MM")
    return time(hour, minute)


def ga_date(lmp: date, weeks: int, days: int = 0) -> date:
    return lmp + timedelta(days=weeks * 7 + days)


def gestational_age(day: date, lmp: date) -> tuple[int, int]:
    delta = (day - lmp).days
    weeks, days = divmod(delta, 7)
    return weeks, days


def gestational_age_text(day: date, lmp: date) -> str:
    weeks, days = gestational_age(day, lmp)
    return f"孕{weeks}周+{days}天"


def format_date(day: date) -> str:
    return f"{day.year}年{day.month}月{day.day}日"


def build_windows(lmp: date) -> list[Window]:
    return [
        Window(
            spec.name,
            ga_date(lmp, spec.start_week, spec.start_day),
            ga_date(lmp, spec.end_week, spec.end_day),
            spec.medical,
            spec.family,
            spec.short,
        )
        for spec in WINDOW_SPECS
    ]


def active_windows(day: date, windows: list[Window]) -> list[Window]:
    return [window for window in windows if window.start <= day <= window.end]


def summary_for_day(day: date, lmp: date, windows: list[Window]) -> str:
    active = active_windows(day, windows)
    short = "/".join(window.short for window in active[:4]) if active else "日常管理"
    return f"{gestational_age_text(day, lmp)}｜{short}"


def daily_description(day: date, lmp: date, due: date, windows: list[Window], source_note: str) -> str:
    lines = [
        f"{gestational_age_text(day, lmp)}。本提醒按{source_note}生成，不能替代医生个体化安排。",
        "",
        "每日固定提醒：",
    ]
    weeks, _ = gestational_age(day, lmp)
    if weeks < 14:
        lines.append("- 叶酸/复合维生素按医嘱；核对叶酸含量，避免重复超量。")
    else:
        lines.append("- 补充剂、铁剂、钙、维生素D或DHA按膳食、化验和医生建议，不自行加量。")

    lines.extend(
        [
            "- 观察危险信号：阴道出血、持续或剧烈腹痛、晕厥/明显头晕、严重呕吐无法进食饮水、发热、呼吸困难、胸痛或明显不适，尽快就医。",
            "- 生活底线：避免烟酒和二手烟；食物充分加热；咖啡因控制在每天少于200 mg；新增药物、保健品或外用药先咨询医生。",
            "- 准爸爸任务：更新产检资料袋，记录近期症状、服用品、检查单和想问医生的问题。",
        ]
    )

    if day < ga_date(lmp, 14, 0):
        lines.append("- 当前重点：完成/核对建档、首次产检、NT和产前筛查路径。")
    elif day <= ga_date(lmp, 28, 0):
        lines.append("- 当前重点：按预约随访，关注体重、血压、贫血风险、运动耐受和关键检查窗口。")
    else:
        lines.append("- 当前重点：按医生频率产检，关注胎动、血压、胎位、羊水与分娩准备。")

    if day > ga_date(lmp, 28, 0):
        lines.append("- 胎动提醒：了解宝宝日常胎动规律；明显减少、消失或和平时显著不同，立即联系产科。")

    active = active_windows(day, windows)
    if active:
        lines.extend(["", "当前产检窗口："])
        for window in active:
            lines.append(f"- {window.name}（{format_date(window.start)}-{format_date(window.end)}）：{window.medical} 家庭提醒：{window.family}")

    upcoming = [window for window in windows if day < window.start <= day + timedelta(days=7)]
    if upcoming:
        lines.extend(["", "未来7天即将进入："])
        for window in upcoming:
            lines.append(f"- {window.name}：{format_date(window.start)}开始，建议提前预约/核对流程。")

    if day == due:
        lines.extend(["", "今天是预计预产期。实际分娩与产检安排以产科医生评估为准。"])

    return "\n".join(lines)


def key_events(lmp: date, due: date, start: date, source_note: str) -> list[tuple[date, str, str, list[int]]]:
    items = [
        (
            start,
            "当前孕周与待办核对",
            f"今天按{source_note}重算为{gestational_age_text(start, lmp)}。请核对当前孕周窗口、已完成检查、下一次产检时间、医生问题清单和资料袋。",
            [0],
        ),
        (
            ga_date(lmp, 5, 0),
            "窗口开始：早孕确认期",
            "预约产科门诊；按医生安排早孕超声，确认宫内妊娠及胚胎发育；若有出血/腹痛及时就诊。",
            [-10080, -1440, 0],
        ),
        (
            ga_date(lmp, 8, 0),
            "窗口临近结束：早孕确认期",
            "如仍未完成早孕产科就诊或超声，尽快联系医院；危险信号不等待预约。",
            [-1440, 0],
        ),
        (
            ga_date(lmp, 11, 0),
            "窗口开始：NT筛查",
            "孕11-13周+6天完成NT超声；同时核对建档和首次系统产检项目。",
            [-10080, -1440, 0],
        ),
        (
            ga_date(lmp, 12, 0),
            "窗口开始：NIPT可适用",
            "无创DNA是血液筛查，需正规机构与知情同意；是否做、何时做听产科建议。",
            [-10080, -1440, 0],
        ),
        (
            ga_date(lmp, 13, 6),
            "窗口临近结束：NT/建档首检",
            "确认NT、建档、首次系统产检与后续产前筛查路径是否完成或已预约。",
            [-10080, -1440, 0],
        ),
        (
            ga_date(lmp, 20, 0),
            "窗口开始：胎儿系统超声",
            "孕20-24周完成胎儿结构筛查超声，属于关键预约项目，建议提前挂号。",
            [-10080, -1440, 0],
        ),
        (
            ga_date(lmp, 22, 6),
            "窗口临近结束：NIPT可适用期",
            "如仍需讨论NIPT或其他筛查/诊断方案，尽快与产科确认。",
            [-10080, -1440, 0],
        ),
        (
            ga_date(lmp, 24, 0),
            "窗口开始：糖耐/OGTT",
            "孕24-28周通常安排75 g OGTT；检查前按医院要求准备，不擅自节食“控结果”。",
            [-10080, -1440, 0],
        ),
        (
            ga_date(lmp, 28, 0),
            "窗口临近结束：糖耐/OGTT",
            "确认OGTT及血常规、尿常规等相应复查是否完成，并记录医生对饮食、运动、复查的建议。",
            [-10080, -1440, 0],
        ),
        (
            ga_date(lmp, 29, 0),
            "窗口开始：29-32周生长评估",
            "按医生安排常规产检，必要时评估胎儿生长、胎位、羊水；开始明确分娩医院与陪护安排。",
            [-10080, -1440, 0],
        ),
        (
            ga_date(lmp, 33, 0),
            "窗口开始：孕晚期准备",
            "关注胎动规律、血压与临产风险；GBS筛查、胎心监护等按医院安排；准备证件、住院包和路线。",
            [-10080, -1440, 0],
        ),
        (
            ga_date(lmp, 37, 0),
            "窗口开始：足月待产",
            "按产科频率复诊；规律宫缩、破水、明显出血或胎动明显减少，及时就医。",
            [-10080, -1440, 0],
        ),
        (
            due,
            "预计预产期",
            f"预计预产期为{format_date(due)}；实际分娩与产检安排以医生评估为准。",
            [-10080, -1440, 0],
        ),
        (
            due + timedelta(days=7),
            "41周提醒：超过预产期请按医生安排复诊",
            "若仍未分娩，需严格按产科安排评估胎动、胎心、羊水、宫缩和分娩时机。",
            [-10080, -1440, 0],
        ),
    ]
    return [item for item in items if item[0] >= start]


def dt_local(day: date, clock: time) -> datetime:
    return datetime.combine(day, clock, tzinfo=LOCAL_OFFSET)


def make_event(uid: str, day: date, clock: time, minutes: int, summary: str, description: str, alarms: list[int]) -> dict:
    start = dt_local(day, clock)
    end = start + timedelta(minutes=minutes)
    return {
        "uid": uid,
        "date": day.isoformat(),
        "summary": summary,
        "description": description,
        "start": start.isoformat(),
        "end": end.isoformat(),
        "alarms": alarms,
    }


def slug(text: str) -> str:
    keep: list[str] = []
    for ch in text:
        if ch.isascii() and ch.isalnum():
            keep.append(ch.lower())
        elif ch in "-_/":
            keep.append("-")
    return "".join(keep) or str(abs(hash(text)))


def build_events(lmp: date, due: date, start: date, end: date, daily_clock: time, key_clock: time, source_note: str) -> tuple[list[dict], list[Window]]:
    windows = build_windows(lmp)
    events: list[dict] = []
    day = start
    uid_stem = f"pregnancy-{due.isoformat()}"
    while day <= end:
        events.append(
            make_event(
                f"{uid_stem}-daily-{day.isoformat()}@{UID_DOMAIN}",
                day,
                daily_clock,
                10,
                summary_for_day(day, lmp, windows),
                daily_description(day, lmp, due, windows, source_note),
                [0],
            )
        )
        day += timedelta(days=1)

    for day, title, description, alarms in key_events(lmp, due, start, source_note):
        usable_alarms = [alarm for alarm in alarms if day + timedelta(minutes=alarm) >= start]
        if not usable_alarms:
            usable_alarms = [0]
        events.append(
            make_event(
                f"{uid_stem}-key-{day.isoformat()}-{slug(title)}@{UID_DOMAIN}",
                day,
                key_clock,
                30,
                f"产检提醒｜{title}",
                description,
                usable_alarms,
            )
        )

    return events, windows


def ics_escape(value: str) -> str:
    return (
        value.replace("\\", "\\\\")
        .replace(";", "\\;")
        .replace(",", "\\,")
        .replace("\n", "\\n")
    )


def ics_fold(line: str) -> str:
    raw = line.encode("utf-8")
    chunks: list[bytes] = []
    while len(raw) > 75:
        cut = 75
        while cut > 0 and (raw[cut] & 0b1100_0000) == 0b1000_0000:
            cut -= 1
        chunks.append(raw[:cut])
        raw = raw[cut:]
    chunks.append(raw)
    return "\r\n ".join(chunk.decode("utf-8") for chunk in chunks)


def utc_stamp() -> str:
    return datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")


def write_ics(events: list[dict], path: Path, calendar_name: str) -> None:
    stamp = utc_stamp()
    lines = [
        "BEGIN:VCALENDAR",
        "VERSION:2.0",
        "PRODID:-//Codex//Pregnancy Calendar Reminders//CN",
        "CALSCALE:GREGORIAN",
        "METHOD:PUBLISH",
        f"X-WR-CALNAME:{ics_escape(calendar_name)}",
        f"X-WR-TIMEZONE:{TZID}",
        "BEGIN:VTIMEZONE",
        f"TZID:{TZID}",
        "BEGIN:STANDARD",
        "DTSTART:19700101T000000",
        "TZOFFSETFROM:+0800",
        "TZOFFSETTO:+0800",
        "TZNAME:CST",
        "END:STANDARD",
        "END:VTIMEZONE",
    ]
    for event in events:
        start = datetime.fromisoformat(event["start"])
        end = datetime.fromisoformat(event["end"])
        lines.extend(
            [
                "BEGIN:VEVENT",
                f"UID:{event['uid']}",
                f"DTSTAMP:{stamp}",
                f"DTSTART;TZID={TZID}:{start.strftime('%Y%m%dT%H%M%S')}",
                f"DTEND;TZID={TZID}:{end.strftime('%Y%m%dT%H%M%S')}",
                f"SUMMARY:{ics_escape(event['summary'])}",
                f"DESCRIPTION:{ics_escape(event['description'])}",
            ]
        )
        for alarm in event["alarms"]:
            trigger = "PT0M" if alarm == 0 else f"-PT{abs(alarm)}M"
            lines.extend(
                [
                    "BEGIN:VALARM",
                    "ACTION:DISPLAY",
                    f"DESCRIPTION:{ics_escape(event['summary'])}",
                    f"TRIGGER:{trigger}",
                    "END:VALARM",
                ]
            )
        lines.append("END:VEVENT")
    lines.append("END:VCALENDAR")
    path.write_text("\r\n".join(ics_fold(line) for line in lines) + "\r\n", encoding="utf-8")


def write_outline(path: Path, events: list[dict], windows: list[Window], lmp_input: date | None, doctor_due: date | None, lmp: date, due: date, start: date, end: date, calendar_name: str, daily_clock: time) -> None:
    lines = [
        "# 孕期提醒日历核对表",
        "",
        f"- 日历名称：{calendar_name}",
        f"- 输入末次月经：{format_date(lmp_input) if lmp_input else '未提供'}",
        f"- 医生校正预产期：{format_date(doctor_due) if doctor_due else '未提供'}",
        f"- 实际孕周锚点：{format_date(lmp)}",
        f"- 预计预产期：{format_date(due)}",
        f"- 日历提醒范围：{format_date(start)} 至 {format_date(end)}",
        f"- 每日提醒时间：{daily_clock.strftime('%H:%M')}（{TZID}）",
        f"- 事件总数：{len(events)}",
        "",
        "## 关键产检窗口",
        "",
    ]
    for window in windows:
        lines.append(f"- {format_date(window.start)}-{format_date(window.end)}：{window.name}。{window.medical} 家庭提醒：{window.family}")
    lines.extend(
        [
            "",
            "## 校验结论",
            "",
            f"- 预产期孕周：{gestational_age_text(due, lmp)}",
            f"- 41周日期：{format_date(due + timedelta(days=7))}",
            f"- 每日提醒数：{sum(1 for event in events if '-daily-' in event['uid'])}",
            f"- 关键提醒数：{sum(1 for event in events if '-key-' in event['uid'])}",
        ]
    )
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def validate(events: list[dict], windows: list[Window], lmp: date, due: date, start: date, end: date, ics_path: Path | None = None) -> list[str]:
    errors: list[str] = []
    if due - lmp != timedelta(days=280):
        errors.append("EDD - LMP anchor is not 280 days")
    if gestational_age(due, lmp) != (40, 0):
        errors.append("Due date is not 40周+0天")
    if gestational_age(end, lmp) != (41, 0):
        errors.append("End date is not 41周+0天")
    if any(window.start > window.end for window in windows):
        errors.append("A window has start date after end date")
    if any(date.fromisoformat(event["date"]) < start for event in events):
        errors.append("An event is before calendar start")
    uids = [event["uid"] for event in events]
    if len(set(uids)) != len(uids):
        errors.append("Duplicate event UID found")
    due_events = [event for event in events if event["summary"] == "产检提醒｜预计预产期"]
    if start <= due and len(due_events) != 1:
        errors.append("Expected exactly one due-date key event")
    if ics_path and ics_path.exists():
        text = ics_path.read_text(encoding="utf-8")
        if text.count("BEGIN:VEVENT") != text.count("END:VEVENT"):
            errors.append("ICS BEGIN:VEVENT and END:VEVENT counts differ")
        if text.count("BEGIN:VEVENT") != len(events):
            errors.append("ICS event count differs from JSON/report event count")
    return errors


def resolve_anchors(args: argparse.Namespace) -> tuple[date | None, date | None, date, date, str]:
    lmp_input: date | None = args.lmp
    doctor_due: date | None = args.doctor_due or args.due
    if not lmp_input and not doctor_due:
        raise SystemExit("Provide --lmp YYYY-MM-DD or --doctor-due YYYY-MM-DD/--due YYYY-MM-DD")
    if doctor_due:
        lmp_anchor = doctor_due - timedelta(days=280)
        due = doctor_due
        if lmp_input:
            expected_due = lmp_input + timedelta(days=280)
            diff = (doctor_due - expected_due).days
            if diff == 0:
                source_note = f"末次月经{format_date(lmp_input)}和医生预产期{format_date(doctor_due)}"
            else:
                source_note = f"医生校正预产期{format_date(doctor_due)}（相对末次月经推算差{diff:+d}天）"
        else:
            source_note = f"医生校正预产期{format_date(doctor_due)}"
    else:
        lmp_anchor = lmp_input
        due = lmp_input + timedelta(days=280)
        source_note = f"末次月经{format_date(lmp_input)}"
    return lmp_input, doctor_due, lmp_anchor, due, source_note


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate a verified pregnancy reminder calendar (.ics).")
    parser.add_argument("--lmp", type=parse_date, help="Last menstrual period date, YYYY-MM-DD.")
    parser.add_argument("--due", type=parse_date, help="Estimated due date, YYYY-MM-DD. Alias for --doctor-due.")
    parser.add_argument("--doctor-due", type=parse_date, help="Doctor-adjusted due date after NT or other assessment, YYYY-MM-DD.")
    parser.add_argument("--start", type=parse_date, help="Calendar reminder start date. Defaults to today unless --include-past is set.")
    parser.add_argument("--include-past", action="store_true", help="Start the calendar at the LMP anchor instead of today/start.")
    parser.add_argument("--end", type=parse_date, help="Calendar end date. Defaults to due date + 7 days (41周+0天).")
    parser.add_argument("--daily-time", type=parse_clock, default=parse_clock(DEFAULT_DAILY_TIME), help="Daily reminder time, HH:MM.")
    parser.add_argument("--key-time", type=parse_clock, default=parse_clock(DEFAULT_KEY_TIME), help="Key event reminder time, HH:MM.")
    parser.add_argument("--calendar-name", help="Calendar display name inside ICS.")
    parser.add_argument("--output-dir", type=Path, default=Path.cwd(), help="Output directory.")
    parser.add_argument("--prefix", default="pregnancy_reminders", help="Output file prefix.")
    args = parser.parse_args()

    lmp_input, doctor_due, lmp, due, source_note = resolve_anchors(args)
    today = datetime.now(LOCAL_OFFSET).date()
    start = lmp if args.include_past else (args.start or max(today, lmp))
    end = args.end or due + timedelta(days=7)
    if start > end:
        raise SystemExit(f"Start date {start.isoformat()} is after end date {end.isoformat()}")

    calendar_name = args.calendar_name or f"孕期提醒 - {due.isoformat()}版"
    out_dir = args.output_dir
    out_dir.mkdir(parents=True, exist_ok=True)
    safe_due = due.isoformat()
    base = f"{args.prefix}_due_{safe_due}"
    json_path = out_dir / f"{base}.json"
    ics_path = out_dir / f"{base}.ics"
    outline_path = out_dir / f"{base}_outline.md"
    report_path = out_dir / f"{base}_validation.json"

    events, windows = build_events(lmp, due, start, end, args.daily_time, args.key_time, source_note)
    write_ics(events, ics_path, calendar_name)
    errors = validate(events, windows, lmp, due, start, end, ics_path)
    write_outline(outline_path, events, windows, lmp_input, doctor_due, lmp, due, start, end, calendar_name, args.daily_time)

    payload = {
        "calendar_name": calendar_name,
        "input_lmp": lmp_input.isoformat() if lmp_input else None,
        "doctor_due": doctor_due.isoformat() if doctor_due else None,
        "active_lmp_anchor": lmp.isoformat(),
        "due": due.isoformat(),
        "start": start.isoformat(),
        "end": end.isoformat(),
        "timezone": TZID,
        "event_count": len(events),
        "daily_event_count": sum(1 for event in events if "-daily-" in event["uid"]),
        "key_event_count": sum(1 for event in events if "-key-" in event["uid"]),
        "windows": [
            {
                "name": window.name,
                "start": window.start.isoformat(),
                "end": window.end.isoformat(),
                "medical": window.medical,
                "family": window.family,
            }
            for window in windows
        ],
        "files": {
            "ics": str(ics_path),
            "json": str(json_path),
            "outline": str(outline_path),
            "validation": str(report_path),
        },
        "validation_passed": not errors,
        "validation_errors": errors,
    }
    json_path.write_text(json.dumps(events, ensure_ascii=False, indent=2), encoding="utf-8")
    report_path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")

    print(json.dumps(payload, ensure_ascii=False, indent=2))
    if errors:
        raise SystemExit(1)


if __name__ == "__main__":
    main()

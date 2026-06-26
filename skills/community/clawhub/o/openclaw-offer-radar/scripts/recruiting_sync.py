#!/usr/bin/env python3
import argparse
import datetime as dt
import hashlib
import json
import os
import re
import shlex
import subprocess
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any


REPO_ROOT = Path(__file__).resolve().parents[1]
STATE_PATH = Path(
    os.environ.get(
        "OFFER_RADAR_STATE_PATH",
        str(Path.home() / ".openclaw" / "workspace" / "memory" / "gmail-reminder-state.json"),
    )
)
REMINDERS_SCRIPT = Path(
    os.environ.get(
        "OFFER_RADAR_REMINDERS_SCRIPT",
        str(REPO_ROOT / "scripts" / "apple_reminders_bridge.py"),
    )
)

SEARCH_QUERY_TEMPLATE = "newer_than:{days}d in:inbox"
DEFAULT_DAYS = 2
DEFAULT_MAX = 60
DEFAULT_ACCOUNT = os.environ.get("GOG_ACCOUNT", "")
DEFAULT_MAIL_ACCOUNT = os.environ.get("OFFER_RADAR_MAIL_ACCOUNT", "")
DEFAULT_LIST = "OpenClaw"
DEFAULT_ACCOUNT_NAME = "iCloud"
MAIL_TIMEOUT_SECONDS = 20
MAIL_BODY_LIMIT = 12000
PAST_START_GRACE_HOURS = 2
MATCH_WINDOW_DAYS = 10
STATE_RETENTION_DAYS = 30

IGNORE_SUBJECT_KEYWORDS = (
    "投递成功",
    "收到你的申请",
    "感谢投递",
    "感谢您的应聘",
    "简历完善通知",
    "简历完善",
    "面试反馈问卷",
    "体验调研",
    "问卷",
    "进度通知",
    "邀请反馈",
)

IMPORTANT_SUBJECT_TOKENS = (
    "面试邀请",
    "面试信息有更新",
    "面试提醒",
    "AI面试",
    "笔试",
    "测评",
    "授权",
    "assessment",
)

UPDATE_KEYWORDS = (
    "更新",
    "变更",
    "调整",
    "改期",
    "重新安排",
)

PRIORITY_EVENT_TYPES = {
    "interview": 0,
    "ai_interview": 1,
    "written_exam": 2,
    "assessment": 3,
    "authorization": 4,
}

KNOWN_SENDERS = (
    "tencent.com",
    "campus.tencent.com",
    "people@mail.bytedance.net",
    "careers.bytedance.com",
    "mail.mokahr.com",
    "nowcoder.net",
    "shmail.ibeisen.com",
    "aixuexi.com",
)

COMPANY_ALIASES = (
    ("字节跳动", "字节跳动"),
    ("bytedance", "字节跳动"),
    ("腾讯", "腾讯"),
    ("pdd", "拼多多"),
    ("拼多多", "拼多多"),
    ("trip.com", "携程"),
    ("携程", "携程"),
    ("美图", "美图"),
    ("科大讯飞", "科大讯飞"),
    ("iflytek", "科大讯飞"),
    ("爱学习", "爱学习教育"),
    ("aixuexi", "爱学习教育"),
    ("高思教育", "爱学习教育"),
)

SOURCE_FAMILY_RULES = (
    ("campus.tencent.com", "tencent"),
    ("@tencent.com", "tencent"),
    ("bytedance", "bytedance"),
    ("mokahr", "mokahr"),
    ("nowcoder", "nowcoder"),
    ("ibeisen", "ibeisen"),
    ("aixuexi", "aixuexi"),
    ("meitu", "meitu"),
    ("trip.com", "trip"),
    ("pdd", "pdd"),
)

URL_RE = re.compile(r"https?://[^\s<>\u3000)）]+")


@dataclass
class CandidateMail:
    thread_id: str
    subject: str
    sender: str
    received_at: dt.datetime
    labels: list[str]
    message_count: int
    body: str = ""


@dataclass
class ReviewItem:
    thread_id: str
    subject: str
    sender: str
    received_at: dt.datetime
    reason: str

    def to_dict(self) -> dict[str, str]:
        return {
            "threadId": self.thread_id,
            "subject": self.subject,
            "sender": self.sender,
            "receivedAt": self.received_at.strftime("%Y-%m-%d %H:%M"),
            "reason": self.reason,
        }


@dataclass
class EventObservation:
    observation_key: str
    identity_key: str
    source_family: str
    company: str
    event_type: str
    lifecycle: str
    title: str
    note: str
    main_due: str
    timing: dict[str, str]
    links: list[dict[str, str]]
    received_at: dt.datetime
    role: str = ""
    source_sender: str = ""
    source_ids: list[str] = field(default_factory=list)
    source_subjects: list[str] = field(default_factory=list)
    priority: str = "high"

    def anchor_at(self) -> dt.datetime | None:
        return anchor_from_timing(self.timing)


def run_json(cmd: list[str]) -> Any:
    proc = subprocess.run(
        cmd,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
    )
    if proc.returncode != 0:
        raise RuntimeError(proc.stderr.strip() or proc.stdout.strip() or "command failed")
    return json.loads(proc.stdout)


def run_text(cmd: list[str], timeout: int | None = None) -> str:
    try:
        proc = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=timeout,
        )
    except subprocess.TimeoutExpired as exc:
        raise RuntimeError(f"command timed out after {timeout}s") from exc
    if proc.returncode != 0:
        raise RuntimeError(proc.stderr.strip() or proc.stdout.strip() or "command failed")
    return proc.stdout


def run_json_shell(command: str) -> Any:
    proc = subprocess.run(
        ["zsh", "-lc", command],
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
    )
    if proc.returncode != 0:
        raise RuntimeError(proc.stderr.strip() or proc.stdout.strip() or "command failed")
    return json.loads(proc.stdout)


def run_bridge(cmd: list[str]) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, str(REMINDERS_SCRIPT), *cmd],
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
    )


def stable_hash(payload: dict[str, Any]) -> str:
    raw = json.dumps(payload, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
    return hashlib.sha1(raw.encode("utf-8")).hexdigest()[:16]


def merge_unique(existing: list[str], incoming: list[str]) -> list[str]:
    merged = list(existing)
    seen = set(existing)
    for item in incoming:
        if item not in seen:
            merged.append(item)
            seen.add(item)
    return merged


def parse_datetime(value: str) -> dt.datetime:
    for fmt in ("%Y-%m-%d %H:%M:%S", "%Y-%m-%d %H:%M"):
        try:
            return dt.datetime.strptime(value, fmt)
        except ValueError:
            continue
    raise ValueError(f"unsupported datetime: {value}")


def parse_optional_datetime(value: str | None) -> dt.datetime | None:
    if not value:
        return None
    try:
        return parse_datetime(value)
    except ValueError:
        return None


def format_due(value: dt.datetime, with_seconds: bool = False) -> str:
    return value.strftime("%Y-%m-%d %H:%M:%S" if with_seconds else "%Y-%m-%d %H:%M")


def display_time(value: dt.datetime) -> str:
    return f"{value.month}月{value.day}日 {value.strftime('%H:%M')}"


def normalize_whitespace(text: str) -> str:
    text = text.replace("\r", "\n").replace("\u00a0", " ").replace("\ufeff", "")
    text = text.replace("\u2002", " ").replace("\u2003", " ").replace("\u2009", " ")
    lines = [line.strip() for line in text.splitlines()]
    return "\n".join(line for line in lines if line)


def applescript_escape(text: str) -> str:
    return text.replace("\\", "\\\\").replace('"', '\\"')


def extract_sender_address(sender: str) -> str:
    match = re.search(r"<([^>]+@[^>]+)>", sender)
    if match:
        return match.group(1).strip().lower()
    match = re.search(r"([A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,})", sender, re.I)
    return match.group(1).strip().lower() if match else ""


def extract_sender_hint(sender: str) -> str:
    address = extract_sender_address(sender)
    if address:
        return address
    return sender.split("<")[0].strip().strip('"')


def normalize_subject_hint(subject: str) -> str:
    lowered = subject.lower()
    for token in (
        "面试信息有更新，请您确认",
        "面试信息有更新",
        "请您确认",
        "邀请函",
        "邀请你参加",
        "校招",
        "招聘",
        "通知",
        "更新",
        "变更",
        "调整",
        "改期",
        "重新安排",
    ):
        lowered = lowered.replace(token.lower(), "")
    lowered = re.sub(r"[\W_]+", "", lowered, flags=re.U)
    return lowered[:40]


def normalize_link(url: str) -> str:
    return re.sub(r"[?#].*$", "", url).rstrip("/")


def fetch_mail_body(mail_account: str, subject: str, sender: str) -> str:
    if not mail_account:
        return ""

    escaped_account = applescript_escape(mail_account)
    escaped_subject = applescript_escape(subject)
    sender_hints = []
    sender_hint = extract_sender_hint(sender)
    if sender_hint:
        sender_hints.append(sender_hint)

    for hint in sender_hints + [""]:
        if hint:
            condition = (
                f'every message of mailbox "INBOX" of account "{escaped_account}" '
                f'whose subject contains "{escaped_subject}" and sender contains "{applescript_escape(hint)}"'
            )
        else:
            condition = (
                f'every message of mailbox "INBOX" of account "{escaped_account}" '
                f'whose subject contains "{escaped_subject}"'
            )
        script = [
            f"with timeout of {MAIL_TIMEOUT_SECONDS} seconds",
            'tell application "Mail"',
            f"set hits to ({condition})",
            'if (count of hits) is 0 then return ""',
            "set m to item 1 of hits",
            "repeat with candidateMessage in hits",
            "if (date received of candidateMessage) > (date received of m) then set m to candidateMessage",
            "end repeat",
            "set c to content of m",
            f"if (length of c) > {MAIL_BODY_LIMIT} then return text 1 thru {MAIL_BODY_LIMIT} of c",
            "return c",
            "end tell",
            "end timeout",
        ]
        cmd = ["osascript"]
        for line in script:
            cmd.extend(["-e", line])
        try:
            content = run_text(cmd, timeout=MAIL_TIMEOUT_SECONDS + 5).strip()
        except RuntimeError:
            content = ""
        if content:
            return content
    return ""


def load_candidates(account: str, days: int, max_results: int) -> list[CandidateMail]:
    account_part = f"-a {shlex.quote(account)} " if account else ""
    query = shlex.quote(SEARCH_QUERY_TEMPLATE.format(days=days))
    command = f"gog gmail search {account_part}-j --results-only {query} --max {max_results}"
    rows = run_json_shell(command)

    candidates: list[CandidateMail] = []
    for row in rows:
        received_at = dt.datetime.strptime(row["date"], "%Y-%m-%d %H:%M")
        candidates.append(
            CandidateMail(
                thread_id=row["id"],
                subject=row["subject"],
                sender=row["from"],
                received_at=received_at,
                labels=row.get("labels", []),
                message_count=row.get("messageCount", 1),
            )
        )
    return candidates


def looks_like_receipt(subject: str) -> bool:
    lowered = subject.lower()
    if any(keyword in subject for keyword in IGNORE_SUBJECT_KEYWORDS):
        return True
    if "感谢" in subject and all(token not in subject for token in ("面试", "笔试", "测评", "授权")):
        return True
    if "申请" in subject and all(token not in subject for token in ("面试", "笔试", "测评", "授权")):
        return True
    return "feedback" in lowered and "面试" not in subject


def is_candidate(mail: CandidateMail) -> bool:
    subject = mail.subject
    sender_lower = mail.sender.lower()
    if looks_like_receipt(subject):
        return False
    if any(domain in sender_lower for domain in KNOWN_SENDERS):
        if any(token.lower() in subject.lower() for token in IMPORTANT_SUBJECT_TOKENS):
            return True
    return any(token.lower() in subject.lower() for token in IMPORTANT_SUBJECT_TOKENS)


def simplify_company(name: str) -> str:
    text = name.strip()
    text = re.sub(r"(有限责任公司|股份有限公司|科技有限公司|集团公司|有限公司|公司)$", "", text)
    text = text.replace("（", "(").replace("）", ")")
    for needle, canonical in COMPANY_ALIASES:
        if needle.lower() in text.lower():
            return canonical
    return text


def detect_source_family(sender: str, subject: str, body: str) -> str:
    merged = "\n".join([sender, subject, body]).lower()
    for needle, family in SOURCE_FAMILY_RULES:
        if needle in merged:
            return family
    address = extract_sender_address(sender)
    if address and "." in address:
        host = address.split("@", 1)[1]
        return host.split(".")[0]
    return "generic"


def detect_company(subject: str, sender: str, body: str, source_family: str) -> str:
    body_patterns = (
        re.compile(r"感谢您对\s*([^\n。！!]{2,40}?)(?:有限公司|集团公司|科技有限公司|公司的)?关注"),
    )
    match = body_patterns[0].search(body)
    if match:
        return simplify_company(match.group(1))

    lowered_body = body.lower()
    if "aixuexi.com" in lowered_body:
        return "爱学习教育"

    merged = f"{subject}\n{sender}\n{body}"
    lowered = merged.lower()
    for needle, canonical in COMPANY_ALIASES:
        if needle.lower() in lowered:
            return canonical

    fallback_companies = {
        "tencent": "腾讯",
        "bytedance": "字节跳动",
        "trip": "携程",
        "pdd": "拼多多",
        "aixuexi": "爱学习教育",
        "meitu": "美图",
    }
    return fallback_companies.get(source_family, "待确认公司")


def detect_event_type(subject: str, body: str) -> str:
    merged = f"{subject}\n{body}"
    lowered = merged.lower()
    if "授权" in merged:
        return "authorization"
    if "ai面试" in lowered:
        return "ai_interview"
    if any(token in subject for token in ("面试邀请", "面试信息有更新", "面试提醒")):
        return "interview"
    if any(token in merged for token in ("面试形式", "面试时间", "加入面试", "视频面试")):
        return "interview"
    if "笔试" in merged:
        return "written_exam"
    if "测评" in merged or "assessment" in lowered:
        return "assessment"
    return "interview"


def detect_lifecycle(subject: str, body: str) -> str:
    merged = f"{subject}\n{body[:600]}"
    cancel_patterns = (
        re.compile(r"(面试|笔试|测评|授权).{0,6}(?:已)?取消"),
        re.compile(r"取消.{0,8}(面试|笔试|测评|授权)"),
        re.compile(r"本次.{0,8}(?:取消|终止|不再进行|不再安排)"),
        re.compile(r"(?:停止安排|不再进行|不再安排)"),
    )
    if any(pattern.search(merged) for pattern in cancel_patterns):
        return "cancelled"
    return "active"


def clean_role(role: str) -> str:
    text = role.strip()
    text = re.sub(r"https?://\S+", "", text)
    text = re.sub(r"(点击链接进入面试|面试地址|链接：).*", "", text)
    text = text.replace("职位", "")
    text = text.replace("产品研发-", "")
    text = re.sub(r"[（(]公共职位?[)）]", "", text)
    text = re.sub(r"\s+", "", text)
    if any(token in text for token in ("http", "meeting", "链接", "地址")):
        return ""
    return text


def extract_role(subject: str, body: str) -> str:
    department_match = re.search(r"面试部门[:：]\s*([^\n]+)", body)
    position_match = re.search(r"面试职位[:：]\s*([^\n]+)", body)
    if department_match and position_match:
        return clean_role(f"{department_match.group(1)}{position_match.group(1)}")

    patterns = (
        re.compile(r"面试职位[:：]\s*([^\n]+)"),
        re.compile(r"现邀请您就\s*([^\n，。,]+?)职位进行一次面试"),
        re.compile(r"诚邀你参加\s*([^\n，。,]+?)职位的面试"),
        re.compile(r"您应聘的([^\n，。,]+?)下的面试信息发生变化"),
    )
    for pattern in patterns:
        match = pattern.search(body)
        if match:
            return clean_role(match.group(1))

    if "QQ" in body and "客户端开发" in body:
        return "QQ客户端开发"
    if "Java" in subject or "Java" in body:
        return "Java开发实习"
    return ""


def should_include_role_in_title(event_type: str, role: str) -> bool:
    if event_type not in ("interview", "ai_interview"):
        return False
    concise = clean_role(role)
    if not concise:
        return False
    if len(concise) > 10:
        return False
    if any(token in concise for token in ("-", "－", "—", "（", "）", "(", ")", "中国", "广告")):
        return False
    return True


def parse_timing(mail: CandidateMail, event_type: str, body: str) -> dict[str, str]:
    body = normalize_whitespace(body)

    patterns = (
        re.compile(
            r"面试时间(?:\[北京时间\])?[:：]\s*(\d{4}-\d{2}-\d{2}).*?(\d{1,2}:\d{2})\s*[-~～至]\s*(\d{1,2}:\d{2})",
            re.S,
        ),
        re.compile(
            r"面试日期[:：]\s*(\d{4}-\d{2}-\d{2}).*?面试时间[:：]\s*(\d{1,2}:\d{2})(?:\s*[-~～至]\s*(\d{1,2}:\d{2}))?",
            re.S,
        ),
        re.compile(
            r"(笔试|测评)时间[:：]\s*(\d{4}-\d{2}-\d{2}).*?(\d{1,2}:\d{2})\s*[-~～至]\s*(\d{1,2}:\d{2})",
            re.S,
        ),
        re.compile(
            r"考试开始时间.*?(\d{4}-\d{2}-\d{2})\s*(\d{1,2}:\d{2}:\d{2}).*?考试结束时间.*?(\d{4}-\d{2}-\d{2})\s*(\d{1,2}:\d{2}:\d{2})",
            re.S,
        ),
        re.compile(
            r"考试时间[:：]\s*(?:\([^)]*\))?\s*(\d{4}-\d{2}-\d{2})\s*(\d{1,2}:\d{2}:\d{2})\s*--\s*(\d{1,2}:\d{2}:\d{2})",
            re.S,
        ),
    )

    for pattern in patterns:
        match = pattern.search(body)
        if not match:
            continue

        if len(match.groups()) == 4 and "考试开始时间" in pattern.pattern:
            start = parse_datetime(f"{match.group(1)} {match.group(2)}")
            end = parse_datetime(f"{match.group(3)} {match.group(4)}")
            return {
                "type": "scheduled_window",
                "start": format_due(start),
                "end": format_due(end),
            }

        if len(match.groups()) == 4 and match.group(1) in ("笔试", "测评"):
            date_part, start_text, end_text = match.group(2), match.group(3), match.group(4)
        else:
            date_part, start_text = match.group(1), match.group(2)
            end_text = match.group(3) if len(match.groups()) >= 3 else None

        start = parse_datetime(f"{date_part} {start_text}")
        timing: dict[str, str] = {"start": format_due(start)}
        if end_text:
            end = parse_datetime(f"{date_part} {end_text}")
            timing["end"] = format_due(end)
            timing["type"] = "scheduled_window"
        else:
            timing["type"] = "scheduled_start"
        return timing

    interview_start_only = re.search(
        r"面试时间[:：]\s*(\d{4}-\d{2}-\d{2})\s*(\d{1,2}:\d{2})(?::\d{2})?(?:\([^)]*\))?",
        body,
    )
    if interview_start_only:
        start = parse_datetime(f"{interview_start_only.group(1)} {interview_start_only.group(2)}")
        return {"type": "scheduled_start", "start": format_due(start)}

    explicit_deadline = re.search(
        r"(?:截止时间|截止|完成期限|有效期至)[:：]?\s*(\d{4}-\d{2}-\d{2}[ T]\d{1,2}:\d{2}(?::\d{2})?)",
        body,
    )
    if explicit_deadline:
        deadline = parse_datetime(explicit_deadline.group(1).replace("T", " "))
        return {"type": "deadline", "deadline": format_due(deadline, with_seconds=True)}

    before_deadline = re.search(
        r"(?:在|请于|请在)?\s*(\d{4}-\d{2}-\d{2})\s*(\d{1,2}:\d{2}:\d{2})(?:前|之前)",
        body,
    )
    if before_deadline:
        deadline = parse_datetime(f"{before_deadline.group(1)} {before_deadline.group(2)}")
        return {"type": "deadline", "deadline": format_due(deadline, with_seconds=True)}

    chinese_deadline = re.search(
        r"(?:于|在)?\s*(\d{4})年(\d{1,2})月(\d{1,2})日(?:[^\n]{0,12})?(\d{1,2}:\d{2})\s*(?:失效|截止)",
        body,
    )
    if chinese_deadline:
        deadline = parse_datetime(
            f"{chinese_deadline.group(1)}-{int(chinese_deadline.group(2)):02d}-{int(chinese_deadline.group(3)):02d} {chinese_deadline.group(4)}"
        )
        return {"type": "deadline", "deadline": format_due(deadline, with_seconds=True)}

    subject_deadline = re.search(r"请在(\d+)小时内完成", mail.subject)
    if subject_deadline:
        hours = int(subject_deadline.group(1))
        deadline = mail.received_at + dt.timedelta(hours=hours)
        return {"type": "deadline", "deadline": format_due(deadline, with_seconds=True)}

    generic_range = re.search(
        r"(\d{4}-\d{2}-\d{2}).*?(\d{1,2}:\d{2})\s*[-~～至]\s*(\d{1,2}:\d{2})",
        body,
        re.S,
    )
    if generic_range:
        start = parse_datetime(f"{generic_range.group(1)} {generic_range.group(2)}")
        end = parse_datetime(f"{generic_range.group(1)} {generic_range.group(3)}")
        return {
            "type": "scheduled_window",
            "start": format_due(start),
            "end": format_due(end),
        }

    return {"type": "unknown", "observedAt": format_due(mail.received_at)}


def anchor_from_timing(timing: dict[str, str]) -> dt.datetime | None:
    if timing.get("type") == "deadline" and timing.get("deadline"):
        return parse_optional_datetime(timing["deadline"])
    if timing.get("start"):
        return parse_optional_datetime(timing["start"])
    return None


def is_timing_expired(timing: dict[str, str], now: dt.datetime) -> bool:
    timing_type = timing.get("type")
    if timing_type == "deadline" and timing.get("deadline"):
        deadline = parse_optional_datetime(timing["deadline"])
        return bool(deadline and deadline < now)
    if timing_type == "scheduled_window" and timing.get("end"):
        end = parse_optional_datetime(timing["end"])
        return bool(end and end < now)
    if timing_type == "scheduled_start" and timing.get("start"):
        start = parse_optional_datetime(timing["start"])
        grace = dt.timedelta(hours=PAST_START_GRACE_HOURS)
        return bool(start and start + grace < now)
    return False


def choose_primary_link(event_type: str, urls: list[str]) -> str:
    if not urls:
        return ""

    priority_rules = {
        "interview": ("meeting.tencent.com", "teams", "zoom", "feishu"),
        "ai_interview": ("nowcoder.com/ai-interview", "exam.nowcoder.com", "meeting.tencent.com"),
        "written_exam": ("nowcoder.com", "mokahr.com", "assessment", "exam"),
        "assessment": ("assessment", "nowcoder.com", "mokahr.com"),
        "authorization": ("mokahr.com", "join.qq.com", "nowcoder.com"),
    }
    priorities = priority_rules.get(event_type, ())
    for needle in priorities:
        for url in urls:
            if needle in url:
                return url
    return urls[0]


def extract_links(body: str) -> list[str]:
    urls = URL_RE.findall(body)
    filtered: list[str] = []
    for url in urls:
        cleaned = url.rstrip(".,)")
        if cleaned not in filtered:
            filtered.append(cleaned)
    return filtered


def describe_event_label(event_type: str, subject: str) -> str:
    if event_type == "authorization":
        return "招聘授权"
    if event_type == "ai_interview":
        return "AI面试"
    if event_type == "assessment":
        return "在线测评"
    if "在线专业笔试" in subject:
        return "在线专业笔试"
    if "在线技术笔试" in subject:
        return "在线技术笔试"
    if event_type == "written_exam":
        return "在线笔试"
    return "面试"


def build_title(company: str, event_type: str, role: str, timing: dict[str, str], subject: str) -> str:
    label = describe_event_label(event_type, subject)
    title_base = company
    if should_include_role_in_title(event_type, role):
        title_base += clean_role(role)

    if timing.get("type") == "deadline" and timing.get("deadline"):
        deadline = parse_datetime(timing["deadline"])
        if event_type == "ai_interview":
            return f"{title_base}{label}（{display_time(deadline)}前完成）"
        return f"{title_base}{label}（{display_time(deadline)}截止）"

    if timing.get("start"):
        start = parse_datetime(timing["start"])
        return f"{title_base}{label}（{display_time(start)}）"

    return f"{title_base}{label}"


def build_note(event_type: str, timing: dict[str, str], role: str, primary_link: str, subject: str) -> str:
    lines: list[str] = []
    if timing.get("type") == "deadline":
        label = "完成期限" if event_type == "ai_interview" else "截止时间"
        lines.append(f"{label}：{timing['deadline']}")
    elif timing.get("start") and timing.get("end"):
        label = "面试时间" if event_type in ("interview", "ai_interview") else "笔试时间"
        lines.append(f"{label}：{timing['start']} - {timing['end'][-5:]}")
    elif timing.get("start"):
        label = "面试时间" if event_type in ("interview", "ai_interview") else "开始时间"
        lines.append(f"{label}：{timing['start']}")

    if role and event_type in ("interview", "ai_interview"):
        lines.append(f"岗位：{role}")

    if event_type == "ai_interview":
        hours_match = re.search(r"请在(\d+)小时内完成", subject)
        if hours_match:
            lines.append(f"说明：收到邮件后 {hours_match.group(1)} 小时内完成")

    if primary_link:
        lines.append(f"入口：{primary_link}")

    return "\n".join(lines)


def build_identity_key(company: str, event_type: str, role: str, source_family: str) -> str:
    role_key = clean_role(role).lower() or "generic"
    return f"{source_family}|{company}|{event_type}|{role_key}"


def build_observation_key(identity_key: str, timing: dict[str, str], subject: str) -> str:
    anchor = anchor_from_timing(timing)
    anchor_key = anchor.strftime("%Y%m%d%H%M") if anchor else "na"
    subject_hint = normalize_subject_hint(subject) or "event"
    return stable_hash(
        {
            "identityKey": identity_key,
            "anchor": anchor_key,
            "subjectHint": subject_hint,
        }
    )


def build_observation(mail: CandidateMail) -> tuple[EventObservation | None, ReviewItem | None]:
    body = normalize_whitespace(mail.body)
    source_family = detect_source_family(mail.sender, mail.subject, body)
    company = detect_company(mail.subject, mail.sender, body, source_family)
    event_type = detect_event_type(mail.subject, body)
    lifecycle = detect_lifecycle(mail.subject, body)
    role = extract_role(mail.subject, body)
    timing = parse_timing(mail, event_type, body)

    if looks_like_receipt(mail.subject):
        return None, None
    if company == "待确认公司":
        return None, ReviewItem(mail.thread_id, mail.subject, mail.sender, mail.received_at, "未能确认公司")

    links = extract_links(body)
    primary_link = choose_primary_link(event_type, links)
    if lifecycle != "cancelled":
        if timing.get("type") == "unknown":
            return None, ReviewItem(mail.thread_id, mail.subject, mail.sender, mail.received_at, "未能解析时间")
        if event_type in ("interview", "written_exam", "assessment", "authorization") and not primary_link:
            return None, ReviewItem(mail.thread_id, mail.subject, mail.sender, mail.received_at, "未找到有效入口")

    title = build_title(company, event_type, role, timing, mail.subject)
    note = build_note(event_type, timing, role, primary_link, mail.subject)
    main_due = (
        timing["deadline"]
        if timing.get("type") == "deadline"
        else timing.get("start", mail.received_at.strftime("%Y-%m-%d %H:%M"))
    )
    identity_key = build_identity_key(company, event_type, role, source_family)
    observation_key = build_observation_key(identity_key, timing, mail.subject)
    link_entries = [{"label": "入口", "url": primary_link}] if primary_link else []

    return (
        EventObservation(
            observation_key=observation_key,
            identity_key=identity_key,
            source_family=source_family,
            company=company,
            event_type=event_type,
            lifecycle=lifecycle,
            title=title,
            note=note,
            main_due=main_due,
            timing=timing,
            links=link_entries,
            received_at=mail.received_at,
            role=role,
            source_sender=mail.sender,
            source_ids=[mail.thread_id],
            source_subjects=[mail.subject],
        ),
        None,
    )


def load_observations(candidates: list[CandidateMail], mail_account: str) -> tuple[list[EventObservation], list[ReviewItem]]:
    filtered = [candidate for candidate in candidates if is_candidate(candidate)]
    observations: list[EventObservation] = []
    reviews: list[ReviewItem] = []
    seen_observations: set[str] = set()

    for candidate in filtered:
        candidate.body = fetch_mail_body(mail_account, candidate.subject, candidate.sender)
        observation, review = build_observation(candidate)
        if review:
            reviews.append(review)
        if not observation:
            continue
        dedupe_key = f"{observation.observation_key}|{candidate.thread_id}|{candidate.received_at.strftime('%Y-%m-%d %H:%M')}"
        if dedupe_key in seen_observations:
            continue
        seen_observations.add(dedupe_key)
        observations.append(observation)

    observations.sort(key=lambda item: item.received_at)
    return observations, reviews


def load_state(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {
            "schemaVersion": 2,
            "list": DEFAULT_LIST,
            "account": DEFAULT_ACCOUNT_NAME,
            "source": "gmail_search_plus_mail_fallback",
            "processed": {},
            "review": [],
        }
    with open(path, "r", encoding="utf-8") as fh:
        data = json.load(fh)
    data.setdefault("processed", {})
    data.setdefault("review", [])
    data.setdefault("list", DEFAULT_LIST)
    data.setdefault("account", DEFAULT_ACCOUNT_NAME)
    return data


def derive_previous_company(entry: dict[str, Any]) -> str:
    if entry.get("company"):
        return entry["company"]
    title = entry.get("title", "")
    source = entry.get("source", {})
    return detect_company(title, source.get("sender", ""), "", entry.get("sourceFamily", "generic"))


def derive_previous_identity_key(entry: dict[str, Any]) -> str:
    if entry.get("identityKey"):
        return entry["identityKey"]
    return build_identity_key(
        derive_previous_company(entry),
        entry.get("eventType", "interview"),
        entry.get("role", ""),
        entry.get("sourceFamily") or detect_source_family(entry.get("source", {}).get("sender", ""), entry.get("title", ""), ""),
    )


def normalize_previous_state(raw_state: dict[str, Any]) -> dict[str, dict[str, Any]]:
    normalized: dict[str, dict[str, Any]] = {}
    for event_id, entry in raw_state.get("processed", {}).items():
        source = entry.get("source", {})
        reminder = entry.get("reminder", {})
        normalized_entry = {
            "eventId": entry.get("eventId", event_id),
            "status": entry.get("status", "active"),
            "identityKey": derive_previous_identity_key(entry),
            "sourceFamily": entry.get("sourceFamily")
            or detect_source_family(source.get("sender", ""), source.get("subject", ""), ""),
            "company": derive_previous_company(entry),
            "eventType": entry.get("eventType", "interview"),
            "role": entry.get("role", ""),
            "title": entry.get("title", ""),
            "note": entry.get("note", ""),
            "timing": entry.get("timing", {}),
            "links": entry.get("links", []),
            "mainReminder": entry.get(
                "mainReminder",
                {
                    "title": entry.get("title", ""),
                    "due": entry.get("timing", {}).get("deadline") or entry.get("timing", {}).get("start"),
                    "priority": "high",
                },
            ),
            "firstSeenAt": entry.get("firstSeenAt") or source.get("lastSeenAt"),
            "updatedAt": entry.get("updatedAt") or source.get("lastSeenAt"),
            "expiredAt": entry.get("expiredAt"),
            "cancelledAt": entry.get("cancelledAt"),
            "fingerprint": entry.get("fingerprint", ""),
            "reminder": reminder,
            "source": {
                "threadIds": source.get("threadIds", [event_id]),
                "subject": source.get("subject", entry.get("title", "")),
                "subjects": source.get("subjects", [source.get("subject", entry.get("title", ""))]),
                "sender": source.get("sender", ""),
                "lastSeenAt": source.get("lastSeenAt", entry.get("updatedAt", "")),
            },
        }
        if not normalized_entry["fingerprint"]:
            normalized_entry["fingerprint"] = stable_hash(
                {
                    "status": normalized_entry["status"],
                    "title": normalized_entry["title"],
                    "note": normalized_entry["note"],
                    "timing": normalized_entry["timing"],
                    "links": normalized_entry["links"],
                    "mainReminder": normalized_entry["mainReminder"],
                }
            )
        normalized[event_id] = normalized_entry
    return normalized


def entry_anchor(entry: dict[str, Any]) -> dt.datetime | None:
    return anchor_from_timing(entry.get("timing", {}))


def event_matches(candidate: EventObservation, entry: dict[str, Any]) -> int:
    if candidate.identity_key != entry.get("identityKey"):
        return -1

    score = 0
    candidate_threads = set(candidate.source_ids)
    previous_threads = set(entry.get("source", {}).get("threadIds", []))
    if candidate_threads & previous_threads:
        score += 120

    candidate_link = normalize_link(candidate.links[0]["url"]) if candidate.links else ""
    previous_links = entry.get("links", [])
    previous_link = normalize_link(previous_links[0]["url"]) if previous_links else ""
    if candidate_link and previous_link and candidate_link == previous_link:
        score += 70

    candidate_anchor = candidate.anchor_at()
    previous_anchor = entry_anchor(entry)
    if candidate_anchor and previous_anchor:
        delta_hours = abs((candidate_anchor - previous_anchor).total_seconds()) / 3600
        if delta_hours <= 48:
            score += 60
        elif delta_hours <= MATCH_WINDOW_DAYS * 24:
            score += 35
        elif candidate.lifecycle == "cancelled" and delta_hours <= 21 * 24:
            score += 20
        else:
            score -= 40
    elif candidate.lifecycle == "cancelled":
        score += 10

    previous_subject = normalize_subject_hint(entry.get("source", {}).get("subject", ""))
    candidate_subject = normalize_subject_hint(candidate.source_subjects[-1] if candidate.source_subjects else "")
    if previous_subject and candidate_subject and previous_subject == candidate_subject:
        score += 15

    if entry.get("status") in {"expired", "cancelled"}:
        score -= 20
    return score


def find_matching_event(candidate: EventObservation, events: dict[str, dict[str, Any]]) -> str | None:
    best_id = None
    best_score = -1
    threshold = 25 if candidate.lifecycle == "cancelled" else 40
    for event_id, entry in events.items():
        score = event_matches(candidate, entry)
        if score > best_score:
            best_score = score
            best_id = event_id
    return best_id if best_score >= threshold else None


def generate_event_id(candidate: EventObservation, existing_ids: set[str]) -> str:
    anchor = candidate.anchor_at()
    anchor_key = anchor.strftime("%Y%m%d%H%M") if anchor else candidate.received_at.strftime("%Y%m%d%H%M")
    base = {
        "identityKey": candidate.identity_key,
        "anchor": anchor_key,
        "subjectHint": normalize_subject_hint(candidate.source_subjects[-1] if candidate.source_subjects else candidate.title),
    }
    event_id = stable_hash(base)
    if event_id not in existing_ids:
        return event_id
    return stable_hash({**base, "threadId": candidate.source_ids[-1], "receivedAt": format_due(candidate.received_at)})


def build_source_payload(previous: dict[str, Any] | None, candidate: EventObservation) -> dict[str, Any]:
    previous_source = previous.get("source", {}) if previous else {}
    subjects = previous_source.get("subjects", [])
    thread_ids = previous_source.get("threadIds", [])
    return {
        "threadIds": merge_unique(thread_ids, candidate.source_ids),
        "subject": candidate.source_subjects[-1],
        "subjects": merge_unique(subjects, candidate.source_subjects),
        "sender": candidate.source_sender or previous_source.get("sender", ""),
        "lastSeenAt": candidate.received_at.strftime("%Y-%m-%d %H:%M"),
    }


def build_active_entry(event_id: str, candidate: EventObservation, previous: dict[str, Any] | None) -> dict[str, Any]:
    first_seen_at = previous.get("firstSeenAt") if previous else candidate.received_at.strftime("%Y-%m-%d %H:%M")
    entry = {
        "eventId": event_id,
        "status": "active",
        "identityKey": candidate.identity_key,
        "sourceFamily": candidate.source_family,
        "company": candidate.company,
        "eventType": candidate.event_type,
        "role": candidate.role,
        "title": candidate.title,
        "note": candidate.note,
        "timing": candidate.timing,
        "links": candidate.links,
        "mainReminder": {
            "title": candidate.title,
            "due": candidate.main_due,
            "priority": candidate.priority,
        },
        "firstSeenAt": first_seen_at,
        "updatedAt": candidate.received_at.strftime("%Y-%m-%d %H:%M"),
        "expiredAt": None,
        "cancelledAt": None,
        "reminder": dict(previous.get("reminder", {})) if previous else {},
        "source": build_source_payload(previous, candidate),
    }
    entry["fingerprint"] = stable_hash(
        {
            "status": entry["status"],
            "title": entry["title"],
            "note": entry["note"],
            "timing": entry["timing"],
            "links": entry["links"],
            "mainReminder": entry["mainReminder"],
        }
    )
    return entry


def build_cancelled_entry(
    event_id: str,
    candidate: EventObservation,
    previous: dict[str, Any],
    now: dt.datetime,
) -> dict[str, Any]:
    entry = dict(previous)
    entry["eventId"] = event_id
    entry["status"] = "cancelled"
    entry["cancelledAt"] = format_due(now)
    entry["updatedAt"] = candidate.received_at.strftime("%Y-%m-%d %H:%M")
    entry["source"] = build_source_payload(previous, candidate)
    note_lines = ["状态：已取消"]
    if previous.get("note"):
        note_lines.append(previous["note"])
    elif candidate.note:
        note_lines.append(candidate.note)
    entry["note"] = "\n".join(note_lines)
    entry["fingerprint"] = stable_hash(
        {
            "status": entry["status"],
            "title": entry.get("title", ""),
            "note": entry["note"],
            "timing": entry.get("timing", {}),
        }
    )
    return entry


def mark_entry_expired(entry: dict[str, Any], now: dt.datetime) -> dict[str, Any]:
    if entry.get("status") == "expired":
        return entry
    updated = dict(entry)
    updated["status"] = "expired"
    updated["expiredAt"] = format_due(now)
    updated["fingerprint"] = stable_hash(
        {
            "status": updated["status"],
            "title": updated.get("title", ""),
            "note": updated.get("note", ""),
            "timing": updated.get("timing", {}),
        }
    )
    return updated


def prune_closed_events(events: dict[str, dict[str, Any]], now: dt.datetime) -> int:
    to_delete: list[str] = []
    for event_id, entry in events.items():
        if entry.get("status") not in {"expired", "cancelled"}:
            continue
        closed_at = parse_optional_datetime(entry.get("expiredAt") or entry.get("cancelledAt"))
        if not closed_at:
            closed_at = parse_optional_datetime(entry.get("updatedAt"))
        if closed_at and closed_at + dt.timedelta(days=STATE_RETENTION_DAYS) < now:
            to_delete.append(event_id)
    for event_id in to_delete:
        del events[event_id]
    return len(to_delete)


def summarize_event_changes(
    previous: dict[str, dict[str, Any]],
    current: dict[str, dict[str, Any]],
) -> dict[str, list[str]]:
    changed = {
        "created": [],
        "updated": [],
        "expired": [],
        "cancelled": [],
    }
    for event_id, entry in current.items():
        prev = previous.get(event_id)
        if not prev:
            if entry.get("status") == "active":
                changed["created"].append(entry["title"])
            continue
        if prev.get("status") != entry.get("status"):
            if entry.get("status") == "expired":
                changed["expired"].append(entry["title"])
            elif entry.get("status") == "cancelled":
                changed["cancelled"].append(entry["title"])
            elif entry.get("status") == "active":
                changed["updated"].append(entry["title"])
        elif entry.get("status") == "active" and prev.get("fingerprint") != entry.get("fingerprint"):
            changed["updated"].append(entry["title"])
    return changed


def reconcile_events(
    previous_state: dict[str, Any],
    observations: list[EventObservation],
    reviews: list[ReviewItem],
    now: dt.datetime,
) -> tuple[dict[str, Any], dict[str, Any]]:
    previous_events = normalize_previous_state(previous_state)
    previous_review_keys = {
        f"{item.get('threadId', '')}|{item.get('reason', '')}"
        for item in previous_state.get("review", [])
    }
    current_events = {event_id: dict(entry) for event_id, entry in previous_events.items()}
    current_review_items = [item.to_dict() for item in reviews]
    new_review_items = [
        item
        for item in current_review_items
        if f"{item.get('threadId', '')}|{item.get('reason', '')}" not in previous_review_keys
    ]
    summary = {
        "created": 0,
        "updated": 0,
        "expired": 0,
        "cancelled": 0,
        "ignoredExpired": 0,
        "ignoredCancelled": 0,
        "review": len(new_review_items),
        "pruned": 0,
    }

    for observation in observations:
        match_id = find_matching_event(observation, current_events)
        if observation.lifecycle == "cancelled":
            if not match_id:
                summary["ignoredCancelled"] += 1
                continue
            current_events[match_id] = build_cancelled_entry(match_id, observation, current_events[match_id], now)
            continue

        if match_id:
            if is_timing_expired(observation.timing, now):
                current_events[match_id] = mark_entry_expired(current_events[match_id], now)
            else:
                current_events[match_id] = build_active_entry(match_id, observation, current_events[match_id])
            continue

        if is_timing_expired(observation.timing, now):
            summary["ignoredExpired"] += 1
            continue

        new_id = generate_event_id(observation, set(current_events))
        current_events[new_id] = build_active_entry(new_id, observation, None)

    for event_id, entry in list(current_events.items()):
        if entry.get("status") == "active" and is_timing_expired(entry.get("timing", {}), now):
            current_events[event_id] = mark_entry_expired(entry, now)

    summary["pruned"] = prune_closed_events(current_events, now)
    changed = summarize_event_changes(previous_events, current_events)
    summary["created"] = len(changed["created"])
    summary["updated"] = len(changed["updated"])
    summary["expired"] = len(changed["expired"])
    summary["cancelled"] = len(changed["cancelled"])

    ordered_items = sorted(
        current_events.items(),
        key=lambda item: (
            parse_optional_datetime(item[1].get("mainReminder", {}).get("due"))
            or entry_anchor(item[1])
            or parse_optional_datetime(item[1].get("updatedAt"))
            or now,
            PRIORITY_EVENT_TYPES.get(item[1].get("eventType", ""), 99),
            item[1].get("title", ""),
        ),
    )
    ordered_processed = {event_id: entry for event_id, entry in ordered_items}
    state = {
        "schemaVersion": 2,
        "list": previous_state.get("list", DEFAULT_LIST),
        "account": previous_state.get("account", DEFAULT_ACCOUNT_NAME),
        "followUpPolicy": "none",
        "source": "gmail_search_plus_mail_fallback",
        "scanPolicy": {
            "days": DEFAULT_DAYS,
            "maxResults": DEFAULT_MAX,
            "strategy": "overlap-safe incremental sync",
        },
        "notePolicy": {
            "keep": [
                "中文标题",
                "事件类型对应的真实时间信息",
                "唯一有效入口链接",
                "必要时的一句说明",
            ],
            "drop": [
                "投递成功回执",
                "Gmail ID",
                "发件人元数据",
                "长摘要",
                "与当前事件无关的说明",
            ],
        },
        "runtime": {
            "lastRunAt": format_due(now),
            "summary": summary,
            "changed": changed,
            "reviewNew": new_review_items,
        },
        "review": current_review_items,
        "processed": ordered_processed,
    }
    return state, summary


def parse_bridge_row(output: str) -> dict[str, str]:
    parts = output.strip().split("\t")
    return {
        "id": parts[0] if parts else "",
        "list": parts[1] if len(parts) > 1 else "",
        "title": parts[2] if len(parts) > 2 else "",
    }


def list_existing_reminders(list_name: str, account_name: str) -> list[dict[str, str]]:
    proc = run_bridge(["list", "--list", list_name, "--account", account_name])
    if proc.returncode != 0:
        raise RuntimeError(proc.stderr.strip() or proc.stdout.strip() or "list reminders failed")
    rows: list[dict[str, str]] = []
    for line in proc.stdout.splitlines():
        if not line.strip():
            continue
        parts = line.split("\t", 1)
        if len(parts) != 2:
            continue
        rows.append({"id": parts[0], "title": parts[1]})
    return rows


def create_reminder_for_entry(entry: dict[str, Any], list_name: str, account_name: str) -> str:
    main = entry.get("mainReminder", {})
    proc = run_bridge(
        [
            "add",
            "--title",
            main.get("title", ""),
            "--list",
            list_name,
            "--account",
            account_name,
            "--priority",
            main.get("priority", "none"),
            "--notes",
            entry.get("note", ""),
            *(["--due", main.get("due")] if main.get("due") else []),
        ]
    )
    if proc.returncode != 0:
        raise RuntimeError(proc.stderr.strip() or proc.stdout.strip() or "create reminder failed")
    return parse_bridge_row(proc.stdout.strip())["id"]


def update_reminder_for_entry(entry: dict[str, Any], reminder_id: str, list_name: str, account_name: str) -> str | None:
    main = entry.get("mainReminder", {})
    proc = run_bridge(
        [
            "update",
            "--id",
            reminder_id,
            "--title",
            main.get("title", ""),
            "--list",
            list_name,
            "--account",
            account_name,
            "--priority",
            main.get("priority", "none"),
            "--notes",
            entry.get("note", ""),
            *(["--due", main.get("due")] if main.get("due") else []),
        ]
    )
    if proc.returncode == 2:
        return None
    if proc.returncode != 0:
        raise RuntimeError(proc.stderr.strip() or proc.stdout.strip() or "update reminder failed")
    return parse_bridge_row(proc.stdout.strip())["id"]


def delete_reminder_by_id(reminder_id: str, list_name: str, account_name: str) -> bool:
    proc = run_bridge(["delete", "--id", reminder_id, "--list", list_name, "--account", account_name])
    if proc.returncode == 2:
        return False
    if proc.returncode != 0:
        raise RuntimeError(proc.stderr.strip() or proc.stdout.strip() or "delete reminder failed")
    return True


def sync_reminders(state: dict[str, Any], dry_run: bool = False) -> dict[str, int]:
    list_name = state.get("list", DEFAULT_LIST)
    account_name = state.get("account", DEFAULT_ACCOUNT_NAME)
    sync_stats = {
        "attached": 0,
        "created": 0,
        "updated": 0,
        "deleted": 0,
        "recreated": 0,
        "unchanged": 0,
    }

    existing_reminders = list_existing_reminders(list_name, account_name)
    available_by_title: dict[str, list[str]] = {}
    for item in existing_reminders:
        available_by_title.setdefault(item["title"], []).append(item["id"])

    for event_id, entry in state.get("processed", {}).items():
        reminder = dict(entry.get("reminder", {}))
        status = entry.get("status", "active")
        desired_fingerprint = entry.get("fingerprint", "")

        if status == "active":
            reminder_id = reminder.get("id", "")
            if not reminder_id:
                attached_ids = available_by_title.get(entry.get("title", ""), [])
                if attached_ids:
                    reminder_id = attached_ids.pop(0)
                    reminder = {"id": reminder_id}
                    sync_stats["attached"] += 1

            if dry_run:
                if not reminder_id:
                    sync_stats["created"] += 1
                elif reminder.get("lastSyncedFingerprint") != desired_fingerprint:
                    sync_stats["updated"] += 1
                else:
                    sync_stats["unchanged"] += 1
                continue

            if not reminder_id:
                reminder_id = create_reminder_for_entry(entry, list_name, account_name)
                sync_stats["created"] += 1
            elif reminder.get("lastSyncedFingerprint") != desired_fingerprint:
                updated_id = update_reminder_for_entry(entry, reminder_id, list_name, account_name)
                if updated_id is None:
                    reminder_id = create_reminder_for_entry(entry, list_name, account_name)
                    sync_stats["recreated"] += 1
                else:
                    reminder_id = updated_id
                    sync_stats["updated"] += 1
            else:
                sync_stats["unchanged"] += 1

            entry["reminder"] = {
                "id": reminder_id,
                "list": list_name,
                "account": account_name,
                "lastSyncedFingerprint": desired_fingerprint,
                "syncedAt": format_due(dt.datetime.now()),
            }
            continue

        reminder_id = reminder.get("id", "")
        if not reminder_id:
            continue
        if dry_run:
            sync_stats["deleted"] += 1
            continue
        deleted = delete_reminder_by_id(reminder_id, list_name, account_name)
        if deleted:
            sync_stats["deleted"] += 1
        entry["reminder"] = {
            "list": list_name,
            "account": account_name,
            "removedAt": format_due(dt.datetime.now()),
        }

    return sync_stats


def write_state(state: dict[str, Any], output: Path) -> None:
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(state, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def print_summary(state: dict[str, Any], sync_stats: dict[str, int] | None = None) -> None:
    runtime = state.get("runtime", {})
    changed = runtime.get("changed", {})
    payload = {
        "summary": runtime.get("summary", {}),
        "changed": changed,
        "sync": sync_stats or {},
        "review": state.get("review", []),
    }
    print(json.dumps(payload, ensure_ascii=False, indent=2))


def main() -> int:
    parser = argparse.ArgumentParser(description="Build recruiting reminder state from Gmail + Mail fallback")
    parser.add_argument("--account", default=DEFAULT_ACCOUNT, help="Gmail account for gog, e.g. your@gmail.com")
    parser.add_argument("--mail-account", default=DEFAULT_MAIL_ACCOUNT, help='Apple Mail account name, e.g. "谷歌"')
    parser.add_argument("--days", type=int, default=DEFAULT_DAYS)
    parser.add_argument("--max-results", type=int, default=DEFAULT_MAX)
    parser.add_argument("--output", default=str(STATE_PATH))
    parser.add_argument("--sync-reminders", action="store_true")
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    now = dt.datetime.now()
    output = Path(args.output).expanduser()
    previous_state = load_state(output)
    candidates = load_candidates(args.account, args.days, args.max_results)
    observations, reviews = load_observations(candidates, args.mail_account)
    state, _ = reconcile_events(previous_state, observations, reviews, now)
    state["scanPolicy"]["days"] = args.days
    state["scanPolicy"]["maxResults"] = args.max_results

    sync_stats: dict[str, int] | None = None
    if args.sync_reminders:
        sync_stats = sync_reminders(state, dry_run=args.dry_run)
        state.setdefault("runtime", {})["sync"] = sync_stats

    if not args.dry_run:
        write_state(state, output)
    print_summary(state, sync_stats)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

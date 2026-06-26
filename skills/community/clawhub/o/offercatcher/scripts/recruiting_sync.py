#!/usr/bin/env python3
"""
OfferCatcher - 招聘邮件提醒同步工具

两种模式：
1. --scan-only: 扫描邮件，返回原始 JSON，供 OpenClaw LLM 解析
2. --apply-events: 应用 LLM 解析结果，同步到 Apple Reminders
"""
import argparse
import datetime as dt
import hashlib
import json
import logging
import os
import re
import shlex
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any

# 日志配置
LOG_LEVEL = os.environ.get("OFFERCATCHER_LOG_LEVEL", "INFO").upper()
logger = logging.getLogger("offercatcher")
logger.setLevel(getattr(logging, LOG_LEVEL, logging.INFO))
handler = logging.StreamHandler(sys.stderr)
handler.setFormatter(logging.Formatter("%(asctime)s %(levelname)s %(message)s", "%H:%M:%S"))
logger.addHandler(handler)

# 路径配置 - 使用固定路径，不接受环境变量覆盖（防止注入）
REPO_ROOT = Path(__file__).resolve().parents[1]
CONFIG_PATH = Path.home() / ".openclaw" / "offercatcher.yaml"
STATE_PATH = Path.home() / ".openclaw" / "workspace" / "memory" / "offercatcher-state.json"
REMINDERS_SCRIPT = REPO_ROOT / "scripts" / "apple_reminders_bridge.py"

# 默认值
DEFAULT_MAILBOX = os.environ.get("OFFERCATCHER_MAILBOX", "INBOX")
DEFAULT_LIST = "OfferCatcher"
DEFAULT_ACCOUNT_NAME = "iCloud"
MAIL_TIMEOUT_SECONDS = 20
MAIL_BODY_LIMIT = 2000  # 扫描模式下的正文截断长度
BODY_RECORD_SEP = "\x00"


def load_config() -> dict[str, Any]:
    """加载 YAML 配置文件，验证配置结构。"""
    if not CONFIG_PATH.exists():
        return {}

    # 检查 yaml 模块是否可用
    try:
        import yaml
    except ImportError:
        logger.warning("yaml 模块未安装，无法加载配置文件")
        return {}

    try:
        with open(CONFIG_PATH, "r", encoding="utf-8") as f:
            data = yaml.safe_load(f)

        # 验证返回值类型
        if data is None:
            return {}
        if not isinstance(data, dict):
            logger.warning("配置文件格式错误：必须是 YAML 字典结构，实际为 %s", type(data).__name__)
            return {}

        # 验证配置字段类型
        validated: dict[str, Any] = {}
        if "mail_account" in data:
            if isinstance(data["mail_account"], str):
                validated["mail_account"] = data["mail_account"]
            else:
                logger.warning("mail_account 配置类型错误，应为字符串")
        if "mailbox" in data:
            if isinstance(data["mailbox"], str):
                validated["mailbox"] = data["mailbox"]
            else:
                logger.warning("mailbox 配置类型错误，应为字符串")
        if "days" in data:
            if isinstance(data["days"], int) and data["days"] > 0:
                validated["days"] = data["days"]
            else:
                logger.warning("days 配置类型错误，应为正整数")
        if "max_results" in data:
            if isinstance(data["max_results"], int) and data["max_results"] > 0:
                validated["max_results"] = data["max_results"]
            else:
                logger.warning("max_results 配置类型错误，应为正整数")

        return validated

    except yaml.YAMLError as e:
        logger.warning("YAML 解析错误：%s", e)
        return {}
    except Exception as e:
        logger.warning("配置文件加载失败：%s", e)
        return {}


_config = load_config()
DEFAULT_MAIL_ACCOUNT = os.environ.get("OFFERCATCHER_MAIL_ACCOUNT") or _config.get("mail_account", "")
DEFAULT_DAYS = int(os.environ.get("OFFERCATCHER_DAYS") or _config.get("days", 2))
DEFAULT_MAX = int(os.environ.get("OFFERCATCHER_MAX_RESULTS") or _config.get("max_results", 60))

# 安全限制
MAX_EVENT_TITLE_LENGTH = 200
MAX_EVENT_NOTE_LENGTH = 2000
MAX_EVENTS_PER_REQUEST = 100
VALID_EVENT_TYPES = ("interview", "ai_interview", "written_exam", "assessment", "authorization", "deadline")


def validate_event(evt: dict[str, Any], index: int) -> list[str]:
    """
    验证单个事件数据的有效性。

    返回错误列表，空列表表示验证通过。
    """
    errors: list[str] = []

    # 验证 event_type
    event_type = evt.get("event_type", "interview")
    if event_type not in VALID_EVENT_TYPES:
        errors.append(f"事件 {index}: 无效的 event_type '{event_type}'")

    # 验证 title 长度
    title = evt.get("title", "")
    if len(title) > MAX_EVENT_TITLE_LENGTH:
        errors.append(f"事件 {index}: title 超过最大长度 {MAX_EVENT_TITLE_LENGTH}")

    # 验证 timing 结构
    timing = evt.get("timing", {})
    if not isinstance(timing, dict):
        errors.append(f"事件 {index}: timing 必须是字典")
    elif timing:
        # 检查时间格式
        for key in ("start", "end", "deadline"):
            if key in timing:
                value = timing[key]
                if not isinstance(value, str):
                    errors.append(f"事件 {index}: timing.{key} 必须是字符串")
                elif value:
                    # 验证时间格式
                    try:
                        dt.datetime.strptime(value[:16], "%Y-%m-%d %H:%M")
                    except ValueError:
                        errors.append(f"事件 {index}: timing.{key} 格式无效 '{value}'")

    # 验证 link 是有效 URL（简单检查）
    link = evt.get("link", "")
    if link and not isinstance(link, str):
        errors.append(f"事件 {index}: link 必须是字符串")

    return errors


# ============== 数据结构 ==============

@dataclass
class MailMessage:
    """Apple Mail 邮件抽象。"""
    message_id: str
    subject: str
    sender: str
    received_at: dt.datetime
    account: str
    mailbox: str
    body: str = ""


@dataclass
class EventInput:
    """LLM 解析后的事件输入。"""
    id: str
    company: str
    event_type: str
    title: str
    timing: dict[str, str]
    role: str
    link: str
    note: str
    message_id: str
    subject: str
    sender: str


def normalize_event_text(text: str) -> str:
    """规范化事件文本，清理转义换行和多余空白。"""
    if not text:
        return ""
    text = text.replace("\\r\\n", "\n").replace("\\n", "\n").replace("\\t", " ")
    text = text.replace("\r\n", "\n").replace("\r", "\n")
    text = text.replace("：", ":")
    lines = [line.strip(" \t-") for line in text.split("\n")]
    lines = [line for line in lines if line]
    return "\n".join(lines)


def sanitize_title(title: str, company: str, event_type: str) -> str:
    """清洗标题，避免噪声符号和不自然空格。"""
    cleaned = normalize_event_text(title or f"{company}{event_type}").replace("\n", " ")
    cleaned = re.sub(r"^[!！·•\s]+", "", cleaned)
    cleaned = cleaned.replace("(", "（").replace(")", "）")
    cleaned = re.sub(r"\s+", " ", cleaned).strip()
    cleaned = re.sub(r"([\u4e00-\u9fff])\s+([\u4e00-\u9fff])", r"\1\2", cleaned)
    cleaned = re.sub(r"([\u4e00-\u9fff])\s+([A-Za-z0-9])", r"\1\2", cleaned)
    cleaned = re.sub(r"([A-Za-z0-9])\s+([\u4e00-\u9fff])", r"\1\2", cleaned)
    return cleaned


def sanitize_note_lines(lines: list[str]) -> str:
    """清洗备注行，统一字段格式。"""
    normalized: list[str] = []
    for raw_line in lines:
        line = normalize_event_text(raw_line)
        if not line:
            continue
        line = re.sub(r"^链接\s*:\s*", "入口：", line)
        line = re.sub(r"^链接：\s*", "入口：", line)
        line = re.sub(r"^入口\s*:\s*", "入口：", line)
        line = re.sub(r"^联系人\s*:\s*", "联系人：", line)
        line = re.sub(r"^会议ID\s*:\s*", "会议ID：", line)
        line = re.sub(r"^会议号\s*:\s*", "会议号：", line)
        line = re.sub(r"^时间\s*:\s*", "时间：", line)
        line = re.sub(r"^截止\s*:\s*", "截止：", line)
        line = re.sub(r"^岗位\s*:\s*", "岗位：", line)
        normalized.extend(part for part in line.split("\n") if part)

    deduped: list[str] = []
    seen: set[str] = set()
    for line in normalized:
        if line not in seen:
            deduped.append(line)
            seen.add(line)
    return "\n".join(deduped)


# ============== Apple Mail 操作 ==============

def run_text(cmd: list[str], timeout: int | None = None) -> str:
    """执行命令并返回输出。"""
    try:
        proc = subprocess.run(
            cmd, capture_output=True, text=True, encoding="utf-8", errors="replace", timeout=timeout
        )
        if proc.returncode != 0:
            raise RuntimeError(proc.stderr.strip() or proc.stdout.strip() or "command failed")
        return proc.stdout
    except subprocess.TimeoutExpired as exc:
        raise RuntimeError(f"命令超时 ({timeout}s)") from exc


def run_osascript(lines: list[str], timeout: int | None = None) -> str:
    """通过 osascript -e 执行 AppleScript，显式 shell 引号避免编码异常。"""
    command = "osascript " + " ".join(f"-e {shlex.quote(line)}" for line in lines)
    return run_text(["/bin/zsh", "-lc", command], timeout=timeout)


def applescript_escape(text: str) -> str:
    """转义 AppleScript 字符串中的特殊字符。"""
    return text.replace("\\", "\\\\").replace('"', '\\"')


def parse_apple_mail_datetime(value: str) -> dt.datetime | None:
    """解析 Apple Mail 返回的中文日期字符串。"""
    text = value.strip()
    match = re.search(
        r"(?P<year>\d{4})年(?P<month>\d{1,2})月(?P<day>\d{1,2})日.*?(?P<hour>\d{1,2}):(?P<minute>\d{2})(?::(?P<second>\d{2}))?",
        text,
    )
    if not match:
        return None

    parts = {key: int(number) for key, number in match.groupdict(default="0").items()}
    try:
        return dt.datetime(
            parts["year"], parts["month"], parts["day"], parts["hour"], parts["minute"], parts["second"]
        )
    except ValueError:
        return None


def list_mail_account_names() -> list[str]:
    """列出 Apple Mail 中可用的账号名。"""
    raw = run_osascript([
        'tell application "Mail"',
        'set accountNames to {}',
        'repeat with acc in (every account)',
        'set end of accountNames to (name of acc as string)',
        'end repeat',
        'return accountNames as string',
        'end tell',
    ], timeout=MAIL_TIMEOUT_SECONDS)
    return [item.strip() for item in raw.split(",") if item.strip()]


def list_recent_mail_messages(days: int, max_results: int, mail_account: str, mailbox: str) -> list[MailMessage]:
    """从 Apple Mail 获取最近 N 天的邮件列表。

    优化：在 AppleScript 层面进行日期筛选，避免遍历全部邮件导致超时。
    """
    mailbox_candidates = [mailbox]
    for candidate in ("Inbox", "收件箱"):
        if candidate not in mailbox_candidates:
            mailbox_candidates.append(candidate)
    target_accounts = [mail_account] if mail_account else list_mail_account_names()
    raw_chunks: list[str] = []

    for account_name in target_accounts:
        escaped_account = applescript_escape(account_name)
        for mailbox_name in mailbox_candidates:
            escaped_mailbox = applescript_escape(mailbox_name)
            # 在 AppleScript 中进行日期筛选，大幅减少遍历量
            script_lines = [
                'tell application "Mail"',
                f'set acc to account "{escaped_account}"',
                f'set mbx to mailbox "{escaped_mailbox}" of acc',
                'set output to ""',
                'set cutoff to (current date) - (' + str(days) + ' * days)',
                'set matchCount to 0',
                'repeat with m in messages of mbx',
                f'if matchCount is greater than or equal to {max_results * 3} then exit repeat',
                'set msgDate to date received of m',
                'if msgDate > cutoff then',
                'set msgId to (id of m) as string',
                'set subj to subject of m as string',
                'set sndr to sender of m as string',
                'set ts to (date received of m) as string',
                f'set lineText to "{escaped_account}" & tab & "{escaped_mailbox}" & tab & msgId & tab & subj & tab & sndr & tab & ts',
                'set output to output & lineText & linefeed',
                'set matchCount to matchCount + 1',
                'end if',
                'end repeat',
                'return output',
                'end tell',
            ]
            try:
                # 增加 timeout 到 60s，防止慢速邮箱超时
                raw_chunks.append(run_osascript(script_lines, timeout=60))
                break
            except RuntimeError as exc:
                logger.debug("读取邮箱失败 account=%s mailbox=%s err=%s", account_name, mailbox_name, exc)
                continue

    raw = "\n".join(chunk for chunk in raw_chunks if chunk.strip())

    messages: list[MailMessage] = []
    for line in raw.splitlines():
        if not line.strip():
            continue
        parts = line.split("\t")
        if len(parts) != 6:
            continue
        account_name, mailbox_name, message_id, subject, sender, received_at = parts
        parsed = parse_apple_mail_datetime(received_at)
        if not parsed:
            continue
        messages.append(MailMessage(
            message_id=message_id.strip(), subject=subject.strip(), sender=sender.strip(),
            received_at=parsed, account=account_name.strip(), mailbox=mailbox_name.strip(),
        ))

    messages.sort(key=lambda item: item.received_at, reverse=True)
    return messages[:max_results]


def fetch_mail_bodies_batch(items: list[tuple[str, str, str]]) -> dict[str, str]:
    """批量获取邮件正文，返回 "account|mailbox|id" → body 映射。"""
    if not items:
        return {}

    by_account_mailbox: dict[str, list[str]] = {}
    for msg_id, account, mailbox in items:
        key = f"{account}|{mailbox}"
        if key not in by_account_mailbox:
            by_account_mailbox[key] = []
        by_account_mailbox[key].append(msg_id)

    result: dict[str, str] = {}
    for key, msg_ids in by_account_mailbox.items():
        account, mailbox = key.split("|", 1)
        escaped_account = applescript_escape(account)
        escaped_mailbox = applescript_escape(mailbox)
        ids_list = ", ".join(f'"{applescript_escape(mid)}"' for mid in msg_ids)

        script = [
            f"with timeout of {MAIL_TIMEOUT_SECONDS * 2} seconds", 'tell application "Mail"',
            f'set targetIds to {{{ids_list}}}', f'set acc to account "{escaped_account}"',
            f'set mbx to mailbox "{escaped_mailbox}" of acc', 'set results to ""',
            'repeat with m in messages of mbx', 'set msgId to id of m as string',
            'if targetIds contains msgId then', 'set c to content of m',
            f'if (length of c) > {MAIL_BODY_LIMIT} then set c to text 1 thru {MAIL_BODY_LIMIT} of c',
            'set results to results & msgId & tab & c & character id 0', 'end if', 'end repeat',
            'return results', 'end tell', 'end timeout',
        ]
        try:
            raw = run_osascript(script, timeout=MAIL_TIMEOUT_SECONDS * 2 + 5)
        except RuntimeError:
            continue

        for record in raw.split(BODY_RECORD_SEP):
            if not record.strip():
                continue
            parts = record.split("\t", 1)
            if len(parts) == 2:
                result[f"{key}|{parts[0]}"] = parts[1]

    return result


# ============== 状态管理 ==============

def validate_path_in_home(path: Path) -> Path:
    """
    验证路径是否安全，防止路径遍历攻击。

    允许的路径：
    - 用户主目录及其子目录
    - 系统临时目录（用于测试）
    - /tmp 目录

    返回规范化后的绝对路径。
    """
    resolved = path.expanduser().resolve()
    home = Path.home().resolve()

    # 允许的主目录
    allowed_roots = [
        home,
        Path("/tmp").resolve(),
        Path(os.environ.get("TMPDIR", "/tmp")).resolve(),
    ]

    for root in allowed_roots:
        try:
            resolved.relative_to(root)
            return resolved  # 路径在允许范围内
        except ValueError:
            continue

    # 如果都不在允许范围内，检查是否有路径遍历尝试
    original_str = str(path)
    if ".." in original_str or original_str.startswith("/etc") or original_str.startswith("/var"):
        raise SystemExit(f"路径 {path} 可能存在安全风险，拒绝访问")

    return resolved


def load_state(path: Path) -> dict[str, Any]:
    """加载状态文件。"""
    validated_path = validate_path_in_home(path)
    if not validated_path.exists():
        return {"schemaVersion": 2, "list": DEFAULT_LIST, "account": DEFAULT_ACCOUNT_NAME, "processed": {}, "review": []}
    with open(validated_path, "r", encoding="utf-8") as f:
        return json.load(f)


def write_state(state: dict[str, Any], path: Path) -> None:
    """写入状态文件。"""
    validated_path = validate_path_in_home(path)
    validated_path.parent.mkdir(parents=True, exist_ok=True)
    validated_path.write_text(json.dumps(state, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


# ============== Apple Reminders 同步 ==============

def run_bridge(cmd: list[str]) -> subprocess.CompletedProcess[str]:
    """调用 Reminders 桥接脚本，使用受限的环境变量。"""
    # 构建最小化的环境变量，只保留必要项
    env = {
        "PATH": os.environ.get("PATH", "/usr/bin:/bin"),
        "HOME": os.environ.get("HOME", ""),
        "USER": os.environ.get("USER", ""),
        "TMPDIR": os.environ.get("TMPDIR", "/tmp"),
    }
    # 添加 Python 相关变量（确保脚本能运行）
    if "PYTHONPATH" in os.environ:
        env["PYTHONPATH"] = os.environ["PYTHONPATH"]
    if "__PYVENV_LAUNCHER__" in os.environ:
        env["__PYVENV_LAUNCHER__"] = os.environ["__PYVENV_LAUNCHER__"]

    return subprocess.run(
        [sys.executable, str(REMINDERS_SCRIPT), *cmd],
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
        shell=False,  # 显式禁止 shell 执行
        env=env,
    )


def parse_bridge_row(output: str) -> dict[str, str]:
    """解析桥接脚本返回的行。"""
    parts = output.strip().split("\t")
    return {"id": parts[0] if parts else "", "list": parts[1] if len(parts) > 1 else "", "title": parts[2] if len(parts) > 2 else ""}


def format_due(value: str) -> str:
    """格式化时间。"""
    for fmt in ("%Y-%m-%d %H:%M:%S", "%Y-%m-%d %H:%M"):
        try:
            return dt.datetime.strptime(value, fmt).strftime("%Y-%m-%d %H:%M:%S")
        except ValueError:
            continue
    return value


def sync_to_reminders(events: list[EventInput], state: dict[str, Any], dry_run: bool) -> dict[str, int]:
    """同步事件到 Apple Reminders。"""
    list_name = state.get("list", DEFAULT_LIST)
    account_name = state.get("account", DEFAULT_ACCOUNT_NAME)

    stats = {"created": 0, "updated": 0, "deleted": 0}

    for evt in events:
        due = evt.timing.get("start") or evt.timing.get("deadline", "")
        if due:
            due = format_due(due)

        priority = "high" if evt.event_type in ("interview", "ai_interview", "written_exam") else "medium"

        if dry_run:
            stats["created"] += 1
            logger.info("[DRY-RUN] 创建: %s", evt.title)
            continue

        proc = run_bridge([
            "add", "--title", evt.title, "--list", list_name, "--account", account_name,
            "--priority", priority, "--notes", evt.note,
        ] + (["--due", due] if due else []))

        if proc.returncode != 0:
            logger.warning("创建提醒失败: %s", proc.stderr.strip())
            continue

        stats["created"] += 1
        logger.debug("创建提醒: %s", evt.title)

    return stats


# ============== 主逻辑 ==============

def scan_emails(args: argparse.Namespace) -> int:
    """扫描邮件，返回原始 JSON。"""
    logger.info("扫描邮件 days=%d max=%d", args.days, args.max_results)

    messages = list_recent_mail_messages(args.days, args.max_results, args.mail_account, args.mailbox)
    logger.info("获取到 %d 封邮件", len(messages))

    # 批量获取正文
    mail_items = [(m.message_id, m.account, m.mailbox) for m in messages if m.account]
    body_cache = fetch_mail_bodies_batch(mail_items) if mail_items else {}

    emails = []
    for m in messages:
        cache_key = f"{m.account}|{m.mailbox}|{m.message_id}"
        body = body_cache.get(cache_key, "")
        emails.append({
            "message_id": m.message_id, "subject": m.subject, "sender": m.sender,
            "received_at": m.received_at.strftime("%Y-%m-%d %H:%M"),
            "account": m.account, "mailbox": m.mailbox, "body": body,
        })

    print(json.dumps({"emails": emails}, ensure_ascii=False, indent=2))
    return 0


def apply_events(args: argparse.Namespace) -> int:
    """应用 LLM 解析后的事件。"""
    events_path = Path(args.apply_events)
    if not events_path.exists():
        print(json.dumps({"error": f"文件不存在: {events_path}"}, ensure_ascii=False))
        return 1

    with open(events_path, "r", encoding="utf-8") as f:
        llm_output = json.load(f)

    # 验证顶层结构
    if not isinstance(llm_output, dict):
        print(json.dumps({"error": "JSON 必须是字典结构"}, ensure_ascii=False))
        return 1

    raw_events = llm_output.get("events", [])
    if not isinstance(raw_events, list):
        print(json.dumps({"error": "events 必须是数组"}, ensure_ascii=False))
        return 1

    # 数量限制
    if len(raw_events) > MAX_EVENTS_PER_REQUEST:
        logger.warning("事件数量 %d 超过限制 %d，只处理前 %d 个", len(raw_events), MAX_EVENTS_PER_REQUEST, MAX_EVENTS_PER_REQUEST)
        raw_events = raw_events[:MAX_EVENTS_PER_REQUEST]

    # 验证每个事件
    validation_errors: list[str] = []
    for idx, evt in enumerate(raw_events):
        if not isinstance(evt, dict):
            validation_errors.append(f"事件 {idx}: 必须是字典")
            continue
        errors = validate_event(evt, idx)
        validation_errors.extend(errors)

    if validation_errors:
        for err in validation_errors:
            logger.warning("验证错误: %s", err)
        print(json.dumps({"error": "事件验证失败", "details": validation_errors[:10]}, ensure_ascii=False))
        return 1

    events = []
    for evt in raw_events:
        timing = evt.get("timing", {})
        note_parts = []
        if timing.get("start"):
            note_parts.append(f"时间：{timing['start']}" + (f" - {timing['end'][-5:]}" if timing.get("end") else ""))
        elif timing.get("deadline"):
            note_parts.append(f"截止：{timing['deadline']}")
        if evt.get("role"):
            note_parts.append(f"岗位：{evt['role']}")
        if evt.get("link"):
            note_parts.append(f"入口：{evt['link']}")
        if evt.get("note"):
            note_parts.append(evt["note"])

        # 截断过长的字段
        title = sanitize_title(evt.get("title", ""), evt.get("company", ""), evt.get("event_type", ""))
        if len(title) > MAX_EVENT_TITLE_LENGTH:
            title = title[:MAX_EVENT_TITLE_LENGTH]
        note = sanitize_note_lines(note_parts)
        if len(note) > MAX_EVENT_NOTE_LENGTH:
            note = note[:MAX_EVENT_NOTE_LENGTH]

        events.append(EventInput(
            id=evt.get("id", hashlib.sha1(json.dumps(evt, sort_keys=True).encode()).hexdigest()[:16]),
            company=evt.get("company", "未知公司"),
            event_type=evt.get("event_type", "interview"),
            title=title,
            timing=timing,
            role=evt.get("role", ""),
            link=evt.get("link", ""),
            note=note,
            message_id=evt.get("message_id", ""),
            subject=evt.get("subject", ""),
            sender=evt.get("sender", ""),
        ))

    logger.info("应用 %d 个事件", len(events))

    output = Path(args.output).expanduser()
    state = load_state(output)

    sync_stats = sync_to_reminders(events, state, args.dry_run)

    # 更新状态
    now = dt.datetime.now().strftime("%Y-%m-%d %H:%M")
    for evt in events:
        event_id = evt.id
        state["processed"][event_id] = {
            "eventId": event_id, "status": "active", "company": evt.company,
            "eventType": evt.event_type, "title": evt.title, "timing": evt.timing,
            "note": evt.note, "updatedAt": now,
            "reminder": {"list": state.get("list", DEFAULT_LIST), "account": state.get("account", DEFAULT_ACCOUNT_NAME)},
            "source": {"messageId": evt.message_id, "subject": evt.subject, "sender": evt.sender},
        }

    if not args.dry_run:
        write_state(state, output)

    print(json.dumps({
        "summary": {"created": sync_stats["created"], "updated": 0, "expired": 0, "cancelled": 0},
        "sync": sync_stats,
    }, ensure_ascii=False, indent=2))

    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description="OfferCatcher - 招聘邮件提醒同步")
    parser.add_argument("--mail-account", default=DEFAULT_MAIL_ACCOUNT, help='Apple Mail 账号名')
    parser.add_argument("--mailbox", default=DEFAULT_MAILBOX, help='邮箱目录')
    parser.add_argument("--days", type=int, default=DEFAULT_DAYS, help='扫描天数')
    parser.add_argument("--max-results", type=int, default=DEFAULT_MAX, help='最大邮件数')
    parser.add_argument("--output", default=str(STATE_PATH), help='状态文件路径')
    parser.add_argument("--dry-run", action="store_true", help='试运行，不实际写入')
    parser.add_argument("--verbose", "-v", action="store_true", help='详细日志')
    parser.add_argument("--scan-only", action="store_true", help='仅扫描返回原始邮件')
    parser.add_argument("--apply-events", type=str, help='应用 LLM 解析后的事件 JSON 文件')
    args = parser.parse_args()

    if args.verbose:
        logger.setLevel(logging.DEBUG)

    if args.scan_only:
        return scan_emails(args)

    if args.apply_events:
        return apply_events(args)

    parser.error("请指定 --scan-only 或 --apply-events")


if __name__ == "__main__":
    raise SystemExit(main())

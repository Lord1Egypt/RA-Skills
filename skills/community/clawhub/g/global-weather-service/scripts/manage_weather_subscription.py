from __future__ import annotations

import argparse
import json
import subprocess
import sys
import time
from datetime import datetime, timedelta
from pathlib import Path
from zoneinfo import ZoneInfo, ZoneInfoNotFoundError

ROOT = Path(__file__).resolve().parent.parent
STATE_PATH = ROOT / "data" / "subscriptions.json"
TIMEZONE_STATE_PATH = ROOT / "data" / "user_timezones.json"
STATE_SYNC_RETRIES = 5
STATE_SYNC_DELAY_SECONDS = 0.2

DAY_MODE_MAP = {
    "today": 1,
    "tomorrow": 2,
    "7day": 7,
}
DAY_MODE_LABEL = {
    "today": "今天天气",
    "tomorrow": "明天天气",
    "7day": "近七日天气",
}


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser()
    p.add_argument("action", choices=["add", "list", "remove", "update", "set-timezone", "get-timezone"])
    p.add_argument("--to")
    p.add_argument("--city")
    p.add_argument("--time")
    p.add_argument("--id")
    p.add_argument("--name")
    p.add_argument("--timezone")
    p.add_argument("--days", type=int)
    p.add_argument("--mode", choices=["today", "tomorrow", "7day"])
    return p.parse_args()


def load_json(path: Path, default):
    if not path.exists():
        return default
    return json.loads(path.read_text(encoding="utf-8"))


def save_json(path: Path, data) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")


def print_json(data) -> None:
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass
    print(json.dumps(data, ensure_ascii=False, indent=2))


def run_cmd(cmd: list[str]) -> subprocess.CompletedProcess[str]:
    return subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8", errors="replace")


def find_openclaw_cmd() -> str:
    candidates = [
        "openclaw.cmd",
        str(Path.home() / "AppData" / "Roaming" / "npm" / "openclaw.cmd"),
    ]
    for candidate in candidates:
        try:
            result = subprocess.run([candidate, "--version"], capture_output=True, text=True, encoding="utf-8", errors="replace")
            if result.returncode == 0 or result.stdout or result.stderr:
                return candidate
        except FileNotFoundError:
            continue
    raise SystemExit("openclaw.cmd not found in PATH.")


def load_state() -> list[dict]:
    return load_json(STATE_PATH, [])


def save_state(items: list[dict]) -> None:
    save_json(STATE_PATH, items)


def load_timezones() -> dict:
    return load_json(TIMEZONE_STATE_PATH, {})


def save_timezones(state: dict) -> None:
    save_json(TIMEZONE_STATE_PATH, state)


def get_timezone_for_target(target: str) -> str | None:
    return load_timezones().get(target)


def set_timezone_for_target(target: str, timezone: str) -> None:
    ZoneInfo(timezone)
    state = load_timezones()
    state[target] = timezone
    save_timezones(state)


def get_timezone(to: str) -> dict:
    return {"to": to, "timezone": get_timezone_for_target(to)}


def set_timezone(to: str, timezone: str) -> dict:
    try:
        ZoneInfo(timezone)
    except ZoneInfoNotFoundError:
        raise SystemExit("无效时区，请使用 IANA 时区名，例如 Asia/Shanghai")
    set_timezone_for_target(to, timezone)
    return {"ok": True, "to": to, "timezone": timezone}


def ensure_timezone(to: str) -> str:
    timezone = get_timezone_for_target(to)
    if not timezone:
        raise SystemExit("missing timezone for target, set timezone first")
    return timezone


def parse_relative_time(text: str, tz_name: str) -> str | None:
    tz = ZoneInfo(tz_name)
    now = datetime.now(tz)
    raw = text.strip().replace("个", "")
    chinese_digits = {"一": 1, "二": 2, "两": 2, "三": 3, "四": 4, "五": 5, "六": 6, "七": 7, "八": 8, "九": 9, "十": 10}

    def parse_num(s: str) -> int | None:
        s = s.strip()
        if not s:
            return None
        if s.isdigit():
            return int(s)
        if s == "十":
            return 10
        if s.startswith("十") and len(s) == 2 and s[1] in chinese_digits:
            return 10 + chinese_digits[s[1]]
        if s.endswith("十") and len(s) == 2 and s[0] in chinese_digits:
            return chinese_digits[s[0]] * 10
        if len(s) == 1 and s in chinese_digits:
            return chinese_digits[s]
        return None

    for suffixes, unit in [(("分钟后", "分后", "分钟", "分"), "minutes"), (("小时后", "钟头后", "小时", "钟头"), "hours")]:
        for suffix in suffixes:
            if raw.endswith(suffix):
                value = parse_num(raw[:-len(suffix)])
                if value is None:
                    return None
                delta = timedelta(minutes=value) if unit == "minutes" else timedelta(hours=value)
                return (now + delta).isoformat(timespec="minutes")
    return None


def parse_time_text(text: str, tz_name: str) -> tuple[str | None, str | None]:
    tz = ZoneInfo(tz_name)
    now = datetime.now(tz)
    raw = text.strip().replace("：", ":").replace(".", ":")

    relative_dt = parse_relative_time(raw, tz_name)
    if relative_dt:
        return relative_dt, None

    recurring_prefix = {
        "每天": "*",
        "每日": "*",
        "工作日": "1-5",
        "周一": "1",
        "周二": "2",
        "周三": "3",
        "周四": "4",
        "周五": "5",
        "周六": "6",
        "周日": "0",
        "周天": "0",
        "星期一": "1",
        "星期二": "2",
        "星期三": "3",
        "星期四": "4",
        "星期五": "5",
        "星期六": "6",
        "星期日": "0",
        "星期天": "0",
    }
    period_map = {"凌晨": 0, "早上": 8, "上午": 9, "中午": 12, "下午": 15, "晚上": 20, "今晚": 20}

    prefix = None
    for key in sorted(recurring_prefix.keys(), key=len, reverse=True):
        if raw.startswith(key):
            prefix = key
            raw = raw[len(key):].strip()
            break

    tomorrow = False
    if raw.startswith("明天"):
        tomorrow = True
        raw = raw[2:].strip()
    elif raw.startswith("今天"):
        raw = raw[2:].strip()

    period = None
    for key in period_map:
        if raw.startswith(key):
            period = key
            raw = raw[len(key):].strip()
            break

    normalized = raw.replace("点半", ":30").replace("点", ":").replace("分", "")
    if normalized.endswith(":"):
        normalized += "00"
    if ":" not in normalized and normalized.isdigit():
        normalized = f"{normalized}:00"

    try:
        hour_str, minute_str = normalized.split(":", 1)
        hour = int(hour_str)
        minute = int(minute_str or "0")
    except ValueError:
        raise SystemExit("无法解析时间，请改用更明确的格式。")

    if period in {"下午", "晚上", "今晚"} and 1 <= hour <= 11:
        hour += 12
    if period == "中午" and hour < 11:
        hour += 12
    if period == "凌晨" and hour == 12:
        hour = 0

    if prefix:
        return None, f"{minute} {hour} * * {recurring_prefix[prefix]}"

    for fmt in ("%Y-%m-%d %H:%M", "%Y/%m/%d %H:%M", "%H:%M"):
        try:
            parsed = datetime.strptime(text.strip().replace(".", ":"), fmt)
            if fmt == "%H:%M":
                dt = now.replace(hour=parsed.hour, minute=parsed.minute, second=0, microsecond=0)
                if dt <= now:
                    dt += timedelta(days=1)
                return dt.isoformat(timespec="minutes"), None
            dt = parsed.replace(tzinfo=tz)
            return dt.isoformat(timespec="minutes"), None
        except ValueError:
            continue

    dt = now.replace(hour=hour, minute=minute, second=0, microsecond=0)
    if tomorrow:
        dt += timedelta(days=1)
    elif dt <= now:
        dt += timedelta(days=1)
    return dt.isoformat(timespec="minutes"), None


def resolve_schedule(time_text: str, timezone: str) -> tuple[str | None, str | None]:
    return parse_time_text(time_text, timezone)


def normalize_mode(mode: str | None, days: int | None) -> tuple[str, int]:
    if mode:
        return mode, DAY_MODE_MAP[mode]
    if days == 2:
        return "tomorrow", 2
    if days == 7:
        return "7day", 7
    return "today", 1 if days is None else days


def build_subscription_name(city: str, mode: str) -> str:
    return f"天气订阅: {city} {DAY_MODE_LABEL.get(mode, f'{mode}天气')}"


def normalize_target(to: str) -> str:
    if to.startswith("qqbot:"):
        return to
    return f"qqbot:c2c:{to}"


def build_agent_message(to: str, city: str, mode: str, days: int) -> str:
    day_phrase = DAY_MODE_LABEL.get(mode, "天气")
    if mode == "tomorrow":
        fetch_hint = "查询明天的天气"
        report_days = 1
    elif mode == "7day":
        fetch_hint = f"输出未来{days}天的天气"
        report_days = days
    else:
        fetch_hint = "查询当天天气"
        report_days = 1
    normalized_to = normalize_target(to)
    return (
        f"请运行 global-weather-service 技能中的 weather_report.py，为用户 {normalized_to} 查询 {city} 的{day_phrase}，并直接投递最终天气内容。"
        "数据源必须使用 Open-Meteo。"
        f"请在触发时重新查询最新数据，{fetch_hint}。"
        f"请使用命令 `python scripts\\weather_report.py \"{city}\" --days {report_days}` 生成天气简报。"
        "如果 mode 是 tomorrow，请在输出文案中明确这是明日天气，但仍只输出一份单日简报。"
        "输出格式必须为中文天气简报，包含标题、日期、天气、温度、生活指数、穿衣建议、紫外线和其他建议。"
        "不要解释过程，不要输出系统说明。"
    )


def create_cron_job(openclaw_cmd: str, *, to: str, city: str, time_text: str, timezone: str, mode: str, days: int) -> dict:
    at_value, cron_expr = resolve_schedule(time_text, timezone)
    name = build_subscription_name(city, mode)
    message = build_agent_message(to, city, mode, days)
    cmd = [
        openclaw_cmd,
        "cron",
        "add",
        "--name",
        name,
        "--session",
        "isolated",
        "--message",
        message,
        "--channel",
        "qqbot",
        "--to",
        normalize_target(to),
        "--announce",
        "--json",
    ]
    delete_after_run = False
    if cron_expr:
        cmd.extend(["--cron", cron_expr, "--tz", timezone])
    else:
        cmd.extend(["--at", at_value, "--delete-after-run"])
        delete_after_run = True
    result = run_cmd(cmd)
    if result.returncode != 0:
        raise SystemExit(result.stderr or result.stdout)
    payload = json.loads(result.stdout.strip())
    return {
        "id": payload.get("id"),
        "name": name,
        "timezone": timezone,
        "schedule": payload.get("schedule"),
        "delivery": payload.get("delivery"),
        "deleteAfterRun": delete_after_run,
    }


def build_entry(payload: dict, *, to: str, city: str, time_text: str, timezone: str, mode: str, days: int) -> dict:
    return {
        "id": payload.get("id"),
        "to": to,
        "city": city,
        "time": time_text,
        "timezone": timezone,
        "mode": mode,
        "days": days,
        "name": payload.get("name"),
        "schedule": payload.get("schedule"),
        "delivery": payload.get("delivery"),
        "deleteAfterRun": payload.get("deleteAfterRun"),
    }


def wait_for_state(predicate) -> None:
    for _ in range(STATE_SYNC_RETRIES):
        if predicate(load_state()):
            return
        time.sleep(STATE_SYNC_DELAY_SECONDS)


def create_subscription(to: str, city: str, time_text: str, days: int | None, mode: str | None) -> dict:
    timezone = ensure_timezone(to)
    openclaw_cmd = find_openclaw_cmd()
    resolved_mode, resolved_days = normalize_mode(mode, days)
    payload = create_cron_job(openclaw_cmd, to=to, city=city, time_text=time_text, timezone=timezone, mode=resolved_mode, days=resolved_days)
    items = load_state()
    entry = build_entry(payload, to=to, city=city, time_text=time_text, timezone=timezone, mode=resolved_mode, days=resolved_days)
    items = [x for x in items if x.get("id") != entry["id"]]
    items.append(entry)
    save_state(items)
    wait_for_state(lambda xs: any(x.get("id") == entry["id"] for x in xs))
    return entry


def list_subscriptions(to: str) -> list[dict]:
    return [x for x in load_state() if x.get("to") == to]


def find_subscription(job_id: str | None = None, name: str | None = None) -> dict:
    items = load_state()
    if job_id:
        found = next((x for x in items if x.get("id") == job_id), None)
        if not found:
            raise SystemExit("subscription not found")
        return found
    if name:
        matched = [x for x in items if x.get("name") == name or x.get("city") == name]
        if not matched:
            raise SystemExit("subscription not found")
        if len(matched) > 1:
            raise SystemExit("matched multiple subscriptions, please remove by --id")
        return matched[0]
    raise SystemExit("need --id or --name")


def remove_subscription(job_id: str | None = None, name: str | None = None) -> dict:
    existing = find_subscription(job_id=job_id, name=name)
    openclaw_cmd = find_openclaw_cmd()
    result = run_cmd([openclaw_cmd, "cron", "rm", existing["id"], "--json"])
    if result.returncode != 0:
        raise SystemExit(result.stderr or result.stdout)
    items = [x for x in load_state() if x.get("id") != existing["id"]]
    save_state(items)
    wait_for_state(lambda xs: all(x.get("id") != existing["id"] for x in xs))
    try:
        payload = json.loads(result.stdout or "{}")
    except Exception:
        payload = {"ok": True, "id": existing["id"]}
    payload["removedSubscription"] = existing
    return payload


def update_subscription(job_id: str, *, city: str | None, time_text: str | None, days: int | None, mode: str | None) -> dict:
    existing = find_subscription(job_id=job_id)
    to = existing.get("to")
    if not to:
        raise SystemExit("subscription missing target")

    next_city = city or existing.get("city")
    next_time = time_text or existing.get("time")
    next_mode = mode or existing.get("mode")
    next_days = days if days is not None else existing.get("days", 1)

    remove_subscription(job_id=job_id)
    try:
        return create_subscription(to, next_city, next_time, next_days, next_mode)
    except Exception:
        recreated = create_subscription(to, existing.get("city"), existing.get("time"), existing.get("days", 1), existing.get("mode"))
        raise SystemExit(f"update failed and original subscription was restored: {recreated.get('id')}")


def main() -> int:
    args = parse_args()

    if args.action == "get-timezone":
        if not args.to:
            raise SystemExit("get-timezone needs --to")
        print_json(get_timezone(args.to))
        return 0

    if args.action == "set-timezone":
        if not args.to or not args.timezone:
            raise SystemExit("set-timezone needs --to and --timezone")
        print_json(set_timezone(args.to, args.timezone))
        return 0

    if args.action == "list":
        if not args.to:
            raise SystemExit("list needs --to")
        print_json(list_subscriptions(args.to))
        return 0

    if args.action == "remove":
        if not args.id and not args.name:
            raise SystemExit("remove needs --id or --name")
        print_json(remove_subscription(job_id=args.id, name=args.name))
        return 0

    if args.action == "update":
        if not args.id:
            raise SystemExit("update needs --id")
        if args.time is None and args.city is None and args.days is None and args.mode is None:
            raise SystemExit("update needs at least one of --time or --city or --days or --mode")
        print_json(update_subscription(args.id, city=args.city, time_text=args.time, days=args.days, mode=args.mode))
        return 0

    if args.action == "add":
        if not args.to or not args.time or not args.city:
            raise SystemExit("add needs --to --time --city")
        ensure_timezone(args.to)
        print_json(create_subscription(args.to, args.city, args.time, args.days, args.mode))
        return 0

    raise SystemExit("unsupported action")


if __name__ == "__main__":
    raise SystemExit(main())

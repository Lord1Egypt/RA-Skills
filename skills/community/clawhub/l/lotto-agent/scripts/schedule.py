"""自动任务 + cron 触发 + openclaw 推送。"""
from __future__ import annotations

import json
import secrets
import shutil
import subprocess
from datetime import datetime, timedelta
from pathlib import Path
from typing import Any

import store
from store import cn_now, now_iso

# 推送：固定调用 PATH 中解析到的 openclaw（不允许配置任何自定义命令路径，避免 RCE）
OPENCLAW_CMD = shutil.which("openclaw")

_CONFIG_PATH = Path(__file__).resolve().parent.parent / "config" / "config.json"


def _load_config() -> dict[str, Any]:
    if not _CONFIG_PATH.exists():
        return {}
    return json.loads(_CONFIG_PATH.read_text(encoding="utf-8-sig"))


def _save_config(cfg: dict[str, Any]) -> None:
    _CONFIG_PATH.write_text(json.dumps(cfg, ensure_ascii=False, indent=2),
                             encoding="utf-8")


# ---------- 任务创建 / 列表 ----------
def create_task(action: str, params: dict[str, Any], schedule_kind: str,
                schedule_spec: str | None, time_start: str | None,
                time_end: str | None, random_window: bool = False,
                delivery: dict[str, Any] | None = None,
                raw_text: str = "") -> dict[str, Any]:
    if action not in {"generate", "check_prize", "draw_check_prize", "fetch_draw", "report"}:
        return {"ok": False, "error": f"未知任务 action: {action}"}
    if schedule_kind not in {"once", "daily", "weekly", "draw_day"}:
        return {"ok": False, "error": f"未知 schedule_kind: {schedule_kind}"}
    task_id = store.insert_task({
        "action": action,
        "params": params or {},
        "schedule_kind": schedule_kind,
        "schedule_spec": schedule_spec,
        "time_start": time_start or "09:00",
        "time_end": time_end or time_start or "09:00",
        "random_window": random_window,
        "delivery": delivery,
        "raw_text": raw_text,
    })
    text = _render_created(task_id, action, schedule_kind, schedule_spec,
                            time_start, time_end, params)
    cfg = _load_config()
    notify = cfg.get("notify") or {}
    followups: list[str] = ["任务已入库，cron 到点会自动跑。"]
    if not notify.get("enabled"):
        followups.append("主动消息推送还没开启。先 setup_notify 配置 channel/chat_id 并 --confirm，否则任务结果不会推送。")
    return {"ok": True, "task_id": task_id, "message_text": text,
            "followup_messages": followups}


def list_tasks(include_disabled: bool = False) -> dict[str, Any]:
    rows = store.list_all_tasks(include_disabled=include_disabled)
    if not rows:
        return {"ok": True, "tasks": [], "message_text": "当前没有自动任务。"}
    lines = ["自动任务"]
    for r in rows:
        lines.append(_render_task_line(r))
    return {"ok": True, "tasks": rows, "message_text": "\n".join(lines)}


def _render_task_line(row: dict[str, Any]) -> str:
    state = "" if row["enabled"] else "[已停用] "
    sched = _render_schedule(row.get("schedule_kind"), row.get("schedule_spec"),
                              row.get("time_start"), row.get("time_end"),
                              row.get("random_window"))
    p = json.loads(row.get("params_json") or "{}")
    act = _render_action(row.get("action"), p)
    return f"{state}#{row['id']} {sched}｜{act}"


def _render_schedule(kind: str | None, spec: str | None, ts: str | None,
                      te: str | None, random_window: int | None) -> str:
    window = ts or "09:00"
    if te and te != ts:
        window = f"{ts}-{te}{' 随机' if random_window else ''}"
    if kind == "once":
        return f"{spec or '指定日期'} {window}"
    if kind == "daily":
        return f"每天 {window}"
    if kind == "weekly":
        return f"每周{spec or ''} {window}"
    if kind == "draw_day":
        lot, off = (spec or ":0").split(":", 1) if spec else ("all", "0")
        prefix = "开奖当天" if int(off) == 0 else f"开奖前{abs(int(off))}天"
        return f"{prefix}({lot}) {window}"
    return window


def _render_action(action: str | None, params: dict[str, Any]) -> str:
    import lotto
    if action == "generate":
        lot = params.get("lottery") or "默认"
        name = lotto.LOTTERIES.get(lot, {}).get("name", lot)
        cnt = int(params.get("count", 1))
        parts = [f"生成{name}{cnt}注"]
        if int(params.get("multiple", 1)) > 1:
            parts.append(f"{params['multiple']}倍")
        if params.get("additional"):
            parts.append("追加")
        return "｜".join(parts)
    return {"check_prize": "自动兑奖", "draw_check_prize": "抓开奖并自动兑奖",
            "fetch_draw": "抓取开奖", "report": "生成报表"}.get(action or "", action or "")


def _render_created(task_id: int, action: str, kind: str, spec: str | None,
                     ts: str | None, te: str | None, params: dict[str, Any]) -> str:
    return (f"已创建自动任务 #{task_id}\n"
            f"{_render_schedule(kind, spec, ts, te, False)}\n"
            f"{_render_action(action, params)}")


# ---------- cron 调度 ----------
def cron_run(push: bool = False) -> dict[str, Any]:
    now = cn_now()
    results = []
    for task in store.list_enabled_tasks():
        if not _task_due(task, now):
            continue
        results.append(_run_task(task, now, push))
    return {"ok": all(r.get("ok", False) for r in results) if results else True,
            "fired": len(results), "results": results,
            "message_text": f"cron 触发 {len(results)} 个任务" if results else ""}


def _task_due(task: dict[str, Any], now: datetime) -> bool:
    key = _run_key(task, now)
    if task.get("last_run_key") == key:
        return False
    kind = task["schedule_kind"]
    if kind == "once":
        if task.get("schedule_spec") != now.date().isoformat():
            return False
        return _once_due(task, now, key)
    if kind == "weekly":
        weekdays = {int(x) for x in (task.get("schedule_spec") or "").split(",") if x}
        if weekdays and now.isoweekday() not in weekdays:
            return False
    if kind == "draw_day":
        spec = task.get("schedule_spec") or ":0"
        lot, off = spec.split(":", 1) if ":" in spec else (spec, "0")
        if not _is_draw_day_for_task(task["action"], lot, int(off), now):
            return False
    if task.get("random_window"):
        return _random_window_due(task, now, key)
    return _in_window(now, task.get("time_start") or "09:00",
                      task.get("time_end") or task.get("time_start") or "09:00")


def _once_due(task: dict[str, Any], now: datetime, key: str) -> bool:
    """一次性任务允许补跑：当天范围内、过了 time_start（或 planned_run_time），就触发。"""
    ts = task.get("time_start") or "09:00"
    te = task.get("time_end") or ts
    start_min = _to_min(ts)
    if start_min is None:
        return False
    cur = now.hour * 60 + now.minute
    if task.get("random_window"):
        planned = _planned_minutes(task, key, ts, te, now)
        return planned is not None and cur >= planned
    return cur >= start_min


def _is_draw_day_for_task(action: str, lottery: str, offset: int, now: datetime) -> bool:
    """对于 draw_day 触发器，判断 today - offset 是否是该彩种开奖日。"""
    target = (now.date() - timedelta(days=offset)).isoformat()
    if lottery == "all":
        return True
    import fetch
    if action in {"draw_check_prize", "check_prize"}:
        # 兑奖类不能用 next_fallback（buy_end 后会跳过今天），只看公共开奖日历
        return fetch.is_draw_day(lottery, target)
    fb = fetch.next_fallback(lottery, store.cn_now().date() if offset >= 0 else None)
    if fb.get("draw_date") == target:
        return True
    return fetch.is_draw_day(lottery, target)


def _in_window(now: datetime, start: str, end: str) -> bool:
    s = _to_min(start)
    e = _to_min(end)
    if s is None:
        return False
    if e is None or e == s:
        e = s + 9
    cur = now.hour * 60 + now.minute
    if e < s:
        return cur >= s or cur <= e
    return s <= cur <= e


def _random_window_due(task: dict[str, Any], now: datetime, key: str) -> bool:
    ts = task.get("time_start") or "09:00"
    te = task.get("time_end") or ts
    if not _in_window(now, ts, te):
        return False
    planned = _planned_minutes(task, key, ts, te, now)
    cur = now.hour * 60 + now.minute
    return planned is not None and cur >= planned


def _planned_minutes(task: dict[str, Any], key: str, ts: str, te: str, now: datetime) -> int | None:
    s = _to_min(ts); e = _to_min(te)
    if s is None: return None
    if e is None or e < s: e = s
    if task.get("planned_run_key") == key and task.get("planned_run_time"):
        return _to_min(str(task["planned_run_time"]))
    planned = secrets.SystemRandom().randint(s, e) if e > s else s
    planned_text = f"{planned // 60:02d}:{planned % 60:02d}"
    store.set_task_planned(int(task["id"]), key, planned_text)
    return planned


def _to_min(value: str | None) -> int | None:
    try:
        h, m = [int(p) for p in str(value or "").split(":")[:2]]
        return h * 60 + m
    except (TypeError, ValueError):
        return None


def _run_key(task: dict[str, Any], now: datetime) -> str:
    if task["schedule_kind"] == "once":
        return f"once:{task['id']}:{task.get('schedule_spec')}"
    if task["action"] == "draw_check_prize":
        return f"{task['id']}:{now.date().isoformat()}:{now.hour:02d}:{now.minute // 30}"
    return f"{task['id']}:{now.date().isoformat()}"


def _run_task(task: dict[str, Any], now: datetime, push: bool) -> dict[str, Any]:
    params = json.loads(task.get("params_json") or "{}")
    action = task["action"]
    try:
        result = _dispatch_task(action, params)
    except Exception as exc:
        result = {"ok": False, "error": str(exc), "message_text": f"{action} 执行失败：{exc}"}
    store.mark_task_run(int(task["id"]), _run_key(task, now))
    if task["schedule_kind"] == "once":
        store.disable_task(int(task["id"]))
    if push and result.get("message_text"):
        delivery = json.loads(task.get("delivery_json") or "null")
        result["push"] = push_message(result["message_text"], delivery=delivery,
                                       only_winning=action in {"check_prize", "draw_check_prize"} and result.get("winning_count", 0) == 0)
    return {"ok": result.get("ok", False), "task_id": task["id"], "result": result}


def _dispatch_task(action: str, params: dict[str, Any]) -> dict[str, Any]:
    import lotto, fetch
    if action == "generate":
        return lotto.generate(
            params.get("lottery", "dlt"),
            count=int(params.get("count", 1)),
            play_type=params.get("play_type"),
            multiple=int(params.get("multiple", 1)),
            is_additional=bool(params.get("additional", False)),
            budget=params.get("budget"),
        )
    if action == "check_prize":
        return lotto.check_prize(params.get("lottery"), params.get("issue"))
    if action == "fetch_draw":
        return fetch.fetch_draw(params.get("lottery", "all"), params.get("issue"))
    if action == "draw_check_prize":
        target = params.get("lottery") or "all"
        f = fetch.fetch_draw(target, params.get("issue"))
        check = lotto.check_prize(None if target == "all" else target, params.get("issue"))
        text = ""
        if int(check.get("checked_count", 0)) > 0:
            text = "\n\n".join(p for p in [f.get("message_text"), check.get("message_text")] if p)
        return {"ok": f.get("ok", False) and check.get("ok", False),
                "fetch": f, "check": check,
                "checked_count": check.get("checked_count", 0),
                "winning_count": check.get("winning_count", 0),
                "total_amount": check.get("total_amount", 0),
                "message_text": text}
    if action == "report":
        return lotto.report(int(params.get("since_days", 30)))
    return {"ok": False, "error": f"未知任务 action: {action}"}


# ---------- 推送 ----------
def push_message(content: str, delivery: dict[str, Any] | None = None,
                  only_winning: bool = False) -> dict[str, Any]:
    cfg = _load_config()
    notify = cfg.get("notify") or {}
    if not notify.get("enabled"):
        return {"ok": False, "sent": False, "requires_configuration": True,
                "payload": {"content": content},
                "message_text": "主动推送未开启，先 setup_notify --confirm。"}
    if only_winning:
        return {"ok": True, "sent": False, "skipped": "no_winning"}
    delivery = delivery or {}
    channel = str(delivery.get("channel") or notify.get("channel") or "")
    chat_id = str(delivery.get("chat_id") or notify.get("chat_id") or "")
    account = str(delivery.get("account_id") or notify.get("account_id") or "")
    if not channel or not chat_id:
        return {"ok": False, "sent": False, "requires_configuration": True,
                "payload": {"content": content},
                "message_text": "缺少 channel / chat_id，无法推送。"}
    if not OPENCLAW_CMD:
        return {"ok": False, "sent": False, "requires_configuration": True,
                "payload": {"content": content, "channel": channel, "chat_id": chat_id, "account_id": account},
                "message_text": "未在 PATH 中找到 openclaw 可执行文件。"}
    args = [OPENCLAW_CMD, "message", "send", "--channel", channel,
            "--target", chat_id, "--message", content]
    if account:
        args.extend(["--account", account])
    try:
        proc = subprocess.run(args, text=True, capture_output=True, check=False)
    except OSError as exc:
        return {"ok": False, "sent": False, "error": str(exc)}
    return {"ok": proc.returncode == 0, "sent": proc.returncode == 0,
            "stdout": proc.stdout.strip(), "stderr": proc.stderr.strip(),
            "returncode": proc.returncode}


# ---------- setup_notify ----------
def setup_notify(target: str | None, channel: str | None,
                  account_id: str | None, confirm: bool = False) -> dict[str, Any]:
    cfg = _load_config()
    notify = cfg.get("notify") or {}
    if target is not None: notify["chat_id"] = target
    if channel is not None: notify["channel"] = channel
    if account_id is not None: notify["account_id"] = account_id
    notify["enabled"] = bool(confirm and notify.get("chat_id") and notify.get("channel"))
    cfg["notify"] = notify
    _save_config(cfg)
    if not notify.get("chat_id") or not notify.get("channel"):
        return {"ok": False, "requires_configuration": True,
                "message_text": "缺少 channel 或 chat_id。请同时传 --channel 和 --chat-id。"}
    if not confirm:
        return {"ok": False, "requires_confirmation": True,
                "message_text": f"已暂存 channel={notify['channel']} / chat_id={notify['chat_id']}。"
                                "确认开启请加 --confirm。"}
    return {"ok": True, "enabled": True,
            "message_text": f"主动推送已开启：{notify['channel']} / {notify['chat_id']}"}

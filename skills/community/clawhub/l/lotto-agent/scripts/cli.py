"""CLI entry: argparse + dispatch. All actions live here as thin wrappers."""
from __future__ import annotations

import argparse
import json
import sys
from typing import Any

import store


def cmd_status(_: argparse.Namespace) -> dict[str, Any]:
    try:
        store.init_db()
    except OSError as exc:
        return {"ok": False, "error": str(exc),
                "data_dir": str(store.data_dir()),
                "db_path": str(store.db_path()),
                "message_text": f"数据库目录不可写：{store.data_dir()}"}
    return {"ok": True,
            "data_dir": str(store.data_dir()),
            "db_path": str(store.db_path()),
            "message_text": f"lotto-agent 正常，数据库就绪：{store.db_path()}"}


def cmd_generate(args: argparse.Namespace) -> dict[str, Any]:
    import lotto
    from nl import guard_text_intent
    guard = guard_text_intent(args.text)
    if guard:
        return guard
    return lotto.generate(
        lottery=args.lottery, count=int(args.count or 1),
        play_type=args.play_type, multiple=int(args.multiple or 1),
        is_additional=args.is_additional,
        budget=args.budget,
    )


def cmd_check_prize(args: argparse.Namespace) -> dict[str, Any]:
    import lotto
    return lotto.check_prize(lottery=args.lottery, issue=args.issue)


def cmd_fetch_draw(args: argparse.Namespace) -> dict[str, Any]:
    import fetch
    return fetch.fetch_draw(lottery=args.lottery or "all", issue=args.issue)


def cmd_report(args: argparse.Namespace) -> dict[str, Any]:
    import lotto
    return lotto.report(since_days=int(args.since or 30))


def cmd_cancel(args: argparse.Namespace) -> dict[str, Any]:
    n = store.cancel_recent(int(args.limit or 10))
    return {"ok": True, "cancelled": n,
            "message_text": f"已取消 {n} 注，不再计入成本和兑奖。"}


def cmd_record(args: argparse.Namespace) -> dict[str, Any]:
    import lotto
    return lotto.record_manual(
        lottery=args.lottery, text=args.text or "",
        multiple=int(args.multiple or 1),
        is_additional=bool(args.is_additional), issue=args.issue,
    )


def cmd_create_task(args: argparse.Namespace) -> dict[str, Any]:
    import schedule
    return schedule.create_task(
        action=args.task_action,
        params=_parse_json(args.params) or {},
        schedule_kind=args.schedule_kind, schedule_spec=args.schedule_spec,
        time_start=args.time_start, time_end=args.time_end,
        random_window=bool(args.random_window),
        delivery=_parse_json(args.delivery),
        raw_text=args.text or args.raw_text or "",
    )


def cmd_list_tasks(args: argparse.Namespace) -> dict[str, Any]:
    import schedule
    return schedule.list_tasks(include_disabled=bool(args.include_disabled))


def cmd_disable_task(args: argparse.Namespace) -> dict[str, Any]:
    n = store.disable_task(int(args.task_id))
    return {"ok": True, "disabled": n,
            "message_text": f"已停用 {n} 个自动任务。"}


def cmd_cron_run(args: argparse.Namespace) -> dict[str, Any]:
    import schedule
    return schedule.cron_run(push=bool(args.push))


def cmd_setup_notify(args: argparse.Namespace) -> dict[str, Any]:
    import schedule
    return schedule.setup_notify(target=args.chat_id or args.target,
                                  channel=args.channel,
                                  account_id=args.account_id,
                                  confirm=bool(args.confirm))


def cmd_parse(args: argparse.Namespace) -> dict[str, Any]:
    import nl
    return nl.parse(args.text or "")


ACTIONS = {
    "status":        cmd_status,
    "generate":      cmd_generate,
    "check_prize":   cmd_check_prize,
    "fetch_draw":    cmd_fetch_draw,
    "report":        cmd_report,
    "cancel":        cmd_cancel,
    "record":        cmd_record,
    "create_task":   cmd_create_task,
    "list_tasks":    cmd_list_tasks,
    "disable_task":  cmd_disable_task,
    "cron_run":      cmd_cron_run,
    "setup_notify":  cmd_setup_notify,
    "parse":         cmd_parse,
}


def _parse_json(value: str | None) -> Any:
    if value is None or value == "":
        return None
    try:
        return json.loads(value)
    except json.JSONDecodeError:
        return None


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(prog="lotto", description="lotto-agent v2 entry")
    p.add_argument("action", choices=list(ACTIONS.keys()))
    p.add_argument("--lottery", "--lottery-type", dest="lottery")
    p.add_argument("--count", type=int)
    p.add_argument("--budget", type=float)
    p.add_argument("--play-type", dest="play_type")
    p.add_argument("--multiple", type=int, default=1)
    p.add_argument("--additional", dest="is_additional", action="store_true")
    p.add_argument("--no-additional", dest="is_additional", action="store_false")
    p.set_defaults(is_additional=False)
    p.add_argument("--issue")
    p.add_argument("--since", type=int)
    p.add_argument("--limit", type=int, default=10)
    p.add_argument("--text")
    p.add_argument("--raw-text", dest="raw_text")
    p.add_argument("--task-action", dest="task_action")
    p.add_argument("--task-id", dest="task_id", type=int)
    p.add_argument("--schedule-kind", dest="schedule_kind")
    p.add_argument("--schedule-spec", dest="schedule_spec")
    p.add_argument("--time-start", dest="time_start")
    p.add_argument("--time-end", dest="time_end")
    p.add_argument("--random-window", dest="random_window", action="store_true")
    p.add_argument("--params")
    p.add_argument("--delivery")
    p.add_argument("--target")
    p.add_argument("--chat-id", dest="chat_id")
    p.add_argument("--channel")
    p.add_argument("--account-id", dest="account_id")
    p.add_argument("--confirm", action="store_true")
    p.add_argument("--include-disabled", dest="include_disabled", action="store_true")
    p.add_argument("--push", action="store_true")
    p.add_argument("--message-text", dest="message_text", action="store_true")
    return p


def main() -> None:
    args = build_parser().parse_args()
    store.init_db()
    handler = ACTIONS[args.action]
    result = handler(args)
    if args.message_text and isinstance(result, dict) and result.get("message_text"):
        print(result["message_text"])
        for msg in result.get("followup_messages") or []:
            print()
            print(msg)
    else:
        print(json.dumps(result, ensure_ascii=False, indent=2, default=str))
    sys.exit(0 if (isinstance(result, dict) and result.get("ok") in (True, None)) else 1)


if __name__ == "__main__":
    main()

from __future__ import annotations

import argparse
import json
import secrets
import string
import time

import cards
import gitea_api as g
import system_config as sc
from utils import json_fail, now_str


def out(data: dict) -> None:
    print(json.dumps(data, ensure_ascii=False))


def actor_id(args: argparse.Namespace) -> str:
    return args.sender_id or args.open_id


def normalize_chat_type(value: str) -> str:
    if value in {"group", "direct"}:
        return value
    if value == "p2p":
        return "direct"
    return value or ""


def require_group(args: argparse.Namespace) -> tuple[bool, dict]:
    chat_type = normalize_chat_type(args.chat_type)
    if chat_type != "group":
        return False, json_fail("not_group_chat", "请把我拉进团队群后，在群聊里 @我绑定本群。")
    if not args.chat_id:
        return False, json_fail("missing_chat_id", "OpenClaw 没有传入群聊 chat_id，不能稳定绑定群聊。")
    return True, {}


def get_actor_team(sender_id: str) -> tuple[dict | None, str, dict | None, dict | None]:
    users = sc.users()
    user = users.get(sender_id)
    if not user:
        return None, "", None, json_fail("user_not_registered", "请先私聊我完成个人知识库初始化。")
    team_id = user.get("team_id", "")
    if not team_id:
        return user, "", None, json_fail("user_not_in_team", "你还没有加入团队，不能绑定团队群。")
    team = sc.teams().get(team_id)
    if not team:
        return user, team_id, None, json_fail("team_not_found", "system-config 中找不到你的团队。")
    if sender_id not in team.get("admins", []):
        return user, team_id, team, json_fail("not_team_admin", "只有团队管理员可以绑定或解绑团队群。")
    return user, team_id, team, None


def make_code(prefix: str, pending: dict) -> str:
    alphabet = string.ascii_uppercase + string.digits
    for _ in range(20):
        suffix = "".join(secrets.choice(alphabet) for _ in range(4))
        code = f"{prefix}-{suffix}"
        if code not in pending:
            return code
    return f"{prefix}-{secrets.token_hex(3).upper()}"


def active_binding(chat_id: str) -> dict | None:
    binding = sc.chat_bindings().get(chat_id)
    if not binding or not binding.get("enabled", True):
        return None
    return binding


def update_team_binding_page(team_id: str, team: dict) -> None:
    bindings = [
        binding for binding in sc.chat_bindings().values()
        if binding.get("team_id") == team_id and binding.get("enabled", True)
    ]
    lines = [
        "# 群聊绑定",
        "",
        "本文件由 AIFusionBot 自动维护，用于人工查看当前团队群聊绑定状态。实际路由以 system-config/chat_bindings.json 为准。",
        "",
        f"更新时间：{now_str()}",
        "",
    ]
    if not bindings:
        lines.append("当前没有已启用的群聊绑定。")
    else:
        lines.extend([
            "| 群聊名称 | chat_id | 绑定人 | 绑定时间 | 状态 |",
            "| --- | --- | --- | --- | --- |",
        ])
        for binding in sorted(bindings, key=lambda item: item.get("bound_at", "")):
            lines.append(
                "| {chat_name} | `{chat_id}` | `{bound_by}` | {bound_at} | enabled |".format(
                    chat_name=binding.get("chat_name") or binding.get("chat_id", ""),
                    chat_id=binding.get("chat_id", ""),
                    bound_by=binding.get("bound_by", ""),
                    bound_at=binding.get("bound_at", ""),
                )
            )
    content = "\n".join(lines) + "\n"
    owner = team.get("team_kb_owner")
    repo = team.get("team_kb_repo")
    existing = g.get_file(owner, repo, "identity/group-bindings.md")
    g.put_file(owner, repo, "identity/group-bindings.md", content, "paper-kb: update group bindings", sha=existing[1] if existing else None)


def append_event(event: dict) -> None:
    event.setdefault("created_at", now_str())

    def mutate(current):
        if not isinstance(current, list):
            current = []
        current.append(event)
        return current

    sc.update_json("chat_binding_events.json", mutate, default=[])


def request_bind(args: argparse.Namespace) -> None:
    ok, error = require_group(args)
    if not ok:
        out(error)
        return
    sender_id = actor_id(args)
    user, team_id, team, error = get_actor_team(sender_id)
    if error:
        out(error)
        return
    binding = active_binding(args.chat_id)
    if binding:
        if binding.get("team_id") != team_id:
            out(json_fail("chat_already_bound", "本群已经绑定到其他团队，不能直接覆盖。请先由原团队管理员解绑。"))
            return
        if args.chat_name and args.chat_name != binding.get("chat_name"):
            binding["chat_name"] = args.chat_name
            binding["updated_at"] = now_str()
            sc.update_json("chat_bindings.json", lambda current: {**current, args.chat_id: binding}, default={})
            update_team_binding_page(team_id, team)
        out({
            "success": True,
            "already_bound": True,
            "chat_id": args.chat_id,
            "team_id": team_id,
            "team_name": team.get("team_name"),
            "message": "本群已经绑定到你的团队。",
        })
        return

    pending = sc.pending_chat_bindings()
    code = make_code("BIND", pending)
    record = {
        "action": "bind",
        "confirm_code": code,
        "chat_id": args.chat_id,
        "chat_name": args.chat_name or args.chat_id,
        "team_id": team_id,
        "team_name": team.get("team_name", ""),
        "team_kb_owner": team.get("team_kb_owner", g.BOT_USERNAME),
        "team_kb_repo": team.get("team_kb_repo", ""),
        "requested_by": sender_id,
        "created_at": now_str(),
        "expires_at_ts": int(time.time()) + args.ttl_minutes * 60,
    }
    sc.update_json("pending_chat_bindings.json", lambda current: {**current, code: record}, default={})
    out({
        "success": True,
        "needs_confirm": True,
        "confirm_code": code,
        "expires_in_minutes": args.ttl_minutes,
        "chat_id": args.chat_id,
        "chat_name": record["chat_name"],
        "team_id": team_id,
        "team_name": team.get("team_name"),
        "interactive_card": cards.bind_confirm("bind", code, team.get("team_name", ""), record["chat_name"], args.ttl_minutes),
    })


def confirm_bind(args: argparse.Namespace) -> None:
    ok, error = require_group(args)
    if not ok:
        out(error)
        return
    code = args.confirm_code.strip().upper()
    pending = sc.pending_chat_bindings()
    record = pending.get(code)
    if not record or record.get("action") != "bind":
        out(json_fail("pending_binding_not_found", "找不到待确认的群绑定请求，可能已过期或确认码错误。"))
        return
    if record.get("chat_id") != args.chat_id:
        out(json_fail("chat_id_mismatch", "确认绑定必须在发起绑定的同一个群里完成。"))
        return
    if int(time.time()) > int(record.get("expires_at_ts", 0)):
        sc.update_json("pending_chat_bindings.json", lambda current: {k: v for k, v in current.items() if k != code}, default={})
        out(json_fail("pending_binding_expired", "该绑定确认码已经过期，请重新发起绑定。"))
        return

    sender_id = actor_id(args)
    _user, team_id, team, error = get_actor_team(sender_id)
    if error:
        out(error)
        return
    if team_id != record.get("team_id"):
        out(json_fail("team_mismatch", "确认人必须是待绑定团队的管理员。"))
        return

    existing = active_binding(args.chat_id)
    if existing and existing.get("team_id") != team_id:
        out(json_fail("chat_already_bound", "本群在确认前已被绑定到其他团队，不能继续。"))
        return

    binding = {
        "chat_id": args.chat_id,
        "chat_name": args.chat_name or record.get("chat_name") or args.chat_id,
        "team_id": team_id,
        "team_name": team.get("team_name", ""),
        "team_kb_owner": team.get("team_kb_owner", g.BOT_USERNAME),
        "team_kb_repo": team.get("team_kb_repo", ""),
        "bound_by": sender_id,
        "bound_at": now_str(),
        "enabled": True,
    }

    def mutate_bindings(current: dict) -> dict:
        current[args.chat_id] = binding
        return current

    def mutate_pending(current: dict) -> dict:
        current.pop(code, None)
        return current

    try:
        sc.update_json("chat_bindings.json", mutate_bindings, default={})
        sc.update_json("pending_chat_bindings.json", mutate_pending, default={})
        append_event({"event": "bind", "chat_id": args.chat_id, "team_id": team_id, "actor": sender_id, "confirm_code": code})
        update_team_binding_page(team_id, team)
    except Exception as exc:
        out(json_fail("confirm_binding_failed", str(exc)))
        return
    out({"success": True, "bound": True, "binding": binding})


def request_unbind(args: argparse.Namespace) -> None:
    ok, error = require_group(args)
    if not ok:
        out(error)
        return
    binding = active_binding(args.chat_id)
    if not binding:
        out(json_fail("chat_not_bound", "本群还没有绑定团队。"))
        return
    sender_id = actor_id(args)
    _user, team_id, team, error = get_actor_team(sender_id)
    if error:
        out(error)
        return
    if binding.get("team_id") != team_id:
        out(json_fail("not_binding_team_admin", "只有当前绑定团队的管理员可以解绑本群。"))
        return

    pending = sc.pending_chat_bindings()
    code = make_code("UNBIND", pending)
    record = {
        "action": "unbind",
        "confirm_code": code,
        "chat_id": args.chat_id,
        "chat_name": binding.get("chat_name") or args.chat_name or args.chat_id,
        "team_id": team_id,
        "team_name": team.get("team_name", ""),
        "requested_by": sender_id,
        "created_at": now_str(),
        "expires_at_ts": int(time.time()) + args.ttl_minutes * 60,
    }
    sc.update_json("pending_chat_bindings.json", lambda current: {**current, code: record}, default={})
    out({
        "success": True,
        "needs_confirm": True,
        "confirm_code": code,
        "expires_in_minutes": args.ttl_minutes,
        "chat_id": args.chat_id,
        "team_id": team_id,
        "team_name": team.get("team_name"),
        "interactive_card": cards.bind_confirm("unbind", code, team.get("team_name", ""), record["chat_name"], args.ttl_minutes),
    })


def confirm_unbind(args: argparse.Namespace) -> None:
    ok, error = require_group(args)
    if not ok:
        out(error)
        return
    code = args.confirm_code.strip().upper()
    pending = sc.pending_chat_bindings()
    record = pending.get(code)
    if not record or record.get("action") != "unbind":
        out(json_fail("pending_unbind_not_found", "找不到待确认的解绑请求，可能已过期或确认码错误。"))
        return
    if record.get("chat_id") != args.chat_id:
        out(json_fail("chat_id_mismatch", "确认解绑必须在发起解绑的同一个群里完成。"))
        return
    if int(time.time()) > int(record.get("expires_at_ts", 0)):
        sc.update_json("pending_chat_bindings.json", lambda current: {k: v for k, v in current.items() if k != code}, default={})
        out(json_fail("pending_unbind_expired", "该解绑确认码已经过期，请重新发起解绑。"))
        return

    binding = active_binding(args.chat_id)
    if not binding:
        out(json_fail("chat_not_bound", "本群已经没有启用中的团队绑定。"))
        return
    sender_id = actor_id(args)
    _user, team_id, team, error = get_actor_team(sender_id)
    if error:
        out(error)
        return
    if binding.get("team_id") != team_id or team_id != record.get("team_id"):
        out(json_fail("not_binding_team_admin", "只有当前绑定团队的管理员可以确认解绑。"))
        return

    disabled = {**binding, "enabled": False, "unbound_by": sender_id, "unbound_at": now_str()}

    def mutate_bindings(current: dict) -> dict:
        current[args.chat_id] = disabled
        return current

    def mutate_pending(current: dict) -> dict:
        current.pop(code, None)
        return current

    try:
        sc.update_json("chat_bindings.json", mutate_bindings, default={})
        sc.update_json("pending_chat_bindings.json", mutate_pending, default={})
        append_event({"event": "unbind", "chat_id": args.chat_id, "team_id": team_id, "actor": sender_id, "confirm_code": code})
        update_team_binding_page(team_id, team)
    except Exception as exc:
        out(json_fail("confirm_unbind_failed", str(exc)))
        return
    out({"success": True, "unbound": True, "chat_id": args.chat_id, "team_id": team_id})


def cancel_pending(args: argparse.Namespace) -> None:
    ok, error = require_group(args)
    if not ok:
        out(error)
        return
    code = args.confirm_code.strip().upper()
    pending = sc.pending_chat_bindings()
    record = pending.get(code)
    if not record:
        out(json_fail("pending_request_not_found", "找不到待取消的群绑定/解绑请求。"))
        return
    if record.get("chat_id") != args.chat_id:
        out(json_fail("chat_id_mismatch", "取消操作必须在发起请求的同一个群里完成。"))
        return
    sender_id = actor_id(args)
    _user, team_id, _team, error = get_actor_team(sender_id)
    if error:
        out(error)
        return
    if team_id != record.get("team_id"):
        out(json_fail("team_mismatch", "只有该团队管理员可以取消本次请求。"))
        return

    def mutate(current: dict) -> dict:
        current.pop(code, None)
        return current

    sc.update_json("pending_chat_bindings.json", mutate, default={})
    append_event({"event": f"cancel_{record.get('action', 'pending')}", "chat_id": args.chat_id, "team_id": team_id, "actor": sender_id, "confirm_code": code})
    out({"success": True, "cancelled": True, "confirm_code": code, "action": record.get("action", "")})


def status(args: argparse.Namespace) -> None:
    chat_type = normalize_chat_type(args.chat_type)
    if chat_type != "group":
        sender_id = actor_id(args)
        user = sc.users().get(sender_id)
        out({"success": True, "chat_type": chat_type or "direct", "user": user, "message": "私聊没有群绑定；私聊按用户 open_id 路由。"})
        return
    if not args.chat_id:
        out(json_fail("missing_chat_id", "OpenClaw 没有传入群聊 chat_id。"))
        return
    binding = active_binding(args.chat_id)
    if not binding:
        out({"success": True, "bound": False, "chat_id": args.chat_id})
        return
    out({"success": True, "bound": True, "binding": binding})


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--action", required=True, choices=["request_bind", "confirm_bind", "request_unbind", "confirm_unbind", "cancel_pending", "status"])
    parser.add_argument("--open_id", default="", help="Backward-compatible alias for SenderId.")
    parser.add_argument("--sender_id", default="", help="OpenClaw SenderId: the message sender open_id.")
    parser.add_argument("--chat_type", default="", help="OpenClaw ChatType: direct/group.")
    parser.add_argument("--chat_id", default="", help="OpenClaw GroupSubject in group chats.")
    parser.add_argument("--chat_name", default="", help="Optional result from feishu_chat(action=get).")
    parser.add_argument("--confirm_code", default="")
    parser.add_argument("--ttl_minutes", type=int, default=10)
    args = parser.parse_args()

    if not actor_id(args):
        out(json_fail("missing_sender_id", "缺少 SenderId，不能校验操作者。"))
        return

    actions = {
        "request_bind": request_bind,
        "confirm_bind": confirm_bind,
        "request_unbind": request_unbind,
        "confirm_unbind": confirm_unbind,
        "cancel_pending": cancel_pending,
        "status": status,
    }
    actions[args.action](args)


if __name__ == "__main__":
    main()

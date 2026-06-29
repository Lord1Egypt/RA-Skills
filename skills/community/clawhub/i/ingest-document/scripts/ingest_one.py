from __future__ import annotations

import argparse
import json

import cards
import chat_context
import system_config as sc
from utils import json_fail


def out(data: dict) -> None:
    print(json.dumps(data, ensure_ascii=False))


def looks_like_team_meeting(text: str) -> bool:
    markers = ["组会", "会议", "参会", "参与者", "待办", "负责人", "我们", "项目", "讨论", "决定"]
    return sum(1 for marker in markers if marker in text) >= 2


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--open_id", default="", help="Backward-compatible alias for SenderId.")
    parser.add_argument("--sender_id", default="", help="OpenClaw SenderId: the message sender open_id.")
    parser.add_argument("--chat_type", default="", help="OpenClaw ChatType: direct/group.")
    parser.add_argument("--chat_id", default="", help="OpenClaw GroupSubject in group chats.")
    parser.add_argument("--message_sid", default="", help="OpenClaw MessageSid for audit.")
    parser.add_argument("--message", default="")
    parser.add_argument("--explicit_target", default="", choices=["", "personal", "team", "both"])
    parser.add_argument("--from_group", action="store_true")
    parser.add_argument("--type_hint", default="")
    parser.add_argument("--project_id", default="")
    args = parser.parse_args()

    sender_id = chat_context.actor_id(args.open_id, args.sender_id)
    if not sender_id:
        out(json_fail("missing_sender_id", "缺少 SenderId，不能识别用户。"))
        return

    chat_type = chat_context.normalize_chat_type(args.chat_type)
    is_group = chat_type == "group" or args.from_group
    if is_group:
        if args.explicit_target in {"personal", "both"}:
            out(json_fail("personal_scope_not_allowed_in_group", "群聊中不能把资料存入个人知识库。请私聊我处理个人资料。"))
            return
        group, error = chat_context.resolve_group_context(sender_id, args.chat_id)
        if error:
            out(error)
            return
        team = group["team"]
        target = "team"
        team_kb = {
            "owner": team.get("team_kb_owner"),
            "repo": team.get("team_kb_repo"),
            "team_id": group["team_id"],
            "project_id": args.project_id or "general",
            "role": group["user"].get("role"),
        }
        out({
            "success": True,
            "chat_type": "group",
            "chat_id": args.chat_id,
            "message_sid": args.message_sid,
            "target": target,
            "needs_confirm": False,
            "confirm_reason": "",
            "personal_kb": None,
            "team_kb": team_kb,
            "binding": group["binding"],
            "created_by": sender_id,
            "can_create_project": chat_context.is_team_admin(sender_id, team),
        })
        return

    users = sc.users()
    user = users.get(sender_id)
    if not user:
        out(json_fail("user_not_registered", "请先完成个人知识库初始化。"))
        return
    teams = sc.teams()
    team = teams.get(user.get("team_id", ""))

    target = args.explicit_target
    needs_confirm = False
    confirm_reason = ""
    if not target:
        if args.type_hint == "meeting" or looks_like_team_meeting(args.message):
            if team:
                needs_confirm = True
                confirm_reason = "这看起来像团队会议或项目资料，请确认存入团队知识库还是个人知识库。"
                target = "needs_target_confirmation"
            else:
                target = "personal"
        else:
            target = "personal"

    if target in {"team", "both"} and not team:
        out(json_fail("no_team", "你还没有加入团队，不能存入团队知识库。"))
        return

    personal = {
        "owner": user.get("personal_kb_owner") or user.get("gitea_username"),
        "repo": user.get("personal_kb_repo"),
    }
    team_kb = ({
        "owner": team.get("team_kb_owner"),
        "repo": team.get("team_kb_repo"),
        "team_id": user.get("team_id"),
        "project_id": args.project_id or "general",
        "role": user.get("role"),
    } if team else None)

    out({
        "success": True,
        "chat_type": chat_type or "direct",
        "chat_id": args.chat_id,
        "message_sid": args.message_sid,
        "target": target,
        "needs_confirm": needs_confirm,
        "confirm_reason": confirm_reason,
        "personal_kb": personal,
        "team_kb": team_kb,
        "created_by": sender_id,
        "can_create_project": bool(team and chat_context.is_team_admin(sender_id, team)),
        "interactive_card": cards.target_confirm(confirm_reason, bool(team)) if needs_confirm else None,
    })


if __name__ == "__main__":
    main()

from __future__ import annotations

import argparse
import json

from utils import json_fail


def out(data: dict) -> None:
    print(json.dumps(data, ensure_ascii=False))


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--action_value", required=True)
    args = parser.parse_args()

    value = args.action_value.strip()
    if value == "register_user":
        out({
            "success": True,
            "action": value,
            "command": "init_user.py",
            "args": {"register": True},
            "form_values_arg": "form_values_json",
        })
        return

    if value in {"join_team", "create_team", "personal_only", "submit_join_team", "submit_create_team"}:
        out({
            "success": True,
            "action": value,
            "command": "resolve_pending_action.py",
            "pass_card_values": True,
        })
        return

    for prefix, command, action in [
        ("confirm_bind:", "bind_chat.py", "confirm_bind"),
        ("confirm_unbind:", "bind_chat.py", "confirm_unbind"),
        ("cancel_bind:", "bind_chat.py", "cancel_pending"),
        ("cancel_unbind:", "bind_chat.py", "cancel_pending"),
    ]:
        if value.startswith(prefix):
            code = value.split(":", 1)[1]
            out({
                "success": True,
                "action": action,
                "command": command,
                "args": {"action": action, "confirm_code": code},
            })
            return

    out(json_fail("unknown_card_action", "无法识别 init_workspace 卡片动作。"))


if __name__ == "__main__":
    main()

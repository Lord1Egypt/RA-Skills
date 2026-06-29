from __future__ import annotations

import argparse
import json

import cards
import system_config as sc
from utils import json_fail, now_str


def out(data: dict) -> None:
    print(json.dumps(data, ensure_ascii=False))


def task_key(kind: str, open_id: str) -> str:
    return f"{kind}:{open_id}"


def normalize_choice(message: str) -> str:
    text = (message or "").strip().lower()
    mapping = {
        "1": "1",
        "一": "1",
        "加入": "1",
        "加入团队": "1",
        "加入已有团队": "1",
        "join_team": "1",
        "submit_join_team": "1",
        "2": "2",
        "二": "2",
        "创建": "2",
        "创建团队": "2",
        "创建新团队": "2",
        "新团队": "2",
        "create_team": "2",
        "submit_create_team": "2",
        "3": "3",
        "三": "3",
        "暂时": "3",
        "暂时不加入": "3",
        "暂时单独使用": "3",
        "单独使用": "3",
        "不加入": "3",
        "personal_only": "3",
    }
    return mapping.get(text, text)


def parse_form_values(raw: str) -> dict:
    if not raw:
        return {}
    try:
        data = json.loads(raw)
    except json.JSONDecodeError:
        return {}
    return data if isinstance(data, dict) else {}


def parse_labeled_text(message: str) -> dict:
    values = {}
    labels = {
        "团队名称": "team_name",
        "团队名": "team_name",
        "team_name": "team_name",
        "研究方向": "research_direction",
        "团队研究方向": "research_direction",
        "research_direction": "research_direction",
        "邀请码": "invite_code",
        "invite_code": "invite_code",
    }
    for line in (message or "").splitlines():
        if ":" in line:
            key, value = line.split(":", 1)
        elif "：" in line:
            key, value = line.split("：", 1)
        else:
            continue
        mapped = labels.get(key.strip())
        if mapped and value.strip():
            values[mapped] = value.strip()
    return values


def form_value(values: dict, key: str) -> str:
    value = values.get(key, "")
    if isinstance(value, dict):
        value = value.get("value") or value.get("text") or value.get("input_value") or ""
    if isinstance(value, list):
        value = value[0] if value else ""
    if isinstance(value, str):
        return value.strip()
    return str(value).strip() if value is not None else ""


def replace_task(remove_key: str, new_key: str | None, new_task: dict | None) -> None:
    def mutate(current: dict) -> dict:
        current.pop(remove_key, None)
        if new_key and new_task:
            current[new_key] = new_task
        return current

    sc.update_json("active_tasks.json", mutate, default={})


def resolve_collect_info_task(open_id: str, message: str, form_values: dict) -> bool:
    tasks = sc.active_tasks()
    merged = {**parse_labeled_text(message), **form_values}

    join_key = task_key("join_team_collect_info", open_id)
    if tasks.get(join_key, {}).get("type") == "join_team_collect_info":
        team_name = form_value(merged, "team_name")
        invite_code = form_value(merged, "invite_code")
        missing = [name for name, value in {"team_name": team_name, "invite_code": invite_code}.items() if not value]
        if missing:
            out({
                "success": True,
                "has_pending_action": True,
                "action": "join_team",
                "needs_input": True,
                "missing_fields": missing,
                "interactive_card": cards.join_team_form(open_id),
            })
            return True
        out({
            "success": True,
            "has_pending_action": True,
            "action": "join_team",
            "ready_to_execute": True,
            "command": "join_team.py",
            "args": {"open_id": open_id, "team_name": team_name, "invite_code": invite_code},
        })
        return True

    create_key = task_key("create_team_collect_info", open_id)
    if tasks.get(create_key, {}).get("type") == "create_team_collect_info":
        team_name = form_value(merged, "team_name")
        direction = form_value(merged, "research_direction")
        missing = [name for name, value in {"team_name": team_name, "research_direction": direction}.items() if not value]
        if missing:
            out({
                "success": True,
                "has_pending_action": True,
                "action": "create_team",
                "needs_input": True,
                "missing_fields": missing,
                "interactive_card": cards.create_team_form(open_id),
            })
            return True
        out({
            "success": True,
            "has_pending_action": True,
            "action": "create_team",
            "ready_to_execute": True,
            "command": "init_team.py",
            "args": {"open_id": open_id, "team_name": team_name, "research_direction": direction},
        })
        return True
    return False


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--open_id", required=True)
    parser.add_argument("--message", default="")
    parser.add_argument("--action_value", default="", help="OpenClaw CardActionValue.")
    parser.add_argument("--form_values_json", default="", help="OpenClaw CardFormValues as JSON.")
    args = parser.parse_args()

    form_values = parse_form_values(args.form_values_json)
    message = args.action_value or args.message
    if resolve_collect_info_task(args.open_id, message, form_values):
        return

    tasks = sc.active_tasks()
    post_key = task_key("post_init_choice", args.open_id)
    post_task = tasks.get(post_key)
    if not post_task:
        out({"success": True, "has_pending_action": False})
        return
    if post_task.get("type") != "post_init_choice":
        out(json_fail("bad_pending_action", "待处理动作不是初始化后选择。"))
        return

    choice = normalize_choice(message)
    if choice not in {"1", "2", "3"}:
        data = json_fail("unknown_choice", "请在 1、2、3 中选择：1 加入已有团队，2 创建新团队，3 暂时单独使用。")
        data["interactive_card"] = cards.post_init_choice(args.open_id)
        out(data)
        return

    if choice == "1":
        new_key = task_key("join_team_collect_info", args.open_id)
        new_task = {
            "type": "join_team_collect_info",
            "open_id": args.open_id,
            "required_fields": ["team_name", "invite_code"],
            "created_at": now_str(),
        }
        replace_task(post_key, new_key, new_task)
        out({
            "success": True,
            "has_pending_action": True,
            "action": "join_team",
            "needs_input": True,
            "required_fields": new_task["required_fields"],
            "prompt": "请提供团队名称和邀请码。",
            "interactive_card": cards.join_team_form(args.open_id),
        })
        return

    if choice == "2":
        new_key = task_key("create_team_collect_info", args.open_id)
        new_task = {
            "type": "create_team_collect_info",
            "open_id": args.open_id,
            "required_fields": ["team_name", "research_direction"],
            "created_at": now_str(),
        }
        replace_task(post_key, new_key, new_task)
        out({
            "success": True,
            "has_pending_action": True,
            "action": "create_team",
            "needs_input": True,
            "required_fields": new_task["required_fields"],
            "prompt": "请提供团队名称和团队研究方向。拿到这两个字段后才能创建团队。",
            "interactive_card": cards.create_team_form(args.open_id),
        })
        return

    replace_task(post_key, None, None)
    out({
        "success": True,
        "has_pending_action": True,
        "action": "personal_only",
        "needs_input": False,
        "message": "已保留为暂时单独使用个人知识库。之后仍可通过“加入团队”或“创建团队”继续配置。",
    })


if __name__ == "__main__":
    main()

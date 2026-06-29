from __future__ import annotations

import argparse
import json
import sys

import cards
import gitea_api as g
import kb_schema as schema
import kb_templates as tpl
import system_config as sc
from utils import json_fail, now_str


def out(data: dict) -> None:
    print(json.dumps(data, ensure_ascii=False))


def init_personal_repo(username: str, name: str, direction: str) -> str:
    repo = f"{username}-personal-kb"
    g.create_repo_for_user(username, repo, f"个人科研知识库 | {direction}", private=True)
    g.add_collaborator(username, repo, g.BOT_USERNAME, "admin")
    for folder in schema.summary_folders() + schema.PERSONAL_EXTRA_DIRS:
        g.ensure_file(username, repo, f"{folder}/.gitkeep", "", f"init {folder}")
    for path, content in {
        "README.md": tpl.readme(f"{name} 的个人知识库", "personal", direction),
        "AGENTS.md": tpl.agents_schema(),
        "index.md": f"# {name} 的个人知识库\n\n",
        "catalog.json": tpl.empty_catalog(),
        "log.md": "# Log\n\n",
        "linked_team_items.json": "[]\n",
    }.items():
        g.ensure_file(username, repo, path, content, f"init {path}")
    return repo


def record_recovery(kind: str, operations: list[dict], error: str) -> str:
    error_id = sc.new_record_id("prov")
    payload = {
        "kind": kind,
        "status": "pending",
        "operations": operations,
        "error": error,
        "created_at": now_str(),
    }
    try:
        sc.update_json("provisioning_errors.json", lambda current: {**current, error_id: payload}, default={})
        return error_id
    except Exception as exc:
        return f"FAILED:{exc}"


def set_post_init_choice(open_id: str) -> None:
    task_id = f"post_init_choice:{open_id}"
    task = {
        "type": "post_init_choice",
        "open_id": open_id,
        "options": {
            "1": "join_team",
            "2": "create_team",
            "3": "personal_only",
        },
        "created_at": now_str(),
    }
    sc.update_json("active_tasks.json", lambda current: {**current, task_id: task}, default={})


def parse_form_values(raw: str) -> dict:
    if not raw:
        return {}
    try:
        data = json.loads(raw)
    except json.JSONDecodeError:
        return {}
    return data if isinstance(data, dict) else {}


def form_value(values: dict, key: str) -> str:
    value = values.get(key, "")
    if isinstance(value, dict):
        value = value.get("value") or value.get("text") or value.get("input_value") or ""
    if isinstance(value, list):
        value = value[0] if value else ""
    return value.strip() if isinstance(value, str) else str(value).strip() if value is not None else ""


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true")
    parser.add_argument("--register", action="store_true")
    parser.add_argument("--open_id", required=True)
    parser.add_argument("--gitea_username", default="")
    parser.add_argument("--name", default="")
    parser.add_argument("--research_direction", default="")
    parser.add_argument("--form_values_json", default="", help="OpenClaw CardFormValues as JSON.")
    args = parser.parse_args()

    if not g.ADMIN_TOKEN:
        out(json_fail("missing_token", "未配置 GITEA_ADMIN_TOKEN。"))
        return
    sc.ensure_system_repo()
    users = sc.users()

    if args.check:
        user = users.get(args.open_id)
        data = {"success": True, "registered": bool(user), "user": user, "gitea_url": g.GITEA_URL}
        if not user:
            data["interactive_card"] = cards.registration_form(g.GITEA_URL)
        out(data)
        return

    if not args.register:
        out(json_fail("invalid_mode", "必须指定 --check 或 --register。"))
        return
    form_values = parse_form_values(args.form_values_json)
    if form_values:
        args.gitea_username = args.gitea_username or form_value(form_values, "gitea_username")
        args.name = args.name or form_value(form_values, "name")
        args.research_direction = args.research_direction or form_value(form_values, "research_direction")
    if not (args.gitea_username and args.name and args.research_direction):
        data = json_fail("missing_arg", "注册需要 Gitea用户名、姓名、研究方向。")
        data["interactive_card"] = cards.registration_form(g.GITEA_URL)
        out(data)
        return
    if args.open_id in users:
        out({"success": True, "already_registered": True, "user": users[args.open_id]})
        return
    for oid, existing in users.items():
        if existing.get("gitea_username") == args.gitea_username:
            out(json_fail("username_taken", f"Gitea 用户 {args.gitea_username} 已绑定到另一个飞书用户。"))
            return
    if not g.get_user(args.gitea_username):
        out(json_fail("gitea_user_not_found", f"Gitea 上找不到用户 {args.gitea_username}，请先在 {g.GITEA_URL} 注册。"))
        return
    try:
        repo = init_personal_repo(args.gitea_username, args.name, args.research_direction)
    except Exception as exc:
        out(json_fail("init_personal_failed", str(exc)))
        return
    record = {
        "gitea_username": args.gitea_username,
        "name": args.name,
        "research_direction": args.research_direction,
        "personal_kb_owner": args.gitea_username,
        "personal_kb_repo": repo,
        "team_id": "",
        "role": "personal_only",
        "created_at": now_str(),
    }
    def mutate(current: dict) -> dict:
        if args.open_id in current:
            raise ValueError("该飞书用户已注册。")
        for existing in current.values():
            if existing.get("gitea_username") == args.gitea_username:
                raise ValueError(f"Gitea 用户 {args.gitea_username} 已绑定到另一个飞书用户。")
        current[args.open_id] = record
        return current

    try:
        sc.update_json("users.json", mutate, default={})
    except Exception as exc:
        recovery_id = record_recovery("init_user", [{
            "file": "users.json",
            "key": args.open_id,
            "record": record,
            "mode": "insert_if_absent",
        }], str(exc))
        recovery_failed = recovery_id.startswith("FAILED:")
        data = json_fail("write_user_failed", str(exc))
        data.update({
            "recoverable": True,
            "recovery_failed": recovery_failed,
            "recovery_id": "" if recovery_failed else recovery_id,
            "recovery_error": recovery_id.removeprefix("FAILED:") if recovery_failed else "",
            "personal_repo_url": f"{g.GITEA_URL}/{args.gitea_username}/{repo}",
        })
        out(data)
        return
    try:
        set_post_init_choice(args.open_id)
    except Exception as exc:
        out({
            "success": True,
            "user": record,
            "personal_repo_url": f"{g.GITEA_URL}/{args.gitea_username}/{repo}",
            "post_init_choice_pending": False,
            "warning": f"个人知识库已创建，但初始化下一步选择状态写入失败：{exc}",
        })
        return
    out({
        "success": True,
        "user": record,
        "personal_repo_url": f"{g.GITEA_URL}/{args.gitea_username}/{repo}",
        "post_init_choice_pending": True,
        "next_options": {
            "1": "join_team",
            "2": "create_team",
            "3": "personal_only",
        },
        "interactive_card": cards.post_init_choice(args.open_id, f"{g.GITEA_URL}/{args.gitea_username}/{repo}"),
    })


if __name__ == "__main__":
    main()

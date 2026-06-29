from __future__ import annotations

import argparse
import hashlib
import json

import gitea_api as g
import kb_schema as schema
import kb_templates as tpl
import system_config as sc
from utils import json_fail, now_str, slugify


def out(data: dict) -> None:
    print(json.dumps(data, ensure_ascii=False))


def make_team_repo_name(team_name: str) -> str:
    return f"{slugify(team_name, 'team')}-team-kb"


def clear_pending_team_creation(open_id: str) -> None:
    def mutate(current: dict) -> dict:
        current.pop(f"post_init_choice:{open_id}", None)
        current.pop(f"create_team_collect_info:{open_id}", None)
        return current

    sc.update_json("active_tasks.json", mutate, default={})


def init_team_repo(repo: str, team_name: str, direction: str, invite_code: str) -> None:
    g.create_bot_repo(repo, f"团队科研知识库 | {team_name}", private=True)
    for folder in schema.summary_folders() + schema.TEAM_EXTRA_DIRS:
        g.ensure_file(g.BOT_USERNAME, repo, f"{folder}/.gitkeep", "", f"init {folder}")
    for name, content in schema.PROJECT_FILES.items():
        g.ensure_file(g.BOT_USERNAME, repo, f"projects/general/{name}", content, f"init general {name}")
    team_catalog = json.loads(tpl.empty_catalog())
    team_catalog["projects"] = [{
        "project_id": "general",
        "name": "General",
        "folder": "projects/general",
        "brief": "团队公共资料",
        "documents": [],
        "people": [],
        "updated_at": now_str(),
    }]
    for path, content in {
        "README.md": tpl.readme(f"{team_name} 团队知识库", "team", direction),
        "TEAM_INFO.md": tpl.team_info(team_name, direction, invite_code, repo),
        "identity/group-bindings.md": "# 群聊绑定\n\n当前没有已启用的群聊绑定。\n",
        "AGENTS.md": tpl.agents_schema(),
        "index.md": f"# {team_name} 团队知识库\n\n",
        "catalog.json": json.dumps(team_catalog, ensure_ascii=False, indent=2),
        "log.md": "# Log\n\n",
    }.items():
        g.ensure_file(g.BOT_USERNAME, repo, path, content, f"init {path}")


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


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--open_id", required=True)
    parser.add_argument("--team_name", required=True)
    parser.add_argument("--research_direction", required=True)
    args = parser.parse_args()

    sc.ensure_system_repo()
    users = sc.users()
    user = users.get(args.open_id)
    if not user:
        out(json_fail("user_not_registered", "请先完成个人知识库初始化。"))
        return
    if user.get("team_id"):
        out(json_fail("already_in_team", "当前版本一个用户只能加入一个团队。"))
        return
    team_id = "team_" + hashlib.sha1(args.team_name.encode("utf-8")).hexdigest()[:8]
    teams = sc.teams()
    if team_id in teams or any(t.get("team_name") == args.team_name for t in teams.values()):
        out(json_fail("team_exists", "已存在同名团队，请加入该团队或换一个名称。"))
        return
    invite = sc.make_invite_code(args.team_name)
    repo = make_team_repo_name(args.team_name)
    if g.repo_exists(g.BOT_USERNAME, repo):
        out(json_fail("team_repo_exists", f"团队知识库仓库名 {repo} 已存在，请换一个团队名称或提供更明确的团队名称。"))
        return
    try:
        init_team_repo(repo, args.team_name, args.research_direction, invite)
        g.add_collaborator(g.BOT_USERNAME, repo, user["gitea_username"], "write")
    except Exception as exc:
        out(json_fail("init_team_failed", str(exc)))
        return
    team_record = {
        "team_id": team_id,
        "team_name": args.team_name,
        "research_direction": args.research_direction,
        "team_kb_owner": g.BOT_USERNAME,
        "team_kb_repo": repo,
        "admins": [args.open_id],
        "members": [args.open_id],
        "invite_code": invite,
        "projects": {"general": {"name": "General", "description": "团队公共资料", "created_at": now_str()}},
        "created_at": now_str(),
    }
    user["team_id"] = team_id
    user["role"] = "admin"
    try:
        sc.update_json("teams.json", lambda current: {**current, team_id: team_record}, default={})

        def mutate_users(current: dict) -> dict:
            current[args.open_id] = user
            return current

        sc.update_json("users.json", mutate_users, default={})
    except Exception as exc:
        recovery_id = record_recovery("init_team", [
            {
                "file": "teams.json",
                "key": team_id,
                "record": team_record,
                "mode": "insert_if_absent",
            },
            {
                "file": "users.json",
                "key": args.open_id,
                "record": user,
                "mode": "replace",
            },
        ], str(exc))
        recovery_failed = recovery_id.startswith("FAILED:")
        data = json_fail("write_team_failed", str(exc))
        data.update({
            "recoverable": True,
            "recovery_failed": recovery_failed,
            "recovery_id": "" if recovery_failed else recovery_id,
            "recovery_error": recovery_id.removeprefix("FAILED:") if recovery_failed else "",
            "team_repo_url": f"{g.GITEA_URL}/{g.BOT_USERNAME}/{repo}",
        })
        out(data)
        return
    cleanup_warning = ""
    try:
        clear_pending_team_creation(args.open_id)
    except Exception as exc:
        cleanup_warning = f"团队已创建，但初始化待办状态清理失败：{exc}"
    out({
        "success": True,
        "team_id": team_id,
        "team_kb_repo": repo,
        "invite_code": invite,
        "team_repo_url": f"{g.GITEA_URL}/{g.BOT_USERNAME}/{repo}",
        "warning": cleanup_warning,
    })


if __name__ == "__main__":
    main()

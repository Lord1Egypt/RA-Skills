from __future__ import annotations

import argparse
import json

import gitea_api as g
import system_config as sc
from utils import json_fail


def out(data: dict) -> None:
    print(json.dumps(data, ensure_ascii=False))


def clear_pending_join(open_id: str) -> None:
    def mutate(current: dict) -> dict:
        current.pop(f"post_init_choice:{open_id}", None)
        current.pop(f"join_team_collect_info:{open_id}", None)
        return current

    sc.update_json("active_tasks.json", mutate, default={})


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--open_id", required=True)
    parser.add_argument("--team_name", required=True)
    parser.add_argument("--invite_code", required=True)
    args = parser.parse_args()
    users = sc.users()
    user = users.get(args.open_id)
    if not user:
        out(json_fail("user_not_registered", "请先完成个人知识库初始化。"))
        return
    if user.get("team_id"):
        out(json_fail("already_in_team", "当前版本一个用户只能加入一个团队。"))
        return
    teams = sc.teams()
    target_id = None
    for team_id, team in teams.items():
        if team.get("team_name") == args.team_name:
            target_id = team_id
            break
    if not target_id:
        out(json_fail("team_not_found", "找不到该团队。"))
        return
    team = teams[target_id]
    if team.get("invite_code") != args.invite_code:
        out(json_fail("bad_invite_code", "邀请码不正确。"))
        return
    try:
        g.add_collaborator(team["team_kb_owner"], team["team_kb_repo"], user["gitea_username"], "read")
    except Exception as exc:
        out(json_fail("grant_permission_failed", str(exc)))
        return
    user["team_id"] = target_id
    user["role"] = "member"
    try:
        def mutate_teams(current: dict) -> dict:
            t = current[target_id]
            members = t.setdefault("members", [])
            if args.open_id not in members:
                members.append(args.open_id)
            current[target_id] = t
            return current

        def mutate_users(current: dict) -> dict:
            current[args.open_id] = user
            return current

        sc.update_json("teams.json", mutate_teams, default={})
        sc.update_json("users.json", mutate_users, default={})
    except Exception as exc:
        out(json_fail("write_join_failed", str(exc)))
        return
    cleanup_warning = ""
    try:
        clear_pending_join(args.open_id)
    except Exception as exc:
        cleanup_warning = f"已加入团队，但初始化待办状态清理失败：{exc}"
    out({
        "success": True,
        "team_id": target_id,
        "team_repo_url": f"{g.GITEA_URL}/{team['team_kb_owner']}/{team['team_kb_repo']}",
        "warning": cleanup_warning,
    })


if __name__ == "__main__":
    main()

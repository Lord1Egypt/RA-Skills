#!/usr/bin/env python3
"""
Harbor 机器人账号管理脚本

功能：
  - 创建机器人账号
  - 列出机器人账号及有效期
  - 轮换（删除旧账号 + 创建新账号）
  - 导出可用作 docker login 的凭证

用法:
  # 创建 CI 用机器人账号
  python3 robot_account.py create --project my-app --name ci-pipeline --actions push,pull

  # 列出所有机器人账号
  python3 robot_account.py list --project my-app

  # 轮换（删除重建）
  python3 robot_account.py rotate --project my-app --name ci-pipeline

  # 导出 docker login 命令
  python3 robot_account.py login-cmd --project my-app --name ci-pipeline --token-var HARBOR_TOKEN
"""

import argparse
import base64
import json
import os
import sys
import time
from dataclasses import dataclass
from typing import List, Dict, Optional

import requests


@dataclass
class RobotAccount:
    id: int
    name: str
    description: str
    project_id: int
    expires_at: int  # 0 = 永不过期
    created_at: str
    token: Optional[str] = None  # 仅创建时返回

    @property
    def is_expired(self) -> bool:
        if self.expires_at == 0:
            return False
        return self.expires_at < int(time.time())

    @property
    def days_until_expiry(self) -> Optional[int]:
        if self.expires_at == 0:
            return None
        return (self.expires_at - int(time.time())) // 86400

    @property
    def expires_at_str(self) -> str:
        if self.expires_at == 0:
            return "永不过期"
        from datetime import datetime
        return datetime.fromtimestamp(self.expires_at).strftime("%Y-%m-%d %H:%M")


ACTION_MAP = {
    "push": "/project/my-app/repository/push",
    "pull": "/project/my-app/repository/pull",
    "delete": "/project/my-app/repository/delete",
    "read": "/project/my-app/repository/read",
}

ACTION_NAMES = ["push", "pull"]  # 默认权限


def parse_args():
    parser = argparse.ArgumentParser(description="Harbor 机器人账号管理")
    sub = parser.add_subparsers(dest="cmd", required=True)

    create = sub.add_parser("create", help="创建机器人账号")
    create.add_argument("--url", required=True)
    create.add_argument("--auth", default=os.environ.get("HARBOR_AUTH", ""))
    create.add_argument("--project", required=True, help="项目名")
    create.add_argument("--name", required=True, help="机器人账号名")
    create.add_argument("--desc", default="", help="描述")
    create.add_argument("--actions", default="push,pull", help="权限，逗号分隔")
    create.add_argument("--expires-days", type=int, default=0,
                        help="过期天数（0=永不过期）")

    lst = sub.add_parser("list", help="列出机器人账号")
    lst.add_argument("--url", required=True)
    lst.add_argument("--auth", default=os.environ.get("HARBOR_AUTH", ""))
    lst.add_argument("--project", required=True)
    lst.add_argument("--show-token", action="store_true", help="显示 Token（谨慎）")

    rotate = sub.add_parser("rotate", help="轮换机器人账号（删重建）")
    rotate.add_argument("--url", required=True)
    rotate.add_argument("--auth", default=os.environ.get("HARBOR_AUTH", ""))
    rotate.add_argument("--project", required=True)
    rotate.add_argument("--name", required=True)
    rotate.add_argument("--desc", default="")
    rotate.add_argument("--actions", default="push,pull")
    rotate.add_argument("--expires-days", type=int, default=365)

    login_cmd = sub.add_parser("login-cmd", help="输出 docker login 命令")
    login_cmd.add_argument("--url", required=True)
    login_cmd.add_argument("--project", required=True)
    login_cmd.add_argument("--name", required=True)
    login_cmd.add_argument("--token-var", default="HARBOR_TOKEN",
                            help="Token 环境变量名")

    delete = sub.add_parser("delete", help="删除机器人账号")
    delete.add_argument("--url", required=True)
    delete.add_argument("--auth", default=os.environ.get("HARBOR_AUTH", ""))
    delete.add_argument("--project", required=True)
    delete.add_argument("--name", required=True)
    delete.add_argument("--robot-id", type=int, help="机器人 ID（可选，自动查找）")

    return parser.parse_args()


def get_auth_header(auth: str) -> Dict[str, str]:
    if ":" in auth:
        encoded = base64.b64encode(auth.encode()).decode()
        return {"Authorization": f"Basic {encoded}", "Content-Type": "application/json"}
    # 示例: admin:password -> base64 编码
    encoded = base64.b64encode(f"{username}:{password}".encode()).decode()
    return {"Authorization": f"Basic {encoded}", "Content-Type": "application/json"}


def get_project_id(url: str, project: str, headers: Dict) -> int:
    r = requests.get(f"{url}/api/v2.0/projects", params={"name": project},
                     headers=headers, timeout=15)
    r.raise_for_status()
    projs = r.json()
    if not projs:
        raise ValueError(f"项目不存在: {project}")
    return projs[0]["project_id"]


def list_robots(url: str, project_id: int, headers: Dict) -> List[RobotAccount]:
    r = requests.get(f"{url}/api/v2.0/projects/{project_id}/robotAccounts",
                     headers=headers, timeout=15)
    r.raise_for_status()
    return [RobotAccount(
        id=b["id"],
        name=b["name"],
        description=b.get("description", ""),
        project_id=b["project_id"],
        expires_at=b.get("expires_at", 0),
        created_at=b.get("creation_time", ""),
    ) for b in r.json()]


def find_robot(url: str, project_id: int, name: str, headers: Dict) -> Optional[RobotAccount]:
    bots = list_robots(url, project_id, headers)
    for bot in bots:
        # robot 名称格式为 robot$project$name
        if bot.name == f"robot${project_id}${name}" or bot.name.endswith(f"${name}"):
            return bot
    return None


def create_robot(url: str, project_id: int, name: str, actions: List[str],
                  expires_days: int, desc: str, headers: Dict) -> RobotAccount:
    expires_at = 0 if expires_days == 0 else int(time.time()) + expires_days * 86400

    access = []
    for action in actions:
        resource = f"/project/{project_id}/repository"
        if action == "push":
            access.append({"resource": resource, "action": "push"})
        elif action == "pull":
            access.append({"resource": resource, "action": "pull"})
        elif action == "delete":
            access.append({"resource": resource, "action": "delete"})
        elif action == "read":
            access.append({"resource": resource, "action": "read"})

    payload = {
        "name": name,
        "description": desc,
        "access": access,
        "expires_at": expires_at,
    }

    r = requests.post(f"{url}/api/v2.0/projects/{project_id}/robots",
                      headers=headers, json=payload, timeout=15)
    r.raise_for_status()
    data = r.json()

    return RobotAccount(
        id=data["id"],
        name=data["name"],
        description=desc,
        project_id=project_id,
        expires_at=expires_at,
        created_at=data.get("creation_time", ""),
        token=data.get("token", ""),
    )


def delete_robot(url: str, project_id: int, robot_id: int, headers: Dict):
    r = requests.delete(f"{url}/api/v2.0/projects/{project_id}/robotAccounts/{robot_id}",
                        headers=headers, timeout=15)
    r.raise_for_status()


def cmd_create(args):
    headers = get_auth_header(args.auth)
    project_id = get_project_id(args.url, args.project, headers)
    actions = [a.strip() for a in args.actions.split(",")]
    expires_days = args.expires_days

    bot = create_robot(args.url, project_id, args.name, actions, expires_days, args.desc, headers)

    print(f"✅ 机器人账号创建成功")
    print(f"   名称: {bot.name}")
    print(f"   ID: {bot.id}")
    print(f"   过期: {bot.expires_at_str}")
    if bot.token:
        print(f"\n   ⚠️  Token（仅显示一次）:")
        print(f"   {bot.token}")
    print(f"\n   Docker login 命令:")
    print(f"   docker login {args.url} -u \"{bot.name}\" -p \"$TOKEN\"")


def cmd_list(args):
    headers = get_auth_header(args.auth)
    project_id = get_project_id(args.url, args.project, headers)
    bots = list_robots(args.url, project_id, headers)

    if not bots:
        print("暂无机器人账号")
        return

    print(f"\n{'='*70}")
    print(f"  项目: {args.project}  机器人账号列表")
    print(f"{'='*70}")
    print(f"{'ID':<6} {'名称':<30} {'过期时间':<20} {'状态'}")
    print("-" * 70)
    for bot in bots:
        status = "✅ 有效" if not bot.is_expired else "❌ 已过期"
        if bot.days_until_expiry is not None and bot.days_until_expiry < 30:
            status = f"⚠️  {bot.days_until_expiry}天后过期"
        print(f"{bot.id:<6} {bot.name:<30} {bot.expires_at_str:<20} {status}")
    print("-" * 70)
    print(f"共 {len(bots)} 个\n")


def cmd_rotate(args):
    headers = get_auth_header(args.auth)
    project_id = get_project_id(args.url, args.project, headers)

    old_bot = find_robot(args.url, project_id, args.name, headers)
    if old_bot:
        print(f"删除旧账号 {old_bot.name} (ID: {old_bot.id})...")
        delete_robot(args.url, project_id, old_bot.id, headers)
        print("✅ 已删除")
    else:
        print(f"未找到现有账号 {args.name}，将直接创建")

    actions = [a.strip() for a in args.actions.split(",")]
    new_bot = create_robot(args.url, project_id, args.name, actions,
                            args.expires_days, args.desc, headers)

    print(f"\n✅ 新机器人账号创建成功")
    print(f"   名称: {new_bot.name}")
    print(f"   过期: {new_bot.expires_at_str}")
    if new_bot.token:
        print(f"\n   ⚠️  Token（仅显示一次）:")
        print(f"   {new_bot.token}")


def cmd_delete(args):
    headers = get_auth_header(args.auth)
    project_id = get_project_id(args.url, args.project, headers)

    if args.robot_id:
        robot_id = args.robot_id
    else:
        bot = find_robot(args.url, project_id, args.name, headers)
        if not bot:
            print(f"未找到机器人账号: {args.name}")
            sys.exit(1)
        robot_id = bot.id

    confirm = input(f"确认删除机器人账号 ID={robot_id}？(y/N): ")
    if confirm.lower() == "y":
        delete_robot(args.url, project_id, robot_id, headers)
        print("✅ 已删除")
    else:
        print("已取消")


def cmd_login_cmd(args):
    # 只需要输出命令格式，不需要真实 token
    full_name = f"robot${args.project}${args.name}"
    print(f"# Docker login 命令（请先设置 $ROBOT_SECRET 环境变量）")
    print(f'docker login {args.url} -u "{full_name}" -p "$ROBOT_SECRET"')


if __name__ == "__main__":
    args = parse_args()
    if not args.auth and "HARBOR_AUTH" not in os.environ:
        print("错误：请通过 --auth 或 HARBOR_AUTH 环境变量提供认证信息", file=sys.stderr)
        sys.exit(1)

    if args.cmd == "create":
        cmd_create(args)
    elif args.cmd == "list":
        cmd_list(args)
    elif args.cmd == "rotate":
        cmd_rotate(args)
    elif args.cmd == "delete":
        cmd_delete(args)
    elif args.cmd == "login-cmd":
        cmd_login_cmd(args)

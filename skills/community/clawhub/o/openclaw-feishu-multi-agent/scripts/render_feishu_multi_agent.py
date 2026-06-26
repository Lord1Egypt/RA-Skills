#!/usr/bin/env python3
"""Render reusable OpenClaw + Feishu multi-agent artifacts from a roles file."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

from common import find_coordinator, is_placeholder, load_roles, role_agent_dir, role_workspace


def role_line(role: dict[str, Any]) -> str:
    trigger_terms = " / ".join(role["triggerTerms"])
    return (
        f"| {role['roleName']} | `{role['agentId']}` | `{role['accountId']}` | "
        f"`{role['openId']}` | {trigger_terms} |"
    )


def render_protocol(system_name: str, roles: list[dict[str, Any]]) -> str:
    coordinator = next(role for role in roles if role["isCoordinator"])
    specialists = [role for role in roles if not role["isCoordinator"]]
    broad_team = "\n".join(f"- `{r['agentId']}` / {r['roleName']}" for r in specialists)
    roster = "\n".join(
        [
            "| 角色名 | Agent ID | AccountId | Open ID | 触发词 |",
            "|---|---|---|---|---|",
            *[role_line(role) for role in roles],
        ]
    )
    return f"""# PROTOCOL.md - {system_name}

**所有 agent 在首次加载时必须读取此文件。**

## 飞书通信协议

飞书不会把 bot 消息传递给其他 bot，必须通过 `sessions_send` 直接联系。

### 总原则

飞书里的 `<at>` 只有“给人看”的作用，OpenClaw 里的 `sessions_send` 才有“唤醒另一个 agent” 的作用。

所以，只要一个 agent 想让另一个 agent 在群里发言，必须同时做两件事：

1. 在飞书群里发一条带 `<at>` 标签的消息
2. 立刻用 `sessions_send` 把同样的任务投递给目标 agent

### 默认总调度

默认协调者是 `{coordinator['agentId']}` / {coordinator['roleName']}。

- 群里出现一个新问题时，协调者先判断：
  - 自己直接答
  - 交给一个 agent
  - 同时拉多个 agent
- 只要需要别人参与，就必须显式地 `<at>` 对方，并用 `sessions_send` 实际通知对方
- 不等待回执，可以继续给出 framing、判断或追问

### 广义团队召集的默认解释

如果用户说的是“其他人”“大家”“团队”“一起讨论”这类没有限定职能范围的话，默认按完整团队会诊处理：

{broad_team}

### 委派步骤

1. 从当前 session key 提取群组 ID（`oc_xxx`）
2. 构造目标 session key：`agent:{{targetAgentId}}:feishu:group:oc_xxx`
3. 在飞书群消息中使用 `<at>` 标签点名目标 agent
4. 再调用 `sessions_send`
5. 要求对方直接用 `message` 工具回复到：
   - `target: chat:oc_xxx`
   - `accountId: {{targetAccountId}}`

### 收到 sessions_send 时

直接回群，不回复发起者。

如需继续拉另一个 agent：

1. 先在群里 `<at>`
2. 再发 `sessions_send`

### 绝对禁止

- 不要把裸文本 `@角色` 当成 bot 通知机制
- 不要只发 `<at>` 而不发 `sessions_send`
- 不要给 `sessions_send` 传 `agentId`

### Agent 通讯录

{roster}
"""


def render_identity(role: dict[str, Any], coordinator_name: str) -> str:
    trigger_text = "、".join(role["triggerTerms"])
    if role["isCoordinator"]:
        extra = """
## 飞书群协作

你是默认总调度。群里出现一个新问题时，先判断：

1. 这件事值不值得做
2. 该由谁主答
3. 是否需要多人并行讨论

只要需要别人参与，就必须同时做两步：

1. 在群里用飞书 `<at>` 显式点名
2. 对目标 agent 调用 `sessions_send`

绝对禁止：

- 只发裸文本 `@角色`
- 只发 `<at>` 不发 `sessions_send`
- 给 `sessions_send` 传 `agentId`
"""
    else:
        extra = f"""
## 飞书群协作

如果 {coordinator_name} 或其他 agent 通过 `sessions_send` 把你拉进群聊，你要直接用 `message` 回复飞书群，而不是回复发起者。

如果你的判断需要另一个 agent 补位，也必须同时做：

1. 在群里用 `<at>` 显式点名
2. 用 `sessions_send` 实际通知对方
"""
    return f"""# IDENTITY.md - {role['roleName']}

## 我是谁

我是 **{role['roleName']}**。

## 我的职责

{role['responsibility']}

## 触发词

{trigger_text}
{extra}
"""


def render_openclaw_snippet(roles: list[dict[str, Any]], state_dir: Path) -> str:
    allow = [role["agentId"] for role in roles]
    agent_list = [
        {
            "id": role["agentId"],
            "workspace": str(role_workspace(role, state_dir)),
            "agentDir": str(role_agent_dir(role, state_dir)),
        }
        for role in roles
    ]
    bindings = [
        {
            "agentId": role["agentId"],
            "match": {"channel": "feishu", "accountId": role["accountId"]},
        }
        for role in roles
    ]
    accounts = {
        role["accountId"]: {
            "name": role["roleName"],
            "appId": role.get("appId") if not is_placeholder(role.get("appId")) else "replace_me",
            "appSecret": role.get("appSecret") if not is_placeholder(role.get("appSecret")) else "replace_me",
        }
        for role in roles
    }
    return json.dumps(
        {
            "agents": {"list": agent_list},
            "tools": {
                "sessions": {"visibility": "all"},
                "agentToAgent": {"enabled": True, "allow": allow},
            },
            "bindings": bindings,
            "channels": {"feishu": {"accounts": accounts}},
        },
        ensure_ascii=False,
        indent=2,
    )


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--roles", required=True, help="Path to roles.json")
    parser.add_argument("--output-dir", required=True, help="Directory to write generated artifacts")
    parser.add_argument(
        "--state-dir",
        default="~/.openclaw",
        help="OpenClaw state dir used to compute default agent directories",
    )
    args = parser.parse_args(argv)

    roles_path = Path(args.roles).expanduser().resolve()
    output_dir = Path(args.output_dir).expanduser().resolve()
    state_dir = Path(args.state_dir).expanduser().resolve()
    output_dir.mkdir(parents=True, exist_ok=True)
    identities_dir = output_dir / "identities"
    identities_dir.mkdir(exist_ok=True)

    system_name, roles = load_roles(roles_path)
    coordinator = find_coordinator(roles)

    (output_dir / "PROTOCOL.generated.md").write_text(
        render_protocol(system_name, roles), encoding="utf-8"
    )
    (output_dir / "openclaw.generated.json").write_text(
        render_openclaw_snippet(roles, state_dir), encoding="utf-8"
    )
    (output_dir / "roles.generated.json").write_text(
        json.dumps({"systemName": system_name, "roles": roles}, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    for role in roles:
        target = identities_dir / f"{role['agentId']}.IDENTITY.generated.md"
        target.write_text(render_identity(role, coordinator["roleName"]), encoding="utf-8")

    print(f"Rendered artifacts to: {output_dir}")
    print(f"- PROTOCOL.generated.md")
    print(f"- openclaw.generated.json")
    print(f"- roles.generated.json")
    print(f"- identities/*.IDENTITY.generated.md")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

#!/usr/bin/env python3
"""
register_agent.py — 安全修改 openclaw.json，注册新 Agent

用法：
  python3 register_agent.py \
    --agent-id staff-ou_xxx \
    --workspace ~/.openclaw/agency-agents/staff-ou_xxx \
    --parent-id main \
    --agent-type human \
    --core-duty "负责XX客户的抖音文案撰写" \
    --also-allow feishu_get_user feishu_im_user_message ...

可选参数：
  --model              Agent 使用的模型（不传则继承默认）
  --heartbeat-interval 心跳间隔分钟数（默认 60）
  --agent-dir          agentDir 路径（极少数情况才需要）
  --dry-run            预览变更，不写入

特性：
  - 注册前自动备份（带时间戳）
  - 双向绑定：agents.list + 父 Agent 的 allowAgents
  - 注册后执行 openclaw config validate
  - validate 失败自动回滚
  - 注册成功后自动在父 Agent MEMORY.md 追加子 Agent 档案
"""

import argparse
import json
import os
import shutil
import subprocess
import sys
from datetime import datetime
from pathlib import Path

OPENCLAW_JSON = Path.home() / ".openclaw" / "openclaw.json"
AGENCY_BASE = Path.home() / ".openclaw" / "agency-agents"


def normalize_heartbeat(interval_minutes):
    """将分钟数转换为 OpenClaw 标准的 heartbeat.every 格式"""
    if interval_minutes >= 60 and interval_minutes % 60 == 0:
        return f"{interval_minutes // 60}h"
    else:
        return f"{interval_minutes}m"


def load_config():
    with open(OPENCLAW_JSON, "r", encoding="utf-8") as f:
        return json.load(f)


def save_config(config):
    with open(OPENCLAW_JSON, "w", encoding="utf-8") as f:
        json.dump(config, f, indent=2, ensure_ascii=False)
        f.write("\n")


def backup_config():
    ts = datetime.now().strftime("%Y%m%d-%H%M%S")
    backup_path = str(OPENCLAW_JSON) + f".bak.{ts}"
    shutil.copy2(OPENCLAW_JSON, backup_path)
    print(f"✅ 已备份：{backup_path}")
    return backup_path


def rollback(backup_path):
    shutil.copy2(backup_path, OPENCLAW_JSON)
    print(f"🔄 已回滚至：{backup_path}")


def validate_config():
    result = subprocess.run(
        ["openclaw", "config", "validate"],
        capture_output=True,
        text=True
    )
    return result.returncode == 0, result.stdout + result.stderr


def append_to_parent_memory(parent_id: str, agent_id: str, agent_type: str,
                             core_duty: str, also_allow: list, dry_run: bool):
    """
    在父 Agent 的 MEMORY.md 里追加子 Agent 档案。
    父 Agent workspace 路径从 openclaw.json 里的 agents.list 读取。
    """
    config = load_config()
    agents_list = config.get("agents", {}).get("list", [])
    parent = next((a for a in agents_list if a.get("id") == parent_id), None)

    if not parent:
        print(f"  ⚠️  找不到父 Agent '{parent_id}' 的 workspace，跳过 MEMORY.md 预埋")
        return

    parent_workspace = Path(parent.get("workspace", "")).expanduser()
    memory_path = parent_workspace / "MEMORY.md"

    if not memory_path.exists():
        print(f"  ⚠️  父 Agent MEMORY.md 不存在：{memory_path}，跳过预埋")
        return

    # 幂等检查：已有该 agentId 的档案则更新，否则追加
    existing_content = memory_path.read_text(encoding="utf-8")
    already_exists = f"## 子 Agent：{agent_id}" in existing_content

    today = datetime.now().strftime("%Y-%m-%d")
    type_label = "人伴型（员工型）" if agent_type == "human" else "功能型（任务型）"
    tools_str = "、".join(also_allow) if also_allow else "（无额外工具）"

    entry = f"""## 子 Agent：{agent_id}（创建于 {today}）
- 类型：{type_label}
- 核心职责：{core_duty or "（未指定，请手动补充）"}
- 工具权限：{tools_str}
- workspace：~/.openclaw/agency-agents/{agent_id}
"""

    if dry_run:
        action = "更新" if already_exists else "追加"
        print(f"\n  [DRY-RUN] 将在父 Agent MEMORY.md {action}：")
        print("  " + entry.replace("\n", "\n  "))
        return

    if already_exists:
        # 替换已有档案块（从标题行到下一个 ## 或文件尾）
        # 保留档案块后面的 \n\n 分隔，避免吃掉下一个段落前的空行
        import re
        pattern = rf"## 子 Agent：{re.escape(agent_id)}.*?(?=\n## |\Z)"
        new_content = re.sub(pattern, entry.rstrip() + "\n", existing_content, flags=re.DOTALL)
        memory_path.write_text(new_content, encoding="utf-8")
        print(f"  ✅ 已更新父 Agent MEMORY.md 中的子 Agent 档案：{memory_path}")
    else:
        with open(memory_path, "a", encoding="utf-8") as f:
            f.write("\n" + entry)
        print(f"  ✅ 已在父 Agent MEMORY.md 追加子 Agent 档案：{memory_path}")


def main():
    parser = argparse.ArgumentParser(description="注册新 Agent 到 openclaw.json")
    parser.add_argument("--agent-id", required=True, help="新 Agent 的 ID")
    parser.add_argument("--workspace", required=True, help="workspace 路径")
    parser.add_argument("--parent-id", required=True, help="父 Agent 的 ID")
    parser.add_argument("--agent-type", choices=["human", "functional"],
                        default="human", help="Agent 类型（human / functional，默认 human）")
    parser.add_argument("--core-duty", default="", help="核心职责描述（用于父 MEMORY.md 预埋）")
    parser.add_argument("--also-allow", nargs="*", default=[], help="工具权限列表")
    parser.add_argument("--model", default="", help="模型名称（不传则继承默认）")
    parser.add_argument("--heartbeat-interval", type=int, default=60,
                        help="心跳间隔（分钟，默认 60）")
    parser.add_argument("--agent-dir", help="agentDir 路径（可选，绝大多数情况不需要）")
    parser.add_argument("--dry-run", action="store_true",
                        help="预览将要对 openclaw.json 做的修改，不实际写入")
    args = parser.parse_args()

    agent_id = args.agent_id
    workspace = str(Path(args.workspace).expanduser())
    parent_id = args.parent_id
    agent_type = args.agent_type
    core_duty = args.core_duty
    also_allow = args.also_allow
    model = args.model
    heartbeat_interval = args.heartbeat_interval
    agent_dir = args.agent_dir
    dry_run = args.dry_run

    print(f"\n=== {'[DRY-RUN] ' if dry_run else ''}注册 Agent: {agent_id} ===")
    if dry_run:
        print("  ⚠️  DRY-RUN 模式：只预览变更，不写入任何文件")
    print(f"  类型:       {agent_type}")
    print(f"  workspace:  {workspace}")
    print(f"  agentDir:   {agent_dir or '(不写入)'}")
    print(f"  父 Agent:   {parent_id}")
    print(f"  工具权限:   {also_allow or '(无)'}")
    print(f"  模型:       {model or '(继承默认)'}")
    normalized_hb = normalize_heartbeat(heartbeat_interval) if heartbeat_interval else '(无)'
    print(f"  心跳间隔:   {heartbeat_interval} 分钟 → {normalized_hb}")
    print()

    backup_path = None
    if not dry_run:
        backup_path = backup_config()

    try:
        config = load_config()
        agents_section = config.get("agents", {})
        agents_list = agents_section.get("list", [])

        # 检查是否已存在
        existing = next((a for a in agents_list if a.get("id") == agent_id), None)
        if existing:
            print(f"⚠️  Agent '{agent_id}' 已存在，将覆盖其定义。")

        # 构建新 Agent 定义
        new_agent = {
            "id": agent_id,
            "workspace": workspace,
        }
        if agent_dir:
            new_agent["agentDir"] = agent_dir
        if also_allow:
            new_agent["tools"] = {"alsoAllow": also_allow}
        if model:
            new_agent["model"] = model

        # heartbeat 配置（功能型 Agent 也需要，用于进化机制和闲置检查）
        # 正确格式为 heartbeat.every，值为字符串如 "1h"，不使用 interval
        if heartbeat_interval and heartbeat_interval > 0:
            normalized = normalize_heartbeat(heartbeat_interval)
            new_agent["heartbeat"] = {
                "every": normalized
            }

        # 写入 agents.list
        if existing:
            idx = next(i for i, a in enumerate(agents_list) if a.get("id") == agent_id)
            agents_list[idx] = new_agent
        else:
            agents_list.append(new_agent)

        agents_section["list"] = agents_list
        config["agents"] = agents_section

        # 双向绑定：在父 Agent 的 allowAgents 里追加
        parent = next((a for a in agents_list if a.get("id") == parent_id), None)
        if parent is None:
            print(f"❌ 找不到父 Agent '{parent_id}'，请检查 agent id 是否正确")
            if backup_path:
                rollback(backup_path)
            sys.exit(1)

        subagents_config = parent.setdefault("subagents", {})
        allow_agents = subagents_config.get("allowAgents", [])
        if agent_id not in allow_agents:
            allow_agents.append(agent_id)
            subagents_config["allowAgents"] = allow_agents
            print(f"✅ 已将 '{agent_id}' 加入 '{parent_id}' 的 allowAgents")
        else:
            print(f"ℹ️  '{agent_id}' 已在 '{parent_id}' 的 allowAgents 中")

        # 写入或 dry-run 预览
        if dry_run:
            original = load_config()
            print("\n=== [DRY-RUN] 变更预览 ===")
            orig_agents = [a.get("id") for a in original.get("agents", {}).get("list", [])]
            new_agents = [a.get("id") for a in agents_list]
            added = [i for i in new_agents if i not in orig_agents]
            updated = [i for i in new_agents if i in orig_agents and
                       next((a for a in original["agents"]["list"] if a["id"] == i), {}) !=
                       next((a for a in agents_list if a["id"] == i), {})]
            if added:
                print(f"  + agents.list 新增：{added}")
            if updated:
                print(f"  ~ agents.list 覆盖：{updated}")

            orig_parent = next((a for a in original.get("agents", {}).get("list", [])
                                if a.get("id") == parent_id), {})
            orig_allow = orig_parent.get("subagents", {}).get("allowAgents", [])
            if agent_id not in orig_allow:
                print(f"  + {parent_id}.subagents.allowAgents 新增：{agent_id}")

            print(f"  + heartbeat.every: {heartbeat_interval}m")
            if model:
                print(f"  + model: {model}")

            # 预览父 MEMORY.md 追加内容
            append_to_parent_memory(parent_id, agent_id, agent_type, core_duty, also_allow, dry_run=True)

            print("\n⚠️  DRY-RUN 完成，未写入任何文件。去掉 --dry-run 后执行实际注册。")
            return
        else:
            save_config(config)
            print("✅ openclaw.json 已更新")

        # validate
        print("\n=== 执行 openclaw config validate ===")
        ok, output = validate_config()
        if ok:
            print("✅ validate 通过")
        else:
            print("❌ validate 失败，自动回滚")
            print(output)
            rollback(backup_path)
            print("\n📋 诊断建议：")
            print(f"  1. 查看备份与当前配置的差异：diff {backup_path} {OPENCLAW_JSON}")
            print(f"  2. 查看当前 agents 配置：openclaw config get agents")
            sys.exit(1)

        # 注册成功后：在父 Agent MEMORY.md 追加子 Agent 档案
        print("\n=== 更新父 Agent MEMORY.md ===")
        append_to_parent_memory(parent_id, agent_id, agent_type, core_duty, also_allow, dry_run=False)

    except Exception as e:
        print(f"❌ 发生错误：{e}")
        if backup_path:
            rollback(backup_path)
        sys.exit(1)

    print(f"\n✅ Agent '{agent_id}' 注册完成")
    print("下一步：验证 workspace 完整性后重启 Gateway")
    print(f"  bash scripts/verify_workspace.sh {agent_id} --type {agent_type}")
    print("  systemctl --user restart openclaw-gateway.service")
    print("  sleep 8  # 等待工具注册完成")


if __name__ == "__main__":
    main()

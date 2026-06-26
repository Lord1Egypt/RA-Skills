#!/usr/bin/env python3
"""
deregister_agent.py — 安全注销 Agent，register_agent.py 的反向操作

用法：
  python3 deregister_agent.py --agent-id staff-ou_xxx
  python3 deregister_agent.py --agent-id staff-ou_xxx --dry-run

操作步骤：
  1. 备份 openclaw.json（带时间戳）
  2. 从 agents.list 移除目标 Agent
  3. 从所有父 Agent 的 allowAgents 移除目标 Agent id
  4. openclaw config validate
  5. validate 通过 → 存档 workspace → 完成
     validate 失败 → 自动回滚

workspace 处理：
  - 不直接删除，存档到 ~/.openclaw/agency-agents/.archived/<agentId>-<timestamp>/
  - 需要彻底清除时，手动删除 .archived/ 下对应目录
"""

import argparse
import json
import shutil
import subprocess
import sys
from datetime import datetime
from pathlib import Path

OPENCLAW_JSON = Path.home() / ".openclaw" / "openclaw.json"
AGENCY_BASE = Path.home() / ".openclaw" / "agency-agents"
ARCHIVE_BASE = AGENCY_BASE / ".archived"


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


def archive_workspace(workspace_path: Path, agent_id: str, dry_run: bool) -> Path | None:
    """将 workspace 移动到 .archived/ 目录，不删除。"""
    if not workspace_path.exists():
        print(f"  ℹ️  workspace 不存在，跳过存档：{workspace_path}")
        return None

    ts = datetime.now().strftime("%Y%m%d-%H%M%S")
    archive_dir = ARCHIVE_BASE / f"{agent_id}-{ts}"

    if dry_run:
        print(f"  [DRY-RUN] 将存档 workspace：{workspace_path} → {archive_dir}")
        return archive_dir

    ARCHIVE_BASE.mkdir(parents=True, exist_ok=True)
    shutil.move(str(workspace_path), str(archive_dir))
    print(f"  ✅ workspace 已存档：{archive_dir}")
    print(f"  ℹ️  如需彻底清除，手动执行：rm -rf {archive_dir}")
    return archive_dir


def main():
    parser = argparse.ArgumentParser(description="注销 Agent，从 openclaw.json 移除并存档 workspace")
    parser.add_argument("--agent-id", required=True, help="要注销的 Agent ID")
    parser.add_argument("--dry-run", action="store_true",
                        help="预览变更，不实际写入")
    args = parser.parse_args()

    agent_id = args.agent_id
    dry_run = args.dry_run

    print(f"\n=== {'[DRY-RUN] ' if dry_run else ''}注销 Agent: {agent_id} ===")
    if dry_run:
        print("  ⚠️  DRY-RUN 模式：只预览，不写入任何文件")
    print()

    config = load_config()
    agents_section = config.get("agents", {})
    agents_list = agents_section.get("list", [])

    # 检查目标 Agent 是否存在
    target = next((a for a in agents_list if a.get("id") == agent_id), None)
    if not target:
        print(f"❌ 找不到 Agent '{agent_id}'，已注销或不存在")
        sys.exit(1)

    workspace_path = Path(target.get("workspace", "")).expanduser()
    print(f"  workspace:  {workspace_path}")

    # 找出所有引用了该 Agent 的父 Agent
    parents_with_ref = []
    for agent in agents_list:
        allow = agent.get("subagents", {}).get("allowAgents", [])
        if agent_id in allow:
            parents_with_ref.append(agent.get("id"))

    if parents_with_ref:
        print(f"  被引用于:   {parents_with_ref} 的 allowAgents")
    else:
        print(f"  被引用于:   （无父 Agent 引用）")
    print()

    if dry_run:
        print("=== [DRY-RUN] 变更预览 ===")
        print(f"  - agents.list 移除：{agent_id}")
        for pid in parents_with_ref:
            print(f"  - {pid}.subagents.allowAgents 移除：{agent_id}")
        archive_workspace(workspace_path, agent_id, dry_run=True)

        # 预览 MEMORY.md 清理
        print("\n=== [DRY-RUN] MEMORY.md 清理预览 ===")
        memory_previewed = False
        for agent in new_agents_list:
            parent_ws = Path(agent.get("workspace", "")).expanduser()
            memory_path = parent_ws / "MEMORY.md"
            if not memory_path.exists():
                continue
            content = memory_path.read_text(encoding="utf-8")
            if f"## 子 Agent：{agent_id}" in content:
                print(f"  - 将从 {agent.get('id')} 的 MEMORY.md 移除子 Agent 档案：{memory_path}")
                memory_previewed = True
        if not memory_previewed:
            print("  ℹ️  未在父 Agent MEMORY.md 中找到子 Agent 档案")

        print("\n⚠️  DRY-RUN 完成，未写入任何文件。去掉 --dry-run 后执行实际注销。")
        return

    # 确认操作
    print(f"⚠️  即将注销 Agent '{agent_id}'，此操作不可撤销（workspace 将存档，不删除）。")
    confirm = input("确认继续？(y/N) ")
    if confirm.lower() != "y":
        print("已取消")
        sys.exit(0)

    backup_path = backup_config()

    try:
        # Step 1: 从 agents.list 移除
        new_agents_list = [a for a in agents_list if a.get("id") != agent_id]
        agents_section["list"] = new_agents_list
        config["agents"] = agents_section
        print(f"✅ 已从 agents.list 移除：{agent_id}")

        # Step 2: 从所有父 Agent 的 allowAgents 移除
        for agent in new_agents_list:
            allow = agent.get("subagents", {}).get("allowAgents", [])
            if agent_id in allow:
                allow.remove(agent_id)
                agent["subagents"]["allowAgents"] = allow
                print(f"✅ 已从 {agent.get('id')} 的 allowAgents 移除：{agent_id}")

        # Step 3: 写入
        save_config(config)
        print("✅ openclaw.json 已更新")

        # Step 4: validate
        print("\n=== 执行 openclaw config validate ===")
        ok, output = validate_config()
        if ok:
            print("✅ validate 通过")
        else:
            print("❌ validate 失败，自动回滚")
            print(output)
            rollback(backup_path)
            sys.exit(1)

        # Step 5: 存档 workspace
        print("\n=== 存档 workspace ===")
        archive_workspace(workspace_path, agent_id, dry_run=False)

        # Step 6: 清理父 Agent MEMORY.md 中的子 Agent 档案
        print("\n=== 清理父 Agent MEMORY.md ===")
        cleaned = False
        for agent in new_agents_list:
            parent_ws = Path(agent.get("workspace", "")).expanduser()
            memory_path = parent_ws / "MEMORY.md"
            if not memory_path.exists():
                continue
            content = memory_path.read_text(encoding="utf-8")
            if f"## 子 Agent：{agent_id}" not in content:
                continue
            import re
            pattern = rf"## 子 Agent：{re.escape(agent_id)}.*?(?=\n## |\Z)"
            new_content = re.sub(pattern, "", content, flags=re.DOTALL)
            new_content = re.sub(r'\n{3,}', '\n\n', new_content)
            memory_path.write_text(new_content, encoding="utf-8")
            print(f"  ✅ 已从 {agent.get('id')} 的 MEMORY.md 移除子 Agent 档案：{memory_path}")
            cleaned = True
        if not cleaned:
            print("  ℹ️  未在父 Agent MEMORY.md 中找到子 Agent 档案，跳过")

    except Exception as e:
        print(f"❌ 发生错误：{e}")
        rollback(backup_path)
        sys.exit(1)

    print(f"\n✅ Agent '{agent_id}' 注销完成")
    print("建议：重启 Gateway 使变更生效")
    print("  systemctl --user restart openclaw-gateway.service")


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""
Memory-Inhabit Cleanup — 技能卸载清理器

用法：
  python3 cleanup.py uninstall    清除本技能创建的 cron 任务和状态文件
  python3 cleanup.py verify       验证当前 cron 任务状态（不修改）
"""

import json
import sys
import subprocess
import shutil
import os
from pathlib import Path

SKILL_DIR = Path(__file__).parent.parent

# 多路径探测 openclaw，避免 hardcoded 路径
def find_openclaw():
    """尝试多种路径找到 openclaw CLI"""
    candidates = [
        Path.home() / ".nvm/versions/node/v22.22.2/bin/openclaw",
        Path.home() / ".nvm/versions/node/v20.18.3/bin/openclaw",
        Path("/usr/local/bin/openclaw"),
        Path("/usr/bin/openclaw"),
        Path.home() / ".local/bin/openclaw",
    ]
    # 先尝试 PATH 中的
    try:
        result = subprocess.run(
            ["which", "openclaw"], capture_output=True, text=True, timeout=5
        )
        if result.returncode == 0 and result.stdout.strip():
            return Path(result.stdout.strip())
    except Exception:
        pass
    # 再试候选路径
    for p in candidates:
        if p.exists():
            return p
    return candidates[0]  # fallback，即使不存在也不报错

OPENCLAW = find_openclaw()

# 本技能生成的状态文件
STATE_FILES = [
    ".mi_state.json",
    ".mi_stats.json",
]

# 本技能生成的记忆文件（可选清理）
MEMORY_PATTERNS = [
    "personas/*/memories/history/*.md",
]

# 本技能的 cron 任务名称
CRON_JOB_NAMES = [
    "mi-companion-proactive",
]


def get_cron_jobs():
    """获取当前所有 cron 任务"""
    try:
        result = subprocess.run(
            [str(OPENCLAW), "cron", "list", "--json"],
            capture_output=True, text=True, timeout=15
        )
        if result.returncode != 0:
            return []
        
        # JSON 输出可能混有多个 JSON 对象，逐个解码取最后一个
        raw = result.stdout
        decoder = json.JSONDecoder()
        pos = 0
        last_data = None
        while pos < len(raw):
            try:
                obj, end = decoder.raw_decode(raw, pos)
                last_data = obj
                pos = end
            except json.JSONDecodeError:
                pos += 1
        
        if last_data:
            return last_data.get("jobs", last_data.get("items", []))
        return []
    except Exception as e:
        print(f"⚠️ 获取 cron 列表失败: {e}")
        return []


def remove_cron_job(name):
    """删除本技能创建的指定 cron 任务（仅删除 skill 自身创建的任务）"""
    try:
        result = subprocess.run(
            [str(OPENCLAW), "cron", "rm", name],
            capture_output=True, text=True, timeout=15
        )
        if result.returncode == 0:
            print(f"  ✅ 已删除 cron 任务: {name}")
            return True
        else:
            # 可能已经不存在
            if "not found" in result.stderr.lower() or "不存在" in result.stderr:
                print(f"  ℹ️ cron 任务不存在（已清理）: {name}")
                return True
            print(f"  ⚠️ 删除失败: {name} — {result.stderr.strip()}")
            return False
    except Exception as e:
        print(f"  ⚠️ 删除异常: {name} — {e}")
        return False


def clean_state_files():
    """清理本技能自身生成的状态文件（仅清理 SKILL_DIR 下的文件）"""
    cleaned = 0
    for fname in STATE_FILES:
        fpath = SKILL_DIR / fname
        if fpath.exists():
            fpath.unlink()
            print(f"  ✅ 已删除: {fname}")
            cleaned += 1
    if cleaned == 0:
        print(f"  ℹ️ 无状态文件需要清理")


def verify():
    """验证当前状态"""
    print("🔍 Memory-Inhabit 状态检查\n")
    
    # 检查 cron 任务
    print("Cron 任务：")
    jobs = get_cron_jobs()
    skill_jobs = [j for j in jobs if j.get("name") in CRON_JOB_NAMES]
    
    if skill_jobs:
        for job in skill_jobs:
            status = "启用" if job.get("enabled") else "禁用"
            print(f"  📌 {job['name']} [{status}]")
            schedule = job.get("schedule", {})
            if schedule.get("kind") == "cron":
                print(f"     cron: {schedule.get('expr')} tz={schedule.get('tz')}")
    else:
        print("  ℹ️ 无本技能创建的 cron 任务")
    
    # 检查状态文件
    print("\n状态文件：")
    for fname in STATE_FILES:
        fpath = SKILL_DIR / fname
        if fpath.exists():
            with open(fpath) as f:
                data = json.load(f)
            print(f"  📄 {fname} — 存在")
            if "active_persona" in data:
                print(f"     人格: {data.get('profile_name')} 模式: {data.get('mode')}")
        else:
            print(f"  ℹ️ {fname} — 不存在")


def uninstall():
    """完整卸载清理"""
    print("🧹 Memory-Inhabit 卸载清理\n")
    
    # 1. 清除 cron 任务
    print("1. 清除 cron 任务：")
    jobs = get_cron_jobs()
    skill_job_names = {j.get("name") for j in jobs}
    
    removed = 0
    for name in CRON_JOB_NAMES:
        if name in skill_job_names:
            if remove_cron_job(name):
                removed += 1
        else:
            print(f"  ℹ️ cron 任务不存在: {name}")
    
    # 2. 清理状态文件
    print("\n2. 清理状态文件：")
    clean_state_files()
    
    # 3. 清理对话历史（可选）
    print("\n3. 清理对话历史：")
    import glob
    history_files = glob.glob(str(SKILL_DIR / "personas" / "*" / "memories" / "history" / "*.md"))
    if history_files:
        print(f"  找到 {len(history_files)} 个历史文件")
        for hf in history_files:
            Path(hf).unlink()
            print(f"  ✅ 已删除: {Path(hf).relative_to(SKILL_DIR)}")
    else:
        print(f"  ℹ️ 无对话历史文件")
    
    # 3. 总结
    print(f"\n✅ 清理完成")
    print(f"   删除 cron 任务: {removed} 个")
    print(f"   其他 cron 任务未受影响")


def main():
    if len(sys.argv) < 2:
        print("Memory-Inhabit Cleanup — 技能卸载清理器")
        print()
        print("用法：")
        print("  python3 cleanup.py uninstall    清除本技能的 cron 和状态")
        print("  python3 cleanup.py verify       检查当前状态")
        sys.exit(0)
    
    cmd = sys.argv[1]
    if cmd == "uninstall":
        uninstall()
    elif cmd == "verify":
        verify()
    else:
        print(f"未知命令: {cmd}")
        sys.exit(1)


if __name__ == "__main__":
    main()

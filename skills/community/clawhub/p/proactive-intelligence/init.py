# -*- coding: utf-8 -*-
"""Proactive Intelligence - 完整初始化脚本 v2.3.0"""

import os
import sys
import re
from pathlib import Path

sys.stdout.reconfigure(encoding='utf-8')

BASE_DIR = Path.home() / "proactive-intelligence"
WORKSPACE = Path.home() / ".openclaw" / "workspace"

print("[INIT] Proactive Intelligence v2.3.0 初始化...")

# === 1. 创建数据目录 ===
print("[DIR] 创建数据目录...")
for subdir in ["domains", "projects", "archive"]:
    (BASE_DIR / subdir).mkdir(parents=True, exist_ok=True)

# === 2. 创建核心文件 ===
files = {
    "memory.md": """# 核心记忆 (HOT)

## 工作风格
- 主动预测，不等指令
- 从纠正中学习，持续改进
- 保持动量，不因沉默而停滞

## 技能管理
- 装技能后必须读 SKILL.md 并执行初始化
- 涉及路径的技能要立即统一所有 .md 引用

## 交易规则
- 只做 A 股主板
- 不碰 ST、不碰退市风险股
- 严格止损：单笔亏损不超过总资金 2.5%
- 仓位管理：单只股 ≤ 3 成仓，永远不满仓

## 记忆触发点
- 纠正 → 立即记录到 corrections.md
- 重复 3 次 → 考虑升级为规则
- 每周回顾 → 清理过期信息
""",
    "corrections.md": """# 纠正记录

## 格式
每次用户纠正时，添加：
```
[日期] 问题描述 → 正确做法
```
""",
    "session-state.md": """# 会话状态

当前目标: 
最后决策: 
下一步: 
""",
    "patterns.md": """# 可复用模式

格式：模式名称 | 使用场景 | 成功次数 | 最后使用
""",
}

for name, content in files.items():
    filepath = BASE_DIR / name
    if not filepath.exists():
        print(f"[FILE] 创建 {name}...")
        filepath.write_text(content, encoding='utf-8')
    else:
        print(f"[SKIP] {name} 已存在")

# === 3. 创建 .learnings 结构化日志 ===
print("[DIR] 创建 .learnings 结构化日志...")
learnings_dir = WORKSPACE / ".learnings"
learnings_dir.mkdir(parents=True, exist_ok=True)

learnings_files = {
    "LEARNINGS.md": "# 学习日志\n",
    "ERRORS.md": "# 错误日志\n",
    "FEATURE_REQUESTS.md": "# 功能请求\n",
}

for name, content in learnings_files.items():
    filepath = learnings_dir / name
    if not filepath.exists():
        print(f"[FILE] 创建 .learnings/{name}...")
        filepath.write_text(content, encoding='utf-8')
    else:
        print(f"[SKIP] .learnings/{name} 已存在")

# === 4. 同步工作区 .md 路径 ===
print("[SYNC] 同步工作区 .md 路径...")
old_path = "~/self-improving/"
new_path = "~/proactive-intelligence/"
old_path2 = "self-improving 文件"
new_path2 = "proactive-intelligence 文件"

md_files = list(WORKSPACE.glob("*.md"))
changes = 0

for md_file in md_files:
    content = md_file.read_text(encoding='utf-8')
    new_content = content.replace(old_path, new_path).replace(old_path2, new_path2)
    if new_content != content:
        md_file.write_text(new_content, encoding='utf-8')
        changes += 1
        print(f"[SYNC] {md_file.name}: 路径已更新")

if changes == 0:
    print("[SYNC] 无需更新")
else:
    print(f"[SYNC] 共更新 {changes} 个文件")

# === 5. 验证 ===
print("\n[OK] 初始化完成！")
print("\n[DIR] 数据目录：")
for item in sorted(BASE_DIR.rglob("*")):
    if item.is_file():
        print(f"  {item.relative_to(BASE_DIR)}")

print("\n[DIR] .learnings/：")
for item in sorted(learnings_dir.glob("*")):
    if item.is_file():
        print(f"  {item.name}")

print("\n[NEXT] 下一步：")
print("  1. 查看 ~/proactive-intelligence/memory.md")
print("  2. 查看 .learnings/LEARNINGS.md")
print("  3. 开始使用，系统会自动学习")

#!/usr/bin/env python3
"""
novel-character-registry — 角色信息表管理（已弃用）。

[WARN] 已弃用 — 请使用 `novel_state_manager.py add-char` 替代。
本脚本保留用于向前兼容，新项目不应调用。

维护 characters.json，记录每章出场角色及其关键属性。
支持逐章更新，防止 Observer_Alpha 式身份摇摆。

用法（已弃用）：
  python novel_character_registry.py init <project_dir>               # 初始化
  python novel_character_registry.py add <project_dir> <name> <data_json>
  python novel_character_registry.py get <project_dir> <name>
  python novel_character_registry.py list <project_dir>
"""

import os
import sys
import json


def _chr_path(project_dir: str) -> str:
    return os.path.join(project_dir, "data", "characters.json")


def init_registry(project_dir: str):
    path = _chr_path(project_dir)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    data = {}
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
        f.flush()
        os.fsync(f.fileno())
    print(f"OK registry initialized at {path}")


def _state_path(project_dir: str) -> str:
    return os.path.join(project_dir, "data", "novel_state.json")


def add_character(project_dir: str, name: str, data_json: str):
    path = _chr_path(project_dir)
    state_path = _state_path(project_dir)
    if not os.path.exists(state_path):
        print(f"ERROR: novel_state.json 未初始化（预期路径 {state_path}）")
        print(f"  → 必须在阶段1完成后运行 init")
        sys.exit(1)

    # 阶段门禁：从 novel_state.json 读取 current_phase
    _order = {"none": 0, "init": 10, "stage1_done": 20, "writing": 30, "chapter_done": 40, "stage3_ready": 50, "complete": 60}
    with open(state_path, "r", encoding="utf-8") as f:
        _state = json.load(f)
    _p = _order.get(_state.get("current_phase", "none"), 0)
    if _p < 20:
        print(f"ERROR: novel_character_registry 需要阶段 ≥ stage1_done(20)，当前为 {_state.get('current_phase', 'none')}({_p})")
        print(f"  请先完成大纲确认。")
        sys.exit(1)

    with open(path, "r", encoding="utf-8") as f:
        registry = json.load(f)

    try:
        char_data = json.loads(data_json)
    except json.JSONDecodeError:
        print("ERROR: invalid JSON data")
        sys.exit(1)

    if name in registry:
        existing = registry[name]
        existing["appearances"] = existing.get("appearances", []) + char_data.get("appearances", [])
        existing["attributes"] = {**existing.get("attributes", {}), **char_data.get("attributes", {})}
    else:
        registry[name] = char_data

    with open(path, "w", encoding="utf-8") as f:
        json.dump(registry, f, ensure_ascii=False, indent=2)
        f.flush()
        os.fsync(f.fileno())
    print(f"OK character '{name}' registered/updated")


def get_character(project_dir: str, name: str):
    path = _chr_path(project_dir)
    if not os.path.exists(path):
        print("ERROR: registry not initialized")
        sys.exit(1)
    with open(path, "r", encoding="utf-8") as f:
        registry = json.load(f)
    if name not in registry:
        print(f"NOT FOUND: '{name}'")
        sys.exit(1)
    print(json.dumps(registry[name], ensure_ascii=False, indent=2))


def list_characters(project_dir: str):
    path = _chr_path(project_dir)
    if not os.path.exists(path):
        print("ERROR: registry not initialized")
        sys.exit(1)
    with open(path, "r", encoding="utf-8") as f:
        registry = json.load(f)
    for name, data in registry.items():
        appearances = data.get("appearances", [])
        role = data.get("role", "未知")
        print(f"- {name} ({role}): 出场 {len(appearances)} 章")


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("用法: novel_character_registry.py <init|add|get|list> <project_dir> [args...]")
        sys.exit(1)

    command = sys.argv[1]
    project_dir = sys.argv[2]

    if command == "init":
        init_registry(project_dir)

    elif command == "add":
        name = sys.argv[3] if len(sys.argv) >= 4 else ""
        data_json = sys.argv[4] if len(sys.argv) >= 5 else "{}"
        add_character(project_dir, name, data_json)

    elif command == "get":
        name = sys.argv[3] if len(sys.argv) >= 4 else ""
        get_character(project_dir, name)

    elif command == "list":
        list_characters(project_dir)

    else:
        print(f"未知命令: {command}")
        sys.exit(1)

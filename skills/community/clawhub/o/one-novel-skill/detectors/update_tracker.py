#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
one-novel-skill 状态追踪自动更新器

从 chapter spec (JSON) 中提取角色状态变化，更新追踪/文件。

用法:
  python update_tracker.py --book "小说目录" --chapter 1
"""

import sys
sys.stdout.reconfigure(encoding='utf-8')
from pathlib import Path
import json

def read_spec(spec_path):
    """解析章节规格文件（统一 JSON 格式）"""
    with open(spec_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    if not isinstance(data, dict):
        raise ValueError(f"规格文件不是有效的字典: {spec_path}")

    result = {
        "chapter": data.get("chapter", 0),
        "title": data.get("title", ""),
        "after_chars": [],
        "plot_advances": [],
        "new_hooks": [],
    }

    # 解析 after_state 或降级到 before_state（v1.1 SpecBuilder 只输出 before_state）
    state_section = data.get("after_state", data.get("before_state", {}))
    if isinstance(state_section, dict):
        chars = state_section.get("characters", [])
        if isinstance(chars, list):
            for char in chars:
                if isinstance(char, dict):
                    result["after_chars"].append({
                        "name": char.get("name", "未知"),
                        # before_state 用 state/location，after_state 用 new_state/new_location
                        "state": char.get("new_state", char.get("state", "")),
                        "location": char.get("new_location", char.get("location", "")),
                    })

        # 解析 plot_advances
        advances = state_section.get("plot_advances", [])
        if isinstance(advances, list):
            result["plot_advances"] = [str(a) for a in advances]

    # 解析 new_hooks
    new_hooks = data.get("new_hooks", [])
    if isinstance(new_hooks, list):
        result["new_hooks"] = [str(h) for h in new_hooks]

    return result


def update_tracker(tracker_dir, spec):
    ch_label = f"#{spec['chapter']:03d} {spec['title']}"
    status_path = tracker_dir / "角色状态.md"
    hooks_path = tracker_dir / "伏笔.md"
    
    # Update 角色状态.md
    if status_path.exists():
        with open(status_path, 'r', encoding='utf-8') as f:
            content = f.read()
        lines = content.split('\n')
        for char in spec["after_chars"]:
            name = char["name"].partition("（")[0]  # Remove (tag) suffix for matching
            found = -1
            for i, line in enumerate(lines):
                if line.strip().startswith(f"## {name}"):
                    found = i; break
            if found >= 0:
                # 遍历角色区块内的表格行
                for i in range(found, min(found+15, len(lines))):
                    if "| 位置 " in lines[i]:
                        old_val = lines[i].split("|")[2].strip()
                        if char["location"]:
                            lines[i] = f"| 位置 | {old_val} \u2192 {char['location']}（{ch_label}时）"
                            print(f"  [OK] {name}: 位置更新 {char['location']}")
                    if "| 状态 " in lines[i]:
                        old_s = lines[i].split("|")[2].strip()
                        if char["state"]:
                            lines[i] = f"| 状态 | {old_s} \u2192 {char['state']}（{ch_label}时）"
                            print(f"  [OK] {name}: 状态更新 {char['state']}")
        with open(status_path, 'w', encoding='utf-8') as f:
            f.write('\n'.join(lines))
    else:
        print(f"  [!] 角色状态.md 不存在，跳过")
    
    # Update 伏笔.md — 幂等追加：检查是否已存在相同条目
    existing_hooks = set()
    if hooks_path.exists():
        with open(hooks_path, 'r', encoding='utf-8') as f:
            for line in f:
                existing_hooks.add(line.strip())

    with open(hooks_path, 'a', encoding='utf-8') as f:
        for h in spec.get("new_hooks", []):
            entry = f"- [{ch_label}] 埋设: {h}"
            if entry not in existing_hooks:
                f.write(entry + "\n")
                print(f"  [OK] 新钩子: {h}")
            else:
                print(f"  [SKIP] 钩子已存在: {h}")
        for a in spec.get("plot_advances", []):
            entry = f"- [{ch_label}] 推进: {a}"
            if entry not in existing_hooks:
                f.write(entry + "\n")
                print(f"  [OK] 伏笔推进: {a}")
            else:
                print(f"  [SKIP] 伏笔推进已存在: {a}")


def main():
    import argparse
    p = argparse.ArgumentParser()
    p.add_argument("--book", "-b", required=True)
    p.add_argument("--chapter", "-c", required=True)
    args = p.parse_args()
    
    book_dir = Path(args.book)
    if not book_dir.exists():
        print(f"[ERR] 小说目录不存在"); sys.exit(1)
    
    spec_path = book_dir / "规格" / f"第{int(args.chapter):03d}章.json"
    if not spec_path.exists():
        print(f"[ERR] 规格文件不存在: {spec_path}"); sys.exit(1)
    
    print(f"\n  状态追踪更新")
    print(f"  Spec: {spec_path}\n")
    spec = read_spec(spec_path)
    print(f"  章 {spec['chapter']}: {spec['title']}")
    
    tracker_dir = book_dir / "追踪"
    if not tracker_dir.exists():
        tracker_dir.mkdir(parents=True)
    
    update_tracker(tracker_dir, spec)
    print(f"\n  更新完成\n")


if __name__ == "__main__":
    main()

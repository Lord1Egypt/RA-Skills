#!/usr/bin/env python3
"""
《深渊狂嚎》追踪数据更新器
在精修/改写章节时手动录入该章的角色出场和伏笔。

用法：
  python3 record_chapter.py <chapter_number> \
    --characters "角色名1,角色名2,..." \
    --new "新角色名:重要性:描述:标签1,标签2" \
    --hook "描述|类别|重要性" \
    --hook "描述2|类别|重要性"

示例：
  python3 record_chapter.py V1Ch031 \
    --characters "理查德,梅丽安,托德,艾琳娜·烬羽" \
    --new "陆沉:minor:铁冠城守备队长:守备队,贵族" \
    --hook "陆沉的左臂纹身似乎与深渊印记相同|plot|major" \
    --hook "壁炉里的火焰突然变绿|world|normal"

类别: plot / character / world / mystery
重要性: normal / major / critical
"""
import json, sys, re, os
from pathlib import Path

NOVEL_DIR = Path(os.environ.get("NOVEL_DIR", "."))
CONTINUITY_DIR = NOVEL_DIR / "continuity"

ROSTER_FILE = CONTINUITY_DIR / "character_roster.json"
APPEAR_FILE = CONTINUITY_DIR / "chapter_appearances.json"
HOOKS_FILE = CONTINUITY_DIR / "hooks.json"

def parse_chapter(chapter_str: str) -> tuple:
    """'V1Ch031' -> (131, 'V1Ch031') 或 'V2Ch45' -> (45, 'V2Ch45')"""
    m = re.match(r'V(\d+)Ch(\d+)', chapter_str)
    if not m:
        raise ValueError(f"无效章节格式: {chapter_str}，请用 V1Ch001 或 V2Ch001 格式")
    vol = int(m.group(1))
    ch = int(m.group(2))
    if vol == 1:
        return ch + 100, chapter_str
    return ch, chapter_str


def load_json(path):
    if not path.exists():
        return {} if "roster" in path.name else []
    return json.loads(path.read_text(encoding="utf-8"))


def save_json(path, data):
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")


def main():
    import argparse
    parser = argparse.ArgumentParser(description="记录单章角色出场和伏笔")
    parser.add_argument("chapter", help="章节号，如 V1Ch031 或 V2Ch045")
    parser.add_argument("--characters", help="本登场角色，逗号分隔")
    parser.add_argument("--new", action="append", default=[], 
                       help="新角色: 格式 '名字:重要性:描述:标签1,标签2'")
    parser.add_argument("--hook", action="append", default=[],
                       help="伏笔: 格式 '描述|类别|重要性'")
    args = parser.parse_args()
    
    ch_num, ch_display = parse_chapter(args.chapter)
    
    # 加载现有数据
    roster = load_json(ROSTER_FILE)
    appearances = load_json(APPEAR_FILE)
    hooks = load_json(HOOKS_FILE)
    
    # 处理新角色
    for new_entry in args.new:
        parts = new_entry.split(":", 3)
        name = parts[0]
        importance = parts[1] if len(parts) > 1 else "minor"
        description = parts[2] if len(parts) > 2 else ""
        tags = parts[3].split(",") if len(parts) > 3 else []
        
        if name not in roster:
            roster[name] = {
                "name": name,
                "importance": importance,
                "first_appearance": ch_num,
                "last_appearance": ch_num,
                "total_appearances": 1,
                "description": description,
                "tags": tags,
                "status": "active",
                "disappears_for": 0,
            }
            print(f"  ✅ 新角色: {name} ({importance})")
        else:
            print(f"  ⚠️ 角色已存在: {name}，跳过")
    
    # 处理出场角色
    if args.characters:
        char_list = [c.strip() for c in args.characters.split(",")]
        
        # 更新名册
        for name in char_list:
            if name not in roster:
                roster[name] = {
                    "name": name,
                    "importance": "minor",
                    "first_appearance": ch_num,
                    "last_appearance": ch_num,
                    "total_appearances": 1,
                    "description": "",
                    "tags": [],
                    "status": "active",
                    "disappears_for": 0,
                }
                print(f"  ⚠️ 自动创建角色: {name} (minor)")
            entry = roster[name]
            if entry["first_appearance"] > ch_num:
                entry["first_appearance"] = ch_num
            if entry["last_appearance"] < ch_num:
                entry["last_appearance"] = ch_num
            entry["total_appearances"] += 1
        
        # 找出本新登场角色
        existing_app = [a for a in appearances if a["chapter"] == ch_num]
        new_chars = [n for n in char_list 
                    if n not in (existing_app[0]["characters"] if existing_app else [])]
        
        # 更新或创建出场记录
        if existing_app:
            app = existing_app[0]
            app["characters"] = sorted(set(app["characters"] + char_list))
            app["total_crowd"] = len(app["characters"])
            for nc in new_chars:
                if nc not in app["new_characters"]:
                    app["new_characters"].append(nc)
        else:
            appearances.append({
                "chapter": ch_num,
                "chapter_display": ch_display,
                "characters": sorted(char_list),
                "new_characters": sorted(new_chars),
                "total_crowd": len(char_list),
            })
        
        print(f"  ✅ 出场角色: {len(char_list)}人 (新{len(new_chars)}人)")
    
    # 处理伏笔
    for hook_str in args.hook:
        parts = hook_str.split("|", 2)
        desc = parts[0]
        cat = parts[1] if len(parts) > 1 else "plot"
        imp = parts[2] if len(parts) > 2 else "normal"
        
        # 去重
        exists = any(h["description"][:60] == desc[:60] for h in hooks)
        if not exists:
            hooks.append({
                "description": desc,
                "planted_chapter": ch_num,
                "chapter_display": ch_display,
                "expected_payoff": ch_num + 25,
                "category": cat,
                "importance": imp,
                "status": "active",
            })
            print(f"  ✅ 伏笔: {desc[:50]}... ({cat}/{imp})")
        else:
            print(f"  ⚠️ 伏笔已存在，跳过: {desc[:40]}...")
    
    # 排序
    appearances.sort(key=lambda a: a["chapter"])
    hooks.sort(key=lambda h: h["planted_chapter"])
    
    # 保存
    save_json(ROSTER_FILE, roster)
    save_json(APPEAR_FILE, appearances)
    save_json(HOOKS_FILE, hooks)
    
    # 统计
    print(f"\n📊 当前总计:")
    print(f"  角色: {len(roster)}人")
    print(f"  章节记录: {len(appearances)}章")
    print(f"  伏笔: {len(hooks)}条")
    print(f"\n✅ 完成！")


if __name__ == "__main__":
    main()

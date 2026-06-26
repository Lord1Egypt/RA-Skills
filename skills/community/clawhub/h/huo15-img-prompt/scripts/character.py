#!/usr/bin/env python3
"""
huo15-img-prompt — 角色卡持久化 v2.6

把 character_sheet 模式的输出存为可复用的"角色卡"，下次 `--char <name>` 直接调出。

每张角色卡 = 角色名 + 视觉描述 + 锁定参数（seed/preset/aspect/camera/lighting/palette）。
存到 ~/.huo15/characters/<safe_name>.json。

工作流：
  Turn 1（创建角色）:
    enhance_prompt.py "银发机甲少女, twin tails, glowing visor" \\
        -p 动漫 --character-sheet --save-char 银发机甲少女

  Turn 2 ~ N（复用）:
    enhance_prompt.py "新场景：在霓虹街头" --char 银发机甲少女 -p 赛博朋克
    enhance_prompt.py "在花海中" --char 银发机甲少女
    # → 自动注入角色描述 + 锁 seed，保证多张图角色一致

调用：
  character.py --list                          # 列出所有角色
  character.py --show 银发机甲少女              # 看角色详情
  character.py --delete 旧角色                  # 删除
  character.py --export 银发机甲少女 > char.json # 导出
  character.py --import < char.json            # 导入

"""

import sys
import os
import json
import re
import time
import argparse
from typing import Dict, List, Optional

VERSION = "3.1.0"

CHAR_DIR = os.path.expanduser("~/.huo15/characters")


def safe_name(name: str) -> str:
    return re.sub(r"[^\w\-]", "_", name)


def char_path(name: str) -> str:
    return os.path.join(CHAR_DIR, f"{safe_name(name)}.json")


def char_save(name: str, recipe: Dict) -> Dict:
    """从 build_prompt 的 result 里抽取角色锁存档。"""
    os.makedirs(CHAR_DIR, exist_ok=True)
    p = char_path(name)
    existing = char_load(name) or {}
    lock = recipe.get("consistency_lock", {}) or {}

    card = {
        "name": name,
        "version": VERSION,
        "created_at": existing.get("created_at") or int(time.time()),
        "updated_at": int(time.time()),
        "use_count": existing.get("use_count", 0),
        "subject_description": recipe.get("original", ""),
        "preset": recipe.get("preset", ""),
        "mix_secondary": recipe.get("mix_secondary", "") or "",
        "mix_ratio": recipe.get("mix_ratio"),
        "aspect": recipe.get("aspect", ""),
        "seed": recipe.get("seed_suggestion"),
        "camera": lock.get("camera", ""),
        "lighting": lock.get("lighting", ""),
        "palette": lock.get("palette", ""),
        "is_character_sheet": recipe.get("character_sheet", False),
        "positive_anchor": recipe.get("positive", "")[:500],
    }
    with open(p, "w", encoding="utf-8") as f:
        json.dump(card, f, ensure_ascii=False, indent=2)
    return card


def char_load(name: str) -> Optional[Dict]:
    p = char_path(name)
    if not os.path.isfile(p):
        return None
    try:
        with open(p, "r", encoding="utf-8") as f:
            return json.load(f)
    except (json.JSONDecodeError, IOError):
        return None


def char_apply(name: str, args) -> Optional[Dict]:
    """加载角色卡作为 args 的默认值。仅在 CLI 未显式给时填充。"""
    card = char_load(name)
    if not card:
        return None

    # 增量计数
    card["use_count"] = card.get("use_count", 0) + 1
    try:
        with open(char_path(name), "w", encoding="utf-8") as f:
            json.dump(card, f, ensure_ascii=False, indent=2)
    except IOError:
        pass

    # 注入到 args
    desc = card.get("subject_description", "")
    if args.subject and desc:
        # 把角色描述前置到主体描述前
        args.subject = f"{desc}, {args.subject}"
    elif desc and not args.subject:
        args.subject = desc

    if not args.preset and card.get("preset"):
        if card.get("mix_secondary"):
            args.preset = f"{card['preset']}+{card['mix_secondary']}"
        else:
            args.preset = card["preset"]

    if not args.aspect and card.get("aspect"):
        args.aspect = card["aspect"]

    # 角色卡的 seed 是核心锁，永远应用（除非 CLI 显式覆盖）
    if args.seed is None and card.get("seed") is not None:
        args.seed = card["seed"]

    return card


def char_list() -> List[Dict]:
    if not os.path.isdir(CHAR_DIR):
        return []
    out = []
    for fn in sorted(os.listdir(CHAR_DIR)):
        if not fn.endswith(".json"):
            continue
        try:
            with open(os.path.join(CHAR_DIR, fn), "r", encoding="utf-8") as f:
                out.append(json.load(f))
        except (json.JSONDecodeError, IOError):
            continue
    return out


def char_delete(name: str) -> bool:
    p = char_path(name)
    if os.path.isfile(p):
        os.remove(p)
        return True
    return False


# ─────────────────────────────────────────────────────────
# CLI
# ─────────────────────────────────────────────────────────
def print_char(card: Dict):
    print(f"\n👤 {card['name']}")
    print(f"  创建: {time.strftime('%Y-%m-%d %H:%M', time.localtime(card.get('created_at', 0)))}")
    print(f"  更新: {time.strftime('%Y-%m-%d %H:%M', time.localtime(card.get('updated_at', 0)))}")
    print(f"  用过: {card.get('use_count', 0)} 次")
    print(f"  描述: {card.get('subject_description', '')[:120]}")
    print(f"  预设: {card.get('preset', '')}", end="")
    if card.get("mix_secondary"):
        print(f" + {card['mix_secondary']} (mix={card.get('mix_ratio', 0.6)})")
    else:
        print()
    print(f"  画幅: {card.get('aspect', '')}")
    print(f"  种子: {card.get('seed', '')} (锁定)")
    if card.get("camera"):
        print(f"  相机: {card['camera']}")
    if card.get("lighting"):
        print(f"  光影: {card['lighting']}")
    if card.get("palette"):
        print(f"  色板: {card['palette']}")
    if card.get("is_character_sheet"):
        print(f"  ✨ 来自 character-sheet 模式（T-pose 多视图）")


def main():
    parser = argparse.ArgumentParser(
        description=f"huo15-img-prompt character v{VERSION} — 角色卡管理",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  character.py --list                              # 列出全部
  character.py --show 银发机甲少女                  # 详情
  character.py --delete 旧角色                      # 删除
  character.py --export 银发机甲少女                # 导出 JSON 到 stdout
  cat char.json | character.py --import             # 从 stdin 导入

✨ 创建/复用角色（在 enhance_prompt.py 里）:
  enhance_prompt.py "银发机甲少女" -p 动漫 --character-sheet --save-char 银发机甲少女
  enhance_prompt.py "在霓虹街头" --char 银发机甲少女
""",
    )
    g = parser.add_mutually_exclusive_group(required=True)
    g.add_argument("--list", action="store_true", help="列出所有角色")
    g.add_argument("--show", help="显示单个角色详情")
    g.add_argument("--delete", help="删除角色")
    g.add_argument("--export", help="导出角色到 stdout（JSON）")
    g.add_argument("--import", dest="imp", action="store_true", help="从 stdin 导入角色")
    parser.add_argument("-j", "--json", action="store_true", help="JSON 输出（配合 --list / --show）")
    parser.add_argument("-v", "--version", action="version", version=f"%(prog)s v{VERSION}")
    args = parser.parse_args()

    if args.list:
        cards = char_list()
        if args.json:
            print(json.dumps({"version": VERSION, "characters": cards}, ensure_ascii=False, indent=2))
            return
        if not cards:
            print(f"\n📭 暂无角色（在 {CHAR_DIR}）\n")
            print("💡 创建：enhance_prompt.py \"主体\" -p 预设 --character-sheet --save-char 名字\n")
            return
        print(f"\n👥 已存角色 ({len(cards)} 个，{CHAR_DIR}):")
        for c in cards:
            print(f"  • {c['name']:20s}  {c.get('preset', '?'):12s}  seed={c.get('seed', '?')}  用过 {c.get('use_count', 0)} 次")
        print()
        return

    if args.show:
        card = char_load(args.show)
        if not card:
            print(f"❌ 角色不存在: {args.show}", file=sys.stderr)
            sys.exit(1)
        if args.json:
            print(json.dumps(card, ensure_ascii=False, indent=2))
        else:
            print_char(card)
            print()
        return

    if args.delete:
        if char_delete(args.delete):
            print(f"✅ 已删除: {args.delete}")
        else:
            print(f"❌ 角色不存在: {args.delete}", file=sys.stderr)
            sys.exit(1)
        return

    if args.export:
        card = char_load(args.export)
        if not card:
            print(f"❌ 角色不存在: {args.export}", file=sys.stderr)
            sys.exit(1)
        print(json.dumps(card, ensure_ascii=False, indent=2))
        return

    if args.imp:
        try:
            card = json.loads(sys.stdin.read())
        except json.JSONDecodeError as e:
            print(f"❌ 解析失败: {e}", file=sys.stderr)
            sys.exit(1)
        name = card.get("name")
        if not name:
            print(f"❌ JSON 缺 name 字段", file=sys.stderr)
            sys.exit(1)
        os.makedirs(CHAR_DIR, exist_ok=True)
        with open(char_path(name), "w", encoding="utf-8") as f:
            json.dump(card, f, ensure_ascii=False, indent=2)
        print(f"✅ 已导入: {name}")
        return


if __name__ == "__main__":
    main()

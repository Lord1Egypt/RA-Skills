#!/usr/bin/env python3
"""
huo15-img-prompt — 品牌套件 v3.0

把品牌 VI（colors/fonts/keywords/forbidden）持久化为 brand kit JSON，
出图时 `--brand-kit <name>` 自动注入到 prompt：
  - colors → palette 锁
  - fonts → 添加到 prompt 的 typography 提示
  - keywords → 视觉关键词追加
  - forbidden → 加入 negative prompt
  - logo_description → 加入 prompt 用于 cref 风格

存储：~/.huo15/brand_kits/<name>.json

工作流：
  Step 1: 创建 brand kit
    brand_kit.py --create huo15 \\
        --colors "#ff6b35,#2d3047,#fafafa" \\
        --fonts "PingFang SC,Source Han Serif" \\
        --keywords "现代,简洁,专业,温暖" \\
        --forbidden "competitor logos, low-quality"

  Step 2: 出图时引用
    enhance_prompt.py "公司年会海报" -p 品牌KV --brand-kit huo15

  Step 3: 配合品牌规范抓取技能（huo15-openclaw-brand-protocol）
    用 brand-protocol 抓品牌规范 → 导入到 brand kit → 用 img-prompt 出图

  brand_kit.py --list / --show / --delete / --export / --import
"""

import sys
import os
import json
import re
import time
import argparse
from typing import Dict, List, Optional

VERSION = "3.1.0"

KIT_DIR = os.path.expanduser("~/.huo15/brand_kits")


def safe_name(name: str) -> str:
    return re.sub(r"[^\w\-]", "_", name)


def kit_path(name: str) -> str:
    return os.path.join(KIT_DIR, f"{safe_name(name)}.json")


def kit_load(name: str) -> Optional[Dict]:
    p = kit_path(name)
    if not os.path.isfile(p):
        return None
    try:
        with open(p, "r", encoding="utf-8") as f:
            return json.load(f)
    except (json.JSONDecodeError, IOError):
        return None


def kit_save(name: str, kit: Dict) -> str:
    os.makedirs(KIT_DIR, exist_ok=True)
    p = kit_path(name)
    existing = kit_load(name) or {}
    kit["name"] = name
    kit["version"] = VERSION
    kit["created_at"] = existing.get("created_at") or int(time.time())
    kit["updated_at"] = int(time.time())
    kit["use_count"] = existing.get("use_count", 0)
    with open(p, "w", encoding="utf-8") as f:
        json.dump(kit, f, ensure_ascii=False, indent=2)
    return p


def kit_list() -> List[Dict]:
    if not os.path.isdir(KIT_DIR):
        return []
    out = []
    for fn in sorted(os.listdir(KIT_DIR)):
        if not fn.endswith(".json"):
            continue
        try:
            with open(os.path.join(KIT_DIR, fn), "r", encoding="utf-8") as f:
                out.append(json.load(f))
        except (json.JSONDecodeError, IOError):
            continue
    return out


def kit_delete(name: str) -> bool:
    p = kit_path(name)
    if os.path.isfile(p):
        os.remove(p)
        return True
    return False


# ─────────────────────────────────────────────────────────
# 注入逻辑（被 enhance_prompt.py import）
# ─────────────────────────────────────────────────────────
def kit_apply(name: str, args) -> Optional[Dict]:
    """加载 brand kit 并注入 args。

    args 是 enhance_prompt.py 的 ArgumentParser Namespace。我们补全：
      - args.subject 末尾追加品牌关键词
      - args.avoid 追加 forbidden（合并到 negative）
    返回 kit dict（用于显示）或 None。
    """
    kit = kit_load(name)
    if not kit:
        return None

    # 计数
    kit["use_count"] = kit.get("use_count", 0) + 1
    try:
        with open(kit_path(name), "w", encoding="utf-8") as f:
            json.dump(kit, f, ensure_ascii=False, indent=2)
    except IOError:
        pass

    # 注入 keywords 到 subject
    keywords = kit.get("keywords") or []
    if keywords and args.subject:
        kw_str = ", ".join(keywords)
        # 不把 keywords 重复加入
        if all(k not in args.subject for k in keywords[:2]):
            args.subject = f"{args.subject}, {kw_str}"

    # 注入 colors 到 subject（作为色板提示）
    colors = kit.get("colors") or []
    if colors and args.subject:
        # 把色板写成自然语言，让 T2I 模型理解
        colors_phrase = f"brand color palette {' '.join(colors)}"
        args.subject = f"{args.subject}, {colors_phrase}"

    # 注入 logo_description（如果有）
    if kit.get("logo_description") and args.subject:
        args.subject = f"{args.subject}, brand identity: {kit['logo_description']}"

    # 注入 forbidden 到 negative
    forbidden = kit.get("forbidden") or []
    if forbidden:
        existing_avoid = args.avoid or ""
        new_avoid = ", ".join(forbidden)
        args.avoid = f"{existing_avoid}, {new_avoid}".strip(", ")

    return kit


# ─────────────────────────────────────────────────────────
# CLI
# ─────────────────────────────────────────────────────────
def parse_csv(s: str) -> List[str]:
    if not s:
        return []
    return [x.strip() for x in s.split(",") if x.strip()]


def print_kit(kit: Dict):
    print(f"\n🎨 {kit['name']}")
    print(f"  创建: {time.strftime('%Y-%m-%d %H:%M', time.localtime(kit.get('created_at', 0)))}")
    print(f"  更新: {time.strftime('%Y-%m-%d %H:%M', time.localtime(kit.get('updated_at', 0)))}")
    print(f"  用过: {kit.get('use_count', 0)} 次")
    if kit.get("colors"):
        print(f"  颜色: {' '.join(kit['colors'])}")
    if kit.get("fonts"):
        print(f"  字体: {' / '.join(kit['fonts'])}")
    if kit.get("keywords"):
        print(f"  关键词: {', '.join(kit['keywords'])}")
    if kit.get("forbidden"):
        print(f"  禁止: {', '.join(kit['forbidden'])}")
    if kit.get("logo_description"):
        print(f"  Logo: {kit['logo_description']}")
    if kit.get("description"):
        print(f"  描述: {kit['description']}")


def main():
    parser = argparse.ArgumentParser(
        description=f"huo15-img-prompt brand_kit v{VERSION} — 品牌套件管理",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  brand_kit.py --create huo15 \\
      --colors "#ff6b35,#2d3047,#fafafa" \\
      --fonts "PingFang SC,Source Han Serif" \\
      --keywords "现代,简洁,专业,温暖" \\
      --forbidden "competitor logos, low quality" \\
      --logo "minimal flame mark in orange"

  brand_kit.py --list
  brand_kit.py --show huo15
  brand_kit.py --delete 旧品牌
  brand_kit.py --export huo15 > huo15.json
  cat huo15.json | brand_kit.py --import

✨ 在 enhance_prompt.py 里使用:
  enhance_prompt.py "公司年会海报" -p 品牌KV --brand-kit huo15
""",
    )
    g = parser.add_mutually_exclusive_group(required=True)
    g.add_argument("--create", metavar="NAME", help="创建品牌套件")
    g.add_argument("--update", metavar="NAME", help="更新品牌套件（保留未指定字段）")
    g.add_argument("--list", action="store_true", help="列出所有")
    g.add_argument("--show", metavar="NAME", help="显示详情")
    g.add_argument("--delete", metavar="NAME", help="删除")
    g.add_argument("--export", metavar="NAME", help="导出 JSON 到 stdout")
    g.add_argument("--import", dest="imp", action="store_true", help="从 stdin 导入")

    parser.add_argument("--colors", default="", help="逗号分隔的色值，例 '#ff6b35,#2d3047'")
    parser.add_argument("--fonts", default="", help="字体，例 'PingFang SC,Source Han Serif'")
    parser.add_argument("--keywords", default="", help="视觉关键词")
    parser.add_argument("--forbidden", default="", help="禁止出现的元素（合并到负面词）")
    parser.add_argument("--logo", default="", help="Logo 一句话描述")
    parser.add_argument("--description", default="", help="品牌描述")

    parser.add_argument("-j", "--json", action="store_true", help="JSON 输出")
    parser.add_argument("-v", "--version", action="version", version=f"%(prog)s v{VERSION}")
    args = parser.parse_args()

    if args.list:
        kits = kit_list()
        if args.json:
            print(json.dumps({"version": VERSION, "kits": kits}, ensure_ascii=False, indent=2))
            return
        if not kits:
            print(f"\n📭 暂无品牌套件 ({KIT_DIR})\n")
            return
        print(f"\n🎨 品牌套件 ({len(kits)} 个):")
        for k in kits:
            print(f"  • {k['name']:20s}  {len(k.get('colors', []))} 色  {len(k.get('keywords', []))} 关键词  用过 {k.get('use_count', 0)} 次")
        print()
        return

    if args.show:
        kit = kit_load(args.show)
        if not kit:
            print(f"❌ 不存在: {args.show}", file=sys.stderr)
            sys.exit(1)
        if args.json:
            print(json.dumps(kit, ensure_ascii=False, indent=2))
        else:
            print_kit(kit)
            print()
        return

    if args.delete:
        if kit_delete(args.delete):
            print(f"✅ 已删除: {args.delete}")
        else:
            print(f"❌ 不存在: {args.delete}", file=sys.stderr)
            sys.exit(1)
        return

    if args.export:
        kit = kit_load(args.export)
        if not kit:
            print(f"❌ 不存在: {args.export}", file=sys.stderr)
            sys.exit(1)
        print(json.dumps(kit, ensure_ascii=False, indent=2))
        return

    if args.imp:
        try:
            kit = json.loads(sys.stdin.read())
        except json.JSONDecodeError as e:
            print(f"❌ 解析失败: {e}", file=sys.stderr)
            sys.exit(1)
        name = kit.get("name")
        if not name:
            print("❌ JSON 缺 name 字段", file=sys.stderr)
            sys.exit(1)
        kit_save(name, kit)
        print(f"✅ 已导入: {name}")
        return

    if args.create or args.update:
        name = args.create or args.update
        if args.create and kit_load(name):
            print(f"⚠️  '{name}' 已存在，用 --update 覆盖", file=sys.stderr)
            sys.exit(1)
        existing = kit_load(name) if args.update else {}
        kit = dict(existing or {})
        if args.colors:
            kit["colors"] = parse_csv(args.colors)
        if args.fonts:
            kit["fonts"] = parse_csv(args.fonts)
        if args.keywords:
            kit["keywords"] = parse_csv(args.keywords)
        if args.forbidden:
            kit["forbidden"] = parse_csv(args.forbidden)
        if args.logo:
            kit["logo_description"] = args.logo
        if args.description:
            kit["description"] = args.description

        kit_save(name, kit)
        action = "创建" if args.create else "更新"
        print(f"✅ 已{action}: {name}")
        print_kit(kit_load(name))
        print()


if __name__ == "__main__":
    main()

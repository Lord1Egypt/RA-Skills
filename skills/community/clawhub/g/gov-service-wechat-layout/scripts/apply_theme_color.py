#!/usr/bin/env python3
"""apply_theme_color.py — 把模板里的占位主题色 #ff6d4d 替换为本篇主题色。

仅替换占位主题色（#ff6d4d 通用默认 / #438EDB A2 默认，大小写不敏感）；**警示红 #ff0000 与 正确蓝 #5f9cef 不动**（固定语义色）。
用法：
    python apply_theme_color.py --input template-C-guide.md.html --color #be5960
    python apply_theme_color.py --input in.html --color 5f9cef --output out.html
    python apply_theme_color.py --list
"""
import argparse
import re
import sys

# 占位主题色（仅这些会被替换）
BRAND_PLACEHOLDERS = ("#ff6d4d", "#438EDB")
# 固定语义色（绝不替换）
FIXED = ("#ff0000", "#5f9cef")

CANDIDATES = {
    "#ff6d4d": "橙红 — 默认/通用（指南、答疑）",
    "#be5960": "玫红 — 政策解读（沉稳）",
    "#ff8587": "粉红 — 新政/温和话题",
    "#fa6729": "橙 — 互动答疑（活泼）",
    "#438EDB": "社保蓝 — A2 新政解读默认（社保政务号品牌色，与正确蓝 #5f9cef 区分）",
    "#289DDA": "医保蓝 — 医保类文章备选（国家医保局官方 CHS 字形色）",
    "无": "黑白 — 通知公告（公文，不设主题色）",
}


def normalize(hexstr: str) -> str:
    s = hexstr.strip()
    if not s.startswith("#"):
        s = "#" + s
    if not re.fullmatch(r"#[0-9a-fA-F]{6}", s):
        sys.exit(f"✗ 无效色值: {hexstr}（需为 #RRGGBB 6 位十六进制）")
    return s.lower()


def main():
    ap = argparse.ArgumentParser(description="替换模板占位主题色为本篇主题色")
    ap.add_argument("--input", help="输入 HTML 模板路径")
    ap.add_argument("--color", help="本篇主题色，如 #be5960")
    ap.add_argument("--output", help="输出路径（默认覆盖 --input）")
    ap.add_argument("--list", action="store_true", help="列出主题色候选库")
    args = ap.parse_args()

    if args.list:
        print("主题色候选库：")
        for c, desc in CANDIDATES.items():
            print(f"  {c:<8} {desc}")
        return

    if not args.input or not args.color:
        ap.error("--input 和 --color 为必填（或用 --list 查看候选库）")

    new_color = normalize(args.color)
    if new_color in FIXED:
        sys.exit(f"✗ {new_color} 是固定语义色，不能用作主题色（警示红 #ff0000 / 正确蓝 #5f9cef 不可换）")

    with open(args.input, "r", encoding="utf-8") as f:
        text = f.read()

    total = 0
    for ph in BRAND_PLACEHOLDERS:
        # 大小写不敏感替换占位主题色
        new_text, n = re.subn(re.escape(ph), new_color, text, flags=re.IGNORECASE)
        total += n
        text = new_text

    out_path = args.output or args.input
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(text)

    print(f"✓ 替换 {total} 处占位主题色 → {new_color}")
    print(f"  警示红 #ff0000 / 正确蓝 #5f9cef 未改动（固定语义色）")
    print(f"  输出: {out_path}")


if __name__ == "__main__":
    main()

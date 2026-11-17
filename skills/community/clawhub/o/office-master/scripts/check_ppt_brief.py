#!/usr/bin/env python3
"""check_ppt_brief.py — 校验演示文稿大纲（brief）的结构合理性。

纯标准库、零依赖、只读、确定性：不联网、不修改任何文件、同输入同输出。
规则来源：assets/doc-style-rules.json（模板驱动脚本，读取时跳过 "_" 开头的注释键）。

约定：Markdown brief 中 H1 为标题，每个 H2 为一页幻灯片；校验页数、页标题长度、
重复标题、单页正文长度、frontmatter 的 title 键。

作用域约定（重要）：围栏代码块（``` 或 ~~~）内部不参与分页——代码块里的 `## step`
是 shell 注释，不是幻灯片页。缺这一步会让页数静默虚增（3 页 brief 被数成 5 页且仍
落在 min/max 区间内、门禁静默通过），下游按 H2 分页的转换随之产出错误页数。

用法:
  python3 scripts/check_ppt_brief.py --help
  python3 scripts/check_ppt_brief.py --check-rules            # 自检规则文件（必须 0 错误）
  python3 scripts/check_ppt_brief.py assets/presentation-brief-template.md

退出码: 0 = 全部合规 / 1 = 发现结构问题 / 2 = 规则文件无法解析。
"""
import argparse
import json
import os
import re
import sys

DEFAULT_RULES = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "assets", "doc-style-rules.json")

HEADING_RE = re.compile(r"^(#{1,6})\s+(.+?)\s*#*$")
# 围栏：``` 或 ~~~ 起，允许最多 3 个前导空格。别写 r"^```{3,}"——{3,} 只作用于第 3 个反引号，
# 会变成「要求 ≥5 个反引号」，普通围栏匹配不上、剥离静默失效。
FENCE_RE = re.compile(r"^ {0,3}(`{3,}|~{3,})")


def iter_prose_lines(text):
    """逐行产出原始行，跳过围栏代码块内部与围栏行本身（闭合须同字符且不短于开启）。"""
    fence_char, fence_len = None, 0
    for line in text.split("\n"):
        m = FENCE_RE.match(line)
        if m:
            marker = m.group(1)
            ch, ln = marker[0], len(marker)
            if fence_char is None:
                fence_char, fence_len = ch, ln
                continue
            if ch == fence_char and ln >= fence_len:
                fence_char, fence_len = None, 0
                continue
        if fence_char is not None:
            continue
        yield line


def load_rules(path):
    try:
        with open(path, encoding="utf-8") as fh:
            return json.load(fh)
    except (OSError, ValueError) as exc:
        print(f"[ERROR] 规则文件无法解析: {path} -> {exc}", file=sys.stderr)
        sys.exit(2)


def visible(data):
    return {k: v for k, v in data.items() if not k.startswith("_")}


def check_rules_schema(rules, path):
    errors = []
    for key in ("ppt_min_slides", "ppt_max_slides", "ppt_max_title_len", "ppt_max_body_chars"):
        if not isinstance(rules.get(key), int):
            errors.append(f"{key} 必须是整数")
    if rules.get("ppt_min_slides", 0) > rules.get("ppt_max_slides", 0):
        errors.append("ppt_min_slides 不能大于 ppt_max_slides")
    if errors:
        print(f"[FAIL] 规则文件结构校验未通过: {path}", file=sys.stderr)
        for e in errors:
            print(f"  ✗ {e}", file=sys.stderr)
        return 1
    print(f"[OK] 规则文件结构合法: {path}（slides {rules['ppt_min_slides']}-{rules['ppt_max_slides']}, max_title {rules['ppt_max_title_len']}）", file=sys.stderr)
    return 0


def parse_brief(path):
    with open(path, encoding="utf-8", errors="replace") as fh:
        text = fh.read()
    # frontmatter title
    title = None
    if text.startswith("---"):
        end = text.find("\n---", 3)
        if end != -1:
            block = text[3:end]
            m = re.search(r"title:\s*(.+)", block)
            if m:
                title = m.group(1).strip().strip("\"'")
    # 按 H2 切分幻灯片。围栏代码块内的 ## 是注释、不切页，但其正文仍计入当页篇幅
    # （幻灯片上代码块确实占版面，故只跳过「切页判定」，不跳过 body 累积）。
    slides = []
    cur = None
    fence_char, fence_len = None, 0
    for line in text.split("\n"):
        fm = FENCE_RE.match(line)
        in_fence_before = fence_char is not None
        if fm:
            marker = fm.group(1)
            ch, ln = marker[0], len(marker)
            if fence_char is None:
                fence_char, fence_len = ch, ln
            elif ch == fence_char and ln >= fence_len:
                fence_char, fence_len = None, 0
        m = None if (in_fence_before or fm) else HEADING_RE.match(line)
        if m and len(m.group(1)) == 2:
            if cur is not None:
                slides.append(cur)
            cur = {"title": m.group(2).strip(), "body": []}
        elif cur is not None:
            cur["body"].append(line)
    if cur is not None:
        slides.append(cur)
    return title, slides


def main():
    ap = argparse.ArgumentParser(description="校验演示文稿大纲结构（只读、确定性）")
    ap.add_argument("--rules", default=DEFAULT_RULES, help="规则文件路径（默认 assets/doc-style-rules.json）")
    ap.add_argument("--check-rules", action="store_true", help="仅自检规则文件结构，必须 0 错误")
    ap.add_argument("paths", nargs="*", help="待校验的 brief .md 文件（默认 assets/presentation-brief-template.md）")
    args = ap.parse_args()

    rules = visible(load_rules(args.rules))
    if args.check_rules:
        return check_rules_schema(rules, args.rules)

    targets = args.paths or [os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "assets", "presentation-brief-template.md")]
    total = 0
    for path in targets:
        if not path.endswith(".md"):
            print(f"[WARN] 跳过非 .md: {path}", file=sys.stderr)
            continue
        title, slides = parse_brief(path)
        n = len(slides)
        if n < rules.get("ppt_min_slides", 1):
            print(f"[结构] {path}: 页数 {n} 少于最小 {rules['ppt_min_slides']}", file=sys.stderr)
            total += 1
        if n > rules.get("ppt_max_slides", 999):
            print(f"[结构] {path}: 页数 {n} 超过最大 {rules['ppt_max_slides']}", file=sys.stderr)
            total += 1
        if title is None:
            print(f"[结构] {path}: frontmatter 缺少 title 键", file=sys.stderr)
            total += 1
        seen = {}
        for s in slides:
            if not s["title"]:
                print(f"[结构] {path}: 存在空页标题", file=sys.stderr)
                total += 1
            elif len(s["title"]) > rules.get("ppt_max_title_len", 999):
                print(f"[结构] {path}: 页标题过长（{len(s['title'])}>{rules['ppt_max_title_len']}）: {s['title']}", file=sys.stderr)
                total += 1
            if s["title"] in seen:
                print(f"[结构] {path}: 重复页标题: {s['title']}", file=sys.stderr)
                total += 1
            else:
                seen[s["title"]] = True
            body = "\n".join(s["body"]).strip()
            if len(body) > rules.get("ppt_max_body_chars", 9999):
                print(f"[结构] {path}: 页正文过长（{len(body)}>{rules['ppt_max_body_chars']}）: {s['title']}", file=sys.stderr)
                total += 1
    if total:
        print(f"\n[FAIL] 发现 {total} 处结构问题", file=sys.stderr)
        return 1
    print("[OK] 演示大纲结构全部通过", file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main())

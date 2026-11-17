#!/usr/bin/env python3
"""check_doc_style.py — 校验 Markdown 文档的标题层级一致性与样式规范。

纯标准库、零依赖、只读、确定性：不联网、不修改任何文件、同输入同输出。
规则来源：assets/doc-style-rules.json（模板驱动脚本，读取时跳过 "_" 开头的注释键）。

校验项：单一 H1、标题层级不跳级、最大深度、重复标题 slug、必需 frontmatter 键、残留 token。

作用域约定（重要）：
  - 围栏代码块（``` 或 ~~~，含缩进不超过 3 空格）内部一律不参与任何校验。
    代码块里的 `# comment` / `## step` 是注释，不是标题；示例代码里的 TODO 是示例，不是交付物残留。
  - 残留 token 检测会剥离行内代码（`TODO` 这种反引号包裹的写法视为「在讲这个 token」而非残留）。
  - 本脚本校验的是**交付稿件**（要转 Word/PPT/PDF 的 .md），required_frontmatter_keys 按稿件规范配置。
    不要对含 SKILL.md 的技能仓库根目录递归跑——SKILL.md 用 name/description/metadata，天然无 title 键。

用法:
  python3 scripts/check_doc_style.py --help
  python3 scripts/check_doc_style.py --check-rules            # 自检规则文件（必须 0 错误）
  python3 scripts/check_doc_style.py docs/outline.md          # 校验单文件
  python3 scripts/check_doc_style.py docs/                    # 递归校验稿件目录

退出码: 0 = 全部合规 / 1 = 发现样式问题 / 2 = 规则文件无法解析。
"""
import argparse
import json
import os
import re
import sys

DEFAULT_RULES = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "assets", "doc-style-rules.json")

HEADING_RE = re.compile(r"^(#{1,6})\s+(.+?)\s*#*$")
# 围栏：``` 或 ~~~ 起，允许最多 3 个前导空格（CommonMark）。
# 注意别写成 r"^```{3,}" —— {3,} 只作用于紧邻的第 3 个反引号，那样实际要求 ≥5 个反引号，
# 普通三反引号围栏会完全匹配不上，代码块剥离静默失效（本仓库曾踩此坑）。
FENCE_RE = re.compile(r"^ {0,3}(`{3,}|~{3,})")
INLINE_CODE_RE = re.compile(r"`[^`\n]*`")


def iter_prose_lines(text):
    """逐行产出 (行号, 原始行)，跳过围栏代码块内部与围栏行本身。

    闭合规则按 CommonMark 简化：闭合围栏字符须与开启一致且长度不短于开启长度，
    否则视为块内普通内容（保证嵌套示例里的 ``` 不会提前闭合外层 ````）。
    """
    fence_char, fence_len = None, 0
    for i, line in enumerate(text.split("\n"), 1):
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
        yield i, line


def load_rules(path):
    try:
        with open(path, encoding="utf-8") as fh:
            return json.load(fh)
    except (OSError, ValueError) as exc:
        print(f"[ERROR] 规则文件无法解析: {path} -> {exc}", file=sys.stderr)
        sys.exit(2)


def visible(data):
    return {k: v for k, v in data.items() if not k.startswith("_")}


def slugify(text):
    text = text.strip().lower()
    text = re.sub(r"[`*_]", "", text)
    text = re.sub(r"[^\w\s-]", "", text, flags=re.UNICODE)
    return text.replace(" ", "-")


def check_rules_schema(rules, path):
    errors = []
    for key in ("single_h1", "no_skipped_levels"):
        if not isinstance(rules.get(key), bool):
            errors.append(f"{key} 必须是布尔")
    if not isinstance(rules.get("required_frontmatter_keys"), list):
        errors.append("required_frontmatter_keys 必须是列表")
    if not isinstance(rules.get("missing_tokens"), list) or not rules["missing_tokens"]:
        errors.append("missing_tokens 必须是非空列表")
    if not isinstance(rules.get("max_heading_depth"), int):
        errors.append("max_heading_depth 必须是整数")
    if errors:
        print(f"[FAIL] 规则文件结构校验未通过: {path}", file=sys.stderr)
        for e in errors:
            print(f"  ✗ {e}", file=sys.stderr)
        return 1
    print(f"[OK] 规则文件结构合法: {path}（single_h1={rules['single_h1']}, max_depth={rules['max_heading_depth']}）", file=sys.stderr)
    return 0


def parse_frontmatter(text):
    if text.startswith("---"):
        end = text.find("\n---", 3)
        if end != -1:
            block = text[3:end].strip("\n")
            keys = [ln.split(":", 1)[0].strip() for ln in block.splitlines() if ":" in ln]
            return set(keys)
    return None


def scan_file(path, rules):
    problems = 0
    with open(path, encoding="utf-8", errors="replace") as fh:
        text = fh.read()

    # frontmatter 必需键
    fm_keys = parse_frontmatter(text)
    if fm_keys is not None:
        for req in rules.get("required_frontmatter_keys", []):
            if req not in fm_keys:
                print(f"[样式] {path}: frontmatter 缺少必需键 '{req}'", file=sys.stderr)
                problems += 1

    # 标题层级（围栏代码块内的 # 注释不算标题）
    headings = []
    for i, line in iter_prose_lines(text):
        m = HEADING_RE.match(line)
        if m:
            headings.append((len(m.group(1)), m.group(2).strip(), i))

    h1 = [h for h in headings if h[0] == 1]
    if rules.get("single_h1") and len(h1) != 1:
        print(f"[样式] {path}: H1 数量应为 1，实际 {len(h1)}", file=sys.stderr)
        problems += 1

    max_depth = rules.get("max_heading_depth", 6)
    prev = 0
    slugs = {}
    for level, txt, ln in headings:
        if level > max_depth:
            print(f"[样式] {path}:{ln} 标题层级 {level} 超过最大深度 {max_depth}", file=sys.stderr)
            problems += 1
        if rules.get("no_skipped_levels") and prev > 0 and level > prev + 1:
            print(f"[样式] {path}:{ln} 标题层级从 {prev} 跳到 {level}（禁止跳级）", file=sys.stderr)
            problems += 1
        s = slugify(txt)
        if s in slugs:
            print(f"[样式] {path}:{ln} 重复标题（slug='{s}'，首次在 {slugs[s]} 行）", file=sys.stderr)
            problems += 1
        else:
            slugs[s] = ln
        prev = level

    # 残留 token（剥离围栏代码块与行内代码：示例/反例/「在讲这个 token」都不算残留）
    tokens = rules.get("missing_tokens", [])
    if tokens:
        token_re = re.compile("|".join(re.escape(t) for t in tokens))
        for i, line in iter_prose_lines(text):
            prose = INLINE_CODE_RE.sub("", line)
            if token_re.search(prose):
                hits = [t for t in tokens if t in prose]
                print(f"[残留] {path}:{i} -> {', '.join(hits)}", file=sys.stderr)
                problems += 1
    return problems


def main():
    ap = argparse.ArgumentParser(description="校验 Markdown 标题层级一致性与样式（只读、确定性）")
    ap.add_argument("--rules", default=DEFAULT_RULES, help="规则文件路径（默认 assets/doc-style-rules.json）")
    ap.add_argument("--check-rules", action="store_true", help="仅自检规则文件结构，必须 0 错误")
    ap.add_argument("paths", nargs="*", help="待校验的 .md 文件或目录（默认当前目录）")
    args = ap.parse_args()

    rules = visible(load_rules(args.rules))
    if args.check_rules:
        return check_rules_schema(rules, args.rules)

    targets = args.paths or ["."]
    total = 0
    for t in targets:
        if os.path.isdir(t):
            for root, _, files in os.walk(t):
                for fn in files:
                    if fn.endswith(".md"):
                        total += scan_file(os.path.join(root, fn), rules)
        elif t.endswith(".md"):
            total += scan_file(t, rules)
        else:
            print(f"[WARN] 跳过非 .md: {t}", file=sys.stderr)

    if total:
        print(f"\n[FAIL] 发现 {total} 处样式问题", file=sys.stderr)
        return 1
    print("[OK] 文档样式与标题层级全部通过", file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main())

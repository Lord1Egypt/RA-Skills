#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""check_links.py — 仓库内 Markdown 相对链接指向的文件真的存在吗？

技能库的说明书互相引用（SKILL.md → playbook、README → docs/QUICKSTART、CHANGELOG → 技能目录）。
改名、拆分、删文件之后，链接会静默变成死链——读者点开是 404，作者却不知道。

本脚本扫所有 Markdown 的 `[文字](路径)` 与 `![图](路径)`：
    - 跳过 http/https/mailto/#anchor 绝对链接（外链不归它管）
    - 相对路径按"引用文件所在目录"解析，存在即通过
    - 允许 `路径#锚点` 形式（只校验文件部分）
只读检查，不改任何文件。

用法：
    python3 tools/check_links.py
    python3 tools/check_links.py -v     # 打印每条通过的链接
"""
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LINK_PAT = re.compile(r"\[[^\]\n]*\]\(([^)\s]+)\)")
FENCE_PAT = re.compile(r"```.*?```", re.S)          # 围栏代码块整体略过
INLINE_CODE_PAT = re.compile(r"`[^`\n]*`")         # 行内代码略过（说明"链接语法怎么写"时不算链接）


def strip_code(text):
    """去掉围栏代码块与行内代码，避免把示例里的假链接当成真链接。"""
    text = FENCE_PAT.sub(lambda m: "\n" * m.group(0).count("\n"), text)
    return INLINE_CODE_PAT.sub(lambda m: " " * len(m.group(0)), text)


def md_files():
    out = []
    for dirpath, _dirs, filenames in os.walk(ROOT):
        if ".git" in dirpath.split(os.sep):
            continue
        for fn in filenames:
            if fn.endswith(".md"):
                out.append(os.path.join(dirpath, fn))
    return sorted(out)


def main():
    verbose = "-v" in sys.argv or "--verbose" in sys.argv
    checked = 0
    bad = []
    for path in md_files():
        base = os.path.dirname(path)
        rel_src = os.path.relpath(path, ROOT)
        with open(path, encoding="utf-8") as f:
            raw_text = f.read()
        for lineno, line in enumerate(strip_code(raw_text).splitlines(), 1):
            if True:
                for raw in LINK_PAT.findall(line):
                    target = raw.strip()
                    if not target or target.startswith(("http://", "https://", "mailto:", "#", "tel:")):
                        continue
                    target = target.split("#", 1)[0]
                    if not target:
                        continue
                    checked += 1
                    resolved = os.path.normpath(os.path.join(base, target))
                    if os.path.exists(resolved):
                        if verbose:
                            print(f"✓ {rel_src}:{lineno} → {target}")
                        continue
                    bad.append((rel_src, lineno, target))
    for src, lineno, target in bad:
        print(f"✗ {src}:{lineno} 死链 → {target}")
    print(f"\n共检查 {checked} 条相对链接，死链 {len(bad)} 条。")
    if bad:
        print("修复方式：改链接指向真实文件，或补上缺的文件（改名后记得全仓 grep 旧名）。")
        return 1
    print("✓ 内部链接全部可达")
    return 0


if __name__ == "__main__":
    sys.exit(main())

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""kb-distiller 三层比例抽验 + 覆盖度 proxy 统计（纯 stdlib，Windows 兼容）。

用法:
    python layer_stats.py <产物目录> [--all]

口径说明:
    - 行数与 validate_skill.py 一致: splitlines() 总行数（含空行）。
    - 法则: 行首 `**XX-n**` 定义行（引用不计）。
    - 场景: `#{2,4} 场景` 标题计数。
    - 坑点: 「坑点」小节内表格数据行（扣除表头/分隔行）。
    - 模板: `#{2,4}` 标题含「模板」计数 + `{{...}}`/`<占位>` 占位符计数。
    - 三层比例 = 法则:场景:坑点行（域内合计）。
    - 覆盖度 proxy: 子域 kb 任一维为 0 → 覆盖缺口候选。

退出码: 0 = 正常输出（proxy 仅供人判，不判失败）。
"""
import argparse
import os
import re
import sys

LAW_DEF = re.compile(r"^(?:\*\*|\[)?[A-Z]+-\d+(?:\*\*|\])?\b")
SCENE_HEAD = re.compile(r"^#{2,4}\s*场景\b")
PITFALL_HEAD = re.compile(r"^##\s*.*坑点")
TEMPLATE_HEAD = re.compile(r"^#{2,4}\s*.*模板\s*\d+|^#{2,4}\s*模板\b")
SECTION_HEAD = re.compile(r"^#{1,4}\s")
H2_HEAD = re.compile(r"^##\s")
TABLE_ROW = re.compile(r"^\|")
TABLE_SEP = re.compile(r"^\|[\s:|-]+\|?$")
PLACEHOLDER = re.compile(r"\{\{[^}]{1,80}\}\}|<待填[^<>]{0,60}>")


def safe_print(text):
    try:
        print(text)
    except UnicodeEncodeError:
        sys.stdout.buffer.write((text + "\n").encode("utf-8", errors="replace"))


def read_text(path):
    with open(path, "r", encoding="utf-8", errors="replace") as f:
        return f.read()


def count_file(path):
    lines = read_text(path).splitlines()
    laws = 0
    scenes = 0
    templates = 0
    pitfalls = 0
    placeholders = 0
    in_pitfall = False
    n = len(lines)
    for i, line in enumerate(lines):
        if SECTION_HEAD.match(line):
            if H2_HEAD.match(line):
                in_pitfall = bool(PITFALL_HEAD.search(line))  # 仅 ## 级切换坑点上下文
            if SCENE_HEAD.match(line):
                scenes += 1
            elif TEMPLATE_HEAD.search(line):
                templates += 1
            continue
        if LAW_DEF.match(line):
            laws += 1
        if in_pitfall and TABLE_ROW.match(line):
            if TABLE_SEP.match(line):
                continue
            nxt = lines[i + 1] if i + 1 < n else ""
            if TABLE_SEP.match(nxt):
                continue  # 表头行（其后紧跟分隔行）
            pitfalls += 1
        placeholders += len(PLACEHOLDER.findall(line))
    return {
        "lines": len(lines),
        "laws": laws,
        "scenes": scenes,
        "pitfalls": pitfalls,
        "templates": templates,
        "placeholders": placeholders,
    }


def main():
    parser = argparse.ArgumentParser(description="三层比例抽验 + 覆盖度 proxy")
    parser.add_argument("target", help="产物目录（含 kb/ 子目录）")
    parser.add_argument("--all", action="store_true", help="纳入横切文件（默认仅列 subdomain kb）")
    args = parser.parse_args()

    kb_dir = os.path.join(args.target, "kb")
    if not os.path.isdir(kb_dir):
        safe_print("错误: 未找到 kb 目录: {}".format(kb_dir))
        return 1
    files = sorted(
        f for f in os.listdir(kb_dir)
        if f.endswith(".md") and (args.all or f not in ("gotchas.md", "laws.md", "ai-mistakes.md", "patterns.md"))
    )

    safe_print("== 三层比例抽验: {} | kb 文件 {} 份 ==".format(args.target, len(files)))
    safe_print("")
    header = "{:<28} {:>6} {:>6} {:>6} {:>8} {:>6} {:>8}".format(
        "文件", "行数", "法则", "场景", "坑点行", "模板", "占位符")
    safe_print(header)
    safe_print("-" * len(header))

    total = {"lines": 0, "laws": 0, "scenes": 0, "pitfalls": 0, "templates": 0, "placeholders": 0}
    gaps = []
    for name in files:
        st = count_file(os.path.join(kb_dir, name))
        for k in total:
            total[k] += st[k]
        safe_print("{:<28} {:>6} {:>6} {:>6} {:>8} {:>6} {:>8}".format(
            name, st["lines"], st["laws"], st["scenes"], st["pitfalls"], st["templates"], st["placeholders"]))
        if not args.all and (st["scenes"] == 0 or st["pitfalls"] == 0):
            gaps.append((name, st["scenes"], st["pitfalls"]))

    safe_print("-" * len(header))
    safe_print("{:<28} {:>6} {:>6} {:>6} {:>8} {:>6} {:>8}".format(
        "合计", total["lines"], total["laws"], total["scenes"], total["pitfalls"], total["templates"], total["placeholders"]))
    safe_print("")
    if total["scenes"] and total["pitfalls"]:
        ratio = "{} : {} : {}".format(
            round(total["laws"] / total["scenes"], 2),
            1,
            round(total["pitfalls"] / total["scenes"], 2),
        )
        safe_print("三层比例（法则:场景:坑点行，场景归一）: {}".format(ratio))
    if gaps:
        safe_print("")
        safe_print("覆盖度 proxy——缺口候选（场景或坑点为 0 的 subdomain kb）:")
        for name, s, p in gaps:
            safe_print("  - {}: 场景 {} / 坑点行 {}".format(name, s, p))
    else:
        safe_print("覆盖度 proxy: subdomain kb 场景/坑点维度无零值缺口。")
    safe_print("")
    safe_print("提示: 比例与计数为抽验 proxy，不设硬阈值；异常偏离（某维为 0 或比例骤变）才需人工复核。")
    return 0


if __name__ == "__main__":
    sys.exit(main())

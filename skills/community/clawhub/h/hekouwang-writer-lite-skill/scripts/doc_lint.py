#!/usr/bin/env python3
"""doc_lint.py — 文档结构体检器（hekouwang-writer-skill）

查三类问题：
  硬错误（退出码 1）：
    - 表格列数不一致：表头/分隔行/数据行的单元格数不相等
    - 标题层级跳跃：如 H1 直接跳 H3
  告警（不阻断）：
    - 分号密度 > 1.5 处/千字（STE：分号是"一句塞两事实"的招牌）
    - 同义词轮换：同一概念多种叫法（--pairs 可补充，默认内置常见组）；
      文档里用 简称/又称/称"X" 声明过的叫法视为合法，不报
    - 重复标题
    - 敏感信息：完整身份证号、手机号（建议脱敏后再转发/打印）
  清点（只报告）：
    - 待核实/待确认/以…为准/暂无出处 的出现处数

用法：
    doc_lint.py FILE [FILE ...]
    doc_lint.py --pairs "经办窗口,社保窗口,政务中心" FILE
    doc_lint.py --json FILE

退出码：有硬错误 = 1；否则 = 0。
"""

import argparse
import json
import re
import sys

CJK_RE = re.compile(r"[\u4e00-\u9fff]")

DEFAULT_PAIR_GROUPS = [
    ("办理地点", ["社保窗口", "政务中心", "经办窗口", "便民服务中心"]),
    ("补差业务", ["提档补差", "升档补差", "补差"]),
]

# 定义行特征：命中则跳过同义词检查（"全文所称X，指……"是定义不是轮换）
DEF_LINE_RE = re.compile(r"所称|系指|指的是|定义为|即指")

MARKER_RE = re.compile(r"待核实|待确认|暂无出处|以.{0,12}为准|建议核实")

# 文档自己声明的叫法：本文简称"补差"、平昌指南称"升档补差"（必须带引号，避免误吞普通"称"字）
ALIAS_RE = re.compile(r"(?:简称|又称|也称|亦称|或称|称为|称)\s*[“\"「『]([^”\"」』\s]{1,12})[”\"」』]")

ID_RE = re.compile(r"(?<![0-9])[1-9]\d{5}(?:19|20)\d{2}(?:0[1-9]|1[0-2])(?:0[1-9]|[12]\d|3[01])\d{3}[0-9Xx](?![0-9])")
MOBILE_RE = re.compile(r"(?<![0-9])1[3-9]\d{9}(?![0-9])")


def split_row(line):
    """按 | 切分表格行，去掉首尾空单元格，返回单元格列表。"""
    s = line.strip()
    if s.startswith("|"):
        s = s[1:]
    if s.endswith("|"):
        s = s[:-1]
    return [c.strip() for c in s.split("|")]


def is_table_line(line):
    return line.strip().startswith("|")


def is_separator(line):
    cells = split_row(line)
    return bool(cells) and all(re.fullmatch(r":?-{2,}:?", c) for c in cells if c != "") and "-" in line


def strip_fences(lines):
    """返回剔除代码围栏内容后的行列表（保留行号占位，用空串填充）。"""
    out = []
    in_fence = False
    for line in lines:
        if line.strip().startswith("```"):
            in_fence = not in_fence
            out.append("")          # 围栏标记行本身也剔除
            continue
        out.append("" if in_fence else line)
    return out


def check_tables(lines):
    """返回硬错误列表（表格列数不一致）。围栏内的示例表格不检查。"""
    errors = []
    lines = strip_fences(lines)
    i, n = 0, len(lines)
    while i < n:
        if is_table_line(lines[i]):
            start = i
            block = []
            while i < n and is_table_line(lines[i]):
                block.append((i + 1, lines[i]))
                i += 1
            header_ln, header = block[0]
            ncol = len(split_row(header))
            for ln, raw in block[1:]:
                cells = split_row(raw)
                # 分隔行允许空（渲染差异），只比非空单元格数
                if is_separator(raw):
                    continue
                if len(cells) != ncol:
                    errors.append(
                        f"L{ln} 表格列数不一致：表头 {ncol} 列，本行 {len(cells)} 列"
                        f"（表头起于 L{header_ln}）")
            if len(block) < 2 or not any(is_separator(raw) for _, raw in block[1:2]):
                errors.append(f"L{header_ln} 表格缺少分隔行（|---|）")
        else:
            i += 1
    return errors


def check_headings(lines):
    """标题层级跳跃 + 重复标题。围栏内的示例标题不检查。"""
    errors, warns = [], []
    seen = {}
    prev_level = 0
    for ln, line in enumerate(strip_fences(lines), 1):
        m = re.match(r"^(#{1,6})\s+(.*)", line)
        if not m:
            continue
        level, title = len(m.group(1)), m.group(2).strip()
        if prev_level and level > prev_level + 1:
            errors.append(f"L{ln} 标题层级跳跃：H{prev_level} → H{level}（{title}）")
        prev_level = level
        seen.setdefault(title, []).append(ln)
    for title, lns in seen.items():
        if len(lns) > 1:
            warns.append(f"重复标题「{title}」出现在 L{'、L'.join(map(str, lns))}")
    return errors, warns


def semicolon_density(text):
    n = len(CJK_RE.findall(text))
    cnt = text.count("；")
    return (cnt / n * 1000) if n else 0.0, cnt


def synonym_check(text, groups):
    """同义词轮换检测。

    两条防误报规则：
    1. 子串重叠：短词是长词的一部分时（补差 ⊂ 提档补差），
       只统计不被任何更长变体覆盖的独立出现；
    2. 定义行豁免：含"所称/系指/指的是"等定义标记的行跳过——
       那是给术语下定义，不是轮换。
    """
    warns = []
    aliases = set(ALIAS_RE.findall(text))
    for concept, variants in groups:
        # 按长度降序，长词优先占位
        ordered = sorted(variants, key=len, reverse=True)
        claimed = []  # 已被更长变体覆盖的 (start, end) 区间
        counts = {}
        for v in ordered:
            n = 0
            for m in re.finditer(re.escape(v), text):
                s, e = m.span()
                if any(cs <= s < ce or cs < e <= ce for cs, ce in claimed):
                    continue  # 落在更长变体内，跳过
                # 定义行豁免
                ln_start = text.rfind("\n", 0, s) + 1
                ln_end = text.find("\n", e)
                line = text[ln_start: ln_end if ln_end != -1 else len(text)]
                if DEF_LINE_RE.search(line):
                    continue
                claimed.append((s, e))
                n += 1
            if n:
                counts[v] = n
        undeclared = {k: v for k, v in counts.items() if k not in aliases}
        if len(counts) > 1 and len(undeclared) > 1:
            detail = "、".join(f"{k}×{v}" for k, v in counts.items())
            warns.append(f"同义词轮换·{concept}：{detail}（建议统一为一种叫法；"
                         f"若某变体仅出现在引用/文件名称中，可人工放行；"
                         f"或在术语表写明 简称\"X\"）")
    return warns


def sensitive_check(text):
    """完整身份证号、手机号。已打码（含 *）的不会命中。"""
    warns = []
    for ln, line in enumerate(text.splitlines(), 1):
        for m in ID_RE.finditer(line):
            v = m.group()
            warns.append(f"L{ln} 疑似完整身份证号 {v[:6]}********{v[-4:]}（建议只留后4位）")
        for m in MOBILE_RE.finditer(line):
            v = m.group()
            warns.append(f"L{ln} 疑似手机号 {v[:3]}****{v[-4:]}（转发前确认是否需要打码）")
    return warns


def selftest():
    """内置自测：表格错列/标题跳级是硬错误；围栏内不查；同义词只告警。"""
    cases = [
        ("表格错列", "| 甲 | 乙 |\n|---|---|\n| 1 | 2 |\n| 3 |\n", True),
        ("表格对齐", "| 甲 | 乙 |\n|---|---|\n| 1 | 2 |\n", False),
        ("标题跳级", "# 一级\n\n### 三级\n", True),
        ("标题递进", "# 一级\n\n## 二级\n", False),
        ("围栏不查", "```\n| 甲 | 乙 |\n| 1 |\n```\n", False),
        ("缺分隔行", "| 甲 | 乙 |\n| 1 | 2 |\n", True),
        ("无尾管道错列", "| 甲 | 乙 |\n|---|---|\n| 1 | 2\n| 3\n", True),
        ("无尾管道对齐", "| 甲 | 乙\n|---|---\n| 1 | 2\n", False),
    ]
    ok = True
    for name, text, expect_hard in cases:
        lines = text.splitlines()
        errs = check_tables(lines) + check_headings(lines)[0]
        got = bool(errs)
        good = got == expect_hard
        ok = ok and good
        print(f"  [{'PASS' if good else 'FAIL'}] {name}"
              f"（期望硬错误 {expect_hard}，实际 {got}）")

    groups = DEFAULT_PAIR_GROUPS
    warn_cases = [
        ("同义词轮换", "先办提档补差。再办补差。", synonym_check, True),
        ("声明过的简称", "提档补差（本文简称\"补差\"）。再办补差。", synonym_check, False),
        ("引用别称", "提档补差。指南称“升档补差”。", synonym_check, False),
        ("完整身份证号", "号码 110105199001011234", None, True),
        ("打码身份证号", "号码 110105********1234", None, False),
        ("手机号", "电话 13812345678", None, True),
        ("座机不算手机", "电话 0827-3369682", None, False),
    ]
    for name, text, fn, expect in warn_cases:
        got = bool(fn(text, groups) if fn else sensitive_check(text))
        good = got == expect
        ok = ok and good
        print(f"  [{'PASS' if good else 'FAIL'}] {name}（期望告警 {expect}，实际 {got}）")
    print("selftest:", "全部通过" if ok else "有失败项")
    return 0 if ok else 1


def main(argv=None):
    ap = argparse.ArgumentParser(description="文档结构体检（表格/标题/分号/同义词）")
    ap.add_argument("files", nargs="*", help="待检查文件；省略时读 stdin")
    ap.add_argument("--pairs", action="append", default=[],
                    help='追加同义词组，格式 "概念:词1,词2,词3"，可多次')
    ap.add_argument("--json", action="store_true", help="JSON 输出")
    ap.add_argument("--selftest", action="store_true", help="运行内置自测")
    args = ap.parse_args(argv)

    if args.selftest:
        return selftest()

    groups = [list(g) for g in DEFAULT_PAIR_GROUPS]
    for p in args.pairs:
        if ":" in p:
            concept, words = p.split(":", 1)
            groups.append((concept.strip(), [w.strip() for w in words.split(",") if w.strip()]))

    texts = []
    if args.files:
        for f in args.files:
            try:
                with open(f, encoding="utf-8") as fh:
                    texts.append((f, fh.read()))
            except OSError as e:
                print(f"读取失败：{f}（{e}）", file=sys.stderr)
                return 2
    else:
        texts.append(("<stdin>", sys.stdin.read()))

    any_hard = False
    all_results = []
    for path, text in texts:
        lines = text.splitlines()
        hard = check_tables(lines)
        h_errors, h_warns = check_headings(lines)
        hard.extend(h_errors)
        density, cnt = semicolon_density(text)
        syn = synonym_check(text, groups)
        markers = MARKER_RE.findall(text)

        if hard:
            any_hard = True

        res = {
            "path": path,
            "hard_errors": hard,
            "warnings": h_warns + syn + sensitive_check(text) +
                        ([f"分号密度 {density:.2f} 处/千字（>1.5）" ] if density > 1.5 else []),
            "semicolon_count": cnt,
            "semicolon_density": round(density, 2),
            "pending_markers": len(markers),
        }
        all_results.append(res)

        if not args.json:
            print(f"文件：{path}")
            print(f"分号：{cnt} 处（密度 {density:.2f}/千字）    待核实类标记：{len(markers)} 处")
            if hard:
                print("【硬错误】")
                for e in hard:
                    print("  ✗ " + e)
            if res["warnings"]:
                print("【告警】")
                for w in res["warnings"]:
                    print("  ! " + w)
            if not hard and not res["warnings"]:
                print("✅ 无硬错误、无告警。")
            print()

    if args.json:
        print(json.dumps(all_results if len(all_results) > 1 else all_results[0],
                         ensure_ascii=False, indent=2))
    return 1 if any_hard else 0


if __name__ == "__main__":
    sys.exit(main())

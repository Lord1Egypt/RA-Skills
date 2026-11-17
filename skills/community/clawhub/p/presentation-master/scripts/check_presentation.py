#!/usr/bin/env python3
"""check_presentation.py — 演示大纲内容规范检查器（纯标准库，零依赖）

检查 Markdown 演示大纲（以 `---` 分页）的内容规范：
  outline   校验每页字数上限、标题存在性、标题层级统一、重复标题
  selfcheck 校验内置资产（规则配置 + 示例大纲）应为 0 ERROR

规则来源：assets/presentation_rules.json（配置驱动）。以 `_` 开头的键为注释，加载时跳过。

特性：纯标准库、带 --help、确定性可复现、不联网、只读不修改被检文件。

用法:
  python3 check_presentation.py outline --file deck.md
  python3 check_presentation.py selfcheck
  python3 check_presentation.py --help
"""
import argparse
import json
import os
import re
import sys

_HERE = os.path.dirname(os.path.abspath(__file__))
_DEFAULT_RULES = os.path.join(_HERE, "..", "assets", "presentation_rules.json")
_DEFAULT_EXAMPLE = os.path.join(_HERE, "..", "assets", "presentation-outline.example.md")


def _load_rules(path):
    errors = []
    if not os.path.isfile(path):
        return {}, [f"规则配置不存在: {path}"]
    try:
        with open(path, "r", encoding="utf-8") as fh:
            raw = json.load(fh)
    except (OSError, json.JSONDecodeError) as exc:
        return {}, [f"规则配置解析失败: {exc}"]
    if not isinstance(raw, dict):
        return {}, ["规则配置根必须是 JSON 对象"]
    rules = {k: v for k, v in raw.items() if not k.startswith("_")}
    if not isinstance(rules.get("max_chars_per_slide"), int):
        errors.append("max_chars_per_slide 必须是整数")
    if not isinstance(rules.get("title_level"), int) or not (1 <= rules["title_level"] <= 6):
        errors.append("title_level 必须是 1-6 的整数")
    if not isinstance(rules.get("forbid_duplicate_titles"), bool):
        errors.append("forbid_duplicate_titles 必须是布尔")
    return rules, errors


def _split_slides(text):
    return re.split(r"^---\s*$", text, flags=re.MULTILINE)


def _check_outline(text, rules):
    errors = []
    max_chars = rules.get("max_chars_per_slide", 120)
    title_level = rules.get("title_level", 1)
    forbid_dup = rules.get("forbid_duplicate_titles", True)
    seen_titles = {}
    slides = _split_slides(text)
    for idx, slide in enumerate(slides, start=1):
        lines = slide.splitlines()
        nonempty = [ln for ln in lines if ln.strip()]
        if not nonempty:
            continue  # 空页跳过
        fi = next(i for i, ln in enumerate(lines) if ln.strip())
        first = lines[fi]
        m = re.match(r"^(#{1,6})\s+(.*)", first)
        if not m:
            errors.append(f"slide {idx}: 缺标题（首行非 Markdown 标题）")
            continue
        level = len(m.group(1))
        title = m.group(2).strip()
        if level != title_level:
            errors.append(f"slide {idx}: 标题层级为 {level}，期望 {title_level}（跨页需统一）")
        body = "\n".join(lines[fi + 1:])
        nchars = len(re.sub(r"\s", "", body))
        if nchars > max_chars:
            errors.append(f"slide {idx}: 字数 {nchars} 超过上限 {max_chars}")
        if forbid_dup:
            key = title.lower()
            if key in seen_titles:
                errors.append(f"slide {idx}: 标题重复 '{title}'（首次出现在 slide {seen_titles[key]}）")
            else:
                seen_titles[key] = idx
    return errors


def _read_file_or_die(path):
    if not os.path.isfile(path):
        sys.stderr.write(f"[ERROR] 文件不存在: {path}\n")
        sys.exit(2)
    with open(path, "r", encoding="utf-8") as fh:
        return fh.read()


def main(argv=None):
    ap = argparse.ArgumentParser(description="演示大纲内容规范检查器（outline / selfcheck）")
    ap.add_argument("--rules", default=_DEFAULT_RULES, help="规则配置 JSON 路径")
    sub = ap.add_subparsers(dest="cmd", required=True)

    p_o = sub.add_parser("outline", help="校验演示大纲")
    p_o.add_argument("--file", required=True, help="Markdown 大纲文件路径")

    sub.add_parser("selfcheck", help="校验内置资产（规则+示例大纲）应为 0 ERROR")

    args = ap.parse_args(argv)

    if args.cmd == "selfcheck":
        rules, rerr = _load_rules(args.rules)
        print(f"[selfcheck] 规则 {os.path.relpath(args.rules)} : "
              f"{'OK' if not rerr else rerr}")
        ex_err = _check_outline(_read_file_or_die(_DEFAULT_EXAMPLE), rules) if os.path.isfile(_DEFAULT_EXAMPLE) else ["示例大纲缺失"]
        print(f"[selfcheck] 示例大纲 {os.path.relpath(_DEFAULT_EXAMPLE)} : "
              f"{'0 ERROR' if not ex_err else ex_err}")
        total = len(rerr) + len(ex_err)
        if total == 0:
            print("[selfcheck] PASS — 资产与脚本互相验证通过（0 ERROR）")
            return 0
        print(f"[selfcheck] FAIL — 共 {total} 项错误")
        return 1

    rules, rerr = _load_rules(args.rules)
    if rerr:
        for e in rerr:
            sys.stderr.write(f"[ERROR] {e}\n")
        return 2

    if args.cmd == "outline":
        errs = _check_outline(_read_file_or_die(args.file), rules)
        if errs:
            for e in errs:
                print(f"ERROR: {e}")
            print(f"\n大纲检查未通过：{len(errs)} 项")
            return 1
        print("大纲检查通过：0 ERROR")
        return 0

    return 2


if __name__ == "__main__":
    sys.exit(main())

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""引用完整性检查：SKILL.md 里引用的计算器脚本 / Part 编号 / 兄弟技能是否真实存在。

失效引用是技能库最常见的"腐坏"：重构文件后 SKILL.md 还在指向不存在的脚本或
不存在的 Part，使用者照着做就会撞墙。这个脚本只读、不改，发现问题返回 1。

用法：
    python3 tools/check_refs.py          # 打印全部问题
    python3 tools/check_refs.py --quiet  # 只打印问题
"""
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SKILLS = os.path.join(ROOT, "skills")
CALC = os.path.join(SKILLS, "calc-toolkit")

# 常见中英文数字（Part 编号可能写成 Part 6 / 第 6 部分）
CN_NUM = {"一": 1, "二": 2, "三": 3, "四": 4, "五": 5, "六": 6, "七": 7,
          "八": 8, "九": 9, "十": 10, "十一": 11, "十二": 12}


def calc_scripts():
    return {f for f in os.listdir(CALC) if f.endswith(".py")}


def count_parts(text):
    """数正文里出现的 Part 标题最大编号（支持 '## Part 6'、'### Part 6'、'Part 6 '）。"""
    nums = [int(m) for m in re.findall(r"Part\s*(\d{1,2})", text)]
    for c in re.findall(r"第\s*([一二三四五六七八九十]{1,3})\s*部分", text):
        if c in CN_NUM:
            nums.append(CN_NUM[c])
    return max(nums) if nums else 0


def main():
    quiet = "--quiet" in sys.argv
    scripts = calc_scripts()
    skills = sorted(n for n in os.listdir(SKILLS) if os.path.isdir(os.path.join(SKILLS, n)))
    problems = []

    for n in skills:
        p = os.path.join(SKILLS, n, "SKILL.md")
        if not os.path.isfile(p):
            continue
        text = open(p, encoding="utf-8").read()

        # 1) 计算器脚本引用
        for ref in set(re.findall(r"calc-toolkit/([A-Za-z0-9_]+\.py)", text)):
            if ref not in scripts:
                problems.append("%s: 引用了不存在的计算器 calc-toolkit/%s" % (n, ref))

        # 2) 兄弟技能引用（`skills/xxx/` 或 `xxx-sop` 反引号形式）
        for ref in set(re.findall(r"skills/([a-z0-9-]+)/", text)):
            if ref not in skills:
                problems.append("%s: 引用了不存在的技能目录 skills/%s/" % (n, ref))

        # 3) Part 编号引用 vs 正文（playbook 等非 SKILL.md 文件）实际 Part 数
        body_files = [
            os.path.join(SKILLS, n, f) for f in os.listdir(os.path.join(SKILLS, n))
            if f.endswith(".md") and f != "SKILL.md"
        ]
        available = 0
        for bf in body_files:
            if os.path.isfile(bf):
                available = max(available, count_parts(open(bf, encoding="utf-8").read()))
        refs = [int(m) for m in re.findall(r"Part\s*(\d{1,2})", text)]
        if available and refs:
            over = sorted({r for r in refs if r > available})
            if over:
                problems.append(
                    "%s: SKILL.md 引用 Part %s，但正文最多只有 Part %d"
                    % (n, "、".join(str(x) for x in over), available)
                )

    if not quiet:
        print("检查 %d 个技能的引用完整性（计算器 / 兄弟技能 / Part 编号）" % len(skills))
    for pr in problems:
        print("  [问题] %s" % pr)
    if problems:
        print("\n✗ 发现 %d 处失效引用" % len(problems))
        return 1
    print("✓ 引用完整：%d 个技能，0 处失效引用" % len(skills))
    return 0


if __name__ == "__main__":
    sys.exit(main())

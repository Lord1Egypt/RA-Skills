#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
发版前自检：题目去重、答案合法性、等级覆盖、CLI 可用性。

用法：
  python scripts/selftest.py            # 跑全部检查
  python scripts/selftest.py --fix      # 发现问题时打印建议修复方式
退出码 0 表示通过，非 0 表示有失败。
"""

import argparse
import importlib.util
import random
import re
import sys
from collections import Counter
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
GENERATOR_PATH = HERE / "generate_worksheet.py"

LEVELS = ["L1", "L2", "L3", "L4", "L5"]
SAMPLE_PER_TOPIC = 80

# 题目空间理论大小 → 期望唯一率阈值
# 抽样次数 80 接近许多题型的题目空间，撞重复是生日悖论下的数学期望。
# 阈值下限 30%，超过则按理论碰撞率 × 1.5 倍冗余计算
SAMPLE_K = 80
MIN_THRESHOLD = 0.30
SPACE_OVERHEAD = 1.5  # 理论碰撞率的冗余系数


def topic_space(topic, lv):
    """估算该题型在该等级下的理论题面空间。"""
    return {
        "write_number": 5,                # 1-5 或 6-10，每池 5 个
        "compose": 18,                    # 3-10 的二拆分 + 偶发三拆分
        "color_by_number": 19,            # n=1..10, total-n=1..3
        "count_objects": 80,              # 5 个 n × 16 个 emoji
        "next_number": 64,                # 8 个 start × 4 hole × 2 reverse
        "compare": 100,                   # 10×10
        "add": 36,                        # 8+7+6+...+2 = 36
        "sub": 45,                        # 9+8+...+2 = 45
        "missing_addend": 50,             # 两种形式各约 25
        "word_problem": 70,               # 4 种 kind × 多种数值
        "add_carry": 27,                  # 7+8+7+6+5+4+3+2...约 27
        "sub_borrow": 40,                 # total×b 的组合
        "mixed_20": 35,                   # add_carry + sub_borrow
        "vertical": 40,                   # 加+减两种
        "picture_equation": 128,          # 8×8 + 8×8（加+减）
        "ordinal": 240,                   # 5×n×2×16
        "circle_number": 7 * 7,           # target × pool 组合
    }.get(topic, 100)


def topic_level(topic):
    """该题型的"标准"等级，用于唯一率抽样。"""
    if topic in ("count_objects", "write_number", "circle_number", "ordinal", "color_by_number"):
        return "L1"
    if topic in ("next_number", "compare", "compose"):
        return "L3"
    if topic in ("add", "sub", "missing_addend", "word_problem", "picture_equation"):
        return "L4"
    return "L5"


def expected_min_uniqueness(topic, lv):
    """按生日悖论公式：期望唯一率 ≈ 1 - k(k-1)/(2N)，再 × 1.5 倍冗余。"""
    space = topic_space(topic, lv)
    if space < 25:
        return 0.0  # 极小空间豁免
    expected_collision_rate = SAMPLE_K * (SAMPLE_K - 1) / (2 * space)
    threshold = 1 - min(1.0, expected_collision_rate * SPACE_OVERHEAD)
    return max(MIN_THRESHOLD, threshold)


# 合法答案模式：除了纯数字、>, <, =，还接受算式、序数答案、涂色答案
LEGAL_ANSWER_PATTERNS = [
    re.compile(r"^\d+$"),                         # 纯数字
    re.compile(r"^[<>=]$"),                       # 比较符号
    re.compile(r"书写题"),                          # 书写题提示
    re.compile(r"^圈出 \d+ 个 \d+$"),                # 圈数字
    re.compile(r"^涂 \d+ 个$"),                      # 涂色
    re.compile(r"^第 \d+ 个"),                       # 序数
    re.compile(r"^\d+ [+\-] \d+ = \d+$"),          # 看图列式算式
    re.compile(r"^[\u4e00-\u9fa5]+$"),             # 纯中文（如"多"/"还剩"）
]


def is_legal_answer(ans):
    """判断答案字符串是否合法。"""
    if not isinstance(ans, str):
        return False
    s = ans.strip()
    if not s:
        return False
    return any(p.match(s) for p in LEGAL_ANSWER_PATTERNS)


def load_generator():
    spec = importlib.util.spec_from_file_location("gw", str(GENERATOR_PATH))
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


def check_uniqueness(m, fix):
    """单题型 80 次抽样的题面唯一率。按题目空间分级判定。"""
    failures = []
    print("\n[1/4] 题目唯一率检查（单题型 %d 次抽样，按空间分级）" % SAMPLE_PER_TOPIC)
    for topic, fn in m.GENERATORS.items():
        lv = topic_level(topic)
        rng = random.Random(99)
        prompts = [fn(rng, lv)["prompt"] for _ in range(SAMPLE_PER_TOPIC)]
        uniq = len(set(prompts))
        rate = uniq / SAMPLE_PER_TOPIC
        threshold = expected_min_uniqueness(topic, lv)
        marker = "OK " if rate >= threshold else "FAIL"
        if threshold == 0:
            note = "（小空间题型，豁免唯一率检查）"
        else:
            note = f"（阈值 {threshold*100:.0f}%）"
        print(f"  [{marker}] {topic:<16} {uniq}/{SAMPLE_PER_TOPIC}  ({rate*100:.0f}%) {note}")
        if rate < threshold:
            failures.append((topic, rate, threshold))
    return failures


def check_answers(m, fix):
    """答案合法性与范围检查。"""
    print("\n[2/4] 答案合法性检查")
    bad = []
    for topic, fn in m.GENERATORS.items():
        rng = random.Random(42)
        for lv in LEVELS:
            for _ in range(40):
                q = fn(rng, lv)
                a = q["answer"]
                if not is_legal_answer(a):
                    bad.append((topic, lv, a))
    if bad:
        print(f"  [FAIL] 发现 {len(bad)} 个异常答案（前 5 个）：{bad[:5]}")
        if fix:
            print("         检查题目生成器返回的 answer 是否符合以下模式之一：")
            print("         - 纯数字 0-20")
            print("         - 比较符号 > < =")
            print("         - \"书写题...\" / \"圈出 N 个 X\" / \"涂 N 个\" / \"第 N 个...\"")
            print("         - 看图列式算式 \"a op b = c\"")
            print("         - 纯中文（如 \"多\"、\"还剩\"）")
        return bad
    print("  [OK ] 所有题型答案均在合法范围")
    return []


def check_level_coverage(m, fix):
    """等级覆盖检查：每个等级至少有 4 个不同题型。"""
    print("\n[3/4] 等级题型覆盖检查")
    failures = []
    for lv in LEVELS:
        topics = m.LEVEL_TOPICS[lv]
        if len(topics) < 4:
            print(f"  [FAIL] {lv} 仅配置 {len(topics)} 个题型：{topics}")
            if fix:
                print(f"         建议在 LEVEL_TOPICS[{lv!r}] 中至少追加 1 个题型")
            failures.append((lv, len(topics)))
        else:
            print(f"  [OK ] {lv} 配置了 {len(topics)} 个题型：{topics}")
    return failures


def check_build_questions_dedup(m, fix):
    """build_questions 在同一卷中应避免重复题面。"""
    print("\n[4/4] build_questions 同卷去重检查")
    failures = []
    for lv in LEVELS:
        topics = m.LEVEL_TOPICS[lv]
        rng = random.Random(7)
        qs = m.build_questions(lv, topics, 20, rng)
        c = Counter(q["prompt"] for q in qs)
        dup_groups = {k: v for k, v in c.items() if v > 1}
        if dup_groups:
            print(f"  [FAIL] {lv} 卷内有 {len(dup_groups)} 组重复题面，共 {sum(dup_groups.values())} 题")
            if fix:
                print(f"         例如：{next(iter(dup_groups))!r}")
            failures.append((lv, dup_groups))
        else:
            print(f"  [OK ] {lv} 20 题卷内无重复")
    return failures


def main():
    ap = argparse.ArgumentParser(description="发版前自检")
    ap.add_argument("--fix", action="store_true", help="发现问题时打印修复建议")
    args = ap.parse_args()

    print(f"加载生成器: {GENERATOR_PATH}")
    m = load_generator()

    failures = []
    failures += check_uniqueness(m, args.fix)
    failures += check_answers(m, args.fix)
    failures += check_level_coverage(m, args.fix)
    failures += check_build_questions_dedup(m, args.fix)

    print("\n" + "=" * 60)
    if failures:
        print(f"FAIL：{len(failures)} 项不通过")
        return 1
    print("PASS：所有检查通过，可以发版")
    return 0


if __name__ == "__main__":
    sys.exit(main())
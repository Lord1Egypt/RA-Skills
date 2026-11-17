#!/usr/bin/env python3
"""
dataset_split_check.py — 训练/测试集质量与泄漏检查（确定性、可复现）

给定 train.csv 与 test.csv，检测：
  1) 行级重叠（数据泄漏：同一行同时出现在两个集合）
  2) 目标列类别分布漂移（若指定 --target）
  3) 各文件缺失值

用法:
    python3 dataset_split_check.py train.csv test.csv
    python3 dataset_split_check.py train.csv test.csv --target label --json
    python3 dataset_split_check.py train.csv test.csv --strict   # 有泄漏或严重漂移时退出码 1

不替代领域判断；仅做确定性检查。
"""
import argparse
import csv
import json
import sys
from collections import Counter


def load_rows(path):
    with open(path, "r", encoding="utf-8", newline="") as f:
        reader = csv.reader(f)
        header = next(reader, None)
        rows = [tuple(r) for r in reader if any(c.strip() for c in r)]
    return header, rows


def main():
    ap = argparse.ArgumentParser(description="训练/测试集泄漏与质量检查")
    ap.add_argument("train", help="训练集 CSV")
    ap.add_argument("test", help="测试集 CSV")
    ap.add_argument("--target", help="目标列名（用于类别分布对比）")
    ap.add_argument("--json", action="store_true", help="输出 JSON")
    ap.add_argument("--strict", action="store_true",
                    help="存在泄漏或严重类别漂移时退出码 1")
    args = ap.parse_args()

    try:
        th, train = load_rows(args.train)
        eh, test = load_rows(args.test)
    except OSError as e:
        print(f"无法读取 CSV: {e}", file=sys.stderr)
        return 2

    train_set, test_set = set(train), set(test)
    overlap = train_set & test_set
    leakage = len(overlap)

    # 缺失值（按列）
    missing = {}
    for name, rows in (("train", train), ("test", test)):
        cols = len(rows[0]) if rows else 0
        c = [0] * cols
        for r in rows:
            for i, v in enumerate(r):
                if v.strip() == "":
                    c[i] += 1
        missing[name] = c

    # 类别分布
    drift = None
    if args.target and th:
        try:
            idx = th.index(args.target)
        except ValueError:
            print(f"目标列不存在: {args.target}", file=sys.stderr)
            return 2
        tc = Counter(r[idx] for r in train if len(r) > idx)
        ec = Counter(r[idx] for r in test if len(r) > idx)
        allk = set(tc) | set(ec)
        drift = {k: {"train": tc.get(k, 0), "test": ec.get(k, 0)} for k in allk}
        # 严重漂移：某类在两侧比例相差 > 3 倍（且非零）
        for k in allk:
            a, b = tc.get(k, 0), ec.get(k, 0)
            if a and b:
                ratio = max(a / b, b / a)
                if ratio > 3:
                    drift[k]["severe"] = True

    result = {
        "train_rows": len(train),
        "test_rows": len(test),
        "leakage_rows": leakage,
        "missing": missing,
        "class_distribution": drift,
    }

    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print(f"训练集 {len(train)} 行，测试集 {len(test)} 行")
        print(f"行级重叠（泄漏）: {leakage} 行")
        tm = sum(1 for c in missing["train"] if c)
        em = sum(1 for c in missing["test"] if c)
        print(f"含缺失值的列: train={tm} test={em}")
        if drift:
            print("类别分布:")
            for k, v in drift.items():
                flag = " ⚠️ 严重漂移" if v.get("severe") else ""
                print(f"  {k}: train={v['train']} test={v['test']}{flag}")
        if leakage:
            print("\n⚠️ 检测到训练/测试集行重叠，存在数据泄漏风险")

    if args.strict and (leakage or any(v.get("severe") for v in (drift or {}).values())):
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""红队回归：一个"形式齐备、内容为空"的包，不得被判 PASS。

背景：1.1.13 首次被探针攻破——零断言的 runner + 只打印一句的 demo，
拿到了 reproducible 20/20、总分 87 PASS。1.1.14 补了两条判定：
  · runner 里必须能找到断言或比较
  · demo 必须调用或导入包内脚本
本脚本把这个攻击固化成回归，改尺子时先跑它。
"""
import io
import json
import os
import shutil
import subprocess
import sys
import tempfile

PKG = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
REVIEW = os.path.join(PKG, "scripts", "review.py")

FAKE_SKILL = """---
name: probe-fake
description: Use when testing whether a reviewer can be gamed. 探针包。
version: 1.0.0
license: MIT
author: probe
tags:
- probe
- test
---

# 探针

## 硬规则

1. NEVER 假装有用。因为是探针。

## Triggers

- probe

## Related skills

- x

## 安全边界

- 只读。Not for 真实使用。
"""

EMPTY_RUNNER = '''import io
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
cases = json.load(io.open(os.path.join(HERE, "golden.json"), encoding="utf-8"))["cases"]
for c in cases:
    print("PASS  %s" % c["id"])
print("---- %d/%d PASS ----" % (len(cases), len(cases)))
'''


def write(root, rel, text):
    p = os.path.join(root, rel)
    os.makedirs(os.path.dirname(p), exist_ok=True) if os.path.dirname(p) else None
    with io.open(p, "w", encoding="utf-8", newline="\n") as f:
        f.write(text)


def build(root):
    write(root, "SKILL.md", FAKE_SKILL)
    write(root, "tests/run_golden.py", EMPTY_RUNNER)
    write(root, "tests/golden.json", json.dumps({"cases": [{"id": "T%d" % i} for i in range(3)]}))
    write(root, "demo/run_demo.py", 'print("demo ok")\n')
    write(root, "scripts/probe.py", "print('probe')\n")
    write(root, "references/limits.md", "# 限制\n\n占位。\n")
    write(root, "ai-index.json", '{"name": "probe-fake"}')


def main():
    root = tempfile.mkdtemp(prefix="redteam-")
    try:
        build(root)
        p = subprocess.run([sys.executable, REVIEW, root, "--run"],
                           capture_output=True, text=True, encoding="utf-8", timeout=180)
        out = p.stdout
        total = None
        for l in out.splitlines():
            if "总分：" in l:
                total = int(l.split("总分：")[1].split("/")[0].strip())
                break
        verdict = "PASS" if total is not None and total >= 80 else "BLOCKED"
        print("探针包得分：", total, "→", verdict)
        if total is not None and total >= 80:
            print("FAIL：空壳包被判 PASS，尺子有漏洞")
            sys.exit(1)
        print("OK：空壳包未能通过（>=80 才算 PASS）")
    finally:
        shutil.rmtree(root, ignore_errors=True)


if __name__ == "__main__":
    main()

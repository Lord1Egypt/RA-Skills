#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""评测器自检：证明 review.py 既会放过好包，也会拦住坏包。

用例全部在临时目录构造，不改动本包。
"""
import io
import json
import os
import shutil
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, ".."))
sys.path.insert(0, os.path.join(ROOT, "scripts"))
import review as rv  # noqa: E402

KEY = "sk-" + "B" * 24

GOOD = """---
name: good-pkg
display_name: 好包
display_name_en: good-pkg
slug: good-pkg
author: 测试
version: 1.0.0
license: MIT
category: developer-tools
description: "A good package. Faithful: no invented claim."
description_zh: "好包"
description_en: "A good package."
tags:
  - a
  - b
  - c
---

# good-pkg

## Triggers
触发词

## 安全边界
只读。

## Sibling skills in the same ecosystem (LGD)
同系列技能（LGD 生态）：summarize-pro、debug-pro、wechat-viral-topic、lgd-skill-review。
"""


def write(p, s):
    os.makedirs(os.path.dirname(p), exist_ok=True)
    io.open(p, "w", encoding="utf-8", newline="\n").write(s)


def mk_good(d):
    md = GOOD.replace("## Triggers",
                      "## 用法\n\n```bash\npython scripts/tool.py run --file x.md\n```\n\n## Triggers")
    write(os.path.join(d, "SKILL.md"), md)
    write(os.path.join(d, "scripts", "tool.py"),
          'import argparse\np=argparse.ArgumentParser()\ns=p.add_subparsers(dest="c", required=True)\n'
          'r=s.add_parser("run")\nr.add_argument("--file", required=True)\np.parse_args()\n')
    write(os.path.join(d, "tests", "golden.json"), '{"cases":[{"id":"a"}]}')
    write(os.path.join(d, "tests", "run_golden.py"), "import sys\nprint('ok')\nsys.exit(0)\n")
    write(os.path.join(d, "demo", "run_demo.py"), "print('demo')\n")
    write(os.path.join(d, "ai-index.json"), '{"schema":"x"}')
    write(os.path.join(d, "llms.txt"), "# x\n")
    write(os.path.join(d, "LICENSE"), "MIT\n")


def check(case):
    base = tempfile.mkdtemp(prefix="lgd_t_")
    d = os.path.join(base, "pkg")
    try:
        kind = case["kind"]
        if kind == "no_skill_md":
            os.makedirs(d, exist_ok=True)
        elif kind in ("good", "secret", "declared"):
            mk_good(d)
        elif kind == "self":
            d = ROOT
        if kind == "secret":
            write(os.path.join(d, "SKILL.md"), GOOD + '\nkey: "%s"\n' % KEY)
        if kind == "declared":
            write(os.path.join(d, "SKILL.md"), GOOD + "\n用本技能的子命令：\npython scripts/t.py run --draft\n")
            write(os.path.join(d, "scripts", "t.py"),
                  'import argparse\np=argparse.ArgumentParser()\ns=p.add_subparsers(dest="c")\n'
                  'r=s.add_parser("run")\nr.add_argument("--file")\np.parse_args()\n')
        res = rv.review(d, do_run=False)
        if not res.get("ok"):
            return ("BLOCK" if res.get("error_id") == "R001" else "FAIL"), res
        return res["data"]["verdict"], res["data"]
    finally:
        if case["kind"] != "self":
            shutil.rmtree(base, ignore_errors=True)


def main():
    d = json.load(io.open(os.path.join(HERE, "golden.json"), encoding="utf-8"))
    total, passed = 0, 0
    for c in d["cases"]:
        total += 1
        verdict, data = check(c)
        exp = c["expect"]
        ok = True
        if "verdict" in exp and verdict != exp["verdict"]:
            ok = False
        if "total_min" in exp and (not isinstance(data, dict) or data.get("total", 0) < exp["total_min"]):
            ok = False
        if "blocking_contains" in exp:
            blk = " ".join(data.get("blocking", [])) if isinstance(data, dict) else ""
            if exp["blocking_contains"] not in blk:
                ok = False
        score = data.get("total") if isinstance(data, dict) else "-"
        print("%s %-38s verdict=%-5s total=%s" % ("PASS" if ok else "FAIL", c["id"], verdict, score))
        passed += ok
    print("---- %d/%d PASS ----" % (passed, total))
    sys.exit(0 if passed == total else 1)


if __name__ == "__main__":
    main()

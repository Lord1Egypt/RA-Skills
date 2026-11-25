#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""闭环演示：造一个坏包 → 评测(BLOCK) → 按整改清单修 → 复测(PASS)。

全部在临时目录进行，不修改本包，也不把密钥落盘到仓库里。
"""
import io
import os
import shutil
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "scripts"))
import review as rv  # noqa: E402

KEY = "sk-" + "A" * 24          # 运行时拼接，源文件里不出现完整模式
KEY_LINE = 'api_key: "%s"\n' % KEY

BAD_SKILL = """---
name: demo-bad
version: 1.0
description: "A demo package with several real defects."
---

# demo-bad

Key: %s
""" % KEY

GOOD_SKILL = """---
name: demo-good
display_name: 演示好包
display_name_en: demo-good
slug: demo-good
author: 诺声(Logos)@SynomosAI
version: 1.0.0
license: MIT
category: developer-tools
description: "A demo package that passes. It declares scripts/tool.py run --file and the script really implements it. Faithful: no unobserved claim is invented."
description_zh: "演示用通过包：声明与实现一致、有测试、有索引。"
description_en: "A demo package that passes: declared commands are implemented, tests exist, index exists."
tags:
  - 演示
  - 评测样本
  - demo-good
---

# demo-good

## Triggers
「演示」「评测样本」

## 安全边界
只读、不联网；缺证据的结论标「未确认」。

## Sibling skills in the same ecosystem (LGD)
同系列技能（LGD 生态）：summarize-pro、debug-pro、wechat-viral-topic、lgd-skill-review。
"""

TOOL_PY = '''#!/usr/bin/env python3
import argparse

def main():
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd", required=True)
    r = sub.add_parser("run")
    r.add_argument("--file", required=True)
    a = ap.parse_args()
    print("ok:" + a.file)

if __name__ == "__main__":
    main()
'''

TEST_JSON = '{"cases":[{"id":"T1","input":"x","expect":{"ok":true}}]}'
TEST_RUN = '''#!/usr/bin/env python3
import json, os, sys
p = os.path.join(os.path.dirname(os.path.abspath(__file__)), "golden.json")
d = json.load(open(p, encoding="utf-8"))
print("cases:", len(d["cases"]))
sys.exit(0)
'''
DEMO_RUN = '''#!/usr/bin/env python3
print("demo ok")
'''


def write(path, body):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    io.open(path, "w", encoding="utf-8", newline="\n").write(body)


def make_bad(root):
    write(os.path.join(root, "SKILL.md"), BAD_SKILL)


def make_good(root):
    write(os.path.join(root, "SKILL.md"), GOOD_SKILL)
    write(os.path.join(root, "scripts", "tool.py"), TOOL_PY)
    write(os.path.join(root, "tests", "golden.json"), TEST_JSON)
    write(os.path.join(root, "tests", "run_golden.py"), TEST_RUN)
    write(os.path.join(root, "demo", "run_demo.py"), DEMO_RUN)
    write(os.path.join(root, "ai-index.json"), '{"schema":"lgd-ai-index/1.0","skill":"demo-good"}')
    write(os.path.join(root, "llms.txt"), "# demo-good\n> demo\n")
    write(os.path.join(root, "LICENSE"), "MIT License\n")


def fix(bad_dir, good_dir):
    """按整改清单逐条修：补字段、去密钥、补测试与索引。"""
    for sub in ("scripts", "tests", "demo"):
        os.makedirs(os.path.join(bad_dir, sub), exist_ok=True)
    fm_fix = """---
name: demo-bad-fixed
display_name: 演示修复包
display_name_en: demo-bad-fixed
slug: demo-bad-fixed
author: 诺声(Logos)@SynomosAI
version: 1.0.0
license: MIT
category: developer-tools
description: "A fixed demo package. Faithful: no unobserved claim is invented."
description_zh: "修复后的演示包。"
description_en: "A fixed demo package."
tags:
  - 演示
  - 修复样本
  - demo-fixed
---

# demo-bad-fixed

## Triggers
「修复样本」

## 安全边界
只读、不联网。

## Sibling skills in the same ecosystem (LGD)
同系列技能（LGD 生态）：summarize-pro、debug-pro、wechat-viral-topic、lgd-skill-review。
"""
    write(os.path.join(bad_dir, "SKILL.md"), fm_fix)
    shutil.copy(os.path.join(good_dir, "scripts", "tool.py"), os.path.join(bad_dir, "scripts", "tool.py"))
    shutil.copy(os.path.join(good_dir, "tests", "golden.json"), os.path.join(bad_dir, "tests", "golden.json"))
    shutil.copy(os.path.join(good_dir, "tests", "run_golden.py"), os.path.join(bad_dir, "tests", "run_golden.py"))
    shutil.copy(os.path.join(good_dir, "demo", "run_demo.py"), os.path.join(bad_dir, "demo", "run_demo.py"))
    write(os.path.join(bad_dir, "ai-index.json"), '{"schema":"lgd-ai-index/1.0","skill":"demo-bad-fixed"}')
    write(os.path.join(bad_dir, "llms.txt"), "# demo-bad-fixed\n> demo\n")
    write(os.path.join(bad_dir, "LICENSE"), "MIT License\n")


def show(tag, data):
    print("%s：%d/100  %s" % (tag, data["total"], data["verdict"]))
    for b in data["blocking"]:
        print("   阻断 %s" % b)
    for a in data["actions"][:6]:
        print("   [%s] %s" % (a["priority"], a["issue"]))


def main():
    base = tempfile.mkdtemp(prefix="lgd_demo_")
    bad = os.path.join(base, "demo-bad")
    good = os.path.join(base, "demo-good")
    try:
        make_bad(bad)
        make_good(good)

        print("=== 第一步：评一个坏包 ===")
        r1 = rv.review(bad, do_run=False)["data"]
        show("改前", r1)

        print("\n=== 第二步：按整改清单修 ===")
        fix(bad, good)
        print("已补：display_name/display_name_en/category、SemVer、去密钥、tests、demo、ai-index、llms.txt、LICENSE")

        print("\n=== 第三步：复测 ===")
        r2 = rv.review(bad, do_run=True)["data"]
        show("改后", r2)

        print("\n=== 第四步：对照组（一开始就合格的包） ===")
        r3 = rv.review(good, do_run=True)["data"]
        show("对照组", r3)

        ok = (r1["verdict"] == "BLOCK" and r2["total"] > r1["total"]
              and r2["verdict"] in ("PASS", "WARN") and r3["total"] >= 80)
        print("\n演示结论：%s（改前 %d → 改后 %d，+%d）"
              % ("通过：闭环成立" if ok else "未通过", r1["total"], r2["total"],
                 r2["total"] - r1["total"]))
        sys.exit(0 if ok else 1)
    finally:
        shutil.rmtree(base, ignore_errors=True)


if __name__ == "__main__":
    main()

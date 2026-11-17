#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
功能回归测试（19 项级别，覆盖生成/复现/单文件答案/红线）
运行：python scripts/test_skill.py
"""
import json
import os
import subprocess
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
SKILL = os.path.dirname(HERE)
GEN = os.path.join(HERE, "generate_worksheet.py")
PY = sys.executable

fails = []


def run(*cli, expect_ok=True):
    p = subprocess.run([PY, GEN, *cli], capture_output=True, text=True)
    if expect_ok and p.returncode != 0:
        fails.append(f"命令失败: {' '.join(cli)}\n{p.stderr}")
    return p


def check(cond, msg):
    if not cond:
        fails.append(msg)


def main():
    tmp = tempfile.mkdtemp(prefix="kcc_test_")
    with open(os.path.join(tmp, "t.json"), "w") as f:
        f.write("{}")

    # 1) --list 可运行
    p = run("--list")
    check("topic" in p.stdout and "等级" in p.stdout, "list 输出异常")

    # 2) 每个等级生成（认字+描红+诗歌），默认含答案
    for lv in ["L1", "L2", "L3", "L4"]:
        out = os.path.join(tmp, f"{lv}.html")
        js = os.path.join(tmp, f"{lv}.json")
        run("--level", lv, "--topics", "recognize,trace,poem"
            + (",word" if lv in ("L3", "L4") else "")
            + (",fill" if lv == "L4" else ""),
            "--seed", "5", "--out", out, "--json", js)
        check(os.path.isfile(out) and os.path.isfile(js), f"{lv} 文件未生成")
        # 单文件答案：同一 HTML 内同时含题目与答案
        html = open(out, encoding="utf-8").read()
        check("参考答案" in html, f"{lv} 答案未内嵌同一 HTML")
        check("看图认汉字" in html or "Look & Read" in html, f"{lv} 题目缺失")
        check("window.print" in html, f"{lv} 缺打印按钮脚本")
        check("打印 / 另存为 PDF" in html or "Print / Save as PDF" in html, f"{lv} 缺打印按钮文案")
        meta = json.load(open(js, encoding="utf-8"))
        check("seed" in meta, f"{lv} JSON 缺 seed")

    # 3) 复现一致性：regen 与首次字节级相同
    out2 = os.path.join(tmp, "L2_regen.html")
    run("--regen", os.path.join(tmp, "L2.json"), "--out", out2,
        "--json", os.path.join(tmp, "L2_regen.json"))
    a = open(os.path.join(tmp, "L2.html"), encoding="utf-8").read()
    b = open(out2, encoding="utf-8").read()
    check(a == b, "regen 与首次生成不一致（字节级）")

    # 4) --no-answers 确实不内嵌答案
    out3 = os.path.join(tmp, "L2_noans.html")
    run("--level", "L2", "--topics", "recognize,trace,poem", "--seed", "5",
        "--no-answers", "--out", out3, "--json", os.path.join(tmp, "L2_noans.json"))
    check("参考答案" not in open(out3, encoding="utf-8").read(), "no-answers 仍含答案")

    # 5) 英文界面
    out4 = os.path.join(tmp, "L1_en.html")
    run("--level", "L1", "--lang", "en", "--seed", "1", "--out", out4,
        "--json", os.path.join(tmp, "L1_en.json"))
    check("Look & Read" in open(out4, encoding="utf-8").read(), "英文界面异常")

    # 6) 未知题型报错
    p = run("--level", "L1", "--topics", "foobar", "--out", os.path.join(tmp, "x.html"),
            "--json", os.path.join(tmp, "x.json"), expect_ok=False)
    check(p.returncode != 0, "未知题型未报错")

    # 7) 跨等级题型被忽略（L1 不能用 fill）
    p = run("--level", "L1", "--topics", "recognize,fill", "--seed", "1",
            "--out", os.path.join(tmp, "lv1fill.html"),
            "--json", os.path.join(tmp, "lv1fill.json"))
    m = json.load(open(os.path.join(tmp, "lv1fill.json"), encoding="utf-8"))
    check("fill" not in m["topics"], "L1 不应含 fill 题型")

    # 汇总
    if fails:
        print(f"FAIL：{len(fails)} 项未通过")
        for f in fails:
            print(" -", f)
        sys.exit(1)
    print("PASS：全部回归通过（生成/复现/单文件答案/红线/英文/校验）")


if __name__ == "__main__":
    main()

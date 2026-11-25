#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""check_commands.py — 文档里的计算器命令，真的能跑吗？

技能库最隐蔽的腐坏：说明书写着一条命令，读者照抄却报错（参数改名、参数单位改了、
工具路径变了）。本脚本把仓库里所有 Markdown 中的 `python3 skills/calc-toolkit/...`
命令抽出来逐条实跑，任何一条非零退出即失败。

用法：
    python3 tools/check_commands.py            # 全部跑一遍
    python3 tools/check_commands.py -v         # 同时打印每条命令的结果

跳过规则（避免误报）：
    - 含占位符的（{{ }}、<xxx>、…、___、××、...）
    - 以 `!` 开头（CI 里的反向断言）、以 $ 开头的 shell 变量行
    - 已带 `# 期望失败` 注释的命令（用于文档里故意演示报错）
只读检查，不改任何文件。
"""
import os
import re
import subprocess
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SKIP_PAT = re.compile(r"(\{\{|<[a-zA-Z_\u4e00-\u9fa5]+>|…|___|××|\.\.\.|\bXXX\b|期望失败)")
CMD_PAT = re.compile(r"^\s*(python3\s+skills/calc-toolkit/[A-Za-z0-9_]+\.py\b.*)$")


def target_files():
    out = []
    for base in ("skills", "docs"):
        d = os.path.join(ROOT, base)
        for dirpath, _dirnames, filenames in os.walk(d):
            for fn in sorted(filenames):
                if fn.endswith(".md"):
                    out.append(os.path.join(dirpath, fn))
    for fn in ("README.md", "README.en.md", "CONTRIBUTING.md", "CHANGELOG.md", "SKILL.md"):
        p = os.path.join(ROOT, fn)
        if os.path.isfile(p):
            out.append(p)
    return out


def extract():
    """返回 [(来源文件:行号, 命令)]，按出现顺序、去重。

    支持反斜杠续行：文档里写惯的
        python3 skills/calc-toolkit/x.py --a 1 \\
            --b 2
    会被拼成一条完整命令再试跑——否则续行的参数永远缺失，必然误报。
    """
    seen, rows = set(), []
    for path in target_files():
        with open(path, encoding="utf-8") as f:
            lines = f.readlines()
        i = 0
        while i < len(lines):
            line = lines[i]
            i += 1
            m = CMD_PAT.match(line)
            if not m:
                continue
            cmd = m.group(1).strip()
            while cmd.endswith("\\") and i < len(lines):
                cmd = cmd[:-1].rstrip() + " " + lines[i].strip()
                i += 1
            if True:
                if SKIP_PAT.search(cmd) or cmd.startswith("!") or "$" in cmd:
                    continue
                cmd = re.sub(r"\s+#.*$", "", cmd)          # 去掉行尾注释
                if cmd in seen:
                    continue
                seen.add(cmd)
                rel = os.path.relpath(path, ROOT)
                rows.append((f"{rel}:{i}", cmd))
    return rows


def run(cmd):
    try:
        p = subprocess.run(cmd, shell=True, cwd=ROOT, timeout=90,
                           stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        return p.returncode, p.stdout.decode("utf-8", "replace").strip()
    except subprocess.TimeoutExpired:
        return 124, "超时（>90s）"


def main():
    verbose = "-v" in sys.argv or "--verbose" in sys.argv
    rows = extract()
    if not rows:
        print("没有找到任何计算器命令（可能正则失效，请检查 CMD_PAT）")
        return 1
    bad = []
    for where, cmd in rows:
        code, out = run(cmd)
        if code != 0:
            bad.append((where, cmd, code, out))
            print(f"✗ {where}\n    $ {cmd}\n    退出码 {code}｜{out.splitlines()[0] if out else ''}")
        elif verbose:
            print(f"✓ {where}｜{cmd}")
    print(f"\n共检查 {len(rows)} 条文档命令，失败 {len(bad)} 条。")
    if bad:
        print("修复方式：改文档里的命令，或改工具参数（改工具时同步改文档，别只改一边）。")
        return 1
    print("✓ 文档命令全部可执行")
    return 0


if __name__ == "__main__":
    sys.exit(main())

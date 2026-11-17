#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""注入 learner 闭环 + 打包技能的编排小工具（供元进化迭代复用）。
用法: python _finalize_skill.py <skill_name>
"""
import sys, os, shutil, subprocess

SK = r"C:/Users/\u5c0f\u6c5f/.workbuddy/skills".encode().decode("unicode_escape")
SK = os.path.expanduser("~/.workbuddy/skills")
PY = sys.executable
OUT = r"C:/Users/\u5c0f\u6c5f/WorkBuddy/2026-07-21-20-44-12/output/skills_packages"
OUT = OUT.encode().decode("unicode_escape")


def finalize(name):
    dir_ = os.path.join(SK, name)
    scripts = os.path.join(dir_, "scripts")
    # 1) copy learner.py
    shutil.copy(os.path.join(SK, "skill-self-improve", "scripts", "learner.py"),
                os.path.join(scripts, "learner.py"))
    # 2) init learned_patterns.json
    subprocess.run([PY, os.path.join(scripts, "learner.py"), "init", dir_], check=True)
    # 3) append self-improve section to SKILL.md (idempotent)
    skill_md = os.path.join(dir_, "SKILL.md")
    with open(skill_md, encoding="utf-8") as f:
        body = f.read()
    if "自进化学习系统" not in body:
        with open(os.path.join(SK, "skill-self-improve", "scripts", "section.md"),
                  encoding="utf-8") as f:
            sec = f.read()
        with open(skill_md, "a", encoding="utf-8") as f:
            f.write("\n" + sec)
    # 4) clean __pycache__
    for root, dirs, files in os.walk(dir_):
        for d in list(dirs):
            if d == "__pycache__":
                shutil.rmtree(os.path.join(root, d), ignore_errors=True)
    # 5) package
    os.makedirs(OUT, exist_ok=True)
    r = subprocess.run([PY, os.path.join(SK, "skill-creator", "scripts", "package_skill.py"),
                        dir_, OUT], capture_output=True, text=True)
    print(r.stdout[-800:])
    if r.stderr:
        print("STDERR:", r.stderr[-400:])
    return r.returncode


if __name__ == "__main__":
    if len(sys.argv) < 2 or sys.argv[1] in ("--help", "-h", "help"):
        print(__doc__)
        sys.exit(0)
    name = sys.argv[1]
    if not os.path.isdir(os.path.join(SK, name)):
        print(f"[error] skill dir not found: {name}  (skills/<name> must exist first)")
        sys.exit(2)
    if not os.path.isfile(os.path.join(SK, name, "SKILL.md")):
        print(f"[error] SKILL.md missing in skills/{name}; create it before finalize")
        sys.exit(2)
    sys.exit(finalize(name))

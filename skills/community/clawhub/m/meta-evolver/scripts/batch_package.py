#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""全量打包技能到 output/skills_packages/ 。
遍历 meta-*/mega-*/gen-* 以及本回合新增引擎技能，调用 package_skill.py 打包，
跳过已存在的 zip（幂等）。统计成功/失败。
"""
import os
import sys
import subprocess
import glob

SKILLS_DIR = r"C:\Users\小江\.workbuddy\skills"
OUT_DIR = r"C:\Users\小江\WorkBuddy\2026-07-21-20-44-12\output\skills_packages"
PACKAGER = os.path.join(SKILLS_DIR, "skill-creator", "scripts", "package_skill.py")
PY = r"C:\Users\小江\.workbuddy\binaries\python\versions\3.13.12\python.exe"

# 需要包含的额外非 meta/mega/gen 引擎技能
EXTRA = ["lifelong-skill-synthesis", "cross-domain-synthesis",
          "model-distillation", "super-agent", "meta-super-agent",
          "mega-agent", "meta-evolver"]


def collect():
    dirs = []
    for pat in ("meta-*", "mega-*", "gen-*"):
        dirs += [os.path.basename(d) for d in glob.glob(os.path.join(SKILLS_DIR, pat))
                  if os.path.isdir(d)]
    for e in EXTRA:
        if os.path.isdir(os.path.join(SKILLS_DIR, e)):
            dirs.append(e)
    # 去重
    return sorted(set(dirs))


def main():
    os.makedirs(OUT_DIR, exist_ok=True)
    done = {os.path.splitext(f)[0] for f in os.listdir(OUT_DIR) if f.endswith(".zip")}
    targets = [d for d in collect() if d not in done]
    print(f"待打包: {len(targets)}  (已完成 {len(done)})", flush=True)
    ok = 0
    fail = 0
    fails = []
    for i, name in enumerate(targets, 1):
        sdir = os.path.join(SKILLS_DIR, name)
        try:
            r = subprocess.run(
                [PY, PACKAGER, sdir, OUT_DIR],
                cwd=os.path.dirname(PACKAGER),
                capture_output=True, text=True, timeout=120)
            if r.returncode == 0 and os.path.exists(os.path.join(OUT_DIR, name + ".zip")):
                ok += 1
                if i % 25 == 0:
                    print(f"  [{i}/{len(targets)}] OK={ok} FAIL={fail}", flush=True)
            else:
                fail += 1
                fails.append((name, (r.stderr or r.stdout)[-200:]))
        except Exception as e:
            fail += 1
            fails.append((name, str(e)[:200]))
    print(f"\n=== 全量打包完成: 成功 {ok} / 失败 {fail} ===", flush=True)
    if fails:
        print("失败清单 (前15):")
        for n, reason in fails[:15]:
            print(f"  - {n}: {reason}")
    print(f"output 总 zip: {len(os.listdir(OUT_DIR))}", flush=True)


if __name__ == "__main__":
    main()

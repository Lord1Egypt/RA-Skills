#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""彻底补丁 v2：覆盖所有打包目标（meta-*/mega-*/gen-* + EXTRA 引擎技能）。
对每个技能目录：
1) 目录名规范化（_ -> -, 合并连续 -, 中文/大写转英文 slug, 不允许首尾 -）
2) 强制 SKILL.md 的 name 字段 == 最终合规目录名
3) 补 description（缺失时）
幂等、不删数据（冲突目录加 -dup 后缀保留）。
"""
import os
import re
import glob
import hashlib

SKILLS = r"C:\Users\小江\.workbuddy\skills"
EXTRA = ["model-distillation", "four-engine-orchestrator",
          "lifelong-skill-synthesis", "cross-domain-synthesis",
          "super-agent", "mega-agent", "meta-super-agent", "meta-evolver"]


def target_name(name):
    s = name.replace("_", "-")
    s = re.sub(r"-+", "-", s).strip("-")
    if re.fullmatch(r"[a-z0-9-]+", s):
        return s, False
    h = re.search(r"([0-9a-f]{6,})", s)
    suffix = (h.group(1).lower() if h else hashlib.md5(name.encode("utf-8")).hexdigest()[:8])
    low = name.lower()
    prefix = "gen" if "gen" in low else ("meta" if low.startswith("meta") else "skill")
    return f"{prefix}-{suffix}", True


def extract_desc(text):
    for line in text.splitlines():
        s = line.strip()
        if not s or s.startswith("#") or s.startswith(">") or s.startswith("---") or s.startswith("|"):
            continue
        if "蒸馏" in s[:12] or "由" in s[:4]:
            return s[:200]
    return "由 meta-evolver 生态生成的技能"


def fix_one(d, final):
    smd = os.path.join(d, "SKILL.md")
    if not os.path.isfile(smd):
        return "no-skillmd"
    t = open(smd, encoding="utf-8").read()
    m = re.match(r"^\s*---\s*\n(.*?)\n---\s*\n?", t, re.S)
    if not m:
        desc = extract_desc(t)
        fm = (f"---\nname: {final}\nversion: 1.0.0\ndescription: |\n  {desc}\n"
               f"agent_created: true\nvisibility: public\n---\n\n")
        open(smd, "w", encoding="utf-8").write(fm + t)
        return "injected"
    block = m.group(1)
    body = t[m.end():]
    # 修正 name
    block = re.sub(r"(?m)^name:\s*.+$", f"name: {final}", block)
    # 补 description
    if not re.search(r"(?m)^description:", block):
        block = block.rstrip() + f"\ndescription: |\n  {extract_desc(body)}\n"
    open(smd, "w", encoding="utf-8").write("---\n" + block + "\n---\n" + body)
    return "patched"


def main():
    targets = []
    for pat in ("meta-*", "mega-*", "gen-*"):
        targets += [os.path.basename(x) for x in glob.glob(os.path.join(SKILLS, pat)) if os.path.isdir(x)]
    targets += [e for e in EXTRA if os.path.isdir(os.path.join(SKILLS, e))]
    targets = sorted(set(targets))

    renamed = 0
    patched = 0
    for base in targets:
        d = os.path.join(SKILLS, base)
        tname, need = target_name(base)
        final = base
        if tname != base:
            cand = tname
            if os.path.exists(os.path.join(SKILLS, cand)):
                cand = tname + "-dup"
            if cand != base:
                os.rename(d, os.path.join(SKILLS, cand))
                final = cand
                renamed += 1
        r = fix_one(os.path.join(SKILLS, final), final)
        if r in ("injected", "patched"):
            patched += 1
    print(f"目录规范化: {renamed} ｜ frontmatter 修正: {patched} ｜ 处理总数: {len(targets)}")


if __name__ == "__main__":
    main()

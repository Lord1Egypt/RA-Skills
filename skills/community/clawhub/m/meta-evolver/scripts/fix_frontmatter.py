#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""修复批量蒸馏产物的打包阻碍：
1) 给所有缺 YAML frontmatter 的 meta-*/gen-* SKILL.md 注入标准块
2) 把 gen-* 中文目录重命名为 hyphen-case 英文名（name 同步）
幂等：已符合的直接跳过。
"""
import os
import re
import glob
import hashlib

SKILLS = r"C:\Users\小江\.workbuddy\skills"


def eng_slug(name):
    # 已是 hyphen-case（仅小写字母/数字/连字符）则保持
    if re.fullmatch(r"[a-z0-9-]+", name):
        return name
    # 取目录名中的 hex 后缀（批量合成常带 -<6位hash>）
    h = re.search(r"([0-9a-f]{6,})", name)
    suffix = h.group(1) if h else hashlib.md5(name.encode("utf-8")).hexdigest()[:8]
    return "gen-" + suffix


def extract_desc(text):
    for line in text.splitlines():
        s = line.strip()
        if not s:
            continue
        if s.startswith("#") or s.startswith(">") or s.startswith("---") or s.startswith("|"):
            continue
        if s.startswith("由") or "蒸馏" in s[:10]:
            return s[:200]
    return "由 model-distillation 蒸馏生成的超越型元技能"


def main():
    fixed_fm = 0
    renamed = 0
    skipped = 0
    for pat in ("meta-*", "gen-*"):
        for d in sorted(glob.glob(os.path.join(SKILLS, pat))):
            if not os.path.isdir(d):
                continue
            name = os.path.basename(d)
            smd = os.path.join(d, "SKILL.md")
            if not os.path.isfile(smd):
                continue
            slug = eng_slug(name)
            # 重命名中文 gen 目录
            if slug != name:
                target = os.path.join(SKILLS, slug)
                if os.path.exists(target):
                    # 目标已就位（可能上次中断残留），沿用
                    d, name, slug = target, slug, slug
                else:
                    os.rename(d, target)
                    d, name, slug = target, slug, slug
                    renamed += 1
            smd = os.path.join(d, "SKILL.md")
            if not os.path.isfile(smd):
                continue
            t = open(smd, encoding="utf-8").read()
            if re.match(r"^\s*---", t):
                skipped += 1
                continue
            desc = extract_desc(t)
            fm = (
                "---\n"
                f"name: {slug}\n"
                "version: 1.0.0\n"
                "description: |\n"
                f"  {desc}\n"
                "agent_created: true\n"
                "visibility: public\n"
                "---\n\n"
            )
            open(smd, "w", encoding="utf-8").write(fm + t)
            fixed_fm += 1
    print(f"注入 frontmatter: {fixed_fm} ｜ 重命名 gen 目录: {renamed} ｜ 已合规跳过: {skipped}")


if __name__ == "__main__":
    main()

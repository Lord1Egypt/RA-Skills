#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
sync_embedded.py — 把本体论智能体技能同步进内嵌它的专家包
本体论智能体 (Ontology Agent) · 天津市微数人工智能科技有限责任公司

问题：专家包（数字公司）内嵌了一份 ontology-agent 技能副本。技能本体更新后，
      内嵌副本不会自动变。本脚本把技能最新内容同步进专家包，使其与技能一致。

用法：
  python sync_embedded.py <专家包目录>
    <专家包目录> 是包含 skills/ontology-agent/ 的目录（即专家包根）。
    脚本自动定位内嵌技能目录并覆盖同步，随后建议重新加载/register 专家包。

同步内容：SKILL.md GUIDE.md VERSION references/ scripts/ connectors/ experts-template/
不同步：instance.yaml / experts/ 等用户运行时产物（不属技能本体）。
"""
import os
import shutil
import sys

SKILL_NAME = "ontology-agent"


def find_embedded(pkg_dir):
    for cand in (os.path.join(pkg_dir, "skills", SKILL_NAME),
                 os.path.join(pkg_dir, ".codebuddy-plugin", "skills", SKILL_NAME)):
        if os.path.isdir(cand):
            return cand
    return None


def main():
    if len(sys.argv) < 2:
        print("用法: python sync_embedded.py <专家包目录>")
        sys.exit(1)
    pkg = sys.argv[1]
    src = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # scripts/.. = 技能根
    dst = find_embedded(pkg)
    if dst is None:
        print("[sync] 未在 %s 找到内嵌 %s 技能目录（skills/%s/）。请确认路径。" % (pkg, SKILL_NAME, SKILL_NAME))
        sys.exit(2)
    sync_items = ["SKILL.md", "GUIDE.md", "VERSION", "LICENSE", "README.md", "references", "scripts", "connectors", "experts-template"]
    for item in sync_items:
        s = os.path.join(src, item)
        d = os.path.join(dst, item)
        if os.path.isdir(s):
            if os.path.isdir(d):
                shutil.rmtree(d)
            shutil.copytree(s, d)
        elif os.path.isfile(s):
            shutil.copy2(s, d)
        else:
            print("  [skip] 源不存在: %s" % item)
    print("[sync] 已同步 %s -> %s" % (src, dst))
    print("[sync] 提示：同步后请在专家中心重新加载 / register 该专家包使其生效。")


if __name__ == "__main__":
    main()

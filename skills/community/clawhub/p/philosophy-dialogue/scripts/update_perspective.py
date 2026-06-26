#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
蒸馏人物 skill 私域化改造脚本
- 从 memory/philosopher-registry.md 读取人物注册表
- 将各人物的 perspective skill 拷贝到 philosophy-dialogue/references/perspective/ 下
- 生成新的 skill 内注册表（路径指向私域副本）

用法:
    cd /path/to/workspace
    python3 skills/philosophy-dialogue/scripts/update_perspective.py

安全声明:
- 仅使用 Python 标准库
- 无网络调用
- 文件读取: memory/philosopher-registry.md, skills/*-perspective/
- 文件写入: skills/philosophy-dialogue/references/perspective/, 
            skills/philosophy-dialogue/references/philosopher-registry.md
"""

import os
import re
import sys
import shutil
from datetime import datetime


def find_workspace_root():
    """查找 workspace 根目录"""
    # 优先从环境变量
    if os.environ.get("WORKSPACE"):
        return os.environ["WORKSPACE"]
    # 从脚本位置推断: scripts/ -> philosophy-dialogue/ -> skills/ -> workspace/
    script_dir = os.path.dirname(os.path.abspath(__file__))
    return os.path.abspath(os.path.join(script_dir, "..", "..", ".."))


def parse_registry(registry_path):
    """
    解析 memory/philosopher-registry.md，提取人物列表。
    返回 list of dict: {num, cn_name, en_name, category, skill_path, created, updated}
    """
    if not os.path.exists(registry_path):
        print(f"❌ 注册表不存在: {registry_path}")
        sys.exit(1)

    entries = []
    with open(registry_path, "r", encoding="utf-8") as f:
        in_table = False
        col_map = {}

        for line in f:
            line = line.strip()
            if not line or "|" not in line:
                in_table = False
                col_map = {}
                continue

            cols = [c.strip() for c in line.split("|")]
            # 去掉首尾空列
            if cols and cols[0] == "":
                cols = cols[1:]
            if cols and cols[-1] == "":
                cols = cols[:-1]

            # 跳过分隔行
            if all(re.match(r"^[-:]+$", c) for c in cols if c):
                continue

            # 解析表头
            if not in_table and not col_map:
                for i, col in enumerate(cols):
                    if "#" in col:
                        col_map["num"] = i
                    elif "中文名称" in col:
                        col_map["cn_name"] = i
                    elif "人物名称" in col:
                        col_map["en_name"] = i
                    elif "类别" in col:
                        col_map["category"] = i
                    elif "蒸馏文件路径" in col:
                        col_map["skill_path"] = i
                    elif "创建时间" in col:
                        col_map["created"] = i
                    elif "更新时间" in col:
                        col_map["updated"] = i
                if "cn_name" in col_map and "skill_path" in col_map:
                    in_table = True
                continue

            # 解析数据行
            if in_table and col_map:
                def get_col(key):
                    idx = col_map.get(key, -1)
                    return cols[idx].strip() if 0 <= idx < len(cols) else ""

                num = get_col("num")
                cn_name = get_col("cn_name")
                en_name = get_col("en_name")
                skill_path = get_col("skill_path")

                if cn_name and skill_path and not re.match(r"^[-:]+$", cn_name):
                    entries.append({
                        "num": num,
                        "cn_name": cn_name,
                        "en_name": en_name,
                        "category": get_col("category"),
                        "skill_path": skill_path,
                        "created": get_col("created"),
                        "updated": get_col("updated"),
                    })

    return entries


def copy_perspectives(entries, workspace_root, dest_base):
    """
    将每个人物的 perspective skill 目录拷贝到 dest_base 下。
    返回 (成功数, 失败数, 失败列表)
    """
    os.makedirs(dest_base, exist_ok=True)

    success = 0
    failed = 0
    failed_list = []

    for entry in entries:
        skill_path = entry["skill_path"]  # e.g. skills/mozi-perspective/SKILL.md
        # 提取目录名: skills/mozi-perspective/SKILL.md -> mozi-perspective
        parts = skill_path.replace("\\", "/").split("/")
        # 找到 *-perspective 目录
        perspective_dir = None
        for p in parts:
            if p.endswith("-perspective"):
                perspective_dir = p
                break

        if not perspective_dir:
            # 尝试从路径推断
            if len(parts) >= 2:
                perspective_dir = parts[-2] if parts[-1].endswith(".md") else parts[-1]
            else:
                print(f"  ⚠️ 无法解析路径: {skill_path} ({entry['cn_name']})")
                failed += 1
                failed_list.append(entry["cn_name"])
                continue

        src_dir = os.path.join(workspace_root, "skills", perspective_dir)
        dst_dir = os.path.join(dest_base, perspective_dir)

        if not os.path.exists(src_dir):
            print(f"  ⚠️ 源目录不存在: {src_dir} ({entry['cn_name']})")
            failed += 1
            failed_list.append(entry["cn_name"])
            continue

        # 拷贝（已存在则覆盖）
        if os.path.exists(dst_dir):
            shutil.rmtree(dst_dir)
        shutil.copytree(src_dir, dst_dir)
        success += 1

    return success, failed, failed_list


def generate_new_registry(entries, dest_base, output_path, skill_base_rel):
    """
    生成新的 philosopher-registry.md，蒸馏文件路径改为私域路径。
    skill_base_rel: 相对路径前缀，如 skills/philosophy-dialogue/references/perspective
    """
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    total = len(entries)

    lines = []
    lines.append("# 哲学家注册表 (Philosopher Registry)")
    lines.append("")
    lines.append(f"**最后更新**: {now}")
    lines.append(f"**总人数**: **{total} 位** ✅")
    lines.append("")
    lines.append("**状态**: 全部蒸馏完成（私域化副本）")
    lines.append("")
    lines.append("---")
    lines.append("")
    lines.append("## 📊 总体统计")
    lines.append("")
    lines.append("| 类别 | 人数 | 百分比 |")
    lines.append("| ------ |------|--------|")
    lines.append(f'| **总计** | **{total}** | **100%** |')
    lines.append("")
    lines.append("## 📋 完整名单")
    lines.append("")
    lines.append("| # | 中文名称 | 人物名称 | 类别 | 蒸馏文件路径 | 创建时间 | 更新时间 |")
    lines.append("| --- |----------|----------|------|-------------|----------|----------|")

    for entry in entries:
        skill_path = entry["skill_path"]
        parts = skill_path.replace("\\", "/").split("/")
        perspective_dir = None
        for p in parts:
            if p.endswith("-perspective"):
                perspective_dir = p
                break
        if not perspective_dir and len(parts) >= 2:
            perspective_dir = parts[-2] if parts[-1].endswith(".md") else parts[-1]

        if perspective_dir:
            new_path = f"{skill_base_rel}/{perspective_dir}/SKILL.md"
        else:
            new_path = entry["skill_path"]  # fallback 保持原路径

        lines.append(
            f"| {entry['num']} | {entry['cn_name']} | {entry['en_name']} "
            f"| {entry['category']} | {new_path} "
            f"| {entry['created']} | {entry['updated']} |"
        )

    with open(output_path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")


def main():
    workspace_root = find_workspace_root()
    print(f"📁 Workspace: {workspace_root}")

    # 路径定义
    source_registry = os.path.join(workspace_root, "memory", "philosopher-registry.md")
    skill_dir = os.path.join(workspace_root, "skills", "philosophy-dialogue")
    dest_base = os.path.join(skill_dir, "references", "perspective")
    output_registry = os.path.join(skill_dir, "references", "philosopher-registry.md")
    skill_base_rel = "skills/philosophy-dialogue/references/perspective"

    # 1. 解析原始注册表
    print(f"\n📖 读取原始注册表: {source_registry}")
    entries = parse_registry(source_registry)
    print(f"   共 {len(entries)} 位人物")

    if not entries:
        print("❌ 未解析到任何人物，请检查注册表格式")
        sys.exit(1)

    # 2. 创建目录并拷贝 perspective skills
    print(f"\n📦 拷贝 perspective skills → {dest_base}")
    success, failed, failed_list = copy_perspectives(entries, workspace_root, dest_base)
    print(f"   ✅ 成功: {success}")
    if failed > 0:
        print(f"   ⚠️ 失败: {failed} ({', '.join(failed_list)})")

    # 3. 生成新注册表
    print(f"\n📝 生成新注册表: {output_registry}")
    generate_new_registry(entries, dest_base, output_registry, skill_base_rel)

    # 4. 统计
    print(f"\n{'='*50}")
    print(f"✅ 私域化改造完成！")
    print(f"{'='*50}")
    print(f"   人物总数: {len(entries)}")
    print(f"   拷贝成功: {success}")
    print(f"   拷贝失败: {failed}")
    print(f"   私域目录: {dest_base}")
    print(f"   新注册表: {output_registry}")


if __name__ == "__main__":
    main()

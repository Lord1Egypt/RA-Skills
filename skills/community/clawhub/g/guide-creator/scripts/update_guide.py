#!/usr/bin/env python3
"""
update_guide.py — 项目文档更新辅助脚本

支持四种操作：
  add-changelog  追加版本更新记录
  add-pitfall    追加踩坑记录
  bump-version   更新版本号
  sync-files     扫描项目文件并与 start.md 文件清单对比

用法:
    python3 update_guide.py --action add-changelog --root /path/to/project
    python3 update_guide.py --action add-pitfall --root .
    python3 update_guide.py --action bump-version --version v2.4 --root .
    python3 update_guide.py --action sync-files --root /path/to/project
"""

import argparse
import os
import re
import sys
import glob
from datetime import datetime


# ============================================================
# 工具函数
# ============================================================

def find_guide_root(root):
    """验证 guide 目录结构存在"""
    guide_dir = os.path.join(root, "guide")
    start_md = os.path.join(root, "start.md")
    if not os.path.isdir(guide_dir):
        print(f"❌ 未找到 guide/ 目录: {guide_dir}")
        print("   请先运行 init_guide.py 初始化文档结构")
        sys.exit(1)
    return guide_dir, start_md


def read_file(path):
    """读取文件内容"""
    if not os.path.exists(path):
        return ""
    with open(path, "r", encoding="utf-8") as f:
        return f.read()


def write_file(path, content):
    """写入文件内容"""
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)


def get_current_version(changelog_path):
    """从 changelog 中提取当前版本号"""
    content = read_file(changelog_path)
    match = re.search(r"## (v[\d.]+)", content)
    if match:
        return match.group(1)
    return "v0.1"


def get_next_pitfall_number(pitfalls_path):
    """获取下一个踩坑编号"""
    content = read_file(pitfalls_path)
    numbers = re.findall(r"## 🔥 坑(\d+)", content)
    if numbers:
        return max(int(n) for n in numbers) + 1
    return 1


# ============================================================
# 操作实现
# ============================================================

def action_add_changelog(root):
    """交互式添加 changelog 条目"""
    guide_dir, _ = find_guide_root(root)
    changelog_path = os.path.join(guide_dir, "08-changelog.md")
    current_version = get_current_version(changelog_path)

    print(f"📝 添加 Changelog 条目")
    print(f"   当前版本: {current_version}")
    print()

    # 交互输入
    new_version = input(f"新版本号 (默认递增为 {bump_version_str(current_version)}): ").strip()
    if not new_version:
        new_version = bump_version_str(current_version)

    title = input("版本标题摘要: ").strip()
    if not title:
        print("❌ 标题不能为空")
        sys.exit(1)

    print("\n请输入改动内容（每行一条，空行结束）:")
    changes = []
    while True:
        line = input("  > ").strip()
        if not line:
            break
        changes.append(line)

    print("\n有 Bug 修复吗？（每行一条，空行跳过）:")
    bugs = []
    while True:
        line = input("  🐛 > ").strip()
        if not line:
            break
        bugs.append(line)

    print("\n代码改动文件列表（每行一条，空行结束）:")
    code_changes = []
    while True:
        line = input("  📝 > ").strip()
        if not line:
            break
        code_changes.append(line)

    # 生成条目
    today = datetime.now().strftime("%Y-%m-%d")
    entry = f"\n## {new_version} — {title} ({today})\n\n"

    if changes:
        entry += "### 🎯 改动内容\n"
        for c in changes:
            entry += f"- {c}\n"
        entry += "\n"

    if bugs:
        entry += "### 🐛 Bug修复\n"
        for b in bugs:
            entry += f"- {b}\n"
        entry += "\n"

    if code_changes:
        entry += "### 📝 代码改动\n"
        for cc in code_changes:
            entry += f"- {cc}\n"
        entry += "\n"

    # 插入到文件中（在第一个 ## 之前）
    content = read_file(changelog_path)
    # 找到 "---" 分隔线后的第一个 ## 位置
    insert_pos = content.find("\n## ")
    if insert_pos == -1:
        # 没有已有版本，追加到文件末尾
        content += "\n" + entry
    else:
        # 在第一个版本之前插入
        content = content[:insert_pos] + "\n" + entry + "---\n" + content[insert_pos:]

    write_file(changelog_path, content)

    # 检查行数是否需要归档
    line_count = content.count("\n")
    if line_count > 500:
        print(f"\n⚠️  changelog 已有 {line_count} 行，建议归档旧版本到 guide/archive/")

    print(f"\n✅ 已添加 {new_version} 到 {os.path.relpath(changelog_path, root)}")
    print(f"   💡 记得同步更新 guide.md 中的版本号")


def action_add_pitfall(root):
    """交互式添加踩坑记录"""
    guide_dir, _ = find_guide_root(root)
    pitfalls_path = os.path.join(guide_dir, "09-pitfalls.md")
    next_num = get_next_pitfall_number(pitfalls_path)

    print(f"🔥 添加踩坑记录（编号: 坑{next_num}）")
    print()

    title = input("坑标题: ").strip()
    if not title:
        print("❌ 标题不能为空")
        sys.exit(1)

    print("\n问题现象（每行一条，空行结束）:")
    symptoms = []
    while True:
        line = input("  现象 > ").strip()
        if not line:
            break
        symptoms.append(line)

    print("\n问题根因（每行一条，空行结束）:")
    causes = []
    while True:
        line = input("  根因 > ").strip()
        if not line:
            break
        causes.append(line)

    print("\n解决方案（每行一条，空行结束）:")
    solutions = []
    while True:
        line = input("  方案 > ").strip()
        if not line:
            break
        solutions.append(line)

    principle = input("\n通用原则（一句话，加粗显示）: ").strip()

    print("\n其他注意事项（每行一条，空行结束）:")
    notes = []
    while True:
        line = input("  注意 > ").strip()
        if not line:
            break
        notes.append(line)

    # 生成条目
    entry = f"\n## 🔥 坑{next_num}：{title}\n\n"

    entry += "### 问题现象\n"
    for s in symptoms:
        entry += f"{s}\n"
    entry += "\n"

    entry += "### 问题根因\n"
    for c in causes:
        entry += f"{c}\n"
    entry += "\n"

    entry += "### 解决方案\n"
    for s in solutions:
        entry += f"{s}\n"
    entry += "\n"

    entry += "### ⚠️ 开发注意\n"
    if principle:
        entry += f"- **{principle}**\n"
    for n in notes:
        entry += f"- {n}\n"
    entry += "\n---\n"

    # 插入到通用原则章节之前
    content = read_file(pitfalls_path)
    principle_section = "## 📋 通用开发原则"
    pos = content.find(principle_section)
    if pos != -1:
        content = content[:pos] + entry + "\n" + content[pos:]
    else:
        content += entry

    write_file(pitfalls_path, content)

    # 检查条数
    pit_count = len(re.findall(r"## 🔥 坑\d+", content))
    if pit_count > 30:
        print(f"\n⚠️  踩坑记录已有 {pit_count} 条，建议按类型分组")

    print(f"\n✅ 已添加 坑{next_num}：{title}")
    if principle:
        print(f"   💡 记得在通用原则章节添加: {principle}")


def action_bump_version(root, new_version=None):
    """更新版本号"""
    guide_dir, _ = find_guide_root(root)
    changelog_path = os.path.join(guide_dir, "08-changelog.md")
    guide_path = os.path.join(guide_dir, "guide.md")

    current = get_current_version(changelog_path)

    if not new_version:
        new_version = input(f"当前版本: {current}，新版本号: ").strip()
        if not new_version:
            new_version = bump_version_str(current)

    updated = []

    # 更新 guide.md
    guide_content = read_file(guide_path)
    new_guide = re.sub(
        r"\*\*当前版本\*\*:\s*v[\d.]+",
        f"**当前版本**: {new_version}",
        guide_content,
    )
    if new_guide != guide_content:
        write_file(guide_path, new_guide)
        updated.append("guide.md")

    print(f"\n✅ 版本号已更新: {current} → {new_version}")
    for f in updated:
        print(f"   · {f}")
    if not updated:
        print("   ⚠️ 未找到需要更新的版本号位置")


def action_sync_files(root):
    """扫描项目文件与 start.md 文件清单对比"""
    _, start_path = find_guide_root(root)

    # 扫描项目文件
    exclude_dirs = {
        "node_modules", "dist", "build", ".git", ".codebuddy",
        "__pycache__", ".venv", "venv", "env", ".next", ".nuxt",
        "coverage", ".nyc_output", "log", "logs", "asset", "assets",
        "guide", "archive",
    }
    exclude_exts = {".pyc", ".pyo", ".map", ".lock", ".log", ".png", ".jpg",
                    ".jpeg", ".gif", ".ico", ".svg", ".woff", ".woff2", ".ttf",
                    ".eot", ".mp3", ".mp4", ".wav"}

    project_files = set()
    for entry in os.listdir(root):
        if entry.startswith("."):
            continue
        if entry in exclude_dirs:
            continue
        full = os.path.join(root, entry)
        if os.path.isfile(full):
            _, ext = os.path.splitext(entry)
            if ext.lower() not in exclude_exts:
                project_files.add(entry)

    # 解析 start.md 中的文件清单
    start_content = read_file(start_path)
    # 匹配 `文件名` 格式
    listed_files = set(re.findall(r"`([^`]+\.\w+)`", start_content))

    # 对比
    new_files = project_files - listed_files
    removed_files = listed_files - project_files

    print(f"📂 文件同步检查")
    print(f"   项目文件: {len(project_files)} 个")
    print(f"   清单文件: {len(listed_files)} 个")
    print()

    if new_files:
        print(f"🆕 新增文件（未在 start.md 中列出）:")
        for f in sorted(new_files):
            print(f"   + {f}")
    else:
        print("✅ 没有新增文件")

    if removed_files:
        print(f"\n🗑️  已删除文件（在 start.md 中但不存在）:")
        for f in sorted(removed_files):
            print(f"   - {f}")
    else:
        print("✅ 没有已删除的文件")

    if new_files or removed_files:
        print(f"\n💡 请更新 start.md 的文件清单表")


def bump_version_str(version):
    """版本号递增 0.1"""
    match = re.match(r"v(\d+)\.(\d+)", version)
    if match:
        major = int(match.group(1))
        minor = int(match.group(2))
        return f"v{major}.{minor + 1}"
    return "v0.2"


# ============================================================
# 主入口
# ============================================================

def main():
    parser = argparse.ArgumentParser(
        description="项目文档更新辅助工具",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
操作说明:
  add-changelog   追加版本更新记录到 08-changelog.md
  add-pitfall     追加踩坑记录到 09-pitfalls.md
  bump-version    更新 guide.md 中的版本号
  sync-files      扫描项目文件并与 start.md 文件清单对比

示例:
  python3 update_guide.py --action add-changelog --root .
  python3 update_guide.py --action sync-files --root /path/to/project
  python3 update_guide.py --action bump-version --version v2.4 --root .
        """,
    )
    parser.add_argument(
        "--action",
        required=True,
        choices=["add-changelog", "add-pitfall", "bump-version", "sync-files"],
        help="执行的操作",
    )
    parser.add_argument("--root", default=".", help="项目根目录（默认当前目录）")
    parser.add_argument("--version", default=None, help="新版本号（仅 bump-version 使用）")

    args = parser.parse_args()
    root = os.path.abspath(args.root)

    actions = {
        "add-changelog": lambda: action_add_changelog(root),
        "add-pitfall": lambda: action_add_pitfall(root),
        "bump-version": lambda: action_bump_version(root, args.version),
        "sync-files": lambda: action_sync_files(root),
    }

    actions[args.action]()


if __name__ == "__main__":
    main()

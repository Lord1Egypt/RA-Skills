#!/usr/bin/env python3
"""
memory-association/scripts/build_index.py
扫描 memory/ 目录，自动生成/更新 MEMORY_INDEX.md

用法: python3 build_index.py [--dry-run]
"""
import os
import re
import argparse
from pathlib import Path
from datetime import datetime

MEMORY_DIR = Path.home() / ".openclaw/workspace/memory"
INDEX_PATH = MEMORY_DIR / "MEMORY_INDEX.md"
SKILL_INDEX = Path(__file__).parent.parent / "references" / "MEMORY_INDEX.md"


def extract_frontmatter(content: str) -> dict:
    """从文件头部提取 name/description/type"""
    fm = {}
    if content.startswith("---"):
        end = content.find("---", 3)
        if end > 0:
            block = content[3:end]
            for line in block.splitlines():
                if ":" in line:
                    key, _, val = line.partition(":")
                    fm[key.strip()] = val.strip().strip('"')
    return fm


def scan_memory_files() -> list[dict]:
    """扫描所有 memory/ 下的 .md 文件"""
    files = []
    for p in sorted(MEMORY_DIR.glob("2026-04-*.md")):
        content = p.read_text()
        fm = extract_frontmatter(content)
        # 取第一行标题
        first_line = content.split("\n")[0].lstrip("# ").strip()
        files.append({
            "name": p.name,
            "path": p,
            "date": p.stat().st_mtime,
            "title": fm.get("name", first_line),
            "description": fm.get("description", ""),
            "type": fm.get("type", "daily"),
        })
    return files


def build_index(files: list[dict]) -> str:
    """生成 MEMORY_INDEX.md 内容"""
    lines = [
        "# Memory Index — OpenClaw 记忆索引",
        f"> 自动生成于 {datetime.now().strftime('%Y-%m-%d %H:%M')}",
        "",
        "---",
        "",
        "## 📊 统计",
        "",
        f"- 每日日志: {sum(1 for f in files if f['type'] == 'daily')} 个",
        f"- 项目档案: {sum(1 for f in files if f['type'] == 'project')} 个",
        f"- 更新于: {datetime.now().strftime('%Y-%m-%d')}",
        "",
        "---",
        "",
        "## 📅 按日期索引（最近30天）",
        "",
    ]

    # 最近30天的文件
    recent = sorted(files, key=lambda x: x["date"], reverse=True)[:30]
    for f in recent:
        age = (datetime.now().timestamp() - f["date"]) / 86400
        age_tag = "🟢" if age < 1 else "🟡" if age < 7 else "🟠" if age < 30 else "🔴"
        desc = f" — {f['description']}" if f["description"] else ""
        lines.append(f"- {age_tag} `{f['name']}`{desc}")

    lines.extend(["", "---", "", "## 🏷️ 关键词快速定位", ""])

    # 按关键词聚合
    keywords = {
        "腾讯云部署": [f for f in files if "deploy" in f["name"].lower() or "腾讯" in f.get("description", "")],
        "Git清理": [f for f in files if "git" in f["name"].lower()],
        "彩色乐园": [f for f in files if "colorful" in f["name"].lower() or "park" in f["name"].lower()],
        "医学科普": [f for f in files if "med" in f["name"].lower() or "科普" in f.get("description", "")],
        "TikTok": [f for f in files if "tiktok" in f["name"].lower()],
        "壹启健康": [f for f in files if "yiqi" in f["name"].lower() or "壹启" in f.get("description", "")],
    }

    for kw, hits in keywords.items():
        if hits:
            names = ", ".join(f"`{f['name']}`" for f in hits[:5])
            lines.append(f"- **{kw}**: {names}")

    lines.extend(["", "---", ""])

    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    print("🔍 扫描 memory/ 文件...")
    files = scan_memory_files()
    print(f"   找到 {len(files)} 个文件")

    print("📝 生成索引...")
    content = build_index(files)

    if args.dry_run:
        print(content)
    else:
        INDEX_PATH.write_text(content)
        SKILL_INDEX.write_text(content)
        print(f"   ✅ 已写入 {INDEX_PATH}")
        print(f"   ✅ 已同步 {SKILL_INDEX}")


if __name__ == "__main__":
    main()

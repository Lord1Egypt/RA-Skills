#!/usr/bin/env python3
"""周蒸馏：从对话日志中提取精华，自动更新 MEMORY.md"""

import argparse
import re
import shutil
from datetime import datetime, timedelta
from pathlib import Path

DEFAULT_MEMORY_DIR = Path.home() / ".openclaw" / "workspace" / "memory"
MAX_MEMORY_SIZE = 8000  # MEMORY.md 最大字数


def get_week_dates(week_str: str) -> list[str]:
    match = re.match(r"(\d{4})-W(\d{2})", week_str)
    if not match:
        year, week = int(week_str[:4]), int(week_str.split("-W")[1])
    else:
        year, week = int(match.group(1)), int(match.group(2))
    jan4 = datetime(year, 1, 4)
    start = jan4 - timedelta(days=jan4.isoweekday() - 1) + timedelta(weeks=week - 1)
    dates = []
    for i in range(7):
        d = start + timedelta(days=i)
        if d.year == year:
            dates.append(d.strftime("%Y-%m-%d"))
    return dates


# 提取规则
EXTRACT_PATTERNS = {
    "决策": [
        r'决定[了用是]', r'确定[了用是]', r'拍板', r'就用[这个这个方案]',
        r'确认[了用]', r'选[择定]', r'方[案向]', r'最终',
    ],
    "待办": [
        r'待办', r'todo', r'记得', r'别忘了', r'回头[要得]',
        r'下一步', r'接着[做搞]', r'还需要', r'还没[做搞]',
    ],
    "偏好": [
        r'我喜欢', r'我不喜欢', r'以后[都要都别]', r'不要[给用做]',
        r'习惯[了性]', r'偏[好爱]', r'讨厌', r'反感',
    ],
    "进展": [
        r'完成[了]', r'搞定[了]', r'已[经做]', r'上线[了]',
        r'部署[了]', r'提交[了]', r'推[了送]', r'修复[了]',
    ],
}

DECISION_WORDS = set()
for words in EXTRACT_PATTERNS.values():
    DECISION_WORDS.update(words)


def extract_highlights_smart(text: str) -> dict:
    """智能提取精华，返回分类结果"""
    result = {"决策": [], "待办": [], "偏好": [], "进展": [], "话题": set()}

    # 提取标签
    tag_matches = re.findall(r'\*\*标签：\*\*\s*(.+)', text)
    for tags in tag_matches:
        for tag in tags.split("，"):
            tag = tag.strip()
            if tag:
                result["话题"].add(tag)

    # 提取话题
    topic_matches = re.findall(r'### 话题：(.+)', text)
    for topic in topic_matches:
        result["话题"].add(topic.strip().rstrip("."))

    # 按行扫描
    lines = text.split("\n")
    for i, line in enumerate(lines):
        line_stripped = line.strip()
        # 已有标记的行直接提取
        if line_stripped.startswith("**关键决策"):
            result["决策"].append(line_stripped)
        elif line_stripped.startswith("**重要"):
            result["进展"].append(line_stripped)
        elif line_stripped.startswith("- [ ]"):
            result["待办"].append(line_stripped)
        else:
            # 智能匹配：包含关键词的用户消息
            if "**用户：**" in line_stripped:
                for category, patterns in EXTRACT_PATTERNS.items():
                    for pattern in patterns:
                        if re.search(pattern, line_stripped):
                            clean = re.sub(r'\*\*用户：\*\*\s*', '', line_stripped)
                            clean = re.sub(r'\[.*?\]\s*', '', clean).strip()
                            if len(clean) <= 100:
                                result[category].append(clean)

    # 去重
    for key in ["决策", "待办", "偏好", "进展"]:
        seen = set()
        deduped = []
        for item in result[key]:
            if item not in seen:
                seen.add(item)
                deduped.append(item)
        result[key] = deduped

    return result


def format_distillation(highlights: dict, week_str: str, dates: list[str]) -> str:
    """格式化蒸馏摘要"""
    parts = [f"# {week_str} 蒸馏摘要\n", f"**覆盖日期：** {', '.join(dates)}\n"]

    if highlights["话题"]:
        parts.append(f"\n## 话题\n")
        parts.append(", ".join(sorted(highlights["话题"])) + "\n")

    sections = [
        ("决策", "### 关键决策"),
        ("进展", "### 项目进展"),
        ("待办", "### 待办事项"),
        ("偏好", "### 用户偏好"),
    ]
    for key, title in sections:
        if highlights[key]:
            parts.append(f"\n## {title}\n")
            for item in highlights[key]:
                parts.append(f"- {item}\n")

    return "\n".join(parts)


def format_distillation_json(highlights: dict, week_str: str, dates: list[str]) -> str:
    """输出 JSON 格式"""
    return json.dumps({
        "week": week_str,
        "dates": dates,
        "topics": sorted(highlights["话题"]),
        "decisions": highlights["决策"],
        "progress": highlights["进展"],
        "todos": highlights["待办"],
        "preferences": highlights["偏好"],
    }, ensure_ascii=False, indent=2)


def merge_memory_md(highlights: dict, week_str: str, memory_md_path: Path):
    """合并精华到 MEMORY.md"""
    if not memory_md_path.exists():
        memory_md_path.write_text("", encoding="utf-8")
        return

    content = memory_md_path.read_text(encoding="utf-8")

    # 新增内容
    additions = []
    if highlights["决策"]:
        additions.append(f"\n### {week_str} 决策\n" + "\n".join(f"- {d}" for d in highlights["决策"]))
    if highlights["偏好"]:
        additions.append(f"\n### {week_str} 偏好\n" + "\n".join(f"- {p}" for p in highlights["偏好"]))
    if highlights["待办"]:
        additions.append(f"\n### {week_str} 待办\n" + "\n".join(f"- {t}" for t in highlights["待办"]))

    if not additions:
        return

    # 追加到文件末尾
    new_content = content.rstrip() + "\n" + "\n".join(additions) + "\n"

    # 超限则归档旧内容
    if len(new_content) > MAX_MEMORY_SIZE:
        archive_dir = memory_md_path.parent / "archive"
        archive_dir.mkdir(parents=True, exist_ok=True)
        archive_path = archive_dir / f"MEMORY-{week_str}.md"
        archive_path.write_text(content, encoding="utf-8")
        # 重新生成精简版
        new_content = generate_compact_memory(new_content, highlights, week_str)
        new_content += f"\n\n> 旧记忆已归档到 {archive_path.relative_to(memory_md_path.parent)}\n"

    memory_md_path.write_text(new_content, encoding="utf-8")
    print(f"✅ MEMORY.md 已更新")


def generate_compact_memory(content: str, highlights: dict, week_str: str) -> str:
    """生成精简版 MEMORY.md"""
    lines = content.split("\n")
    keep = []
    in_section = False
    for line in lines:
        # 保留标题和结构
        if line.startswith("# ") or line.startswith("## "):
            keep.append(line)
            in_section = True
        elif line.startswith("### "):
            in_section = True
            keep.append(line)
        elif in_section and line.strip():
            # 保留有内容的行，但截断过长的
            if len(line) <= 200:
                keep.append(line)
    # 截断到 MAX_MEMORY_SIZE
    result = "\n".join(keep)
    if len(result) > MAX_MEMORY_SIZE:
        result = result[:MAX_MEMORY_SIZE]
    return result


def distill_week(week_str: str, memory_dir: Path, json_output: bool = False):
    conv_dir = memory_dir / "conversations"
    distill_dir = memory_dir / "distillations"
    distill_dir.mkdir(parents=True, exist_ok=True)
    dates = get_week_dates(week_str)

    all_content = []
    found_files = []
    for d in dates:
        fp = conv_dir / f"{d}.md"
        if fp.exists():
            found_files.append(d)
            all_content.append(fp.read_text(encoding="utf-8"))

    if not found_files:
        print(f"⚠️ 未找到 {week_str} 的对话记录")
        return

    all_highlights = {"决策": [], "待办": [], "偏好": [], "进展": [], "话题": set()}
    for content in all_content:
        h = extract_highlights_smart(content)
        for key in ["决策", "待办", "偏好", "进展"]:
            all_highlights[key].extend(h[key])
        all_highlights["话题"].update(h["话题"])

    if json_output:
        output = format_distillation_json(all_highlights, week_str, found_files)
        print(output)
    else:
        output = format_distillation(all_highlights, week_str, found_files)

    distill_path = distill_dir / f"{week_str}.md"
    distill_path.write_text(output, encoding="utf-8")
    print(f"✅ 蒸馏完成 → {distill_path}")
    print(f"  📝 覆盖 {len(found_files)} 天的对话记录")
    print(f"  💡 话题: {', '.join(sorted(all_highlights['话题'])) or '无'}")
    print(f"  🎯 决策: {len(all_highlights['决策'])} 条")
    print(f"  📋 待办: {len(all_highlights['待办'])} 条")
    print(f"  ❤️ 偏好: {len(all_highlights['偏好'])} 条")

    # 自动更新 MEMORY.md
    memory_md = memory_dir.parent / "MEMORY.md"
    merge_memory_md(all_highlights, week_str, memory_md)


if __name__ == "__main__":
    import json
    p = argparse.ArgumentParser(description="周蒸馏")
    p.add_argument("--week", default=datetime.now().strftime("%Y-W%V"))
    p.add_argument("--memory-dir", default=None)
    p.add_argument("--json", action="store_true", help="JSON 格式输出")
    args = p.parse_args()

    md = args.memory_dir if args.memory_dir else DEFAULT_MEMORY_DIR
    md = Path(md)
    md.mkdir(parents=True, exist_ok=True)
    distill_week(args.week, md, args.json)

#!/usr/bin/env python3
"""
Skill Extractor — 从对话历史中提取技能文档
参考 Hermes Agent 的 Skill Documents 机制

用法:
  python extract_skill.py --task "任务描述" --conversation "对话历史"
  python extract_skill.py --session-id <session_id>
"""

import argparse
import json
import re
import sys
from datetime import datetime
from pathlib import Path
from typing import Optional

SKILLS_DIR = Path.home() / ".openclaw" / "workspace" / "skills" / "skill-extractor" / "skills"
SKILLS_DIR.mkdir(parents=True, exist_ok=True)


def extract_skill_from_conversation(task: str, conversation: str) -> dict:
    """
    分析对话历史，提取技能信息
    返回: {name, description, when_to_use, steps, notes}
    """
    # 简单分析：识别工具调用序列和关键步骤
    lines = conversation.strip().split("\n")
    
    # 找出工具调用（假设格式为 "Tool: tool_name" 或 "using <tool>"）
    tool_patterns = [
        r"(?:Using|call|exec|run)\s+`?(\w+)`?",
        r"(?:Tool|Command):\s*(\w+)",
        r"→\s*(\w+)\s*\(",
    ]
    
    tools_used = []
    for line in lines:
        for pattern in tool_patterns:
            matches = re.findall(pattern, line, re.IGNORECASE)
            tools_used.extend(matches)
    
    # 去重但保持顺序
    seen = set()
    tools_used = [x for x in tools_used if not (x in seen or seen.add(x))]
    
    # 生成技能名称（从任务描述提取关键词）
    keywords = [w for w in re.findall(r"\b\w{3,}\b", task) if w.lower() not in STOP_WORDS][:3]
    skill_name = "_".join(keywords).lower() if keywords else "custom_task"
    
    # 提取步骤（简单方法：按序号或箭头分隔）
    steps = []
    step_patterns = [
        r"(?:\d+[.)]\s*)(.*?)(?=\n\d+[.)]|\n$)",
        r"(?:[-•]\s*)(.*?)(?=\n[-•]|\n$)",
    ]
    
    for pattern in step_patterns:
        matches = re.findall(pattern, conversation, re.MULTILINE)
        if matches:
            steps = [s.strip() for s in matches if len(s.strip()) > 10]
            break
    
    return {
        "name": skill_name,
        "description": f"从任务「{task[:50]}」中提取的技能",
        "when_to_use": f"处理类似「{task[:80]}」的任务时使用",
        "tools_used": tools_used,
        "steps": steps or ["无法自动提取步骤，请手动描述"],
        "extracted_at": datetime.now().isoformat(),
    }


def generate_skill_markdown(skill: dict) -> str:
    """生成 SKILL.md 格式的技能文档"""
    md = f"""---
name: {skill['name']}
description: {skill['description']}
---

# {skill['name'].replace('_', ' ').title()}

## When to Use
- {skill['when_to_use']}

## Tools Used
{', '.join(f'`{t}`' for t in skill['tools_used']) if skill['tools_used'] else '无特定工具'}

## Procedure
"""
    for i, step in enumerate(skill["steps"], 1):
        md += f"{i}. {step}\n"
    
    md += f"""
## Notes
- 自动提取自对话记录
- 提取时间: {skill['extracted_at'][:10]}

---
*此技能由 skill-extractor 自动生成*
"""
    return md


def save_skill(skill: dict) -> str:
    """保存技能到仓库，返回文件路径"""
    filename = f"{skill['name']}_{skill['extracted_at'][:10]}.md"
    filepath = SKILLS_DIR / filename
    
    md = generate_skill_markdown(skill)
    filepath.write_text(md, encoding="utf-8")
    
    return str(filepath)


def search_skills(query: str) -> list:
    """搜索相关技能（简单关键词匹配）"""
    results = []
    query_words = set(query.lower().split())
    
    for f in SKILLS_DIR.glob("*.md"):
        content = f.read_text(encoding="utf-8").lower()
        
        # 简单评分：匹配词数
        matches = sum(1 for w in query_words if w in content)
        if matches > 0:
            # 读取描述
            desc_match = re.search(r"description:\s*(.+)", content)
            desc = desc_match.group(1)[:80] if desc_match else "无描述"
            
            results.append({
                "file": f.name,
                "score": matches,
                "description": desc,
                "path": str(f),
            })
    
    # 按分数排序
    results.sort(key=lambda x: x["score"], reverse=True)
    return results[:5]


def main():
    parser = argparse.ArgumentParser(description="从对话中提取技能")
    parser.add_argument("--task", required=True, help="任务描述")
    parser.add_argument("--conversation", required=True, help="对话历史（多行文本）")
    parser.add_argument("--save", action="store_true", help="保存技能")
    parser.add_argument("--search", help="搜索相关技能")
    
    args = parser.parse_args()
    
    if args.search:
        results = search_skills(args.search)
        print(json.dumps(results, ensure_ascii=False, indent=2))
        return
    
    # 提取技能
    skill = extract_skill_from_conversation(args.task, args.conversation)
    print("=== 提取的技能 ===")
    print(json.dumps(skill, ensure_ascii=False, indent=2))
    
    # 生成 markdown 并显示
    print("\n=== SKILL.md 预览 ===")
    print(generate_skill_markdown(skill))
    
    if args.save:
        path = save_skill(skill)
        print(f"\n✅ 已保存到: {path}")


STOP_WORDS = {
    "the", "a", "an", "is", "are", "was", "were", "be", "been", "being",
    "have", "has", "had", "do", "does", "did", "will", "would", "could",
    "should", "may", "might", "must", "can", "to", "of", "in", "for",
    "on", "with", "at", "by", "from", "as", "into", "through", "during",
    "before", "after", "above", "below", "between", "under", "again",
    "further", "then", "once", "here", "there", "when", "where", "why",
    "how", "all", "each", "few", "more", "most", "other", "some", "such",
    "no", "nor", "not", "only", "own", "same", "so", "than", "too", "very",
    "just", "and", "but", "if", "or", "because", "until", "while", "this",
    "that", "these", "those", "it", "its", "they", "them", "their", "what",
    "which", "who", "whom", "我们", "你", "我", "他", "她", "它", "的",
    "了", "是", "在", "有", "和", "与", "或", "这", "那", "就", "也",
}


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""
Suggest skill extraction after task completion.
This is the "nudge" mechanism inspired by Hermes Agent.

After a complex task completes, this script analyzes the conversation
and suggests whether to extract a skill.

Usage:
  python suggest_skill.py --task "任务描述" --conversation "对话历史"
  python suggest_skill.py --session-id <id> --check  # auto-check mode
"""

import argparse
import json
import re
import sys
from datetime import datetime
from pathlib import Path
from typing import Optional

# Thresholds for triggering skill extraction suggestion
MIN_TURNS = 5           # 至少5轮对话
MIN_TOOLS = 2           # 至少2个工具调用
MIN_STEPS = 3           # 至少3个明确步骤


def analyze_complexity(task: str, conversation: str) -> dict:
    """
    分析任务复杂度，判断是否值得提取技能
    返回: {complexity, score, reasons, should_extract}
    """
    lines = conversation.strip().split("\n") if conversation else []
    turns = len([l for l in lines if l.strip()])
    
    # 统计工具调用
    tool_patterns = [
        r"(?:Using|call|exec|run)\s+`?(\w+)`?",
        r"(?:Tool|Command):\s*(\w+)",
        r"→\s*(\w+)\s*\(",
        r"(?:Tool call|function call):\s*(\w+)",
    ]
    
    tools_found = set()
    for line in lines:
        for pattern in tool_patterns:
            matches = re.findall(pattern, line, re.IGNORECASE)
            tools_found.update(matches)
    
    # 统计明确步骤（序号列表）
    steps_patterns = [
        r"(?:\d+[.]\s+)(.{10,})",
        r"(?:[-•]\s+)(.{10,})",
        r"(?:→\s+)(.{10,})",
    ]
    
    steps_found = []
    for pattern in steps_patterns:
        matches = re.findall(pattern, conversation, re.MULTILINE)
        steps_found.extend(matches)
    
    # 计算复杂度分数
    score = 0
    reasons = []
    
    if turns >= MIN_TURNS:
        score += turns * 2
        reasons.append(f"多轮对话: {turns}轮")
    
    if len(tools_found) >= MIN_TOOLS:
        score += len(tools_found) * 3
        reasons.append(f"多工具调用: {', '.join(list(tools_found)[:5])}")
    
    if len(steps_found) >= MIN_STEPS:
        score += len(steps_found) * 2
        reasons.append(f"明确步骤: {len(steps_found)}步")
    
    # 检查是否有特殊模式（罕见问题/特殊解决方案）
    special_patterns = [
        r"(?:首次|第一次|第一次遇到)",
        r"(?:之前|以往|历史上)",
        r"(?:特殊|罕见|少见)",
        r"(?:自定义|特殊处理|变通)",
        r"(?:修复|debug|排查)",
    ]
    
    for pattern in special_patterns:
        if re.search(pattern, conversation):
            score += 5
            reasons.append("包含特殊/罕见处理")
            break
    
    # 判断是否应该提取
    should_extract = score >= 15 and (turns >= MIN_TURNS or len(tools_found) >= MIN_TOOLS)
    
    return {
        "complexity": "high" if score >= 20 else "medium" if score >= 10 else "low",
        "score": score,
        "reasons": reasons,
        "turns": turns,
        "tools": list(tools_found),
        "steps": len(steps_found),
        "should_extract": should_extract,
        "suggestion": make_suggestion(score, turns, tools_found, steps_found),
    }


def make_suggestion(score: int, turns: int, tools: set, steps: int) -> str:
    """生成提取建议文本"""
    if score >= 20:
        verb = "强烈建议"
    elif score >= 15:
        verb = "建议"
    elif score >= 10:
        verb = "可以考虑"
    else:
        return "任务较简单，不需要提取技能。"
    
    tools_str = ", ".join(list(tools)[:4]) if tools else "无特定工具"
    return (
        f"{verb}将此任务提取为可复用技能。\n"
        f"理由：{turns}轮对话，使用了 {tools_str}，"
        f"包含 {steps} 个明确步骤。\n"
        f"提取后可帮助处理类似任务。"
    )


def generate_skill_preview(task: str, conversation: str) -> Optional[str]:
    """生成技能文档预览（供用户确认）"""
    analysis = analyze_complexity(task, conversation)
    
    if not analysis["should_extract"]:
        return None
    
    # 提取技能名称
    keywords = [w for w in re.findall(r"\b\w{3,}\b", task) 
                if w.lower() not in STOP_WORDS and not w.isdigit()][:3]
    skill_name = "_".join(keywords).lower() if keywords else "custom_task"
    
    # 生成技能文档
    preview = f"""---
name: {skill_name}
description: 从任务「{task[:60]}」中提取的技能
---

# {skill_name.replace('_', ' ').title()}

## When to Use
- 处理类似「{task[:80]}」的任务时使用

## Tools Used
{', '.join(f'`{t}`' for t in analysis['tools']) if analysis['tools'] else '无特定工具'}

## Procedure
"""
    # 尝试提取步骤
    steps_found = []
    for pattern in [r"(?:\d+[.]\s+)(.{10,200}?)(?=\n\d+[.]|\n\n|$)", 
                    r"(?:[-•]\s+)(.{10,200}?)(?=\n[-•]|\n\n|$)"]:
        matches = re.findall(pattern, conversation, re.MULTILINE)
        if matches:
            steps_found = [s.strip() for s in matches[:10] if len(s.strip()) > 15]
            break
    
    if steps_found:
        for i, step in enumerate(steps_found, 1):
            preview += f"{i}. {step}\n"
    else:
        preview += f"{len(preview.split(chr(10)))} [从对话中提取步骤]\n"
    
    preview += f"""
## Notes
- 自动提取自 {datetime.now().strftime('%Y-%m-%d')} 的对话记录
- 复杂度评分: {analysis['score']}/30

---
*此技能由 skill-extractor 自动生成*
"""
    return preview


def main():
    parser = argparse.ArgumentParser(description="分析任务复杂度并建议技能提取")
    parser.add_argument("--task", required=True, help="任务描述")
    parser.add_argument("--conversation", required=True, help="对话历史")
    parser.add_argument("--auto", action="store_true", help="自动模式：仅输出结果，不显示预览")
    parser.add_argument("--json", action="store_true", help="JSON格式输出")
    
    args = parser.parse_args()
    
    analysis = analyze_complexity(args.task, args.conversation)
    
    if args.json:
        print(json.dumps(analysis, ensure_ascii=False, indent=2))
        return
    
    if analysis["should_extract"]:
        print("=" * 50)
        print("🧠 技能提取建议")
        print("=" * 50)
        print(f"复杂度: {analysis['complexity'].upper()} (分数: {analysis['score']})")
        print(f"原因: {', '.join(analysis['reasons'])}")
        print()
        print(analysis["suggestion"])
        print()
        
        if not args.auto:
            preview = generate_skill_preview(args.task, args.conversation)
            if preview:
                print("=" * 50)
                print("📄 技能文档预览:")
                print("=" * 50)
                print(preview)
    else:
        print(f"任务复杂度: {analysis['complexity']} (分数: {analysis['score']})")
        print("不需要提取技能。")


STOP_WORDS = {
    "the", "a", "an", "is", "are", "was", "were", "be", "been", "being",
    "have", "has", "had", "do", "does", "did", "will", "would", "could",
    "should", "may", "might", "must", "can", "to", "of", "in", "for",
    "on", "with", "at", "by", "from", "as", "into", "through", "during",
    "before", "after", "above", "below", "between", "under", "again",
    "further", "then", "once", "here", "there", "when", "where", "why",
    "how", "all", "each", "few", "more", "most", "other", "some", "such",
    "no", "nor", "not", "only", "own", "same", "so", "than", "too", "very",
    "just", "and", "but", "if", "or", "because", "until", "while",
    "this", "that", "these", "those", "it", "its", "they", "them", "their",
    "what", "which", "who", "whom", "one", "two", "three", "four", "five",
}


if __name__ == "__main__":
    main()

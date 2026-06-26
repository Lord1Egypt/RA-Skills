"""
Action Item Extractor - Extract tasks from meeting transcripts
Author: ClawHub Skill
"""

import re
from typing import Dict, List
import json


def extract_actions(transcript_path: str) -> List[Dict]:
    """
    Extract action items from meeting transcript.
    
    Args:
        transcript_path: Path to transcript file
    
    Returns:
        List of action item dictionaries
    """
    try:
        with open(transcript_path, 'r', encoding='utf-8') as f:
            text = f.read()
    except Exception as e:
        return [{"error": f"Failed to read transcript: {e}"}]
    
    action_items = []
    
    # Pattern 1: "X needs to do Y"
    pattern1 = re.finditer(
        r'(\w+)[\s需要必须负责跟进]*(做|完成|处理|跟进|提交|准备|研究|分析|审查|测试|实现|部署)[：:]?\s*([^。\n]+)',
        text
    )
    for match in pattern1:
        assignee = match.group(1)
        action = match.group(2)
        task = match.group(3).strip()
        action_items.append({
            "assignee": assignee,
            "action_verb": action,
            "task": task,
            "priority": "medium",
            "confidence": "high"
        })
    
    # Pattern 2: "Action item: ..."
    pattern2 = re.finditer(
        r'(action item|task|todo|待办)[：:]\s*([^。\n]+)(?:[，,]\s*(\w+)[负责跟进])?',
        text,
        re.IGNORECASE
    )
    for match in pattern2:
        task = match.group(2).strip()
        assignee = match.group(3) if match.group(3) else "TBD"
        action_items.append({
            "assignee": assignee,
            "task": task,
            "priority": "high",
            "confidence": "high"
        })
    
    # Pattern 3: "By next week, X should..."
    pattern3 = re.finditer(
        r'(截止|by|before|在)[\s\w]*[,，]?\s*(\w+)[必须需要]*(做|完成|提交)[：:]?\s*([^。\n]+)',
        text,
        re.IGNORECASE
    )
    for match in pattern3:
        assignee = match.group(2)
        task = match.group(4).strip()
        action_items.append({
            "assignee": assignee,
            "task": task,
            "priority": "high",
            "confidence": "medium"
        })
    
    # Remove duplicates
    unique_items = []
    seen = set()
    for item in action_items:
        key = f"{item['assignee']}:{item['task']}"
        if key not in seen:
            seen.add(key)
            unique_items.append(item)
    
    return unique_items


def export_actions_to_json(actions: List[Dict], output_path: str) -> bool:
    """
    Export action items to JSON file.
    
    Args:
        actions: List of action item dictionaries
        output_path: Path to save JSON file
    
    Returns:
        True if successful
    """
    try:
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(actions, f, ensure_ascii=False, indent=2)
        return True
    except Exception as e:
        print(f"Error exporting actions: {e}")
        return False


def format_actions_as_markdown(actions: List[Dict]) -> str:
    """
    Format action items as markdown checklist.
    
    Args:
        actions: List of action item dictionaries
    
    Returns:
        Markdown formatted string
    """
    md = "## Action Items\n\n"
    md += "| # | Task | Assignee | Priority | Status |\n"
    md += "|---|------|----------|----------|--------|\n"
    
    for i, action in enumerate(actions, 1):
        task = action.get('task', 'N/A')[:50]
        assignee = action.get('assignee', 'TBD')
        priority = action.get('priority', 'medium')
        md += f"| {i} | {task} | {assignee} | {priority} | [ ] |\n"
    
    return md


if __name__ == "__main__":
    print("Action Item Extractor")
    print("=" * 50)

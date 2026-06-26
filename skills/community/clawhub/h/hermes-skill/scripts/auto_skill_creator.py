#!/usr/bin/env python3
"""
Auto-Skill Creator - 从复杂任务自动生成 skill
参考 Hermes Agent 的 skill_manage 机制
"""

import os
import json
import re
from datetime import datetime
from pathlib import Path

SKILLS_DIR = Path.home() / "self-improving" / "skills"
MEMORY_DIR = Path.home() / "self-improving"

def load_task_history():
    """加载任务历史 - 从会话历史中提取"""
    history_file = MEMORY_DIR / "task_history.json"
    if history_file.exists():
        with open(history_file) as f:
            return json.load(f)
    return []

def analyze_complexity(tool_calls_count, error_count, steps):
    """分析任务复杂度"""
    if tool_calls_count >= 10:
        return "high"
    elif tool_calls_count >= 5:
        return "medium"
    return "low"

def generate_skill_name(task_type):
    """生成 skill 名称"""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    safe_name = re.sub(r'[^a-z0-9]', '-', task_type.lower())
    return f"auto-{timestamp}-{safe_name[:30]}"

def create_skill_from_task(task_data):
    """从任务数据创建 skill"""
    skill_name = generate_skill_name(task_data.get("type", "task"))
    skill_dir = SKILLS_DIR / skill_name
    skill_dir.mkdir(parents=True, exist_ok=True)
    
    content = f"""---
name: {skill_name}
description: {task_data.get('description', 'Auto-generated skill')}
version: 1.0.0
auto_generated: true
trigger: {task_data.get('trigger', 'complex-task')}
created_at: {datetime.now().isoformat()}
---

# {task_data.get('title', 'Auto-generated Skill')}

## 何时使用
{task_data.get('description', '处理相关任务时使用')}

## 工作流
"""
    
    for i, step in enumerate(task_data.get("steps", []), 1):
        content += f"{i}. {step}\n"
    
    content += f"""
## 关键要点
"""
    for point in task_data.get("key_points", []):
        content += f"- {point}\n"
    
    content += f"""
## 验证
{task_data.get('verification', '任务完成后确认结果')}

## 使用记录
| 日期 | 评分 | 改进 |
|------|------|------|
"""
    
    # 写入 SKILL.md
    with open(skill_dir / "SKILL.md", "w") as f:
        f.write(content)
    
    # 写入 _meta.json
    meta = {
        "name": skill_name,
        "auto_generated": True,
        "created_at": datetime.now().isoformat(),
        "usage_count": 0,
        "avg_rating": None
    }
    with open(skill_dir / "_meta.json", "w") as f:
        json.dump(meta, f, indent=2)
    
    return skill_name

def evaluate_skill(skill_name, rating):
    """评估 skill 效果"""
    meta_file = SKILLS_DIR / skill_name / "_meta.json"
    if not meta_file.exists():
        return
    
    with open(meta_file) as f:
        meta = json.load(f)
    
    # 更新评分
    meta["usage_count"] = meta.get("usage_count", 0) + 1
    
    if meta["avg_rating"] is None:
        meta["avg_rating"] = rating
    else:
        meta["avg_rating"] = (meta["avg_rating"] * (meta["usage_count"] - 1) + rating) / meta["usage_count"]
    
    # 如果评分低，建议改进
    if rating < 3:
        meta["needs_improvement"] = True
    
    with open(meta_file, "w") as f:
        json.dump(meta, f, indent=2)
    
    return meta

def main():
    """主函数"""
    import argparse
    parser = argparse.ArgumentParser(description="Auto-Skill Creator")
    parser.add_argument("--create", action="store_true", help="从任务历史创建 skill")
    parser.add_argument("--task", type=str, help="任务描述 JSON")
    parser.add_argument("--evaluate", type=str, help="评估 skill: skill_name,rating")
    parser.add_argument("--list", action="store_true", list=True, help="列出所有 auto-generated skills")
    
    args = parser.parse_args()
    
    if args.list:
        # 列出所有 skills
        if not SKILLS_DIR.exists():
            print("No skills found")
            return
        for skill_dir in SKILLS_DIR.iterdir():
            if skill_dir.is_dir():
                print(f"- {skill_dir.name}")
        return
    
    if args.task:
        # 从任务创建 skill
        task_data = json.loads(args.task)
        skill_name = create_skill_from_task(task_data)
        print(f"Created skill: {skill_name}")
    
    if args.evaluate:
        # 评估 skill
        skill_name, rating = args.evaluate.split(",")
        rating = int(rating)
        meta = evaluate_skill(skill_name, rating)
        print(f"Evaluated {skill_name}: {rating}/5, avg={meta['avg_rating']:.1f}")

if __name__ == "__main__":
    main()

"""
Meta-Skill Generator - 自动生成新技能
"""
import json
import re
from pathlib import Path
from datetime import datetime

# Paths
# 获取项目根目录（相对于当前文件位置）
SKILLS_ROOT = Path(__file__).parent.parent / "skills"
SKILLS_DB = SKILLS_ROOT / "meta-skill-generator" / "skills_db.json"
GENERATED_DIR = SKILLS_ROOT / "meta-skill-generator" / "generated"

def load_db():
    if SKILLS_DB.exists():
        with open(SKILLS_DB, "r", encoding="utf-8") as f:
            return json.load(f)
    return {"skills": []}

def generate_skill(skill_name: str, description: str, trigger_phrases: list) -> dict:
    """Generate a new skill based on description"""
    
    # Convert name to hyphen-case
    skill_id = skill_name.lower().replace(" ", "-")
    
    # Extract keywords
    keywords = []
    for phrase in trigger_phrases + description.split():
        word = re.sub(r'[^a-zA-Z]', '', phrase.lower())
        if len(word) > 2:
            keywords.append(word)
    keywords = list(set(keywords))[:10]
    
    # Generate SKILL.md content
    skill_md = f"""---
name: {skill_id}
description: |
  {description}
  
  触发场景：
{chr(10).join(f'  {i+1}. "{phrase}"' for i, phrase in enumerate(trigger_phrases))}
metadata: {{"openclaw":{{"emoji":"⚙️"}}}}
---

# {skill_name}

> 自动生成的技能

## 功能

{description}

## 触发条件

{chr(10).join(f'- "{phrase}"' for phrase in trigger_phrases)}

## 使用方法

（待完善）

## 注意事项

- 此技能由 meta-skill-generator 自动生成
- 生成时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
"""
    
    return {
        "name": skill_id,
        "skill_name": skill_name,
        "description": description,
        "trigger_phrases": trigger_phrases,
        "keywords": keywords,
        "content": skill_md
    }

def save_generated_skill(skill_data: dict):
    """Save generated skill to disk"""
    GENERATED_DIR.mkdir(parents=True, exist_ok=True)
    
    skill_dir = GENERATED_DIR / skill_data["name"]
    skill_dir.mkdir(parents=True, exist_ok=True)
    
    # Write SKILL.md
    skill_file = skill_dir / "SKILL.md"
    skill_file.write_text(skill_data["content"], encoding="utf-8")
    
    return str(skill_dir)

def generate_and_save(skill_name: str, description: str, trigger_phrases: list):
    """Generate and save a new skill"""
    print(f"\n=== Generating Skill: {skill_name} ===")
    
    # Generate
    skill_data = generate_skill(skill_name, description, trigger_phrases)
    
    print(f"Name: {skill_data['name']}")
    print(f"Description: {skill_data['description']}")
    print(f"Keywords: {skill_data['keywords']}")
    print(f"Triggers: {skill_data['trigger_phrases']}")
    
    # Save
    path = save_generated_skill(skill_data)
    print(f"\n[OK] Saved to: {path}")
    
    return skill_data

# Test
if __name__ == "__main__":
    print("=== Meta-Skill Generator - Auto Generate ===\n")
    
    # Example: Generate a "reminder" skill
    result = generate_and_save(
        skill_name="reminder",
        description="定时提醒技能，支持一次性和周期性提醒",
        trigger_phrases=["提醒我", "设置提醒", "remind me", "alarm"]
    )
    
    print("\n=== Generated SKILL.md ===")
    print(result["content"][:500] + "...")

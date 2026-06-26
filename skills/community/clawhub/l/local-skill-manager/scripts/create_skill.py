import os
import sys
import re

def create_skill(skill_name):
    # Validate skill name
    if not re.match(r'^[a-z0-9-]+$', skill_name):
        print("Error: Skill name must only contain lowercase letters, numbers, and hyphens.")
        return

    # Determine paths
    current_dir = os.path.dirname(os.path.abspath(__file__))
    # Go up from scripts/ to local-skill-manager/ to skills/
    skills_root = os.path.abspath(os.path.join(current_dir, '../../'))
    
    new_skill_dir = os.path.join(skills_root, skill_name)
    
    if os.path.exists(new_skill_dir):
        print(f"Error: Skill '{skill_name}' already exists.")
        return

    print(f"Creating new skill '{skill_name}' at {new_skill_dir}...")
    
    try:
        # Create directories
        os.makedirs(os.path.join(new_skill_dir, 'scripts'), exist_ok=True)
        os.makedirs(os.path.join(new_skill_dir, 'assets'), exist_ok=True)
        os.makedirs(os.path.join(new_skill_dir, 'references'), exist_ok=True)
        
        # Create SKILL.md template
        skill_md_content = f"""---
name: {skill_name}
description: [Short description of what this skill does]
triggers:
  - {skill_name.replace('-', ' ')}
version: 0.1.0
---

# {skill_name.replace('-', ' ').title()}

## Overview
[Detailed description of the skill]

## Usage
[How to use this skill]
"""
        
        with open(os.path.join(new_skill_dir, 'SKILL.md'), 'w', encoding='utf-8') as f:
            f.write(skill_md_content)
            
        print(f"Skill '{skill_name}' created successfully!")
    except Exception as e:
        print(f"Error creating skill: {e}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python create_skill.py <skill_name>")
    else:
        create_skill(sys.argv[1])

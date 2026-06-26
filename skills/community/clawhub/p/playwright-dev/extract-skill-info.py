# 整理 Skill 信息的脚本
import json
import os
from pathlib import Path
from datetime import datetime

skills_dir = r"C:\Users\Xiabi\.openclaw\workspace\skills"
memory_dir = r"C:\Users\Xiabi\.openclaw\workspace\memory"

# 获取所有 skill 信息
skills = []
for skill_folder in os.listdir(skills_dir):
    skill_path = os.path.join(skills_dir, skill_folder, "SKILL.md")
    if os.path.exists(skill_path):
        stat = os.stat(skill_path)
        skills.append({
            "name": skill_folder,
            "create_time": datetime.fromtimestamp(stat.st_ctime).strftime("%Y-%m-%d %H:%M"),
            "modify_time": datetime.fromtimestamp(stat.st_mtime).strftime("%Y-%m-%d %H:%M"),
            "path": skill_path
        })

# 按创建时间排序
skills.sort(key=lambda x: x["create_time"])

# 输出为 JSON
print(json.dumps(skills, ensure_ascii=False, indent=2))

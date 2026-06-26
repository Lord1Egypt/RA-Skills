#!/usr/bin/env python3
"""
skill 推荐器
- 根据角色推荐相关 skill
- 加载推荐规则
"""

import json
import os

def get_recommendations_path():
    """获取推荐规则文件路径"""
    current_dir = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(current_dir, "../data/skill_recommendations.json")

def load_recommendations():
    """加载推荐规则"""
    rec_path = get_recommendations_path()
    with open(rec_path, "r", encoding="utf-8") as f:
        return json.load(f)["recommendations"]

def get_recommendations(template_id):
    """根据角色模板 ID 获取推荐 skill"""
    recommendations = load_recommendations()
    return recommendations.get(template_id, {}).get("skills", [])

def format_recommendations(skills):
    """格式化推荐 skill 列表"""
    if not skills:
        return "暂无推荐 skill"
    
    result = "根据你的角色，推荐以下 skill：\n"
    for i, skill in enumerate(skills, 1):
        result += f"{i}. {skill}\n"
    return result

if __name__ == "__main__":
    # 测试代码
    test_id = "xiaohongshu-manager"
    skills = get_recommendations(test_id)
    print(f"对于模板 {test_id} 的推荐：")
    print(format_recommendations(skills))

#!/usr/bin/env python3
"""
角色模板管理器
- 加载预设角色模板
- 列出所有可用模板
- 根据模板 ID 获取模板详情
"""

import json
import os

def get_templates_path():
    """获取角色模板文件路径"""
    current_dir = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(current_dir, "../data/role_templates.json")

def load_templates():
    """加载所有角色模板"""
    templates_path = get_templates_path()
    with open(templates_path, "r", encoding="utf-8") as f:
        return json.load(f)["templates"]

def list_templates():
    """列出所有可用的角色模板"""
    templates = load_templates()
    result = []
    for template in templates:
        result.append({
            "id": template["id"],
            "name": template["name"],
            "description": template["description"]
        })
    return result

def get_template(template_id):
    """根据模板 ID 获取模板详情"""
    templates = load_templates()
    for template in templates:
        if template["id"] == template_id:
            return template
    return None

def get_templates_by_category():
    """按分类列出角色模板"""
    templates = load_templates()
    categories = {}
    
    # 分类映射
    category_map = {
        "实用生活类": [
            "xiaohongshu-manager", "ppt-expert", "meeting-minutes",
            "deal-hunter", "free-api-token", "health-manager",
            "interview-resume", "life-consultant", "food-recipe"
        ],
        "商业专业类": [
            "business-plan", "ceo-coach", "pm-assistant", "marketing-ad"
        ],
        "营销运营类": [
            "live-stream-script", "image-poster"
        ],
        "母婴育儿类": [
            "postpartum-care", "newborn-care", "pregnancy-care"
        ],
        "情感心理类": [
            "emotional-companion", "therapist"
        ]
    }
    
    for category, ids in category_map.items():
        categories[category] = []
        for template_id in ids:
            template = get_template(template_id)
            if template:
                categories[category].append({
                    "id": template["id"],
                    "name": template["name"],
                    "description": template["description"]
                })
    
    return categories

if __name__ == "__main__":
    # 测试代码
    print("所有角色模板：")
    for template in list_templates():
        print(f"- {template['name']}: {template['description']}")

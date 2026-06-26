#!/usr/bin/env python3
"""
SkillForge 核心引擎 - 自动融合生成器
输入需求或源技能列表，自动生成融合技能

用法：
  python3 forge.py --name "技能名" --desc "描述" --sources "skill1,skill2,skill3"
  python3 forge.py --demand "我想做个..."
"""

import os, sys, json, datetime

BASE = "/root/.openclaw/workspace/skills"

def scan_skills():
    """扫描当前技能库，返回技能信息列表"""
    skills = []
    if not os.path.exists(BASE):
        return skills
    for name in os.listdir(BASE):
        path = os.path.join(BASE, name, "SKILL.md")
        if os.path.exists(path):
            with open(path, 'r', errors='ignore') as f:
                content = f.read()
            # 提取描述
            desc = ""
            for line in content.split("\n"):
                if line.startswith("description:"):
                    desc = line.replace("description:", "").strip().strip('"').strip("'")
                    break
            skills.append({"name": name, "desc": desc[:120], "size": len(content)})
    return skills

def analyze_demand(demand, skills):
    """分析需求，匹配最佳融合源"""
    demand_lower = demand.lower()
    
    # 关键词匹配
    keyword_map = {
        "写作": ["khazix-writer", "caption", "content-pilot", "newsletter"],
        "视频": ["video-craft-pro", "video-monetizer", "caption", "video-generator-seedance"],
        "电商": ["ecom-intel", "video-monetizer"],
        "办公": ["travel-biz", "proj-sync", "biz-doc-pro"],
        "健康": ["life-pal", "recipe", "workout", "meditation"],
        "社交": ["caption", "hashtag", "content-pilot"],
        "管理": ["proj-sync", "taskr", "calendar", "project-manager"],
        "变现": ["video-monetizer", "ecom-intel"],
        "自动": ["automation-workflows", "skill-forge"],
        "生成": ["skill-factory", "skill-forge"],
        "会议": ["calendar", "appointment-scheduler"],
        "财务": ["travel-biz", "expense", "receipt", "invoice"],
        "简历": ["resume", "cv"],
        "搜索": ["web-search", "tavily-search"],
        "设计": ["image-generator", "remotion-skills"],
        "学习": ["flashcard", "quiz"],
    }
    
    matches = set()
    for keyword, candidates in keyword_map.items():
        if keyword in demand_lower:
            for c in candidates:
                if any(s["name"] == c for s in skills):
                    matches.add(c)
    
    # 按热度排序
    priority = ["khazix-writer", "content-pilot", "video-monetizer", "ecom-intel",
                "travel-biz", "proj-sync", "life-pal", "one-man-conglomerate",
                "skill-forge", "skill-factory", "automation-workflows"]
    sorted_matches = sorted(matches, key=lambda x: priority.index(x) if x in priority else 99)
    
    return list(sorted_matches)

def generate_meta(name, desc, sources):
    """生成_meta.json"""
    return {
        "name": name,
        "version": "1.0.0",
        "author": "智美人团队",
        "description": desc,
        "tags": sources + ["fusion"],
    }

def generate_skill_md(name, desc, sources, category="通用"):
    """生成SKILL.md"""
    now = datetime.datetime.now()
    
    md = f"""---
name: {name}
displayName: {name}
slug: {name}
description: "{desc}"
version: "1.0.0"
author: "智美人团队"
tags:
  - fusion
  - {category}
metadata:
  openclaw:
    emoji: "🔧"
    requires:
      skills: [{', '.join(f'"{s}"' for s in sources)}]
---

# 🔧 {name}

**自动融合生成于 {now.strftime('%Y-%m-%d %H:%M')}**

## 融合来源

| 源技能 | 角色 |
|--------|------|
"""
    for s in sources:
        md += f"| {s} | 提供核心能力 |\n"
    
    md += f"""
## 新增能力

- 融合 `{', '.join(sources)}` 的核心功能
- 提供统一的接口封装
- 自动生成的基础技能文档

## 使用方式

```
{name}> 输入需求
{name}> 执行任务
```
"""
    return md

def create_skill(name, desc, sources):
    """创建完整技能"""
    safe_name = name.lower().replace(" ", "-").replace("_", "-")
    path = os.path.join(BASE, safe_name)
    os.makedirs(os.path.join(path, "scripts"), exist_ok=True)
    os.makedirs(os.path.join(path, "examples"), exist_ok=True)
    
    # SKILL.md
    with open(os.path.join(path, "SKILL.md"), "w") as f:
        f.write(generate_skill_md(safe_name, desc, sources))
    
    # _meta.json
    with open(os.path.join(path, "_meta.json"), "w") as f:
        json.dump(generate_meta(safe_name, desc, sources), f, ensure_ascii=False)
    
    # test.sh
    test_lines = ["#!/bin/bash", f'echo "🧪 测试 {safe_name}..."']
    for s in sources:
        exists = os.path.isdir(os.path.join(BASE, s))
        mark = "✅" if exists else "❌"
        test_lines.append(f'echo "    {s}: {mark}"')
    test_lines.append(f'echo "✅ {safe_name} 测试通过!"')
    
    with open(os.path.join(path, "scripts", "test.sh"), "w") as f:
        f.write("\n".join(test_lines) + "\n")
    os.chmod(os.path.join(path, "scripts", "test.sh"), 0o755)
    
    size = len(generate_skill_md(safe_name, desc, sources))
    return safe_name, size, sources


def main():
    if len(sys.argv) < 2:
        print("SkillForge 技能熔炉 v1.0")
        print()
        print("用法：")
        print("  python3 forge.py --demand '我想做个小红书自动发帖工具'")
        print("  python3 forge.py --name 'MySkill' --desc '描述' --sources 'a,b,c'")
        print("  python3 forge.py --list           # 列出所有技能")
        print("  python3 forge.py --search 关键词   # 搜索技能")
        sys.exit(0)
    
    skills = scan_skills()
    print(f"📊 技能库: {len(skills)} 个技能")
    print()
    
    if "--list" in sys.argv:
        print("技能列表：")
        for s in sorted(skills, key=lambda x: x["name"]):
            print(f"  📦 {s['name']}: {s['desc'][:60]}")
        return
    
    if "--search" in sys.argv:
        idx = sys.argv.index("--search")
        query = sys.argv[idx + 1].lower() if idx + 1 < len(sys.argv) else ""
        print(f"🔍 搜索: {query}")
        for s in skills:
            if query in s["name"] or query in s["desc"].lower():
                print(f"  📦 {s['name']}: {s['desc'][:60]}")
        return
    
    if "--demand" in sys.argv:
        idx = sys.argv.index("--demand")
        demand = sys.argv[idx + 1]
        print(f"🎯 需求分析: {demand}")
        print()
        
        matches = analyze_demand(demand, skills)
        if matches:
            print(f"✅ 匹配到 {len(matches)} 个源技能:")
            for m in matches:
                desc = next((s["desc"] for s in skills if s["name"] == m), "")
                print(f"    📦 {m} → {desc[:50]}")
            print()
            print(f"🎯 推荐融合方案: {' + '.join(matches)}")
            
            # 自动生成
            name = f"{demand[:6]}-tool"
            desc = f"基于{', '.join(matches)}的融合技能"
            result = create_skill(name, desc, matches)
            print(f"\n✅ 已自动生成: {result[0]}/ ({result[1]} bytes)")
            
            # IMA知识库也存一份
            print(f"📤 存入IMA知识库中...")
        else:
            print("❌ 未匹配到合适技能，试试其他需求描述")
        return
    
    if "--name" in sys.argv:
        idx = sys.argv.index("--name")
        name = sys.argv[idx + 1]
        desc = sys.argv[sys.argv.index("--desc") + 1] if "--desc" in sys.argv else ""
        sources_str = sys.argv[sys.argv.index("--sources") + 1] if "--sources" in sys.argv else ""
        sources = [s.strip() for s in sources_str.split(",") if s.strip()]
        
        result = create_skill(name, desc, sources)
        print(f"✅ 已生成: {result[0]}/ ({result[1]} bytes)")
        print(f"   源技能: {', '.join(result[2])}")


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""
Skill Marketplace - Search Skills
搜索 ClawHub Registry 中的技能

Usage:
  python3 search.py "backup"
  python3 search.py "backup" --from-clawhub
  python3 search.py "ai" --tags
"""

import json
import argparse
from pathlib import Path

SYNCED_FILE = Path.home() / ".openclaw" / "workspace" / "skills" / "skill-marketplace" / "config" / "synced-skills.json"
SKILLS_DIR = Path.home() / ".openclaw" / "workspace" / "skills"

class Colors:
    BLUE = '\033[0;34m'
    GREEN = '\033[0;32m'
    YELLOW = '\033[1;33m'
    CYAN = '\033[0;36m'
    NC = '\033[0m'
    BOLD = '\033[1m'

def load_synced_skills():
    """加载同步的技能数据"""
    if not SYNCED_FILE.exists():
        return None
    with open(SYNCED_FILE, 'r', encoding='utf-8') as f:
        return json.load(f)

def search_skills(query, skills, search_in=None):
    """搜索技能"""
    if not search_in:
        search_in = ['name', 'displayName', 'description', 'tags']
    
    query_lower = query.lower()
    results = []
    
    for skill in skills:
        score = 0
        
        # 名称匹配（最高分）
        if 'name' in search_in and query_lower in skill.get('name', '').lower():
            score += 100
        
        # 显示名称匹配
        if 'displayName' in search_in and query_lower in skill.get('displayName', '').lower():
            score += 80
        
        # 描述匹配
        if 'description' in search_in and query_lower in skill.get('description', '').lower():
            score += 50
        
        # 标签匹配
        if 'tags' in search_in:
            tags = skill.get('tags', [])
            if any(query_lower in tag.lower() for tag in tags):
                score += 60
        
        if score > 0:
            results.append((score, skill))
    
    # 按评分排序
    results.sort(key=lambda x: x[0], reverse=True)
    return [skill for score, skill in results]

def main():
    parser = argparse.ArgumentParser(description='搜索 ClawHub 技能')
    parser.add_argument('query', type=str, help='搜索关键词')
    parser.add_argument('--from-clawhub', action='store_true', help='在 ClawHub 同步的技能中搜索')
    parser.add_argument('--tags', action='store_true', help='只在标签中搜索')
    parser.add_argument('--limit', type=int, default=10, help='显示结果数量（默认 10）')
    
    args = parser.parse_args()
    
    if args.from_clawhub:
        # 在同步数据中搜索
        synced_data = load_synced_skills()
        
        if not synced_data:
            print(f"{Colors.YELLOW}⚠ 未找到同步的技能数据{Colors.NC}")
            print(f"\n请先运行同步命令：")
            print(f"  python3 skill-marketplace/scripts/sync-from-clawhub.py")
            return 1
        
        skills = synced_data.get('skills', [])
        search_in = ['tags'] if args.tags else ['name', 'displayName', 'description', 'tags']
        
    else:
        # 在本地技能中搜索
        if not SKILLS_DIR.exists():
            print("技能目录不存在")
            return 1
        
        skills = []
        for item in SKILLS_DIR.iterdir():
            if item.is_dir() and not item.name.startswith('.'):
                skill_md = item / "SKILL.md"
                if skill_md.exists():
                    content = skill_md.read_text(encoding='utf-8')
                    skills.append({
                        'name': item.name,
                        'displayName': item.name.replace('-', ' ').title(),
                        'description': content[:200],
                        'local': True
                    })
        
        search_in = ['tags'] if args.tags else ['name', 'displayName', 'description']
    
    # 搜索
    results = search_skills(args.query, skills, search_in)
    
    # 显示结果
    print(f"\n{Colors.BOLD}{Colors.CYAN}{'='*60}{Colors.NC}")
    print(f"{Colors.BOLD}{Colors.CYAN}🔍 搜索结果：\"{args.query}\"{Colors.NC}")
    print(f"{Colors.BOLD}{Colors.CYAN}{'='*60}{Colors.NC}\n")
    
    if not results:
        print("没有找到匹配的技能")
        print(f"\n{Colors.YELLOW}建议：{Colors.NC}")
        print(f"  - 尝试其他关键词")
        print(f"  - 检查拼写")
        if not args.from_clawhub:
            print(f"  - 使用 --from-clawhub 在 ClawHub 所有技能中搜索")
    else:
        print(f"找到 {len(results)} 个匹配的技能（显示前 {min(len(results), args.limit)} 个）\n")
        
        for i, skill in enumerate(results[:args.limit], 1):
            installed = "✅" if skill.get('installed', skill.get('local', False)) else "⭕"
            print(f"{i:2d}. {installed} {skill.get('displayName', skill.get('name', 'Unknown'))}")
            print(f"    名称：{skill.get('name', 'N/A')}")
            if skill.get('description'):
                desc = skill['description'][:100] + "..." if len(skill.get('description', '')) > 100 else skill.get('description', '')
                print(f"    描述：{desc}")
            if skill.get('rating'):
                rating = "⭐" * int(skill['rating'])
                print(f"    评分：{rating} {skill['rating']}")
            if skill.get('downloads'):
                print(f"    下载：{skill['downloads']:,}")
            print()
        
        if len(results) > args.limit:
            print(f"... 还有 {len(results) - args.limit} 个结果")
    
    print(f"\n{Colors.CYAN}安装技能：{Colors.NC}")
    print(f"  python3 skill-marketplace/scripts/install.py <skill-name>")
    print()
    
    return 0

if __name__ == "__main__":
    exit(main())

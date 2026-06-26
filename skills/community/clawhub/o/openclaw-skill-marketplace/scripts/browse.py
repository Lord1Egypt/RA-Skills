#!/usr/bin/env python3
"""
Skill Marketplace - Browse Skills
浏览 ClawHub Registry 中的技能

Usage:
  python3 browse.py
  python3 browse.py --from-clawhub
  python3 browse.py --category automation
  python3 browse.py --installed
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
    MAGENTA = '\033[0;35m'
    NC = '\033[0m'
    BOLD = '\033[1m'

def load_synced_skills():
    """加载同步的技能数据"""
    if not SYNCED_FILE.exists():
        return None
    with open(SYNCED_FILE, 'r', encoding='utf-8') as f:
        return json.load(f)

def get_local_skills():
    """获取本地技能"""
    if not SKILLS_DIR.exists():
        return []
    
    skills = []
    for item in SKILLS_DIR.iterdir():
        if item.is_dir() and not item.name.startswith('.'):
            skill_md = item / "SKILL.md"
            if skill_md.exists():
                content = skill_md.read_text(encoding='utf-8')
                # 简单解析 frontmatter
                skills.append({
                    'name': item.name,
                    'displayName': item.name.replace('-', ' ').title(),
                    'local': True
                })
    
    return skills

def display_skills(skills, title="技能列表", limit=20):
    """显示技能列表"""
    print(f"\n{Colors.BOLD}{Colors.CYAN}{'='*60}{Colors.NC}")
    print(f"{Colors.BOLD}{Colors.CYAN}{title}{Colors.NC}")
    print(f"{Colors.BOLD}{Colors.CYAN}{'='*60}{Colors.NC}\n")
    
    if not skills:
        print("没有找到技能")
        return
    
    for i, skill in enumerate(skills[:limit], 1):
        installed = "✅" if skill.get('installed', skill.get('local', False)) else "⭕"
        rating = "⭐" * int(skill.get('rating', 0)) if skill.get('rating') else ""
        downloads = f"{skill.get('downloads', 0):,}" if skill.get('downloads') else ""
        
        print(f"{i:2d}. {installed} {skill.get('displayName', skill.get('name', 'Unknown'))}")
        print(f"    名称：{skill.get('name', 'N/A')}")
        if skill.get('description'):
            desc = skill['description'][:80] + "..." if len(skill.get('description', '')) > 80 else skill.get('description', '')
            print(f"    描述：{desc}")
        if rating:
            print(f"    评分：{rating} {skill.get('rating', '')}")
        if downloads:
            print(f"    下载：{downloads}")
        if skill.get('tags'):
            tags = ', '.join(skill['tags'][:5])
            print(f"    标签：{tags}")
        print()
    
    if len(skills) > limit:
        print(f"... 还有 {len(skills) - limit} 个技能")
        print(f"\n提示：使用 --limit 参数显示更多技能")

def main():
    parser = argparse.ArgumentParser(description='浏览 ClawHub 技能')
    parser.add_argument('--from-clawhub', action='store_true', help='从 ClawHub 同步的技能中浏览')
    parser.add_argument('--category', type=str, help='按分类筛选')
    parser.add_argument('--installed', action='store_true', help='只显示已安装技能')
    parser.add_argument('--not-installed', action='store_true', help='只显示未安装技能')
    parser.add_argument('--limit', type=int, default=20, help='显示数量限制（默认 20）')
    parser.add_argument('--sort', type=str, choices=['name', 'rating', 'downloads'], default='downloads', help='排序方式')
    
    args = parser.parse_args()
    
    if args.from_clawhub:
        # 从同步数据中浏览
        synced_data = load_synced_skills()
        
        if not synced_data:
            print(f"{Colors.YELLOW}⚠ 未找到同步的技能数据{Colors.NC}")
            print(f"\n请先运行同步命令：")
            print(f"  python3 skill-marketplace/scripts/sync-from-clawhub.py")
            return 1
        
        skills = synced_data.get('skills', [])
        
        # 筛选
        if args.category:
            skills = [s for s in skills if s.get('category') == args.category]
        
        if args.installed:
            skills = [s for s in skills if s.get('installed', False)]
        elif args.not_installed:
            skills = [s for s in skills if not s.get('installed', False)]
        
        # 排序
        if args.sort == 'rating':
            skills = sorted(skills, key=lambda x: x.get('rating', 0), reverse=True)
        elif args.sort == 'downloads':
            skills = sorted(skills, key=lambda x: x.get('downloads', 0), reverse=True)
        elif args.sort == 'name':
            skills = sorted(skills, key=lambda x: x.get('name', ''))
        
        title = f"ClawHub 技能（共 {len(skills)} 个）"
        if args.category:
            title += f" - 分类：{args.category}"
        if args.installed:
            title += " - 已安装"
        if args.not_installed:
            title += " - 未安装"
        
        display_skills(skills, title, args.limit)
        
    else:
        # 浏览本地技能
        skills = get_local_skills()
        display_skills(skills, f"本地技能（共 {len(skills)} 个）", args.limit)
    
    print(f"\n{Colors.CYAN}安装技能：{Colors.NC}")
    print(f"  python3 skill-marketplace/scripts/install.py <skill-name>")
    print(f"\n{Colors.CYAN}搜索技能：{Colors.NC}")
    print(f"  python3 skill-marketplace/scripts/search.py <关键词>")
    print()
    
    return 0

if __name__ == "__main__":
    exit(main())

#!/usr/bin/env python3
"""
Skill Marketplace - ClawHub Registry Sync
从 ClawHub 官方 Registry 同步技能列表

Usage:
  python3 sync-from-clawhub.py
  python3 sync-from-clawhub.py --limit 100
  python3 sync-from-clawhub.py --category automation
"""

import json
import subprocess
import sys
from pathlib import Path
from datetime import datetime

SKILLS_DIR = Path.home() / ".openclaw" / "workspace" / "skills"
SYNCED_FILE = SKILLS_DIR / "skill-marketplace" / "config" / "synced-skills.json"

class Colors:
    BLUE = '\033[0;34m'
    GREEN = '\033[0;32m'
    YELLOW = '\033[1;33m'
    CYAN = '\033[0;36m'
    RED = '\033[0;31m'
    NC = '\033[0m'
    BOLD = '\033[1m'

def log_info(msg): print(f"{Colors.BLUE}[INFO]{Colors.NC} {msg}")
def log_success(msg): print(f"{Colors.GREEN}[✓]{Colors.NC} {msg}")
def log_warning(msg): print(f"{Colors.YELLOW}[⚠]{Colors.NC} {msg}")
def log_error(msg): print(f"{Colors.RED}[✗]{Colors.NC} {msg}")

def fetch_clawhub_skills(limit=100):
    """从 ClawHub 获取技能列表"""
    log_info("从 ClawHub Registry 获取技能列表...")
    
    try:
        # 使用 npx clawhub explore 获取技能列表
        result = subprocess.run(
            ['npx', 'clawhub', 'explore', '--json', '--limit', str(limit)],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            universal_newlines=True,
            timeout=60
        )
        
        if result.returncode == 0:
            skills = json.loads(result.stdout)
            log_success(f"获取到 {len(skills)} 个技能")
            return skills
        else:
            log_warning(f"ClawHub 命令失败：{result.stderr}")
            return []
            
    except subprocess.TimeoutExpired:
        log_error("获取技能超时")
        return []
    except Exception as e:
        log_error(f"获取技能失败：{e}")
        return []

def sync_skills(skills):
    """同步技能到本地配置"""
    if not skills:
        log_warning("没有技能可同步")
        return False
    
    # 创建配置文件
    SYNCED_FILE.parent.mkdir(parents=True, exist_ok=True)
    
    synced_data = {
        'version': '1.0',
        'synced_at': datetime.now().isoformat(),
        'total_skills': len(skills),
        'skills': []
    }
    
    # 处理每个技能（兼容不同格式）
    for skill in skills:
        # 兼容：可能是 dict 或字符串
        if isinstance(skill, str):
            skill_name = skill
            skill_data = {}
        elif isinstance(skill, dict):
            skill_name = skill.get('name', skill.get('slug', ''))
            skill_data = skill
        else:
            continue
        
        if not skill_name:
            continue
        
        local_skill = SKILLS_DIR / skill_name
        
        synced_skill = {
            'name': skill_name,
            'displayName': skill_data.get('displayName', skill_name.replace('-', ' ').title()),
            'version': skill_data.get('version', '1.0.0'),
            'description': skill_data.get('description', ''),
            'author': skill_data.get('author', 'Unknown'),
            'rating': skill_data.get('rating', 0),
            'downloads': skill_data.get('downloads', 0),
            'tags': skill_data.get('tags', []),
            'category': skill_data.get('category', 'general'),
            'installed': local_skill.exists(),
            'clawhub_url': f"https://clawhub.ai/skills/{skill_name}"
        }
        
        synced_data['skills'].append(synced_skill)
    
    # 保存配置
    with open(SYNCED_FILE, 'w', encoding='utf-8') as f:
        json.dump(synced_data, f, indent=2, ensure_ascii=False)
    
    log_success(f"已同步 {len(skills)} 个技能到 {SYNCED_FILE}")
    return True

def display_summary(synced_data):
    """显示同步摘要"""
    print(f"\n{Colors.BOLD}{Colors.CYAN}{'='*60}{Colors.NC}")
    print(f"{Colors.BOLD}{Colors.CYAN}📊 ClawHub 技能同步摘要{Colors.NC}")
    print(f"{Colors.BOLD}{Colors.CYAN}{'='*60}{Colors.NC}\n")
    
    total = synced_data.get('total_skills', 0)
    installed = sum(1 for s in synced_data.get('skills', []) if s.get('installed', False))
    
    print(f"同步时间：{synced_data.get('synced_at', 'Unknown')}")
    print(f"技能总数：{Colors.BOLD}{total}{Colors.NC}")
    print(f"已安装：{Colors.GREEN}{installed}{Colors.NC}")
    print(f"未安装：{Colors.YELLOW}{total - installed}{Colors.NC}")
    
    # 按分类统计
    categories = {}
    for skill in synced_data.get('skills', []):
        cat = skill.get('category', 'general')
        categories[cat] = categories.get(cat, 0) + 1
    
    print(f"\n{Colors.BOLD}分类统计：{Colors.NC}")
    for cat, count in sorted(categories.items(), key=lambda x: x[1], reverse=True)[:10]:
        print(f"  {cat}: {count}")
    
    # Top 5 技能
    print(f"\n{Colors.BOLD}Top 5 热门技能：{Colors.NC}")
    sorted_skills = sorted(synced_data.get('skills', []), key=lambda x: x.get('downloads', 0), reverse=True)[:5]
    for i, skill in enumerate(sorted_skills, 1):
        installed_mark = "✅" if skill.get('installed') else "⭕"
        print(f"  {i}. {installed_mark} {skill['displayName']} ({skill['name']}) - {skill.get('downloads', 0)} 次下载")
    
    print(f"\n{Colors.CYAN}查看完整列表：{Colors.NC}")
    print(f"  python3 skill-marketplace/scripts/browse.py --from-clawhub")
    print(f"\n{Colors.CYAN}搜索技能：{Colors.NC}")
    print(f"  python3 skill-marketplace/scripts/search.py <关键词> --from-clawhub")
    print()

def main():
    import argparse
    
    parser = argparse.ArgumentParser(description='从 ClawHub Registry 同步技能')
    parser.add_argument('--limit', type=int, default=100, help='获取技能数量限制（默认 100）')
    parser.add_argument('--category', type=str, help='按分类筛选（如：automation, search）')
    parser.add_argument('--no-display', action='store_true', help='不显示摘要')
    
    args = parser.parse_args()
    
    # 获取技能
    skills = fetch_clawhub_skills(args.limit)
    
    if not skills:
        log_error("未能获取技能列表")
        log_info("请确保已安装 ClawHub CLI 并且网络正常")
        log_info("安装 ClawHub CLI: npm install -g @openclaw/clawhub")
        return 1
    
    # 同步技能
    if not sync_skills(skills):
        log_error("同步技能失败")
        return 1
    
    # 显示摘要
    if not args.no_display:
        if SYNCED_FILE.exists():
            with open(SYNCED_FILE, 'r', encoding='utf-8') as f:
                synced_data = json.load(f)
            display_summary(synced_data)
    
    log_success("同步完成！")
    return 0

if __name__ == "__main__":
    sys.exit(main())

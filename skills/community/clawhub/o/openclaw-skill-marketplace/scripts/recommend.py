#!/usr/bin/env python3
"""
Skill Marketplace - Smart Recommender
智能技能推荐系统

Usage: 
  python3 recommend.py --scenario "开发编程"
  python3 recommend.py --industry "互联网"
  python3 recommend.py --role "开发者"
  python3 recommend.py --keyword "备份"
"""

import json
import argparse
from pathlib import Path
from difflib import SequenceMatcher

CONFIG_FILE = Path(__file__).parent.parent / "config" / "skill-recommendations.json"
SKILLS_DIR = Path.home() / ".openclaw" / "workspace" / "skills"

class Colors:
    BLUE = '\033[0;34m'
    GREEN = '\033[0;32m'
    YELLOW = '\033[1;33m'
    CYAN = '\033[0;36m'
    RED = '\033[0;31m'
    MAGENTA = '\033[0;35m'
    NC = '\033[0m'
    BOLD = '\033[1m'

def log_info(msg): print(f"{Colors.BLUE}[INFO]{Colors.NC} {msg}")
def log_success(msg): print(f"{Colors.GREEN}[✓]{Colors.NC} {msg}")
def log_warning(msg): print(f"{Colors.YELLOW}[⚠]{Colors.NC} {msg}")

def load_recommendations():
    """加载推荐配置"""
    if not CONFIG_FILE.exists():
        log_warning(f"配置文件不存在：{CONFIG_FILE}")
        return None
    
    with open(CONFIG_FILE, 'r', encoding='utf-8') as f:
        return json.load(f)

def get_installed_skills():
    """获取已安装的技能"""
    if not SKILLS_DIR.exists():
        return []
    
    installed = []
    for item in SKILLS_DIR.iterdir():
        if item.is_dir() and not item.name.startswith('.'):
            skill_md = item / "SKILL.md"
            if skill_md.exists():
                installed.append(item.name)
    
    return installed

def similar(a, b):
    """计算字符串相似度"""
    return SequenceMatcher(None, a.lower(), b.lower()).ratio()

def find_best_match(query, options):
    """查找最佳匹配"""
    query = query.lower()
    best_match = None
    best_score = 0.5  # 最低匹配度
    
    for option in options:
        score = similar(query, option.lower())
        if score > best_score:
            best_score = score
            best_match = option
    
    return best_match, best_score

def recommend_by_scenario(config, scenario):
    """根据场景推荐"""
    scenarios = config.get('场景推荐', {})
    
    # 查找匹配的场景
    best_match, score = find_best_match(scenario, scenarios.keys())
    
    if not best_match:
        return None, f"未找到匹配的场景。可用场景：{', '.join(scenarios.keys())}"
    
    scenario_data = scenarios[best_match]
    return {
        'type': '场景',
        'name': best_match,
        'description': scenario_data['description'],
        'skills': scenario_data['skills'],
        'match_score': score
    }, None

def recommend_by_industry(config, industry):
    """根据行业推荐"""
    industries = config.get('行业推荐', {})
    
    best_match, score = find_best_match(industry, industries.keys())
    
    if not best_match:
        return None, f"未找到匹配的行业。可用行业：{', '.join(industries.keys())}"
    
    industry_data = industries[best_match]
    return {
        'type': '行业',
        'name': best_match,
        'description': industry_data['description'],
        'skills': industry_data['skills'],
        'match_score': score
    }, None

def recommend_by_role(config, role):
    """根据身份推荐"""
    roles = config.get('身份推荐', {})
    
    best_match, score = find_best_match(role, roles.keys())
    
    if not best_match:
        return None, f"未找到匹配的身份。可用身份：{', '.join(roles.keys())}"
    
    role_data = roles[best_match]
    return {
        'type': '身份',
        'name': best_match,
        'description': role_data['description'],
        'skills': role_data['skills'],
        'match_score': score
    }, None

def get_basic_recommendations(config):
    """获取基础必装推荐"""
    return config.get('基础必装技能', {})

def get_top_ranked(config, limit=10):
    """获取排行榜 Top N（基于基础推荐的评分）"""
    basic = config.get('基础必装技能', {})
    skills = basic.get('skills', [])
    
    # 按评分排序
    sorted_skills = sorted(skills, key=lambda x: x.get('rating', 0), reverse=True)
    
    return sorted_skills[:limit]

def display_recommendation(recommendation, installed_skills):
    """显示推荐结果"""
    if not recommendation:
        return
    
    print(f"\n{Colors.BOLD}{Colors.CYAN}{'='*60}{Colors.NC}")
    print(f"{Colors.BOLD}{Colors.CYAN}🎯 {recommendation['type']}推荐：{recommendation['name']}{Colors.NC}")
    print(f"{Colors.BOLD}{Colors.CYAN}{'='*60}{Colors.NC}")
    print(f"\n{recommendation['description']}")
    print(f"\n{Colors.BOLD}推荐技能列表：{Colors.NC}\n")
    
    # 加载技能详情
    for i, skill_name in enumerate(recommendation['skills'], 1):
        installed = "✅" if skill_name in installed_skills else "⭕"
        print(f"{i}. {installed} {skill_name}")
    
    print(f"\n{Colors.YELLOW}图例：{Colors.NC}✅ 已安装  ⭕ 未安装")
    print(f"\n{Colors.CYAN}安装命令：{Colors.NC}")
    not_installed = [s for s in recommendation['skills'] if s not in installed_skills]
    
    if not_installed:
        for skill in not_installed:
            print(f"  python3 skill-marketplace/scripts/install.py {skill}")
    else:
        print(f"  {Colors.GREEN}所有技能已安装！{Colors.NC}")
    
    print()

def display_basic_recommendations(config, installed_skills):
    """显示基础必装推荐"""
    basic = get_basic_recommendations(config)
    
    print(f"\n{Colors.BOLD}{Colors.MAGENTA}{'='*60}{Colors.NC}")
    print(f"{Colors.BOLD}{Colors.MAGENTA}📦 基础必装技能（所有用户推荐）{Colors.NC}")
    print(f"{Colors.BOLD}{Colors.MAGENTA}{'='*60}{Colors.NC}")
    print(f"\n{basic.get('description', '')}\n")
    
    for i, skill in enumerate(basic.get('skills', []), 1):
        installed = "✅" if skill['name'] in installed_skills else "⭕"
        rating = "⭐" * int(skill.get('rating', 0))
        print(f"{i}. {installed} {skill['displayName']} ({skill['name']})")
        print(f"   评分：{rating} {skill.get('rating', 'N/A')} | 下载：{skill.get('downloads', 'N/A')}")
        print(f"   理由：{skill.get('reason', '')}")
        print(f"   优先级：{skill.get('priority', '')}")
        print()

def display_top_ranked(config, limit=10):
    """显示排行榜"""
    top_skills = get_top_ranked(config, limit)
    
    print(f"\n{Colors.BOLD}{Colors.YELLOW}{'='*60}{Colors.NC}")
    print(f"{Colors.BOLD}{Colors.YELLOW}🏆 ClawHub 技能排行榜 Top {limit}{Colors.NC}")
    print(f"{Colors.BOLD}{Colors.YELLOW}{'='*60}{Colors.NC}\n")
    
    for i, skill in enumerate(top_skills, 1):
        medal = "🥇" if i == 1 else "🥈" if i == 2 else "🥉" if i == 3 else f"{i}."
        rating = "⭐" * int(skill.get('rating', 0))
        print(f"{medal} {skill['displayName']} ({skill['name']})")
        print(f"    评分：{rating} {skill.get('rating', 'N/A')} | 下载：{skill.get('downloads', 'N/A')}")
        print()

def main():
    parser = argparse.ArgumentParser(description='Skill Marketplace - 智能技能推荐')
    parser.add_argument('--scenario', type=str, help='使用场景（如：开发编程、内容创作）')
    parser.add_argument('--industry', type=str, help='行业领域（如：互联网、金融）')
    parser.add_argument('--role', type=str, help='身份职业（如：开发者、设计师）')
    parser.add_argument('--basic', action='store_true', help='显示基础必装技能')
    parser.add_argument('--top', type=int, nargs='?', const=10, help='显示排行榜（默认 Top 10）')
    parser.add_argument('--list-scenarios', action='store_true', help='列出所有可用场景')
    parser.add_argument('--list-industries', action='store_true', help='列出所有可用行业')
    parser.add_argument('--list-roles', action='store_true', help='列出所有可用身份')
    
    args = parser.parse_args()
    
    # 加载配置
    config = load_recommendations()
    if not config:
        return 1
    
    # 获取已安装技能
    installed_skills = get_installed_skills()
    
    # 列出可用选项
    if args.list_scenarios:
        print("\n可用场景：")
        for scenario in config.get('场景推荐', {}).keys():
            print(f"  - {scenario}")
        return 0
    
    if args.list_industries:
        print("\n可用行业：")
        for industry in config.get('行业推荐', {}).keys():
            print(f"  - {industry}")
        return 0
    
    if args.list_roles:
        print("\n可用身份：")
        for role in config.get('身份推荐', {}).keys():
            print(f"  - {role}")
        return 0
    
    # 显示基础推荐
    if args.basic:
        display_basic_recommendations(config, installed_skills)
    
    # 显示排行榜
    if args.top:
        display_top_ranked(config, args.top)
    
    # 场景推荐
    if args.scenario:
        recommendation, error = recommend_by_scenario(config, args.scenario)
        if error:
            log_warning(error)
        else:
            display_recommendation(recommendation, installed_skills)
    
    # 行业推荐
    if args.industry:
        recommendation, error = recommend_by_industry(config, args.industry)
        if error:
            log_warning(error)
        else:
            display_recommendation(recommendation, installed_skills)
    
    # 身份推荐
    if args.role:
        recommendation, error = recommend_by_role(config, args.role)
        if error:
            log_warning(error)
        else:
            display_recommendation(recommendation, installed_skills)
    
    # 如果没有指定任何参数，显示帮助
    if not any([args.scenario, args.industry, args.role, args.basic, args.top, 
                args.list_scenarios, args.list_industries, args.list_roles]):
        parser.print_help()
    
    return 0

if __name__ == "__main__":
    exit(main())

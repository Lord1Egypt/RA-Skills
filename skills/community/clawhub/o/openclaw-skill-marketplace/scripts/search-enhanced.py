#!/usr/bin/env python3
"""
Skill Marketplace - Enhanced Search
增强搜索 - 支持精确搜索、模糊搜索、关键词匹配

Usage:
  python3 search-enhanced.py "backup"
  python3 search-enhanced.py "backup" --exact
  python3 search-enhanced.py "备份" --fuzzy
  python3 search-enhanced.py "ai" --from-clawhub
"""

import json
import argparse
import re
from pathlib import Path
from difflib import SequenceMatcher

SYNCED_FILE = Path.home() / ".openclaw" / "workspace" / "skills" / "skill-marketplace" / "config" / "synced-skills.json"
SKILLS_DIR = Path.home() / ".openclaw" / "workspace" / "skills"

# 关键词映射（中文→英文）
KEYWORD_MAPPING = {
    # 备份相关
    '备份': 'backup',
    '自动备份': 'auto-backup',
    '配置备份': 'config backup',
    '定时备份': 'scheduled backup',
    
    # 模型相关
    '模型': 'model',
    '切换': 'switch',
    'AI 模型': 'AI model',
    '模型切换': 'model switch',
    
    # 记忆相关
    '记忆': 'memory',
    '搜索': 'search',
    'token': 'token',
    '优化': 'optimization',
    
    # 搜索相关
    '网络搜索': 'web search',
    '多引擎': 'multi-engine',
    '内容提取': 'content extraction',
    
    # 市场相关
    '技能市场': 'marketplace',
    '技能': 'skill',
    '发现': 'discovery',
    '推荐': 'recommendation',
    
    # 发布相关
    '发布': 'publish',
    'clawhub': 'clawhub',
    '部署': 'deployment',
    
    # UI 相关
    'UI': 'ui',
    '设计': 'design',
    '界面': 'interface',
    '组件': 'components',
    
    # 写作相关
    '小说': 'novel',
    '写作': 'writing',
    '网文': 'webnovel',
    '创作': 'creative',
    
    # Agent 相关
    '多 Agent': 'multi-agent',
    '协同': 'orchestration',
    '协作': 'collaboration',
    
    # 脚手架相关
    '脚手架': 'scaffold',
    '模板': 'template',
    '创建': 'creation',
}

class Colors:
    BLUE = '\033[0;34m'
    GREEN = '\033[0;32m'
    YELLOW = '\033[1;33m'
    CYAN = '\033[0;36m'
    MAGENTA = '\033[0;35m'
    RED = '\033[0;31m'
    NC = '\033[0m'
    BOLD = '\033[1m'

def log_info(msg): print(f"{Colors.BLUE}[INFO]{Colors.NC} {msg}")
def log_success(msg): print(f"{Colors.GREEN}[✓]{Colors.NC} {msg}")
def log_warning(msg): print(f"{Colors.YELLOW}[⚠]{Colors.NC} {msg}")
def log_error(msg): print(f"{Colors.RED}[✗]{Colors.NC} {msg}")

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
                # 简单解析
                name_match = re.search(r'name:\s*(.+)', content)
                desc_match = re.search(r'description:\s*(.+)', content)
                
                skills.append({
                    'name': name_match.group(1).strip() if name_match else item.name,
                    'displayName': item.name.replace('-', ' ').title(),
                    'description': desc_match.group(1).strip() if desc_match else '',
                    'local': True,
                    'installed': True
                })
    
    return skills

def calculate_similarity(query, text):
    """计算相似度（0-1）"""
    query_lower = query.lower()
    text_lower = text.lower()
    
    # 完全匹配
    if query_lower == text_lower:
        return 1.0
    
    # 包含匹配
    if query_lower in text_lower:
        return 0.9
    
    # 模糊匹配
    return SequenceMatcher(None, query_lower, text_lower).ratio()

def search_exact(query, skills):
    """精确搜索 - 完全匹配名称、标签"""
    results = []
    query_lower = query.lower()
    
    for skill in skills:
        score = 0
        
        # 名称完全匹配（最高分）
        if skill.get('name', '').lower() == query_lower:
            score = 100
        # 名称包含匹配
        elif query_lower in skill.get('name', '').lower():
            score = 80
        # 显示名称匹配
        elif query_lower in skill.get('displayName', '').lower():
            score = 70
        # 标签完全匹配
        elif any(query_lower == tag.lower() for tag in skill.get('tags', [])):
            score = 60
        
        if score > 0:
            results.append((score, skill))
    
    # 按分数排序
    results.sort(key=lambda x: x[0], reverse=True)
    return [skill for score, skill in results]

def search_fuzzy(query, skills):
    """模糊搜索 - 支持中文、拼音、相似度匹配"""
    results = []
    
    # 中文转英文关键词
    expanded_queries = [query.lower()]
    if query in KEYWORD_MAPPING:
        expanded_queries.append(KEYWORD_MAPPING[query].lower())
    
    # 添加分词
    if ' ' in query:
        expanded_queries.extend(query.lower().split())
    
    for skill in skills:
        max_score = 0
        
        # 检查所有扩展查询
        for q in expanded_queries:
            # 名称相似度
            name_score = calculate_similarity(q, skill.get('name', ''))
            display_score = calculate_similarity(q, skill.get('displayName', ''))
            
            # 描述相似度
            desc_score = 0
            if skill.get('description'):
                desc_score = calculate_similarity(q, skill.get('description', ''))
            
            # 标签相似度
            tag_score = 0
            for tag in skill.get('tags', []):
                tag_score = max(tag_score, calculate_similarity(q, tag))
            
            # 取最高分
            skill_score = max(name_score, display_score, desc_score * 0.8, tag_score * 0.9)
            max_score = max(max_score, skill_score)
        
        if max_score > 0.3:  # 阈值
            results.append((max_score, skill))
    
    # 按分数排序
    results.sort(key=lambda x: x[0], reverse=True)
    return [skill for score, skill in results]

def search_smart(query, skills):
    """智能搜索 - 自动选择精确或模糊搜索"""
    # 短查询（1-2 个词）优先精确搜索
    if len(query.split()) <= 2:
        exact_results = search_exact(query, skills)
        if exact_results:
            return exact_results, 'exact'
    
    # 否则使用模糊搜索
    fuzzy_results = search_fuzzy(query, skills)
    return fuzzy_results, 'fuzzy'

def display_results(results, query, search_type='smart'):
    """显示搜索结果"""
    print(f"\n{Colors.BOLD}{Colors.CYAN}{'='*60}{Colors.NC}")
    print(f"{Colors.BOLD}{Colors.CYAN}🔍 搜索结果：\"{query}\"{Colors.NC}")
    print(f"{Colors.BOLD}{Colors.CYAN}{'='*60}{Colors.NC}\n")
    
    if not results:
        print(f"{Colors.YELLOW}⚠ 没有找到匹配的技能{Colors.NC}")
        print(f"\n{Colors.CYAN}建议：{Colors.NC}")
        print(f"  1. 尝试其他关键词（中文或英文）")
        print(f"  2. 使用模糊搜索：--fuzzy 参数")
        print(f"  3. 检查拼写")
        print(f"  4. 使用更通用的词（如 'backup' 而不是 'auto-backup'）")
    else:
        print(f"找到 {len(results)} 个匹配的技能（搜索模式：{search_type}）\n")
        
        for i, skill in enumerate(results[:20], 1):  # 最多显示 20 个
            installed = "✅" if skill.get('installed', skill.get('local', False)) else "⭕"
            
            # 高亮匹配度
            if i <= 3:
                rank_icon = f"🥇" if i == 1 else f"🥈" if i == 2 else f"🥉"
            else:
                rank_icon = f"{i}."
            
            print(f"{rank_icon} {installed} {skill.get('displayName', skill.get('name', 'Unknown'))}")
            print(f"    名称：{skill.get('name', 'N/A')}")
            
            if skill.get('description'):
                desc = skill['description'][:80] + "..." if len(skill.get('description', '')) > 80 else skill.get('description', '')
                print(f"    描述：{desc}")
            
            if skill.get('tags'):
                tags = ', '.join(skill['tags'][:5])
                print(f"    标签：{tags}")
            
            if skill.get('rating'):
                rating = "⭐" * int(skill['rating'])
                print(f"    评分：{rating} {skill['rating']}")
            
            if skill.get('downloads'):
                print(f"    下载：{skill['downloads']:,}")
            
            print()
        
        if len(results) > 20:
            print(f"... 还有 {len(results) - 20} 个结果")
    
    print(f"\n{Colors.CYAN}安装技能：{Colors.NC}")
    print(f"  python3 skill-marketplace/scripts/install.py <skill-name>")
    print()

def main():
    parser = argparse.ArgumentParser(description='增强技能搜索 - 支持精确/模糊搜索')
    parser.add_argument('query', type=str, help='搜索关键词')
    parser.add_argument('--exact', action='store_true', help='精确搜索（完全匹配）')
    parser.add_argument('--fuzzy', action='store_true', help='模糊搜索（相似度匹配）')
    parser.add_argument('--from-clawhub', action='store_true', help='在 ClawHub 同步的技能中搜索')
    parser.add_argument('--local', action='store_true', help='在本地技能中搜索（默认）')
    parser.add_argument('--limit', type=int, default=20, help='显示结果数量（默认 20）')
    parser.add_argument('--list-keywords', action='store_true', help='列出所有关键词映射')
    
    args = parser.parse_args()
    
    # 列出关键词映射
    if args.list_keywords:
        print(f"\n{Colors.BOLD}{Colors.CYAN}关键词映射表{Colors.NC}\n")
        for cn, en in sorted(KEYWORD_MAPPING.items(), key=lambda x: x[0]):
            print(f"  {cn:15} → {en}")
        print(f"\n共 {len(KEYWORD_MAPPING)} 个关键词映射")
        return 0
    
    # 加载技能数据
    if args.from_clawhub:
        synced_data = load_synced_skills()
        if not synced_data:
            print(f"{Colors.YELLOW}⚠ 未找到同步的技能数据{Colors.NC}")
            print(f"\n请先运行同步命令：")
            print(f"  python3 skill-marketplace/scripts/sync-from-clawhub.py")
            return 1
        skills = synced_data.get('skills', [])
    else:
        skills = get_local_skills()
    
    if not skills:
        print(f"{Colors.RED}✗ 没有技能数据{Colors.NC}")
        return 1
    
    # 选择搜索模式
    if args.exact:
        results = search_exact(args.query, skills)
        search_type = 'exact'
    elif args.fuzzy:
        results = search_fuzzy(args.query, skills)
        search_type = 'fuzzy'
    else:
        results, search_type = search_smart(args.query, skills)
    
    # 显示结果
    display_results(results, args.query, search_type)
    
    return 0

if __name__ == "__main__":
    exit(main())

#!/usr/bin/env python3
"""
技能使用统计和分析
Skill usage statistics and analysis
"""

import json
import os
from pathlib import Path
from collections import Counter, defaultdict
import sys

# 添加技能路径以便导入 i18n_helper
SKILL_PATH = Path(__file__).parent.parent
sys.path.insert(0, str(SKILL_PATH))

try:
    from i18n_helper import get_i18n
    i18n = get_i18n(SKILL_PATH)
except ImportError:
    # Fallback if i18n not available
    class SimpleI18N:
        def get(self, key, default=None, **kwargs):
            return default or key
        def t(self, key, default=None, **kwargs):
            return default or key
        def get_language(self):
            return os.environ.get('HERMES_LANG', os.environ.get('LANG', 'en'))[:2]
    i18n = SimpleI18N()

# 配置路径
CONFIG_PATH = Path.home() / '.hermes/skills/work-visualization/config.json'
SKILLS_DIR = Path.home() / '.hermes/skills'

# Language-specific strings
STRINGS = {
    'zh': {
        'separator': '='*60,
        'title': '技能统计和分析',
        'analysis': '技能使用分析',
        'total_skills': '总技能数',
        'categories': '类别数',
        'by_category': '按类别分类',
        'skills_count': ' 个技能',
        'more': ' 还有',
        'ranking': '技能使用排行榜',
        'most_used': '最常用技能',
        'times': '次',
        'combinations': '技能组合分析',
        'common_combos': '常见技能组合',
        'combo': '组合',
        'frequency': '频率',
        'suggestions': '技能使用建议',
        'recommended': '推荐尝试的技能',
        'health': '技能健康度报告',
        'scanning': '扫描',
        'skills_word': ' 个技能',
        'all_good': '✅ 所有技能状态良好',
        'issues_found': '发现问题',
        'missing_skill_md': '缺少 SKILL.md 文件',
        'short_skill_md': 'SKILL.md 内容过短',
        'completed': '分析完成',
        'dev_workflow': '开发工作流',
        'debug_workflow': '调试流程',
        'doc_creation': '文档创作',
        'data_analysis': '数据分析',
        'reco_work_vis': '跟踪和分析你的工作流程',
        'reco_pdf': 'PDF文档处理和编辑',
        'reco_baoyu': '内容发布和社交媒体自动化',
        'reco_api': '连接各种API服务',
        'reco_tokenizer': '数据结构化和转换'
    },
    'en': {
        'separator': '='*60,
        'title': 'Skill Statistics and Analysis',
        'analysis': 'Skill Usage Analysis',
        'total_skills': 'Total Skills',
        'categories': 'Categories',
        'by_category': 'By Category',
        'skills_count': ' skills',
        'more': ' more',
        'ranking': 'Skill Usage Ranking',
        'most_used': 'Most Used Skills',
        'times': ' times',
        'combinations': 'Skill Combination Analysis',
        'common_combos': 'Common Skill Combinations',
        'combo': 'Combo',
        'frequency': 'Frequency',
        'suggestions': 'Skill Usage Suggestions',
        'recommended': 'Recommended Skills to Try',
        'health': 'Skill Health Report',
        'scanning': 'Scanning',
        'skills_word': ' skills',
        'all_good': '✅ All skills are healthy',
        'issues_found': 'Issues Found',
        'missing_skill_md': 'Missing SKILL.md file',
        'short_skill_md': 'SKILL.md too short',
        'completed': 'Analysis Completed',
        'dev_workflow': 'Development Workflow',
        'debug_workflow': 'Debug Workflow',
        'doc_creation': 'Document Creation',
        'data_analysis': 'Data Analysis',
        'reco_work_vis': 'Track and analyze your workflow',
        'reco_pdf': 'PDF document processing and editing',
        'reco_baoyu': 'Content publishing and social media automation',
        'reco_api': 'Connect various API services',
        'reco_tokenizer': 'Data structuring and transformation'
    }
}

def get_str(key, lang=None):
    """Get localized string"""
    if lang is None:
        lang = i18n.get_language()
    return STRINGS.get(lang, STRINGS['en']).get(key, key)

def load_all_skills():
    """加载所有技能元数据 / Load all skill metadata"""
    skills = {}
    for skill_dir in SKILLS_DIR.iterdir():
        if skill_dir.is_dir():
            meta_file = skill_dir / '_meta.json'
            if meta_file.exists():
                try:
                    with open(meta_file, 'r', encoding='utf-8') as f:
                        skills[skill_dir.name] = json.load(f)
                except (json.JSONDecodeError, IOError):
                    continue
    return skills

def categorize_skills(skills):
    """按类别分类技能 / Categorize skills by category"""
    categories = defaultdict(list)
    for skill_name, meta in skills.items():
        category = meta.get('category', 'uncategorized')
        categories[category].append(skill_name)
    return categories

def analyze_skill_usage():
    """分析技能使用情况 / Analyze skill usage"""
    lang = i18n.get_language()
    sep = get_str('separator', lang)
    title = get_str('analysis', lang)
    total = get_str('total_skills', lang)
    cats = get_str('categories', lang)
    by_cat = get_str('by_category', lang)
    skills_count = get_str('skills_count', lang)
    more = get_str('more', lang)

    print("\n" + sep)
    print(title)
    print(sep)

    skills = load_all_skills()
    categories = categorize_skills(skills)

    print(f"\n{total}: {len(skills)}")
    print(f"{cats}: {len(categories)}")

    # 按类别显示
    print(f"\n{by_cat}:")
    for category, skill_list in sorted(categories.items()):
        print(f"\n📂 {category} ({len(skill_list)}{skills_count})")
        for skill in skill_list[:5]:  # 只显示前5个
            print(f"   • {skill}")
        if len(skill_list) > 5:
            print(f"   ... {more} {len(skill_list) - 5}")

def generate_skill_popularity():
    """生成技能流行度排行（模拟数据）/ Generate skill popularity ranking (mock data)"""
    lang = i18n.get_language()
    sep = get_str('separator', lang)
    title = get_str('ranking', lang)
    most_used = get_str('most_used', lang)
    times = get_str('times', lang)

    print("\n" + sep)
    print(title)
    print(sep)

    # 模拟技能使用数据
    usage_data = {
        "github-code-review": 42,
        "systematic-debugging": 38,
        "test-driven-development": 35,
        "jupyter-live-kernel": 32,
        "plan": 28,
        "writing-plans": 25,
        "gitops": 22,
        "session_search": 20,
        "requesting-code-review": 18,
        "subagent-driven-development": 15,
    }

    sorted_skills = sorted(usage_data.items(), key=lambda x: x[1], reverse=True)
    max_count = sorted_skills[0][1] if sorted_skills else 1

    print(f"\n{most_used}:")
    for i, (skill, count) in enumerate(sorted_skills, 1):
        bar_length = 30
        filled = int((count / max_count) * bar_length)
        bar = '█' * filled + '░' * (bar_length - filled)

        rank_icon = "🥇" if i == 1 else "🥈" if i == 2 else "🥉" if i == 3 else f"{i:3d}"
        print(f"  {rank_icon} {skill:30s} {count:3d}{times:6s} {bar}")

def analyze_skill_combinations():
    """分析技能组合使用模式 / Analyze skill combination patterns"""
    lang = i18n.get_language()
    sep = get_str('separator', lang)
    title = get_str('combinations', lang)
    common = get_str('common_combos', lang)
    combo_str = get_str('combo', lang)
    freq = get_str('frequency', lang)
    times = get_str('times', lang)

    print("\n" + sep)
    print(title)
    print(sep)

    # 模拟技能组合数据
    if lang == 'zh':
        combinations = [
            {"name": "开发工作流", "skills": ["plan", "test-driven-development", "github-code-review"], "usage": 15},
            {"name": "调试流程", "skills": ["systematic-debugging", "session_search"], "usage": 12},
            {"name": "文档创作", "skills": ["writing-plans", "obsidian"], "usage": 8},
            {"name": "数据分析", "skills": ["jupyter-live-kernel", "python"], "usage": 6},
        ]
    else:
        combinations = [
            {"name": "Development Workflow", "skills": ["plan", "test-driven-development", "github-code-review"], "usage": 15},
            {"name": "Debug Workflow", "skills": ["systematic-debugging", "session_search"], "usage": 12},
            {"name": "Document Creation", "skills": ["writing-plans", "obsidian"], "usage": 8},
            {"name": "Data Analysis", "skills": ["jupyter-live-kernel", "python"], "usage": 6},
        ]

    if combinations:
        max_usage = max(c['usage'] for c in combinations)

        print(f"\n{common}:")
        for combo in combinations:
            bar_length = 25
            filled = int((combo['usage'] / max_usage) * bar_length)
            bar = '█' * filled + '░' * (bar_length - filled)

            print(f"\n  🔗 {combo['name']} ({combo['usage']}{times})")
            print(f"     {combo_str}: {' + '.join(combo['skills'])}")
            print(f"     {freq}: {bar}")
    else:
        print(f"\n{common}:")
        print("  No combinations found.")

def generate_skill_recommendations():
    """生成技能推荐 / Generate skill recommendations"""
    lang = i18n.get_language()
    sep = get_str('separator', lang)
    title = get_str('suggestions', lang)
    recommended = get_str('recommended', lang)
    reco_work = get_str('reco_work_vis', lang)
    reco_pdf = get_str('reco_pdf', lang)
    reco_baoyu = get_str('reco_baoyu', lang)
    reco_api = get_str('reco_api', lang)
    reco_token = get_str('reco_tokenizer', lang)

    print("\n" + sep)
    print(title)
    print(sep)

    print(f"\n💡 {recommended}:")

    recommendations = [
        {"skill": "work-visualization", "reason": reco_work},
        {"skill": "nano-pdf", "reason": reco_pdf},
        {"skill": "baoyu-skills", "reason": reco_baoyu},
        {"skill": "api-gateway", "reason": reco_api},
        {"skill": "data-tokenizer", "reason": reco_token},
    ]

    for rec in recommendations:
        print(f"\n  📦 {rec['skill']}")
        print(f"     {rec['reason']}")

def generate_skill_health():
    """生成技能健康度报告 / Generate skill health report"""
    lang = i18n.get_language()
    sep = get_str('separator', lang)
    title = get_str('health', lang)
    scanning = get_str('scanning', lang)
    skills_word = get_str('skills_word', lang)
    all_good = get_str('all_good', lang)
    issues = get_str('issues_found', lang)
    missing = get_str('missing_skill_md', lang)
    short = get_str('short_skill_md', lang)

    print("\n" + sep)
    print(title)
    print(sep)

    skills = load_all_skills()

    print(f"\n{scanning} {len(skills)}{skills_word}\n")

    health_issues = []

    for skill_name, meta in skills.items():
        # 检查技能文件是否存在
        skill_dir = SKILLS_DIR / skill_name
        skill_file = skill_dir / 'SKILL.md'

        if not skill_file.exists():
            health_issues.append(f"⚠️  {skill_name}: {missing}")
        elif skill_file.stat().st_size < 500:
            health_issues.append(f"⚠️  {skill_name}: {short}")

    if not health_issues:
        print(all_good)
    else:
        print(f"{issues} {len(health_issues)}:\n")
        for issue in health_issues[:10]:  # 只显示前10个
            print(f"  {issue}")

def main():
    """主函数 / Main function"""
    lang = i18n.get_language()
    sep = get_str('separator', lang)
    title = get_str('title', lang)
    completed = get_str('completed', lang)

    print("\n" + sep)
    print(title)
    print(sep)

    analyze_skill_usage()
    generate_skill_popularity()
    analyze_skill_combinations()
    generate_skill_recommendations()
    generate_skill_health()

    print("\n" + sep)
    print(completed)
    print(sep + "\n")

if __name__ == "__main__":
    main()

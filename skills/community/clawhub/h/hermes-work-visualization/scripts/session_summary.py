#!/usr/bin/env python3
"""
生成当前会话的工作摘要可视化
Generate session summary visualization
"""

import json
import os
from datetime import datetime
from pathlib import Path
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
OUTPUT_DIR = Path.home() / '.hermes/skills/work-visualization/output'
CACHE_DIR = Path.home() / '.hermes/skills/work-visualization/cache'

# Language-specific strings
STRINGS = {
    'zh': {
        'separator': '='*60,
        'title': 'Hermes 工作可视化摘要',
        'task_progress': '任务进度概览',
        'skill_usage': '技能使用统计',
        'tool_calls': '工具调用统计',
        'code_changes': '代码改动统计',
        'session_summary': '会话摘要',
        'completed': '报告生成完成',
        'most_used_skills': '最常用技能:',
        'total_tool_calls': '工具调用总数',
        'times': ' 次',
        'total': '总计',
        'lines': ' 行',
        'session_time': '会话时间',
        'work_duration': '工作时长',
        'main_results': '主要成果',
        'next_steps': '下一步',
        'status': {
            'completed': '已完成',
            'in_progress': '进行中',
            'pending': '待开始'
        },
        'progress': '进度',
        'subtasks': '子任务'
    },
    'en': {
        'separator': '='*60,
        'title': 'Hermes Work Visualization Summary',
        'task_progress': 'Task Progress Overview',
        'skill_usage': 'Skill Usage Statistics',
        'tool_calls': 'Tool Call Statistics',
        'code_changes': 'Code Change Statistics',
        'session_summary': 'Session Summary',
        'completed': 'Report generation completed',
        'most_used_skills': 'Most Used Skills:',
        'total_tool_calls': 'Total Tool Calls',
        'times': ' times',
        'total': 'Total',
        'lines': ' lines',
        'session_time': 'Session Time',
        'work_duration': 'Work Duration',
        'main_results': 'Main Results',
        'next_steps': 'Next Steps',
        'status': {
            'completed': 'Completed',
            'in_progress': 'In Progress',
            'pending': 'Pending'
        },
        'progress': 'Progress',
        'subtasks': 'subtasks'
    }
}

def get_str(key, lang=None):
    """Get localized string"""
    if lang is None:
        lang = i18n.get_language()
    return STRINGS.get(lang, STRINGS['en']).get(key, key)

def load_config():
    """加载配置文件 / Load configuration file"""
    try:
        with open(CONFIG_PATH, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        return {}

def generate_task_progress():
    """生成任务进度可视化 / Generate task progress visualization"""
    lang = i18n.get_language()
    sep = get_str('separator', lang)
    title = get_str('task_progress', lang)
    status = get_str('status', lang)
    progress_str = get_str('progress', lang)
    subtasks = get_str('subtasks', lang)

    print("\n" + sep)
    print(title)
    print(sep)

    tasks = [
        {"name": "Data import and analysis" if lang == 'en' else "数据导入和分析", "completed": 2, "total": 3, "status": status['in_progress']},
        {"name": "Create visualization scripts" if lang == 'en' else "创建可视化脚本", "completed": 1, "total": 5, "status": status['in_progress']},
        {"name": "Testing and optimization" if lang == 'en' else "测试和优化", "completed": 0, "total": 4, "status": status['pending']},
    ]

    for task in tasks:
        progress = int((task['completed'] / task['total']) * 100)
        bar_length = 50
        filled = int((progress / 100) * bar_length)
        bar = '=' * filled + '-' * (bar_length - filled)

        status_icon = "✓" if progress == 100 else "⚙" if progress > 0 else "○"

        print(f"\n{status_icon} {task['name']}")
        print(f"   [{bar}] {progress}%")
        print(f"   {progress_str}: {task['completed']}/{task['total']} {subtasks}")

def generate_skill_usage():
    """生成技能使用统计 / Generate skill usage statistics"""
    lang = i18n.get_language()
    sep = get_str('separator', lang)
    title = get_str('skill_usage', lang)
    most_used = get_str('most_used_skills', lang)

    print("\n" + sep)
    print(title)
    print(sep)

    # 模拟技能使用数据
    skills = [
        {"name": "terminal", "count": 15},
        {"name": "file_operations", "count": 12},
        {"name": "search", "count": 8},
        {"name": "browser", "count": 5},
        {"name": "memory", "count": 3},
    ]

    max_count = max(s['count'] for s in skills)
    times_str = get_str('times', lang)

    print(f"\n{most_used}")
    for i, skill in enumerate(skills, 1):
        bar_length = 30
        filled = int((skill['count'] / max_count) * bar_length)
        bar = '█' * filled + '░' * (bar_length - filled)

        print(f"  {i:2d}. {skill['name']:20s} {skill['count']:3d}{times_str:6s} {bar}")

def generate_tool_calls():
    """生成工具调用统计 / Generate tool call statistics"""
    lang = i18n.get_language()
    sep = get_str('separator', lang)
    title = get_str('tool_calls', lang)
    total_str = get_str('total_tool_calls', lang)

    print("\n" + sep)
    print(title)
    print(sep)

    tools = [
        {"name": "terminal", "count": 28},
        {"name": "write_file", "count": 15},
        {"name": "read_file", "count": 12},
        {"name": "search_files", "count": 8},
        {"name": "patch", "count": 6},
    ]

    total = sum(t['count'] for t in tools)
    max_count = max(t['count'] for t in tools)
    times_str = get_str('times', lang)

    print(f"\n{total_str}: {total} {times_str}\n")

    for tool in tools:
        percentage = (tool['count'] / total) * 100
        bar_length = 40
        filled = int((tool['count'] / max_count) * bar_length)
        bar = '█' * filled + '░' * (bar_length - filled)

        print(f"  {tool['name']:20s} {tool['count']:3d}  ({percentage:5.1f}%)  {bar}")

def generate_code_changes():
    """生成代码改动统计 / Generate code change statistics"""
    lang = i18n.get_language()
    sep = get_str('separator', lang)
    title = get_str('code_changes', lang)
    total = get_str('total', lang)
    lines = get_str('lines', lang)

    print("\n" + sep)
    print(title)
    print(sep)

    files = [
        {"name": "SKILL.md", "added": 150, "deleted": 0},
        {"name": "config.json", "added": 20, "deleted": 5},
        {"name": "scripts/session_summary.py", "added": 85, "deleted": 12},
    ]

    total_added = sum(f['added'] for f in files)
    total_deleted = sum(f['deleted'] for f in files)

    print(f"\n{total}: +{total_added} -{total_deleted} {lines}\n")

    total_changes = total_added + total_deleted
    for file in files:
        change = file['added'] + file['deleted']
        bar_length = 20
        if total_changes > 0:
            filled = min(int((change / total_changes) * bar_length), bar_length)
        else:
            filled = 0
        bar = '█' * filled + '░' * (bar_length - filled)

        print(f"  {file['name']}")
        print(f"    +{file['added']:3d} -{file['deleted']:3d}  {bar}")

def generate_session_summary():
    """生成会话摘要 / Generate session summary"""
    lang = i18n.get_language()
    sep = get_str('separator', lang)
    title = get_str('session_summary', lang)
    session_time = get_str('session_time', lang)
    work_duration = get_str('work_duration', lang)
    main_results = get_str('main_results', lang)
    next_steps = get_str('next_steps', lang)

    print("\n" + sep)
    print(title)
    print(sep)

    now = datetime.now()

    print(f"\n{session_time}: {now.strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"{work_duration}: ~15 minutes" if lang == 'en' else "约 15 分钟")
    print(f"\n{main_results}:")
    print("  ✓ Created work-visualization skill" if lang == 'en' else "  ✓ 创建 work-visualization 技能包")
    print("  ✓ Configured visualization parameters" if lang == 'en' else "  ✓ 配置可视化参数")
    print("  ✓ Generated session summary scripts" if lang == 'en' else "  ✓ 生成会话摘要脚本")
    print(f"\n{next_steps}:")
    print("  • Complete other core scripts (generate_report.py, skill_stats.py)" if lang == 'en' else "  • 完成其他核心脚本")
    print("  • Add real-time monitoring" if lang == 'en' else "  • 添加实时监控功能")
    print("  • Test and optimize visualization" if lang == 'en' else "  • 测试和优化可视化效果")

def main():
    """主函数 / Main function"""
    lang = i18n.get_language()
    sep = get_str('separator', lang)
    title = get_str('title', lang)
    completed = get_str('completed', lang)

    print("\n" + sep)
    print(title)
    print(sep)

    generate_task_progress()
    generate_skill_usage()
    generate_tool_calls()
    generate_code_changes()
    generate_session_summary()

    print("\n" + sep)
    print(completed)
    print(sep + "\n")

if __name__ == "__main__":
    main()

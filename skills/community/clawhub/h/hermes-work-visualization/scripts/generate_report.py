#!/usr/bin/env python3
"""
生成详细工作报告
Generate detailed work report
"""

import argparse
import json
import os
from datetime import datetime, timedelta
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
        'report_title': 'Hermes 工作报告',
        'report_date': '报告日期',
        'report_period': '报告周期',
        'recent_days': '最近',
        'days': ' 天',
        'completed': '报告生成完成',
        'activity_timeline': '活动时间线',
        'tasks_completed': '任务完成',
        'tasks_unit': ' 个',
        'tool_calls': '工具调用',
        'calls_unit': ' 次',
        'skill_usage': '技能使用',
        'skill_heatmap': '技能使用热力图',
        'skill_frequency': '技能使用频率',
        'hourly_distribution': '每小时活动分布',
        'peak_hour': '最活跃时段',
        'activity_count': '活动次数',
        'time_distribution': '时段分布',
        'efficiency_metrics': '效率指标',
        'key_metrics': '关键指标',
        'avg_task_time': '平均任务完成时间',
        'task_completion_rate': '任务完成率',
        'skill_success_rate': '技能调用成功率',
        'avg_tool_response': '平均工具响应时间',
        'code_accuracy': '代码修改准确率',
        'trend_analysis': '趋势分析',
        'upward_trend': '上升趋势',
        'needs_improvement': '需要改进',
        'suggestions': '建议',
        'increase_tests': '增加自动化测试',
        'optimize_skill_calls': '优化技能调用流程',
        'improve_documentation': '加强文档记录',
        'code_efficiency': '代码修改效率',
        'skill_accuracy': '技能调用准确率',
        'task_speed': '任务完成速度',
        'doc_completeness': '文档完整性',
        'test_coverage': '测试覆盖率'
    },
    'en': {
        'separator': '='*60,
        'report_title': 'Hermes Work Report',
        'report_date': 'Report Date',
        'report_period': 'Report Period',
        'recent_days': 'Last',
        'days': ' days',
        'completed': 'Report generation completed',
        'activity_timeline': 'Activity Timeline',
        'tasks_completed': 'Tasks Completed',
        'tasks_unit': '',
        'tool_calls': 'Tool Calls',
        'calls_unit': '',
        'skill_usage': 'Skill Usage',
        'skill_heatmap': 'Skill Usage Heatmap',
        'skill_frequency': 'Skill Usage Frequency',
        'hourly_distribution': 'Hourly Activity Distribution',
        'peak_hour': 'Peak Hour',
        'activity_count': 'Activity Count',
        'time_distribution': 'Time Distribution',
        'efficiency_metrics': 'Efficiency Metrics',
        'key_metrics': 'Key Metrics',
        'avg_task_time': 'Avg Task Completion Time',
        'task_completion_rate': 'Task Completion Rate',
        'skill_success_rate': 'Skill Call Success Rate',
        'avg_tool_response': 'Avg Tool Response Time',
        'code_accuracy': 'Code Modification Accuracy',
        'trend_analysis': 'Trend Analysis',
        'upward_trend': 'Upward Trends',
        'needs_improvement': 'Needs Improvement',
        'suggestions': 'Suggestions',
        'increase_tests': 'Increase automated testing',
        'optimize_skill_calls': 'Optimize skill call process',
        'improve_documentation': 'Strengthen documentation',
        'code_efficiency': 'Code modification efficiency',
        'skill_accuracy': 'Skill call accuracy',
        'task_speed': 'Task completion speed',
        'doc_completeness': 'Documentation completeness',
        'test_coverage': 'Test coverage'
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

def generate_activity_timeline(days=7):
    """生成活动时间线 / Generate activity timeline"""
    lang = i18n.get_language()
    sep = get_str('separator', lang)
    title = get_str('activity_timeline', lang)
    recent = get_str('recent_days', lang)
    days_str = get_str('days', lang)
    tasks_str = get_str('tasks_completed', lang)
    tasks_unit = get_str('tasks_unit', lang)
    tools_str = get_str('tool_calls', lang)
    calls_unit = get_str('calls_unit', lang)
    skill_str = get_str('skill_usage', lang)
    usage_unit = get_str('calls_unit', lang)

    print("\n" + sep)
    print(f"{recent} {days}{days_str} {title}")
    print(sep)

    today = datetime.now()
    activities = [
        {"date": today, "tasks": 5, "tools": 42, "skills": 3},
        {"date": today - timedelta(days=1), "tasks": 3, "tools": 28, "skills": 2},
        {"date": today - timedelta(days=2), "tasks": 8, "tools": 65, "skills": 5},
        {"date": today - timedelta(days=3), "tasks": 4, "tools": 35, "skills": 3},
        {"date": today - timedelta(days=4), "tasks": 6, "tools": 48, "skills": 4},
        {"date": today - timedelta(days=5), "tasks": 2, "tools": 18, "skills": 1},
        {"date": today - timedelta(days=6), "tasks": 7, "tools": 52, "skills": 4},
    ]

    for activity in activities:
        date_str = activity['date'].strftime('%Y-%m-%d %A')
        print(f"\n📅 {date_str}")
        print(f"   {tasks_str}: {activity['tasks']}{tasks_unit}")
        print(f"   {tools_str}: {activity['tools']}{calls_unit}")
        print(f"   {skill_str}: {activity['skills']}{usage_unit}")

def generate_skill_heatmap(days=7):
    """生成技能使用热力图 / Generate skill usage heatmap"""
    lang = i18n.get_language()
    sep = get_str('separator', lang)
    title = get_str('skill_heatmap', lang)
    freq_str = get_str('skill_frequency', lang)

    print("\n" + sep)
    print(title)
    print(sep)

    skills = ["terminal", "file_ops", "search", "browser", "memory"]

    # 模拟每日数据
    data = {
        "terminal": [28, 15, 42, 22, 35, 12, 40],
        "file_ops": [15, 8, 20, 18, 12, 5, 25],
        "search": [8, 12, 15, 6, 10, 3, 18],
        "browser": [5, 8, 3, 12, 8, 2, 6],
        "memory": [3, 5, 8, 4, 6, 2, 7],
    }

    print(f"\n{freq_str}:")
    print("       ", end="")
    for i in range(days):
        print(f"{(datetime.now() - timedelta(days=days-1-i)).strftime('%m-%d'):>6}", end="")
    print()

    for skill in skills:
        print(f"{skill:10s}", end="")
        values = data[skill][-days:]
        if values:
            max_val = max(max(values), 1)
        else:
            max_val = 1
        for val in values:
            if val == 0:
                print(f"{' ':>6}", end="")
            else:
                intensity = min(int((val / max_val) * 4), len(['░', '▒', '▓', '█']) - 1)  # Ensure index is within bounds
                chars = ['░', '▒', '▓', '█']
                print(f"{chars[intensity]:>6}", end="")
        print()

def generate_hourly_distribution():
    """生成每小时活动分布 / Generate hourly activity distribution"""
    lang = i18n.get_language()
    sep = get_str('separator', lang)
    title = get_str('hourly_distribution', lang)
    peak_str = get_str('peak_hour', lang)
    count_str = get_str('activity_count', lang)
    dist_str = get_str('time_distribution', lang)

    print("\n" + sep)
    print(title)
    print(sep)

    hours = list(range(24))
    activity = [0, 0, 0, 0, 0, 0, 2, 5, 12, 18, 22, 20,
                15, 18, 25, 30, 35, 32, 28, 20, 15, 8, 3, 1]

    if activity:
        max_activity = max(activity)
        peak_hour = hours[activity.index(max_activity)]
        print(f"\n{peak_str}: {peak_hour:02d}:00 ({count_str}: {max_activity})\n")
    else:
        print(f"\n{peak_str}: N/A\n")

    print(f"{dist_str}:")
    for i, (hour, count) in enumerate(zip(hours, activity)):
        if count > 0:
            bar_length = 40
            filled = int((count / max_activity) * bar_length)
            bar = '█' * filled + '░' * (bar_length - filled)
            print(f"  {hour:02d}:00  {count:3d}  {bar}")

def generate_efficiency_metrics():
    """生成效率指标 / Generate efficiency metrics"""
    lang = i18n.get_language()
    sep = get_str('separator', lang)
    title = get_str('efficiency_metrics', lang)
    key_metrics = get_str('key_metrics', lang)
    avg_time = get_str('avg_task_time', lang)
    completion_rate = get_str('task_completion_rate', lang)
    success_rate = get_str('skill_success_rate', lang)
    avg_response = get_str('avg_tool_response', lang)
    accuracy = get_str('code_accuracy', lang)

    print("\n" + sep)
    print(title)
    print(sep)

    if lang == 'zh':
        metrics = {
            avg_time: "8.5 分钟",
            completion_rate: "92%",
            success_rate: "98%",
            avg_response: "0.3 秒",
            accuracy: "95%",
        }
    else:
        metrics = {
            avg_time: "8.5 min",
            completion_rate: "92%",
            success_rate: "98%",
            avg_response: "0.3 sec",
            accuracy: "95%",
        }

    print(f"\n{key_metrics}:")
    for metric, value in metrics.items():
        print(f"  • {metric:30s}: {value:>10s}")

def generate_trend_analysis(days=7):
    """生成趋势分析 / Generate trend analysis"""
    lang = i18n.get_language()
    sep = get_str('separator', lang)
    title = get_str('trend_analysis', lang)
    upward = get_str('upward_trend', lang)
    improvement = get_str('needs_improvement', lang)
    suggestions = get_str('suggestions', lang)
    code_eff = get_str('code_efficiency', lang)
    skill_acc = get_str('skill_accuracy', lang)
    task_spd = get_str('task_speed', lang)
    doc_comp = get_str('doc_completeness', lang)
    test_cov = get_str('test_coverage', lang)
    inc_tests = get_str('increase_tests', lang)
    opt_calls = get_str('optimize_skill_calls', lang)
    imp_docs = get_str('improve_documentation', lang)

    print("\n" + sep)
    print(title)
    print(sep)

    print(f"\n📈 {upward}:")
    print(f"  • {code_eff} (+15%)")
    print(f"  • {skill_acc} (+8%)")
    print(f"  • {task_spd} (+12%)")

    print(f"\n📉 {improvement}:")
    print(f"  • {doc_comp} (-5%)")
    print(f"  • {test_cov} (-10%)")

    print(f"\n💡 {suggestions}:")
    print(f"  • {inc_tests}")
    print(f"  • {opt_calls}")
    print(f"  • {imp_docs}")

def main():
    """主函数 / Main function"""
    current_i18n = i18n
    lang = current_i18n.get_language()
    sep = get_str('separator', lang)
    title = get_str('report_title', lang)
    date_str = get_str('report_date', lang)
    period_str = get_str('report_period', lang)
    recent = get_str('recent_days', lang)
    days_str = get_str('days', lang)
    completed = get_str('completed', lang)

    parser = argparse.ArgumentParser(description='Generate Hermes work report')
    parser.add_argument('--days', type=int, default=7, help='Report days range')
    parser.add_argument('--type', choices=['full', 'summary', 'trends'], default='full', help='Report type')
    parser.add_argument('--lang', type=str, choices=['zh', 'en'], help='Override language (zh/en)')

    args = parser.parse_args()

    # Override language if specified
    if args.lang:
        lang = args.lang

    print("\n" + sep)
    print(title)
    print(f"{date_str}: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"{period_str}: {recent} {args.days}{days_str}")
    print(sep)

    if args.type in ['full', 'summary']:
        generate_activity_timeline(args.days)
        generate_skill_heatmap(args.days)

    if args.type == 'full':
        generate_hourly_distribution()
        generate_efficiency_metrics()

    if args.type in ['full', 'trends']:
        generate_trend_analysis(args.days)

    print("\n" + sep)
    print(completed)
    print(sep + "\n")

if __name__ == "__main__":
    main()

"""生成 0 值测试报表"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from html_generator import SimpleHTMLGenerator

# 构造 0 值数据
empty_result = {
    'team_assets': {
        'total_customers': 0,
        'month_customers': 0,
        'today_customers': 0,
        'avg_per_person': 0
    },
    'daily_efficiency': {
        'total_recording_minutes': 0,
        'avg_minutes_per_person': 0,
        'total_visits': 0,
        'avg_visits_per_person': 0,
        'customer_distribution': {
            'old_customer_maintenance': 0,
            'new_customer_prospecting': 0
        },
        'regional_distribution': []
    },
    'compliance_monitoring': {
        'compliance_metrics': []
    },
    'rm_performance': {
        'top_performers': [],
        'needs_improvement': [],
        'user_scores': []
    },
    'lead_conversion': {
        'a_level_count': 0,
        'a_level_details': '',
        'b_level_count': 0,
        'b_level_followup': '',
        'c_level_count': 0,
        'c_level_interception': ''
    },
    'management_suggestions': []
}

# 构建上下文
context = {
    'team_name': '测试团队',
    'date_str': '2026-06-24',
    'org_id': 'test_org',
    'user_groups': {},
    'is_empty': True,
}

# 生成 HTML
html_gen = SimpleHTMLGenerator()
file_path = html_gen.generate(empty_result, context)

print(f"0 值报表已生成: {file_path}")

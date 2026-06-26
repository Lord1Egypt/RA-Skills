"""
Office Pro - Report Templates

Built-in report templates with professional formatting.
"""

# Meeting Minutes Template
MEETING_MINUTES_TEMPLATE = {
    'title': '会议纪要',
    'default_data': {
        'meeting_type': '周例会',
        'meeting_time': '09:00-10:00',
        'meeting_location': '会议室A',
    },
    'sections': [
        {
            'title': '会议基本信息',
            'content': '''会议主题：{meeting_title}
会议类型：{meeting_type}
会议时间：{meeting_date} {meeting_time}
会议地点：{meeting_location}
主持人：{chairperson}
记录人：{secretary}
参会人员：{attendees}'''
        },
        {
            'title': '会议议程',
            'content': '''{agenda}'''
        },
        {
            'title': '讨论内容',
            'content': '''{discussion}'''
        },
        {
            'title': '决议事项',
            'content': '''{decisions}'''
        },
        {
            'title': '行动项',
            'content': '''{action_items}'''
        },
    ]
}

# Work Report Template
WORK_REPORT_TEMPLATE = {
    'title': '工作报告',
    'default_data': {
        'report_period': '2024年第一季度',
        'department': '技术部',
    },
    'sections': [
        {
            'title': '报告概述',
            'content': '''报告人：{reporter}
报告期间：{report_period}
部门：{department}
报告日期：{report_date}'''
        },
        {
            'title': '工作总结',
            'content': '''{summary}'''
        },
        {
            'title': '主要成果',
            'content': '''{achievements}'''
        },
        {
            'title': '存在问题',
            'content': '''{problems}'''
        },
        {
            'title': '下一步计划',
            'content': '''{next_steps}'''
        },
    ]
}

# Report templates dictionary
REPORT_TEMPLATES = {
    'meeting_minutes': MEETING_MINUTES_TEMPLATE,
    'work_report': WORK_REPORT_TEMPLATE,
}

__all__ = ['REPORT_TEMPLATES']

#!/usr/bin/env python3
"""
Personal Growth Advisor - Main Script
Provides goal setting, habit formation, and growth tracking
"""

import sys
import json
import argparse
from typing import Dict, List, Optional
from datetime import datetime


class GrowthAdvisor:
    """个人成长顾问"""
    
    def create_goal(self, goal: str, timeline: str = "3个月", obstacles: str = "") -> Dict:
        """创建目标（SMART框架）"""
        return {
            'goal': goal,
            'timeline': timeline,
            'smart_breakdown': self._smart_breakdown(goal, timeline),
            'milestones': self._create_milestones(goal, timeline),
            'obstacles': obstacles.split(',') if obstacles else [],
            'solutions': self._suggest_solutions(obstacles),
            'tips': [
                '每天早上先做与目标相关的一件事',
                '记录进度，保持可见性',
                '设置提醒和问责机制',
                '庆祝每个小里程碑'
            ]
        }
    
    def _smart_breakdown(self, goal: str, timeline: str) -> Dict:
        """SMART目标分解"""
        return {
            'Specific': f'明确定义: {goal}',
            'Measurable': '设定可衡量的指标和KPI',
            'Achievable': '评估资源和能力，制定可行计划',
            'Relevant': '确认目标与长期价值观一致',
            'Time-bound': f'设定明确的时间节点: {timeline}'
        }
    
    def _create_milestones(self, goal: str, timeline: str) -> List[Dict]:
        """创建里程碑"""
        milestones = [
            {'week': 1, 'title': '启动阶段', 'description': '明确目标，制定详细计划'},
            {'week': 2, 'title': '适应阶段', 'description': '开始行动，建立基础'},
            {'week': 3, 'title': '推进阶段', 'description': '持续执行，解决障碍'},
            {'week': 4, 'title': '复盘阶段', 'description': '评估进度，调整策略'}
        ]
        return milestones
    
    def _suggest_solutions(self, obstacles: str) -> List[str]:
        """解决障碍建议"""
        common_solutions = [
            '将大目标分解为小步骤',
            '建立问责机制（朋友、APP）',
            '消除干扰，创造专注环境',
            '使用两分钟规则启动',
            '设置奖励机制'
        ]
        return common_solutions
    
    def create_habit(self, habit: str, frequency: str = "Daily", cue: str = "", reward: str = "") -> Dict:
        """创建习惯"""
        return {
            'habit': habit,
            'frequency': frequency,
            'habit_loop': {
                'cue': cue or '设定触发条件（如：起床后）',
                'routine': f'执行: {habit}',
                'reward': reward or '设定奖励（如：喝咖啡）'
            },
            'tips': [
                '从最小可行行动开始',
                '保持一致性而非完美',
                '不要打断连续记录',
                '逐渐增加难度'
            ],
            'stacking': '在现有习惯后添加新习惯',
            'environment': '让好习惯更容易，坏习惯更难'
        }
    
    def generate_review(self) -> Dict:
        """生成复盘模板"""
        return {
            'weekly_review': {
                'accomplishments': ['列出本周完成的事项'],
                'learnings': ['本周学到了什么'],
                'challenges': ['遇到什么困难'],
                'next_week': ['下周计划']
            },
            'questions': [
                '这周我完成了什么？',
                '我遇到了哪些挑战？',
                '我从中学到了什么？',
                '下周我要改进什么？',
                '我的感受如何？'
            ]
        }
    
    def get_motivation(self, category: str = "general") -> Dict:
        """动机激励"""
        quotes = {
            'general': [
                '成长是一辈子的事情。',
                '每天进步1%，一年后强大37倍。',
                '最大的挑战就是战胜自己。'
            ],
            'habit': [
                '习惯比动力更可靠。',
                '成功的关键在于日常的坚持。',
                '不要追求完美，要追求进步。'
            ],
            'goal': [
                '目标是梦想的路线图。',
                '伟大的成就来自于小目标的累积。',
                '有目标的人生更有方向。'
            ]
        }
        
        return {
            'category': category,
            'quotes': quotes.get(category, quotes['general']),
            'tips': [
                '相信过程，相信自己',
                '保持耐心，长期思维',
                '庆祝每一次进步'
            ]
        }
    
    def time_management(self) -> Dict:
        """时间管理建议"""
        return {
            'techniques': [
                {'name': '番茄工作法', 'desc': '25分钟专注，5分钟休息'},
                {'name': '时间块', 'desc': '将一天分成不同主题的时间块'},
                {'name': 'Eat the Frog', 'desc': '先完成最难的任务'},
                {'name': '2分钟规则', 'desc': '2分钟内能做的事立即做'}
            ],
            'prioritization': [
                '重要且紧急 - 立即处理',
                '重要不紧急 - 计划处理',
                '紧急不重要 - 委托处理',
                '不重要不紧急 - 减少/删除'
            ],
            'tips': [
                '每天第一件事做最重要的决定',
                '保护你的专注时间',
                '设置截止日期',
                '定期清理/整理'
            ]
        }


def format_goal(result: Dict) -> str:
    """格式化目标输出"""
    output = []
    output.append("=" * 50)
    output.append(f"🎯 目标: {result['goal']}")
    output.append("=" * 50)
    output.append(f"📅 时间线: {result['timeline']}")
    
    output.append("\n📋 SMART 分解:")
    for k, v in result['smart_breakdown'].items():
        output.append(f"  {k}: {v}")
    
    output.append("\n🏁 里程碑:")
    for m in result['milestones']:
        output.append(f"  Week {m['week']}: {m['title']} - {m['description']}")
    
    output.append("\n💡 建议:")
    for tip in result['tips']:
        output.append(f"  • {tip}")
    
    output.append("\n" + "=" * 50)
    return "\n".join(output)


def format_habit(result: Dict) -> str:
    """格式化习惯输出"""
    output = []
    output.append("=" * 50)
    output.append(f"🔄 习惯: {result['habit']}")
    output.append("=" * 50)
    output.append(f"📅 频率: {result['frequency']}")
    
    output.append("\n🔄 习惯循环:")
    for k, v in result['habit_loop'].items():
        output.append(f"  {k}: {v}")
    
    output.append("\n💡 养成技巧:")
    for tip in result['tips']:
        output.append(f"  • {tip}")
    
    output.append("\n" + "=" * 50)
    return "\n".join(output)


def main():
    parser = argparse.ArgumentParser(description='Personal Growth Advisor - 个人成长顾问')
    parser.add_argument('command', choices=['goal', 'habit', 'review', 'motivation', 'time', 'demo'],
                       help='命令类型')
    parser.add_argument('--goal', '-g', help='目标内容')
    parser.add_argument('--timeline', '-t', default='3个月', help='时间线')
    parser.add_argument('--habit', help='习惯内容')
    parser.add_argument('--frequency', '-f', default='Daily', help='频率')
    parser.add_argument('--json', action='store_true', help='JSON输出')
    
    args = parser.parse_args()
    
    advisor = GrowthAdvisor()
    
    if args.command == 'demo':
        print("=== 目标设定示例 ===")
        result = advisor.create_goal('学习Python编程', '6个月')
        print(format_goal(result))
        print("\n=== 习惯养成示例 ===")
        result = advisor.create_habit('每天运动30分钟', 'Daily', '下班后', '洗澡')
        print(format_habit(result))
        return
    
    result = None
    if args.command == 'goal':
        goal = args.goal or '学习新技能'
        result = advisor.create_goal(goal, args.timeline)
    elif args.command == 'habit':
        habit = args.habit or '每天阅读30分钟'
        result = advisor.create_habit(habit, args.frequency)
    elif args.command == 'review':
        result = advisor.generate_review()
    elif args.command == 'motivation':
        result = advisor.get_motivation()
    elif args.command == 'time':
        result = advisor.time_management()
    
    if args.json:
        print(json.dumps(result, indent=2, ensure_ascii=False))
    else:
        if args.command == 'goal':
            print(format_goal(result))
        elif args.command == 'habit':
            print(format_habit(result))
        else:
            print(json.dumps(result, indent=2, ensure_ascii=False))


if __name__ == '__main__':
    main()

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
警察执法资格考试机器人助手核心模块
Police Qualification Exam Bot Core Module
"""

import json
import os
import re
from datetime import datetime
from typing import Dict, List, Optional, Any

class PQEBotCore:
    """警察执法资格考试机器人助手核心类"""
    
    def __init__(self, data_dir: str = None):
        """初始化PQEBot助手"""
        if data_dir:
            self.data_dir = data_dir
        else:
            # 从脚本目录向上找到数据目录
            script_dir = os.path.dirname(__file__)
            self.data_dir = os.path.join(script_dir, '../data')
        
        self.exam_outline = self.load_exam_outline()
        self.past_papers = self.load_past_papers()
        self.knowledge_points = self.load_knowledge_points()
        self.user_session = {}  # 存储用户会话状态
    
    def reset_session(self):
        """重置用户会话"""
        self.user_session = {
            'exam_level': None,      # 'basic' 或 'advanced'
            'mode': None,           # 'practice' 或 'simulation' 或 'past_papers'
            'subject': None,        # 当前科目
            'progress': {}          # 学习进度
        }
        
    def load_exam_outline(self) -> Dict:
        """加载考试大纲"""
        outline_path = os.path.join(self.data_dir, 'exam_outline_2026.json')
        if os.path.exists(outline_path):
            try:
                with open(outline_path, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except:
                pass
        
        # 默认大纲结构
        return {
            "version": "2026",
            "title": "公安机关人民警察执法资格等级考试大纲（2026年版）",
            "subjects": [
                {
                    "name": "公安基础理论",
                    "chapters": [
                        {"name": "公安工作概述", "weight": 0.1},
                        {"name": "公安机关组织管理", "weight": 0.15},
                        {"name": "公安队伍建设", "weight": 0.1}
                    ]
                },
                {
                    "name": "法律基础知识",
                    "chapters": [
                        {"name": "宪法及相关法律", "weight": 0.1},
                        {"name": "行政法与行政诉讼法", "weight": 0.2},
                        {"name": "刑法与刑事诉讼法", "weight": 0.25},
                        {"name": "民法与民事诉讼法", "weight": 0.1},
                        {"name": "警察法及相关法规", "weight": 0.15}
                    ]
                },
                {
                    "name": "警务实战技能",
                    "chapters": [
                        {"name": "警务指挥与战术", "weight": 0.1},
                        {"name": "现场处置规范", "weight": 0.15},
                        {"name": "执法安全防护", "weight": 0.05}
                    ]
                }
            ],
            "exam_info": {
                "exam_levels": ["初级", "中级", "高级"],
                "question_types": ["单选题", "多选题", "判断题", "案例分析题"],
                "total_score": 100,
                "passing_score": 60,
                "exam_duration": "120分钟"
            }
        }
    
    def load_past_papers(self) -> Dict:
        """加载历年真题"""
        papers_path = os.path.join(self.data_dir, 'past_papers.json')
        if os.path.exists(papers_path):
            try:
                with open(papers_path, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except Exception as e:
                print(f"加载真题数据出错: {e}")
                return self._get_default_papers()
        
        return self._get_default_papers()
    
    def _get_default_papers(self) -> Dict:
        """获取默认真题数据"""
        return {
            "past_papers": [],
            "exam_statistics": {
                "years_covered": [],
                "total_papers": 0,
                "total_questions": 0
            },
            "high_frequency_topics": []
        }
    
    def load_knowledge_points(self) -> Dict:
        """加载知识点库"""
        points_path = os.path.join(self.data_dir, 'knowledge_points.json')
        if os.path.exists(points_path):
            try:
                with open(points_path, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except:
                pass
        
        return {
            "points": [],
            "categories": []
        }
    
    def get_exam_outline_summary(self) -> str:
        """获取考试大纲摘要"""
        outline = self.exam_outline
        summary = f"《{outline.get('title', '执法资格考试大纲')}》\n"
        summary += f"版本：{outline.get('version', '2026')}年版\n"
        summary += f"来源：{outline.get('source', '相关考试资料整理')}\n\n"
        
        # 考试级别
        if 'exam_levels' in outline:
            summary += "📋 考试级别：\n"
            for level in outline['exam_levels']:
                summary += f"  • {level.get('level', '')}: {level.get('target', '')}\n"
        
        # 考试科目
        summary += "\n📚 考试科目及比重：\n"
        if 'subjects' in outline:
            for subject in outline['subjects']:
                weight = subject.get('weight', 0)
                summary += f"  • {subject.get('name', '')} ({weight*100:.0f}%)\n"
        
        # 考试参数
        if 'exam_parameters' in outline:
            params = outline['exam_parameters']
            summary += f"\n📊 考试参数：\n"
            summary += f"  • 总分：{params.get('total_score', 100)}分\n"
            summary += f"  • 及格线：{params.get('passing_score', 60)}分\n"
            summary += f"  • 考试时长：{params.get('exam_duration_minutes', 120)}分钟\n"
            summary += f"  • 题目数量：{params.get('question_count', 100)}题\n"
            summary += f"  • 考试形式：{params.get('exam_mode', '闭卷笔试')}\n"
        
        # 题型分布
        if 'question_types' in outline:
            summary += f"\n📝 题型分布：\n"
            for qtype in outline['question_types']:
                proportion = qtype.get('proportion', 0) * 100
                summary += f"  • {qtype.get('type', '')}: {proportion:.0f}%\n"
        
        return summary
    
    def get_subject_details(self, subject_name: str) -> Optional[str]:
        """获取具体科目详情"""
        for subject in self.exam_outline['subjects']:
            if subject['name'] == subject_name:
                details = f"📖 {subject['name']} 详细内容：\n\n"
                for i, chapter in enumerate(subject['chapters'], 1):
                    details += f"{i}. {chapter['name']} (占比：{chapter['weight']*100:.0f}%)\n"
                return details
        return None
    
    def search_questions(self, keyword: str, limit: int = 5) -> List[Dict]:
        """搜索题目"""
        results = []
        # 这里可以连接题库数据库进行搜索
        # 目前返回模拟结果
        return results
    
    def generate_study_plan(self, days: int = 30, hours_per_day: int = 2) -> Dict:
        """生成学习计划"""
        plan = {
            "total_days": days,
            "daily_hours": hours_per_day,
            "total_hours": days * hours_per_day,
            "schedule": [],
            "goals": []
        }
        
        # 简单的计划生成逻辑
        subjects = self.exam_outline['subjects']
        days_per_subject = max(1, days // len(subjects))
        
        for i, subject in enumerate(subjects):
            start_day = i * days_per_subject + 1
            end_day = min((i + 1) * days_per_subject, days)
            plan['schedule'].append({
                "subject": subject['name'],
                "days": f"第{start_day}-{end_day}天",
                "focus": "掌握核心知识点和常考题型"
            })
        
        # 最后几天安排复习和模拟
        review_days = min(5, days // 5)
        if review_days > 0:
            plan['schedule'].append({
                "subject": "总复习与模拟考试",
                "days": f"第{days-review_days+1}-{days}天",
                "focus": "查漏补缺，进行模拟考试训练"
            })
        
        return plan
    
    def get_high_frequency_points(self, top_n: int = 10) -> List[Dict]:
        """获取高频考点"""
        # 优先从真题数据中获取
        if "high_frequency_topics" in self.past_papers and self.past_papers["high_frequency_topics"]:
            topics = self.past_papers["high_frequency_topics"]
            return topics[:top_n]
        
        # 备用数据
        points = [
            {"topic": "行政处罚程序", "frequency": 0.92, "appears_in_years": [2023, 2024, 2025], "question_count": 28},
            {"topic": "正当防卫与紧急避险", "frequency": 0.88, "appears_in_years": [2024, 2025], "question_count": 22},
            {"topic": "人民警察职责权限", "frequency": 0.85, "appears_in_years": [2023, 2024, 2025], "question_count": 25},
            {"topic": "证据规则", "frequency": 0.82, "appears_in_years": [2024, 2025], "question_count": 20},
            {"topic": "强制措施适用", "frequency": 0.78, "appears_in_years": [2024, 2025], "question_count": 18},
            {"topic": "刑事立案标准", "frequency": 0.75, "appears_in_years": [2024, 2025], "question_count": 15},
            {"topic": "治安调解原则", "frequency": 0.72, "appears_in_years": [2023, 2024], "question_count": 12},
            {"topic": "执法记录仪使用", "frequency": 0.68, "appears_in_years": [2025], "question_count": 8},
            {"topic": "现场处置原则", "frequency": 0.65, "appears_in_years": [2024, 2025], "question_count": 10},
            {"topic": "警察职业道德", "frequency": 0.60, "appears_in_years": [2023, 2024], "question_count": 9}
        ]
        return points[:top_n]
    
    def get_past_papers_summary(self) -> str:
        """获取历年真题摘要"""
        if "past_papers" not in self.past_papers:
            return "暂无真题数据"
        
        papers = self.past_papers["past_papers"]
        if not papers:
            return "暂无真题数据"
        
        summary = "📚 历年真题库\n\n"
        
        for paper in papers:
            summary += f"📅 {paper['year']}年 {paper['exam_level']}考试\n"
            summary += f"   题目数量：{paper['question_count']}题\n"
            if 'total_score' in paper:
                summary += f"   总分：{paper['total_score']}分\n"
            if 'passing_score' in paper:
                summary += f"   及格：{paper['passing_score']}分\n"
            if 'subjects_covered' in paper:
                summary += f"   科目：{', '.join(paper['subjects_covered'])}\n"
            if "sample_questions" in paper and paper["sample_questions"]:
                summary += f"   示例题目：{len(paper['sample_questions'])}道\n"
            summary += "\n"
        
        # 添加统计信息
        if "exam_statistics" in self.past_papers:
            stats = self.past_papers["exam_statistics"]
            summary += "📊 真题统计：\n"
            years = stats.get('years_covered', [])
            summary += f"   覆盖年份：{', '.join(map(str, years))}\n"
            summary += f"   总套数：{stats.get('total_papers', 0)}套\n"
            summary += f"   总题量：{stats.get('total_questions', 0)}题\n"
        
        return summary
    
    def get_sample_questions(self, year: int = None, limit: int = 3) -> List[Dict]:
        """获取示例题目"""
        if "past_papers" not in self.past_papers:
            return []
        
        papers = self.past_papers["past_papers"]
        questions = []
        
        for paper in papers:
            if year is None or paper["year"] == year:
                if "sample_questions" in paper:
                    questions.extend(paper["sample_questions"])
        
        return questions[:limit]
    
    def search_questions_by_topic(self, topic: str, limit: int = 5) -> List[Dict]:
        """按主题搜索题目"""
        results = []
        
        # 这里可以扩展为全文搜索
        # 目前简单匹配关键词
        if "past_papers" in self.past_papers:
            for paper in self.past_papers["past_papers"]:
                if "sample_questions" in paper:
                    for question in paper["sample_questions"]:
                        if (topic in question.get("question", "") or 
                            topic in question.get("point", "")):
                            results.append(question)
        
        return results[:limit]
    
    # ==================== 用户选择流程 ====================
    
    def get_exam_levels_menu(self) -> str:
        """获取考试级别选择菜单"""
        menu = "🎓 请选择考试级别：\n\n"
        menu += "1️⃣ **基本级（初级）**\n"
        menu += "   适合：入警不满3年或拟任初级执法资格的人民警察\n"
        menu += "   要求：掌握基础法律知识和基本执法技能\n\n"
        
        menu += "2️⃣ **高级（中级/高级）**\n"
        menu += "   适合：担任执法办案岗位3年以上或拟任中高级执法资格的人民警察\n"
        menu += "   要求：熟练掌握法律法规，具备独立办案和复杂案件处理能力\n\n"
        
        menu += "请回复 1 或 2 选择考试级别："
        return menu
    
    def set_exam_level(self, level_choice: str) -> tuple:
        """设置考试级别"""
        if level_choice == '1':
            self.user_session['exam_level'] = 'basic'
            level_name = '基本级（初级）'
        elif level_choice == '2':
            self.user_session['exam_level'] = 'advanced'
            level_name = '高级（中级/高级）'
        else:
            return False, "无效的选择，请回复 1 或 2"
        
        return True, f"✅ 已选择：{level_name}"
    
    def get_learning_modes_menu(self) -> str:
        """获取学习模式选择菜单"""
        if not self.user_session.get('exam_level'):
            return "请先选择考试级别！"
        
        menu = f"📚 {self.get_level_display_name()} - 请选择学习模式：\n\n"
        menu += "1️⃣ **模块练习**\n"
        menu += "   按科目章节进行专项练习，巩固知识点\n"
        menu += "   📋 包含：选择题、判断题、案例分析\n\n"
        
        menu += "2️⃣ **模拟测试**\n"
        menu += "   全真模拟考试环境，检验学习成果\n"
        menu += f"   ⏰ 时长：{self.get_exam_duration()}分钟，{self.get_question_count()}题\n\n"
        
        menu += "3️⃣ **历年真题**\n"
        menu += f"   查看{self.get_past_paper_years()}年历年真题\n"
        menu += "   📊 包含：答案解析、高频考点、错题分析\n\n"
        
        menu += "请回复 1、2 或 3 选择学习模式："
        return menu
    
    def set_learning_mode(self, mode_choice: str) -> tuple:
        """设置学习模式"""
        if mode_choice == '1':
            self.user_session['mode'] = 'practice'
            mode_name = '模块练习'
        elif mode_choice == '2':
            self.user_session['mode'] = 'simulation'
            mode_name = '模拟测试'
        elif mode_choice == '3':
            self.user_session['mode'] = 'past_papers'
            mode_name = '历年真题'
        else:
            return False, "无效的选择，请回复 1、2 或 3"
        
        return True, f"✅ 已选择：{mode_name}"
    
    def get_subject_selection_menu(self) -> str:
        """获取科目选择菜单"""
        mode = self.user_session.get('mode')
        if not mode:
            return "请先选择学习模式！"
        
        menu = f"📚 {self.get_level_display_name()} - {self.get_mode_display_name()} - 请选择学习科目：\n\n"
        
        # 根据考试级别显示不同的科目
        if self.user_session['exam_level'] == 'basic':
            subjects = self.get_basic_subjects()
        else:
            subjects = self.get_advanced_subjects()
        
        for i, subject in enumerate(subjects, 1):
            subject_name = subject['name']
            subject_weight = subject.get('weight', 0) * 100
            question_count = subject.get('question_count', 0)
            
            menu += f"{i}️⃣ **{subject_name}** ({subject_weight:.0f}%)\n"
            menu += f"   知识点：{subject.get('description', '')}\n"
            if mode == 'practice' and question_count > 0:
                menu += f"   练习题：{question_count}题\n"
            menu += "\n"
        
        menu += "请回复数字选择科目，或回复 0 返回上一级："
        return menu
    
    def set_subject(self, subject_choice: str) -> tuple:
        """设置学习科目"""
        if subject_choice == '0':
            self.user_session['mode'] = None
            return True, "返回学习模式选择"
        
        # 根据考试级别获取科目列表
        if self.user_session['exam_level'] == 'basic':
            subjects = self.get_basic_subjects()
        else:
            subjects = self.get_advanced_subjects()
        
        try:
            choice_idx = int(subject_choice) - 1
            if 0 <= choice_idx < len(subjects):
                self.user_session['subject'] = subjects[choice_idx]['id']
                subject_name = subjects[choice_idx]['name']
                return True, f"✅ 已选择：{subject_name}"
            else:
                return False, f"无效的选择，请输入 0-{len(subjects)} 之间的数字"
        except ValueError:
            return False, "请输入有效的数字"
    
    def get_current_session_info(self) -> str:
        """获取当前会话信息"""
        info = "📋 当前设置：\n\n"
        
        if self.user_session.get('exam_level'):
            info += f"• 考试级别：{self.get_level_display_name()}\n"
        
        if self.user_session.get('mode'):
            info += f"• 学习模式：{self.get_mode_display_name()}\n"
        
        if self.user_session.get('subject'):
            subject_name = self.get_subject_name(self.user_session['subject'])
            info += f"• 当前科目：{subject_name}\n"
        
        return info
    
    # ==================== 辅助方法 ====================
    
    def get_level_display_name(self) -> str:
        """获取考试级别显示名称"""
        if self.user_session.get('exam_level') == 'basic':
            return '基本级（初级）'
        elif self.user_session.get('exam_level') == 'advanced':
            return '高级（中级/高级）'
        return '未选择'
    
    def get_mode_display_name(self) -> str:
        """获取学习模式显示名称"""
        modes = {
            'practice': '模块练习',
            'simulation': '模拟测试',
            'past_papers': '历年真题'
        }
        return modes.get(self.user_session.get('mode'), '未选择')
    
    def get_basic_subjects(self) -> list:
        """获取基本级科目列表"""
        return [
            {
                'id': 'basic_s01',
                'name': '公安基础理论',
                'weight': 0.25,
                'description': '公安机关性质、任务、职责，公安工作方针原则',
                'question_count': 50
            },
            {
                'id': 'basic_s02',
                'name': '法律基础知识',
                'weight': 0.50,
                'description': '宪法、行政法、刑法、刑事诉讼法基础知识',
                'question_count': 100
            },
            {
                'id': 'basic_s03',
                'name': '警察法律法规',
                'weight': 0.15,
                'description': '人民警察法、执法规范化相关规定',
                'question_count': 30
            },
            {
                'id': 'basic_s04',
                'name': '警务实战技能',
                'weight': 0.10,
                'description': '警务指挥、现场处置、安全防护技能',
                'question_count': 20
            }
        ]
    
    def get_advanced_subjects(self) -> list:
        """获取高级科目列表"""
        return [
            {
                'id': 'advanced_s01',
                'name': '高级法律理论',
                'weight': 0.35,
                'description': '法律适用、法律解释、法律推理',
                'question_count': 70
            },
            {
                'id': 'advanced_s02',
                'name': '疑难案件办理',
                'weight': 0.30,
                'description': '复杂案件定性、证据审查、法律适用',
                'question_count': 60
            },
            {
                'id': 'advanced_s03',
                'name': '执法监督与责任',
                'weight': 0.20,
                'description': '执法监督、错案追究、国家赔偿',
                'question_count': 40
            },
            {
                'id': 'advanced_s04',
                'name': '警务领导与管理',
                'weight': 0.15,
                'description': '警务指挥、团队管理、应急处突',
                'question_count': 30
            }
        ]
    
    def get_exam_duration(self) -> int:
        """获取考试时长（分钟）"""
        return 120
    
    def get_question_count(self) -> int:
        """获取题目数量"""
        return 100
    
    def get_past_paper_years(self) -> str:
        """获取历年真题年份"""
        if "exam_statistics" in self.past_papers:
            years = self.past_papers["exam_statistics"]["years_covered"]
            return "、".join(map(str, sorted(years)))
        return "2021-2025"
    
    def get_subject_name(self, subject_id: str) -> str:
        """根据科目ID获取科目名称"""
        # 基本级科目
        basic_subjects = {s['id']: s['name'] for s in self.get_basic_subjects()}
        if subject_id in basic_subjects:
            return basic_subjects[subject_id]
        
        # 高级科目
        advanced_subjects = {s['id']: s['name'] for s in self.get_advanced_subjects()}
        if subject_id in advanced_subjects:
            return advanced_subjects[subject_id]
        
        return "未知科目"


def main():
    """主函数，测试新的用户选择流程"""
    bot = PQEBotCore()
    bot.reset_session()
    
    print("=== 警察执法资格考试助手 ===\n")
    print("🎯 欢迎使用警察执法资格考试助手！")
    print("本助手基于《公安机关人民警察执法资格等级考试大纲》（2026年版）附历年真题\n")
    
    # 演示完整的用户选择流程
    print("=" * 50)
    print("🚀 演示用户选择流程：\n")
    
    # 步骤1：选择考试级别
    print(bot.get_exam_levels_menu())
    print("➡️ 模拟用户选择：1（基本级）")
    success, message = bot.set_exam_level('1')
    print(f"{message}\n")
    
    # 步骤2：选择学习模式
    print(bot.get_learning_modes_menu())
    print("➡️ 模拟用户选择：3（历年真题）")
    success, message = bot.set_learning_mode('3')
    print(f"{message}\n")
    
    # 步骤3：显示当前会话信息
    print("📊 用户选择完成，当前设置：")
    print(bot.get_current_session_info())
    
    # 显示历年真题
    print("=" * 50)
    print("📚 历年真题库（根据用户选择）：")
    print(bot.get_past_papers_summary())
    
    # 显示高频考点
    print("🔝 高频考点（基于5年真题）：")
    points = bot.get_high_frequency_points(5)
    for i, point in enumerate(points, 1):
        freq_percent = point['frequency'] * 100
        years = point.get('appears_in_years', [])
        years_str = f"（{', '.join(map(str, years))}年）" if years else ""
        print(f"{i}. {point['topic']} {years_str} - 出现频率：{freq_percent:.0f}%")
    
    # 演示其他选择路径
    print("\n" + "=" * 50)
    print("🔄 演示另一个选择路径：\n")
    
    bot.reset_session()
    
    # 选择高级考试
    print("➡️ 模拟用户选择考试级别：2（高级）")
    bot.set_exam_level('2')
    
    # 选择模块练习
    print("➡️ 模拟用户选择学习模式：1（模块练习）")
    bot.set_learning_mode('1')
    
    # 选择科目
    print(bot.get_subject_selection_menu())
    print("➡️ 模拟用户选择：2（疑难案件办理）")
    success, message = bot.set_subject('2')
    print(f"{message}\n")
    
    # 显示最终设置
    print("✅ 最终设置：")
    print(bot.get_current_session_info())
    print(f"📝 即将开始：{bot.get_subject_name(bot.user_session['subject'])}的模块练习")


if __name__ == "__main__":
    main()
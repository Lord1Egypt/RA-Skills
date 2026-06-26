#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
个人AI能力测评工具 - 核心逻辑
"""

import json
import os
import math
from datetime import datetime
from typing import Dict, List, Any, Tuple

class PersonalAIAssessment:
    """个人AI能力测评工具"""
    
    def __init__(self):
        """初始化"""
        self.workspace = os.path.expanduser('~/.openclaw/workspace')
        self.output_dir = os.path.join(self.workspace, 'ai_assessment_reports')
        os.makedirs(self.output_dir, exist_ok=True)
        
        # 能力等级划分
        self.levels = {
            'master': {'name': '大师级', 'range': (450, 500), 'icon': '🏆'},
            'professional': {'name': '专业级', 'range': (350, 449), 'icon': '⭐'},
            'intermediate': {'name': '进阶级', 'range': (250, 349), 'icon': '📈'},
            'beginner': {'name': '入门级', 'range': (150, 249), 'icon': '🌱'},
            'novice': {'name': '小白级', 'range': (0, 149), 'icon': '📖'},
        }
        
        # 5大能力维度
        self.dimensions = {
            'knowledge': 'AI知识储备',
            'tools': 'AI工具使用',
            'practice': 'AI实战应用',
            'innovation': 'AI创新思维',
            'ethics': 'AI伦理意识',
        }
    
    def assess_knowledge(self, answers: Dict[str, Any]) -> Tuple[int, Dict]:
        """
        评估AI知识储备
        
        Args:
            answers: 答案字典
            
        Returns:
            (分数, 详细分析)
        """
        score = 0
        analysis = {
            'strengths': [],
            'weaknesses': [],
            'details': {}
        }
        
        # 基础概念（30分）
        if answers.get('basic_concepts', False):
            score += 30
            analysis['strengths'].append('AI基础概念清晰')
        else:
            analysis['weaknesses'].append('AI基础概念需加强')
        analysis['details']['基础概念'] = answers.get('basic_concepts', False)
        
        # 发展历史（20分）
        if answers.get('history', False):
            score += 20
            analysis['strengths'].append('了解AI发展历程')
        else:
            analysis['weaknesses'].append('AI发展历史了解不足')
        analysis['details']['发展历史'] = answers.get('history', False)
        
        # 技术原理（30分）
        if answers.get('tech_principles', False):
            score += 30
            analysis['strengths'].append('理解AI技术原理')
        else:
            analysis['weaknesses'].append('AI技术原理理解不深')
        analysis['details']['技术原理'] = answers.get('tech_principles', False)
        
        # 应用领域（20分）
        if answers.get('applications', False):
            score += 20
            analysis['strengths'].append('熟悉AI应用领域')
        else:
            analysis['weaknesses'].append('AI应用领域认知有限')
        analysis['details']['应用领域'] = answers.get('applications', False)
        
        return score, analysis
    
    def assess_tools(self, answers: Dict[str, Any]) -> Tuple[int, Dict]:
        """
        评估AI工具使用能力
        
        Args:
            answers: 答案字典
            
        Returns:
            (分数, 详细分析)
        """
        score = 0
        analysis = {
            'strengths': [],
            'weaknesses': [],
            'details': {}
        }
        
        # 对话AI（25分）
        if answers.get('chatgpt_usage', 'never') == 'frequent':
            score += 25
            analysis['strengths'].append('熟练使用对话AI')
        elif answers.get('chatgpt_usage', 'never') == 'sometimes':
            score += 15
            analysis['details']['对话AI'] = '偶尔使用'
        else:
            analysis['weaknesses'].append('对话AI使用经验不足')
        
        # 图片AI（25分）
        if answers.get('image_ai_usage', 'never') == 'frequent':
            score += 25
            analysis['strengths'].append('熟练使用图片AI')
        elif answers.get('image_ai_usage', 'never') == 'sometimes':
            score += 15
            analysis['details']['图片AI'] = '偶尔使用'
        else:
            analysis['weaknesses'].append('图片AI使用经验不足')
        
        # 写作AI（25分）
        if answers.get('writing_ai_usage', 'never') == 'frequent':
            score += 25
            analysis['strengths'].append('熟练使用写作AI')
        elif answers.get('writing_ai_usage', 'never') == 'sometimes':
            score += 15
            analysis['details']['写作AI'] = '偶尔使用'
        else:
            analysis['weaknesses'].append('写作AI使用经验不足')
        
        # 办公AI（25分）
        if answers.get('office_ai_usage', 'never') == 'frequent':
            score += 25
            analysis['strengths'].append('熟练使用办公AI')
        elif answers.get('office_ai_usage', 'never') == 'sometimes':
            score += 15
            analysis['details']['办公AI'] = '偶尔使用'
        else:
            analysis['weaknesses'].append('办公AI使用经验不足')
        
        return score, analysis
    
    def assess_practice(self, answers: Dict[str, Any]) -> Tuple[int, Dict]:
        """
        评估AI实战应用能力
        
        Args:
            answers: 答案字典
            
        Returns:
            (分数, 详细分析)
        """
        score = 0
        analysis = {
            'strengths': [],
            'weaknesses': [],
            'details': {}
        }
        
        # 提示词能力（30分）
        prompt_level = answers.get('prompt_level', 'beginner')
        if prompt_level == 'expert':
            score += 30
            analysis['strengths'].append('提示词编写能力强')
        elif prompt_level == 'intermediate':
            score += 20
            analysis['details']['提示词能力'] = '中等水平'
        else:
            analysis['weaknesses'].append('提示词编写能力需提升')
        
        # 工作流搭建（30分）
        if answers.get('workflow_building', False):
            score += 30
            analysis['strengths'].append('能搭建AI工作流')
        else:
            analysis['weaknesses'].append('AI工作流搭建能力不足')
        
        # 问题解决（20分）
        if answers.get('problem_solving', False):
            score += 20
            analysis['strengths'].append('能用AI解决实际问题')
        else:
            analysis['weaknesses'].append('AI实际问题解决能力不足')
        
        # 效率提升（20分）
        if answers.get('efficiency_improvement', False):
            score += 20
            analysis['strengths'].append('能通过AI提升效率')
        else:
            analysis['weaknesses'].append('AI效率提升能力不足')
        
        return score, analysis
    
    def assess_innovation(self, answers: Dict[str, Any]) -> Tuple[int, Dict]:
        """
        评估AI创新思维能力
        
        Args:
            answers: 答案字典
            
        Returns:
            (分数, 详细分析)
        """
        score = 0
        analysis = {
            'strengths': [],
            'weaknesses': [],
            'details': {}
        }
        
        # AI+行业创新（30分）
        if answers.get('industry_innovation', False):
            score += 30
            analysis['strengths'].append('有AI+行业创新思路')
        else:
            analysis['weaknesses'].append('AI+行业创新思维不足')
        
        # AI+业务创新（30分）
        if answers.get('business_innovation', False):
            score += 30
            analysis['strengths'].append('有AI+业务创新思路')
        else:
            analysis['weaknesses'].append('AI+业务创新思维不足')
        
        # 商业模式（20分）
        if answers.get('business_model', False):
            score += 20
            analysis['strengths'].append('理解AI商业模式')
        else:
            analysis['weaknesses'].append('AI商业模式理解不足')
        
        # 未来发展（20分）
        if answers.get('future_trends', False):
            score += 20
            analysis['strengths'].append('关注AI未来发展趋势')
        else:
            analysis['weaknesses'].append('对AI未来发展趋势关注不足')
        
        return score, analysis
    
    def assess_ethics(self, answers: Dict[str, Any]) -> Tuple[int, Dict]:
        """
        评估AI伦理意识
        
        Args:
            answers: 答案字典
            
        Returns:
            (分数, 详细分析)
        """
        score = 0
        analysis = {
            'strengths': [],
            'weaknesses': [],
            'details': {}
        }
        
        # 数据安全（30分）
        if answers.get('data_security', False):
            score += 30
            analysis['strengths'].append('重视AI数据安全')
        else:
            analysis['weaknesses'].append('AI数据安全意识不足')
        
        # AI偏见（25分）
        if answers.get('ai_bias', False):
            score += 25
            analysis['strengths'].append('了解AI偏见问题')
        else:
            analysis['weaknesses'].append('对AI偏见问题认识不足')
        
        # AI风险（25分）
        if answers.get('ai_risks', False):
            score += 25
            analysis['strengths'].append('了解AI风险')
        else:
            analysis['weaknesses'].append('AI风险意识不足')
        
        # AI合规（20分）
        if answers.get('ai_compliance', False):
            score += 20
            analysis['strengths'].append('了解AI合规要求')
        else:
            analysis['weaknesses'].append('AI合规知识不足')
        
        return score, analysis
    
    def calculate_level(self, total_score: int) -> Dict:
        """
        计算能力等级
        
        Args:
            total_score: 总分
            
        Returns:
            等级信息
        """
        for level_key, level_info in self.levels.items():
            min_score, max_score = level_info['range']
            if min_score <= total_score <= max_score:
                return {
                    'level': level_key,
                    'name': level_info['name'],
                    'icon': level_info['icon'],
                    'range': level_info['range'],
                }
        
        return {
            'level': 'novice',
            'name': '小白级',
            'icon': '📖',
            'range': (0, 149),
        }
    
    def generate_learning_path(self, 
                              scores: Dict[str, int],
                              level: Dict) -> List[Dict]:
        """
        生成学习路径
        
        Args:
            scores: 各维度分数
            level: 等级信息
            
        Returns:
            学习路径列表
        """
        learning_path = []
        
        # 找出最弱的维度
        sorted_dimensions = sorted(scores.items(), key=lambda x: x[1])
        
        for dimension, score in sorted_dimensions[:3]:
            if score < 60:
                priority = '高'
            elif score < 80:
                priority = '中'
            else:
                priority = '低'
            
            dimension_name = self.dimensions.get(dimension, dimension)
            
            # 根据维度提供具体建议
            suggestions = self._get_learning_suggestions(dimension, score)
            
            learning_path.append({
                'dimension': dimension_name,
                'score': score,
                'priority': priority,
                'suggestions': suggestions,
            })
        
        return learning_path
    
    def _get_learning_suggestions(self, dimension: str, score: int) -> List[str]:
        """
        获取学习建议
        
        Args:
            dimension: 维度
            score: 分数
            
        Returns:
            建议列表
        """
        suggestions = {
            'knowledge': [
                '阅读《人工智能简史》',
                '学习机器学习基础概念',
                '了解深度学习原理',
                '关注AI行业动态',
            ],
            'tools': [
                '注册并使用ChatGPT',
                '尝试Midjourney图片生成',
                '使用Notion AI写作',
                '探索GitHub Copilot',
            ],
            'practice': [
                '学习提示词工程',
                '搭建个人AI工作流',
                '参与AI实战项目',
                '加入AI学习社群',
            ],
            'innovation': [
                '研究AI+行业案例',
                '思考AI商业应用',
                '参加AI创新比赛',
                '阅读AI商业模式书籍',
            ],
            'ethics': [
                '学习AI伦理准则',
                '了解AI法律法规',
                '关注AI安全话题',
                '参与AI伦理讨论',
            ],
        }
        
        return suggestions.get(dimension, [])
    
    def generate_report(self,
                       name: str,
                       scores: Dict[str, int],
                       analyses: Dict[str, Dict],
                       level: Dict,
                       learning_path: List[Dict]) -> str:
        """
        生成测评报告
        
        Args:
            name: 姓名
            scores: 各维度分数
            analyses: 各维度分析
            level: 等级信息
            learning_path: 学习路径
            
        Returns:
            Markdown格式的报告
        """
        total_score = sum(scores.values())
        
        report = f"""# 个人AI能力测评报告

**姓名**：{name}
**测评时间**：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

---

## 🏆 能力等级

**{level['icon']} {level['name']}**

- 总分：{total_score}/500
- 等级范围：{level['range'][0]}-{level['range'][1]}分

---

## 📊 能力雷达图（5大维度）

"""
        
        # 添加各维度分数
        for dimension, score in scores.items():
            dimension_name = self.dimensions.get(dimension, dimension)
            stars = '⭐' * (score // 20)
            report += f"**{dimension_name}**：{score}/100 {stars}\n\n"
        
        report += """---

## 💪 优势能力

"""
        
        # 找出优势（分数>=80的维度）
        for dimension, score in scores.items():
            if score >= 80:
                dimension_name = self.dimensions.get(dimension, dimension)
                analysis = analyses.get(dimension, {})
                strengths = analysis.get('strengths', [])
                report += f"### {dimension_name}（{score}分）\n\n"
                for strength in strengths:
                    report += f"- ✅ {strength}\n"
                report += "\n"
        
        report += """---

## ⚠️ 待提升能力

"""
        
        # 找出弱势（分数<80的维度）
        for dimension, score in scores.items():
            if score < 80:
                dimension_name = self.dimensions.get(dimension, dimension)
                analysis = analyses.get(dimension, {})
                weaknesses = analysis.get('weaknesses', [])
                report += f"### {dimension_name}（{score}分）\n\n"
                for weakness in weaknesses:
                    report += f"- ❌ {weakness}\n"
                report += "\n"
        
        report += """---

## 📚 学习路径建议

"""
        
        # 添加学习路径
        for i, path in enumerate(learning_path, 1):
            priority_icon = '🔥' if path['priority'] == '高' else ('⚡' if path['priority'] == '中' else '💡')
            report += f"### {i}. {path['dimension']}（优先级：{priority_icon} {path['priority']}）\n\n"
            report += f"**当前分数**：{path['score']}/100\n\n"
            report += "**学习建议**：\n\n"
            for suggestion in path['suggestions']:
                report += f"- {suggestion}\n"
            report += "\n"
        
        report += f"""---

## 🎯 总结

**你的AI能力等级**：{level['icon']} {level['name']}

**总分**：{total_score}/500

**核心优势**：
{self._get_top_strengths(scores)}

**重点提升**：
{self._get_top_weaknesses(scores)}

**下一步行动**：
1. 优先提升{learning_path[0]['dimension'] if learning_path else '基础能力'}
2. 参加AI培训课程
3. 加入AI学习社群
4. 持续实践和应用

---

## 📞 后续支持

如需进一步咨询或定制学习计划，请联系：
- 邮箱：87287416@qq.com
- 飞书：@胡大大

---

**报告生成**：个人AI能力测评工具 v1.0
**小龙虾协助制作** 🦞
"""
        
        return report
    
    def _get_top_strengths(self, scores: Dict[str, int]) -> str:
        """获取最强的能力"""
        sorted_scores = sorted(scores.items(), key=lambda x: x[1], reverse=True)
        top_2 = sorted_scores[:2]
        strengths = []
        for dimension, score in top_2:
            dimension_name = self.dimensions.get(dimension, dimension)
            strengths.append(f"- {dimension_name}（{score}分）")
        return '\n'.join(strengths)
    
    def _get_top_weaknesses(self, scores: Dict[str, int]) -> str:
        """获取最弱的能力"""
        sorted_scores = sorted(scores.items(), key=lambda x: x[1])
        bottom_2 = sorted_scores[:2]
        weaknesses = []
        for dimension, score in bottom_2:
            dimension_name = self.dimensions.get(dimension, dimension)
            weaknesses.append(f"- {dimension_name}（{score}分）")
        return '\n'.join(weaknesses)
    
    def generate_html_report(self,
                            name: str,
                            scores: Dict[str, int],
                            analyses: Dict[str, Dict],
                            level: Dict,
                            learning_path: List[Dict]) -> str:
        """
        生成HTML格式的报告
        
        Args:
            name: 姓名
            scores: 各维度分数
            analyses: 各维度分析
            level: 等级信息
            learning_path: 学习路径
            
        Returns:
            HTML格式的报告
        """
        total_score = sum(scores.values())
        
        # 生成雷达图SVG
        radar_svg = self._generate_radar_chart_svg(scores)
        
        html = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>个人AI能力测评报告 - {name}</title>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: #333;
            line-height: 1.6;
            padding: 20px;
        }}
        .container {{
            max-width: 900px;
            margin: 0 auto;
            background: white;
            border-radius: 20px;
            box-shadow: 0 20px 60px rgba(0,0,0,0.3);
            overflow: hidden;
        }}
        .header {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 40px;
            text-align: center;
        }}
        .header h1 {{
            font-size: 2.5em;
            margin-bottom: 10px;
        }}
        .level-badge {{
            text-align: center;
            padding: 30px;
            background: linear-gradient(135deg, #ffeaa7 0%, #fdcb6e 100%);
            margin: 20px 0;
            border-radius: 15px;
        }}
        .level-badge .level {{
            font-size: 3em;
            margin-bottom: 10px;
        }}
        .level-badge .title {{
            font-size: 2em;
            font-weight: bold;
            color: #2d3436;
        }}
        .content {{
            padding: 40px;
        }}
        .dimension {{
            margin: 30px 0;
            padding: 25px;
            background: #f8f9fa;
            border-radius: 15px;
            border-left: 5px solid #667eea;
        }}
        .progress-bar {{
            background: #e9ecef;
            border-radius: 10px;
            height: 30px;
            overflow: hidden;
            margin: 15px 0;
        }}
        .progress-fill {{
            height: 100%;
            background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
            transition: width 1s ease-out;
            display: flex;
            align-items: center;
            justify-content: flex-end;
            padding-right: 10px;
            color: white;
            font-weight: bold;
        }}
        .skills-list {{
            list-style: none;
            margin-top: 15px;
        }}
        .skills-list li {{
            padding: 8px 0;
            font-size: 1.1em;
        }}
        .skills-list li:before {{
            content: "✅ ";
            margin-right: 10px;
        }}
        .skills-list li.weak:before {{
            content: "❌ ";
        }}
        .footer {{
            background: #2d3436;
            color: white;
            padding: 30px;
            text-align: center;
            margin-top: 40px;
        }}
        @media (max-width: 768px) {{
            .header h1 {{
                font-size: 1.8em;
            }}
            .content {{
                padding: 20px;
            }}
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🦞 个人AI能力测评报告</h1>
            <div class="subtitle">
                <div>测评对象：{name}</div>
                <div>测评时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</div>
            </div>
        </div>
        
        <div class="content">
            <div class="level-badge">
                <div class="level">{level['icon']}</div>
                <div class="title">{level['name']}</div>
                <div class="score">总分：{total_score}/500</div>
            </div>
            
            <h2 style="text-align: center; margin: 40px 0; color: #2d3436;">📊 能力雷达图</h2>
            
            <div style="text-align: center; margin: 40px 0;">
                {radar_svg}
            </div>
"""
        
        # 添加各维度
        for dimension, score in scores.items():
            dimension_name = self.dimensions.get(dimension, dimension)
            analysis = analyses.get(dimension, {})
            
            html += f"""
            <div class="dimension">
                <h3>{self._get_dimension_icon(dimension)} {dimension_name} - {score}/100</h3>
                <div class="progress-bar">
                    <div class="progress-fill" style="width: {score}%;">{score}%</div>
                </div>
                <ul class="skills-list">
"""
            
            # 添加优势
            for strength in analysis.get('strengths', []):
                html += f"                    <li>{strength}</li>\n"
            
            # 添加弱势
            for weakness in analysis.get('weaknesses', []):
                html += f"                    <li class=\"weak\">{weakness}</li>\n"
            
            html += """                </ul>
            </div>
"""
        
        # 添加学习路径
        html += """
            <div style="background: linear-gradient(135deg, #74b9ff 0%, #0984e3 100%); color: white; padding: 30px; border-radius: 15px; margin: 30px 0;">
                <h3 style="font-size: 1.8em; margin-bottom: 20px;">📚 学习路径建议</h3>
"""
        
        for i, path in enumerate(learning_path, 1):
            priority_icon = '🔥' if path['priority'] == '高' else ('⚡' if path['priority'] == '中' else '💡')
            html += f"""
                <div style="background: rgba(255,255,255,0.2); padding: 20px; border-radius: 10px; margin: 15px 0;">
                    <h4>{priority_icon} {i}. {path['dimension']}（优先级：{path['priority']}）</h4>
                    <p style="margin-top: 10px;">当前分数：{path['score']}/100</p>
                    <ul style="margin-top: 10px; margin-left: 20px;">
"""
            for suggestion in path['suggestions']:
                html += f"                        <li>{suggestion}</li>\n"
            html += """                    </ul>
                </div>
"""
        
        html += f"""
            </div>
            
            <div style="background: linear-gradient(135deg, #a29bfe 0%, #6c5ce7 100%); color: white; padding: 40px; border-radius: 15px; margin: 30px 0; text-align: center;">
                <h3 style="font-size: 2em; margin-bottom: 20px;">🎯 总结</h3>
                <div style="font-size: 1.3em;">
                    <p><strong>你的AI能力等级：{level['icon']} {level['name']}</strong></p>
                    <p style="font-size: 2em; margin: 20px 0;">总分：{total_score}/500</p>
                </div>
            </div>
        </div>
        
        <div class="footer">
            <h3>📞 后续支持</h3>
            <p style="margin-top: 15px;">如需进一步咨询或定制学习计划，请联系：</p>
            <p style="margin-top: 10px;">📧 邮箱：87287416@qq.com</p>
            <p style="margin-top: 30px; opacity: 0.7;">
                报告生成：个人AI能力测评工具 v1.0<br>
                小龙虾协助制作 🦞
            </p>
        </div>
    </div>
    
    <script>
        document.addEventListener('DOMContentLoaded', function() {{
            const progressBars = document.querySelectorAll('.progress-fill');
            progressBars.forEach(bar => {{
                const width = bar.style.width;
                bar.style.width = '0%';
                setTimeout(() => {{
                    bar.style.width = width;
                }}, 100);
            }});
        }});
    </script>
</body>
</html>
"""
        
        return html
    
    def _generate_radar_chart_svg(self, scores: Dict[str, int]) -> str:
        """
        生成雷达图SVG
        
        Args:
            scores: 各维度分数
            
        Returns:
            SVG字符串
        """
        # 计算雷达图坐标点
        dimensions = list(scores.keys())
        num_dimensions = len(dimensions)
        center_x, center_y = 250, 250
        max_radius = 200
        
        # 生成背景网格
        grid_svg = ""
        for i in range(1, 5):
            radius = max_radius * i / 4
            points = []
            for j in range(num_dimensions):
                angle = 2 * 3.14159 * j / num_dimensions - 3.14159 / 2
                x = center_x + radius * math.cos(angle)
                y = center_y + radius * math.sin(angle)
                points.append(f"{x},{y}")
            grid_svg += f'<polygon points="{" ".join(points)}" fill="none" stroke="#e9ecef" stroke-width="2"/>\n'
        
        # 生成数据区域
        data_points = []
        for i, dimension in enumerate(dimensions):
            score = scores[dimension]
            radius = max_radius * score / 100
            angle = 2 * 3.14159 * i / num_dimensions - 3.14159 / 2
            x = center_x + radius * math.cos(angle)
            y = center_y + radius * math.sin(angle)
            data_points.append(f"{x},{y}")
        
        data_svg = f'<polygon points="{" ".join(data_points)}" fill="rgba(102, 126, 234, 0.3)" stroke="#667eea" stroke-width="3"/>\n'
        
        # 生成标签
        labels_svg = ""
        dimension_names = [self.dimensions.get(d, d) for d in dimensions]
        for i, (dimension, name) in enumerate(zip(dimensions, dimension_names)):
            score = scores[dimension]
            angle = 2 * 3.14159 * i / num_dimensions - 3.14159 / 2
            label_radius = max_radius + 30
            x = center_x + label_radius * math.cos(angle)
            y = center_y + label_radius * math.sin(angle)
            labels_svg += f'<text x="{x}" y="{y}" text-anchor="middle" font-size="16" font-weight="bold">{name} {score}</text>\n'
        
        return f"""<svg viewBox="0 0 500 500" xmlns="http://www.w3.org/2000/svg">
            {grid_svg}
            {data_svg}
            {labels_svg}
        </svg>"""
    
    def _get_dimension_icon(self, dimension: str) -> str:
        """
        获取维度图标
        
        Args:
            dimension: 维度名称
            
        Returns:
            图标
        """
        icons = {
            'knowledge': '🎓',
            'tools': '🛠️',
            'practice': '⚡',
            'innovation': '💡',
            'ethics': '⚖️',
        }
        return icons.get(dimension, '📊')
    
    def save_report(self, report: str, filename: str = None) -> str:
        """
        保存Markdown报告
        
        Args:
            report: 报告内容
            filename: 文件名（可选）
            
        Returns:
            文件路径
        """
        if filename is None:
            filename = f"ai_assessment_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md"
        
        filepath = os.path.join(self.output_dir, filename)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(report)
        
        return filepath
    
    def save_html_report(self, html: str, filename: str = None) -> str:
        """
        保存HTML报告
        
        Args:
            html: HTML内容
            filename: 文件名（可选）
            
        Returns:
            文件路径
        """
        if filename is None:
            filename = f"ai_assessment_{datetime.now().strftime('%Y%m%d_%H%M%S')}.html"
        
        filepath = os.path.join(self.output_dir, filename)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(html)
        
        return filepath


def main():
    """示例使用"""
    # 创建测评实例
    assessment = PersonalAIAssessment()
    
    # 示例：测评答案（模拟中等水平用户）
    answers = {
        # 知识储备
        'basic_concepts': True,
        'history': False,
        'tech_principles': True,
        'applications': True,
        
        # 工具使用
        'chatgpt_usage': 'sometimes',
        'image_ai_usage': 'never',
        'writing_ai_usage': 'sometimes',
        'office_ai_usage': 'never',
        
        # 实战应用
        'prompt_level': 'intermediate',
        'workflow_building': False,
        'problem_solving': True,
        'efficiency_improvement': True,
        
        # 创新思维
        'industry_innovation': False,
        'business_innovation': True,
        'business_model': False,
        'future_trends': True,
        
        # 伦理意识
        'data_security': True,
        'ai_bias': False,
        'ai_risks': True,
        'ai_compliance': False,
    }
    
    # 评估各维度
    knowledge_score, knowledge_analysis = assessment.assess_knowledge(answers)
    tools_score, tools_analysis = assessment.assess_tools(answers)
    practice_score, practice_analysis = assessment.assess_practice(answers)
    innovation_score, innovation_analysis = assessment.assess_innovation(answers)
    ethics_score, ethics_analysis = assessment.assess_ethics(answers)
    
    # 汇总分数
    scores = {
        'knowledge': knowledge_score,
        'tools': tools_score,
        'practice': practice_score,
        'innovation': innovation_score,
        'ethics': ethics_score,
    }
    
    # 汇总分析
    analyses = {
        'knowledge': knowledge_analysis,
        'tools': tools_analysis,
        'practice': practice_analysis,
        'innovation': innovation_analysis,
        'ethics': ethics_analysis,
    }
    
    # 计算等级
    total_score = sum(scores.values())
    level = assessment.calculate_level(total_score)
    
    # 生成学习路径
    learning_path = assessment.generate_learning_path(scores, level)
    
    # 生成Markdown报告
    md_report = assessment.generate_report(
        name='示例用户',
        scores=scores,
        analyses=analyses,
        level=level,
        learning_path=learning_path
    )
    
    # 生成HTML报告
    html_report = assessment.generate_html_report(
        name='示例用户',
        scores=scores,
        analyses=analyses,
        level=level,
        learning_path=learning_path
    )
    
    # 保存Markdown报告
    md_filepath = assessment.save_report(md_report)
    
    # 保存HTML报告
    html_filepath = assessment.save_html_report(html_report)
    
    print(f"✅ 测评报告已生成：")
    print(f"  📄 Markdown版本：{md_filepath}")
    print(f"  🌐 HTML版本：{html_filepath}")
    print(f"\n测评结果：")
    print(f"  - 总分：{total_score}/500")
    print(f"  - 等级：{level['icon']} {level['name']}")
    print(f"  - AI知识储备：{knowledge_score}/100")
    print(f"  - AI工具使用：{tools_score}/100")
    print(f"  - AI实战应用：{practice_score}/100")
    print(f"  - AI创新思维：{innovation_score}/100")
    print(f"  - AI伦理意识：{ethics_score}/100")


if __name__ == '__main__':
    main()

#!/usr/bin/env python3
"""
视频号脚本生成辅助工具
帮助快速生成符合老胡风格的口播脚本
"""

from typing import Optional, List
import json
from datetime import datetime


class ScriptGenerator:
    """视频号脚本生成器"""
    
    def __init__(self, name: str = "老胡"):
        self.name = name
        self.title = "技术成果转化咨询师"
        self.background = "央企投资公司前副总、产权交易机构前负责人，十余年实战经验"
    
    def generate_policy_script(
        self,
        policy_name: str,
        key_points: List[str],
        personal_view: str,
        practical_tips: List[str]
    ) -> str:
        """
        生成政策解读类脚本
        
        Args:
            policy_name: 政策名称
            key_points: 核心要点列表
            personal_view: 老胡观点
            practical_tips: 实操建议
        """
        script = f"""
【开场 Hook】
大家好，我是{self.name}。
最近{policy_name}出台，很多人都来问我怎么看。
今天我就用两分钟，把这个政策的核心给大家讲清楚。

【政策核心】
这个政策主要说了三件事：
"""
        for i, point in enumerate(key_points, 1):
            script += f"\n第一，{point}" if i == 1 else f"\n第二，{point}" if i == 2 else f"\n第三，{point}"
        
        script += f"""

【{self.name}观点】
我的看法是：{personal_view}

【实操建议】
如果你正在做技术转化业务，要注意这几点：
"""
        for i, tip in enumerate(practical_tips, 1):
            script += f"\n{i}、{tip}"
        
        script += f"""

【互动结尾】
这个政策你怎么看？评论区聊聊。
觉得有用，点个赞。
关注{self.name}，懂技术转化。
我是{self.name}，咱们下期见！
"""
        return script
    
    def generate_case_script(
        self,
        case_summary: str,
        case_background: str,
        solution_steps: List[str],
        key_experiences: List[str],
        warnings: List[str]
    ) -> str:
        """
        生成案例分享类脚本
        
        Args:
            case_summary: 案例一句话概括
            case_background: 案例背景
            solution_steps: 解决步骤
            key_experiences: 核心经验
            warnings: 注意事项/坑
        """
        script = f"""
【开场 Hook】
大家好，我是{self.name}。
今天分享一个我刚完成的案例，{case_summary}。
这个案例过程非常曲折，但结果不错，希望能给你一些启发。

【案例背景】
这家企业的情况是这样的：{case_background}

【解决过程】
我是怎么处理的？分三步：
"""
        for i, step in enumerate(solution_steps, 1):
            script += f"\n第一步，{step}" if i == 1 else f"\n第二步，{step}" if i == 2 else f"\n第三步，{step}"
        
        script += f"""

【核心经验】
总结下来，有三点最重要的经验：
"""
        for i, exp in enumerate(key_experiences, 1):
            script += f"\n{i}、{exp}"
        
        script += f"""

【踩坑提醒】
还有几个坑大家千万不要踩：
"""
        for i, warn in enumerate(warnings, 1):
            script += f"\n坑{i}：{warn}"
        
        script += f"""

【互动结尾】
你们有没有遇到过类似的情况？评论区说说。
关注{self.name}，学习更多实战经验。
我是{self.name}，咱们下期见！
"""
        return script
    
    def generate_industry_insight_script(
        self,
        event_name: str,
        impact_analysis: str,
        trend_prediction: str,
        suggestions: str
    ) -> str:
        """
        生成行业洞察类脚本
        
        Args:
            event_name: 事件名称
            impact_analysis: 影响分析
            trend_prediction: 趋势预判
            suggestions: 建议
        """
        script = f"""
【开场 Hook】
大家好，我是{self.name}。
{event_name}，这件事最近在圈子里讨论很多。
今天说说我的看法。

【影响分析】
首先，这件事为什么重要？
{impact_analysis}

【趋势预判】
接下来会怎么发展？
{trend_prediction}

【从业建议】
对于我们从业者，我的建议是：
{suggestions}

【互动结尾】
这个判断对不对，咱们拭目以待。
想持续关注，点个关注。
我是{self.name}，下期接着聊。
"""
        return script
    
    def generate_qa_script(
        self,
        question: str,
        answer: str,
        example: Optional[str] = None,
        action_suggestions: Optional[List[str]] = None
    ) -> str:
        """
        生成问答互动类脚本
        
        Args:
            question: 问题
            answer: 回答
            example: 举例
            action_suggestions: 行动建议
        """
        script = f"""
【开场 Hook】
大家好，我是{self.name}。
今天回答一个粉丝的问题。

【问题复述】
这位朋友问：{question}

【直接回答】
这个问题挺有代表性的。
我的看法是：{answer}
"""
        if example:
            script += f"\n\n举个例子：{example}"
        
        if action_suggestions:
            script += f"\n\n针对这个情况，我建议你可以这样做："
            for i, suggestion in enumerate(action_suggestions, 1):
                script += f"\n{i}、{suggestion}"
        
        script += f"""

【互动结尾】
还有问题的话，评论区继续问。
关注{self.name}，咱们下期见！
"""
        return script
    
    def generate_tutorial_script(
        self,
        skill_name: str,
        benefit: str,
        steps: List[str],
        common_mistakes: List[tuple],
        key_reminder: str
    ) -> str:
        """
        生成干货教程类脚本
        
        Args:
            skill_name: 技能名称
            benefit: 学会后的好处
            steps: 操作步骤
            common_mistakes: 常见错误 [(错误, 正确做法), ...]
            key_reminder: 重点提醒
        """
        script = f"""
【开场 Hook】
大家好，我是{self.name}。
今天教大家一个技能：{skill_name}
学会了之后，{benefit}。

【效果展示】
这个方法，我已经帮很多人用过了。
效果确实不错。

【具体步骤】
具体怎么操作？
"""
        for i, step in enumerate(steps, 1):
            script += f"\n第一步，{step}" if i == 1 else f"\n第二步，{step}" if i == 2 else f"\n第三步，{step}"
        
        script += f"""

【常见错误】
还有几个坑千万不要踩：
"""
        for mistake, correct in common_mistakes:
            script += f"\n错误：{mistake} → 正确：{correct}"
        
        script += f"""

【重点提醒】
最后一点最关键：{key_reminder}

【行动号召】
赶紧去试试，用完有问题评论区告诉我。
关注{self.name}，我是{self.name}，咱们下期见！
"""
        return script
    
    def save_script(self, script: str, filename: str) -> str:
        """保存脚本到文件"""
        filepath = f"scripts/{filename}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(script)
        return filepath


# 使用示例
if __name__ == "__main__":
    generator = ScriptGenerator()
    
    # 示例：生成政策解读脚本
    policy_script = generator.generate_policy_script(
        policy_name="《促进科技成果转化法》最新修订",
        key_points=[
            "科研人员可以享受更大比例的成果转化收益",
            "国有高校、科研机构的转化流程进一步简化",
            "明确了技术经纪人的法律地位和作用"
        ],
        personal_view="这是近年来力度最大的一次修订，体现了国家对技术转化的重视。对我们从业者来说是重大利好。",
        practical_tips=[
            "尽快熟悉新政策的具体条款",
            "与单位法务沟通新的操作流程",
            "关注后续配套细则的出台"
        ]
    )
    
    print(policy_script)

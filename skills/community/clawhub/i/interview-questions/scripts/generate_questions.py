#!/usr/bin/env python3
"""
面试题生成器
根据岗位生成专业面试题
"""

import re
from typing import Dict, List, Optional


class InterviewQuestionsGenerator:
    """面试题生成器类"""
    
    def __init__(self):
        self.question_templates = self._load_templates()
    
    def _load_templates(self) -> Dict:
        """加载面试题模板"""
        return {
            'general': {
                'opening': [
                    "请简单介绍一下你自己",
                    "您为什么对我们公司这个岗位感兴趣？",
                    "您目前的状态是？"
                ],
                'career': [
                    "您未来3-5年的职业规划是什么？",
                    "您上一份工作的主要职责是什么？",
                    "您为什么考虑离开现在的公司？"
                ],
                'strength_weakness': [
                    "您觉得自己最大的优势是什么？",
                    "您觉得自己需要改进的地方是什么？",
                    "您的同事通常如何评价您？"
                ]
            },
            'tech': {
                'basic': [
                    "请介绍一下您最擅长的技术栈",
                    "遇到技术难题通常如何解决？",
                    "如何保持技术学习？"
                ],
                'project': [
                    "请介绍一下您参与过最重要的项目",
                    "在项目中您承担什么角色？",
                    "项目遇到过最大的挑战是什么？"
                ],
                'system_design': [
                    "如果让您设计一个XX系统，您会怎么做？",
                    "如何保证系统的高可用性？",
                    "如何处理高并发场景？"
                ]
            },
            'product': {
                'product_sense': [
                    "您最喜欢的产品是什么？为什么？",
                    "如果让您优化这个产品，您会怎么做？",
                    "您认为什么是好的产品？"
                ],
                'requirement': [
                    "如何判断一个需求该不该做？",
                    "需求优先级如何确定？",
                    "和技术团队有分歧时怎么处理？"
                ],
                'data': [
                    "如何定义产品的核心指标？",
                    "数据下降如何分析原因？",
                    "如何验证需求的效果？"
                ]
            },
            'sales': {
                'ability': [
                    "您过往最成功的销售案例？",
                    "如何挖掘客户需求？",
                    "如何应对客户拒绝？"
                ],
                'relationship': [
                    "如何维护大客户关系？",
                    "客户投诉怎么处理？",
                    "如何进行客户分层管理？"
                ],
                'performance': [
                    "您是如何完成业绩目标的？",
                    "业绩不达标怎么办？",
                    "如何制定销售计划？"
                ]
            }
        }
    
    def generate_questions(self,
                          job_title: str,
                          job_requirements: str = "",
                          interview_round: str = "first",
                          interview_type: str = "general") -> str:
        """生成面试题"""
        
        # 确定面试类型
        interview_type = self._detect_type(job_title, job_requirements, interview_type)
        
        # 获取对应类型的题库
        templates = self.question_templates.get(interview_type, self.question_templates['general'])
        
        # 构建面试题
        output = f"# {job_title} - {self._get_round_name(interview_round)}面试题\n\n"
        output += f"**岗位**：[{job_title}]\n"
        output += f"**面试轮次**：[{self._get_round_name(interview_round)}]\n\n"
        output += "---\n\n"
        
        # 开场暖场
        output += "## 一、开场暖场\n"
        for i, q in enumerate(templates.get('opening', []), 1):
            output += f"{i}. {q}\n"
        output += "\n"
        
        # 核心问题
        output += "## 二、核心考察\n"
        if 'basic' in templates:
            output += "### 2.1 基础知识\n"
            for i, q in enumerate(templates['basic'], 1):
                output += f"{i}. {q}\n"
            output += "\n"
        
        if 'project' in templates:
            output += "### 2.2 项目经验\n"
            for i, q in enumerate(templates['project'], 1):
                output += f"{i}. {q}\n"
            output += "\n"
        
        if 'career' in templates:
            output += "### 2.3 职业发展\n"
            for i, q in enumerate(templates['career'], 1):
                output += f"{i}. {q}\n"
            output += "\n"
        
        # 追问和延伸
        output += "## 三、追问与延伸\n"
        output += "- 追问要点：STAR法则（情境、任务、行动、结果）\n"
        output += "- 延伸问题：根据候选人回答选择深入追问\n\n"
        
        # 候选人提问
        output += "## 四、候选人提问环节\n"
        output += "- 常见问题：职业发展、培训机会、团队氛围\n"
        output += "- 建议预留5-10分钟\n\n"
        
        # 评分标准
        output += "## 五、评分参考\n"
        output += "| 维度 | 权重 | 评分标准 |\n"
        output += "|------|------|----------|\n"
        output += "| 专业能力 | 40% | 与岗位要求的匹配度 |\n"
        output += "| 沟通表达 | 20% | 逻辑清晰、表达流畅 |\n"
        output += "| 逻辑思维 | 20% | 分析问题的条理性 |\n"
        output += "| 学习能力 | 10% | 持续学习的意识和方式 |\n"
        output += "| 价值观 | 10% | 与公司文化的契合度 |\n"
        
        return output
    
    def _detect_type(self, job_title: str, requirements: str, interview_type: str) -> str:
        """检测面试类型"""
        if interview_type != "general":
            return interview_type
        
        job_text = (job_title + requirements).lower()
        
        if any(k in job_text for k in ['开发', '工程', '技术', 'java', 'python', '前端', '后端']):
            return 'tech'
        elif any(k in job_text for k in ['产品', '经理', '策划']):
            return 'product'
        elif any(k in job_text for k in ['销售', '商务', '客户']):
            return 'sales'
        else:
            return 'general'
    
    def _get_round_name(self, round_code: str) -> str:
        """获取轮次名称"""
        round_map = {
            'first': '初试',
            'second': '复试',
            'final': '终面',
            'hr': 'HR面'
        }
        return round_map.get(round_code, '面试')


if __name__ == "__main__":
    generator = InterviewQuestionsGenerator()
    
    # 示例：生成Java开发岗位面试题
    questions = generator.generate_questions(
        job_title="Java高级开发工程师",
        job_requirements="5年以上Java开发经验，熟悉Spring生态，有微服务经验",
        interview_round="first",
        interview_type="tech"
    )
    
    print(questions)

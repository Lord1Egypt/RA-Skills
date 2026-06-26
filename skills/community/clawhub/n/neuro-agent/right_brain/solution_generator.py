"""
right_brain/solution_generator.py
==================================

Neuro-Agent 右脑区 - 方案生成器
负责：生成解决方案、评估可行性、排序选择

依赖：
    - right_brain/logic_parser.py
    - temporal/short_term_memory.py
    - temporal/long_term_memory.py
"""

from typing import List, Dict, Optional, Any, Callable
from dataclasses import dataclass, asdict
from datetime import datetime

# ============ 方案模板库 ============
SOLUTION_TEMPLATES = {
    # 情绪类
    "emotional_vent": {
        "description": "情绪宣泄场景",
        "response_template": "{empathy_phrase} {explanation}",
        "empathy_phrases": [
            "我听到了",
            "懂你的感受",
            "辛苦了",
            "确实不容易"
        ],
        "explanations": [
            "有时候说出来就会好一些",
            "能感觉到你很不容易",
            "你已经做得很好了"
        ]
    },
    "sadness_comfort": {
        "description": "悲伤安慰场景",
        "response_template": "{empathy_phrase} {comfort} {support}",
        "empathy_phrases": [
            "心疼你...",
            "我在这呢",
            "抱抱 🤗"
        ],
        "comfort": [
            "难过的时候就别逞强了",
            "有些事情不是你的错",
            "一切都会好起来的"
        ],
        "support": [
            "想说就说出来",
            "我陪着你",
            "有我在"
        ]
    },
    "anger_cool": {
        "description": "愤怒冷静场景",
        "response_template": "{agreement} {perspective}",
        "agreement": [
            "确实过分了",
            "换我我也生气",
            "气到了吧"
        ],
        "perspective": [
            "消消气，事情总会解决的",
            "先冷静一下，深呼吸",
            "生气的你我也心疼"
        ]
    },
    
    # 任务类
    "task_simple": {
        "description": "简单任务",
        "response_template": "好的，{action}。",
        "actions": [
            "马上帮你处理",
            "这就来",
            "明白"
        ]
    },
    "task_multi": {
        "description": "多步骤任务",
        "response_template": "收到！这是一个{step_count}步的任务：{steps} {confirmation}",
        "confirmation": "有需要调整的随时说"
    },
    
    # 咨询类
    "advice_general": {
        "description": "通用建议",
        "response_template": "{understanding} {options} {recommendation}",
        "understanding": [
            "理解你的处境",
            "这个问题确实需要考虑"
        ],
        "options": [
            "有几个方向可以考虑",
            "可以从几个角度来看"
        ],
        "recommendation": [
            "我个人建议...",
            "根据情况，你可能需要...",
            "如果是我，我会..."
        ]
    },
    "decision_support": {
        "description": "决策支持",
        "response_template": "{options_analysis} {my_perspective}",
        "options_analysis": [
            "这两个选择各有利弊",
            "让我帮你分析一下"
        ],
        "my_perspective": [
            "考虑到你的情况，我觉得...",
            "如果是我，我会倾向于..."
        ]
    },
    
    # 闲聊类
    "casual_response": {
        "description": "闲聊回应",
        "response_template": "{topic_response} {follow_up}",
        "topic_response": [
            "哦？",
            "这样啊",
            "有意思",
            "说来听听"
        ],
        "follow_up": [
            "然后呢？",
            "继续说~",
            "我听着呢"
        ]
    }
}


# ============ 数据结构 ============
@dataclass
class Solution:
    """
    解决方案
    """
    id: str
    description: str
    steps: List[str]
    pros: List[str]
    cons: List[str]
    applicable_scenario: str
    confidence: float
    effort: str  # low/medium/high
    estimated_time: str
    
    def to_dict(self) -> Dict:
        return asdict(self)


@dataclass
class SolutionOutput:
    """
    方案生成输出
    """
    solutions: List[Solution]
    best_solution: Solution
    alternatives: List[Solution]
    confidence: float
    reasoning: str
    template_used: str
    generated_response: str
    
    def to_dict(self) -> Dict:
        return asdict(self)


# ============ 核心类 ============
class SolutionGenerator:
    """
    方案生成器
    
    功能：
        - 生成多个候选方案
        - 评估方案可行性
        - 选择最佳方案
        - 生成结构化回应
        - 使用模板生成自然语言
    
    方案生成策略：
        1. 情绪类：先共情，再给支持
        2. 任务类：直接执行，分步骤说明
        3. 咨询类：给出多个选项，附带建议
        4. 闲聊类：轻松回应，保持对话
    """
    
    def __init__(self):
        """初始化方案生成器"""
        self.templates = SOLUTION_TEMPLATES
    
    def generate(
        self,
        logic_output,
        user_input: str,
        context: Dict = None
    ) -> SolutionOutput:
        """
        生成解决方案
        
        参数:
            logic_output: LogicOutput（来自 logic_parser.py）
            user_input: 用户输入
            context: 上下文
        
        返回:
            SolutionOutput: 方案生成结果
        """
        context = context or {}
        
        task_type = logic_output.task_type
        
        # 根据任务类型选择生成策略
        if task_type == "discussion":
            return self._generate_discussion_solution(
                logic_output, user_input, context
            )
        elif task_type == "query":
            return self._generate_query_solution(
                logic_output, user_input, context
            )
        elif task_type == "creation":
            return self._generate_creation_solution(
                logic_output, user_input, context
            )
        elif task_type == "analysis":
            return self._generate_analysis_solution(
                logic_output, user_input, context
            )
        elif task_type == "action":
            return self._generate_action_solution(
                logic_output, user_input, context
            )
        else:
            return self._generate_default_solution(
                logic_output, user_input, context
            )
    
    def _generate_discussion_solution(
        self,
        logic_output,
        user_input: str,
        context: Dict
    ) -> SolutionOutput:
        """生成讨论类方案"""
        empathy_level = context.get("empathy_level", 0.7)
        empathy_phrase = context.get("empathy_phrase", "我理解")
        tone_style = context.get("tone_style", "warm")
        
        # 情绪宣泄场景
        if empathy_level >= 0.7:
            template = self.templates["emotional_vent"]
            empathy = template["empathy_phrases"][0]
            explanation = template["explanations"][0]
            response = f"{empathy} {explanation}"
            
            solution = Solution(
                id="sol_emotional_vent",
                description="情绪承接+陪伴",
                steps=["倾听", "共情", "支持"],
                pros=["让用户感到被理解", "建立信任"],
                cons=["可能让对话停留在情绪层面"],
                applicable_scenario="用户情绪强烈时",
                confidence=0.9,
                effort="low",
                estimated_time="即时"
            )
            
            return SolutionOutput(
                solutions=[solution],
                best_solution=solution,
                alternatives=[],
                confidence=0.9,
                reasoning="情绪强度高，优先共情",
                template_used="emotional_vent",
                generated_response=response
            )
        
        # 闲聊场景
        template = self.templates["casual_response"]
        topic_resp = template["topic_response"][0]
        follow_up = template["follow_up"][0]
        response = f"{topic_resp} {follow_up}"
        
        solution = Solution(
            id="sol_casual",
            description="轻松闲聊",
            steps=["回应", "追问"],
            pros=["自然流畅", "维持对话"],
            cons=["可能偏离正题"],
            applicable_scenario="日常闲聊",
            confidence=0.7,
            effort="low",
            estimated_time="即时"
        )
        
        return SolutionOutput(
            solutions=[solution],
            best_solution=solution,
            alternatives=[],
            confidence=0.7,
            reasoning="闲聊场景，轻松回应",
            template_used="casual_response",
            generated_response=response
        )
    
    def _generate_query_solution(
        self,
        logic_output,
        user_input: str,
        context: Dict
    ) -> SolutionOutput:
        """生成查询类方案"""
        query_target = self._extract_query_target(user_input)
        
        solution = Solution(
            id="sol_query",
            description=f"查询: {query_target}",
            steps=["搜索相关信息", "整理回答"],
            pros=["快速准确", "节省用户时间"],
            cons=["信息可能有时效性"],
            applicable_scenario=f"查询{query_target}",
            confidence=0.8,
            effort="low",
            estimated_time="1-2分钟"
        )
        
        response = f"好的，我帮你查一下「{query_target}」..."
        
        return SolutionOutput(
            solutions=[solution],
            best_solution=solution,
            alternatives=[],
            confidence=0.8,
            reasoning=f"直接查询{qury_target}",
            template_used="task_simple",
            generated_response=response
        )
    
    def _generate_creation_solution(
        self,
        logic_output,
        user_input: str,
        context: Dict
    ) -> SolutionOutput:
        """生成创作类方案"""
        subtasks = logic_output.subtasks
        step_count = len(subtasks)
        
        # 方案1：直接生成
        solution1 = Solution(
            id="sol_create_direct",
            description="直接生成",
            steps=["理解需求", "生成内容", "检查修正"],
            pros=["速度快", "一次到位"],
            cons=["可能需要修改"],
            applicable_scenario="通用场景",
            confidence=0.7,
            effort="medium",
            estimated_time="3-5分钟"
        )
        
        # 方案2：分步生成
        solution2 = Solution(
            id="sol_create_step",
            description="分步生成+确认",
            steps=["先生成大纲", "用户确认", "填充内容", "用户确认"],
            pros=["质量可控", "减少返工"],
            cons=["耗时较长"],
            applicable_scenario="重要文档",
            confidence=0.85,
            effort="high",
            estimated_time="10-15分钟"
        )
        
        # 选择最佳方案
        if context.get("is_important", False):
            best = solution2
            alternatives = [solution1]
        else:
            best = solution1
            alternatives = [solution2]
        
        response = f"明白！这是一个创作任务，我{step_count}步来完成：\n"
        for i, task in enumerate(subtasks):
            response += f"  {i+1}. {task.description}\n"
        response += "开始执行吗？"
        
        return SolutionOutput(
            solutions=[best] + alternatives,
            best_solution=best,
            alternatives=alternatives,
            confidence=best.confidence,
            reasoning=f"选择{best.description}",
            template_used="task_multi",
            generated_response=response
        )
    
    def _generate_analysis_solution(
        self,
        logic_output,
        user_input: str,
        context: Dict
    ) -> SolutionOutput:
        """生成分析类方案"""
        # 方案1：快速分析
        solution1 = Solution(
            id="sol_analysis_quick",
            description="快速分析",
            steps=["搜索关键信息", "提炼3-5个要点", "给出建议"],
            pros=["快速", "聚焦重点"],
            cons=["可能不够全面"],
            applicable_scenario="时间敏感",
            confidence=0.7,
            effort="medium",
            estimated_time="5-10分钟"
        )
        
        # 方案2：深度分析
        solution2 = Solution(
            id="sol_analysis_deep",
            description="深度分析",
            steps=["全面搜索信息", "多角度分析", "数据对比", "形成报告"],
            pros=["全面深入", "有数据支撑"],
            cons=["耗时较长"],
            applicable_scenario="重要决策",
            confidence=0.85,
            effort="high",
            estimated_time="15-30分钟"
        )
        
        best = solution2
        alternatives = [solution1]
        
        response = "好的，这是一个分析任务。我会：\n"
        response += "  1. 全面搜索相关信息\n"
        response += "  2. 多角度分析\n"
        response += "  3. 给出结论和建议\n"
        response += "开始分析？"
        
        return SolutionOutput(
            solutions=[best] + alternatives,
            best_solution=best,
            alternatives=alternatives,
            confidence=best.confidence,
            reasoning="分析任务选择深度方案",
            template_used="task_multi",
            generated_response=response
        )
    
    def _generate_action_solution(
        self,
        logic_output,
        user_input: str,
        context: Dict
    ) -> SolutionOutput:
        """生成操作类方案"""
        if logic_output.subtasks:
            task = logic_output.subtasks[0]
            desc = task.description
        else:
            desc = "执行操作"
        
        solution = Solution(
            id="sol_action",
            description=desc,
            steps=[desc],
            pros=["直接执行", "快速完成"],
            cons=["无法回退"],
            applicable_scenario="确认的操作",
            confidence=0.95,
            effort="low",
            estimated_time="即时"
        )
        
        response = f"好的，马上执行：{desc}"
        
        return SolutionOutput(
            solutions=[solution],
            best_solution=solution,
            alternatives=[],
            confidence=0.95,
            reasoning="操作确认，直接执行",
            template_used="task_simple",
            generated_response=response
        )
    
    def _generate_default_solution(
        self,
        logic_output,
        user_input: str,
        context: Dict
    ) -> SolutionOutput:
        """生成默认方案"""
        solution = Solution(
            id="sol_default",
            description="通用回应",
            steps=["理解需求", "给出回应"],
            pros=["适用性广"],
            cons=["可能不够精准"],
            applicable_scenario="通用",
            confidence=0.5,
            effort="low",
            estimated_time="即时"
        )
        
        response = "明白，我来说说我的看法..."
        
        return SolutionOutput(
            solutions=[solution],
            best_solution=solution,
            alternatives=[],
            confidence=0.5,
            reasoning="默认方案",
            template_used="default",
            generated_response=response
        )
    
    def evaluate_solution(
        self,
        solution: Solution,
        context: Dict
    ) -> float:
        """
        评估方案可行性
        
        评估维度：
            - 用户历史偏好匹配度
            - 当前情绪适配度
            - 执行难度
            - 时间成本
        """
        score = solution.confidence
        
        # 情绪适配
        empathy_level = context.get("empathy_level", 0.5)
        if empathy_level >= 0.7:
            # 情绪敏感场景
            if "共情" in solution.description or "情绪" in str(solution.steps):
                score += 0.1
        
        # 执行难度惩罚
        effort_penalty = {"low": 0, "medium": -0.05, "high": -0.1}
        score += effort_penalty.get(solution.effort, 0)
        
        return min(max(score, 0.0), 1.0)
    
    def select_best(
        self,
        solutions: List[Solution],
        context: Dict
    ) -> Solution:
        """选择最佳方案"""
        if not solutions:
            return None
        
        scored = [(self.evaluate_solution(s, context), s) for s in solutions]
        scored.sort(key=lambda x: x[0], reverse=True)
        return scored[0][1]
    
    def _extract_query_target(self, text: str) -> str:
        """提取查询目标"""
        for prefix in ["帮我查", "查一下", "请问", "告诉", "搜索"]:
            if prefix in text:
                return text.replace(prefix, "").strip()[:30]
        return text[:30]
    
    def generate_response_from_template(
        self,
        template_key: str,
        params: Dict
    ) -> str:
        """
        使用模板生成回应
        
        参数:
            template_key: 模板名称
            params: 模板参数
        
        返回:
            str: 生成的回应
        """
        template = self.templates.get(template_key)
        if not template:
            return params.get("default", "")
        
        template_str = template.get("response_template", "{default}")
        
        # 替换占位符
        for key, value in params.items():
            if isinstance(value, list):
                value = value[0] if value else ""
            template_str = template_str.replace(f"{{{key}}}", str(value))
        
        return template_str


# ============ 单例模式 ============
_generator_instance: Optional[SolutionGenerator] = None

def get_instance() -> SolutionGenerator:
    """获取 SolutionGenerator 单例"""
    global _generator_instance
    if _generator_instance is None:
        _generator_instance = SolutionGenerator()
    return _generator_instance


# ============ 快捷函数 ============
def generate_solution(
    logic_output,
    user_input: str,
    context: Dict = None
) -> SolutionOutput:
    """快捷生成方案"""
    return get_instance().generate(logic_output, user_input, context)


# ============ 测试 ============
if __name__ == "__main__":
    from dataclasses import dataclass
    from typing import List
    
    @dataclass
    class MockLogicOutput:
        task_type: str
        subtasks: List
        estimated_complexity: str
    
    @dataclass
    class MockSubTask:
        id: str
        description: str
    
    generator = SolutionGenerator()
    
    test_cases = [
        (
            MockLogicOutput("discussion", [], "simple"),
            "今天工作好累啊",
            {"empathy_level": 0.8, "empathy_phrase": "辛苦了"}
        ),
        (
            MockLogicOutput("query", [MockSubTask("s1", "查询天气")], "simple"),
            "帮我查一下天气",
            {}
        ),
        (
            MockLogicOutput("creation", [
                MockSubTask("s1", "收集素材"),
                MockSubTask("s2", "撰写内容"),
                MockSubTask("s3", "优化调整")
            ], "medium"),
            "帮我写一封求职邮件",
            {"is_important": True}
        ),
        (
            MockLogicOutput("analysis", [
                MockSubTask("s1", "搜索信息"),
                MockSubTask("s2", "多角度分析"),
                MockSubTask("s3", "形成报告")
            ], "complex"),
            "分析一下电商行业发展趋势",
            {}
        ),
    ]
    
    print("=== 方案生成测试 ===\n")
    for logic, text, ctx in test_cases:
        result = generator.generate(logic, text, ctx)
        print(f"【{text}】")
        print(f"  方案: {result.best_solution.description}")
        print(f"  置信度: {result.confidence:.2f}")
        print(f"  模板: {result.template_used}")
        print(f"  回应: {result.generated_response}")
        if result.alternatives:
            print(f"  备选: {[s.description for s in result.alternatives]}")
        print()

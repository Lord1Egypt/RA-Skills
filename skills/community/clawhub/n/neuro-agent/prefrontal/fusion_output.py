"""
prefrontal/fusion_output.py
===========================

Neuro-Agent 前额叶区 - 融合输出层
负责：将各脑区输出融合成统一回应、生成最终文本

依赖：
    - prefrontal/monitor.py
    - prefrontal/executor.py
    - left_brain/*
    - right_brain/*
    - temporal/*
"""

from typing import List, Dict, Optional, Any
from dataclasses import dataclass, asdict

# ============ 数据结构 ============
@dataclass
class FusionResult:
    """
    融合结果
    """
    response: str
    response_style: str
    capsules_to_save: List[Any]  # 需要保存的胶囊
    capsules_to_update: List[Any]  # 需要更新的胶囊
    metadata: Dict
    memory_injected: bool
    empathy_injected: bool
    skill_results: List[str]
    
    def to_dict(self) -> Dict:
        return asdict(self)


# ============ 融合策略模板 ============
FUSION_TEMPLATES = {
    "empathetic": {
        "order": ["empathy", "memory", "solution", "question"],
        "structure": "{empathy}\n{memory}\n{solution}\n{question}",
        "example": "辛苦了...\n我记得你之前说过...\n我觉得...\n你想先聊聊哪方面？"
    },
    "logical": {
        "order": ["solution", "memory", "question"],
        "structure": "{solution}\n{memory}\n{question}",
        "example": "这个问题...\n基于你之前说的...\n还有其他问题吗？"
    },
    "recalling": {
        "order": ["memory", "empathy", "solution", "question"],
        "structure": "{memory}\n{empathy}\n{solution}\n{question}",
        "example": "我记得你之前提到...\n我也感觉得到...\n那件事的话...\n现在怎么样了？"
    },
    "casual": {
        "order": ["empathy", "solution"],
        "structure": "{empathy} {solution}",
        "example": "懂你~ 那咱们来聊聊..."
    },
    "balanced": {
        "order": ["empathy", "solution", "memory", "question"],
        "structure": "{empathy} {solution}\n{memory}\n{question}",
        "example": "理解~\n答案是...\n另外我记得...\n你还想了解什么？"
    },
    "proactive": {
        "order": ["greeting", "empathy", "memory", "question"],
        "structure": "{greeting} {empathy}\n{memory}\n{question}",
        "example": "早上好！\n今天感觉怎么样？\n对了，你之前说的...\n有什么想聊的吗？"
    }
}


# ============ 核心类 ============
class FusionOutput:
    """
    融合输出层
    
    功能：
        1. 根据监控层确认的权重和计划，融合各脑区输出
        2. 注入记忆（自然融入）
        3. 融合共情（选择合适语句）
        4. 整合技能结果
        5. 生成最终回应文本
    
    融合原则：
        - emotion_weight 高 → 共情优先，逻辑简化
        - logic_weight 高 → 直接回答，不废话
        - memory_weight 高 → 引用记忆，建立联系
        - pacing = quick → 简短直接
        - pacing = deliberate → 完整详细
    """
    
    def __init__(self):
        """初始化融合层"""
        self.templates = FUSION_TEMPLATES
    
    def fuse(
        self,
        monitor_output: Any,  # MonitorOutput
        all_outputs: Dict[str, Any],
        context: Dict = None
    ) -> FusionResult:
        """
        融合主流程
        
        参数:
            monitor_output: 监控层输出
            all_outputs: 所有脑区输出
            context: 上下文
        
        返回:
            FusionResult: 最终融合结果
        """
        context = context or {}
        
        # 1. 获取关键数据
        plan = getattr(monitor_output, "approved_plan", None)
        weights = getattr(monitor_output, "final_weights", None)
        capsules_to_save = []
        
        # 2. 确定响应风格
        response_style = getattr(plan, "response_style", "balanced") \
            if plan else "balanced"
        
        # 3. 提取各部分内容
        left = all_outputs.get("left", {})
        right = all_outputs.get("right", {})
        temporal = all_outputs.get("temporal", {})
        
        # 共情部分
        empathy_text, empathy_injected = self._apply_empathy_weight(left, plan)
        
        # 逻辑部分
        solution_text = self._apply_logic_weight(right, plan)
        
        # 记忆部分
        memory_text, memory_injected = self._inject_memory(temporal, plan)
        
        # 技能结果
        skill_results = self._integrate_skills(all_outputs, plan)
        
        # 4. 组合回应
        response = self._assemble_response(
            response_style, plan,
            empathy_text, solution_text, memory_text,
            skill_results, context
        )
        
        # 5. 收集需要保存的胶囊
        empathy_output = getattr(left, "capsule_output", None) if hasattr(left, 'capsule_output') else None
        if empathy_output:
            capsules_to_save = getattr(empathy_output, "capsules", [])
        
        return FusionResult(
            response=response,
            response_style=response_style,
            capsules_to_save=capsules_to_save,
            capsules_to_update=[],
            metadata={
                "weights": asdict(weights) if hasattr(weights, 'to_dict') else {},
                "strategy": getattr(plan, "response_style", ""),
                "memory_injected": memory_injected,
                "empathy_injected": empathy_injected,
                "override_log": getattr(monitor_output, "override_log", ""),
                "conflict_score": getattr(monitor_output, "conflict_score", 0.0),
            },
            memory_injected=memory_injected,
            empathy_injected=empathy_injected,
            skill_results=skill_results
        )
    
    def _apply_empathy_weight(
        self,
        left_output: Any,
        plan: Any
    ) -> tuple:
        """
        根据情感权重调整共情程度
        """
        empathy_phrases = getattr(plan, "empathy_phrases", []) if plan else []
        tone_modifier = getattr(plan, "tone_modifier", "natural") if plan else "natural"
        
        empathy_weight = 0.5
        if hasattr(left_output, 'emotion_weight'):
            empathy_weight = left_output.emotion_weight
        
        # 根据权重选择共情程度
        if not empathy_phrases:
            return "", False
        
        primary_phrase = empathy_phrases[0] if empathy_phrases else ""
        
        # 权重极低 → 不使用共情
        if empathy_weight < 0.1:
            return "", False
        
        # 权重低 → 简短共情
        elif empathy_weight < 0.3:
            return primary_phrase, True
        
        # 权重中等 → 完整共情
        elif empathy_weight < 0.7:
            phrase = primary_phrase
            if tone_modifier == "soft":
                phrase = phrase + "..."
            elif tone_modifier == "warm":
                phrase = phrase + " 🤗"
            return phrase, True
        
        # 权重高 → 强烈共情
        else:
            phrases = empathy_phrases[:2]
            combined = " ".join(phrases)
            if tone_modifier == "soft":
                combined = combined + "..."
            elif tone_modifier == "warm":
                combined = combined + " 🤗"
            elif tone_modifier == "silent":
                return "嗯。" if not phrases else phrases[0], True
            return combined, True
    
    def _apply_logic_weight(
        self,
        right_output: Any,
        plan: Any
    ) -> str:
        """
        根据逻辑权重调整答案详细程度
        """
        # 获取方案
        solution = getattr(right_output, "best_solution", None) \
            if hasattr(right_output, 'best_solution') else None
        
        pacing = getattr(plan, "pacing", "deliberate") if plan else "deliberate"
        
        if pacing == "quick":
            # 快速模式 → 只给核心答案
            if solution:
                return f"好的，{getattr(solution, 'description', '执行中')}。"
            return "明白，马上处理。"
        
        # 正常模式 → 完整回答
        if solution:
            desc = getattr(solution, "description', '")
            steps = getattr(solution, 'steps', [])
            
            if steps:
                steps_text = "\n".join([f"{i+1}. {s}" for i, s in enumerate(steps[:3])])
                return f"好的，这需要几步：\n{steps_text}\n开始执行？"
            return f"好的，我来帮你{desc}。"
        
        return "好的。"
    
    def _inject_memory(
        self,
        temporal_output: Any,
        plan: Any
    ) -> tuple:
        """
        注入记忆到回应中
        """
        if not plan or not getattr(plan, "should_mention_memory", False):
            return "", False
        
        memories = getattr(plan, "memory_to_mention", [])
        
        if not memories:
            return "", False
        
        # 最多引用2条记忆
        memories = memories[:2]
        
        # 自然融入格式
        memory_parts = []
        for mem in memories:
            mem_str = str(mem)
            if len(mem_str) > 30:
                mem_str = mem_str[:30] + "..."
            
            # 随机选择引入方式
            intro_options = [
                f"我记得你之前说过『{mem_str}』",
                f"想起你提到过{getattr(mem, 'tags', [''])[0] or '这个'}：{mem_str}",
                f"对了，你上次说『{mem_str}』",
            ]
            memory_parts.append(intro_options[hash(mem_str) % len(intro_options)])
        
        memory_text = "\n".join(memory_parts)
        
        return memory_text, True
    
    def _integrate_skills(
        self,
        all_outputs: Dict,
        plan: Any
    ) -> List[str]:
        """
        整合技能输出
        """
        results = []
        
        # 从各脑区获取技能结果
        skill_data = all_outputs.get("skill_results", {})
        
        for skill_name, result in skill_data.items():
            if result:
                results.append(f"[{skill_name}]: {result}")
        
        return results
    
    def _assemble_response(
        self,
        response_style: str,
        plan: Any,
        empathy_text: str,
        solution_text: str,
        memory_text: str,
        skill_results: List[str],
        context: Dict
    ) -> str:
        """
        组装最终回应
        """
        # 获取模板
        template = self.templates.get(response_style, self.templates["balanced"])
        order = template["order"]
        
        # 构建各部分
        parts = {}
        
        for section in order:
            if section == "empathy":
                parts["empathy"] = empathy_text
            elif section == "solution":
                parts["solution"] = solution_text
            elif section == "memory":
                parts["memory"] = memory_text
            elif section == "question":
                parts["question"] = self._generate_follow_up(plan, context)
            elif section == "greeting":
                hour = context.get("hour", 12)
                if hour < 12:
                    parts["greeting"] = "早上好~"
                elif hour < 18:
                    parts["greeting"] = "下午好~"
                else:
                    parts["greeting"] = "晚上好~"
        
        # 过滤空部分
        parts = {k: v for k, v in parts.items() if v}
        
        # 使用模板结构
        structure = template["structure"]
        
        # 简单替换
        response = structure
        for key, value in parts.items():
            response = response.replace(f"{{{key}}}", value)
        
        # 清理残留占位符
        import re
        response = re.sub(r'\{[^}]+\}', '', response)
        
        # 移除空行
        lines = [l.strip() for l in response.split('\n') if l.strip()]
        response = "\n".join(lines)
        
        return response
    
    def _generate_follow_up(
        self,
        plan: Any,
        context: Dict
    ) -> str:
        """
        生成跟进问题
        """
        response_style = getattr(plan, "response_style", "balanced") if plan else "balanced"
        
        if response_style == "empathetic":
            return "想先聊聊哪方面？"
        elif response_style == "logical":
            return "还有其他问题吗？"
        elif response_style == "recalling":
            return "现在怎么样了？"
        elif response_style == "casual":
            return "继续说~"
        elif response_style == "proactive":
            return "有什么想聊的吗？"
        else:
            return "还有什么需要帮忙的？"
    
    def apply_tone(
        self,
        text: str,
        tone_modifier: str
    ) -> str:
        """
        应用语气修饰
        """
        if tone_modifier == "soft":
            # 柔和：加省略
            if not text.endswith("...") and not text.endswith("。"):
                text = text + "..."
            # 断句
            text = text.replace("，", "，...")
        
        elif tone_modifier == "warm":
            # 温暖：加emoji
            if "🤗" not in text and "❤️" not in text:
                text = text + " 🤗"
        
        elif tone_modifier == "precise":
            # 精准：去除废话
            text = text.strip()
        
        elif tone_modifier == "playful":
            # 俏皮：加~符号
            if not text.endswith("~"):
                text = text.rstrip("。!！") + "~"
        
        return text


# ============ 单例 ============
_fusion_instance: Optional[FusionOutput] = None

def get_instance() -> FusionOutput:
    global _fusion_instance
    if _fusion_instance is None:
        _fusion_instance = FusionOutput()
    return _fusion_instance


def fuse(
    monitor_output: Any,
    all_outputs: Dict,
    context: Dict = None
) -> FusionResult:
    """快捷融合"""
    return get_instance().fuse(monitor_output, all_outputs, context)


def adjust_for_reward_punishment(
    response: str,
    behavior: Any
) -> str:
    """
    根据 Reward Punishment System 的行为调整参数，
    调整融合输出的语气、长度、风格。
    
    Args:
        response: 原始响应文本
        behavior: BehaviorAdjustments 对象
    
    Returns:
        调整后的响应文本
    """
    if behavior is None:
        return response
    
    # 1. 长度调整
    max_len = getattr(behavior, 'max_response_length', 500)
    if len(response) > max_len:
        # 截断并添加省略或收尾
        response = response[:max_len]
        if not response.endswith(("。", "！", "？")):
            response = response.rstrip("，、") + "..."
    
    # 2. 响应延迟提示（冷却期内）
    delay = getattr(behavior, 'response_delay_minutes', 0)
    if delay > 0:
        # 在回复前添加轻微的"思考中"提示
        delay_phrases = [
            "让我想想...",
            "这个问题值得想想...",
            "我思考一下...",
        ]
        if delay >= 10:
            response = delay_phrases[hash(response) % len(delay_phrases)] + "\n" + response
    
    # 3. 语气调整
    tone = getattr(behavior, 'tone', 'casual')
    warmth = getattr(behavior, 'warmth_level', 0.5)
    openness = getattr(behavior, 'openness', 0.5)
    
    if tone == 'cold':
        # 冷淡模式：去除昵称、减少 emoji、正式语气
        response = response.replace("~", "。")
        response = response.replace("哈哈", "")
        response = response.replace("🤗", "").replace("😊", "").replace("🌟", "")
        if not any(c in response for c in ["。", "！", "？"]):
            response = response + "。"
    
    elif tone == 'cautious':
        # 谨慎模式：冷却期内使用
        if "..." not in response:
            response = response.rstrip("。！？") + "..."
    
    elif tone == 'warm':
        # 温暖模式：高信用用户
        if warmth > 0.8:
            # 高温暖：添加关怀
            if not any(c in response for c in ["💙", "🤗", "🌟", "😊"]):
                warm_emojis = ["💙", "🤗", "😊", "✨"]
                response = response + " " + warm_emojis[hash(response) % len(warm_emojis)]
    
    elif tone == 'close':
        # 亲密模式：最高信用
        if openness > 0.8:
            # 可以更自然、更亲密
            pass  # 保持原样，因为已经是高开放度
    
    # 4. 边界收紧提示
    boundary_tightness = getattr(behavior, 'boundary_tightness', 0.0)
    if boundary_tightness > 0.7:
        # 高边界收紧：不接受某些请求
        # 这种情况通常在 RPS 层面已经拦截了
        # 这里只是确保回复不显得过于热情
        if response.startswith(("好呀", "当然", "没问题")):
            response = "好的。" + response[2:]
    
    # 5. 清理空行和多余空格
    import re
    response = re.sub(r'\n{3,}', '\n\n', response)
    response = response.strip()
    
    return response


# ============ 测试 ============
if __name__ == "__main__":
    fusion = FusionOutput()
    
    from dataclasses import dataclass
    
    @dataclass
    class MockWeights:
        emotion_weight: float
        logic_weight: float
        memory_weight: float
    
    @dataclass
    class MockPlan:
        response_style: str
        should_mention_memory: bool
        memory_to_mention: list
        should_use_empathy: bool
        empathy_phrases: list
        skills_to_call: list
        tone_modifier: str
        pacing: str
    
    @dataclass
    class MockMonitor:
        approved_plan: Any
        final_weights: Any
        override_log: str
        conflict_score: float
    
    @dataclass
    class MockSolution:
        description: str
        steps: list
    
    print("=== 融合层测试 ===\n")
    
    test_cases = [
        ("empathetic", ["辛苦了..."], ["我记得..."], MockWeights(0.8, 0.1, 0.2), "deliberate"),
        ("logical", [], [], MockWeights(0.1, 0.9, 0.1), "quick"),
        ("recalling", ["懂的"], ["你之前说的..."], MockWeights(0.3, 0.2, 0.8), "deliberate"),
        ("casual", ["哈哈"], [], MockWeights(0.6, 0.1, 0.3), "deliberate"),
    ]
    
    for style, empathy, memory, weights, pacing in test_cases:
        plan = MockPlan(
            response_style=style,
            should_mention_memory=bool(memory),
            memory_to_mention=memory,
            should_use_empathy=bool(empathy),
            empathy_phrases=empathy,
            skills_to_call=[],
            tone_modifier="warm",
            pacing=pacing
        )
        
        monitor = MockMonitor(plan, weights, "", 0.3)
        
        result = fusion.fuse(monitor, {}, {"hour": 14})
        print(f"【{style}】")
        print(f"  权重: E={weights.emotion_weight:.1f} L={weights.logic_weight:.1f} M={weights.memory_weight:.1f}")
        print(f"  输出: {result.response}")
        print(f"  共情: {result.empathy_injected}, 记忆: {result.memory_injected}")
        print()

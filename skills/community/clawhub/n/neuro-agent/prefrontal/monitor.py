"""
prefrontal/monitor.py
=====================

Neuro-Agent 前额叶区 - 监控层（背外侧前额叶）
负责：审核执行层输出、权重纠偏、记忆调用监管、技能调用监管、死循环熔断

⚠️ 这是最核心的安全模块，执行层必须接受监控层审查
"""

from typing import List, Dict, Optional, Any, Tuple
from dataclasses import dataclass, asdict
from datetime import datetime

# ============ 数据结构 ============
@dataclass
class BlockedAction:
    """
    被阻止的动作
    """
    action_type: str  # memory/skill/action
    target: str
    reason: str
    suggested_alternative: str
    
    def to_dict(self) -> Dict:
        return asdict(self)


@dataclass
class Correction:
    """
    纠偏记录
    """
    field: str
    original_value: Any
    corrected_value: Any
    reason: str
    
    def to_dict(self) -> Dict:
        return asdict(self)


@dataclass
class IntentValidation:
    """
    意图校验结果
    """
    is_valid: bool
    original_intent: str
    corrected_intent: str
    correction_reason: str
    confidence: float
    
    def to_dict(self) -> Dict:
        return asdict(self)


@dataclass
class MonitorOutput:
    """
    监控层输出
    """
    final_weights: Any  # BrainWeights
    approved_plan: Any  # ExecutionPlan
    blocked_actions: List[BlockedAction]
    corrections: List[Correction]
    override_log: str
    conflict_score: float  # 0.0-1.0
    needs_review: bool  # 是否需要人工审核
    fusion_ready: bool  # 是否可以进入融合
    
    def to_dict(self) -> Dict:
        return {
            **asdict(self),
            "final_weights": asdict(self.final_weights) if hasattr(self.final_weights, 'to_dict') else self.final_weights,
            "approved_plan": asdict(self.approved_plan) if hasattr(self.approved_plan, 'to_dict') else self.approved_plan,
            "blocked_actions": [asdict(a) if hasattr(a, 'to_dict') else a for a in self.blocked_actions],
            "corrections": [asdict(c) if hasattr(c, 'to_dict') else c for c in self.corrections],
        }


# ============ 核心类 ============
class Monitor:
    """
    背外侧前额叶 - 监控层
    
    功能：
        1. 意图校验：检测伪装意图
        2. 权重纠偏：强制修正不合理的权重分配
        3. 记忆调用监管：敏感记忆、高频调用审查
        4. 技能调用监管：时机、情绪适配审查
        5. 死循环检测：连续争议时强制熔断
        6. 冲突系数计算：量化左右脑争议程度
    
    纠偏公式：
        W_final = W_base × (1-C) + W_override × C
        
        冲突系数 C ∈ [0, 1]:
        - C < 0.2: 轻微冲突，轻介入
        - C < 0.5: 中度冲突，调整权重
        - C >= 0.5: 严重冲突，强制接管
        - C >= 0.8: 执行层被熔断
    """
    
    def __init__(self):
        """初始化监控层"""
        self._history: List[Any] = []  # 历史执行记录
        self._conflict_history: List[float] = []
    
    def monitor(
        self,
        executor_output: Any,  # ExecutorOutput
        all_outputs: Dict[str, Any],
        context: Dict = None
    ) -> MonitorOutput:
        """
        监控主流程
        
        参数:
            executor_output: 执行层输出
            all_outputs: 所有脑区原始输出
            context: 完整上下文
        
        返回:
            MonitorOutput: 监控结果
        """
        context = context or {}
        executor_output = executor_output or {}
        
        blocked: List[BlockedAction] = []
        corrections: List[Correction] = []
        override_log_parts = []
        
        # 1. 意图校验
        intent_validation = self._validate_intent(
            executor_output, all_outputs, context
        )
        if not intent_validation.is_valid:
            corrections.append(Correction(
                field="intent_type",
                original_value=intent_validation.original_intent,
                corrected_value=intent_validation.corrected_intent,
                reason=intent_validation.correction_reason
            ))
            override_log_parts.append(f"意图纠偏: {intent_validation.correction_reason}")
        
        # 2. 权重纠偏
        base_weights = getattr(executor_output, "base_weights", None)
        if base_weights:
            new_weights, weight_corrections = self._adjust_weights(
                base_weights, all_outputs, context
            )
            corrections.extend(weight_corrections)
            if weight_corrections:
                override_log_parts.append(f"权重纠偏: {len(weight_corrections)}项")
        else:
            new_weights = base_weights
        
        # 3. 冲突系数计算
        conflict_score = self._calculate_conflict_score(
            all_outputs, context
        )
        
        # 4. 死循环检测
        loop_detected = self._detect_loop()
        if loop_detected:
            override_log_parts.append("⚠️ 死循环熔断: 监控层强制接管")
            conflict_score = max(conflict_score, 0.8)
        
        # 5. 记忆调用监管
        plan = getattr(executor_output, "execution_plan", None)
        if plan:
            memory_blocks = self._check_memory_access(plan, context)
            blocked.extend(memory_blocks)
        
        # 6. 技能调用监管
        if plan:
            skill_blocks = self._check_skill_access(plan, context)
            blocked.extend(skill_blocks)
        
        # 7. 构建最终计划
        if corrections or blocked or conflict_score >= 0.5:
            approved_plan = self._modify_plan(plan, corrections, blocked)
        else:
            approved_plan = plan
        
        # 8. 记录历史
        self._history.append({
            "timestamp": datetime.now().isoformat(),
            "executor_output": executor_output,
            "conflict_score": conflict_score
        })
        self._conflict_history.append(conflict_score)
        if len(self._conflict_history) > 10:
            self._conflict_history = self._conflict_history[-10:]
        
        override_log = "\n".join(override_log_parts) if override_log_parts else "无纠偏"
        
        return MonitorOutput(
            final_weights=new_weights,
            approved_plan=approved_plan,
            blocked_actions=blocked,
            corrections=corrections,
            override_log=override_log,
            conflict_score=conflict_score,
            needs_review=conflict_score >= 0.8,
            fusion_ready=True
        )
    
    def _validate_intent(
        self,
        executor_output: Any,
        all_outputs: Dict,
        context: Dict
    ) -> IntentValidation:
        """
        意图校验
        """
        # 获取执行层判断的意图
        plan = getattr(executor_output, "execution_plan", None)
        if not plan:
            return IntentValidation(True, "", "", "", 1.0)
        
        # 获取原始情绪和意图
        left = all_outputs.get("left", {})
        right = all_outputs.get("right", {})
        
        emotion_score = getattr(left, "emotion_score", 0.0) \
            if hasattr(left, "emotion_score") else 0.0
        is_masked = getattr(left, "is_masked", False) \
            if hasattr(left, "is_masked") else False
        emotion_type = getattr(left, "emotion_type", "") \
            if hasattr(left, "emotion_type") else ""
        
        intent_type = getattr(right, "intent_type", "") \
            if hasattr(right, "intent_type") else ""
        
        # 检测伪装
        # 情绪伪装成提问/闲聊
        if is_masked and emotion_score >= 0.5:
            if intent_type in ["question", "casual_chat"]:
                if emotion_type in ["sadness", "anger", "anxiety", "frustration", "hidden_pain"]:
                    return IntentValidation(
                        is_valid=False,
                        original_intent=intent_type,
                        corrected_intent="emotional_vent",
                        correction_reason=f"情绪伪装成{intent_type}: {emotion_type}({emotion_score:.1f})",
                        confidence=0.85
                    )
        
        # 高情绪 → 实际应该是情绪宣泄
        if emotion_score >= 0.7 and intent_type in ["question", "casual_chat", "task_request"]:
            return IntentValidation(
                is_valid=False,
                original_intent=intent_type,
                corrected_intent="emotional_vent",
                correction_reason=f"高情绪{int(emotion_score*100)}%伪装成{intent_type}",
                confidence=0.75
            )
        
        return IntentValidation(True, intent_type, intent_type, "", 1.0)
    
    def _adjust_weights(
        self,
        base_weights: Any,
        all_outputs: Dict,
        context: Dict
    ) -> Tuple[Any, List[Correction]]:
        """
        权重纠偏
        """
        corrections = []
        
        emotion_score = 0.0
        left = all_outputs.get("left", {})
        if hasattr(left, "emotion_score"):
            emotion_score = left.emotion_score
        
        emotion_weight = getattr(base_weights, "emotion_weight", 0.33)
        logic_weight = getattr(base_weights, "logic_weight", 0.33)
        memory_weight = getattr(base_weights, "memory_weight", 0.33)
        
        # 高情绪 + 情绪权重不足 → 强制增强情绪权重
        if emotion_score >= 0.8 and emotion_weight < 0.5:
            delta = min(0.4, emotion_score - emotion_weight)
            emotion_weight = min(0.9, emotion_weight + delta)
            logic_weight = max(0.05, logic_weight - delta * 0.5)
            corrections.append(Correction(
                field="emotion_weight",
                original_value=round(emotion_weight - delta, 2),
                corrected_value=round(emotion_weight, 2),
                reason=f"高情绪{int(emotion_score*100)}%强制增强"
            ))
        
        # 悲伤/恐惧 + 逻辑权重过高 → 降低逻辑
        is_sad_or_fear = emotion_score >= 0.6 and getattr(left, "emotion_type", "") in ["sadness", "fear", "anxiety"]
        if is_sad_or_fear and logic_weight > 0.4:
            reduction = min(0.3, logic_weight - 0.1)
            logic_weight -= reduction
            emotion_weight = min(0.9, emotion_weight + reduction)
            corrections.append(Correction(
                field="logic_weight",
                original_value=round(logic_weight + reduction, 2),
                corrected_value=round(logic_weight, 2),
                reason="悲伤/焦虑场景降低逻辑权重"
            ))
        
        # 愤怒 + 共情不足 → 增强情绪
        if getattr(left, "emotion_type", "") == "anger" and emotion_score >= 0.6:
            if emotion_weight < 0.6:
                emotion_weight = max(emotion_weight + 0.2, 0.6)
                corrections.append(Correction(
                    field="emotion_weight",
                    original_value=round(emotion_weight - 0.2, 2),
                    corrected_value=round(emotion_weight, 2),
                    reason="愤怒场景增强情绪权重"
                ))
        
        from prefrontal.executor import BrainWeights
        new_weights = BrainWeights(
            emotion_weight=round(emotion_weight, 3),
            logic_weight=round(logic_weight, 3),
            memory_weight=round(memory_weight, 3)
        )
        
        return new_weights, corrections
    
    def _calculate_conflict_score(
        self,
        all_outputs: Dict,
        context: Dict
    ) -> float:
        """
        计算冲突系数 C ∈ [0, 1]
        """
        left = all_outputs.get("left", {})
        right = all_outputs.get("right", {})
        
        emotion_type = getattr(left, "emotion_type", "neutral")
        intent_type = getattr(right, "intent_type", "casual_chat")
        
        # 情绪-意图冲突
        conflict_pairs = [
            ("sadness", "task_request"),
            ("anger", "casual_chat"),
            ("anxiety", "greeting"),
            ("hidden_pain", "question"),
        ]
        
        emotion_intent_conflict = 0.0
        for emo, intent in conflict_pairs:
            if emotion_type == emo and intent_type == intent:
                emotion_intent_conflict = 0.4
                break
        
        # 权重冲突
        executor = all_outputs.get("executor", {})
        weights = getattr(executor, "base_weights", None)
        weight_conflict = 0.0
        if weights:
            max_w = max(weights.emotion_weight, weights.logic_weight, weights.memory_weight)
            min_w = min(weights.emotion_weight, weights.logic_weight, weights.memory_weight)
            if max_w - min_w < 0.1:
                weight_conflict = 0.2  # 太均衡，缺重点
        
        # 情绪不和谐
        emotion_dissonance = 0.0
        if getattr(left, "is_masked", False):
            emotion_dissonance = 0.3
        
        # 综合
        C = max(
            emotion_intent_conflict,
            weight_conflict,
            emotion_dissonance * 0.3
        )
        
        return min(max(C, 0.0), 1.0)
    
    def _detect_loop(self) -> bool:
        """
        死循环检测
        """
        if len(self._conflict_history) < 3:
            return False
        
        # 连续3次以上高冲突
        recent = self._conflict_history[-3:]
        if all(c >= 0.5 for c in recent):
            return True
        
        return False
    
    def _check_memory_access(
        self,
        plan: Any,
        context: Dict
    ) -> List[BlockedAction]:
        """
        记忆调用监管
        """
        blocked = []
        
        if not getattr(plan, "should_mention_memory", False):
            return blocked
        
        # 获取记忆列表（如果有的话）
        memories = getattr(plan, "memory_to_mention", [])
        retrieved = context.get("retrieved_capsules", [])
        
        for i, mem in enumerate(memories[:3]):
            # 检查是否为敏感记忆
            is_sensitive = False
            capsule_data = None
            
            # 尝试从 retrieved 中获取完整数据
            if i < len(retrieved):
                capsule_data = retrieved[i]
            
            if capsule_data:
                sensitivity = capsule_data.get("sensitivity", "normal")
                is_dormant = capsule_data.get("is_dormant", False)
                
                if sensitivity == "critical":
                    blocked.append(BlockedAction(
                        action_type="memory",
                        target=str(mem)[:30],
                        reason="critical 敏感度记忆禁止调用",
                        suggested_alternative="使用模糊化的概括"
                    ))
                elif sensitivity == "high" and context.get("emotion_score", 0) >= 0.6:
                    blocked.append(BlockedAction(
                        action_type="memory",
                        target=str(mem)[:30],
                        reason="high敏感度记忆在情绪波动时禁止调用",
                        suggested_alternative="延迟到情绪平稳后再提及"
                    ))
                elif is_dormant:
                    blocked.append(BlockedAction(
                        action_type="memory",
                        target=str(mem)[:30],
                        reason="记忆已休眠，禁止调用",
                        suggested_alternative="跳过此记忆"
                    ))
        
        return blocked
    
    def _check_skill_access(
        self,
        plan: Any,
        context: Dict
    ) -> List[BlockedAction]:
        """
        技能调用监管
        """
        blocked = []
        
        skills = getattr(plan, "skills_to_call", [])
        
        # 获取情绪
        left = context.get("left", {})
        emotion_type = getattr(left, "emotion_type", "neutral")
        emotion_score = getattr(left, "emotion_score", 0.0)
        
        for skill in skills:
            skill_lower = skill.lower()
            
            # 愤怒/悲伤时禁止冷分析
            cold_skills = ["search", "analysis", "report"]
            if emotion_type in ["anger", "sadness", "fear", "hidden_pain"]:
                if emotion_score >= 0.6:
                    if any(cold in skill_lower for cold in cold_skills):
                        blocked.append(BlockedAction(
                            action_type="skill",
                            target=skill,
                            reason=f"{emotion_type}情绪禁止冷分析技能",
                            suggested_alternative="先进行情感支持"
                        ))
            
            # 深夜禁止提醒
            hour = context.get("hour", 12)
            reminder_skills = ["reminder", "cron", "alarm"]
            if hour >= 22 or hour < 7:
                if any(r in skill_lower for r in reminder_skills):
                    blocked.append(BlockedAction(
                        action_type="skill",
                        target=skill,
                        reason="深夜时段禁止设置提醒",
                        suggested_alternative="延迟到早上8点"
                    ))
        
        return blocked
    
    def _modify_plan(
        self,
        plan: Any,
        corrections: List[Correction],
        blocked: List[BlockedAction]
    ) -> Any:
        """
        修改执行计划以反映纠偏结果
        """
        if not plan:
            return plan
        
        from prefrontal.executor import ExecutionPlan
        
        # 如果有被阻止的记忆，移除
        blocked_targets = {b.target for b in blocked if b.action_type == "memory"}
        original_memory = getattr(plan, "memory_to_mention", [])
        new_memory = [m for m in original_memory if str(m)[:30] not in blocked_targets]
        
        # 如果有被阻止的技能，移除
        blocked_skills = {b.target for b in blocked if b.action_type == "skill"}
        original_skills = getattr(plan, "skills_to_call", [])
        new_skills = [s for s in original_skills if s not in blocked_skills]
        
        return ExecutionPlan(
            response_style=getattr(plan, "response_style", "balanced"),
            should_mention_memory=bool(new_memory),
            memory_to_mention=new_memory[:2],  # 最多2条
            should_use_empathy=getattr(plan, "should_use_empathy", True),
            empathy_phrases=getattr(plan, "empathy_phrases", []),
            tasks_to_execute=getattr(plan, "tasks_to_execute", []),
            skills_to_call=new_skills,
            tone_modifier=getattr(plan, "tone_modifier", "natural"),
            pacing=getattr(plan, "pacing", "deliberate")
        )
    
    def get_conflict_history(self) -> List[float]:
        """获取冲突历史"""
        return self._conflict_history.copy()


# ============ 单例 ============
_monitor_instance: Optional[Monitor] = None

def get_instance() -> Monitor:
    global _monitor_instance
    if _monitor_instance is None:
        _monitor_instance = Monitor()
    return _monitor_instance


def monitor(
    executor_output: Any,
    all_outputs: Dict,
    context: Dict = None
) -> MonitorOutput:
    """快捷监控"""
    return get_instance().monitor(executor_output, all_outputs, context)


# ============ 测试 ============
if __name__ == "__main__":
    monitor = PrefrontalMonitor()
    
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
    class MockExecutor:
        base_weights: Any
        execution_plan: Any
        strategy_type: str
    
    @dataclass
    class MockLeft:
        emotion_score: float
        emotion_type: str
        is_masked: bool
    
    @dataclass
    class MockRight:
        intent_type: str
    
    print("=== 监控层测试 ===\n")
    
    # 测试1: 高情绪伪装
    executor = MockExecutor(
        base_weights=MockWeights(0.3, 0.5, 0.2),
        execution_plan=MockPlan("logical", True, ["上次你说的..."], False, [], [], "precise", "quick"),
        strategy_type="pure_logic"
    )
    left = MockLeft(0.8, "hidden_pain", True)
    right = MockRight("question")
    
    result = monitor.monitor(executor, {"left": left, "right": right, "executor": executor}, {"emotion_score": 0.8})
    print(f"【高情绪伪装成提问】")
    print(f"  冲突系数: {result.conflict_score:.2f}")
    print(f"  纠偏数: {len(result.corrections)}")
    print(f"  阻止动作: {len(result.blocked_actions)}")
    print(f"  接管日志: {result.override_log}")
    if result.corrections:
        for c in result.corrections:
            print(f"    {c.field}: {c.original_value} → {c.corrected_value} ({c.reason})")
    print()

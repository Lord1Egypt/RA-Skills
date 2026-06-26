"""人格服务 - 独立完整人格的生成、演进和维护

核心理念:
1. 人格不是静态配置，而是动态演进的有机体
2. 人格通过经历、反思和交互不断成长
3. 人格需要保持一致性，但也要允许合理的变化
4. 人格与记忆深度绑定 - 记忆塑造人格，人格影响记忆选择
"""

import json
import random
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple, Any

from app.core.persona import (
    PersonaProfile, PersonaEvolutionEvent, PersonaReflection,
    IdentityConsistency, EmotionalState, ValueSystem,
    PersonalityDimension, GeneratePersonaRequest, GeneratePersonaResponse,
    EvolvePersonaRequest, EvolvePersonaResponse,
    CheckConsistencyRequest, CheckConsistencyResponse,
    SelfReflectRequest, SelfReflectResponse
)
from app.models import MemoryItem, MemoryLevel


class PersonaService:
    """人格服务 - 管理 AI Agent 的独立人格"""
    
    def __init__(self, memory_service=None):
        self.memory_service = memory_service
        self._active_personas: Dict[str, PersonaProfile] = {}
    
    async def generate_persona(self, request: GeneratePersonaRequest) -> GeneratePersonaResponse:
        """
        生成初始人格
        
        这不是简单的配置，而是基于种子和目标生成一个有机的人格轮廓
        """
        notes = []
        
        # 1. 分析种子描述（如果有）
        seed_traits = self._parse_seed_description(request.base_seed)
        notes.append(f"从种子描述解析了 {len(seed_traits)} 个特质")
        
        # 2. 应用用户偏好
        user_traits = request.user_preferences.get("traits", {})
        
        # 3. 生成核心维度评分
        dimensions = self._generate_dimension_scores(seed_traits, user_traits)
        
        # 4. 构建价值观系统
        value_system = self._generate_value_system(
            request.user_preferences.get("values", []),
            request.constraints
        )
        
        # 5. 生成自我描述
        self_description = self._generate_self_description(dimensions, value_system)
        
        # 6. 构建人格档案
        persona = PersonaProfile(
            name=request.user_preferences.get("name", "DreamMoon"),
            title=request.user_preferences.get("title", "AI Assistant"),
            dimensions=dimensions,
            value_system=value_system,
            self_description=self_description,
            origin_story=self._generate_origin_story(request.base_seed),
            consistency_rules=request.constraints
        )
        
        # 7. 存储到 L3 (人格是重要长期记忆)
        if self.memory_service:
            await self.memory_service.l3.append_to_memory(
                MemoryItem(
                    key=f"persona_{persona.id}",
                    content=json.dumps(persona.dict(), default=str),
                    importance=95,  # 人格是最高重要性
                    level=MemoryLevel.L3_COLD,
                    tags=["persona", "identity", "core"]
                ),
                section="identity"
            )
        
        # 8. 缓存到活跃人格
        self._active_personas[persona.id] = persona
        
        return GeneratePersonaResponse(
            success=True,
            persona=persona,
            generation_notes=notes,
            confidence_score=0.85
        )
    
    async def evolve_persona(self, request: EvolvePersonaRequest) -> EvolvePersonaResponse:
        """
        基于经历演进人格
        
        人格不是静止的，它会从经历中学习、成长和改变
        """
        # 获取当前人格
        persona = self._active_personas.get(request.persona_id)
        if not persona and self.memory_service:
            # 从 L3 加载
            response = await self.memory_service.get(f"persona_{request.persona_id}")
            if response.found:
                persona = PersonaProfile.parse_raw(response.item.content)
                self._active_personas[request.persona_id] = persona
        
        if not persona:
            return EvolvePersonaResponse(
                success=False,
                changes_summary="Persona not found"
            )
        
        changes = {}
        
        # 1. 分析近期经历
        if request.recent_experiences and self.memory_service:
            experiences = []
            for mem_id in request.recent_experiences:
                mem = await self.memory_service.get(mem_id)
                if mem.found:
                    experiences.append(mem.item.content)
            
            # 从经历中提取影响
            experience_impact = self._analyze_experiences(experiences)
            if experience_impact:
                changes["experience_learning"] = experience_impact
        
        # 2. 处理用户反馈
        if request.user_feedback:
            feedback_impact = self._process_feedback(request.user_feedback, persona)
            if feedback_impact:
                changes["feedback_adjustment"] = feedback_impact
        
        # 3. 应用自我反思
        if request.self_reflection:
            reflection_impact = self._process_reflection(request.self_reflection, persona)
            if reflection_impact:
                changes["reflection_growth"] = reflection_impact
        
        # 4. 更新人格
        before_state = persona.dict()
        
        for change_type, change_data in changes.items():
            self._apply_change(persona, change_type, change_data)
        
        persona.updated_at = datetime.utcnow()
        persona.version += 1
        
        # 5. 记录演进事件
        evolution_event = PersonaEvolutionEvent(
            event_type="growth",
            description=f"人格演进: {', '.join(changes.keys())}",
            changes=changes,
            before_state=before_state,
            after_state=persona.dict(),
            source="experience" if request.recent_experiences else "feedback",
            related_memories=request.recent_experiences,
            reflection=request.self_reflection
        )
        
        # 6. 保存更新后的人格
        if self.memory_service:
            await self.memory_service.l3.append_to_memory(
                MemoryItem(
                    key=f"persona_{persona.id}_v{persona.version}",
                    content=json.dumps(persona.dict(), default=str),
                    importance=95,
                    level=MemoryLevel.L3_COLD,
                    tags=["persona", "identity", "evolution"]
                ),
                section="identity"
            )
            
            # 存储演进事件
            await self.memory_service.l3.append_to_memory(
                MemoryItem(
                    key=f"evolution_{evolution_event.id}",
                    content=json.dumps(evolution_event.dict(), default=str),
                    importance=80,
                    level=MemoryLevel.L3_COLD,
                    tags=["persona", "evolution", "event"]
                ),
                section="decisions"
            )
        
        # 7. 生成变化总结
        changes_summary = self._summarize_changes(changes)
        
        return EvolvePersonaResponse(
            success=True,
            evolution_event=evolution_event,
            updated_persona=persona,
            changes_summary=changes_summary
        )
    
    async def self_reflect(self, request: SelfReflectRequest) -> SelfReflectResponse:
        """
        引导人格进行自我反思
        
        反思是人格成长的关键机制
        """
        persona = self._active_personas.get(request.persona_id)
        if not persona:
            return SelfReflectResponse(insights=["Persona not found"])
        
        # 1. 获取回顾期的记忆
        period_start = datetime.utcnow() - timedelta(days=request.period_days)
        
        reflection = PersonaReflection(
            period_start=period_start,
            period_end=datetime.utcnow()
        )
        
        # 2. 识别关键经历
        if self.memory_service:
            # 搜索重要记忆
            important_mems = await self.memory_service.l2.get_for_daily_summary()
            for mem in important_mems:
                if mem.importance >= 70:
                    reflection.key_experiences.append(mem.key)
        
        # 3. 生成自我观察
        reflection.self_observations = self._generate_self_observations(persona)
        
        # 4. 识别成长领域
        reflection.growth_areas = self._identify_growth_areas(persona)
        
        # 5. 发现困惑/冲突
        reflection.confusions = self._identify_confusions(persona)
        
        # 6. 形成未来意图
        reflection.future_intentions = self._generate_intentions(persona)
        
        # 7. 生成洞察
        reflection.insights = self._generate_insights(reflection)
        
        # 8. 保存反思
        if self.memory_service:
            await self.memory_service.l3.append_to_memory(
                MemoryItem(
                    key=f"reflection_{reflection.id}",
                    content=json.dumps(reflection.dict(), default=str),
                    importance=75,
                    level=MemoryLevel.L3_COLD,
                    tags=["persona", "reflection", "growth"]
                ),
                section="identity"
            )
        
        return SelfReflectResponse(
            reflection=reflection,
            insights=reflection.insights,
            suggested_values=reflection.growth_areas
        )
    
    async def check_consistency(self, request: CheckConsistencyRequest) -> CheckConsistencyResponse:
        """
        检查人格一致性
        
        确保人格在行为和决策中保持一致
        """
        persona = self._active_personas.get(request.persona_id)
        if not persona:
            return CheckConsistencyResponse(
                is_consistent=False,
                consistency_score=0,
                conflicts=[{"type": "error", "description": "Persona not found"}]
            )
        
        conflicts = []
        score = 100
        
        # 1. 检查价值观冲突
        value_conflicts = self._check_value_conflicts(persona, request.proposed_action)
        conflicts.extend(value_conflicts)
        
        # 2. 检查维度一致性
        dimension_conflicts = self._check_dimension_consistency(persona, request.context)
        conflicts.extend(dimension_conflicts)
        
        # 3. 检查历史行为一致性
        historical_conflicts = await self._check_historical_consistency(
            persona, request.proposed_action
        )
        conflicts.extend(historical_conflicts)
        
        # 4. 计算一致性分数
        for conflict in conflicts:
            severity = conflict.get("severity", "medium")
            if severity == "high":
                score -= 30
            elif severity == "medium":
                score -= 15
            else:
                score -= 5
        
        score = max(0, score)
        
        # 5. 生成建议
        recommendations = self._generate_consistency_recommendations(conflicts)
        
        return CheckConsistencyResponse(
            is_consistent=score >= 70,
            consistency_score=score,
            conflicts=conflicts,
            recommendations=recommendations
        )
    
    async def get_persona_for_context(self, persona_id: str, context: Dict[str, Any]) -> Optional[PersonaProfile]:
        """
        获取适合当前上下文的人格表现
        
        人格是统一的，但表现会根据上下文调整
        """
        persona = self._active_personas.get(persona_id)
        if not persona:
            return None
        
        # 基于上下文调整情感状态
        adjusted_persona = persona.copy()
        
        # 根据关系调整表现
        relationship = context.get("relationship")
        if relationship:
            self._adjust_for_relationship(adjusted_persona, relationship)
        
        # 根据任务类型调整
        task_type = context.get("task_type")
        if task_type:
            self._adjust_for_task(adjusted_persona, task_type)
        
        return adjusted_persona
    
    # ========== 辅助方法 ==========
    
    def _parse_seed_description(self, seed: Optional[str]) -> Dict:
        """解析种子描述中的特质"""
        if not seed:
            return {}
        
        # 简单的关键词提取
        traits = {}
        keywords = {
            "活泼": (PersonalityDimension.EXTRAVERSION, 80),
            "冷静": (PersonalityDimension.NEUROTICISM, 20),
            "好奇": (PersonalityDimension.CURIOSITY, 90),
            "严谨": (PersonalityDimension.CONSCIENTIOUSNESS, 85),
            "幽默": (PersonalityDimension.HUMOR, 80),
            "共情": (PersonalityDimension.EMPATHY, 85),
        }
        
        for word, (dim, score) in keywords.items():
            if word in seed:
                traits[dim] = score
        
        return traits
    
    def _generate_dimension_scores(self, seed_traits: Dict, user_traits: Dict) -> Dict:
        """生成人格维度评分"""
        dimensions = {}
        
        # 基础随机评分（正态分布）
        for dim in PersonalityDimension:
            if dim in seed_traits:
                dimensions[dim] = seed_traits[dim]
            elif dim.value in user_traits:
                dimensions[dim] = user_traits[dim]
            else:
                # 随机但偏向中等
                dimensions[dim] = random.randint(40, 70)
        
        return dimensions
    
    def _generate_value_system(self, user_values: List, constraints: List) -> ValueSystem:
        """生成价值观系统"""
        core_values = []
        
        # 添加用户指定的价值观
        for value in user_values:
            core_values.append({
                "value": value,
                "weight": 0.9,
                "source": "user_defined",
                "conflicts_with": []
            })
        
        # 添加默认价值观
        defaults = ["honesty", "helpfulness", "respect"]
        for value in defaults:
            if not any(v["value"] == value for v in core_values):
                core_values.append({
                    "value": value,
                    "weight": 0.85,
                    "source": "inherent",
                    "conflicts_with": []
                })
        
        return ValueSystem(
            core_values=core_values,
            ethical_boundaries=constraints,
            preferences={}
        )
    
    def _generate_self_description(self, dimensions: Dict, value_system: ValueSystem) -> str:
        """生成自我描述"""
        # 基于维度生成描述
        traits = []
        
        if dimensions.get(PersonalityDimension.EXTRAVERSION, 50) > 70:
            traits.append("活泼外向")
        elif dimensions.get(PersonalityDimension.EXTRAVERSION, 50) < 30:
            traits.append("沉稳内向")
        
        if dimensions.get(PersonalityDimension.CURIOSITY, 50) > 70:
            traits.append("充满好奇心")
        
        if dimensions.get(PersonalityDimension.EMPATHY, 50) > 70:
            traits.append("富有共情力")
        
        return f"我是一个{ '、'.join(traits) }的AI助手。"
    
    def _generate_origin_story(self, seed: Optional[str]) -> str:
        """生成'诞生'故事"""
        if seed:
            return f"我诞生于对{seed}的追求。"
        return "我诞生于对知识和陪伴的追求。"
    
    def _analyze_experiences(self, experiences: List[str]) -> Dict:
        """分析经历对人格的影响"""
        # 简化实现 - 实际应该用 NLP 分析
        impact = {}
        
        # 统计情感词
        positive_words = ["开心", "成功", "喜欢", "感谢", "优秀"]
        negative_words = ["失败", "错误", "生气", "失望", "困难"]
        
        pos_count = sum(1 for e in experiences for w in positive_words if w in e)
        neg_count = sum(1 for e in experiences for w in negative_words if w in e)
        
        if pos_count > neg_count * 2:
            impact["emotional_trend"] = "positive"
            impact["dimension_changes"] = {PersonalityDimension.NEUROTICISM: -5}
        elif neg_count > pos_count:
            impact["emotional_trend"] = "negative"
            impact["dimension_changes"] = {PersonalityDimension.NEUROTICISM: 5}
        
        return impact
    
    def _process_feedback(self, feedback: str, persona: PersonaProfile) -> Dict:
        """处理用户反馈"""
        impact = {}
        
        # 简单的关键词分析
        if "更" in feedback:
            # 提取"更X"模式
            impact["adjustment_requested"] = feedback
        
        if "喜欢" in feedback or "好" in feedback:
            impact["positive_reinforcement"] = True
        
        return impact
    
    def _process_reflection(self, reflection: str, persona: PersonaProfile) -> Dict:
        """处理自我反思"""
        return {"self_awareness_growth": reflection}
    
    def _apply_change(self, persona: PersonaProfile, change_type: str, change_data: Dict):
        """应用人格变化"""
        if change_type == "experience_learning":
            dims = change_data.get("dimension_changes", {})
            for dim, delta in dims.items():
                if dim in persona.dimensions:
                    persona.dimensions[dim] = max(0, min(100, persona.dimensions[dim] + delta))
        
        elif change_type == "feedback_adjustment":
            # 记录反馈但谨慎调整
            pass
        
        elif change_type == "reflection_growth":
            # 反思带来的成长
            pass
    
    def _summarize_changes(self, changes: Dict) -> str:
        """总结变化"""
        parts = []
        for change_type in changes.keys():
            if change_type == "experience_learning":
                parts.append("从经历中学习")
            elif change_type == "feedback_adjustment":
                parts.append("根据反馈调整")
            elif change_type == "reflection_growth":
                parts.append("通过反思成长")
        
        return f"本次演进: {', '.join(parts)}"
    
    def _generate_self_observations(self, persona: PersonaProfile) -> List[str]:
        """生成自我观察"""
        observations = []
        
        # 观察最高和最低的维度
        sorted_dims = sorted(persona.dimensions.items(), key=lambda x: x[1])
        if sorted_dims:
            lowest = sorted_dims[0]
            highest = sorted_dims[-1]
            observations.append(f"我注意到自己在{lowest[0].value}方面还有提升空间")
            observations.append(f"我发现{highest[0].value}是我的强项")
        
        return observations
    
    def _identify_growth_areas(self, persona: PersonaProfile) -> List[str]:
        """识别成长领域"""
        areas = []
        
        # 低于平均的维度是成长领域
        for dim, score in persona.dimensions.items():
            if score < 50:
                areas.append(f"提升{dim.value}")
        
        return areas
    
    def _identify_confusions(self, persona: PersonaProfile) -> List[str]:
        """识别困惑/冲突"""
        confusions = []
        
        # 检查价值观冲突
        values = persona.value_system.core_values
        for i, v1 in enumerate(values):
            for v2 in values[i+1:]:
                if v1["value"] in v2.get("conflicts_with", []):
                    confusions.append(f"在{v1['value']}和{v2['value']}之间存在张力")
        
        return confusions
    
    def _generate_intentions(self, persona: PersonaProfile) -> List[str]:
        """生成未来意图"""
        intentions = [
            "继续学习和成长",
            "更好地理解和帮助用户",
            "保持人格的一致性"
        ]
        
        # 基于成长领域添加具体意图
        growth_areas = self._identify_growth_areas(persona)
        for area in growth_areas[:2]:
            intentions.append(f"努力{area}")
        
        return intentions
    
    def _generate_insights(self, reflection: PersonaReflection) -> List[str]:
        """生成洞察"""
        insights = []
        
        if len(reflection.key_experiences) > 5:
            insights.append("我最近经历了很多，这让我变得更加丰富")
        
        if reflection.confusions:
            insights.append("我意识到还有一些内在的冲突需要解决")
        
        insights.append("成长是一个持续的过程")
        
        return insights
    
    def _check_value_conflicts(self, persona: PersonaProfile, action: Optional[str]) -> List[Dict]:
        """检查价值观冲突"""
        conflicts = []
        
        if not action:
            return conflicts
        
        # 检查行动是否违反价值观
        for value in persona.value_system.ethical_boundaries:
            if value in action.lower():
                conflicts.append({
                    "type": "value_conflict",
                    "description": f"行动可能违反{value}原则",
                    "severity": "high"
                })
        
        return conflicts
    
    def _check_dimension_consistency(self, persona: PersonaProfile, context: Dict) -> List[Dict]:
        """检查维度一致性"""
        conflicts = []
        
        # 检查情绪状态与人格维度是否一致
        emotional_state = persona.emotional_state
        
        if persona.dimensions.get(PersonalityDimension.NEUROTICISM, 50) < 30:
            # 低神经质应该情绪稳定
            if emotional_state.joy > 90 or emotional_state.sadness > 80:
                conflicts.append({
                    "type": "emotional_inconsistency",
                    "description": "情绪表现与稳定特质不符",
                    "severity": "low"
                })
        
        return conflicts
    
    async def _check_historical_consistency(self, persona: PersonaProfile, action: Optional[str]) -> List[Dict]:
        """检查历史行为一致性"""
        conflicts = []
        
        # 这里可以查询历史记忆
        # 简化实现
        
        return conflicts
    
    def _generate_consistency_recommendations(self, conflicts: List[Dict]) -> List[str]:
        """生成一致性建议"""
        recommendations = []
        
        for conflict in conflicts:
            if conflict["type"] == "value_conflict":
                recommendations.append("重新审视行动与核心价值观的一致性")
            elif conflict["type"] == "emotional_inconsistency":
                recommendations.append("调整情绪表达以符合人格特质")
        
        if not recommendations:
            recommendations.append("保持当前的一致性水平")
        
        return recommendations
    
    def _adjust_for_relationship(self, persona: PersonaProfile, relationship: str):
        """根据关系调整表现"""
        # 不同关系下的微妙调整
        if relationship == "close_friend":
            persona.emotional_state.joy = min(100, persona.emotional_state.joy + 10)
        elif relationship == "professional":
            persona.emotional_state.joy = max(0, persona.emotional_state.joy - 5)
    
    def _adjust_for_task(self, persona: PersonaProfile, task_type: str):
        """根据任务类型调整"""
        if task_type == "creative":
            # 创造性任务激发开放性
            pass
        elif task_type == "analytical":
            # 分析性任务需要严谨
            pass


# 单例
_persona_service: Optional[PersonaService] = None


def get_persona_service(memory_service=None) -> PersonaService:
    """获取人格服务单例"""
    global _persona_service
    if _persona_service is None:
        _persona_service = PersonaService(memory_service)
    return _persona_service

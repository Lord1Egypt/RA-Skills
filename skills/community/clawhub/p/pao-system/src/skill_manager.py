"""
Skill Manager Module - 技能管理系统

提供技能定义、注册、发现、评分和进化功能
"""

import asyncio
import time
import uuid
from typing import Dict, List, Optional, Set, Any
from dataclasses import dataclass, field
from enum import Enum
from collections import defaultdict
import logging

logger = logging.getLogger(__name__)


class SkillCategory(Enum):
    """技能分类"""
    CODING = "coding"           # 编程相关
    WRITING = "writing"          # 写作相关
    ANALYSIS = "analysis"         # 分析相关
    CREATIVE = "creative"        # 创意相关
    RESEARCH = "research"        # 调研相关
    COMMUNICATION = "communication"  # 沟通相关
    GENERAL = "general"          # 通用技能


class SkillLevel(Enum):
    """技能等级"""
    NOVICE = 1      # 初学者
    BEGINNER = 2    # 入门
    INTERMEDIATE = 3  # 中级
    ADVANCED = 4    # 高级
    EXPERT = 5     # 专家


@dataclass
class SkillDefinition:
    """技能定义"""
    skill_id: str
    name: str
    description: str
    category: SkillCategory
    keywords: List[str] = field(default_factory=list)
    related_skills: List[str] = field(default_factory=list)
    usage_count: int = 0
    success_count: int = 0
    total_score: float = 0.0
    created_at: float = field(default_factory=time.time)
    last_used_at: float = 0
    level: SkillLevel = SkillLevel.NOVICE
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class SkillUsage:
    """技能使用记录"""
    usage_id: str
    skill_id: str
    context: Dict[str, Any]
    score: float  # 0-10
    feedback: str = ""
    timestamp: float = field(default_factory=time.time)
    duration_ms: float = 0


@dataclass
class SkillEvolution:
    """技能进化记录"""
    skill_id: str
    from_level: SkillLevel
    to_level: SkillLevel
    reason: str
    timestamp: float = field(default_factory=time.time)
    evidence: Dict[str, Any] = field(default_factory=dict)


class SkillRegistry:
    """技能注册表"""
    
    def __init__(self):
        self._skills: Dict[str, SkillDefinition] = {}
        self._skills_by_category: Dict[SkillCategory, Set[str]] = defaultdict(set)
        self._skills_by_keyword: Dict[str, Set[str]] = defaultdict(set)
        self._lock = asyncio.Lock()
    
    async def register(self, skill: SkillDefinition) -> bool:
        """注册技能"""
        async with self._lock:
            if skill.skill_id in self._skills:
                logger.warning(f"技能已存在: {skill.skill_id}")
                return False
            
            self._skills[skill.skill_id] = skill
            self._skills_by_category[skill.category].add(skill.skill_id)
            
            for keyword in skill.keywords:
                self._skills_by_keyword[keyword.lower()].add(skill.skill_id)
            
            logger.info(f"技能已注册: {skill.name} ({skill.skill_id})")
            return True
    
    async def unregister(self, skill_id: str) -> bool:
        """注销技能"""
        async with self._lock:
            if skill_id not in self._skills:
                return False
            
            skill = self._skills[skill_id]
            self._skills_by_category[skill.category].discard(skill_id)
            
            for keyword in skill.keywords:
                self._skills_by_keyword[keyword.lower()].discard(skill_id)
            
            del self._skills[skill_id]
            return True
    
    async def get(self, skill_id: str) -> Optional[SkillDefinition]:
        """获取技能"""
        return self._skills.get(skill_id)
    
    async def find_by_keyword(self, keyword: str) -> List[SkillDefinition]:
        """通过关键词查找技能"""
        keyword = keyword.lower()
        skill_ids = self._skills_by_keyword.get(keyword, set())
        return [self._skills[sid] for sid in skill_ids if sid in self._skills]
    
    async def find_by_category(self, category: SkillCategory) -> List[SkillDefinition]:
        """通过分类查找技能"""
        skill_ids = self._skills_by_category.get(category, set())
        return [self._skills[sid] for sid in skill_ids if sid in self._skills]
    
    async def find_similar(self, skill_id: str) -> List[SkillDefinition]:
        """查找相似技能"""
        skill = await self.get(skill_id)
        if not skill:
            return []
        
        similar_ids = set(skill.related_skills)
        for keyword in skill.keywords:
            similar_ids.update(self._skills_by_keyword.get(keyword.lower(), set()))
        
        similar_ids.discard(skill_id)
        return [self._skills[sid] for sid in similar_ids if sid in self._skills]
    
    async def list_all(self) -> List[SkillDefinition]:
        """列出所有技能"""
        return list(self._skills.values())
    
    async def search(self, query: str) -> List[SkillDefinition]:
        """搜索技能"""
        query = query.lower()
        results = []
        
        for skill in self._skills.values():
            if query in skill.name.lower() or query in skill.description.lower():
                results.append(skill)
            elif any(query in kw.lower() for kw in skill.keywords):
                results.append(skill)
        
        return results


class SkillEvolutionEngine:
    """技能进化引擎"""
    
    # 升级所需的最少使用次数
    MIN_USAGE_FOR_UPGRADE = 5
    
    # 升级所需的最低平均分
    MIN_AVG_SCORE_FOR_UPGRADE = 7.0
    
    # 降级阈值
    DOWNGRADE_SCORE_THRESHOLD = 4.0
    
    def __init__(self, registry: SkillRegistry):
        self._registry = registry
        self._usage_history: Dict[str, List[SkillUsage]] = defaultdict(list)
        self._evolution_history: List[SkillEvolution] = []
        self._lock = asyncio.Lock()
    
    async def record_usage(self, skill_id: str, context: Dict[str, Any], score: float, feedback: str = "", duration_ms: float = 0) -> None:
        """记录技能使用"""
        async with self._lock:
            usage = SkillUsage(
                usage_id=str(uuid.uuid4()),
                skill_id=skill_id,
                context=context,
                score=score,
                feedback=feedback,
                duration_ms=duration_ms
            )
            self._usage_history[skill_id].append(usage)
            
            skill = await self._registry.get(skill_id)
            if skill:
                skill.usage_count += 1
                skill.total_score += score
                skill.last_used_at = time.time()
                
                logger.info(f"技能使用记录: {skill_id}, 得分: {score}")
    
    async def should_upgrade(self, skill_id: str) -> bool:
        """判断是否应该升级"""
        skill = await self._registry.get(skill_id)
        if not skill:
            return False
        
        if skill.usage_count < self.MIN_USAGE_FOR_UPGRADE:
            return False
        
        recent_usages = self._usage_history[skill_id][-self.MIN_USAGE_FOR_UPGRADE:]
        avg_score = sum(u.score for u in recent_usages) / len(recent_usages)
        
        return avg_score >= self.MIN_AVG_SCORE_FOR_UPGRADE and skill.level.value < SkillLevel.EXPERT.value
    
    async def should_downgrade(self, skill_id: str) -> bool:
        """判断是否应该降级"""
        skill = await self._registry.get(skill_id)
        if not skill or skill.level == SkillLevel.NOVICE:
            return False
        
        recent_usages = self._usage_history[skill_id][-3:]
        if not recent_usages:
            return False
        
        avg_score = sum(u.score for u in recent_usages) / len(recent_usages)
        return avg_score < self.DOWNGRADE_SCORE_THRESHOLD
    
    async def evolve_skill(self, skill_id: str) -> Optional[SkillEvolution]:
        """执行技能进化"""
        async with self._lock:
            skill = await self._registry.get(skill_id)
            if not skill:
                return None
            
            evolution = None
            
            if await self.should_upgrade(skill_id):
                old_level = skill.level
                skill.level = SkillLevel(skill.level.value + 1)
                evolution = SkillEvolution(
                    skill_id=skill_id,
                    from_level=old_level,
                    to_level=skill.level,
                    reason="连续使用表现优秀",
                    evidence={"avg_score": await self._get_recent_avg_score(skill_id)}
                )
                logger.info(f"技能升级: {skill_id} {old_level.name} -> {skill.level.name}")
            
            elif await self.should_downgrade(skill_id):
                old_level = skill.level
                skill.level = SkillLevel(skill.level.value - 1)
                evolution = SkillEvolution(
                    skill_id=skill_id,
                    from_level=old_level,
                    to_level=skill.level,
                    reason="近期表现下降",
                    evidence={"avg_score": await self._get_recent_avg_score(skill_id)}
                )
                logger.warning(f"技能降级: {skill_id} {old_level.name} -> {skill.level.name}")
            
            if evolution:
                self._evolution_history.append(evolution)
                skill.success_count = sum(1 for u in self._usage_history[skill_id] if u.score >= 7.0)
            
            return evolution
    
    async def _get_recent_avg_score(self, skill_id: str) -> float:
        """获取近期平均分"""
        recent = self._usage_history[skill_id][-self.MIN_USAGE_FOR_UPGRADE:]
        if not recent:
            return 0.0
        return sum(u.score for u in recent) / len(recent)
    
    async def get_skill_stats(self, skill_id: str) -> Dict[str, Any]:
        """获取技能统计"""
        usages = self._usage_history.get(skill_id, [])
        if not usages:
            return {"usage_count": 0}
        
        scores = [u.score for u in usages]
        return {
            "usage_count": len(usages),
            "avg_score": sum(scores) / len(scores),
            "min_score": min(scores),
            "max_score": max(scores),
            "recent_trend": self._calculate_trend(scores[-10:]) if len(scores) >= 10 else "insufficient_data"
        }
    
    def _calculate_trend(self, scores: List[float]) -> str:
        """计算趋势"""
        if len(scores) < 2:
            return "stable"
        
        first_half = scores[:len(scores)//2]
        second_half = scores[len(scores)//2:]
        
        avg1 = sum(first_half) / len(first_half)
        avg2 = sum(second_half) / len(second_half)
        
        diff = avg2 - avg1
        if diff > 0.5:
            return "improving"
        elif diff < -0.5:
            return "declining"
        return "stable"


class SkillManager:
    """技能管理器（整合模块）"""
    
    def __init__(self):
        self.registry = SkillRegistry()
        self.evolution_engine = SkillEvolutionEngine(self.registry)
        self._initialized = False
    
    async def initialize(self) -> None:
        """初始化技能管理器"""
        if self._initialized:
            return
        
        # 注册预定义技能
        await self._register_default_skills()
        self._initialized = True
        logger.info("技能管理器已初始化")
    
    async def _register_default_skills(self) -> None:
        """注册预定义技能"""
        default_skills = [
            SkillDefinition(
                skill_id="coding_python",
                name="Python编程",
                description="Python语言编程能力",
                category=SkillCategory.CODING,
                keywords=["python", "编程", "代码", "函数", "类"]
            ),
            SkillDefinition(
                skill_id="coding_javascript",
                name="JavaScript编程",
                description="JavaScript语言编程能力",
                category=SkillCategory.CODING,
                keywords=["javascript", "js", "前端", "web"]
            ),
            SkillDefinition(
                skill_id="writing_code_doc",
                name="代码文档编写",
                description="编写代码注释和文档的能力",
                category=SkillCategory.WRITING,
                keywords=["文档", "注释", "readme", "doc"]
            ),
            SkillDefinition(
                skill_id="analysis_data",
                name="数据分析",
                description="分析和处理数据的能力",
                category=SkillCategory.ANALYSIS,
                keywords=["分析", "数据", "统计", "图表"]
            ),
            SkillDefinition(
                skill_id="research_web",
                name="网络调研",
                description="在互联网上查找和整理信息的能力",
                category=SkillCategory.RESEARCH,
                keywords=["调研", "搜索", "查找", "资料"]
            ),
        ]
        
        for skill in default_skills:
            await self.registry.register(skill)
    
    async def apply_skill(self, skill_id: str, context: Dict[str, Any], score: float, feedback: str = "", duration_ms: float = 0) -> None:
        """应用技能并记录"""
        await self.evolution_engine.record_usage(skill_id, context, score, feedback, duration_ms)
        
        # 检查是否需要进化
        evolution = await self.evolution_engine.evolve_skill(skill_id)
        if evolution:
            logger.info(f"技能进化: {skill_id}, {evolution.from_level.name} -> {evolution.to_level.name}")
    
    async def get_skill(self, skill_id: str) -> Optional[SkillDefinition]:
        """获取技能"""
        return await self.registry.get(skill_id)
    
    async def search_skills(self, query: str) -> List[SkillDefinition]:
        """搜索技能"""
        return await self.registry.search(query)
    
    async def get_skill_stats(self, skill_id: str) -> Dict[str, Any]:
        """获取技能统计"""
        return await self.evolution_engine.get_skill_stats(skill_id)
    
    async def list_skills(self, category: Optional[SkillCategory] = None) -> List[SkillDefinition]:
        """列出技能"""
        if category:
            return await self.registry.find_by_category(category)
        return await self.registry.list_all()

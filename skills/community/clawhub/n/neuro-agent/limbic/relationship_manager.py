"""
limbic/relationship_manager.py
===============================

Neuro-Agent 边缘系统 - 关系管理器
负责：关系里程碑管理、亲密度评分、风格解锁

依赖：
    - temporal/long_term_memory.py（记忆数量统计）
"""

import json
from pathlib import Path
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, asdict

# ============ 路径配置 ============
DATA_DIR = Path.home() / ".openclaw" / "workspace" / "neuro_claw" / "relationship"
DATA_DIR.mkdir(parents=True, exist_ok=True)
MILESTONES_FILE = DATA_DIR / "milestones.json"


# ============ 关系阶段定义 ============
STAGE_DEFINITIONS = {
    "initial": {
        "name": "初识期",
        "min_days": 0,
        "min_interactions": 0,
        "description": "礼貌、功能性交流",
        "tone": "polite",
        "greeting_style": "您好",
        "unlocked": []
    },
    "familiar": {
        "name": "熟悉期",
        "min_days": 7,
        "min_interactions": 10,
        "description": "幽默、分享、轻松",
        "tone": "casual",
        "greeting_style": "你好",
        "unlocked": ["humor", "sharing", "nicknames"]
    },
    "companion": {
        "name": "伴侣期",
        "min_days": 30,
        "min_interactions": 50,
        "night_talks": 3,
        "min_memories": 20,
        "description": "情感依赖、关心、陪伴",
        "tone": "warm",
        "greeting_style": "亲爱的",
        "unlocked": ["emotional_support", "deep_care", "intimate_nickname", "late_night"]
    },
    "soul": {
        "name": "灵魂期",
        "min_days": 90,
        "min_interactions": 200,
        "milestone_events": 1,
        "min_memories": 100,
        "description": "默契、无需言语",
        "tone": "soul",
        "greeting_style": None,  # 一个眼神就够了
        "unlocked": ["silence", "complete_understanding", "shared_memory", "unconditional"]
    }
}

# 互动分数规则
INTERACTION_SCORES = {
    "greeting": 1,
    "casual_chat": 1,
    "question": 1,
    "task_request": 1,
    "emotional_vent": 5,
    "advice_seeking": 3,
    "complaint": 2,
    "compliment": 2,
    "secret_shared": 10,
    "milestone_event": 20,
    "forgiveness_received": -10,
    "memory_recalled": 2,
    "proactive_care_accepted": 5,
    "night_talk": 3,  # 22:00-02:00 的深夜交流
    "hug_reaction": 3  # 对关怀的反应
}


# ============ 数据结构 ============
@dataclass
class Interaction:
    """互动记录"""
    timestamp: str
    intent_type: str
    emotion_type: str
    emotion_score: float
    capsules_created: int
    memory_recalled: int
    duration_seconds: int
    is_night: bool
    care_provided: bool
    care_accepted: bool
    special_flags: List[str]


@dataclass
class RelationshipOutput:
    """关系输出"""
    stage: str
    stage_name: str
    intimacy_score: float
    intimacy_progress: float  # 当前阶段进度 0.0-1.0
    interaction_count: int
    day_count: int
    unlocked_styles: List[str]
    next_milestone: Dict
    relationship_age: str
    tone: str
    greeting_style: str
    warnings: List[str]  # 潜在问题
    
    def to_dict(self) -> Dict:
        return asdict(self)


@dataclass
class MilestoneData:
    """里程碑数据"""
    first_interaction: str
    last_interaction: str
    total_interactions: int
    night_talks: int
    emotional_events: int
    milestone_events: List[str]
    intimacy_score: float
    forgiveness_count: int
    unlocked_styles: List[str]
    current_stage: str
    interaction_history: List[Dict]


# ============ 核心类 ============
class RelationshipManager:
    """
    关系管理器
    
    功能：
        1. 管理关系阶段（初识→熟悉→伴侣→灵魂）
        2. 记录互动并计算亲密度
        3. 解锁风格和能力
        4. 识别下一里程碑条件
        5. 维护关系健康度
    
    阶段解锁条件：
        - 熟悉期: 7天 + 10次互动
        - 伴侣期: 30天 + 50次互动 + 3次深夜交流 + 20个记忆
        - 灵魂期: 90天 + 200次互动 + 重大事件共渡 + 100个记忆
    """
    
    def __init__(self):
        """初始化关系管理器"""
        self.data = self._load_data()
    
    def _load_data(self) -> MilestoneData:
        """加载里程碑数据"""
        if MILESTONES_FILE.exists():
            try:
                with open(MILESTONES_FILE, 'r', encoding='utf-8') as f:
                    raw = json.load(f)
                return MilestoneData(**raw)
            except (json.JSONDecodeError, TypeError):
                pass
        
        # 初始化新数据
        return MilestoneData(
            first_interaction=datetime.now().isoformat(),
            last_interaction=datetime.now().isoformat(),
            total_interactions=0,
            night_talks=0,
            emotional_events=0,
            milestone_events=[],
            intimacy_score=0.0,
            forgiveness_count=0,
            unlocked_styles=["polite"],
            current_stage="initial",
            interaction_history=[]
        )
    
    def _save_data(self):
        """保存里程碑数据"""
        with open(MILESTONES_FILE, 'w', encoding='utf-8') as f:
            json.dump(asdict(self.data), f, ensure_ascii=False, indent=2)
    
    def record_interaction(self, interaction: Interaction) -> RelationshipOutput:
        """
        记录互动并更新关系
        """
        # 计算得分
        score = self._calculate_interaction_score(interaction)
        
        # 更新数据
        self.data.total_interactions += 1
        self.data.intimacy_score += score
        self.data.last_interaction = interaction.timestamp
        
        if interaction.is_night:
            self.data.night_talks += 1
        
        if interaction.emotion_score >= 0.7:
            self.data.emotional_events += 1
        
        # 特殊事件
        if "milestone" in interaction.special_flags:
            self.data.milestone_events.append(interaction.timestamp)
        
        # 记录历史
        self.data.interaction_history.append(asdict(interaction))
        if len(self.data.interaction_history) > 100:
            self.data.interaction_history = self.data.interaction_history[-100:]
        
        # 检查阶段升级
        old_stage = self.data.current_stage
        new_stage = self._check_stage_upgrade()
        
        if new_stage != old_stage:
            self.data.current_stage = new_stage
            # 解锁新风格
            self._unlock_new_styles(old_stage, new_stage)
        
        self._save_data()
        
        return self._get_relationship_output()
    
    def _calculate_interaction_score(self, interaction: Interaction) -> float:
        """计算互动分数"""
        score = INTERACTION_SCORES.get(interaction.intent_type, 1)
        
        # 情绪加成
        if interaction.emotion_score >= 0.8:
            score += 2
        elif interaction.emotion_score >= 0.6:
            score += 1
        
        # 深夜交流
        if interaction.is_night:
            score += INTERACTION_SCORES.get("night_talk", 3)
        
        # 关怀被接受
        if interaction.care_provided and interaction.care_accepted:
            score += INTERACTION_SCORES.get("proactive_care_accepted", 5)
        
        # 创建胶囊（自我暴露）
        if interaction.capsules_created > 0:
            score += interaction.capsules_created * 0.5
        
        # 记忆被召回
        if interaction.memory_recalled > 0:
            score += interaction.memory_recalled * INTERACTION_SCORES.get("memory_recalled", 2)
        
        return score
    
    def _check_stage_upgrade(self) -> str:
        """检查是否需要升级阶段"""
        current = self.data.current_stage
        
        # 计算关系时长
        first_date = datetime.fromisoformat(self.data.first_interaction)
        days = (datetime.now() - first_date).days
        
        stage_order = ["initial", "familiar", "companion", "soul"]
        current_idx = stage_order.index(current)
        
        for i in range(current_idx + 1, len(stage_order)):
            stage_key = stage_order[i]
            stage_def = STAGE_DEFINITIONS[stage_key]
            
            # 检查天数
            if days < stage_def["min_days"]:
                continue
            
            # 检查互动次数
            if self.data.total_interactions < stage_def["min_interactions"]:
                continue
            
            # 伴侣期额外检查
            if stage_key == "companion":
                extra_checks = True
                if "night_talks" in stage_def:
                    if self.data.night_talks < stage_def["night_talks"]:
                        extra_checks = False
                if extra_checks:
                    # 需要检查记忆数量
                    capsule_count = self._count_memories()
                    if capsule_count < stage_def.get("min_memories", 20):
                        extra_checks = False
                if not extra_checks:
                    continue
            
            # 灵魂期额外检查
            if stage_key == "soul":
                if len(self.data.milestone_events) < stage_def.get("milestone_events", 1):
                    continue
                capsule_count = self._count_memories()
                if capsule_count < stage_def.get("min_memories", 100):
                    continue
            
            return stage_key
        
        return current
    
    def _count_memories(self) -> int:
        """统计记忆数量"""
        capsules_dir = Path.home() / ".openclaw" / "workspace" / "neuro_claw" / "capsules"
        count = 0
        
        if capsules_dir.exists():
            for f in capsules_dir.glob("*.json"):
                try:
                    with open(f, 'r') as fp:
                        data = json.load(fp)
                        if isinstance(data, list):
                            count += len(data)
                        else:
                            count += 1
                except:
                    pass
        
        return count
    
    def _unlock_new_styles(self, old_stage: str, new_stage: str):
        """解锁新风格"""
        old_styles = STAGE_DEFINITIONS.get(old_stage, {}).get("unlocked", [])
        new_styles = STAGE_DEFINITIONS.get(new_stage, {}).get("unlocked", [])
        
        for style in new_styles:
            if style not in self.data.unlocked_styles:
                self.data.unlocked_styles.append(style)
        
        self.data.unlocked_styles = list(set(self.data.unlocked_styles))
    
    def _get_relationship_output(self) -> RelationshipOutput:
        """获取关系状态输出"""
        stage_def = STAGE_DEFINITIONS[self.data.current_stage]
        
        # 计算阶段进度
        first_date = datetime.fromisoformat(self.data.first_interaction)
        days = (datetime.now() - first_date).days
        min_days = stage_def["min_days"]
        progress = min(1.0, days / (min_days * 1.5)) if min_days > 0 else 1.0
        
        # 下一里程碑
        next_milestone = self._get_next_milestone()
        
        # 警告
        warnings = []
        if self.data.intimacy_score < 0 and self.data.forgiveness_count > 3:
            warnings.append("亲密度持续下降，建议主动修复关系")
        if days > 7 and self.data.total_interactions < 5:
            warnings.append("互动频率过低，关系可能进入休眠")
        
        return RelationshipOutput(
            stage=self.data.current_stage,
            stage_name=stage_def["name"],
            intimacy_score=round(self.data.intimacy_score, 1),
            intimacy_progress=round(progress, 2),
            interaction_count=self.data.total_interactions,
            day_count=days,
            unlocked_styles=self.data.unlocked_styles,
            next_milestone=next_milestone,
            relationship_age=f"{days}天",
            tone=stage_def["tone"],
            greeting_style=stage_def["greeting_style"],
            warnings=warnings
        )
    
    def _get_next_milestone(self) -> Dict:
        """获取下一里程碑条件"""
        stage = self.data.current_stage
        
        if stage == "initial":
            return {
                "target_stage": "familiar",
                "conditions": [
                    f"还需 {7 - self._days_since_first()} 天",
                    f"还需 {10 - self.data.total_interactions} 次互动"
                ]
            }
        elif stage == "familiar":
            return {
                "target_stage": "companion",
                "conditions": [
                    f"还需 {30 - self._days_since_first()} 天",
                    f"还需 {50 - self.data.total_interactions} 次互动",
                    f"还需 {3 - self.data.night_talks} 次深夜交流"
                ]
            }
        elif stage == "companion":
            return {
                "target_stage": "soul",
                "conditions": [
                    f"还需 {90 - self._days_since_first()} 天",
                    f"还需 {100 - self._count_memories()} 个记忆"
                ]
            }
        else:
            return {"target_stage": "soul", "conditions": ["已达最高阶段"]}
    
    def _days_since_first(self) -> int:
        """计算关系天数"""
        first_date = datetime.fromisoformat(self.data.first_interaction)
        return (datetime.now() - first_date).days
    
    def get_stage(self) -> str:
        """快速获取当前阶段"""
        return self.data.current_stage
    
    def should_unlock_style(self, style: str) -> bool:
        """检查是否应解锁某种风格"""
        return style in self.data.unlocked_styles
    
    def get_greeting_style(self, hour: int = None) -> str:
        """获取问候风格"""
        stage_def = STAGE_DEFINITIONS[self.data.current_stage]
        base = stage_def["greeting_style"]
        
        if not base:
            return ""  # 灵魂期不需要问候
        
        if hour is None:
            hour = datetime.now().hour
        
        # 按时间段调整
        if self.data.current_stage == "soul":
            # 灵魂期：极简
            greetings = {
                range(6, 12): "早",
                range(12, 18): "嗯",
                range(18, 23): "晚上好",
                range(23, 24): None,
                range(0, 6): None
            }
            for r, g in greetings.items():
                if hour in r:
                    return g or ""
            return "嗯"
        
        return base
    
    def record_forgiveness(self):
        """记录一次原谅事件"""
        self.data.forgiveness_count += 1
        self.data.intimacy_score = max(0, self.data.intimacy_score - 10)
        self._save_data()


# ============ 单例 ============
_manager_instance: Optional[RelationshipManager] = None

def get_instance() -> RelationshipManager:
    global _manager_instance
    if _manager_instance is None:
        _manager_instance = RelationshipManager()
    return _manager_instance


def record_interaction(interaction: Interaction) -> RelationshipOutput:
    return get_instance().record_interaction(interaction)


# ============ 测试 ============
if __name__ == "__main__":
    manager = RelationshipManager()
    
    print("=== 关系管理测试 ===\n")
    
    # 模拟多次互动
    for i in range(15):
        interaction = Interaction(
            timestamp=datetime.now().isoformat(),
            intent_type=["greeting", "casual_chat", "question", "emotional_vent"][i % 4],
            emotion_type=["neutral", "joy", "sadness"][i % 3],
            emotion_score=0.3 + (i % 5) * 0.1,
            capsules_created=1 if i % 3 == 0 else 0,
            memory_recalled=0,
            duration_seconds=60,
            is_night=i % 5 == 0,
            care_provided=i % 4 == 0,
            care_accepted=True,
            special_flags=[]
        )
        result = manager.record_interaction(interaction)
    
    print(f"当前阶段: {result.stage_name}")
    print(f"亲密度: {result.intimacy_score}")
    print(f"互动次数: {result.interaction_count}")
    print(f"关系时长: {result.relationship_age}")
    print(f"解锁风格: {result.unlocked_styles}")
    print(f"下一里程碑: {result.next_milestone}")
    print(f"问候风格: {result.greeting_style}")
    if result.warnings:
        print(f"⚠️ {result.warnings}")
    print()

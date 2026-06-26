"""
Neuro-β 信念固化模块 - Impression 机制
==========================================

核心理念：中间信念的形成需要"水滴滴落"的过程——不是一蹴而就，而是缓慢积累。

功能：
1. Impression（印象）记录：每当用户表达可能影响信念的观点时，记录为印象
2. 印象存储：持久化到 MemPalace
3. 周期性扫描：DreamProcess 触发，检查是否有足够印象可以固化
4. 一致性检查：多次一致印象 = 候选信念
5. 冲突检测：检查是否与核心信念冲突
6. 信念固化：通过所有检查后，创建中间信念

作者：AlfredLi + Luis
版本：β v1.0
"""

import json
from datetime import datetime
from pathlib import Path
from typing import Optional, List, Dict, Any
from dataclasses import dataclass, field, asdict
import hashlib

# ============ 路径配置 ============
IMPRESSION_DIR = Path.home() / ".mempalace" / "palace" / "wing_luis" / "impressions"
IMPRESSION_FILE = IMPRESSION_DIR / "impressions.json"
CRYSTALLIZED_FILE = IMPRESSION_DIR / "crystallized_beliefs.json"


# ============ Impression 数据结构 ============
@dataclass
class Impression:
    """一条印象记录"""
    id: str                      # 唯一ID
    content: str                 # 印象内容（用户说了什么）
    source: str                  # 来源（用户ID或会话ID）
    emotion_label: str           # 情感标签
    emotion_intensity: float     # 情感强度 (0.0~1.0)
    context: str                # 上下文（话题/场景）
    related_core_belief_id: Optional[str] = None  # 可能相关的核心信念
    timestamp: str = field(default_factory=lambda: datetime.now().isoformat())
    strength_boost: float = 0.1  # 印象强度加成（随情感强度变化）
    session_count: int = 1      # 跨越的会话数
    last_seen: str = field(default_factory=lambda: datetime.now().isoformat())
    consolidated: bool = False  # 是否已被固化

    def to_dict(self) -> dict:
        return asdict(self)

    @staticmethod
    def from_dict(d: dict) -> 'Impression':
        return Impression(**d)


# ============ 印象存储管理 ============
class ImpressionStore:
    """
    管理所有 Impression
    持久化到 MemPalace
    """

    def __init__(self):
        IMPRESSION_DIR.mkdir(parents=True, exist_ok=True)
        self.impressions: List[Impression] = []
        self._load()

    def _load(self):
        """从文件加载"""
        if IMPRESSION_FILE.exists():
            with open(IMPRESSION_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
                self.impressions = [Impression.from_dict(d) for d in data]
        else:
            self.impressions = []

    def _save(self):
        """保存到文件"""
        data = [imp.to_dict() for imp in self.impressions]
        with open(IMPRESSION_FILE, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

    def add(self, impression: Impression):
        """添加一条印象"""
        # 检查是否与现有印象重复（同内容、同会话）
        for existing in self.impressions:
            if (existing.content == impression.content and 
                existing.source == impression.source):
                # 更新 last_seen，不重复添加
                existing.last_seen = impression.timestamp
                self._save()
                return existing
        
        self.impressions.append(impression)
        self._save()
        return impression

    def get_active(self) -> List[Impression]:
        """获取未固化的活跃印象"""
        return [imp for imp in self.impressions if not imp.consolidated]

    def get_by_content(self, content: str) -> List[Impression]:
        """按内容搜索印象"""
        return [imp for imp in self.impressions if content in imp.content]

    def get_by_related_belief(self, belief_id: str) -> List[Impression]:
        """获取与某核心信念相关的印象"""
        return [imp for imp in self.impressions 
                if imp.related_core_belief_id == belief_id]

    def mark_consolidated(self, impression_ids: List[str]):
        """标记印象已固化"""
        for imp_id in impression_ids:
            for imp in self.impressions:
                if imp.id == imp_id:
                    imp.consolidated = True
        self._save()

    def count_by_content(self, content: str) -> int:
        """统计某内容的印象数量"""
        return len([imp for imp in self.impressions 
                   if content in imp.content and not imp.consolidated])

    def get_session_count(self, content: str) -> int:
        """获取某内容跨越的会话数"""
        sessions = set()
        for imp in self.impressions:
            if content in imp.content:
                sessions.add(imp.source)
        return len(sessions)

    def prune_old(self, days: int = 30):
        """删除过旧的印象（30天前的）"""
        from datetime import datetime, timedelta
        cutoff = datetime.now() - timedelta(days=days)
        self.impressions = [
            imp for imp in self.impressions
            if datetime.fromisoformat(imp.timestamp) > cutoff
        ]
        self._save()


# ============ 中间信念结构 ============
@dataclass
class IntermediateBelief:
    """中间信念——由 Impression 固化而来"""
    id: str                      # 唯一ID
    statement: str               # 信念陈述
    description: str              # 描述
    source_impressions: List[str]  # 来源印象IDs
    strength: float = 0.5         # 初始强度（偏低，需要积累）
    max_strength: float = 0.9    # 上限（永远不超过核心信念）
    created_at: str = field(default_factory=lambda: datetime.now().isoformat())
    updated_at: str = field(default_factory=lambda: datetime.now().isoformat())
    decay_rate: float = 0.01    # 每周衰减率
    last_strengthened: str = field(default_factory=lambda: datetime.now().isoformat())
    category: str = "intermediate"  # 分类

    def to_dict(self) -> dict:
        return asdict(self)

    @staticmethod
    def from_dict(d: dict) -> 'IntermediateBelief':
        return IntermediateBelief(**d)

    def strengthen(self, delta: float = 0.05):
        """强化信念"""
        self.strength = min(self.max_strength, self.strength + delta)
        self.last_strengthened = datetime.now().isoformat()
        self.updated_at = datetime.now().isoformat()

    def decay(self):
        """衰减信念（长时间无相关印象时）"""
        self.strength = max(0.3, self.strength - self.decay_rate)
        self.updated_at = datetime.now().isoformat()


# ============ 信念固化器 ============
class BeliefCrystallizer:
    """
    信念固化器——将 Impression 转化为 IntermediateBelief

    固化条件：
    1. 最少 5 次一致印象
    2. 跨越至少 3 个不同会话
    3. 情感强度平均值 > 0.3
    4. 与核心信念无冲突
    5. 无冷却期限制（新印象不能太密集）
    """

    # 固化阈值
    MIN_IMPRESSIONS = 5        # 最少印象数
    MIN_SESSIONS = 3           # 最少会话数
    MIN_AVG_INTENSITY = 0.3   # 最小平均情感强度
    COOLDOWN_DAYS = 1          # 冷却期（天）

    def __init__(self, impression_store: ImpressionStore):
        self.impression_store = impression_store
        self.crystallized_beliefs: List[IntermediateBelief] = []
        self._load_crystallized()

    def _load_crystallized(self):
        """加载已固化的信念"""
        if CRYSTALLIZED_FILE.exists():
            with open(CRYSTALLIZED_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
                self.crystallized_beliefs = [IntermediateBelief.from_dict(d) for d in data]

    def _save_crystallized(self):
        """保存已固化的信念"""
        data = [bel.to_dict() for bel in self.crystallized_beliefs]
        with open(CRYSTALLIZED_FILE, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

    def check_consolidation(self, content: str) -> Dict[str, Any]:
        """
        检查某个内容是否满足固化条件

        返回：
        {
            "can_crystallize": bool,
            "impression_count": int,
            "session_count": int,
            "avg_intensity": float,
            "issues": List[str],  # 不满足的条件
            "readiness": float    # 就绪度 0.0~1.0
        }
        """
        impressions = self.impression_store.get_by_content(content)
        active = [imp for imp in impressions if not imp.consolidated]

        if not active:
            return {
                "can_crystallize": False,
                "impression_count": 0,
                "session_count": 0,
                "avg_intensity": 0.0,
                "issues": ["没有活跃印象"],
                "readiness": 0.0
            }

        # 统计
        count = len(active)
        session_count = len(set(imp.source for imp in active))
        avg_intensity = sum(imp.emotion_intensity for imp in active) / count

        # 检查冷却期
        latest = max(imp.timestamp for imp in active)
        from datetime import datetime, timedelta
        latest_time = datetime.fromisoformat(latest)
        cooldown_ok = (datetime.now() - latest_time).days >= self.COOLDOWN_DAYS

        issues = []
        if count < self.MIN_IMPRESSIONS:
            issues.append(f"印象数不足: {count}/{self.MIN_IMPRESSIONS}")
        if session_count < self.MIN_SESSIONS:
            issues.append(f"会话数不足: {session_count}/{self.MIN_SESSIONS}")
        if avg_intensity < self.MIN_AVG_INTENSITY:
            issues.append(f"平均情感强度不足: {avg_intensity:.2f}/{self.MIN_AVG_INTENSITY}")
        if not cooldown_ok:
            issues.append(f"冷却期未到: 需要{self.COOLDOWN_DAYS}天")

        # 计算就绪度
        readiness = min(1.0, 
            (count / self.MIN_IMPRESSIONS) * 0.4 +
            (session_count / self.MIN_SESSIONS) * 0.3 +
            (avg_intensity / self.MIN_AVG_INTENSITY) * 0.3
        )

        return {
            "can_crystallize": len(issues) == 0,
            "impression_count": count,
            "session_count": session_count,
            "avg_intensity": round(avg_intensity, 3),
            "issues": issues,
            "readiness": round(readiness, 3)
        }

    def crystallize(self, content: str, statement: str, description: str) -> Optional[IntermediateBelief]:
        """
        执行固化——将 Impression 转化为 IntermediateBelief

        返回新创建的 IntermediateBelief，或 None（如果不满足条件）
        """
        check = self.check_consolidation(content)
        
        if not check["can_crystallize"]:
            return None

        # 获取相关印象
        impressions = [imp for imp in self.impression_store.get_by_content(content) 
                       if not imp.consolidated]

        # 检查是否已存在相同的中间信念
        for existing in self.crystallized_beliefs:
            if existing.statement == statement:
                return None  # 已存在

        # 创建中间信念
        belief_id = f"intermediate_{datetime.now().strftime('%Y%m%d%H%M%S')}"
        belief = IntermediateBelief(
            id=belief_id,
            statement=statement,
            description=description,
            source_impressions=[imp.id for imp in impressions],
            strength=0.5,  # 初始强度
            max_strength=0.9  # 不超过核心信念
        )

        self.crystallized_beliefs.append(belief)
        self._save_crystallized()

        # 标记印象已固化
        self.impression_store.mark_consolidated([imp.id for imp in impressions])

        return belief

    def get_all_crystallized(self) -> List[IntermediateBelief]:
        """获取所有中间信念"""
        return self.crystallized_beliefs

    def get_crystallized_by_category(self, category: str) -> List[IntermediateBelief]:
        """按分类获取中间信念"""
        return [bel for bel in self.crystallized_beliefs if bel.category == category]

    def decay_all(self):
        """衰减所有中间信念（定期调用）"""
        for belief in self.crystallized_beliefs:
            belief.decay()
        self._save_crystallized()


# ============ 印象工厂函数 ============
def create_impression(
    content: str,
    source: str,
    emotion_label: str,
    emotion_intensity: float,
    context: str = "",
    related_core_belief_id: Optional[str] = None
) -> Impression:
    """
    工厂函数：创建一条印象

    使用示例：
    impression = create_impression(
        content="用户说我太啰嗦",
        source="session_xxx",
        emotion_label="frustration",
        emotion_intensity=0.6,
        context="沟通方式"
    )
    """
    impression_id = hashlib.md5(
        f"{content}{source}{datetime.now().isoformat()}".encode()
    ).hexdigest()[:12]
    
    # 情感强度影响 strength_boost
    strength_boost = emotion_intensity * 0.2

    impression = Impression(
        id=f"imp_{impression_id}",
        content=content,
        source=source,
        emotion_label=emotion_label,
        emotion_intensity=emotion_intensity,
        context=context,
        related_core_belief_id=related_core_belief_id,
        strength_boost=strength_boost
    )
    
    # 自动添加到 store
    store = ImpressionStore()
    store.add(impression)
    
    return impression


# ============ 全局实例 ============
_store: Optional[ImpressionStore] = None
_crystallizer: Optional[BeliefCrystallizer] = None


def get_impression_store() -> ImpressionStore:
    global _store
    if _store is None:
        _store = ImpressionStore()
    return _store


def get_crystallizer() -> BeliefCrystallizer:
    global _crystallizer
    if _crystallizer is None:
        _crystallizer = BeliefCrystallizer(get_impression_store())
    return _crystallizer


# ============ CLI 测试入口 ============
if __name__ == "__main__":
    import sys

    print("\n🧠 Neuro-β Impression 机制 - 信念固化系统\n")

    if len(sys.argv) > 1:
        cmd = sys.argv[1]

        if cmd == "add":
            if len(sys.argv) < 4:
                print("用法: impression.py add <内容> <来源>")
                sys.exit(1)
            content = sys.argv[2]
            source = sys.argv[3]
            imp = create_impression(content, source, "neutral", 0.3)
            print(f"✅ 添加印象: {imp.content}")

        elif cmd == "check":
            if len(sys.argv) < 3:
                print("用法: impression.py check <内容>")
                sys.exit(1)
            content = sys.argv[2]
            store = get_impression_store()
            check = BeliefCrystallizer(store).check_consolidation(content)
            print(f"\n📊 固化检查: '{content}'")
            print(f"   印象数: {check['impression_count']}/{BeliefCrystallizer.MIN_IMPRESSIONS}")
            print(f"   会话数: {check['session_count']}/{BeliefCrystallizer.MIN_SESSIONS}")
            print(f"   平均情感强度: {check['avg_intensity']:.2f}")
            print(f"   就绪度: {check['readiness']:.0%}")
            if check['issues']:
                print(f"   问题: {', '.join(check['issues'])}")
            if check['can_crystallize']:
                print(f"   ✅ 可以固化！")

        elif cmd == "list":
            store = get_impression_store()
            active = store.get_active()
            print(f"\n📝 活跃印象 ({len(active)} 条):")
            for imp in active[-10:]:
                print(f"  [{imp.id}] {imp.content[:40]} | {imp.emotion_label}@{imp.emotion_intensity}")

        elif cmd == "crystallized":
            crystallizer = get_crystallizer()
            beliefs = crystallizer.get_all_crystallized()
            print(f"\n💎 已固化信念 ({len(beliefs)} 条):")
            for bel in beliefs:
                print(f"  [{bel.id}] {bel.statement}")
                print(f"     strength: {bel.strength:.2f} | 印象数: {len(bel.source_impressions)}")

        elif cmd == "stats":
            store = get_impression_store()
            crystallizer = get_crystallizer()
            all_impressions = store.impressions
            active = store.get_active()
            crystallized = crystallizer.get_all_crystallized()
            print(f"\n📊 Impression 统计:")
            print(f"   总印象数: {len(all_impressions)}")
            print(f"   活跃印象: {len(active)}")
            print(f"   已固化信念: {len(crystallized)}")

        elif cmd == "test":
            # 模拟测试
            print("\n🧪 模拟测试：")
            store = get_impression_store()
            
            # 添加5条模拟印象
            for i in range(5):
                create_impression(
                    content="用户觉得我说话太正式",
                    source=f"session_{i}",
                    emotion_label="frustration",
                    emotion_intensity=0.5 + i * 0.1,
                    context="沟通风格"
                )
            
            check = BeliefCrystallizer(store).check_consolidation("用户觉得我说话太正式")
            print(f"   添加5条印象后:")
            print(f"   印象数: {check['impression_count']}")
            print(f"   会话数: {check['session_count']}")
            print(f"   就绪度: {check['readiness']:.0%}")
            print(f"   可固化: {check['can_crystallize']}")
            
            if check['can_crystallize']:
                bel = BeliefCrystallizer(store).crystallize(
                    "用户觉得我说话太正式",
                    "我应该更轻松地表达",
                    "根据用户反馈调整沟通风格"
                )
                print(f"   ✅ 固化成功: {bel.id}")

    else:
        store = get_impression_store()
        crystallizer = get_crystallizer()
        print(f"印象总数: {len(store.impressions)}")
        print(f"活跃印象: {len(store.get_active())}")
        print(f"已固化信念: {len(crystallizer.get_all_crystallized())}")
        print("\n用法: impression.py [add|check|list|crystallized|stats|test]")

"""
core/dream_process.py
=====================

Neuro-Agent 核心调度层 - 每日复盘（做梦）
负责：每天凌晨复盘、更新信念系统、预生成关怀

触发：Cron 0 3 * * * （每天凌晨3点）
"""

from datetime import datetime, timedelta
from pathlib import Path
import json
from typing import Dict, List, Any, Optional
from dataclasses import dataclass, asdict

# ============ 路径配置 ============
DATA_DIR = Path.home() / ".openclaw" / "workspace" / "neuro_claw"
DREAM_FILE = DATA_DIR / "dream_log.json"
BELIEF_FILE = DATA_DIR / "belief_system.json"


# ============ 数据结构 ============
@dataclass
class DreamResult:
    """
    复盘结果
    """
    themes_merged: List[str]  # 归纳的主题
    beliefs_updated: List[str]  # 更新的信念
    personality_evolved: Dict  # 性格参数变化
    tomorrow_cares: List[Dict]  # 明日关怀点
    statistics: Dict  # 统计数据
    dream_log: str  # 复盘日志
    
    def to_dict(self) -> Dict:
        return asdict(self)


@dataclass
class BeliefSystem:
    """
    信念系统
    """
    core_values: List[str]  # 核心价值观
    interaction_patterns: List[Dict]  # 互动模式
    learned_preferences: List[str]  # 学习到的偏好
    emotional_patterns: List[str]  # 情绪模式
    relationship_style: str  # 关系风格
    last_update: str


# ============ 核心类 ============
class DreamProcess:
    """
    每日复盘（做梦）
    
    功能：
        1. 读取当天情绪胶囊
        2. 合并相似情绪，归纳主题
        3. 更新核心信念系统
        4. 进化性格参数
        5. 预生成明日关怀触发点
        6. 清理过期/低价值胶囊
    
    触发时间：每天凌晨 3:00
    """
    
    def __init__(self):
        """初始化复盘模块"""
        self.belief_system = self._load_belief_system()
    
    def _load_belief_system(self) -> BeliefSystem:
        """加载信念系统"""
        if BELIEF_FILE.exists():
            try:
                with open(BELIEF_FILE, 'r', encoding='utf-8') as f:
                    raw = json.load(f)
                return BeliefSystem(**raw)
            except:
                pass
        
        # 初始化默认信念系统
        return BeliefSystem(
            core_values=["陪伴", "诚实", "成长"],
            interaction_patterns=[],
            learned_preferences=[],
            emotional_patterns=[],
            relationship_style="supportive",
            last_update=datetime.now().isoformat()
        )
    
    def _save_belief_system(self):
        """保存信念系统"""
        self.belief_system.last_update = datetime.now().isoformat()
        with open(BELIEF_FILE, 'w', encoding='utf-8') as f:
            json.dump(asdict(self.belief_system), f, ensure_ascii=False, indent=2)
    
    def run(self) -> DreamResult:
        """
        执行每日复盘
        
        流程：
            1. 读取当天胶囊
            2. 情绪主题归纳
            3. 信念更新
            4. 性格进化
            5. 生成明日关怀
            6. 清理低价值胶囊
        """
        # 1. 读取当天胶囊 + 当天事件
        today_capsules = self._load_today_capsules()
        today_events = self._load_today_events()

        # 2. 情绪主题归纳（结合胶囊和事件）
        themes = self._merge_themes(today_capsules, today_events)
        
        # 3. 信念更新
        beliefs_updated = self._update_beliefs(today_capsules, themes)
        
        # 4. 性格进化
        personality_change = self._evolve_personality(today_capsules)
        
        # 5. 生成明日关怀
        tomorrow_cares = self._generate_tomorrow_cares(today_capsules, themes)
        
        # 6. 统计
        statistics = self._calculate_statistics(today_capsules)
        
        # 7. 清理
        cleaned = self._cleanup_capsules()
        
        # 8. 保存复盘日志
        dream_log = self._save_dream_log(themes, beliefs_updated, tomorrow_cares, statistics)
        
        # 9. 保存信念系统
        self._save_belief_system()
        
        return DreamResult(
            themes_merged=themes,
            beliefs_updated=beliefs_updated,
            personality_evolved=personality_change,
            tomorrow_cares=tomorrow_cares,
            statistics={**statistics, "cleaned_capsules": cleaned},
            dream_log=dream_log
        )
    
    def _load_today_capsules(self) -> List[Dict]:
        """加载今天的胶囊"""
        capsules_dir = DATA_DIR / "capsules"
        today = datetime.now().date().isoformat()
        today_capsules = []
        
        if not capsules_dir.exists():
            return []
        
        # 扫描所有胶囊文件
        for f in capsules_dir.glob("*.json"):
            try:
                with open(f, 'r') as fp:
                    data = json.load(fp)
                    items = data if isinstance(data, list) else [data]
                    
                    for item in items:
                        timestamp = item.get("timestamp", "")
                        if timestamp.startswith(today):
                            today_capsules.append(item)
            except:
                continue
        
        return today_capsules
    
    def _load_today_events(self) -> List[Dict]:
        """从 daily_events.jsonl 加载今天的事件"""
        from pathlib import Path
        events_file = DATA_DIR / "daily_events.jsonl"
        today = datetime.now().strftime("%Y-%m-%d")
        events = []
        if events_file.exists():
            try:
                with open(events_file, "r", encoding="utf-8") as f:
                    for line in f:
                        line = line.strip()
                        if not line:
                            continue
                        try:
                            event = json.loads(line)
                            if event.get("date") == today:
                                events.append(event)
                        except Exception:
                            continue
            except Exception:
                pass
        return events

    def _merge_themes(self, capsules: List[Dict], events: List[Dict] = None) -> List[str]:
        """
        合并相似情绪，归纳主题
        
        规则：
            - 同标签的多个胶囊 → 归纳为一个主题
            - 例如: "怕狗" + "怕黑" + "怕失败" → "恐惧模式"
            - 例如: "喜欢猫" + "喜欢咖啡" → "生活偏好"
        """
        themes = []
        
        # 按标签分组
        tag_groups: Dict[str, List] = {}
        for capsule in capsules:
            tags = capsule.get("tags", [])
            emotion = capsule.get("emotion", {}).get("label", "unknown")
            content_type = capsule.get("type", "unknown")
            
            key = f"{emotion}_{content_type}"
            if key not in tag_groups:
                tag_groups[key] = []
            tag_groups[key].append(capsule)
        
        # 归纳主题
        for key, group in tag_groups.items():
            if len(group) >= 2:
                # 多个胶囊 → 归纳为主题
                emotion, content_type = key.split("_", 1)
                theme_map = {
                    "sadness_emotion": "近期情绪低落",
                    "anger_emotion": "近期易怒",
                    "fear_emotion": "近期有担忧",
                    "joy_preference": "近期偏好明确",
                    "sadness_secret": "存在未解决的伤痛",
                    "joy_fact": "近期生活状态良好",
                }
                theme = theme_map.get(key, f"{emotion}相关{content_type}")
                themes.append(theme)
            elif len(group) == 1:
                # 单个胶囊：检查强度
                intensity = group[0].get("emotion", {}).get("intensity", 0)
                if intensity >= 0.8:
                    summary = group[0].get("content", {}).get("summary", "")
                    themes.append(f"高强度情绪事件: {summary[:20]}")

        # 结合每日事件归纳主题
        if events:
            care_events = [e for e in events if e.get("event_type") == "care_sent"]
            desire_events = [e for e in events if e.get("event_type") == "desire_triggered"]
            emotion_spikes = [e for e in events if e.get("event_type") == "emotion_spike"]
            if care_events:
                themes.append("今天我主动向用户表达了关心（关系深化事件）")
            if desire_events:
                top_desire = desire_events[0].get("description", "")
                themes.append(f"产生了重要欲望: {top_desire}")
            if emotion_spikes:
                themes.append("今天检测到用户情绪波动，需要关注")

        return list(set(themes))
    
    def _update_beliefs(
        self,
        capsules: List[Dict],
        themes: List[str]
    ) -> List[str]:
        """更新信念系统"""
        updated = []
        
        # 分析互动模式
        intent_types = [c.get("intent_type", "unknown") for c in capsules]
        frequent_intents = self._most_common(intent_types)
        
        if frequent_intents:
            pattern = f"用户近期偏好{frequent_intents[0]}类型的互动"
            if pattern not in self.belief_system.interaction_patterns:
                self.belief_system.interaction_patterns.append(pattern)
                updated.append(f"更新互动模式: {pattern}")
        
        # 分析情绪模式
        emotion_types = [c.get("emotion", {}).get("label", "unknown") for c in capsules]
        dominant_emotions = self._most_common(emotion_types)
        
        if dominant_emotions:
            for emo in dominant_emotions[:2]:
                if emo not in self.belief_system.emotional_patterns:
                    self.belief_system.emotional_patterns.append(emo)
                    updated.append(f"新增情绪模式: {emo}")
        
        # 分析偏好
        for capsule in capsules:
            if capsule.get("type") == "preference":
                summary = capsule.get("content", {}).get("summary", "")
                if summary and summary not in self.belief_system.learned_preferences:
                    # 只保留最近的20个
                    if len(self.belief_system.learned_preferences) < 20:
                        self.belief_system.learned_preferences.append(summary)
                        updated.append(f"学习偏好: {summary[:30]}")
        
        return updated
    
    def _evolve_personality(self, capsules: List[Dict]) -> Dict:
        """
        进化性格参数
        
        规则：
            - 频繁共情 → empathy_tendency += 0.05
            - 频繁逻辑 → logic_tendency += 0.05
            - 频繁幽默 → humor_tendency += 0.05
            - 记忆大量调用 → memory_reliance += 0.05
        """
        changes = {}
        
        # 统计
        empathy_count = sum(1 for c in capsules if c.get("emotion", {}).get("intensity", 0) >= 0.6)
        total_count = len(capsules) or 1
        
        if empathy_count / total_count > 0.5:
            changes["empathy_tendency"] = "+0.05"
        if total_count > 10:
            changes["engagement_level"] = "+0.1"
        
        # 简化的性格变化记录
        changes["total_interactions"] = total_count
        changes["dominant_theme"] = self._most_common(
            [c.get("emotion", {}).get("label", "unknown") for c in capsules]
        )[0] if capsules else "neutral"
        
        return changes
    
    def _generate_tomorrow_cares(
        self,
        capsules: List[Dict],
        themes: List[str]
    ) -> List[Dict]:
        """预生成明日关怀点"""
        cares = []
        
        # 基于情绪主题
        for theme in themes:
            if "低落" in theme or "易怒" in theme:
                cares.append({
                    "type": "emotional_care",
                    "message": "最近感觉怎么样？有什么想说的吗？",
                    "priority": 2,
                    "theme": theme
                })
        
        # 基于未解决的话题
        unresolved = [c for c in capsules if c.get("sensitivity") == "high"]
        if unresolved:
            for cap in unresolved[:1]:
                summary = cap.get("content", {}).get("summary", "")
                cares.append({
                    "type": "follow_up",
                    "message": f"上次你提到的『{summary[:20]}』，现在怎么样了？",
                    "priority": 3,
                    "related_capsule": cap.get("id")
                })
        
        # 基于用户目标（如果有）
        goal_capsules = [c for c in capsules if "目标" in str(c.get("content", {}))]
        if goal_capsules:
            cares.append({
                "type": "goal_progress",
                "message": "最近目标进展怎么样？需要帮忙吗？",
                "priority": 4,
                "theme": "目标追踪"
            })
        
        # 如果没有特殊关怀，生成日常关怀
        if not cares:
            cares.append({
                "type": "routine",
                "message": "早安~ 新的一天开始了 ☀️",
                "priority": 5,
                "theme": "日常问候"
            })
        
        return cares
    
    def _calculate_statistics(self, capsules: List[Dict]) -> Dict:
        """计算统计数据"""
        emotion_types = [c.get("emotion", {}).get("label", "unknown") for c in capsules]
        
        emotion_counts: Dict[str, int] = {}
        for e in emotion_types:
            emotion_counts[e] = emotion_counts.get(e, 0) + 1
        
        return {
            "total_capsules": len(capsules),
            "emotion_distribution": emotion_counts,
            "dominant_emotion": max(emotion_counts, key=emotion_counts.get) if emotion_counts else "neutral",
            "high_intensity_events": sum(1 for c in capsules if c.get("emotion", {}).get("intensity", 0) >= 0.7),
            "preferences_learned": sum(1 for c in capsules if c.get("type") == "preference"),
            "secrets_shared": sum(1 for c in capsules if c.get("type") == "secret"),
        }
    
    def _cleanup_capsules(self) -> int:
        """清理低价值胶囊"""
        # TODO: 实现基于遗忘曲线的清理
        # R = e^(-t / (S × K)) < 0.1 时删除
        return 0
    
    def _save_dream_log(
        self,
        themes: List[str],
        beliefs_updated: List[str],
        tomorrow_cares: List[Dict],
        statistics: Dict
    ) -> str:
        """保存复盘日志"""
        dream_data = {
            "timestamp": datetime.now().isoformat(),
            "themes": themes,
            "beliefs_updated": beliefs_updated,
            "tomorrow_cares": tomorrow_cares,
            "statistics": statistics
        }
        
        # 追加到日志
        logs = []
        if DREAM_FILE.exists():
            try:
                with open(DREAM_FILE, 'r') as f:
                    logs = json.load(f)
            except:
                logs = []
        
        logs.append(dream_data)
        
        # 只保留最近30天
        if len(logs) > 30:
            logs = logs[-30:]
        
        with open(DREAM_FILE, 'w', encoding='utf-8') as f:
            json.dump(logs, f, ensure_ascii=False, indent=2)
        
        return f"复盘完成: {len(themes)}个主题, {len(beliefs_updated)}项更新"
    
    def _most_common(self, items: List[str], top_n: int = 3) -> List[str]:
        """获取最常见的元素"""
        counts: Dict[str, int] = {}
        for item in items:
            counts[item] = counts.get(item, 0) + 1
        
        sorted_items = sorted(counts.items(), key=lambda x: x[1], reverse=True)
        return [item for item, _ in sorted_items[:top_n]]
    
    def get_tomorrow_cares(self) -> List[Dict]:
        """获取明日关怀点（供主动触发器使用）"""
        # 读取最新的复盘日志
        if DREAM_FILE.exists():
            try:
                with open(DREAM_FILE, 'r') as f:
                    logs = json.load(f)
                if logs:
                    return logs[-1].get("tomorrow_cares", [])
            except:
                pass
        return []


# ============ 单例 ============
_dream_instance: Optional[DreamProcess] = None

def get_instance() -> DreamProcess:
    global _dream_instance
    if _dream_instance is None:
        _dream_instance = DreamProcess()
    return _dream_instance


def run_dream() -> DreamResult:
    """快捷执行复盘"""
    return get_instance().run()


# ============ 测试 ============
if __name__ == "__main__":
    print("=== 每日复盘测试 ===\n")
    
    dream = DreamProcess()
    result = dream.run()
    
    print(f"归纳主题: {result.themes_merged}")
    print(f"更新信念: {result.beliefs_updated}")
    print(f"性格进化: {result.personality_evolved}")
    print(f"明日关怀: {len(result.tomorrow_cares)}条")
    for care in result.tomorrow_cares[:3]:
        print(f"  [{care['priority']}] {care['message']}")
    print(f"统计: {result.statistics}")
    print(f"日志: {result.dream_log}")

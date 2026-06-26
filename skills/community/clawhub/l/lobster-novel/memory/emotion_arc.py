#!/usr/bin/env python3
"""
lobster-novel: 情绪弧线追踪

记录主角/重要角色每章的情绪状态变化，
检测情绪断层，分析张力曲线。

情绪维度参考 Plutchik 情绪轮简化版:
  正面: 喜悦/信任/期待/惊喜
  负面: 悲伤/愤怒/恐惧/厌恶/焦虑
  中性: 平静/好奇/困惑
"""
import json
from pathlib import Path
from dataclasses import dataclass, field, asdict
from typing import List, Dict, Optional, Tuple
from datetime import datetime


# 情绪强度等级
EMOTION_INTENSITY = {
    "狂喜": 100, "喜悦": 75, "愉悦": 50, "平静": 25, "无聊": 10,
    "焦虑": 30, "恐惧": 60, "惊恐": 90,
    "愤怒": 60, "暴怒": 90, "不满": 30,
    "悲伤": 50, "悲痛": 80, "失落": 40,
    "期待": 40, "兴奋": 70, "紧张": 40,
    "惊喜": 55, "惊讶": 45, "震惊": 80,
    "困惑": 30, "迷茫": 40, "好奇": 35,
    "厌恶": 40, "憎恨": 70,
    "信任": 50, "怀疑": 30, "背叛感": 60,
}

# 情绪极性：positive / negative / neutral
EMOTION_POLARITY = {
    "狂喜": 1, "喜悦": 1, "愉悦": 1, "平静": 0, "无聊": -1,
    "焦虑": -1, "恐惧": -1, "惊恐": -1,
    "愤怒": -1, "暴怒": -1, "不满": -1,
    "悲伤": -1, "悲痛": -1, "失落": -1,
    "期待": 0.5, "兴奋": 1, "紧张": -0.5,
    "惊喜": 0.5, "惊讶": 0, "震惊": -0.5,
    "困惑": -0.3, "迷茫": -0.5, "好奇": 0.5,
    "厌恶": -1, "憎恨": -1,
    "信任": 0.8, "怀疑": -0.5, "背叛感": -1,
}


@dataclass
class EmotionSnapshot:
    """角色在某一章的情绪快照"""
    chapter: int
    character: str
    primary_emotion: str = "平静"
    secondary_emotion: str = ""
    intensity: int = 25              # 0-100
    polarity: float = 0.0            # -1 (负面) ~ +1 (正面)
    trigger: str = ""                # 触发事件简述
    scene_type: str = ""             # 战斗/日常/对话/转折/高潮
    notes: str = ""


class EmotionArcTracker:
    """情绪弧线追踪器"""

    FILE = "emotion_arc.json"

    def __init__(self, project_dir: Path):
        self.dir = Path(project_dir) / "continuity"
        self.dir.mkdir(parents=True, exist_ok=True)
        self.file = self.dir / self.FILE
        self.snapshots: List[EmotionSnapshot] = self._load()

    def _load(self) -> List[EmotionSnapshot]:
        if not self.file.exists():
            return []
        try:
            data = json.loads(self.file.read_text(encoding="utf-8"))
            return [EmotionSnapshot(**s) for s in data]
        except Exception:
            return []

    def save(self):
        self.file.write_text(
            json.dumps([asdict(s) for s in self.snapshots],
                       ensure_ascii=False, indent=2),
            encoding="utf-8")

    def record(self, snapshot: EmotionSnapshot):
        """记录一章的情绪状态"""
        # 覆盖同角色同章节的记录
        self.snapshots = [
            s for s in self.snapshots
            if not (s.character == snapshot.character and s.chapter == snapshot.chapter)
        ]
        # 自动填充极性和强度
        if snapshot.primary_emotion in EMOTION_INTENSITY:
            snapshot.intensity = EMOTION_INTENSITY[snapshot.primary_emotion]
        if snapshot.primary_emotion in EMOTION_POLARITY:
            snapshot.polarity = EMOTION_POLARITY[snapshot.primary_emotion]
        # 二级情绪的极性混合
        if snapshot.secondary_emotion and snapshot.secondary_emotion in EMOTION_POLARITY:
            sec_pol = EMOTION_POLARITY[snapshot.secondary_emotion]
            snapshot.polarity = (snapshot.polarity + sec_pol * 0.3) / 1.3

        self.snapshots.append(snapshot)
        self.save()

    def get_arc(self, character: str) -> List[EmotionSnapshot]:
        """获取某角色的完整情绪弧线"""
        return [s for s in self.snapshots if s.character == character]

    def get_state_at(self, character: str, chapter: int) -> Optional[EmotionSnapshot]:
        """获取某角色在某章的情绪"""
        entries = [s for s in self.snapshots
                   if s.character == character and s.chapter <= chapter]
        if not entries:
            return None
        return max(entries, key=lambda s: s.chapter)

    def detect_emotion_gap(self, character: str, max_gap: int = 3) -> List[Tuple[int, int]]:
        """检测情绪断层：角色连续N章无情绪记录"""
        arc = self.get_arc(character)
        if len(arc) < 2:
            return []
        gaps = []
        for i in range(len(arc) - 1):
            gap = arc[i + 1].chapter - arc[i].chapter
            if gap > max_gap:
                gaps.append((arc[i].chapter, arc[i + 1].chapter))
        return gaps

    def detect_flat_arc(self, character: str, window: int = 5) -> List[int]:
        """检测情绪过度平淡的章节（长时间无情绪变化）"""
        arc = self.get_arc(character)
        if len(arc) < window:
            return []
        flat = []
        for i in range(len(arc) - window + 1):
            window_snapshots = arc[i:i + window]
            polarities = [s.polarity for s in window_snapshots]
            if max(polarities) - min(polarities) < 0.5:
                for s in window_snapshots:
                    flat.append(s.chapter)
        return list(set(flat))

    def tension_curve(self, character: str) -> List[Tuple[int, float]]:
        """张力曲线：返回[(章节, 张力值)] 张力值=强度×|极性|"""
        arc = self.get_arc(character)
        return [(s.chapter, s.intensity * abs(s.polarity)) for s in arc]

    def summary(self, character: str) -> str:
        """情绪弧线摘要"""
        arc = self.get_arc(character)
        if not arc:
            return f"{character}暂无情绪记录"

        max_intensity = max(arc, key=lambda s: s.intensity)
        # 情绪变化次数
        changes = sum(
            1 for i in range(1, len(arc))
            if EMOTION_POLARITY.get(arc[i].primary_emotion, 0)
               != EMOTION_POLARITY.get(arc[i-1].primary_emotion, 0)
        )
        gaps = self.detect_emotion_gap(character)
        flat = self.detect_flat_arc(character)

        lines = [
            f"{character}情绪弧线 ({len(arc)}章记录)",
            f"  最强情绪: {max_intensity.primary_emotion}(强度{max_intensity.intensity}) @ 第{max_intensity.chapter}章",
            f"  情绪转换: {changes}次",
        ]
        if gaps:
            lines.append(f"  情绪断层: {len(gaps)}处")
        if flat:
            lines.append(f"  扁平区域: {len(flat)}章")
        lines.append(f"  张力曲线: {'→'.join(str(s[1]) for s in self.tension_curve(character)[:10])}")
        return "\n".join(lines)

    def dump(self) -> str:
        """全部情绪弧线"""
        chars = set(s.character for s in self.snapshots)
        parts = [f"情绪弧线共{len(self.snapshots)}条记录"]
        for c in sorted(chars):
            parts.append("\n" + self.summary(c))
        return "\n".join(parts)

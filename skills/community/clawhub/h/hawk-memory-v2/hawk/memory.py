"""
memory.py — 四层记忆管理器（Working/Short/Long/Archive）

功能：
- Working: 当前会话短期记忆
- Short: 近期重要记忆（带Weibull衰减）
- Long: 长期记忆（高价值）
- Archive: 归档（极少访问）
"""

import os
import time
import json
from dataclasses import dataclass, asdict
from typing import Optional
from pathlib import Path


@dataclass
class MemoryItem:
    id: str
    text: str
    category: str  # fact | preference | decision | entity | other
    importance: float  # 0.0-1.0
    access_count: int
    last_accessed: float
    created_at: float
    layer: str  # working | short | long | archive
    metadata: dict


class MemoryManager:
    """
    四层记忆管理器
    - store(text): 存入对应层
    - recall(query): 检索记忆
    - decay(): 触发衰减，更新层级
    """

    LAYERS = ['working', 'short', 'long', 'archive']
    LAYER_THRESHOLDS = {
        'working': 0,      # 始终在working
        'short': 3,        # 访问≥3次或importance≥0.6
        'long': 10,        # 访问≥10次或importance≥0.8
        'archive': 100,    # 长期休眠
    }
    DECAY_RATE = 0.95  # Weibull衰减率

    def __init__(self, db_path: str = "~/.hawk/memories.json"):
        self.db_path = os.path.expanduser(db_path)
        os.makedirs(os.path.dirname(self.db_path), exist_ok=True)
        self.memories: dict[str, MemoryItem] = {}
        self._load()

    def _load(self):
        if os.path.exists(self.db_path):
            with open(self.db_path) as f:
                data = json.load(f)
                for k, v in data.items():
                    self.memories[k] = MemoryItem(**v)

    def _save(self):
        with open(self.db_path, 'w') as f:
            json.dump({k: asdict(v) for k, v in self.memories.items()}, f, ensure_ascii=False)

    def store(self, text: str, category: str = "other", importance: float = 0.5, metadata: dict = None) -> str:
        """存入记忆，自动判断层级"""
        import hashlib
        id = hashlib.sha256(f"{text[:100]}{time.time()}".encode()).hexdigest()[:16]
        now = time.time()
        layer = self._compute_layer(importance, 0)
        item = MemoryItem(
            id=id, text=text, category=category,
            importance=importance, access_count=0,
            last_accessed=now, created_at=now,
            layer=layer, metadata=metadata or {}
        )
        self.memories[id] = item
        self._save()
        return id

    def recall(self, query: str, top_k: int = 5) -> list[MemoryItem]:
        """简单关键词检索记忆（配合VectorRetriever做语义检索）"""
        query_lower = query.lower()
        scored = []
        for m in self.memories.values():
            if m.layer == 'archive':
                continue
            # 简单重叠词打分
            words = set(query_lower.split())
            content_words = set(m.text.lower().split())
            overlap = len(words & content_words)
            if overlap > 0:
                score = overlap / len(words) * m.importance * (self.DECAY_RATE ** max(0, int(time.time() - m.last_accessed) // 86400))
                scored.append((score, -m.created_at, m))
        scored.sort(reverse=True)
        return [m for _, _, m in scored[:top_k]]

    def access(self, id: str) -> Optional[MemoryItem]:
        """访问一条记忆，更新计数器"""
        if id not in self.memories:
            return None
        m = self.memories[id]
        m.access_count += 1
        m.last_accessed = time.time()
        # 检查是否需要升级层级
        new_layer = self._compute_layer(m.importance, m.access_count)
        if self.LAYERS.index(new_layer) > self.LAYERS.index(m.layer):
            m.layer = new_layer
        self._save()
        return m

    def _compute_layer(self, importance: float, access_count: int) -> str:
        if access_count >= self.LAYER_THRESHOLDS['long'] or importance >= 0.8:
            return 'long'
        elif access_count >= self.LAYER_THRESHOLDS['short'] or importance >= 0.6:
            return 'short'
        return 'working'

    def decay(self):
        """所有记忆衰减，更新层级， archive 超过180天删除"""
        now = time.time()
        changed = False
        to_archive = []
        to_delete = []

        for m in self.memories.values():
            if m.layer == 'archive':
                if now - m.last_accessed > 180 * 86400:
                    to_delete.append(m.id)
                continue
            # Weibull衰减
            days_idle = max(0, int(now - m.last_accessed) // 86400)
            m.importance *= (self.DECAY_RATE ** days_idle)
            changed = True
            # 降级
            if m.importance < 0.3 and m.layer != 'archive':
                m.layer = 'archive'
            elif m.importance < 0.5 and m.layer == 'short':
                m.layer = 'working'

        for id in to_delete:
            del self.memories[id]
            changed = True

        if changed:
            self._save()

    def count(self) -> dict:
        return {layer: sum(1 for m in self.memories.values() if m.layer == layer) for layer in self.LAYERS}

    def get_stats(self) -> dict:
        counts = self.count()
        total = sum(counts.values())
        avg_importance = sum(m.importance for m in self.memories.values()) / max(1, total)
        return {**counts, "total": total, "avg_importance": round(avg_importance, 3)}

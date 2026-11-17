#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
记忆存储（M2）——6 类记忆的持久化与管理

兼容约定（重要）：
写入的记忆条目是 **v1 结构的超集**（保留 id / content / created_at），
因此 v1 的 manager.py 依然能正常读取，升级无损、可回退。

数据主权（方案红线 4）：
- delete(id)         单条删除
- delete_keyword(kw) 按关键词删除
- delete_conversation(cid) 遗忘某段关系
- export()           批量导出
- clear()            一键清除
"""

import json
import re
import sys
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional

# 允许 `python scripts/memory/store.py` 直接跑（此时 sys.path[0] 是脚本所在目录）
_ROOT = Path(__file__).resolve().parents[2]
if str(_ROOT) not in sys.path:
    sys.path.insert(0, str(_ROOT))

from scripts.core import schema  # noqa: E402
from scripts.core import settings as core_settings  # noqa: E402
from scripts.core.storage import read_json, write_json  # noqa: E402


def _now() -> str:
    return datetime.now().isoformat(timespec="seconds")


def _bigrams(text: str) -> set:
    """字符二元组集合（中英文通用，用于近似去重）"""
    t = re.sub(r"\s+", "", str(text or ""))
    return {t[i:i + 2] for i in range(len(t) - 1)} or {t}


def _similar(a: str, b: str, threshold: float = 0.75) -> bool:
    """重叠系数（|∩|/min）≥ threshold 视为重复表述。

    不用 Jaccard：短句是长句的子集时（"我喜欢喝果茶" ⊂ "用户喜欢喝果茶，
    最爱棒打鲜橙"），Jaccard 被长句稀释而漏配；重叠系数只看短句覆盖率。
    """
    ba, bb = _bigrams(a), _bigrams(b)
    smaller = ba if len(ba) <= len(bb) else bb
    return bool(smaller) and len(ba & bb) / len(smaller) >= threshold


class MemoryStore:
    """六类记忆的本地存储"""

    def __init__(self, data_dir: Optional[str] = None):
        self.data_dir = core_settings.resolve_data_dir(data_dir)
        self.data_dir.mkdir(parents=True, exist_ok=True)
        self.file = self.data_dir / "memory.json"

    # ---------- IO ----------

    def _load(self) -> List[Dict[str, Any]]:
        data = read_json(self.file, [])
        return data if isinstance(data, list) else []

    def _save(self, memories: List[Dict[str, Any]]) -> None:
        write_json(self.file, memories)

    def all(self) -> List[Dict[str, Any]]:
        """返回已规范化为 v2 结构的全部记忆"""
        return [schema.normalize_memory_entry(m, entry_id=i)
                for i, m in enumerate(self._load(), 1)]

    # ---------- 增 ----------

    def add(self, content: str, memory_type: str = "事实", source: str = "",
            importance: float = 0.5, valence: float = 0.0,
            conversation_id: str = "") -> Dict[str, Any]:
        """新增一条记忆

        去重策略（v2.1 加强）：
        1. 精确去重：同 type 同 content 只保留一条并刷新时间
        2. 近似去重：同 type 下二元组相似度 ≥0.7 的两条视为重复表述，
           保留信息量更大（更长）的那条，重要度取 max、时间刷新。
           避免「我喜欢喝果茶」和「用户喜欢喝果茶，最爱棒打鲜橙」入库两份。
        """
        content = str(content or "").strip()
        if not content:
            raise ValueError("记忆 content 不能为空")
        memories = self.all()
        for m in memories:
            if m.get("type") != memory_type:
                continue
            exact = m.get("content") == content
            fuzzy = not exact and _similar(m.get("content", ""), content)
            if exact or fuzzy:
                # 近似重复时保留信息量更大的表述；精确重复时内容不变
                if fuzzy and len(content) > len(str(m.get("content", ""))):
                    m["content"] = content
                m["updated_at"] = _now()
                m["importance"] = max(float(m.get("importance", 0.5)), importance)
                for i, old in enumerate(memories, 1):
                    old["id"] = i
                self._save(memories)
                return m

        entry = schema.memory_entry(
            content=content, memory_type=memory_type, source=source,
            importance=importance, valence=valence, conversation_id=conversation_id,
        )
        entry["id"] = len(memories) + 1
        memories.append(entry)
        for i, m in enumerate(memories, 1):
            m["id"] = i
        self._save(memories)
        return entry

    # ---------- 查 ----------

    def get(self, memory_id: int) -> Optional[Dict[str, Any]]:
        for m in self.all():
            if m.get("id") == memory_id:
                return m
        return None

    def by_type(self, memory_type: str) -> List[Dict[str, Any]]:
        return [m for m in self.all() if m.get("type") == memory_type]

    def search(self, keyword: str) -> List[Dict[str, Any]]:
        kw = (keyword or "").lower()
        return [m for m in self.all() if kw in str(m.get("content", "")).lower()]

    def update(self, memory_id: int, content: Optional[str] = None,
               memory_type: Optional[str] = None,
               importance: Optional[float] = None) -> Optional[Dict[str, Any]]:
        """编辑一条记忆（内容/类型/重要度），成功返回更新后的条目

        管理 CLI 之前只能删了重加（id 会变、来源丢失），现在支持原地修订。
        """
        memories = self.all()
        target = next((m for m in memories if m.get("id") == memory_id), None)
        if target is None:
            return None
        if content is not None:
            content = str(content).strip()
            if not content:
                raise ValueError("记忆 content 不能为空")
            target["content"] = content
        if memory_type is not None:
            if memory_type not in schema.MEMORY_TYPES:
                raise ValueError(f"未知记忆类型 {memory_type!r}，可选：{', '.join(schema.MEMORY_TYPES)}")
            target["type"] = memory_type
        if importance is not None:
            target["importance"] = max(0.0, min(1.0, float(importance)))
        target["updated_at"] = _now()
        self._save(memories)
        return target

    # ---------- 删（数据主权） ----------

    def delete(self, memory_id: int) -> bool:
        memories = self.all()
        left = [m for m in memories if m.get("id") != memory_id]
        if len(left) == len(memories):
            return False
        for i, m in enumerate(left, 1):
            m["id"] = i
        self._save(left)
        return True

    def delete_keyword(self, keyword: str) -> int:
        kw = (keyword or "").lower()
        memories = self.all()
        left = [m for m in memories if kw not in str(m.get("content", "")).lower()]
        removed = len(memories) - len(left)
        for i, m in enumerate(left, 1):
            m["id"] = i
        self._save(left)
        return removed

    def delete_conversation(self, conversation_id: str) -> int:
        """遗忘某段关系：整段会话产生的记忆一次性清除"""
        return self._delete_by_field("conversation_id", conversation_id)

    def _delete_by_field(self, field: str, value: Any) -> int:
        memories = self.all()
        left = [m for m in memories if m.get(field) != value]
        removed = len(memories) - len(left)
        for i, m in enumerate(left, 1):
            m["id"] = i
        self._save(left)
        return removed

    def clear(self) -> int:
        count = len(self.all())
        self._save([])
        return count

    def export(self) -> str:
        return json.dumps(self.all(), ensure_ascii=False, indent=2)

    # ---------- 召回与衰减 ----------

    def recall(self, memory_ids: List[int]) -> None:
        """标记被注入上下文的记忆：召回计数 +1，重要性回升

        v2.1：回升幅度随当前重要度递减（越接近 1.0 提升越小），
        打破「老条目每轮被召回→重要度更高→下轮还是它」的马太效应。
        """
        if not memory_ids:
            return
        memories = self.all()
        cfg = core_settings.decay_params(str(self.data_dir))
        boost = cfg["recall_boost"]
        ceiling = cfg["max_importance"]
        for m in memories:
            if m.get("id") in memory_ids:
                cur = float(m.get("importance", 0.5))
                headroom = max(0.0, ceiling - cur)
                effective = boost * (headroom / ceiling) if ceiling > 0 else 0.0
                m["recall_count"] = int(m.get("recall_count", 0)) + 1
                m["importance"] = min(ceiling, cur + effective)
                m["last_recalled_at"] = _now()
        self._save(memories)

    def decay(self, now: Optional[datetime] = None) -> int:
        """长期记忆重要性按半衰期衰减，返回被衰减的条数"""
        now = now or datetime.now()
        cfg = core_settings.decay_params(str(self.data_dir))
        half_life = cfg["half_life_days"]
        floor = cfg["min_importance"]
        memories = self.all()
        changed = 0
        for m in memories:
            updated = m.get("updated_at") or m.get("created_at")
            try:
                last = datetime.fromisoformat(str(updated))
            except (TypeError, ValueError):
                continue
            days = max(0.0, (now - last).total_seconds() / 86400.0)
            if days < 1:
                continue
            factor = 0.5 ** (days / half_life)
            new_imp = max(floor, float(m.get("importance", 0.5)) * factor)
            if abs(new_imp - float(m.get("importance", 0.5))) > 1e-6:
                m["importance"] = round(new_imp, 4)
                changed += 1
        if changed:
            self._save(memories)
        return changed

    # ---------- 统计 ----------

    def stats(self) -> Dict[str, Any]:
        memories = self.all()
        by_type: Dict[str, int] = {}
        for m in memories:
            t = m.get("type", "?")
            by_type[t] = by_type.get(t, 0) + 1
        return {
            "total": len(memories),
            "by_type": by_type,
            "avg_importance": round(
                sum(float(m.get("importance", 0)) for m in memories) / len(memories), 3
            ) if memories else 0.0,
        }


if __name__ == "__main__":
    import sys
    store = MemoryStore()
    if len(sys.argv) > 1 and sys.argv[1] == "stats":
        print(json.dumps(store.stats(), ensure_ascii=False, indent=2))
    elif len(sys.argv) > 1 and sys.argv[1] == "list":
        for m in store.all():
            print(f"#{m['id']} [{m['type']}] {m['content']} (重要度 {m['importance']})")
    else:
        print(json.dumps(store.stats(), ensure_ascii=False))

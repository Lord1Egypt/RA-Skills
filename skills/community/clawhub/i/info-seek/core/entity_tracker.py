#!/usr/bin/env python3
"""
core/entity_tracker.py — Infoseek 实体追踪器（v2.1.0 新增，v2.5.0 持久层扩展）

功能：
- record_hit(): NER 识别后记录一次命中
- apply_decay(): 90 天半衰期衰减 hit_count_30d
- get_hot_entities(): 返回 hit_count top N
- get_stale_entities(): 返回 90 天未使用的
- get_stats(): 综合统计

数据源：core/entities.py（v2.1.0 含元数据）

v2.5.0 持久层（P1-1 G1 修复）：
- 运行时状态（hit_count_30d / last_seen_at / last_verified_at）落盘
  `~/.infoseek/entities_state.json`（INFOSEEK_DATA_DIR 可覆盖），跨进程保留
- 增量状态叠加静态词典（静态源零污染）：读路径 = 静态实体 + 状态覆盖
- 开关 INFOSEEK_ENTITY_PERSIST=0 可关闭（行为回退 v2.1.0 纯内存）
"""

import json
import os
import sys
from datetime import datetime, date
from typing import List, Dict, Optional
from pathlib import Path

CORE_DIR = Path(__file__).parent

# v2.4.2 PATCH (P2 顺手): EntityTracker 模块级单例化
# 测试环境 predict_heat × 200 每次都新建实例耗时 40ms；
# 单例后稳定在 <1ms（与单跑一致），并惠及所有用 EntityTracker 的接口
_TRACKER_INSTANCE = None

_STATE_VERSION = 1
_STATE_FILENAME = 'entities_state.json'
# 可持久化的运行时字段
_RUNTIME_FIELDS = ('hit_count_30d', 'last_seen_at', 'last_verified_at')


def get_tracker() -> 'EntityTracker':
    """获取 EntityTracker 单例（v2.4.2 新增）"""
    global _TRACKER_INSTANCE
    if _TRACKER_INSTANCE is None:
        _TRACKER_INSTANCE = EntityTracker()
    return _TRACKER_INSTANCE


def reset_tracker():
    """手动失效单例（测试/单元 reset 用）"""
    global _TRACKER_INSTANCE
    _TRACKER_INSTANCE = None
sys.path.insert(0, str(CORE_DIR))


def _today() -> date:
    return date.today()


def _date_diff_days(date_str: str, base: Optional[date] = None) -> int:
    """计算 days since"""
    if not date_str:
        return 999
    try:
        d = datetime.fromisoformat(date_str).date()
        base = base or _today()
        return (base - d).days
    except Exception:
        return 999


def _persist_enabled() -> bool:
    """持久层开关（默认开；0 关闭回退纯内存）"""
    v = os.environ.get('INFOSEEK_ENTITY_PERSIST', '1')
    return v not in ('0', 'false', 'False', 'no')


class EntityTracker:
    """v2.1.0 实体追踪器（v2.5.0 + 持久层）"""

    def __init__(self,
                 decay_days: int = 90,
                 half_life_factor: float = 0.5,
                 stale_threshold_days: int = 90):
        self.decay_days = decay_days
        self.half_life_factor = half_life_factor
        self.stale_threshold = stale_threshold_days
        self._state: Dict[str, dict] = {}
        self._dirty = False
        if _persist_enabled():
            self._load_state()

    # ── 持久层 ────────────────────────────────────────────────────

    def _state_path(self) -> Path:
        from state_dir import state_path
        return state_path(_STATE_FILENAME)

    def _load_state(self) -> None:
        """加载状态文件；缺失/损坏 → 空状态（损坏文件备份防丢）"""
        p = self._state_path()
        if not p.exists():
            self._state = {}
            return
        try:
            data = json.loads(p.read_text(encoding='utf-8'))
            ents = data.get('entities', {}) if isinstance(data, dict) else {}
            self._state = {
                k: dict(v) for k, v in ents.items()
                if isinstance(v, dict)
            }
        except Exception as e:  # noqa: BLE001 损坏容错
            try:
                backup = Path(str(p) + '.corrupt.bak')
                backup.write_text(p.read_text(encoding='utf-8', errors='replace'),
                                  encoding='utf-8')
            except Exception:  # noqa: BLE001
                pass
            self._state = {}

    def _save_state(self) -> bool:
        """原子写状态文件（tmp + os.replace）；开关关闭 / 无变更 → 跳过"""
        if not _persist_enabled() or not self._dirty:
            return False
        try:
            p = self._state_path()
            payload = {
                'version': _STATE_VERSION,
                'updated': _today().isoformat(),
                'entities': self._state,
            }
            tmp = p.with_suffix('.tmp')
            tmp.write_text(json.dumps(payload, ensure_ascii=False, indent=2),
                           encoding='utf-8')
            os.replace(str(tmp), str(p))
            self._dirty = False
            return True
        except Exception:  # noqa: BLE001 持久层失败静默降级（不影响功能）
            return False

    def _mark_dirty(self) -> None:
        self._dirty = True

    def _view_entity(self, e: dict) -> dict:
        """静态实体 + 状态覆盖 → 只读视图（浅拷贝，不污染静态源）"""
        view = dict(e)
        st = self._state.get(e.get('name', ''))
        if st:
            for f in _RUNTIME_FIELDS:
                if f in st:
                    view[f] = st[f]
        # 状态中有但静态没有的实体字段（未来扩展）
        return view

    def _state_meta(self, name: str) -> dict:
        """获取实体的可变状态槽（不存在则基于静态默认初始化）"""
        st = self._state.get(name)
        if st is None:
            st = {
                'hit_count_30d': 0,
                'last_seen_at': _today().isoformat(),
                'last_verified_at': _today().isoformat(),
            }
            self._state[name] = st
        return st

    # ── 读路径 ────────────────────────────────────────────────────

    def _all_entities(self) -> List[Dict]:
        """加载所有实体（合并视图：静态 + 持久状态）"""
        from entities import get_all_entities
        return [self._view_entity(e) for e in get_all_entities()]

    def _find_entity(self, name: str) -> Optional[Dict]:
        """按 name 查找实体（合并视图）"""
        for e in self._all_entities():
            if e['name'] == name:
                return e
        return None

    # ── 写路径（全部走状态槽 + 落盘） ────────────────────────────

    def record_hit(self, entity_name: str) -> bool:
        """NER 识别后调用：记录一次命中 + 更新 last_seen_at

        返回 True=成功，False=实体不存在
        """
        from entities import get_all_entities
        known = {e['name'] for e in get_all_entities()}
        if entity_name not in known:
            return False

        st = self._state_meta(entity_name)
        st['hit_count_30d'] = st.get('hit_count_30d', 0) + 1
        st['last_seen_at'] = _today().isoformat()
        self._mark_dirty()
        self._save_state()
        return True

    def record_hits_batch(self, names: List[str]) -> dict:
        """批量记录（共享一次落盘）"""
        from entities import get_all_entities
        known = {e['name'] for e in get_all_entities()}
        success = 0
        for n in names:
            if n not in known:
                continue
            st = self._state_meta(n)
            st['hit_count_30d'] = st.get('hit_count_30d', 0) + 1
            st['last_seen_at'] = _today().isoformat()
            success += 1
            self._mark_dirty()
        self._save_state()
        return {
            'total': len(names),
            'success': success,
            'unknown': len(names) - success,
        }

    def apply_decay(self) -> dict:
        """应用 90 天半衰期衰减（基于持久状态，落盘）

        算法：
          age = days since last_seen
          if age > 90: factor = 0.5^((age-90)/90)
          hit_count *= factor
        """
        decayed_count = 0
        total_reduction = 0
        total_entities = 0

        from entities import get_all_entities
        statics = {e['name']: e for e in get_all_entities()}
        # 状态槽 + 静态实体（未进状态槽的 hit=0 不衰减）
        names = set(self._state.keys()) | set(statics.keys())
        total_entities = len(names)

        for name in names:
            st = self._state_meta(name)
            hit = st.get('hit_count_30d', 0)
            if hit == 0:
                continue

            age = _date_diff_days(st.get('last_seen_at', ''))
            if age <= self.decay_days:
                continue

            # 半衰期公式
            factor = self.half_life_factor ** ((age - self.decay_days) / self.decay_days)
            new_hit = max(0, int(hit * factor))

            if new_hit < hit:
                total_reduction += (hit - new_hit)
                decayed_count += 1
                st['hit_count_30d'] = new_hit
                self._mark_dirty()

        self._save_state()
        return {
            'decayed_count': decayed_count,
            'total_reduction': total_reduction,
            'total_entities': total_entities,
        }

    # ── 查询（基于合并视图） ──────────────────────────────────────

    def get_hot_entities(self, top_n: int = 10, min_hit: int = 1) -> List[Dict]:
        """返回 hit_count_30d 最高的 top N

        按 hit_count_30d 降序
        """
        entities = self._all_entities()
        hot = sorted(
            [e for e in entities if e.get('hit_count_30d', 0) >= min_hit],
            key=lambda x: -x['hit_count_30d'],
        )
        return [
            {
                'name': e['name'],
                'category': e.get('category', ''),
                'hit_count_30d': e['hit_count_30d'],
                'last_seen_at': e.get('last_seen_at', ''),
            }
            for e in hot[:top_n]
        ]

    def get_stale_entities(self, threshold_days: Optional[int] = None) -> List[Dict]:
        """返回 N 天未使用的冷条目"""
        threshold = threshold_days or self.stale_threshold
        entities = self._all_entities()
        stale = []
        for e in entities:
            age = _date_diff_days(e.get('last_seen_at', ''))
            if age > threshold:
                stale.append({
                    'name': e['name'],
                    'category': e.get('category', ''),
                    'age_days': age,
                    'last_seen_at': e.get('last_seen_at', ''),
                    'hit_count_30d': e.get('hit_count_30d', 0),
                })
        return stale

    def get_stats(self) -> Dict:
        """综合统计"""
        entities = self._all_entities()
        total = len(entities)
        total_hit = sum(e.get('hit_count_30d', 0) for e in entities)

        # 按 source 分类
        sources = {}
        for e in entities:
            s = e.get('source', 'manual')
            sources[s] = sources.get(s, 0) + 1

        # 热/冷条目统计
        hot = len([e for e in entities if e.get('hit_count_30d', 0) >= 5])
        stale = len(self.get_stale_entities())

        # 类别分布
        categories = {}
        for e in entities:
            cat = e.get('category', 'UNKNOWN')
            categories[cat] = categories.get(cat, 0) + 1

        return {
            'total_entities': total,
            'total_hit_count': total_hit,
            'avg_hit_count': round(total_hit / total, 2) if total else 0,
            'hot_entities': hot,
            'stale_entities': stale,
            'by_source': sources,
            'by_category': dict(sorted(categories.items(), key=lambda x: -x[1])),
        }


# ═══════════════════════════════════════════════════════════════
# CLI
# ═══════════════════════════════════════════════════════════════

def main():
    if len(sys.argv) < 2:
        print("Usage: python -m core.entity_tracker [stats | decay | hot | stale | persist]")
        sys.exit(1)

    cmd = sys.argv[1]
    tracker = EntityTracker()

    if cmd == 'stats':
        import json
        stats = tracker.get_stats()
        print(json.dumps(stats, ensure_ascii=False, indent=2))
    elif cmd == 'decay':
        result = tracker.apply_decay()
        print(f"衰减: {result}")
    elif cmd == 'hot':
        n = int(sys.argv[2]) if len(sys.argv) > 2 else 10
        for e in tracker.get_hot_entities(top_n=n):
            print(f"  {e['name']:25s} hit={e['hit_count_30d']:3d} ({e['category']})")
    elif cmd == 'stale':
        for e in tracker.get_stale_entities():
            print(f"  {e['name']:25s} age={e['age_days']}d ({e['category']})")
    elif cmd == 'persist':
        if _persist_enabled():
            print(f"状态文件: {tracker._state_path()}")
            print(f"实体状态槽: {len(tracker._state)}")
        else:
            print("持久层已关闭（INFOSEEK_ENTITY_PERSIST=0）")
    else:
        print(f"未知命令: {cmd}")


if __name__ == '__main__':
    main()
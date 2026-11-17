#!/usr/bin/env python3
"""
core/claim_store.py — Infoseek 持久 claim store（v2.3.1 新增）

为冲突检测提供跨来源 / 跨 research 会话的声明持久层：
- add_claim(entity, claim)：累积某实体的事实声明
- get_claims(entity)：取该实体的全部声明（供跨源/跨会话比对）
- decay(ttl_days)：超龄声明清理（v2.4.0 跨会话历史冲突用）

claim 结构（与 conflict_v3 的 claim 一致）：
    {'entity_name', 'mention', 'source', 'source_title', 'text', 'timestamp', 'matched_alias'}
"""

import sys
import json
import datetime
from pathlib import Path
from typing import List, Dict, Optional

CORE_DIR = Path(__file__).parent
sys.path.insert(0, str(CORE_DIR))

try:
    from state_dir import state_path
except ImportError:  # 作为 core 包导入时
    from .state_dir import state_path

DEFAULT_FILE = 'claims.json'
TTL_DAYS = 180          # 默认保留 180 天（超期由 decay() 清理）
MAX_PER_ENTITY = 200    # 单实体上限，防无界增长


class ClaimStore:
    """v2.3.1 持久 claim store（内存缓存 + JSON 落盘）"""

    def __init__(self, path: Optional[str] = None):
        self.path = state_path(path or DEFAULT_FILE)
        self._data: Optional[Dict[str, list]] = None

    # ── 加载 / 保存 ──────────────────────────────────────────────
    def load(self) -> Dict[str, list]:
        if self._data is not None:
            return self._data
        if not self.path.exists():
            self._data = {}
            return self._data
        try:
            with open(self.path, 'r', encoding='utf-8') as f:
                self._data = json.load(f)
        except Exception:
            self._data = {}
        return self._data

    def save(self):
        try:
            with open(self.path, 'w', encoding='utf-8') as f:
                json.dump(self.load(), f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"[claim_store] 保存失败: {e}")

    # ── 读写接口 ────────────────────────────────────────────────
    def add_claim(self, entity: str, claim: Dict):
        """累积一条声明（自动补 timestamp）"""
        data = self.load()
        claim = dict(claim)
        if 'timestamp' not in claim:
            claim['timestamp'] = datetime.date.today().isoformat()
        data.setdefault(entity, []).append(claim)
        # 限额防无界
        if len(data[entity]) > MAX_PER_ENTITY:
            data[entity] = data[entity][-MAX_PER_ENTITY:]

    def get_claims(self, entity: str) -> List[Dict]:
        return self.load().get(entity, [])

    def all_entities(self) -> List[str]:
        return list(self.load().keys())

    def stats(self) -> Dict:
        data = self.load()
        total = sum(len(v) for v in data.values())
        return {
            'entities': len(data),
            'total_claims': total,
            'path': str(self.path),
        }

    def clear(self):
        self._data = {}
        self.save()

    # ── v2.4.0 跨会话用：TTL/decay 清理 ─────────────────────────
    def decay(self, ttl_days: int = TTL_DAYS) -> Dict:
        data = self.load()
        today = datetime.date.today()
        removed = 0
        for ent, claims in data.items():
            kept = []
            for c in claims:
                ts = c.get('timestamp', '')
                d = None
                if ts:
                    try:
                        d = datetime.date.fromisoformat(ts)
                    except Exception:
                        d = None
                if d and (today - d).days > ttl_days:
                    removed += 1
                    continue
                kept.append(c)
            data[ent] = kept
        self.save()
        return {'removed': removed, 'remaining': sum(len(v) for v in data.values())}

    # ── v2.4.0 跨会话比对（给 conflict_v3 用） ─────────────────
    def cross_session_compare(self, entity: str, session_sources: set,
                              session_texts: Optional[List[str]] = None) -> Dict:
        """比对历史声明 vs 本会话声明

        参数:
            entity: 实体名
            session_sources: 当前会话出现的 source 集合
            session_texts: 当前会话中该实体的声明文本（可选，用于判断是否有冲突历史）

        返回:
            {
              'historical_count': int,         # 历史声明数（不含本会话）
              'historical_sources': [str],     # 历史来源 URL（去重）
              'has_historical_conflict': bool, # 若历史中有与 session 文本相反的声明
            }
        """
        all_claims = self.get_claims(entity)
        historical = [c for c in all_claims
                      if c.get('source') and c['source'] not in session_sources]
        historical_sources = list(dict.fromkeys(c['source'] for c in historical))[:10]

        has_conflict = False
        if session_texts:
            # 极简判定：历史文本是否包含明确否定词（与 session_texts 任一不一致）
            neg = {'不', '否', '非', 'no', 'not', "n't"}
            sess_has_neg = any(any(w in t.lower() for w in neg) for t in session_texts)
            hist_has_neg = any(any(w in (c.get('text', '') or '').lower()
                                   for w in neg) for c in historical)
            if sess_has_neg != hist_has_neg:
                has_conflict = True
        else:
            has_conflict = len(historical) > 0

        return {
            'historical_count': len(historical),
            'historical_sources': historical_sources,
            'has_historical_conflict': has_conflict,
        }


# ═══════════════════════════════════════════════════════════════
# v2.4.3 PATCH (P2 顺手): 模块级单例 helper
# ═══════════════════════════════════════════════════════════════
_DEFAULT_INSTANCE = None

def get_claim_store(path: Optional[str] = None) -> 'ClaimStore':
    """v2.4.3 新增：ClaimStore 单例（共享 DEFAULT_FILE 路径）"""
    global _DEFAULT_INSTANCE
    if path:
        # 显式路径不走单例（隔离场景）
        return ClaimStore(path=path)
    if _DEFAULT_INSTANCE is None:
        _DEFAULT_INSTANCE = ClaimStore()
    return _DEFAULT_INSTANCE

def reset_claim_store():
    """v2.4.3 新增：手动失效单例"""
    global _DEFAULT_INSTANCE
    _DEFAULT_INSTANCE = None


# ═══════════════════════════════════════════════════════════════
# CLI
# ═══════════════════════════════════════════════════════════════

def main():
    import sys as _sys
    cmd = _sys.argv[1] if len(_sys.argv) > 1 else 'stats'
    store = ClaimStore()
    if cmd == 'stats':
        print(json.dumps(store.stats(), ensure_ascii=False, indent=2))
    elif cmd == 'clear':
        store.clear()
        print('[claim_store] 已清空')
    elif cmd == 'decay':
        ttl = int(_sys.argv[2]) if len(_sys.argv) > 2 else TTL_DAYS
        print(json.dumps(store.decay(ttl), ensure_ascii=False, indent=2))
    else:
        print(f"未知命令: {cmd}")


if __name__ == '__main__':
    main()

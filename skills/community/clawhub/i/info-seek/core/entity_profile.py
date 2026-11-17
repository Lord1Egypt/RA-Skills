#!/usr/bin/env python3
"""
core/entity_profile.py — Infoseek 实体画像（v2.3.0 新增）

为高频实体自动积累调研档案，形成知识库：
- 每次 research() 后调用 update_profiles() 累计
- 每实体记录：topics（主题关键词）、source_domains、时间轨迹、hit 总量、冲突引用
- 持久化：运行时数据目录（默认 ~/.infoseek/entity_profiles.json，可由 INFOSEEK_DATA_DIR / INFOSEEK_DB 配置）

CLI:
  python -m core.entity_profile top [K]    查看 Top-K 实体画像
  python -m core.entity_profile get NAME    查看单实体画像
  python -m core.entity_profile stats       画像概览
"""

import sys
import json
import re
import datetime
from pathlib import Path
from typing import List, Dict, Optional

CORE_DIR = Path(__file__).parent
sys.path.insert(0, str(CORE_DIR))

try:
    from state_dir import state_path
except ImportError:  # 作为 core 包导入时
    from .state_dir import state_path


class EntityProfile:
    """v2.3.0 实体画像积累器"""

    PROFILE_FILE = 'entity_profiles.json'

    def __init__(self):
        self.path = state_path(self.PROFILE_FILE)
        self._data: Optional[Dict[str, dict]] = None  # v2.4.3 PATCH: 初始化缓存字段
        self._cached_mtime: Optional[float] = None

    def load(self) -> Dict[str, dict]:
        """v2.4.3 PATCH (P2): 加 _data 缓存 + 文件 mtime 失效"""
        if not self.path.exists():
            self._data = {}
            return self._data
        try:
            mtime = self.path.stat().st_mtime
            if self._data is None or getattr(self, '_cached_mtime', None) != mtime:
                with open(self.path, 'r', encoding='utf-8') as f:
                    self._data = json.load(f)
                self._cached_mtime = mtime
            return self._data if self._data is not None else {}
        except Exception:
            return {}

    def invalidate_cache(self):
        """v2.4.3 新增：手动失效 load 缓存"""
        self._data = None
        self._cached_mtime = None

    def save(self, data: Dict[str, dict]):
        try:
            with open(self.path, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"[entity_profile] 保存失败: {e}")

    def _extract_topics(self, text: str, limit: int = 5) -> List[str]:
        """从文本提取主题关键词（jieba 优先，兜底简单切分）

        2026-09-29：jieba 探测统一经 jieba_bridge（进程内缓存；
        原实现每次调用裸 try-import）。
        """
        topics = []
        import jieba_bridge as _jb
        words = _jb.lcut(text)
        if words is not None:
            # 过滤：长度≥2 的实词
            stop = {'公司', '集团', '发布', '模型', '技术', '合作', '研究', '市场', '报告', '数据'}
            topics = [w for w in words if len(w) >= 2 and w not in stop][:limit]
        else:
            # 兜底：按空白/标点切分
            words = re.split(r'[\s,，。;；:：]+', text)
            topics = [w for w in words if len(w) >= 2][:limit]
        return topics

    def update_profiles(self, sources: List[Dict], entity_index: List[Dict],
                        conflicts: Optional[List[Dict]] = None) -> dict:
        """每次 research() 后调用，累计实体画像

        参数:
            sources: 调研来源列表
            entity_index: research() 的 entity_index（v2.2.0）
            conflicts: 冲突列表（v2.3.0 冲突引用）

        返回: {'updated': N, 'new': M, 'total': T}
        """
        profiles = self.load()
        today = datetime.date.today().isoformat()
        updated, new = 0, 0

        # 来源主题词
        all_text = ' '.join(
            s.get('title', '') + ' ' + (s.get('snippet', '') or s.get('text', '') or '')
            for s in sources
        )
        source_topics = self._extract_topics(all_text)

        for e in entity_index:
            name = e['entity_name']
            if name not in profiles:
                profiles[name] = {
                    'entity_name': name,
                    'entity_type': e.get('entity_type', 'UNKNOWN'),
                    'topics': [],
                    'source_domains': [],
                    'first_seen': today,
                    'last_seen': today,
                    'hit_total': 0,
                    'conflict_refs': [],
                }
                new += 1
            else:
                updated += 1
            p = profiles[name]
            p['last_seen'] = today
            p['hit_total'] += e.get('hit_count', 1)
            # topics 合并去重
            for t in source_topics:
                if t not in p['topics']:
                    p['topics'].append(t)
            p['topics'] = p['topics'][:10]
            # 冲突引用
            if conflicts:
                for c in conflicts:
                    if c.get('entity_name') == name and c.get('conflict_id') not in p['conflict_refs']:
                        p['conflict_refs'].append(c['conflict_id'])
                p['conflict_refs'] = p['conflict_refs'][:20]

        self.save(profiles)
        return {'updated': updated, 'new': new, 'total': len(profiles)}

    def get_profile(self, entity_name: str) -> Optional[dict]:
        """单实体画像"""
        return self.load().get(entity_name)

    def get_top_entities(self, k: int = 20) -> List[dict]:
        """按 hit_total 排序 Top-K"""
        profiles = self.load()
        ranked = sorted(profiles.values(), key=lambda x: -x['hit_total'])
        return ranked[:k]

    def profile_summary(self) -> dict:
        """画像概览"""
        profiles = self.load()
        return {
            'total_profiles': len(profiles),
            'top_entities': [p['entity_name'] for p in self.get_top_entities(5)],
            'with_conflicts': sum(1 for p in profiles.values() if p['conflict_refs']),
        }

    def clear(self):
        self.save({})


# ═══════════════════════════════════════════════════════════════
# v2.4.3 PATCH (P2 顺手): 模块级单例 helper
# ═══════════════════════════════════════════════════════════════
_PROFILE_INSTANCE = None

def get_profile() -> 'EntityProfile':
    """v2.4.3 新增：EntityProfile 单例"""
    global _PROFILE_INSTANCE
    if _PROFILE_INSTANCE is None:
        _PROFILE_INSTANCE = EntityProfile()
    return _PROFILE_INSTANCE

def reset_profile():
    """v2.4.3 新增：手动失效单例"""
    global _PROFILE_INSTANCE
    _PROFILE_INSTANCE = None


# v2.7.2 PATCH: update_profiles 异步版本
async def update_profiles_async(sources: List[Dict], entity_index: List[Dict],
                              conflicts: Optional[List[Dict]] = None,
                              profiler=None) -> dict:
    """v2.7.2 新增：update_profiles 异步版（asyncio.to_thread 包装）"""
    import asyncio
    p = profiler if profiler is not None else EntityProfile()
    return await asyncio.to_thread(p.update_profiles, sources, entity_index, conflicts)


# ═══════════════════════════════════════════════════════════════
# CLI
# ═══════════════════════════════════════════════════════════════

def main():
    cmd = sys.argv[1] if len(sys.argv) > 1 else 'stats'
    prof = EntityProfile()

    if cmd == 'top':
        k = int(sys.argv[2]) if len(sys.argv) > 2 else 10
        print(f"Top-{k} 实体画像:")
        for p in prof.get_top_entities(k):
            print(f"  {p['entity_name']:20s} type={p['entity_type']:12s} "
                  f"hit_total={p['hit_total']:4d} topics={p['topics'][:3]}")
    elif cmd == 'get':
        if len(sys.argv) < 3:
            print("Usage: python -m core.entity_profile get NAME")
            sys.exit(1)
        p = prof.get_profile(sys.argv[2])
        if p:
            import json
            print(json.dumps(p, ensure_ascii=False, indent=2))
        else:
            print(f"未找到画像: {sys.argv[2]}")
    elif cmd == 'stats':
        import json
        print(json.dumps(prof.profile_summary(), ensure_ascii=False, indent=2))
    elif cmd == 'clear':
        prof.clear()
        print("✅ 画像已清空")
    else:
        print(f"未知命令: {cmd}")


if __name__ == '__main__':
    main()

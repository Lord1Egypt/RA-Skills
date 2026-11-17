#!/usr/bin/env python3
"""
core/entity_aliases.py — Infoseek 别名持久化管理（v2.1.1 新增）

独立 JSON 持久化（不污染 entities.py）：
- 持久化路径：运行时数据目录（默认 ~/.infoseek/entity_aliases.json，可由 INFOSEEK_DATA_DIR / INFOSEEK_DB 配置）
- 结构：{entity_name: [auto_alias_1, auto_alias_2, ...]}

API：
- get_aliases(name) → 完整别名（含 entities.py）
- add_alias(name, alias, source='auto') → 添加
- auto_expand(name, text) → 从命中上下文提取候选
- load() / save()
- clear(name=None) → 清空
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


class EntityAliases:
    """v2.1.1 别名管理（v2.1.2 升级：来源标签 + 拒绝日志）"""

    FILE = 'entity_aliases.json'

    # v2.1.3: 热/冷别名分离
    HOT_ALIASES_FILE = 'hot_aliases.json'
    COLD_ALIASES_FILE = 'cold_aliases.json'
    # 热/冷阈值：别名被引用次数
    HOT_THRESHOLD = 5
    COLD_THRESHOLD = 1

    # v2.2.0: 生命周期参数
    STALE_PARENT_DAYS = 90        # 父实体 N 天未出现 → alias 视为 stale
    AUTO_CLEAN_DAYS = 90          # stale alias 保留 N 天后自动清理（可重建）

    # v2.2.1: 优先检索缓存（TTL 秒，避免每次 NER 重复 IO）
    PRIORITY_CACHE_TTL = 300

    # v2.1.2: 拒词词典（auto_expand 排除）
    STOPWORDS = {
        # 中文
        '公司', '集团', '有限', '股份', '科技', '股份公司', '有限责任',
        '股份有限', '技术', '信息', '网络', '数据', '公司', '中心',
        '研究院', '大学', '学院', '研究所', '实验室',
        # 英文
        'Inc', 'Inc.', 'Corp', 'Corp.', 'Ltd', 'Ltd.', 'LLC', 'Co', 'Co.',
        'Company', 'Corporation', 'Limited', 'GmbH', 'AG', 'S.A.',
        'Holdings', 'Group', 'Holdings Group',
    }

    def __init__(self):
        self.path = state_path(self.FILE)
        # v2.2.1: 优先检索缓存 {entity_name: (timestamp, result)}
        self._priority_cache: Dict[str, tuple] = {}
        self._cache_hits = 0  # 统计缓存命中（测试/监控用）

    def _migrate_old_format(self, data: dict) -> dict:
        """v2.1.2 迁移：旧 [alias1, alias2] → [{'alias': ..., 'source': 'manual'}, ...]"""
        new_data = {}
        for name, aliases in data.items():
            new_list = []
            for item in aliases:
                if isinstance(item, str):
                    # 旧格式：纯字符串
                    new_list.append({
                        'alias': item,
                        'source': 'manual',  # 旧数据无法追溯，标记 manual
                        'created_at': '2026-08-08',
                    })
                elif isinstance(item, dict):
                    # 已迁移
                    new_list.append(item)
            new_data[name] = new_list
        return new_data

    def load(self) -> Dict[str, List]:
        """加载所有 alias（v2.1.2 自动迁移旧格式）"""
        if not self.path.exists():
            return {}
        try:
            with open(self.path, 'r', encoding='utf-8') as f:
                raw = json.load(f)
            return self._migrate_old_format(raw)
        except Exception:
            return {}

    def save(self, data: Dict[str, List[str]]):
        """持久化"""
        try:
            with open(self.path, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"[entity_aliases] 保存失败: {e}")

    def get_aliases(self, entity_name: str) -> List[str]:
        """获取某实体的所有 alias（entities.py + 本 JSON）

        v2.4.1 PATCH: 改为相对导入 `from entities import get_all_entities`，
        原 `import core.entities as _ent` 在沙箱路径下因 core 不是顶层包名而 ModuleNotFoundError，
        导致 alias_map 全空，v2.3.0/v2.3.1 别名归并能力失效（DEF-F）。
        """
        from entities import get_all_entities
        all_ents = get_all_entities()
        result = []
        for e in all_ents:
            if e['name'] == entity_name:
                result = list(e.get('aliases', []))
                break
        # 合并 JSON 中的 alias（v2.1.2 提取 alias 字段）
        data = self.load()
        for item in data.get(entity_name, []):
            if isinstance(item, dict):
                result.append(item.get('alias', ''))
            else:
                result.append(item)
        # 去重（保序）
        seen = set()
        unique = []
        for a in result:
            if a and a.lower() not in seen:
                seen.add(a.lower())
                unique.append(a)
        return unique

    def get_prioritized_aliases(self, entity_name: str) -> Dict[str, List[str]]:
        """v2.2.0: 高频别名优先检索（v2.2.1: TTL 缓存）

        返回分级 dict（供 NER 按优先级匹配）:
            {
                'static': [...],   # entities.py 内嵌别名（权威）
                'hot': [...],      # 父实体热（hit≥HOT_THRESHOLD）→ 高频优先
                'cold': [...],     # 父实体冷 → 降级
            }

        策略：alias 生命周期跟随父实体（B+C 混合）
        """
        import time
        # v2.2.1: 缓存命中检查
        cached = self._priority_cache.get(entity_name)
        if cached and (time.time() - cached[0]) < self.PRIORITY_CACHE_TTL:
            self._cache_hits += 1
            return cached[1]

        from entity_tracker import EntityTracker
        tracker = EntityTracker()
        entity = tracker._find_entity(entity_name)
        if entity is None:
            result = {'static': self.get_aliases(entity_name), 'hot': [], 'cold': []}
        else:
            hit = entity.get('hit_count_30d', 0)
            all_aliases = self.get_aliases(entity_name)

            # 静态别名 = entities.py 内嵌（无法区分，用 JSON 数据反查）
            data = self.load()
            json_aliases = [a.get('alias', '') if isinstance(a, dict) else a for a in data.get(entity_name, [])]
            json_lower = {a.lower() for a in json_aliases}
            static = [a for a in all_aliases if a.lower() not in json_lower]

            if hit >= self.HOT_THRESHOLD:
                result = {'static': static, 'hot': json_aliases, 'cold': []}
            else:
                result = {'static': static, 'hot': [], 'cold': json_aliases}

        # v2.2.1: 写入缓存
        self._priority_cache[entity_name] = (time.time(), result)
        return result

    def clear_priority_cache(self):
        """v2.2.1: 手动失效优先检索缓存（add_alias/clean 后调用）"""
        self._priority_cache.clear()

    def add_alias(self, entity_name: str, alias: str, source: str = 'auto') -> bool:
        """添加新 alias（自动去重 + 来源标签）"""
        if not entity_name or not alias:
            return False

        data = self.load()
        if entity_name not in data:
            data[entity_name] = []

        # 检查是否已存在（不区分大小写）
        existing_aliases = self.get_aliases(entity_name)
        if any(a.lower() == alias.lower() for a in existing_aliases):
            return False  # 已存在

        # v2.1.2: 添加 source 标签 + 时间戳
        data[entity_name].append({
            'alias': alias,
            'source': source,  # 'auto' / 'manual'
            'created_at': datetime.date.today().isoformat(),
        })
        self.save(data)
        self.clear_priority_cache()  # v2.2.1: 失效缓存
        return True

    def auto_expand(self, entity_name: str, text: str, min_hit: int = 5) -> List[str]:
        """自动从命中文本提取新 alias（v2.1.3 噪声消除版）

        触发条件：entity_name 在 entity_tracker.hit_count_30d >= min_hit

        v2.1.3 优化（相对 v2.1.2）：
        - NER 句子切分：只提取与 entity 同一子句的候选（消除跨句噪声）
        - jieba 词性过滤：候选须为名词类（n/nr/nt/nz/org）才保留（消除动词/形容词）
        - 过滤"发布/开发/是/的/也"等常见谓词
        - 中英混合识别优化

        v2.1.2 保留：
        - 实体类型感知（ORG=30 / TECH=20 窗口）
        - STOPWORDS 词典排除介词
        - 按距离排序（近者优先）
        """
        from entity_tracker import EntityTracker
        tracker = EntityTracker()
        entity = tracker._find_entity(entity_name)

        # 触发条件检查
        if not entity or entity.get('hit_count_30d', 0) < min_hit:
            return []

        # 实体类型感知（不同类型窗口不同）
        entity_category = entity.get('category', 'ORG')
        if entity_category in ('TECH', 'PRODUCT'):
            window = 20  # 短窗口
            min_alias_len = 3
        else:  # ORG / PERSON / METRIC
            window = 30  # 正常窗口
            min_alias_len = 3

        # v2.1.3 / 2026-09-29: jieba 词性能力统一经 jieba_bridge 探测（进程内缓存，
        # 原实现每次调用裸 try-import；收敛后仅一次，热路径零 import 开销）
        import jieba_bridge as _jb
        pseg = _jb.get_posseg()
        HAS_JIEBA = pseg is not None

        # v2.1.3: 常见谓词（中文动词/形容词，jieba 不可用时的 fallback 过滤）
        VERB_STOPWORDS = {
            '发布', '开发', '推出', '使用', '提供', '发布新', '开发新',
            '成立', '创立', '是', '的', '也', '和', '与', '由', '在',
            '很', '最', '新', '旧', '有', '没有', '进行', '实现',
            '框架很', '公司开发', '公司称', '发布新模型', '公司也称',
        }

        existing_aliases = set(a.lower() for a in self.get_aliases(entity_name))
        candidates_with_dist = []  # [(alias, distance)]

        # 1) 找 entity_name 所有出现位置
        text_lower = text.lower()
        name_lower = entity_name.lower()

        for m in re.finditer(re.escape(name_lower), text_lower):
            start, end = m.span()

            # v2.1.3: NER 句子切分（限定同一子句）
            # 找到当前子句边界（句号/逗号/分号/感叹号/问号）
            sent_boundaries = [i for i, ch in enumerate(text) if ch in '。；！？，,;!?']
            sent_start = 0
            sent_end = len(text)
            for b in sent_boundaries:
                if b < start:
                    sent_start = b + 1
                elif b > end:
                    sent_end = b
                    break

            # 子句内窗口（比全局窗口更精确）
            before = text[max(sent_start, start-window):start]
            after = text[end:min(sent_end, end+window)]

            # 2) 提取中文别名（v2.1.3 词性过滤）
            for c in re.findall(r'[\u4e00-\u9fff]{2,8}', before + after):
                if c.lower() in existing_aliases:
                    continue
                if c in self.STOPWORDS:
                    continue
                if c.lower() == name_lower:
                    continue
                if c in VERB_STOPWORDS:
                    continue

                # v2.1.3: jieba 词性过滤（保留纯名词类候选）
                if HAS_JIEBA:
                    try:
                        words = list(pseg.cut(c))
                        # 只要包含动词/形容词/副词/助词（v/a/d/ul/uj）→ 过滤
                        has_verb_like = any(
                            w.flag[0] in ('v', 'a', 'd', 'u', 'p', 'c') and len(w.word) >= 2
                            for w in words
                        )
                        # 纯名词判断：所有词都是 n/nr/nt/nz/ng/eng/j/x
                        all_noun_like = all(
                            w.flag.startswith('n') or w.flag.startswith('j')
                            or w.flag.startswith('eng') or w.flag.startswith('x')
                            or w.flag.startswith('org') or w.flag.startswith('nt')
                            for w in words if len(w.word) >= 2
                        )
                        if has_verb_like or not all_noun_like:
                            continue  # 含动词或非名词 → 过滤
                    except Exception:
                        pass

                # 距离（越近越好）
                dist = min(
                    start - text.rfind(c, max(0, start-30), start) if c in before else 999,
                    text.find(c, end, min(len(text), end+30)) - end if c in after else 999,
                )
                candidates_with_dist.append((c, dist))

            # 3) 提取英文别名（v2.1.2 至少 2 个 CapitalCase）
            for c in re.findall(r'(?:[A-Z][a-zA-Z]{1,}\s+){1,3}[A-Z][a-zA-Z]{1,}', before + after):
                if c.lower() == name_lower or c.lower() in existing_aliases:
                    continue
                # 排除 STOPWORDS
                if any(sw in c for sw in self.STOPWORDS if len(sw) > 3):
                    if c.endswith(('Inc', 'Corp', 'Ltd', 'Group')) or ' Company' in c:
                        continue
                if len(c) < min_alias_len or len(c) > 30:
                    continue
                dist = 999
                candidates_with_dist.append((c, dist))

        # 4) 去重 + 按距离排序（v2.1.2 优先级）
        seen = set()
        unique = []
        for alias, dist in sorted(candidates_with_dist, key=lambda x: x[1]):
            if alias.lower() in seen:
                continue
            seen.add(alias.lower())
            unique.append(alias)

        # 5) 过滤长度 + 谓词
        unique = [c for c in unique
                  if len(c) >= min_alias_len
                  and c.lower() != name_lower
                  and c not in VERB_STOPWORDS]

        # 6) 自动入库（带 source='auto' 标签）
        added = []
        for c in unique[:5]:  # 最多 5 个
            if self.add_alias(entity_name, c, source='auto'):
                added.append(c)

        return added

    def count(self) -> int:
        """返回总 alias 数"""
        return sum(len(v) for v in self.load().values())

    def list_all(self) -> Dict[str, List[str]]:
        """列出所有 alias"""
        return self.load()

    def clear(self, entity_name: Optional[str] = None):
        """清空（指定 entity 或全部）"""
        if entity_name:
            data = self.load()
            data.pop(entity_name, None)
            self.save(data)
        else:
            self.save({})

    # ═══════════════════════════════════════════════════════════════
    # v2.1.3: 别名热/冷分离
    # ═══════════════════════════════════════════════════════════════

    def _hot_path(self) -> Path:
        return state_path(self.HOT_ALIASES_FILE)

    def _cold_path(self) -> Path:
        return state_path(self.COLD_ALIASES_FILE)

    def get_alias_stats(self) -> Dict:
        """统计每个别名的引用频次（基于 entity_tracker hit_count）

        返回: {'hot_aliases': [...], 'cold_aliases': [...], 'by_entity': {...}}
        """
        from entity_tracker import EntityTracker
        tracker = EntityTracker()
        data = self.load()

        hot = []
        cold = []
        by_entity = {}

        for entity_name, aliases in data.items():
            entity = tracker._find_entity(entity_name)
            hit_count = entity.get('hit_count_30d', 0) if entity else 0

            alias_entries = []
            for item in aliases:
                alias = item.get('alias', '') if isinstance(item, dict) else item
                alias_entries.append({
                    'alias': alias,
                    'entity_name': entity_name,
                    'entity_hit_count': hit_count,
                    'source': item.get('source', 'manual') if isinstance(item, dict) else 'manual',
                    'created_at': item.get('created_at', '') if isinstance(item, dict) else '',
                })

            if hit_count >= self.HOT_THRESHOLD:
                hot.extend(alias_entries)
            else:
                cold.extend(alias_entries)
            by_entity[entity_name] = alias_entries

        return {
            'hot_aliases': hot,
            'cold_aliases': cold,
            'by_entity': by_entity,
            'hot_count': len(hot),
            'cold_count': len(cold),
        }

    def persist_hot_cold(self) -> Dict:
        """持久化热/冷别名到独立 JSON 文件（v2.1.3）"""
        stats = self.get_alias_stats()
        try:
            with open(self._hot_path(), 'w', encoding='utf-8') as f:
                json.dump({
                    'generated_at': datetime.date.today().isoformat(),
                    'threshold': self.HOT_THRESHOLD,
                    'aliases': stats['hot_aliases'],
                }, f, ensure_ascii=False, indent=2)
            with open(self._cold_path(), 'w', encoding='utf-8') as f:
                json.dump({
                    'generated_at': datetime.date.today().isoformat(),
                    'threshold': self.COLD_THRESHOLD,
                    'aliases': stats['cold_aliases'],
                }, f, ensure_ascii=False, indent=2)
            return {'hot_count': stats['hot_count'], 'cold_count': stats['cold_count']}
        except Exception as e:
            print(f"[entity_aliases] 热冷持久化失败: {e}")
            return {'error': str(e)}

    # ═══════════════════════════════════════════════════════════════
    # v2.2.0: alias 生命周期管理
    # ═══════════════════════════════════════════════════════════════

    def get_lifecycle_stats(self) -> Dict:
        """生命周期评估（跟随父实体策略）

        返回:
            {
                'active_aliases': [...],   # 父实体热（hit≥5）
                'downgraded_aliases': [...], # 父实体冷（hit<5）→ 降级保留
                'stale_aliases': [...],    # 父实体 90 天未出现 → stale 可清理
                'stats': {...},
            }
        """
        from entity_tracker import EntityTracker
        tracker = EntityTracker()
        data = self.load()

        active = []
        downgraded = []
        stale = []

        for entity_name, aliases in data.items():
            entity = tracker._find_entity(entity_name)
            if entity is None:
                # 父实体已不存在 → alias 直接 stale
                for item in aliases:
                    alias = item.get('alias', '') if isinstance(item, dict) else item
                    stale.append({
                        'alias': alias,
                        'entity_name': entity_name,
                        'status': 'stale_parent_missing',
                    })
                continue

            hit = entity.get('hit_count_30d', 0)
            last_seen = entity.get('last_seen_at', '1970-01-01')
            try:
                age = (datetime.date.today() - datetime.datetime.fromisoformat(last_seen).date()).days
            except Exception:
                age = self.STALE_PARENT_DAYS + 1  # 无时间戳 → 视为 stale

            for item in aliases:
                alias = item.get('alias', '') if isinstance(item, dict) else item
                if age > self.STALE_PARENT_DAYS:
                    # 父实体 90 天未出现 → stale
                    stale.append({
                        'alias': alias,
                        'entity_name': entity_name,
                        'status': 'stale_parent_inactive',
                        'parent_hit_count': hit,
                        'parent_age_days': age,
                    })
                elif hit >= self.HOT_THRESHOLD:
                    # 父实体热 → active
                    active.append({
                        'alias': alias,
                        'entity_name': entity_name,
                        'status': 'active',
                        'parent_hit_count': hit,
                    })
                else:
                    # 父实体冷 → downgraded
                    downgraded.append({
                        'alias': alias,
                        'entity_name': entity_name,
                        'status': 'downgraded',
                        'parent_hit_count': hit,
                    })

        return {
            'active_aliases': active,
            'downgraded_aliases': downgraded,
            'stale_aliases': stale,
            'stats': {
                'active_count': len(active),
                'downgraded_count': len(downgraded),
                'stale_count': len(stale),
                'total_aliases': len(active) + len(downgraded) + len(stale),
            },
        }

    def clean_stale_aliases(self, auto_delete: bool = True) -> dict:
        """清理 stale alias（v2.2.0）

        策略：跟随父实体
        - 父实体 90 天未出现 → alias stale
        - auto_delete=True → 从 aliases.json 移除（可被 auto_expand 重建）
        - auto_delete=False → 仅标记（保留查看）

        返回: {'cleaned': N, 'kept': M, 'stale': [...]}
        """
        stats = self.get_lifecycle_stats()
        stale = stats['stale_aliases']
        data = self.load()

        cleaned = 0
        kept = 0
        cleaned_details = []

        if auto_delete:
            # 按实体分组清理
            for item in stale:
                entity_name = item['entity_name']
                alias = item['alias']
                if entity_name in data:
                    # 移除该 alias
                    new_list = [
                        e for e in data[entity_name]
                        if (e.get('alias', '') if isinstance(e, dict) else e) != alias
                    ]
                    if len(new_list) != len(data[entity_name]):
                        cleaned += 1
                        cleaned_details.append(item)
                    data[entity_name] = new_list
                    # 实体无 alias → 移除空实体
                    if not data[entity_name]:
                        del data[entity_name]
            self.save(data)
        else:
            kept = len(stale)

        self.clear_priority_cache()  # v2.2.1: 失效缓存
        return {
            'cleaned': cleaned if auto_delete else 0,
            'kept': kept if not auto_delete else len(stale) - cleaned,
            'stale_details': stale[:10],
            'total_stale': len(stale),
        }


# ═══════════════════════════════════════════════════════════════
# CLI
# ═══════════════════════════════════════════════════════════════

def main():
    if len(sys.argv) < 2:
        print("Usage: python -m core.entity_aliases [list | get NAME | add NAME ALIAS | clear]")
        sys.exit(1)

    cmd = sys.argv[1]
    mgr = EntityAliases()

    if cmd == 'list':
        data = mgr.list_all()
        print(f"Total alias entries: {sum(len(v) for v in data.values())}")
        for name, aliases in list(data.items())[:10]:
            print(f"  {name}: {aliases}")
    elif cmd == 'get':
        if len(sys.argv) < 3:
            print("Usage: python -m core.entity_aliases get NAME")
            sys.exit(1)
        name = sys.argv[2]
        aliases = mgr.get_aliases(name)
        print(f"{name}: {aliases}")
    elif cmd == 'add':
        if len(sys.argv) < 4:
            print("Usage: python -m core.entity_aliases add NAME ALIAS")
            sys.exit(1)
        name, alias = sys.argv[2], sys.argv[3]
        success = mgr.add_alias(name, alias)
        print(f"{'✅' if success else '❌'} add '{alias}' to '{name}'")
    elif cmd == 'expand':
        # auto_expand 测试
        if len(sys.argv) < 4:
            print("Usage: python -m core.entity_aliases expand NAME TEXT")
            sys.exit(1)
        name = sys.argv[2]
        text = sys.argv[3]
        added = mgr.auto_expand(name, text)
        print(f"auto_expand '{name}': added {added}")
    elif cmd == 'clear':
        mgr.clear()
        print("✅ Aliases 已清空")
    elif cmd == 'hot-cold':
        # v2.1.3: 统计 + 持久化热冷别名
        stats = mgr.get_alias_stats()
        print(f"热别名: {stats['hot_count']} 个（hit ≥ {mgr.HOT_THRESHOLD}）")
        for a in stats['hot_aliases'][:10]:
            print(f"  🔥 {a['alias']} ({a['entity_name']}, hit={a['entity_hit_count']})")
        print(f"冷别名: {stats['cold_count']} 个（hit < {mgr.COLD_THRESHOLD}）")
        for a in stats['cold_aliases'][:5]:
            print(f"  🧊 {a['alias']} ({a['entity_name']}, hit={a['entity_hit_count']})")
        result = mgr.persist_hot_cold()
        print(f"✅ 持久化: {result}")
    elif cmd == 'lifecycle':
        # v2.2.0: 生命周期评估
        stats = mgr.get_lifecycle_stats()
        s = stats['stats']
        print(f"别名生命周期（跟随父实体策略）:")
        print(f"  🟢 active: {s['active_count']} 个（父实体 hit≥{mgr.HOT_THRESHOLD}）")
        for a in stats['active_aliases'][:5]:
            print(f"    - {a['alias']} ({a['entity_name']}, hit={a['parent_hit_count']})")
        print(f"  🟡 downgraded: {s['downgraded_count']} 个（父实体冷）")
        for a in stats['downgraded_aliases'][:5]:
            print(f"    - {a['alias']} ({a['entity_name']}, hit={a['parent_hit_count']})")
        print(f"  🔴 stale: {s['stale_count']} 个（父实体 {mgr.STALE_PARENT_DAYS} 天未出现）")
        for a in stats['stale_aliases'][:5]:
            print(f"    - {a['alias']} ({a['entity_name']}, {a.get('parent_age_days', '?')}d)")
    elif cmd == 'clean-stale':
        # v2.2.0: 清理 stale alias
        auto = len(sys.argv) < 3 or sys.argv[2] != '--keep'
        result = mgr.clean_stale_aliases(auto_delete=auto)
        print(f"清理结果: {result}")
    else:
        print(f"未知命令: {cmd}")


if __name__ == '__main__':
    main()
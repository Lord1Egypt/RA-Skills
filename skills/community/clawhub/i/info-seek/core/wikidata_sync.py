#!/usr/bin/env python3
"""
core/wikidata_sync.py — Infoseek Wikidata 同步器（v2.1.1 新增）

通过 Wikidata 公开 SPARQL API 拉取行业头部实体。
零依赖（公开 API，无需 auth）。

支持类别：
- AI_COMPANY: 人工智能公司
- TECH_COMPANY: 科技公司
- BANK: 银行
- UNIVERSITY: 大学
- AUTOMOBILE_MFR: 汽车制造商
"""

import sys
import json
import urllib.request
import urllib.error
import urllib.parse
from typing import List, Dict, Optional
from pathlib import Path

CORE_DIR = Path(__file__).parent
sys.path.insert(0, str(CORE_DIR))


def _dep_reg():
    """S7：外部依赖可用性统一经 dep_registry 事实层求值（懒加载，缺失回退）。"""
    try:
        import dep_registry as _dr
    except ImportError:
        from core import dep_registry as _dr  # type: ignore
    return _dr


# Wikidata QID 映射
WIKIDATA_CATEGORIES = {
    'AI_COMPANY': 'Q891723',          # AI company
    'TECH_COMPANY': 'Q783794',        # technology company
    'BANK': 'Q22687',                 # bank
    'UNIVERSITY': 'Q3918',            # university
    'AUTOMOBILE_MFR': 'Q786820',      # automobile manufacturer
    'SOFTWARE_COMPANY': 'Q1058912',   # software company
    'SEMICONDUCTOR': 'Q134290',       # semiconductor company
    'PUBLISHER': 'Q2085381',          # publisher
}


class WikidataSync:
    """v2.1.1 Wikidata 同步器"""

    ENDPOINT = 'https://query.wikidata.org/sparql'

    def __init__(self, language: str = 'zh', timeout: int = 15):
        self.language = language
        self.timeout = timeout

    def _query(self, sparql: str) -> Optional[Dict]:
        """执行 SPARQL 查询"""
        url = self.ENDPOINT + '?' + urllib.parse.urlencode({
            'query': sparql,
            'format': 'json',
        })
        try:
            req = urllib.request.Request(url, headers={
                'User-Agent': 'Infoseek/2.1.1',
                'Accept': 'application/json',
            })
            with urllib.request.urlopen(req, timeout=self.timeout) as resp:
                return json.loads(resp.read().decode('utf-8'))
        except (urllib.error.URLError, urllib.error.HTTPError, TimeoutError) as e:
            print(f"[wikidata_sync] 查询失败: {type(e).__name__}: {str(e)[:80]}")
            return None
        except Exception as e:
            print(f"[wikidata_sync] 异常: {type(e).__name__}: {str(e)[:80]}")
            return None

    def fetch_entities(self, category: str, limit: int = 50) -> List[Dict]:
        """从 Wikidata 拉取某类实体

        返回: [{'name': ..., 'wikidata_id': 'Q12345'}, ...]
        """
        if category not in WIKIDATA_CATEGORIES:
            return []

        qid = WIKIDATA_CATEGORIES[category]
        sparql = f"""
        SELECT ?item ?itemLabel WHERE {{
            ?item wdt:P31 wd:{qid} .
            SERVICE wikibase:label {{ bd:serviceParam wikibase:language "{self.language},en" }}
        }} LIMIT {limit}
        """

        result = self._query(sparql)
        if not result:
            return []

        entities = []
        for binding in result.get('results', {}).get('bindings', []):
            qid_value = binding['item']['value'].split('/')[-1]
            label = binding.get('itemLabel', {}).get('value', '')
            if label and label != qid_value:  # 过滤掉 ID 形式
                entities.append({
                    'name': label,
                    'wikidata_id': qid_value,
                    'category': category,
                    'source': 'wikidata',
                    'confidence': 0.7,
                })

        return entities

    def verify_existence(self, entity_name: str) -> bool:
        """Wikidata 验证实体存在

        用于 v2.1.0 entity_tracker 冷条目验证
        """
        sparql = f"""
        SELECT ?item WHERE {{
            ?item rdfs:label "{entity_name}"@{self.language} .
        }} LIMIT 1
        """
        result = self._query(sparql)
        if not result:
            return False
        return len(result.get('results', {}).get('bindings', [])) > 0

    async def verify_existence_async(self, entity_name: str) -> bool:
        """v2.5.0 MINOR 新增：async 版本；v2.5.1 PATCH: httpx 真异步 + 降级路径

        优先用 httpx.AsyncClient（不占线程池）；
        httpx 未装或初始化失败时降级到 asyncio.to_thread（兼容旧路径）。
        """
        import asyncio
        # v2.5.1: 尝试 httpx 真异步；S7：可用性经 dep_registry 统一求值
        try:
            if not _dep_reg().is_available("httpx"):
                raise ImportError
            import httpx
            if not hasattr(self, '_httpx_client') or self._httpx_client is None:
                self._httpx_client = httpx.AsyncClient(timeout=self.timeout)
            sparql = f"""
            SELECT ?item WHERE {{
                ?item rdfs:label "{entity_name}"@{self.language} .
            }} LIMIT 1
            """
            resp = await self._httpx_client.get(
                self.ENDPOINT,
                params={'query': sparql, 'format': 'json'},
                headers={'User-Agent': 'Infoseek/2.5.1'}
            )
            data = resp.json()
            return len(data.get('results', {}).get('bindings', [])) > 0
        except ImportError:
            # httpx 未装 → 降级到 asyncio.to_thread
            try:
                return await asyncio.to_thread(self.verify_existence, entity_name)
            except Exception:
                return False
        except Exception:
            return False

    async def verify_batch_async(self, entity_names: List[str]) -> Dict[str, bool]:
        """v2.5.0 新增：批量并发验证（asyncio.gather）"""
        import asyncio
        results = await asyncio.gather(
            *[self.verify_existence_async(name) for name in entity_names],
            return_exceptions=True,
        )
        out = {}
        for name, r in zip(entity_names, results):
            out[name] = bool(r) if not isinstance(r, Exception) else False
        return out

    def merge_to_dict(self, entities: List[Dict]) -> dict:
        """合并到 entities.py（标注 source='wikidata'）

        返回: {'added': N, 'skipped': M}
        """
        from entities import get_all_entities
        from entity_meta import _default_meta

        existing = {e['name'].lower() for e in get_all_entities()}
        added, skipped = [], []

        for ent in entities:
            if ent['name'].lower() in existing:
                skipped.append(ent['name'])
                continue

            # 补默认元数据
            ent.update(_default_meta())
            added.append(ent['name'])

        return {'added': added, 'skipped': skipped, 'added_count': len(added), 'skipped_count': len(skipped)}

    def fetch_top_companies(self, category: str = 'TECH_COMPANY', limit: int = 30) -> List[Dict]:
        """拉取头部公司（按 Wikidata 知名度）"""
        return self.fetch_entities(category, limit)


# ═══════════════════════════════════════════════════════════════
# CLI
# ═══════════════════════════════════════════════════════════════

def main():
    if len(sys.argv) < 2:
        print("Usage: python -m core.wikidata_sync [fetch CATEGORY | verify NAME]")
        sys.exit(1)

    cmd = sys.argv[1]
    sync = WikidataSync()

    if cmd == 'fetch':
        category = sys.argv[2] if len(sys.argv) > 2 else 'TECH_COMPANY'
        limit = int(sys.argv[3]) if len(sys.argv) > 3 else 30
        entities = sync.fetch_entities(category, limit=limit)
        print(f"Wikidata {category} (limit={limit}): 找到 {len(entities)} 个实体")
        for ent in entities[:10]:
            print(f"  - {ent['name']} ({ent['wikidata_id']})")
        result = sync.merge_to_dict(entities)
        print(f"\n合并到字典: {result}")
    elif cmd == 'verify':
        name = sys.argv[2] if len(sys.argv) > 2 else 'OpenAI'
        exists = sync.verify_existence(name)
        print(f"Wikidata 验证 '{name}': {'存在' if exists else '不存在'}")
    else:
        print(f"未知命令: {cmd}")


if __name__ == '__main__':
    main()
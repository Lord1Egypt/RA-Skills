#!/usr/bin/env python3
"""
core/entity_enricher.py — Infoseek LLM 实体抽取器（v2.1.0 新增）

从调研文本中自动抽取新实体候选（带置信度阈值 + 队列管理）。

工作流：
  1. extract_candidates(text): LLM 调用 → 候选列表
  2. suggest_additions(candidates): 过滤已存在 + 校验相似
  3. persist_suggestions(suggestions, auto_confirm): 入库或入 pending 队列

依赖：core/llm_router.py（4 provider 自动 fallback）
"""

import sys
import json
import re
from pathlib import Path
from typing import List, Dict, Optional
from datetime import date

CORE_DIR = Path(__file__).parent
sys.path.insert(0, str(CORE_DIR))

try:
    from state_dir import state_path
except ImportError:  # 作为 core 包导入时
    from .state_dir import state_path


class EntityEnricher:
    """v2.1.0 LLM 实体抽取器"""

    # 提示词模板
    EXTRACT_PROMPT = """从以下文本中提取实体，每条带置信度（0-1）。

文本：
{text}

输出格式（严格 JSON 数组）：
[
  {{"name": "实体名", "type": "ORG|PRODUCT|TECH|PERSON|METRIC", "confidence": 0.8, "alias": "可选别名"}}
]

只输出 JSON 数组，不要其他文字。"""

    def __init__(self,
                 confidence_threshold: float = 0.6,
                 auto_confirm_threshold: float = 0.85):
        self.confidence_threshold = confidence_threshold
        self.auto_confirm_threshold = auto_confirm_threshold

    def _call_llm(self, text: str) -> str:
        """调用 LLM（mock 模式返回模拟结果）"""
        try:
            from llm_router import llm_call
            prompt = self.EXTRACT_PROMPT.format(text=text[:1500])
            result = llm_call(prompt, max_tokens=300, prefer_cheap=True)
            return result['content']
        except Exception as e:
            return f"[]"  # fallback：返回空数组

    def _parse_llm_response(self, response: str) -> List[Dict]:
        """解析 LLM JSON 响应"""
        # 尝试直接 JSON 解析
        try:
            data = json.loads(response)
            if isinstance(data, list):
                return data
        except Exception:
            pass

        # fallback：从文本中提取 JSON 数组
        match = re.search(r'\[.*?\]', response, re.DOTALL)
        if match:
            try:
                data = json.loads(match.group(0))
                if isinstance(data, list):
                    return data
            except Exception:
                pass

        return []

    def extract_candidates(self, text: str, max_candidates: int = 20) -> List[Dict]:
        """从文本中抽取候选实体

        返回：[{"name": ..., "type": ..., "confidence": ..., "alias": ...}, ...]
        """
        if not text or len(text.strip()) < 50:
            return []

        response = self._call_llm(text)
        candidates = self._parse_llm_response(response)

        # 过滤：confidence ≥ 阈值
        filtered = [
            c for c in candidates
            if c.get('confidence', 0) >= self.confidence_threshold
            and c.get('name')
        ]
        return filtered[:max_candidates]

    def _entity_exists(self, name: str) -> bool:
        """检查实体是否已存在"""
        from entities import get_all_entities
        all_ents = get_all_entities()
        for e in all_ents:
            if e['name'].lower() == name.lower():
                return True
            # 检查别名
            for alias in e.get('aliases', []):
                if alias.lower() == name.lower():
                    return True
        return False

    def suggest_additions(self, candidates: List[Dict]) -> List[Dict]:
        """过滤已存在 → 返回建议入库的实体"""
        suggestions = []
        for c in candidates:
            name = c.get('name', '').strip()
            if not name or self._entity_exists(name):
                continue
            suggestions.append({
                'name': name,
                'aliases': [c.get('alias', name)] if c.get('alias') else [name],
                'category': c.get('type', 'UNKNOWN').upper(),
                'source': 'llm',
                'confidence': c.get('confidence', 0.0),
                'created_at': date.today().isoformat(),
                'last_verified_at': date.today().isoformat(),
                'last_seen_at': date.today().isoformat(),
                'hit_count_30d': 0,
            })
        return suggestions

    def persist_suggestions(self,
                            suggestions: List[Dict],
                            auto_confirm: bool = False) -> dict:
        """入库建议

        参数:
            suggestions: 候选实体列表
            auto_confirm: True = 自动入库；False = 仅入 pending 队列

        返回:
            {'auto_added': N, 'queued': M}
        """
        if not suggestions:
            return {'auto_added': 0, 'queued': 0}

        auto_added = 0
        queued = 0
        pending = self._load_pending()

        for s in suggestions:
            if auto_confirm and s['confidence'] >= self.auto_confirm_threshold:
                # 直接入库
                from entities import ORG_ENTITIES, PRODUCT_ENTITIES, TECH_ENTITIES, PERSON_ENTITIES, METRIC_ENTITIES
                target = {
                    'ORG': ORG_ENTITIES,
                    'PRODUCT': PRODUCT_ENTITIES,
                    'TECH': TECH_ENTITIES,
                    'PERSON': PERSON_ENTITIES,
                    'METRIC': METRIC_ENTITIES,
                }.get(s['category'], ORG_ENTITIES)
                target.append(s)
                auto_added += 1
            else:
                # 入 pending 队列
                pending.append(s)
                queued += 1

        self._save_pending(pending)
        return {'auto_added': auto_added, 'queued': queued}

    def _pending_path(self) -> Path:
        return state_path('pending_entities.json')

    def _load_pending(self) -> List[Dict]:
        path = self._pending_path()
        if not path.exists():
            return []
        try:
            with open(path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception:
            return []

    def _save_pending(self, pending: List[Dict]):
        path = self._pending_path()
        try:
            with open(path, 'w', encoding='utf-8') as f:
                json.dump(pending, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"[entity_enricher] 保存 pending 失败: {e}")

    def get_pending(self) -> List[Dict]:
        """返回当前 pending 队列"""
        return self._load_pending()

    def clear_pending(self):
        """清空 pending 队列"""
        self._save_pending([])


# ═══════════════════════════════════════════════════════════════
# CLI
# ═══════════════════════════════════════════════════════════════

def main():
    if len(sys.argv) < 2:
        print("Usage: python -m core.entity_enricher [extract <text> | pending | clear]")
        sys.exit(1)

    cmd = sys.argv[1]
    enricher = EntityEnricher()

    if cmd == 'extract':
        text = sys.argv[2] if len(sys.argv) > 2 else 'Apple released Vision Pro in 2024.'
        candidates = enricher.extract_candidates(text)
        suggestions = enricher.suggest_additions(candidates)
        print(f"抽取候选: {len(candidates)}")
        for c in candidates[:5]:
            print(f"  - {c.get('name')} ({c.get('type')}, conf={c.get('confidence')})")
        print(f"\n建议入库: {len(suggestions)}")
        for s in suggestions[:5]:
            print(f"  + {s['name']} (source={s['source']})")
    elif cmd == 'pending':
        pending = enricher.get_pending()
        print(f"Pending 队列 ({len(pending)} 条):")
        for s in pending[:10]:
            print(f"  - {s['name']} (conf={s.get('confidence')})")
    elif cmd == 'clear':
        enricher.clear_pending()
        print("✅ Pending 队列已清空")
    else:
        print(f"未知命令: {cmd}")


if __name__ == '__main__':
    main()
#!/usr/bin/env python3
"""
core/entity_meta.py — 实体元数据辅助（v2.1.0 新增）

为 entities.py 中所有实体补充 v2.1.0 元数据字段：
- created_at
- last_verified_at
- last_seen_at
- hit_count_30d
- source (manual / llm / wikidata)
- confidence (0-1)

向后兼容：v2.0.1 调用仍可访问原字段。
"""

import sys
from datetime import datetime, date
from pathlib import Path

CORE_DIR = Path(__file__).parent
sys.path.insert(0, str(CORE_DIR))


def _today_str() -> str:
    """今天日期 ISO 格式"""
    return date.today().isoformat()


def _default_meta() -> dict:
    """新实体的默认元数据"""
    today = _today_str()
    return {
        'created_at': today,
        'last_verified_at': today,
        'last_seen_at': today,
        'hit_count_30d': 0,
        'source': 'manual',
        'confidence': 1.0,
    }


def ensure_meta(entity: dict, source: str = 'manual', confidence: float = 1.0) -> dict:
    """确保单个实体有元数据（缺失则补默认值）

    参数:
        entity: 实体 dict（会被修改）
        source: 数据来源（manual/llm/wikidata）
        confidence: 置信度（0-1）
    """
    defaults = _default_meta()
    defaults['source'] = source
    defaults['confidence'] = confidence

    for k, v in defaults.items():
        if k not in entity:
            entity[k] = v
    return entity


def migrate_entities(entities: list, source: str = 'manual') -> dict:
    """批量迁移：给实体列表补元数据

    返回迁移摘要：{'migrated_count', 'already_count', 'total'}
    """
    migrated = 0
    already = 0
    for e in entities:
        if 'hit_count_30d' in e and 'created_at' in e:
            already += 1
        else:
            ensure_meta(e, source=source, confidence=1.0 if source == 'manual' else 0.7)
            migrated += 1

    return {
        'migrated_count': migrated,
        'already_count': already,
        'total': len(entities),
    }


def is_stale(entity: dict, threshold_days: int = 90) -> bool:
    """判断实体是否冷条目（90 天未识别）"""
    last_seen = entity.get('last_seen_at', '1970-01-01')
    try:
        last = datetime.fromisoformat(last_seen).date()
        age = (date.today() - last).days
        return age > threshold_days
    except Exception:
        return True


def apply_decay(entity: dict, half_life_days: int = 90) -> dict:
    """90 天半衰期衰减 hit_count_30d

    算法：age > 90 → hit_count *= 0.5^((age-90)/90)
    """
    last_seen = entity.get('last_seen_at', '1970-01-01')
    try:
        last = datetime.fromisoformat(last_seen).date()
        age = (date.today() - last).days
    except Exception:
        age = 365

    if age <= half_life_days:
        return entity  # 不衰减

    # 半衰期公式：每 90 天减半
    factor = 0.5 ** ((age - half_life_days) / half_life_days)
    entity['hit_count_30d'] = max(0, int(entity.get('hit_count_30d', 0) * factor))
    return entity


# ═══════════════════════════════════════════════════════════════
# CLI
# ═══════════════════════════════════════════════════════════════

def main():
    """CLI: python -m core.entity_meta migrate"""
    if len(sys.argv) < 2:
        print("Usage: python -m core.entity_meta [migrate | stats | decay]")
        sys.exit(1)

    cmd = sys.argv[1]

    if cmd == 'migrate':
        # 给 entities.py 所有实体补元数据
        from entities import get_all_entities
        entities = get_all_entities()
        result = migrate_entities(entities, source='manual')
        print(f"迁移完成: {result}")
        # 写回 entities.py（实际只更新内存对象）
        print(f"总实体数: {result['total']}, 新迁移: {result['migrated_count']}, 已有: {result['already_count']}")
    elif cmd == 'stats':
        from entities import get_all_entities, entity_count
        entities = get_all_entities()
        total_hit = sum(e.get('hit_count_30d', 0) for e in entities)
        sources = {}
        for e in entities:
            s = e.get('source', 'manual')
            sources[s] = sources.get(s, 0) + 1
        print(f"实体总数: {len(entities)}")
        print(f"总 hit_count: {total_hit}")
        print(f"按 source: {sources}")
    elif cmd == 'decay':
        from entities import get_all_entities
        entities = get_all_entities()
        decayed = 0
        for e in entities:
            before = e.get('hit_count_30d', 0)
            apply_decay(e)
            if e.get('hit_count_30d', 0) < before:
                decayed += 1
        print(f"已对 {decayed}/{len(entities)} 个实体应用衰减")
    else:
        print(f"未知命令: {cmd}")


if __name__ == '__main__':
    main()
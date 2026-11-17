#!/usr/bin/env python3
"""
core/conflict_v2.py — Infoseek 实体感知冲突检测 v2（v2.0.1 正式实现）

升级自 v2.0.0 临时方案，整合：
- core/ner.py 跨语言实体识别
- v1.8.0 conflict_detection 数值/文本冲突检测
- 新增：实体感知冲突（同一实体不同源的冲突）
"""

import sys
import re
import warnings
from pathlib import Path
from typing import List, Dict, Optional

# 添加 core/ 路径
CORE_DIR = Path(__file__).parent
sys.path.insert(0, str(CORE_DIR))

from ner import extract_entities

# ⚠️ 弃用声明：conflict_v2 为 v2.x 遗留实现，已停止演进。
# 新代码请使用 core/conflict_v3（detect_conflicts_v3）+ core/contradiction_scorer（score_contradiction）。
# 保留仅为向后兼容导入；计划于 v4.0.0 移除。
warnings.warn(
    "core/conflict_v2 已弃用（v2.x 遗留实现），请改用 core/conflict_v3 + core/contradiction_scorer。",
    DeprecationWarning,
    stacklevel=2,
)


def _detect_numeric_conflicts(values: List[dict]) -> dict:
    """v1 数值冲突检测（继承）"""
    if len(values) < 2:
        return None

    numbers = []
    for v in values:
        nums = re.findall(r'\d+(?:\.\d+)?', v['value'])
        if nums:
            numbers.append((nums, v))

    if len(numbers) < 2:
        return None

    all_lhs = [float(n[0][0]) for n in numbers if len(n[0]) > 0]
    all_rhs = [float(n[0][1]) if len(n[0]) > 1 else float(n[0][0]) for n in numbers if len(n[0]) > 0]

    if not all_lhs:
        return None

    delta = max(all_lhs + all_rhs) - min(all_lhs + all_rhs)
    avg = sum(all_lhs + all_rhs) / len(all_lhs + all_rhs)
    rel_delta = (delta / avg * 100) if avg > 0 else 0

    if rel_delta > 30:
        severity = 'high'
    elif rel_delta > 15:
        severity = 'medium'
    else:
        severity = 'low'

    return {
        'severity': severity,
        'delta': delta,
        'rel_delta_percent': round(rel_delta, 1),
    }


def detect_entity_conflicts(sources: List[Dict]) -> List[Dict]:
    """检测同一实体在不同源中的不同表述（v2.0.1 新增）

    算法:
      1. 抽取每个源的实体
      2. 对每个实体，找多个源中提到该实体的内容
      3. 比较同一实体的上下文（数值/观点）
      4. 输出实体级冲突列表
    """
    if not sources or len(sources) < 2:
        return []

    # 1) 收集每个源的 (entity, value) 对
    entity_data = {}  # entity_name → [{source_title, value, ...}]
    for source in sources:
        text = source.get('text', '') or source.get('snippet', '')
        if not text:
            continue
        entities = extract_entities(text)
        for ent in entities:
            ent_name = ent['entity_name']
            if ent_name not in entity_data:
                entity_data[ent_name] = []
            entity_data[ent_name].append({
                'source_title': source.get('title', 'Untitled'),
                'source_url': source.get('url', ''),
                'source_score': source.get('score', 0),
                'text_excerpt': text[:200],
                'entity_type': ent.get('entity_type', 'UNKNOWN'),
            })

    # 2) 对每个实体：检查是否有 ≥2 源提到
    conflicts = []
    for ent_name, mentions in entity_data.items():
        unique_sources = set(m['source_title'] for m in mentions)
        if len(unique_sources) < 2:
            continue

        # 3) 抽取每源的数值/观点
        values_per_source = {}
        for mention in mentions:
            text = mention['text_excerpt']
            nums = re.findall(r'\d+(?:\.\d+)?(?:\s*[\-~到至]\s*\d+(?:\.\d+)?)?\s*%?', text)
            if nums:
                key = mention['source_title']
                if key not in values_per_source:
                    values_per_source[key] = []
                values_per_source[key].extend(nums)

        if len(values_per_source) < 2:
            continue

        # 4) 构造冲突条目
        conflict = {
            'conflict_type': 'entity_aware',
            'entity_name': ent_name,
            'entity_type': mentions[0]['entity_type'],
            'mentions_count': len(mentions),
            'unique_sources_count': len(unique_sources),
            'sources': [
                {
                    'title': m['source_title'],
                    'url': m['source_url'],
                    'score': m['source_score'],
                    'extracted_values': list(set(values_per_source.get(m['source_title'], [])))[:5],
                }
                for m in mentions
            ],
        }

        # 5) 数值差距评估
        all_values = [v for values in values_per_source.values() for v in values]
        if all_values:
            nums_only = [float(re.search(r'\d+(?:\.\d+)?', v).group()) for v in all_values if re.search(r'\d', v)]
            if nums_only and len(nums_only) >= 2:
                delta = max(nums_only) - min(nums_only)
                avg = sum(nums_only) / len(nums_only)
                rel = (delta / avg * 100) if avg > 0 else 0
                conflict['severity'] = 'high' if rel > 30 else 'medium' if rel > 15 else 'low'
                conflict['delta'] = round(delta, 2)
                conflict['rel_delta_percent'] = round(rel, 1)

        conflicts.append(conflict)

    # 按严重度排序
    severity_order = {'high': 3, 'medium': 2, 'low': 1}
    conflicts.sort(key=lambda c: -severity_order.get(c.get('severity', 'low'), 0))
    return conflicts


def detect_conflicts_v2(sources: List[Dict], subject: str = '',
                         use_v1: bool = True) -> Dict:
    """冲突检测 v2 入口（v2.0.1 正式实现）

    整合：
      1. v1 数值/文本冲突（use_v1=True 时调用）
      2. v2 实体感知冲突（detect_entity_conflicts）
      3. 跨源实体覆盖度统计

    参数:
        sources: 来源列表
        subject: 调研主题
        use_v1: 是否同时调用 v1 数值冲突检测

    返回:
        {
            'conflicts': [...],  # 合并所有冲突
            'entity_conflicts': [...],  # 仅实体感知冲突
            'entity_coverage': [...],  # 各源实体覆盖率
            'summary': '...',
            'version': '2.0.1',
        }
    """
    result = {
        'conflicts': [],
        'entity_conflicts': [],
        'entity_coverage': [],
        'summary': '',
        'version': '2.0.1',
        'subject': subject,
        'total_sources': len(sources),
    }

    if not sources or len(sources) < 2:
        result['summary'] = '来源不足 2 个，无法检测冲突'
        return result

    # 1) v1 数值/文本冲突
    if use_v1:
        try:
            from conflict_detection import detect_conflicts as v1_detect
            v1_result = v1_detect(sources, subject=subject)
            result['conflicts'] = v1_result.get('conflicts', [])
            if 'v2_entity_coverage' in v1_result:
                result['entity_coverage'] = v1_result['v2_entity_coverage']
        except ImportError:
            pass

    # 2) v2 实体感知冲突
    result['entity_conflicts'] = detect_entity_conflicts(sources)

    # 3) 跨源实体覆盖度
    all_entities = set()
    per_source_entities = {}
    for source in sources:
        text = source.get('text', '') or source.get('snippet', '')
        entities = extract_entities(text)
        ent_names = set(e['entity_name'] for e in entities)
        per_source_entities[source.get('title', 'Untitled')] = ent_names
        all_entities.update(ent_names)

    coverage_data = []
    for title, ent_set in per_source_entities.items():
        coverage = len(ent_set & all_entities) / len(all_entities) if all_entities else 0
        coverage_data.append({
            'source': title,
            'entities_count': len(ent_set),
            'coverage_percent': round(coverage * 100, 1),
            'entities': list(ent_set)[:5],
        })
    result['entity_coverage'] = coverage_data

    # 4) 合并冲突
    result['conflicts'].extend([
        {
            **ec,
            'origin': 'entity_aware_v2',
        }
        for ec in result['entity_conflicts']
    ])

    # 5) 摘要
    result['summary'] = (
        f'v2.0.1 冲突检测：{len(result["conflicts"])} 总冲突 '
        f'({len(result["entity_conflicts"])} 实体感知)，'
        f'覆盖 {len(all_entities)} 实体'
    )

    return result


# ═══════════════════════════════════════════════════════════════
# CLI 测试
# ═══════════════════════════════════════════════════════════════

if __name__ == '__main__':
    sources = [
        {'title': '金属学会', 'url': '#1', 'score': 85,
         'text': '宝钢工艺圆盘刀重叠量 20-30%。'},
        {'title': '设备厂商', 'url': '#2', 'score': 72,
         'text': '宝钢推荐 15-25%。'},
        {'title': '论文', 'url': '#3', 'score': 65,
         'text': '宁德时代 CATL 25-35% 时最优。'},
    ]
    result = detect_conflicts_v2(sources, subject='钢卷分切工艺')
    print(f'总冲突: {len(result["conflicts"])}')
    print(f'实体感知冲突: {len(result["entity_conflicts"])}')
    print(f'摘要: {result["summary"]}')
    print(f'\\n实体感知冲突详情:')
    for ec in result['entity_conflicts']:
        print(f'  {ec["entity_name"]} ({ec["entity_type"]}): {ec["unique_sources_count"]} 源, severity={ec.get("severity", "?")}')
        for s in ec['sources']:
            print(f'    - {s["title"]}: values={s["extracted_values"]}')
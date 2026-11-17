#!/usr/bin/env python3
"""
conflict_detection.py — Infoseek 冲突检测器（v1.8.0）

检测多个来源中对**同一事实**的**不同表述/数值/观点**的冲突。

算法:
  1. 提取所有来源中的关键事实三元组（subject, predicate, value）
  2. 按 subject+predicate 分组
  3. 比较 value 的差异（数值差异 / 文本语义差异）
  4. 输出冲突列表（带严重程度评估）

返回:
  {
    "conflicts": [
      {
        "subject": "钢卷分切圆盘刀重叠量",
        "predicate": "推荐范围",
        "values": [
          {"source": "...", "value": "20-30%", "score": 85},
          {"source": "...", "value": "15-25%", "score": 70},
        ],
        "severity": "high|medium|low",
        "type": "numeric|text",
        "delta": 5  # 百分比差距
      }
    ],
    "summary": "发现 N 个冲突"
  }
"""

import re
import sys
from pathlib import Path
from typing import List, Optional


# 数值事实模式（数字 + 单位）
NUMERIC_PATTERNS = [
    # 百分比：20-30%、20%~30%
    (r'(\d+(?:\.\d+)?)\s*[\-~到至]\s*(\d+(?:\.\d+)?)\s*%', 'range_percent'),
    (r'(\d+(?:\.\d+)?)\s*%', 'single_percent'),
    # 数值 + 单位：5.2 mm、12 kg
    (r'(\d+(?:\.\d+)?)\s*(mm|cm|m|kg|g|MPa|psi|nm|um|μm|°C|°F|m/s|rpm)', 'value_with_unit'),
    # 单一数值
    (r'(\d+(?:\.\d+)?)', 'number_only'),
]


def extract_numeric_facts(text: str) -> List[dict]:
    """从文本中提取数值事实（去重 + 优先级去重）"""
    seen_spans = set()
    facts = []

    # 按优先级提取（长模式优先）
    for pattern, fact_type in NUMERIC_PATTERNS:
        for m in re.finditer(pattern, text):
            span = m.span()
            # 去重：与已发现的 span 重叠 → 跳过
            if any(s <= span[0] < e or s < span[1] <= e for s, e in seen_spans):
                continue
            seen_spans.add(span)

            value_str = m.group(0)
            context_start = max(0, m.start() - 30)
            context = text[context_start:m.end() + 30].strip()
            facts.append({
                'value': value_str,
                'type': fact_type,
                'context': context,
                'span': span,
            })
    return facts


def detect_numeric_conflict(values: List[dict]) -> dict:
    """检测数值冲突

    values: [{'value_str': '20-30%', 'source': 'A', ...}, ...]
    """
    if len(values) < 2:
        return None

    # 提取所有数字
    numbers = []
    for v in values:
        nums = re.findall(r'\d+(?:\.\d+)?', v['value'])
        if nums:
            numbers.append((nums, v))

    if len(numbers) < 2:
        return None

    # 计算差距
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


def detect_conflicts(sources: list, subject: str = "") -> dict:
    """检测跨来源的事实冲突（v1.8.0 v1）

    参数:
        sources: [{'text': '...', 'title': '...', 'url': '...', 'score': 0}, ...]
        subject: 调研主题（用于过滤）

    返回:
        {
          'conflicts': [...],
          'summary': 'N 个冲突',
          'total_sources': len(sources),
        }
    """
    if not sources or len(sources) < 2:
        return {
            'conflicts': [],
            'summary': '来源不足 2 个，无法检测冲突',
            'total_sources': len(sources),
        }

    # 1) 提取所有数值事实
    source_facts = []
    for s in sources:
        text = s.get('text', '') or s.get('snippet', '')
        title = s.get('title', 'Untitled')
        facts = extract_numeric_facts(text)
        source_facts.append({
            'source_title': title,
            'source_url': s.get('url', ''),
            'source_score': s.get('score', 0),
            'facts': facts,
        })

    # 2) 按"核心实体"分组（聚焦"修饰哪个实体"）
    # 策略：context 中出现 0个或多个"实体词典"中的词，使用第一个匹配的实体作为 key
    ENTITY_DICT = {
        '重叠量', '侧隙', '张力', '锥度', '张力', '重叠',
        '刀轴', '重叠', '锥度张力', '偏振', '同轴度',
        '重叠', '间隙', '重合', '重叠率', '重叠角',
        '温度', '压力', '速度', '功率', '电压', '电流',
        '直径', '宽度', '厚度', '长度', '高度', '深度',
        '含量', '比例', '占比', '浓度', '纯度',
        '频率', '转速', '进给', '切割深度', '入刀', '出刀',
        '精度', '公差', '粗糙度', '圆度', '垂直度',
    }

    conflict_groups = {}
    for sf in source_facts:
        for fact in sf['facts'][:20]:  # 限制每源事实数
            text = fact['context']
            value_str = fact['value']
            v_pos = text.find(value_str)
            if v_pos < 0:
                v_pos = len(text) // 2

            # 1) 找 context 中最近实体（在数字前后 ±20 字符内）
            entity_found = None
            for entity in ENTITY_DICT:
                # 在数字前后 ±10 字符内查找
                start = max(0, v_pos - 10)
                end = min(len(text), v_pos + len(value_str) + 10)
                nearby = text[start:end]
                if entity in nearby:
                    e_pos = nearby.find(entity) + start
                    if entity_found is None or abs(e_pos - v_pos) < abs(entity_found[1] - v_pos):
                        entity_found = (entity, e_pos)
            if entity_found:
                context_key = entity_found[0]  # 直接用 entity_found[0] 不重复
            else:
                # 2) fallback: 数字前最后 4 个汉字
                before_text = text[:v_pos]
                chinese_before = re.findall(r'[\u4e00-\u9fff]', before_text)
                context_key = ''.join(chinese_before[-4:])

            if not context_key or len(context_key) < 2:
                continue

            if context_key not in conflict_groups:
                conflict_groups[context_key] = []
            conflict_groups[context_key].append({
                'source_title': sf['source_title'],
                'source_url': sf['source_url'],
                'source_score': sf['source_score'],
                'value': fact['value'],
                'fact_type': fact['type'],
                'context': fact['context'],
            })

    # 3) 冲突判定（同一 context_key 下有 ≥2 个不同 value，且来源不同）
    conflicts = []
    for context_key, fact_list in conflict_groups.items():
        # 按 value 字符串去重
        seen_values = {}
        for f in fact_list:
            v = f['value']
            if v not in seen_values:
                seen_values[v] = f
            else:
                seen_values[v]['source_count'] = seen_values[v].get('source_count', 1) + 1

        unique_values = list(seen_values.values())
        if len(unique_values) < 2:
            continue  # 单一值，无冲突

        # 跨源判定：来源数量 ≥ 2
        unique_sources = set(v['source_title'] for v in unique_values)
        if len(unique_sources) < 2:
            continue  # 同一源多处引用同值，不算冲突

        # 数值冲突检测
        if any('number' in uv.get('fact_type', '') or 'value' in uv.get('fact_type', '') for uv in unique_values):
            numeric_assessment = detect_numeric_conflict(unique_values)
            if numeric_assessment:
                conflicts.append({
                    'subject': context_key,
                    'predicate': 'value_range',
                    'values': [{
                        'source_title': uv['source_title'],
                        'source_url': uv['source_url'],
                        'source_score': uv['source_score'],
                        'value': uv['value'],
                    } for uv in unique_values],
                    'type': 'numeric',
                    'severity': numeric_assessment['severity'],
                    'delta': numeric_assessment['delta'],
                    'rel_delta_percent': numeric_assessment['rel_delta_percent'],
                })
        else:
            # 非数值冲突（文本表述差异）
            conflicts.append({
                'subject': context_key,
                'predicate': 'statement',
                'values': [{
                    'source_title': uv['source_title'],
                    'source_url': uv['source_url'],
                    'source_score': uv['source_score'],
                    'value': uv['value'],
                } for uv in unique_values],
                'type': 'text',
                'severity': 'medium',  # 文本表述差异默认 medium
            })

    # 按严重度排序
    severity_order = {'high': 3, 'medium': 2, 'low': 1}
    conflicts.sort(key=lambda c: -severity_order.get(c.get('severity', 'low'), 0))

    return {
        'conflicts': conflicts[:20],  # 最多 20 个冲突
        'summary': f'检测到 {len(conflicts)} 个跨源冲突（共 {len(sources)} 来源）',
        'total_sources': len(sources),
        'subject': subject,
    }


# ═══════════════════════════════════════════════════════════════
# CLI 入口
# ═══════════════════════════════════════════════════════════════

if __name__ == '__main__':
    import json

    if len(sys.argv) < 2:
        print("Usage: python conflict_detection.py <sources.json>")
        sys.exit(1)

    sources_path = sys.argv[1]
    with open(sources_path, 'r', encoding='utf-8') as f:
        sources = json.load(f)

    result = detect_conflicts(sources)
    print(json.dumps(result, ensure_ascii=False, indent=2))

#!/usr/bin/env python3
"""
MBTI Report Generator - Bilingual reports
"""

from typing import Dict, List

def generate_report(type_code: str, scores: Dict, clarity_levels: Dict) -> str:
    """
    Generate comprehensive bilingual report
    
    Args:
        type_code: MBTI type like "INFP"
        scores: Dict of dimension scores
        clarity_levels: Dict of clarity for each dimension
    """
    from lib.mbti_types import get_type
    
    type_data = get_type(type_code)
    if not type_data:
        return "Type not found"
    
    name_en = type_data.get("name_en", "")
    name_cn = type_data.get("name_cn", "")
    summary = type_data.get("summary", "")
    summary_cn = type_data.get("summary_cn", "")
    strengths = type_data.get("strengths", [])
    weaknesses = type_data.get("weaknesses", [])
    careers = type_data.get("careers", [])
    relationships = type_data.get("relationships", {})
    
    # Calculate overall clarity
    total_clarity = sum(c[0] for c in clarity_levels.values()) / len(clarity_levels)
    
    # Build report
    report = f"""
╔══════════════════════════════════════════════════════════════════╗
║                                                                  ║
║              MBTI PERSONALITY ANALYSIS REPORT                   ║
║                  MBTI 人格分析报告                             ║
║                                                                  ║
╠══════════════════════════════════════════════════════════════════╣
║                                                                  ║
║   🧠 {type_code}                                            ║
║      {name_en}                                         ║
║      {name_cn}                                            ║
║                                                                  ║
║   ─────────────────────────────────────────────────────────   ║
║                                                                  ║
║   Overall Clarity / 综合清晰度: {total_clarity:.0f}%                          ║
║                                                                  ║
║   Dimension Scores / 维度得分:                                   ║
║     • Energy / 能量:      {scores.get('EI', 50):.0f}% → {'E' if scores.get('EI', 50) > 50 else 'I'}                                     ║
║     • Information / 信息: {scores.get('SN', 50):.0f}% → {'S' if scores.get('SN', 50) > 50 else 'N'}                                     ║
║     • Decisions / 决策: {scores.get('TF', 50):.0f}% → {'T' if scores.get('TF', 50) > 50 else 'F'}                                     ║
║     • Structure / 结构: {scores.get('JP', 50):.0f}% → {'J' if scores.get('JP', 50) > 50 else 'P'}                                     ║
║                                                                  ║
║   ─────────────────────────────────────────────────────────   ║
║                                                                  ║
║   Brief Summary / 简介:                                        ║
║   {summary[:60]}                                               ║
║   {summary_cn[:50]}                                            ║
║                                                                  ║
╚══════════════════════════════════════════════════════════════════╝
"""
    
    report += f"""

╔══════════════════════════════════════════════════════════════════╗
║                   STRENGTHS / 优势                           ║
╠══════════════════════════════════════════════════════════════════╣"""

    for i, s in enumerate(strengths[:5], 1):
        report += f"""
║   {i}. {s[:60]:<60} ║"""

    report += """

╚══════════════════════════════════════════════════════════════════╝

╔══════════════════════════════════════════════════════════════════╗
║                   WEAKNESSES / 劣势                         ║
╠══════════════════════════════════════════════════════════════════╣"""

    for i, w in enumerate(weaknesses[:5], 1):
        report += f"""
║   {i}. {w[:60]:<60} ║"""

    report += """

╚══════════════════════════════════════════════════════════════════╝

╔══════════════════════════════════════════════════════════════════╗
║                   CAREERS / 职业建议                       ║
╠══════════════════════════════════════════════════════════════════╣"""

    for i, c in enumerate(careers[:5], 1):
        report += f"""
║   {i}. {c[:60]:<60} ║"""

    # Best matches
    best_matches = relationships.get("best", [])
    challenging = relationships.get("challenging", [])
    
    report += """

╚══════════════════════════════════════════════════════════════════╝

╔══════════════════════════════════════════════════════════════════╗
║              COMPATIBLE TYPES / 性格匹配                    ║
╠══════════════════════════════════════════════════════════════════╣
║                                                                  ║
║   🌟 Best Match / 最佳匹配:                                  ║
"""

    for m in best_matches[:3]:
        report += f"""║      {m}                                                     ║
"""

    report += """║                                                                  ║
║   ⚠️ Challenging / 挑战类型:                                  ║"""

    for m in challenging[:2]:
        report += f"""║      {m}                                                     ║
"""

    report += """
╚══════════════════════════════════════════════════════════════════╝
"""
    
    return report


def generate_summary_report(type_code: str, scores: Dict) -> str:
    """Generate brief summary report"""
    from lib.mbti_types import get_type
    
    type_data = get_type(type_code)
    if not type_data:
        return "Type not found"
    
    name_en = type_data.get("name_en", "")
    name_cn = type_data.get("name_cn", "")
    summary = type_data.get("summary", "")[:80]
    summary_cn = type_data.get("summary_cn", "")[:60]
    
    return f"""
╔══════════════════════════════════════════════════════════════════╗
║                  YOUR PERSONALITY TYPE                      ║
║                    您的性格类型                          ║
╠══════════════════════════════════════════════════════════════════╣
║                                                                  ║
║   🧠 {type_code}                                             ║
║      {name_en}                                          ║
║      {name_cn}                                             ║
║                                                                  ║
║   Summary / 简介:                                            ║
║   {summary[:65]}                                  ║
║   {summary_cn[:50]}                                           ║
║                                                                  ║
║   Dimension Breakdown / 维度分析:                               ║
║     EI: {scores.get('EI', 50):.0f}% → {'Extraversion' if scores.get('EI', 50) > 50 else 'Introversion'}                          ║
║     SN: {scores.get('SN', 50):.0f}% → {'Sensing' if scores.get('SN', 50) > 50 else 'Intuition'}                              ║
║     TF: {scores.get('TF', 50):.0f}% → {'Thinking' if scores.get('TF', 50) > 50 else 'Feeling'}                              ║
║     JP: {scores.get('JP', 50):.0f}% → {'Judging' if scores.get('JP', 50) > 50 else 'Perceiving'}                            ║
║                                                                  ║
╚══════════════════════════════════════════════════════════════════╝
"""

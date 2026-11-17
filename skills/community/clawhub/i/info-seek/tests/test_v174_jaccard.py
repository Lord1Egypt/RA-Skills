#!/usr/bin/env python3
"""v1.7.4 PATCH 沙箱验证：关键词 Jaccard 修复 TF-IDF"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent / 'scripts'))

from anchor_adapter import (
    compute_semantic_similarity,
    _jaccard_similarity,
    _tfidf_similarity,  # alias
    _extract_keywords_three_run,
)


# 3 个英文源（与 v1.7.3 测试相同）
en_text_1 = """
AI Agent Skill is a structured capability for autonomous systems that can plan,
execute, and adapt across tasks. Skills combine tool use, prompt templates,
and knowledge retrieval to enable reliable agent behavior.
"""

en_text_2 = """
Last30days Skill scans recent community discussions from Hacker News,
Reddit, and X.com to surface emerging AI Agent techniques and trends.
The Skill integrates with Claude Code workflows for daily briefings.
"""

en_text_3 = """
Quant 2026 strategy combines KDJ golden cross with MACD bottom divergence
to detect multi-timeframe alignment. The Skill emphasizes daily entry timing
with strict risk management and no leverage during high-volatility regimes.
"""

# 3 个对应 subject
subject_1 = "AI Agent Skill"
subject_2 = "Last30days"
subject_3 = "2026 Quant Strategy"

# 中文源（验证中文不退化）
zh_text = """
钢卷分切是冷轧带钢的关键工序，需要控制圆盘刀重叠量、侧隙、锥度张力。
大直径钢卷分切内部宽度不均主要源自锥度张力缺失、刀轴三失配、
材料板形遗传、检验拦截失效这四个维度。
"""
zh_subject = "钢卷分切工艺"


print("=" * 70)
print("v1.7.4 PATCH 验证：关键词集合 Jaccard 相似度")
print("=" * 70)

# 测试 1: 英文源相似度
print("\n【测试 1】英文源 Jaccard 相似度（应≥15）")
print("-" * 70)
for i, (text, subj) in enumerate([
    (en_text_1, subject_1),
    (en_text_2, subject_2),
    (en_text_3, subject_3),
]):
    sim_jaccard = _jaccard_similarity(text, subj)
    sim_default = compute_semantic_similarity(text, subj)  # 默认 jaccard
    sim_tfidf = _tfidf_similarity(text, subj)  # alias
    print(f"  {subj:30s} → Jaccard={sim_jaccard:3d}  默认方法={sim_default:3d}  TF-IDF别名={sim_tfidf:3d}")

# 测试 2: 中文源相似度
print("\n【测试 2】中文源 Jaccard 相似度（应≥15）")
print("-" * 70)
sim_zh_jaccard = _jaccard_similarity(zh_text, zh_subject)
sim_zh_default = compute_semantic_similarity(zh_text, zh_subject)
print(f"  {zh_subject:30s} → Jaccard={sim_zh_jaccard:3d}  默认方法={sim_zh_default:3d}")

# 测试 3: 三跑择优
print("\n【测试 3】三跑关键词提取（英文源 #1）")
print("-" * 70)
kw = _extract_keywords_three_run(en_text_1, max_keywords=20)
print(f"  AI Agent Skill 关键词数: {len(kw)}")
print(f"  Top-10: {list(kw)[:10]}")

# 测试 4: v1.7.3 vs v1.7.4 对比
print("\n【测试 4】v1.7.3 公式 vs v1.7.4 修复对比")
print("-" * 70)
print("  v1.7.3 公式：常数 stub（无 log）→ 英文源 0/100")
print("  v1.7.4 修复：关键词 Jaccard（summa+jieba+regex 三跑）")

# 验证 method="tfidf" 仍可用（向后兼容）
print("\n【测试 5】method='tfidf' 向后兼容（应走 jaccard）")
print("-" * 70)
import warnings
with warnings.catch_warnings(record=True) as w:
    warnings.simplefilter("always")
    sim_compat = compute_semantic_similarity(en_text_1, subject_1, method="tfidf")
    if w:
        print(f"  ⚠️ 触发 DeprecationWarning: {str(w[0].message)[:80]}...")
    print(f"  method='tfidf' → {sim_compat}（内部走 jaccard）")

print("\n" + "=" * 70)
print("结论：v1.7.4 修复")
print("=" * 70)
all_en = [_jaccard_similarity(t, s) for t, s in [
    (en_text_1, subject_1), (en_text_2, subject_2), (en_text_3, subject_3)
]]
print(f"英文源 Jaccard 范围: {min(all_en)}-{max(all_en)}（期望 ≥15）")
print(f"中文源 Jaccard: {_jaccard_similarity(zh_text, zh_subject)}（期望 ≥15）")
print(f"向后兼容 method='tfidf': {sim_compat}（期望 = jaccard 结果）")

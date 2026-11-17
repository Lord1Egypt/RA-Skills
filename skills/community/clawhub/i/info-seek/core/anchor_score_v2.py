#!/usr/bin/env python3
"""
core/anchor_score_v2.py — Infoseek v2 评分（mod-v2.0.2 重构）

版本维度声明（v1.8.1 治理）：v2.0.2 为「模块内部版本 mod-v」，非 skill 对外版本
（见 scripts/mcp_tools_common.py:SKILL_VERSION），不可比较大小。

v2.0.2 目标：脱离 v1 shim，纯函数式评分

设计要点：
1. 纯函数（无副作用，不修改 source dict）
2. 模块化（trust_bonus + jaccard + domain_bonus 各算各的）
3. 可测试（每个评分维度可独立测试）
4. 向后兼容（v1 shim 仍可用，但内部调 v2）

API：
- compute_score_v2(source, subject) → 评分 dict
- compute_trust_bonus_v2(url, platform, domain) → 0-30
- compute_jaccard_v2(text, subject) → 0-100
- compute_domain_bonus_v2(source, profile) → 0-20
- compute_final_score_v2(...) → 聚合
"""

import sys
import re
import datetime
from pathlib import Path
from typing import Optional, Dict, List

CORE_DIR = Path(__file__).parent
sys.path.insert(0, str(CORE_DIR))


def compute_trust_bonus_v2(url: str, platform: str = '',
                          domain: str = 'general') -> int:
    """v2.0.2 信任源加权（核心/trust_sources.compute_trust_bonus 包装）"""
    try:
        from trust_sources import compute_trust_bonus
        return compute_trust_bonus(url or '', domain, platform)
    except Exception:
        return 0


def compute_jaccard_v2(text: str, subject: str) -> int:
    """v2.0.2 关键词 Jaccard 相似度（v1.7.4 Jaccard 包装）"""
    if not text or not subject:
        return 0
    try:
        sys.path.insert(0, str(Path(__file__).parent))
        from anchor_adapter import _jaccard_similarity
        return _jaccard_similarity(text, subject)
    except Exception:
        return 0


def compute_decay_factor_v2(days_since_published: int) -> float:
    """v2.0.2 时间衰减因子（与 v1.5.0 一致）"""
    if days_since_published < 30:
        return 1.0
    elif days_since_published < 90:
        return 0.9
    elif days_since_published < 180:
        return 0.7
    elif days_since_published < 365:
        return 0.5
    else:
        return 0.3


def compute_cross_platform_v2(platforms: int) -> int:
    """v2.0.2 跨平台分布度（v1.6.0 第 6 维）"""
    if platforms <= 1:
        return 0
    return min(100, (platforms - 1) * 25)


def compute_domain_bonus_v2(source: dict, profile: Optional[dict] = None,
                            prefer_kb: bool = False, subject: str = '') -> int:
    """v2.0.2 领域加权（单源委托 domain_router.trust_source_bonus）；v1.7.2 收敛

    subject 优先（G12）：主链路 source 通常无 'subject' 键，此前恒返回 0。
    """
    if not profile:
        subj = subject or source.get('subject', '') or source.get('_subject', '')
        if not subj:
            return 0
        try:
            from domain_router import detect_domain
            routing = detect_domain(subj)
            if routing.get('profile_path'):
                profile = {
                    'name': routing['domain'],
                    'raw': open(routing['profile_path'], encoding='utf-8').read(),
                }
        except Exception:
            return 0

    if not profile:
        return 0

    try:
        from domain_router import trust_source_bonus, kb_intersect_bonus, domain_bonus_cap
    except ImportError:
        return 0  # 单源不可用 → 不加分

    bonus = trust_source_bonus(source, profile)
    if prefer_kb:
        bonus += kb_intersect_bonus(source, profile)
    # v1.8.3 §8.4：cap 委托 domain_router.domain_bonus_cap()（原硬编码 20 不跟随 env
    # INFOSEEK_DOMAIN_BONUS_CAP → 声明化配置半失效；现与 apply_profile_to_score 同源）
    return min(bonus, domain_bonus_cap())


def compute_base_score_v2(source: dict, subject: str = '') -> float:
    """v2.0.2 基础评分（四维 base；v1.5.0 曾五维，v2 合并信任源为加权层）

    计算 4 维：
    - interaction（互动深度）
    - topic_match（主题一致性）
    - credibility（来源可信度）
    - llm_readability（LLM 上下文可读性）
    """
    interaction = source.get('interaction', source.get('score', 50))
    topic_match = source.get('topic_match', 50)
    credibility = source.get('credibility', 50)
    llm_readability = source.get('llm_readability', 50)

    base = (
        interaction * 0.20 +
        topic_match * 0.30 +
        credibility * 0.40 +
        llm_readability * 0.10
    )
    return round(base, 2)


# ═══════════════════════════════════════════════════════════════
# v1.8.3 §8.4 三链路口径一致性 —— 唯一聚合真源
# ═══════════════════════════════════════════════════════════════
RESURRECTION_THRESHOLD = 90   # 简化复活触发门槛（base_score >= 90）
RESURRECTION_FLOOR = 70       # 简化复活保底分
CLASSIFY_CORE = 70            # 分类门槛：🟢核心
CLASSIFY_POTENTIAL = 40       # 分类门槛：🟡潜力


def aggregate_score_v2(base_score: float, *,
                       days_since_published: int = 0,
                       cross_platform_score: int = 0,
                       semantic_score: int = 0,
                       trust_bonus: int = 0,
                       domain_bonus: int = 0,
                       with_cross_platform: bool = False,
                       with_semantic: bool = False) -> Dict:
    """唯一聚合真源（v1.8.3 · §8.4 三链路口径一致性）

    聚合顺序（口径单源，禁止任何消费方自行重写）：
        复活门控 → 时间衰减 → 跨平台(5%) → 语义(5%) → 信任加权 → 领域加权 → 分类

    两条链**必须**共用本函数：
      链A = `compute_final_score_v2`（core 纯函数，唯一完整评分口径）
      链B = `scripts/infoseek_core_v2.score_source`（MCP 第 10 工具 score_source 入口）
    历史分叉根因：链B 曾自算 `min(base + trust_bonus, 100)`，缺复活标志 / 缺时间衰减
    环节 / 分类阈值各自硬编码 → 同一 source 在两链可得不同分类（实测陈旧源 400 天：
    链A 38.7 ❌噪声 vs 链B 70.7 🟢核心，分类翻转级分叉）。

    口径事实（实测 40004 样本）：简化复活 `base>=90 → max(base,70)` 对数值**恒为
    no-op**（base>=90 必然 >=70），仅 `whitelist_triggered` 标志位有效。保留该环节是
    为返回 schema 兼容 + 未来门控扩展挂点，不产生评分实效。

    返回（中间量全暴露，供两链各自组装返回体 + 守护测试对拍）：
        after_whitelist / after_decay / final_score / classification /
        whitelist_triggered / top3_triggered(DEPRECATED 恒 False) / decay_factor
    """
    # 0) G4/G5（边界硬化 openfix）：入口有限性 + 类型守卫 ——
    #    NaN / None / ±inf / 非数字 → 归零并置 score_invalid 留痕；
    #    负值最终由下界夹取（max 0）收纳。禁止 NaN / 负分静默传播到下游分类。
    score_invalid = False
    if (not isinstance(base_score, (int, float))) or (base_score != base_score) \
            or base_score in (float("inf"), float("-inf")):
        score_invalid = True
        base_score = 0
    # 1) 复活门控（简化复活；数值 no-op，标志位有效 —— 见 docstring 口径事实）
    final = base_score
    whitelist_triggered = False
    if base_score >= RESURRECTION_THRESHOLD:
        whitelist_triggered = True
        final = max(final, RESURRECTION_FLOOR)

    # 2) 时间衰减
    decay = compute_decay_factor_v2(days_since_published)
    after_decay = round(final * decay, 1)

    # 3) 跨平台（v1.6.0 第 6 维，占 5%）
    if with_cross_platform:
        after_decay = round(after_decay * 0.95 + cross_platform_score * 0.05, 1)

    # 4) Jaccard 语义（v1.7.0 第 8 维，占 5%）
    if with_semantic:
        after_decay = round(after_decay * 0.95 + semantic_score * 0.05, 1)

    # 5) 信任加权（0-30，trust_sources 内已封顶）
    final_score = min(max(after_decay + trust_bonus, 0), 100)  # G5：上下界双夹取

    # 6) 领域加权（0-20，domain_router.domain_bonus_cap 可配）
    if domain_bonus:
        final_score = min(final_score + domain_bonus, 100)

    # 7) 分类（阈值单源常量）
    if final_score >= CLASSIFY_CORE:
        classification = '🟢核心'
    elif final_score >= CLASSIFY_POTENTIAL:
        classification = '🟡潜力'
    else:
        classification = '❌噪声'

    return {
        'after_whitelist': final,
        'after_decay': after_decay,
        'final_score': final_score,
        'classification': classification,
        'whitelist_triggered': whitelist_triggered,
        'top3_triggered': False,   # DEPRECATED（v1 双层复活已废弃，见 compute_final_score_v2 注释）
        'decay_factor': decay,
        'score_invalid': score_invalid,   # G4：入参非法（NaN/None/±inf/非数字）留痕
    }


def resolve_tier_v2(url: str, domain: str = 'general') -> int:
    """tier 单源口径（v1.8.3 · §8.4）：委托 trust_sources.get_tier_level → 1-4

    历史分叉：本模块曾用 `compute_trust_bonus_v2(url, platform, 'general') // 10`
    推算 tier —— domain 硬编码 general + 除以 10 的换算无业务依据，实测产出**域外
    非法值 0**（信任源命中 tech-research 时 tier=0，而真源 get_tier_level=1）。
    现统一委托 trust_sources 唯一 tier 真源。
    """
    try:
        from trust_sources import get_tier_level
        return get_tier_level(url or '', domain or 'general')
    except Exception:
        return 4


def compute_final_score_v2(source: dict, subject: str = '',
                            with_llm_readability: bool = True,
                            with_cross_platform: bool = False,
                            platforms: int = 1,
                            with_semantic: bool = False,
                            semantic_text: str = None,
                            days_since_published: int = 0,
                            with_domain: bool = False,
                            domain_profile: dict = None,
                            prefer_kb: bool = False) -> Dict:
    """v2.0.2 终极评分入口（纯函数版）；v1.8.3 起聚合环节委托 `aggregate_score_v2`

    与 v1 calculate_score() 行为一致，但：
    - 不修改 source dict
    - 返回 dict 不含 'version'（调用方负责）
    - 各评分维度独立计算
    - **聚合公式单源（§8.4 三链路口径一致性）**：复活 / 衰减 / 跨平台 / 语义 / 信任 /
      领域 / 分类七环节全部由 `aggregate_score_v2` 承担；本函数只做「维度取值」。
      链B（`infoseek_core_v2.score_source`）复用同一聚合真源，禁止另写公式。
    """
    # 1) 基础评分（四维 base —— 链A 唯一 base 口径）
    base_score = compute_base_score_v2(source, subject)

    # 2) 跨平台维度取值（v1.6.0 第 6 维）
    cross_platform_score = compute_cross_platform_v2(platforms) if with_cross_platform else 0

    # 3) Jaccard 语义维度取值（v1.7.0 第 8 维）
    semantic_score = 0
    if with_semantic:
        text = semantic_text or source.get('text', '') or source.get('snippet', '')
        semantic_score = compute_jaccard_v2(text, subject)

    # 4) Trust 加权取值（v2.0.0；0-30，封顶在 trust_sources 内）
    trust_bonus = compute_trust_bonus_v2(
        source.get('url', ''),
        source.get('platform', ''),
        source.get('domain', 'general'),
    )

    # 5) Domain 加权取值（v1.9.0；上限 domain_router.domain_bonus_cap()）
    domain_bonus = (compute_domain_bonus_v2(source, domain_profile, prefer_kb, subject)
                    if with_domain else 0)

    # 6) 聚合（唯一真源：复活 → 衰减 → 跨平台 → 语义 → 信任 → 领域 → 分类）
    agg = aggregate_score_v2(
        base_score,
        days_since_published=days_since_published,
        cross_platform_score=cross_platform_score,
        semantic_score=semantic_score,
        trust_bonus=trust_bonus,
        domain_bonus=domain_bonus,
        with_cross_platform=with_cross_platform,
        with_semantic=with_semantic,
    )

    return {
        'base_score': base_score,
        'after_whitelist': agg['after_whitelist'],
        'after_decay': agg['after_decay'],
        'after_whitelist_final': agg['final_score'],  # alias for after_whitelist
        'cross_platform_score': cross_platform_score,
        'semantic_similarity': semantic_score,
        'trust_bonus': trust_bonus,
        'domain_bonus': domain_bonus,
        'classification': agg['classification'],
        'whitelist_triggered': agg['whitelist_triggered'],
        'top3_triggered': agg['top3_triggered'],  # DEPRECATED 恒 False（v1 双层复活已废弃）
        # v1.8.3 §8.4：tier 委托 trust_sources.get_tier_level 唯一真源（1-4）。
        # 原口径 compute_trust_bonus_v2(url, platform, 'general') // 10 有两处缺陷：
        # domain 硬编码 general（丢失真实领域白名单）+ 除以 10 无业务依据 → 实测产出
        # 域外非法值 0（信任源命中 tech-research 时链A tier=0 / 链B tier=1）。
        'tier': resolve_tier_v2(source.get('url', ''), source.get('domain', 'general')),
        'version': '2.0.2',  # algo-v：下游契约稳定，不随 skill / mod 版本变动
    }


# ═══════════════════════════════════════════════════════════════
# CLI 测试
# ═══════════════════════════════════════════════════════════════

def main():
    """CLI: python -m core.anchor_score_v2 test"""
    if len(sys.argv) < 2:
        print("Usage: python -m core.anchor_score_v2 test")
        sys.exit(1)

    cmd = sys.argv[1]
    if cmd == 'test':
        source = {
            'url': 'https://baosteel.com/article',
            'platform': '宝钢集团',
            'interaction': 80,
            'topic_match': 90,
            'credibility': 95,
            'llm_readability': 85,
            'snippet': '钢卷分切工艺圆盘刀重叠量 20-30%。',
        }
        result = compute_final_score_v2(
            source, subject='钢卷分切工艺',
            with_llm_readability=True,
            with_semantic=True,
            semantic_text=source['snippet'],
            with_domain=True,
        )
        print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    import json
    main()
#!/usr/bin/env python3
"""
Mapulse — 信任增强组件 (Trust Enhancement Badge)

在分析性回答后附加4个固定标签:
  1. 【依据범围】 — 数据时间范围与来源
  2. 【신호강도】 — 信号强度(置信度)
  3. 【직접증거】 — 直接证据
  4. 【경계설명】 — 边界说明

规则驱动，非模型自由发挥。
"""

import datetime

# ─── Intent Categories ───

# 必须启用信任徽章的intent
TRUST_BADGE_INTENTS = {
    "community",        # 社区情绪
    "market_overview",  # 市场总览
    "outlook",          # 前景分析
    "why_drop",         # 下跌原因
    "why_rise",         # 上涨原因
    "sector_ranking",   # 板块轮动
    "hot_rank",         # 热点归纳
    "fear_greed",       # 恐贪指数
    "supply_demand",    # 资金流向
}


def should_attach_badge(intent):
    """判断是否需要附加信任徽章"""
    intent_str = str(intent).lower().replace("intent.", "")
    return intent_str in TRUST_BADGE_INTENTS


# ─── Signal Strength (规则判断) ───

def _calc_signal_strength(context):
    """
    基于实际收集到的数据源判断信号强度。
    
    高置信: ≥3种硬数据源
    中等置信: 1-2种硬数据源 + 模型归纳
    低置信: 几乎无硬数据, 主要靠推断
    
    Returns: ("high"|"medium"|"low", label_ko, label_zh)
    """
    hard_sources = 0
    
    # 结构化价格/指数数据
    if context.get("price"):
        hard_sources += 1
    if context.get("market_indices") or context.get("kospi") or context.get("kosdaq"):
        hard_sources += 1
    
    # 资金流/供需
    if context.get("supply_demand"):
        hard_sources += 1
    if context.get("foreign_flow"):
        hard_sources += 1
    
    # 新闻 (可验证)
    if context.get("news") and len(context["news"]) >= 2:
        hard_sources += 1
    if context.get("global_news") and len(context["global_news"]) >= 2:
        hard_sources += 1
    
    # 社区数据 (实际抓取)
    has_community_scrape = bool(
        context.get("community_sentiment") or 
        context.get("opentalk_sample") or
        context.get("jongtobang_sample")
    )
    if has_community_scrape:
        hard_sources += 1
    
    # 研报
    if context.get("research"):
        hard_sources += 1
    
    # VIX / Fear&Greed
    if context.get("vix") or context.get("fear_greed"):
        hard_sources += 1
    
    # 板块数据
    if context.get("sectors") or context.get("peers"):
        hard_sources += 1
    
    if hard_sources >= 3:
        return "high", "높은 신뢰도", "高置信"
    elif hard_sources >= 1:
        return "medium", "중간 신뢰도", "中等置信"
    else:
        return "low", "낮은 신뢰도", "低置信"


# ─── Scope (依据范围) ───

def _build_scope(context, intent_str):
    """构建【依据范围】— 基于实际收集的数据源"""
    parts = []
    today = datetime.datetime.now().strftime("%Y-%m-%d")
    
    # 时间范围
    if context.get("price"):
        parts.append("최근 5거래일 주가 데이터")
    
    if context.get("market_indices") or context.get("kospi") or context.get("kosdaq"):
        parts.append("KOSPI/KOSDAQ 지수")
    
    if context.get("supply_demand") or context.get("foreign_flow"):
        parts.append("외국인/기관/개인 수급 데이터")
    
    if context.get("news") or context.get("global_news"):
        parts.append("최근 주요 뉴스")
    
    if context.get("community_sentiment") or context.get("opentalk_sample"):
        parts.append("네이버 종토방/오픈톡 커뮤니티 샘플")
    
    if context.get("research"):
        parts.append("증권사 리서치 보고서")
    
    if context.get("vix"):
        parts.append("VIX 변동성 지수")
    
    if context.get("fear_greed"):
        parts.append("Fear & Greed 지수")
    
    if context.get("sectors") or context.get("peers"):
        parts.append("업종별 등락 데이터")
    
    if not parts:
        parts.append("공개 시장 데이터 및 뉴스")
    
    return f"기준일: {today} | " + "; ".join(parts)


# ─── Evidence (直接证据) ───

def _extract_evidence(context):
    """从结构化数据中提取2-4条可验证的直接证据"""
    evidence = []
    
    # Price data
    price = context.get("price")
    if price and isinstance(price, dict):
        close = price.get("close") or price.get("종가")
        change = price.get("change_pct") or price.get("등락률")
        name = price.get("name", "")
        if close and change is not None:
            direction = "상승" if float(change) > 0 else "하락"
            evidence.append(f"{name} 종가 ₩{close:,} ({direction} {abs(float(change)):.1f}%)")
    
    # Supply/demand
    sd = context.get("supply_demand")
    if sd and isinstance(sd, list):
        for item in sd[:2]:
            if isinstance(item, dict):
                investor = item.get("investor", item.get("투자자", ""))
                net = item.get("net", item.get("순매수", ""))
                if investor and net:
                    evidence.append(f"{investor} 순매수: {net}")
            elif isinstance(item, str):
                evidence.append(item)
    
    # Community sentiment
    cs = context.get("community_sentiment")
    if cs and isinstance(cs, dict):
        label = cs.get("label", "")
        bull = cs.get("bull", 0)
        bear = cs.get("bear", 0)
        if label:
            evidence.append(f"커뮤니티 감성: {label} (매수 {bull} / 매도 {bear})")
    
    # News headlines
    news = context.get("news", [])
    if news:
        headline = news[0] if isinstance(news[0], str) else news[0].get("title", "")
        if headline:
            evidence.append(f"주요 뉴스: {headline[:60]}")
    
    # VIX
    vix = context.get("vix")
    if vix and isinstance(vix, dict):
        evidence.append(f"VIX: {vix.get('value', 'N/A')}")
    
    # Fear & Greed
    fg = context.get("fear_greed")
    if fg and isinstance(fg, dict):
        evidence.append(f"Fear & Greed: {fg.get('value', 'N/A')}/100 ({fg.get('label', '')})")
    
    # Peers/sectors
    peers = context.get("peers", [])
    if peers and isinstance(peers, list):
        top = peers[0] if isinstance(peers[0], dict) else {}
        if top.get("name"):
            evidence.append(f"동종업종: {top['name']} {top.get('change', '')}")
    
    return evidence[:4]  # Max 4


# ─── Boundaries (边界说明) ───

def _build_boundaries(context, intent_str):
    """构建【边界说明】— 根据场景自动附加"""
    boundaries = []
    
    # 社区类: 必须说明是否真的做了全量抓取
    is_community = intent_str in ("community",)
    has_community_data = bool(
        context.get("community_sentiment") or 
        context.get("opentalk_sample") or 
        context.get("jongtobang_sample")
    )
    
    if is_community:
        if has_community_data:
            boundaries.append("커뮤니티 분석은 네이버 종토방/오픈톡 샘플 기반이며, 전체 원문을 전수 분석한 결과가 아닙니다")
        else:
            boundaries.append("커뮤니티 원문을 직접 수집하지 못했으며, 시장 데이터와 뉴스 기반의 분위기 추정입니다")
    
    # 市场分析: 说明短期性
    if intent_str in ("market_overview", "outlook", "sector_ranking", "hot_rank"):
        boundaries.append("단기 시장 판단이며, 중장기 추세를 보장하지 않습니다")
    
    # 下跌/上涨原因: 说明因果推断的局限性
    if intent_str in ("why_drop", "why_rise"):
        boundaries.append("가격 변동 원인은 복합적이며, 제시된 원인이 유일한 요인이 아닐 수 있습니다")
    
    # 通用: 数据范围说明
    if not context.get("news") and not context.get("global_news"):
        boundaries.append("실시간 뉴스를 수집하지 못한 상태에서의 분석입니다")
    
    # 通用免责
    boundaries.append("AI 분석 참고용이며 투자 조언이 아닙니다")
    
    return boundaries


# ─── Main: Generate Badge ───

def generate_trust_badge(context, intent, lang="ko"):
    """
    生成信任增强组件文本。
    
    Args:
        context: dict — 收集到的数据上下文 (price, news, supply_demand, etc.)
        intent: str — 查询意图
        lang: str — 输出语言 (ko/zh/en)
    
    Returns:
        str — 格式化的信任徽章文本, 可直接拼接到回答末尾
    """
    if not context:
        context = {}
    
    intent_str = str(intent).lower().replace("intent.", "")
    
    # 1. 信号强度
    strength_level, strength_ko, strength_zh = _calc_signal_strength(context)
    
    # 2. 依据范围
    scope = _build_scope(context, intent_str)
    
    # 3. 直接证据
    evidence = _extract_evidence(context)
    
    # 4. 边界说明
    boundaries = _build_boundaries(context, intent_str)
    
    # ─── Format ───
    
    if lang == "zh":
        lines = [
            "",
            "─── 分析依据 ───",
            "",
            f"📋 *【依据范围】*",
            f"  {scope}",
            "",
            f"📊 *【信号强度】*",
            f"  {strength_zh}" + _strength_bar(strength_level),
            "",
            f"🔍 *【直接证据】*",
        ]
        if evidence:
            for e in evidence:
                lines.append(f"  • {e}")
        else:
            lines.append("  • 当前缺少可直接引用的结构化数据")
        
        lines.append("")
        lines.append(f"⚠️ *【边界说明】*")
        for b in boundaries:
            lines.append(f"  • {b}")
    
    elif lang == "en":
        lines = [
            "",
            "─── Analysis Basis ───",
            "",
            f"📋 *[Scope]*",
            f"  {scope}",
            "",
            f"📊 *[Signal Strength]*",
            f"  {strength_level.capitalize()}" + _strength_bar(strength_level),
            "",
            f"🔍 *[Direct Evidence]*",
        ]
        if evidence:
            for e in evidence:
                lines.append(f"  • {e}")
        else:
            lines.append("  • Insufficient structured data for this query")
        
        lines.append("")
        lines.append(f"⚠️ *[Scope Limitations]*")
        for b in boundaries:
            lines.append(f"  • {b}")
    
    else:  # Korean (default)
        lines = [
            "",
            "─── 분석 근거 ───",
            "",
            f"📋 *【의거범위】*",
            f"  {scope}",
            "",
            f"📊 *【신호강도】*",
            f"  {strength_ko}" + _strength_bar(strength_level),
            "",
            f"🔍 *【직접증거】*",
        ]
        if evidence:
            for e in evidence:
                lines.append(f"  • {e}")
        else:
            lines.append("  • 현재 직접 인용 가능한 구조화 데이터 부족")
        
        lines.append("")
        lines.append(f"⚠️ *【경계설명】*")
        for b in boundaries:
            lines.append(f"  • {b}")
    
    return "\n".join(lines)


def _strength_bar(level):
    """可视化信号强度条"""
    if level == "high":
        return "  🟢🟢🟢"
    elif level == "medium":
        return "  🟡🟡⚪"
    else:
        return "  🔴⚪⚪"


# ─── Test ───

if __name__ == "__main__":
    # Simulate context with some data
    test_context = {
        "price": {"name": "삼성전자", "close": 82900, "change_pct": 2.7},
        "supply_demand": [
            {"investor": "외국인", "net": "+1,234억"},
            {"investor": "개인", "net": "-987억"},
        ],
        "news": ["삼성전자, HBM3E 양산 본격화", "반도체 업황 회복 신호"],
        "community_sentiment": {"label": "중립", "bull": 45, "bear": 38, "ratio": 0.54},
        "vix": {"value": 18.5},
    }
    
    print("=== Korean ===")
    print(generate_trust_badge(test_context, "community", "ko"))
    print("\n=== Chinese ===")
    print(generate_trust_badge(test_context, "community", "zh"))
    print("\n=== Empty context (low confidence) ===")
    print(generate_trust_badge({}, "community", "ko"))

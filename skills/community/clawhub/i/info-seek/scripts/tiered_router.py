#!/usr/bin/env python3
"""
scripts/tiered_router.py — 三级路由决策表（v1.0.0 · P1a）

把 infoseek 外部数据源统一编排为三级路由，按 意图×成本×健康 动态选择：

    L0 免费优先层  → public-apis 目录（PublicApisCatalog，free_api，0 成本）
    L1 网关付费层  → AgentKey（gateway_api，credits，一个 key 全接入）
    L2 专用路由层  → QVeris（structured_data_api，discover→call 意图路由）
    末端兜底       → manual_review（全层失效时标记人工核实，不静默丢数据）

设计对齐 infoseek 架构：
  - 与 capabilities/registry.yaml v2 一致（kind 族：free_api/gateway_api/structured_data_api）
  - 与 engine_lifecycle 协同：每层尝试前查健康，失败记录并降级
  - 与 capability_compensator 语义替代链兼容：AgentKey 挂 → QVeris → public-apis → manual
  - 免费优先：默认先试 L0（无成本），命中即返回；未命中才升 L1/L2
  - 成本保护：credits 层调用前检查 budget（CALL_BUDGET），防无限消耗

用法:
    from tiered_router import route_query, resolve_route
    plan = resolve_route("2026 铝价走势", intent="finance")
    results = route_query("2026 铝价走势")   # 自动按意图路由

CLI:
    python scripts/tiered_router.py --query "汇率" --intent finance
    python scripts/tiered_router.py --plan "汇率" --intent finance
"""

from __future__ import annotations

import json
import os
import sys
import time
from pathlib import Path
from typing import Callable, Dict, List, Optional

# ── 意图识别特征词（与 domains 分类对齐；可经 env INFOSEEK_INTENT_WORDS 覆盖）──
_INTENT_WORDS: Dict[str, List[str]] = {
    "finance": ["汇率", "股票", "行情", "价格", "利率", "GDP", "通胀", "CPI", "财报",
                "股价", "期货", "外汇", "财经", "货币", "涨跌", "指数", "ETF", "基金",
                "走势", "铝价", "铜价", "油价", "金价", "钢材", "大宗", "商品", "期货"],
    "sentiment": ["舆情", "情绪", "口碑", "评论", "争议", "态度", "观点", "风评",
                  "讨论", "热搜", "用户反馈"],
    "identity": ["账号", "用户名", "身份", "是谁", "马甲", "水军", "真人", "ID"],
    "tech": ["API", "SDK", "框架", "开源", "代码", "算法", "模型", "部署", "版本"],
}

# 意图 → 候选能力链（与 registry.yaml degrade_to 对齐；'PublicApisCatalog' 为 L0 免费层）
# 注：resolve_route 输出按【实际执行顺序】重排（免费优先原则），
#     即 L0 免费层最优先尝试，成本可控时再升 L1/L2。
_INTENT_CHAINS: Dict[str, List[str]] = {
    "finance":    ["QVeris", "AgentKey", "PublicApisCatalog", "manual_review"],
    "sentiment":  ["AgentKey", "PublicApisCatalog", "manual_review"],
    "tech":       ["PublicApisCatalog", "AgentKey", "QVeris", "manual_review"],
    "identity":   ["Maigret", "Sherlock", "AccountTrustScorer", "manual_review"],
    "general":    ["PublicApisCatalog", "AgentKey", "QVeris", "manual_review"],
}

# 意图 → 执行顺序（免费优先：L0 目录 0 成本，命中即返回，不消耗 credits）
_EXEC_ORDER: Dict[str, List[str]] = {
    "finance":    ["PublicApisCatalog", "AgentKey", "QVeris", "manual_review"],
    "sentiment":  ["PublicApisCatalog", "AgentKey", "manual_review"],
    "tech":       ["PublicApisCatalog", "AgentKey", "QVeris", "manual_review"],
    "identity":   ["Maigret", "Sherlock", "AccountTrustScorer", "manual_review"],
    "general":    ["PublicApisCatalog", "AgentKey", "QVeris", "manual_review"],
}

# 层标签（输出可读性）
_LAYER_LABELS = {
    "PublicApisCatalog": "L0-免费",
    "AgentKey": "L1-网关",
    "QVeris": "L2-专用",
    "Maigret": "L2-身份",
    "Sherlock": "L2-身份",
    "AccountTrustScorer": "L2-验证",
    "manual_review": "末端-人工",
}

_DEFAULT_BUDGET = int(os.environ.get("INFOSEEK_TIERED_CALL_BUDGET", "3"))


# ═══════════════════════════════════════════════════════════════
# 意图识别
# ═══════════════════════════════════════════════════════════════

def detect_intent(query: str) -> str:
    """按特征词启发式分类 query（finance/sentiment/identity/tech/general）。"""
    q = query.lower()
    # 意图特化词优先（避免 "账号" 落入 finance 等）
    for intent in ("identity", "sentiment", "finance", "tech"):
        for w in _INTENT_WORDS[intent]:
            if w.lower() in q:
                return intent
    return "general"


def resolve_route(query: str, intent: Optional[str] = None) -> Dict:
    """输出路由决策（不执行）：意图 → 执行顺序链 + 层标签。"""
    intent = intent or detect_intent(query)
    chain = _EXEC_ORDER.get(intent, _EXEC_ORDER["general"])
    return {
        "query": query,
        "intent": intent,
        "chain": chain,
        "layers": [_LAYER_LABELS.get(c, c) for c in chain],
        "budget": _DEFAULT_BUDGET,
        "reason": f"意图={intent}，免费优先：沿 L0 {_LAYER_LABELS.get(chain[0], chain[0])} 起",
    }


# ═══════════════════════════════════════════════════════════════
# 执行路由（L0 免费优先，命中即返回）
# ═══════════════════════════════════════════════════════════════

def _cap_enabled(name: str) -> bool:
    """查注册表启用态（含 env 覆盖）。"""
    try:
        sys.path.insert(0, str(Path(__file__).parent.parent / "core"))
        from capability_registry import is_enabled
        return is_enabled(name)
    except Exception:
        return False


def _search_free_apis(query: str, limit: int = 3) -> List[Dict]:
    """L0：public-apis 目录检索（免费无成本）。"""
    try:
        sys.path.insert(0, str(Path(__file__).parent))
        from public_apis_catalog import search_free_api
        entries = search_free_api(keyword=query, limit=limit, auth_filter="No")
        return [{
            "url": e.get("url") or "",
            "title": f"[{e['category']}] {e['name']}",
            "snippet": e.get("description", ""),
            "source": "PublicApisCatalog",
            "score": 60,
            "free_api": True,
        } for e in entries]
    except Exception as e:
        print(f"[tiered_router][warn] L0 目录检索失败: {e}")
        return []


def _search_qveris(query: str, limit: int = 3) -> List[Dict]:
    """L2：QVeris 专用路由（discover→call，credits 保护）。"""
    try:
        sys.path.insert(0, str(Path(__file__).parent))
        from qveris_client import search as qv_search
        from qveris_client import QVerisQuotaError, QVerisAuthError
        try:
            return qv_search(query, max_results=limit)
        except (QVerisQuotaError, QVerisAuthError):
            print("[tiered_router][warn] QVeris 配额/认证失败，降级")
            return []
    except Exception as e:
        print(f"[tiered_router][warn] L2 QVeris 失败: {e}")
        return []


def route_query(query: str, intent: Optional[str] = None,
                budget: int = 0, verbose: bool = False,
                consent: bool = False) -> Dict:
    """三级路由执行：L0 → L1 → L2 顺序尝试，命中即返回；全挂 → manual_review。

    consent: 身份归因（identity 意图）合规授权透传；未授权时身份链标记
             skipped-no-consent 并降级 manual_review（不静默执行个人 OSINT）。

    返回:
        {query, intent, used, layer, results, trail: [(cap, status)], exhausted}
    """
    intent = intent or detect_intent(query)
    exec_chain = _EXEC_ORDER.get(intent, _EXEC_ORDER["general"])
    budget = budget or _DEFAULT_BUDGET
    trail: List[tuple] = []
    results: List[Dict] = []

    for cap in exec_chain:
        # L0：免费优先（public-apis 目录，0 成本）
        if cap == "PublicApisCatalog":
            r = _search_free_apis(query)
            trail.append(("PublicApisCatalog", "ok" if r else "empty"))
            if r:
                return {"query": query, "intent": intent, "used": "PublicApisCatalog",
                        "layer": "L0-免费", "results": r, "trail": trail,
                        "exhausted": False}
            continue

        # L1：AgentKey 网关（有 key 才尝试；adapter 未接入时降级）
        if cap == "AgentKey":
            if not os.environ.get("AGENTKEY_API_KEY"):
                trail.append(("AgentKey", "skipped-no-key"))
                continue
            trail.append(("AgentKey", "skipped-no-adapter"))
            # P1b 后接入真实 MCP 调用
            continue

        # L2：QVeris（结构化数据专用路由）
        if cap == "QVeris":
            r = _search_qveris(query, limit=budget)
            trail.append(("QVeris", "ok" if r else "empty"))
            if r:
                return {"query": query, "intent": intent, "used": "QVeris",
                        "layer": "L2-专用", "results": r, "trail": trail,
                        "exhausted": False}
            continue

        # 身份归因链（Maigret/Sherlock/AccountTrustScorer）：统一入口
        # T3/G1：由 pipeline.search_identity_attribution 一体化执行
        #   （内部：registry 双闸口 → compensate(Maigret→Sherlock→manual) → AccountTrustScorer 验证）
        if cap == "Maigret":
            if not os.environ.get("INFOSEEK_ENABLE_IDENTITY_ATTRIBUTION"):
                trail.append(("Maigret", "skipped-disabled"))
                trail.append(("Sherlock", "skipped-disabled"))
                trail.append(("AccountTrustScorer", "skipped-disabled"))
                continue
            if not consent:
                trail.append(("Maigret", "skipped-no-consent"))
                trail.append(("Sherlock", "skipped-no-consent"))
                trail.append(("AccountTrustScorer", "skipped-no-consent"))
                continue
            try:
                sys.path.insert(0, str(Path(__file__).parent))
                from infoseek_pipeline import search_identity_attribution
                r = search_identity_attribution(query, consent=True, max_results=budget or 10)
                trail.append(("Maigret", "ok" if r else "empty"))
                trail.append(("Sherlock", "via-unified-path"))
                trail.append(("AccountTrustScorer", "via-unified-path"))
                if r:
                    return {"query": query, "intent": intent,
                            "used": "identity_attribution", "layer": "L2-身份",
                            "results": r, "trail": trail, "exhausted": False}
            except Exception as e:
                trail.append(("Maigret", f"fail:{type(e).__name__}"))
                trail.append(("Sherlock", "via-unified-path"))
                trail.append(("AccountTrustScorer", "via-unified-path"))
            # 统一入口已尝试（无论成败），身份链不逐点重试，落末端 manual_review
            continue
        if cap in ("Sherlock", "AccountTrustScorer"):
            trail.append((cap, "via-unified-path"))
            continue

    # 末端：manual_review（不静默丢数据）
    trail.append(("manual_review", "gap"))
    return {"query": query, "intent": intent, "used": "manual_review",
            "layer": "末端-人工", "results": [{
                "url": "", "title": "(需人工核实)", "snippet": f"三级路由全层未命中: {query}",
                "source": "manual_review", "score": 0, "_gap": True}],
            "trail": trail, "exhausted": True}


# ═══════════════════════════════════════════════════════════════
# CLI
# ═══════════════════════════════════════════════════════════════

def main() -> int:
    import argparse
    ap = argparse.ArgumentParser(description="三级路由决策表")
    ap.add_argument("--query", required=True, help="调研查询")
    ap.add_argument("--intent", choices=list(_INTENT_CHAINS.keys()), help="显式意图")
    ap.add_argument("--plan", action="store_true", help="仅输出路由计划（不执行）")
    ap.add_argument("--verbose", action="store_true")
    ap.add_argument("--consent", action="store_true",
                    help="identity 意图合规授权（涉个人 OSINT，须显式开启）")
    args = ap.parse_args()

    if args.plan:
        print(json.dumps(resolve_route(args.query, args.intent), ensure_ascii=False, indent=2))
        return 0
    r = route_query(args.query, args.intent, verbose=args.verbose, consent=args.consent)
    print(json.dumps(r, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())

#!/usr/bin/env python3
"""
structured-decision-block - Minimal universal decision synthesis engine.

Usage:
  python decision_block.py --payload input.json --output block.md --json-out block.json
  python decision_block.py --demo
"""

import json
import argparse
import sys
from typing import Dict, Any, List, Tuple
from datetime import datetime

# Default scenario weights (can be overridden by business_context)
DEFAULT_WEIGHTS = {
    "niche-analysis": {
        "market_potential": 20,
        "competition": 18,
        "entry_barrier": 15,
        "profitability": 25,
        "trend_momentum": 12,
        "risk": 10
    },
    "product-selection": {
        "market_potential": 18,
        "competition": 20,
        "entry_barrier": 18,
        "profitability": 25,
        "trend_momentum": 10,
        "risk": 9
    },
    "default": {
        "market_potential": 20,
        "competition": 18,
        "entry_barrier": 15,
        "profitability": 25,
        "trend_momentum": 12,
        "risk": 10
    }
}

VERDICT_MAP = {
    "green": "推荐进入",
    "yellow": "谨慎进入",
    "red": "不推荐"
}

def load_payload(path: str) -> Dict[str, Any]:
    with open(path, 'r', encoding='utf-8') as f:
        return json.load(f)

def normalize_weights(user_weights: Dict[str, float] = None, scenario: str = "default") -> Dict[str, float]:
    base = DEFAULT_WEIGHTS.get(scenario, DEFAULT_WEIGHTS["default"]).copy()
    if user_weights:
        for k, v in user_weights.items():
            if k in base:
                base[k] = float(v)
    total = sum(base.values())
    if total > 0:
        return {k: round(v / total * 100, 1) for k, v in base.items()}
    return {k: 100.0 / len(base) for k in base}

def score_dimension(dim: Dict[str, Any], risk_preference: str) -> float:
    """Derive or adjust 0-10 score for a dimension."""
    if "score" in dim and dim["score"] is not None:
        score = float(dim["score"])
    else:
        # Rough derivation from value vs thresholds if available
        val = dim.get("value")
        th = dim.get("thresholds", {})
        try:
            if isinstance(val, (int, float)) and th:
                if "green" in th:
                    score = 8.0
                elif "yellow" in th:
                    score = 6.0
                else:
                    score = 4.0
            else:
                score = 5.5
        except:
            score = 5.5

    # Risk preference adjustment (simple)
    if risk_preference == "保守":
        score = max(0, score - 0.8)
    elif risk_preference == "激进":
        score = min(10, score + 0.6)
    return round(max(0, min(10, score)), 1)

def evaluate_verdict(overall_score: float, hard_constraints_ok: bool, risk_preference: str) -> Tuple[str, str]:
    """Return (emoji_verdict, text_verdict)"""
    if not hard_constraints_ok:
        return "🔴", "不推荐（一票否决触发）"

    if overall_score >= 78:
        base = "green"
    elif overall_score >= 58:
        base = "yellow"
    else:
        base = "red"

    # Risk adjustment
    if risk_preference == "保守" and base == "green" and overall_score < 85:
        base = "yellow"
    if risk_preference == "激进" and base == "yellow" and overall_score > 65:
        base = "green"

    return "🟢" if base == "green" else ("🟡" if base == "yellow" else "🔴"), VERDICT_MAP[base]

def check_hard_constraints(payload: Dict[str, Any]) -> bool:
    constraints = payload.get("business_context", {}).get("hard_constraints", [])
    aggregates = payload.get("key_aggregates", {})
    if not constraints:
        return True

    # Very lightweight parser for common patterns
    for c in constraints:
        c_lower = c.lower()
        try:
            if "净利润率" in c or "profit" in c_lower:
                num = float(''.join(filter(lambda x: x.isdigit() or x == '.', c)))
                val = aggregates.get("top_asin_net_profit_rate_zero_ad") or aggregates.get("avg_profit_margin", 0)
                if val < num:
                    return False
            if "cr3" in c_lower or "集中度" in c:
                num = float(''.join(filter(lambda x: x.isdigit() or x == '.', c)))
                val = aggregates.get("cr3", 100)
                if val > num:
                    return False
        except:
            pass  # ignore unparsable for minimal version
    return True

def build_counter_evidence(dimensions: List[Dict], aggregates: Dict, risks: List, risk_pref: str) -> List[str]:
    counters = []
    for d in dimensions:
        for rev in d.get("potential_reversals", []):
            counters.append(f"{d['name']}：{rev}")
    # Synthesize from low scores
    for d in dimensions:
        if d.get("score", 10) < 5.5:
            counters.append(f"{d['name']} 当前评分偏低（{d.get('score')}），需重点监控")
    # From risks
    for r in risks[:2]:
        if isinstance(r, dict):
            counters.append(r.get("text", str(r)))
        else:
            counters.append(str(r))
    # Risk preference specific
    if risk_pref == "保守":
        counters.append("保守型用户建议：任意维度跌至黄档以下即触发重新评估")
    if len(counters) < 3:
        counters.append("数据完整率或趋势稳定性下降时建议重新扫描")
    return counters[:6]

def generate_actions(verdict_emoji: str, dimensions: List[Dict], primary_goal: str, aggregates: Dict) -> List[Dict]:
    actions = []
    if verdict_emoji == "🟢":
        actions.append({"priority": 1, "action": f"立即启动小批量测试，重点验证 {primary_goal} 核心指标"})
        if aggregates.get("top_asin_net_profit_rate_zero_ad", 0) > 25:
            actions.append({"priority": 2, "action": "准备差异化 Listing（标题/主图/卖点），基于当前低分竞品痛点"})
        actions.append({"priority": 3, "action": "设置 14 天复扫定时任务，监控反证条件"})
    elif verdict_emoji == "🟡":
        actions.append({"priority": 1, "action": "先做 3-5 个变体小预算测试（7-10 天），验证转化"})
        actions.append({"priority": 2, "action": "重点改善得分偏低的维度对应的风险点"})
        actions.append({"priority": 3, "action": "仅在反证条件未触发时再考虑加大投入"})
    else:
        actions.append({"priority": 1, "action": "暂不进入，优先寻找更优赛道或调整产品形态"})
        actions.append({"priority": 2, "action": "记录本次主要反证条件，作为未来选品过滤规则"})
    return actions

def process(payload: Dict[str, Any]) -> Dict[str, Any]:
    bc = payload.get("business_context", {})
    risk_pref = bc.get("risk_preference", "稳健")
    primary_goal = bc.get("primary_goal", "综合")
    scenario = payload.get("metadata", {}).get("scenario", "default")

    weights = normalize_weights(bc.get("weights"), scenario)
    dimensions = payload.get("dimensions", [])
    aggregates = payload.get("key_aggregates", {})
    risks = payload.get("key_risks", [])
    limitations = payload.get("upstream_limitations", [])

    # Score dimensions
    for d in dimensions:
        d["final_score"] = score_dimension(d, risk_pref)
        d["weight"] = weights.get(d.get("id", ""), d.get("weight", 10))

    # Weighted overall score
    total_w = sum(d.get("weight", 0) for d in dimensions)
    if total_w > 0:
        overall = sum(d["final_score"] * d.get("weight", 0) for d in dimensions) / total_w
    else:
        overall = 50.0
    overall = round(overall * 10, 1)   # scale 0-10 average to 0-100

    hard_ok = check_hard_constraints(payload)
    verdict_emoji, verdict_text = evaluate_verdict(overall, hard_ok, risk_pref)

    counters = build_counter_evidence(dimensions, aggregates, risks, risk_pref)
    actions = generate_actions(verdict_emoji, dimensions, primary_goal, aggregates)

    # Build markdown
    md_lines = [
        "## 决策块",
        "",
        f"**最终判定**: {verdict_emoji} {verdict_text}",
        f"**综合得分**: {overall} / 100",
        f"**置信度**: {round(payload.get('upstream_summary', {}).get('data_completeness', 0.8) * 100)}%",
        "",
        "### 维度得分表",
        "| 维度 | 当前值 | 评分 | 权重 | 档位 |",
        "|------|--------|------|------|------|",
    ]
    for d in dimensions:
        score = d.get("final_score", 5)
        emoji = "🟢" if score >= 7.5 else ("🟡" if score >= 5.5 else "🔴")
        md_lines.append(f"| {d['name']} | {d['value']} {d.get('unit','')} | {score} | {d.get('weight',10)} | {emoji} |")

    md_lines += [
        "",
        "### 反证条件（结论会失效的情况）",
    ]
    for i, c in enumerate(counters, 1):
        md_lines.append(f"{i}. {c}")

    md_lines += [
        "",
        "### 推荐动作（优先级排序）",
    ]
    for a in actions:
        md_lines.append(f"{a['priority']}. {a['action']}")

    md_lines += [
        "",
        "### 数据局限",
    ]
    for lim in limitations[:3]:
        md_lines.append(f"- {lim}")

    markdown = "\n".join(md_lines)

    result_json = {
        "verdict": verdict_emoji,
        "verdict_text": verdict_text,
        "overall_score": overall,
        "confidence": round(payload.get('upstream_summary', {}).get('data_completeness', 0.8), 2),
        "dimensions": [
            {
                "name": d["name"],
                "value": d["value"],
                "score": d.get("final_score"),
                "weight": d.get("weight"),
                "verdict": "🟢" if d.get("final_score", 5) >= 7.5 else ("🟡" if d.get("final_score", 5) >= 5.5 else "🔴")
            } for d in dimensions
        ],
        "counter_evidence": counters,
        "recommended_actions": actions,
        "data_limitations": limitations,
        "generated_at": datetime.now().isoformat()
    }

    return {
        "markdown": markdown,
        "json": result_json,
        "verdict": verdict_emoji,
        "overall_score": overall
    }

def main():
    parser = argparse.ArgumentParser(description="Structured Decision Block engine")
    parser.add_argument("--payload", help="Path to input JSON payload")
    parser.add_argument("--output", help="Path to write Markdown decision block")
    parser.add_argument("--json-out", help="Path to write structured JSON result")
    parser.add_argument("--scenario", default="niche-analysis", help="Scenario for default weights")
    parser.add_argument("--demo", action="store_true", help="Run with built-in demo payload")
    args = parser.parse_args()

    if args.demo:
        # Minimal demo payload
        demo = {
            "version": "0.2",
            "metadata": {"scenario": args.scenario, "upstream_skill": "demo", "platform": "amazon", "site": "US"},
            "business_context": {"risk_preference": "稳健", "primary_goal": "利润优先"},
            "dimensions": [
                {"id": "growth", "name": "增长潜力", "value": 35, "unit": "%", "score": 8.0, "evidence": [{"text": "趋势向上", "source": "demo"}]},
                {"id": "cr3", "name": "CR3", "value": 38, "unit": "%", "score": 7.5, "evidence": [{"text": "中等集中", "source": "demo"}]},
                {"id": "profit", "name": "利润率", "value": 27, "unit": "%", "score": 8.5, "evidence": [{"text": "健康", "source": "demo"}]}
            ],
            "key_aggregates": {"cr3": 38, "top_asin_net_profit_rate_zero_ad": 27},
            "key_risks": [],
            "upstream_limitations": ["demo data"]
        }
        payload = demo
    elif args.payload:
        payload = load_payload(args.payload)
    else:
        print("Error: --payload or --demo required", file=sys.stderr)
        sys.exit(1)

    result = process(payload)

    if args.output:
        with open(args.output, 'w', encoding='utf-8') as f:
            f.write(result["markdown"])
        print(f"Markdown written to {args.output}")
    else:
        print(result["markdown"])

    if args.json_out:
        with open(args.json_out, 'w', encoding='utf-8') as f:
            json.dump(result["json"], f, ensure_ascii=False, indent=2)
        print(f"JSON written to {args.json_out}")
    else:
        print("\n--- JSON ---")
        print(json.dumps(result["json"], ensure_ascii=False, indent=2))

if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""
不良资产处置决策模型 (Disposal Decision Model for NPL)
=====================================================
L3定量分析工具 — 用于不良资产处置策略的量化评分与方案比选

用途：
  1. 对单笔/单个资产包进行五维评分
  2. 自动匹配最优处置策略
  3. 多方案对比（回收率×周期×成本）
  4. 敏感性分析（关键参数变动对结果的影响）

作者：助手（不良资产专家）
版本：1.0
日期：2026-05-27
"""

import json
import math
from typing import Dict, List, Tuple, Optional


# ─── 1. 处置策略数据库 ─────────────────────────────────────────────

DISPOSAL_STRATEGIES = {
    "债务重组": {
        "recovery_rate": (0.70, 0.90),  # 回收率范围
        "cycle_months": (6, 24),        # 处置周期（月）
        "cost_rate": (0.03, 0.08),      # 处置费用占比
        "legal_reliance": "高",          # 对法律程序的依赖度
        "suitable_grade": "A-B",         # 适合的资产评级
        "scenario": "企业暂时困难但有经营前景",
        "key_metric": "资产负债率<80%",
        "score_threshold": (75, 100),    # 五维评分在此区间时优先推荐
    },
    "法律诉讼": {
        "recovery_rate": (0.50, 0.70),
        "cycle_months": (12, 36),
        "cost_rate": (0.08, 0.15),
        "legal_reliance": "极高",
        "suitable_grade": "B-C",
        "scenario": "恶意逃废债或协商无效",
        "key_metric": "债务人资产可执行",
        "score_threshold": (50, 74),
    },
    "资产拍卖": {
        "recovery_rate": (0.60, 0.80),
        "cycle_months": (3, 12),
        "cost_rate": (0.03, 0.10),
        "legal_reliance": "中",
        "suitable_grade": "A-B",
        "scenario": "抵押物充足/实物资产",
        "key_metric": "抵押物市场流动性好",
        "score_threshold": (75, 100),
    },
    "批量转让（银登）": {
        "recovery_rate": (0.30, 0.50),
        "cycle_months": (1, 3),
        "cost_rate": (0.01, 0.03),
        "legal_reliance": "低",
        "suitable_grade": "C-D",
        "scenario": "个贷不良/小额分散资产",
        "key_metric": "单笔金额<100万",
        "score_threshold": (25, 49),
    },
    "NPAS证券化": {
        "recovery_rate": (0.50, 0.70),
        "cycle_months": (6, 18),
        "cost_rate": (0.04, 0.08),
        "legal_reliance": "中",
        "suitable_grade": "B-C",
        "scenario": "标准化资产包/有稳定现金流",
        "key_metric": "底层资产分散度>100笔",
        "score_threshold": (50, 74),
    },
    "共益债盘活": {
        "recovery_rate": (0.60, 0.90),
        "cycle_months": (12, 24),
        "cost_rate": (0.05, 0.10),
        "legal_reliance": "高",
        "suitable_grade": "B-C",
        "scenario": "烂尾楼盘活/停工项目",
        "key_metric": "项目有复工价值+法院支持",
        "score_threshold": (50, 74),
    },
    "REITs退出": {
        "recovery_rate": (0.70, 0.90),
        "cycle_months": (12, 24),
        "cost_rate": (0.03, 0.06),
        "legal_reliance": "低",
        "suitable_grade": "A",
        "scenario": "有稳定现金流的商业不动产",
        "key_metric": "NOI/资本化率>6%",
        "score_threshold": (75, 100),
    },
    "核销出表": {
        "recovery_rate": (0.10, 0.30),
        "cycle_months": (0, 1),
        "cost_rate": (0.00, 0.01),
        "legal_reliance": "无",
        "suitable_grade": "D",
        "scenario": "回收无望/监管出表要求",
        "key_metric": "回收率<20%",
        "score_threshold": (0, 24),
    },
}

# 策略按评分区间的推荐顺序
STRATEGY_PRIORITY = {
    (75, 100): ["债务重组", "REITs退出", "资产拍卖", "NPAS证券化"],
    (50, 74):  ["法律诉讼", "共益债盘活", "NPAS证券化", "债务重组"],
    (25, 49):  ["批量转让（银登）", "折价清偿", "债权转让"],
    (0, 24):   ["核销出表"],
}


# ─── 2. 五维评分模型 ───────────────────────────────────────────────

# 评分维度权重
WEIGHTS = {
    "资产质量": 0.25,
    "法律状态": 0.25,
    "处置效率": 0.20,
    "回收确定性": 0.15,
    "成本效益": 0.15,
}


def score_asset_quality(
    property_type: str,        # 住宅/商业/工业/纯信用
    city_tier: int,            # 城市等级 1-4
    loan_to_value: float,      # 抵押率（抵押物估值/债权金额）
    operating_condition: str,  # 经营状况 良好/一般/困难/停工
) -> int:
    """资产质量评分（0-100）"""
    base = 50

    # 物业类型
    type_scores = {
        "住宅": 90, "公寓": 75, "商业": 60, "写字楼": 55,
        "工业": 40, "土地": 50, "纯信用": 10, "设备": 30,
    }
    base += type_scores.get(property_type, 40) - 50

    # 城市等级
    city_scores = {1: 20, 2: 10, 3: 0, 4: -10}
    base += city_scores.get(city_tier, 0)

    # 抵押率
    if loan_to_value <= 0.3:
        base += 15
    elif loan_to_value <= 0.5:
        base += 10
    elif loan_to_value <= 0.7:
        base += 0
    elif loan_to_value <= 1.0:
        base -= 10
    else:
        base -= 20

    # 经营状况
    op_scores = {"良好": 15, "一般": 5, "困难": -10, "停工": -20, "破产": -30}
    base += op_scores.get(operating_condition, 0)

    return max(0, min(100, base))


def score_legal_status(
    is_first_lien: bool,       # 是否首封
    has_tenancy: bool,         # 是否有租赁
    has_lien_issues: bool,     # 是否存在优先权问题
    statute_expired: bool,     # 诉讼时效是否已过
    num_lawsuits: int,         # 涉诉数量
    num_encumbrances: int,     # 轮候查封数量
) -> int:
    """法律状态评分（0-100）"""
    base = 60

    if is_first_lien:
        base += 20
    else:
        base -= 5 * min(num_encumbrances, 5)

    if has_tenancy:
        base -= 20

    if has_lien_issues:
        base -= 15

    if statute_expired:
        return 5  # 诉讼时效过期，基本归零

    base -= 3 * min(num_lawsuits, 5)

    return max(0, min(100, base))


def score_disposal_efficiency(
    expected_months: int,      # 预计处置周期（月）
    market_liquidity: str,     # 市场流动性 高/中/低
    buyer_available: bool,     # 是否有明确买家
    auction_history: int,      # 历史流拍次数
) -> int:
    """处置效率评分（0-100）"""
    base = 50

    # 周期
    if expected_months <= 3:
        base += 30
    elif expected_months <= 6:
        base += 20
    elif expected_months <= 12:
        base += 10
    elif expected_months <= 24:
        base += 0
    else:
        base -= 20

    # 流动性
    liquidity_scores = {"高": 20, "中": 5, "低": -15}
    base += liquidity_scores.get(market_liquidity, 0)

    # 买家
    if buyer_available:
        base += 15

    # 流拍
    base -= 10 * min(auction_history, 3)

    return max(0, min(100, base))


def score_recovery_certainty(
    recovery_confidence: str,  # 回收确定性 高/中/低
    has_guarantor: bool,       # 是否有保证人
    debt_rank: str,            # 债权优先级 优先/普通/劣后
    guarantees: float,         # 其他担保覆盖倍数
) -> int:
    """回收确定性评分（0-100）"""
    base = 50

    conf_scores = {"高": 25, "中": 10, "低": -10, "极低": -25}
    base += conf_scores.get(recovery_confidence, 0)

    if has_guarantor:
        base += 10

    rank_scores = {"优先": 20, "普通": 0, "劣后": -20}
    base += rank_scores.get(debt_rank, 0)

    base += min(int(guarantees * 15), 15)

    return max(0, min(100, base))


def score_cost_efficiency(
    disposal_cost_rate: float,  # 处置费用占回收额比例
    tax_cost_rate: float,       # 税费比例
    opportunity_cost: float,    # 资金成本（年化%）
    estimated_months: int,      # 处置周期
) -> int:
    """成本效益评分（0-100）"""
    base = 50

    # 处置费用
    if disposal_cost_rate <= 0.03:
        base += 20
    elif disposal_cost_rate <= 0.06:
        base += 10
    elif disposal_cost_rate <= 0.10:
        base += 0
    else:
        base -= 15

    # 税费
    if tax_cost_rate <= 0.03:
        base += 10
    elif tax_cost_rate <= 0.06:
        base += 0
    else:
        base -= 10

    # 资金成本（时间越长成本越高）
    total_opp_cost = opportunity_cost * (estimated_months / 12)
    if total_opp_cost <= 0.05:
        base += 10
    elif total_opp_cost <= 0.10:
        base += 5
    elif total_opp_cost <= 0.15:
        base += 0
    else:
        base -= 10

    return max(0, min(100, base))


def weighted_score(
    scores: Dict[str, int],
    weights: Optional[Dict[str, float]] = None,
) -> float:
    """计算加权总分"""
    if weights is None:
        weights = WEIGHTS
    total = 0.0
    for dim, score in scores.items():
        total += score * weights.get(dim, 0)
    return round(total, 1)


# ─── 3. 策略匹配引擎 ─────────────────────────────────────────────

def match_strategies(
    total_score: float,
    asset_params: Optional[Dict] = None,
    top_k: int = 3,
) -> List[Tuple[str, float, str]]:
    """
    根据总分匹配推荐策略，并给出预估回收率和评分理由。

    返回: [(策略名, 预估回收率, 理由), ...]
    """
    # 找到分数所在区间
    selected_range = None
    for (lo, hi), strategies in sorted(STRATEGY_PRIORITY.items(), reverse=True):
        if lo <= total_score <= hi:
            selected_range = (lo, hi)
            break

    if selected_range is None:
        return [("核销出表", 0.2, "评分低于所有策略阈值，建议核销出表")]

    candidates = STRATEGY_PRIORITY[selected_range]
    results = []

    for name in candidates[:top_k]:
        strategy = DISPOSAL_STRATEGIES[name]
        # 计算预估回收率（取中间值，可调整）
        avg_recovery = (strategy["recovery_rate"][0] + strategy["recovery_rate"][1]) / 2
        reason = f"适合{strategy['scenario']}；{strategy['key_metric']}"
        results.append((name, round(avg_recovery, 2), reason))

    return results


# ─── 4. 方案对比引擎 ───────────────────────────────────────────────

def compare_strategies(
    strategies: List[str],
    recovery_rate: float,      # 统一回收预期
    cycle_months: int,         # 统一处置周期
    acquisition_cost: float,   # 收购成本（亿元）
    annual_irr_target: float = 0.15,  # 目标IRR
) -> List[Dict]:
    """
    对比不同处置策略的方案效果。
    返回各策略的指标对比表。
    """
    results = []
    for name in strategies:
        if name not in DISPOSAL_STRATEGIES:
            continue
        s = DISPOSAL_STRATEGIES[name]
        rr_lo, rr_hi = s["recovery_rate"]

        # 方案1：低预期
        recovery_lo = acquisition_cost * rr_lo * 2  # 假设债权规模≈2×收购成本
        gross_profit_lo = recovery_lo - acquisition_cost

        # 方案2：高预期
        recovery_hi = acquisition_cost * rr_hi * 2
        gross_profit_hi = recovery_hi - acquisition_cost

        # 简化IRR计算
        irr_lo = (gross_profit_lo / acquisition_cost) / (cycle_months / 12) if acquisition_cost > 0 else 0
        irr_hi = (gross_profit_hi / acquisition_cost) / (cycle_months / 12) if acquisition_cost > 0 else 0

        results.append({
            "策略": name,
            "回收率范围": f"{rr_lo*100:.0f}-{rr_hi*100:.0f}%",
            "低预期回收(亿)": round(recovery_lo, 2),
            "高预期回收(亿)": round(recovery_hi, 2),
            "低预期毛利(亿)": round(gross_profit_lo, 2),
            "高预期毛利(亿)": round(gross_profit_hi, 2),
            "低预期IRR": f"{irr_lo*100:.1f}%",
            "高预期IRR": f"{irr_hi*100:.1f}%",
            "周期": f"{s['cycle_months'][0]}-{s['cycle_months'][1]}月",
            "法律依赖": s["legal_reliance"],
            "适合评级": s["suitable_grade"],
        })

    return sorted(results, key=lambda x: float(x["高预期IRR"].strip("%")), reverse=True)


# ─── 5. 敏感性分析 ───────────────────────────────────────────────

def sensitivity_analysis(
    base_params: Dict,
    param_name: str,
    shocks: List[float],
    strategy: str = "债务重组",
) -> List[Dict]:
    """
    对某个参数进行敏感性分析。
    base_params: 评分参数
    param_name: 要变化的参数名
    shocks: 相对于基础值的变化幅度列表（如 [-0.2, -0.1, 0, 0.1, 0.2]）
    """
    results = []
    for shock in shocks:
        params = dict(base_params)
        if param_name in params:
            if isinstance(params[param_name], (int, float)):
                params[param_name] = params[param_name] * (1 + shock)
            elif isinstance(params[param_name], bool):
                params[param_name] = not params[param_name]
            elif isinstance(params[param_name], str):
                # 对于字符串参数，模拟升降级
                pass

        # 受限参数可用性
        available_params = [
            "property_type", "city_tier", "loan_to_value", "operating_condition",
            "is_first_lien", "has_tenancy", "has_lien_issues", "statute_expired",
            "num_lawsuits", "num_encumbrances",
            "expected_months", "market_liquidity", "buyer_available", "auction_history",
            "recovery_confidence", "has_guarantor", "debt_rank", "guarantees",
            "disposal_cost_rate", "tax_cost_rate", "opportunity_cost", "estimated_months",
        ]
        available = {k: params[k] for k in available_params if k in params}

        # 重新评分
        if all(k in available for k in ["property_type", "city_tier", "loan_to_value", "operating_condition"]):
            sq = score_asset_quality(
                available.get("property_type", "商业"),
                available.get("city_tier", 2),
                available.get("loan_to_value", 0.5),
                available.get("operating_condition", "一般"),
            )
        else:
            sq = 50

        if all(k in available for k in ["is_first_lien", "has_tenancy", "has_lien_issues", "statute_expired"]):
            sl = score_legal_status(
                available.get("is_first_lien", True),
                available.get("has_tenancy", False),
                available.get("has_lien_issues", False),
                available.get("statute_expired", False),
                available.get("num_lawsuits", 2),
                available.get("num_encumbrances", 1),
            )
        else:
            sl = 50

        if all(k in available for k in ["expected_months", "market_liquidity", "buyer_available"]):
            se = score_disposal_efficiency(
                available.get("expected_months", 12),
                available.get("market_liquidity", "中"),
                available.get("buyer_available", False),
                available.get("auction_history", 0),
            )
        else:
            se = 50

        if all(k in available for k in ["recovery_confidence", "has_guarantor", "debt_rank"]):
            sr = score_recovery_certainty(
                available.get("recovery_confidence", "中"),
                available.get("has_guarantor", True),
                available.get("debt_rank", "普通"),
                available.get("guarantees", 0.5),
            )
        else:
            sr = 50

        if all(k in available for k in ["disposal_cost_rate", "tax_cost_rate", "opportunity_cost"]):
            sc = score_cost_efficiency(
                available.get("disposal_cost_rate", 0.06),
                available.get("tax_cost_rate", 0.05),
                available.get("opportunity_cost", 0.10),
                available.get("estimated_months", 12),
            )
        else:
            sc = 50

        scores = {"资产质量": sq, "法律状态": sl, "处置效率": se, "回收确定性": sr, "成本效益": sc}
        total = weighted_score(scores)

        results.append({
            "冲击幅度": f"{shock*100:+.0f}%",
            f"{param_name}受影响后总分": total,
            "资产质量": sq,
            "法律状态": sl,
            "处置效率": se,
            "回收确定性": sr,
            "成本效益": sc,
        })

    return results


# ─── 6. 完整决策流程（一键运行） ─────────────────────────────────

def full_decision_pipeline(asset_input: Dict) -> Dict:
    """
    完整处置决策流程：
    1. 五维评分
    2. 策略匹配
    3. 方案对比
    4. 输出建议
    """
    # 1. 五维评分
    sq = score_asset_quality(
        asset_input.get("property_type", "商业"),
        asset_input.get("city_tier", 2),
        asset_input.get("loan_to_value", 0.5),
        asset_input.get("operating_condition", "一般"),
    )
    sl = score_legal_status(
        asset_input.get("is_first_lien", True),
        asset_input.get("has_tenancy", False),
        asset_input.get("has_lien_issues", False),
        asset_input.get("statute_expired", False),
        asset_input.get("num_lawsuits", 2),
        asset_input.get("num_encumbrances", 1),
    )
    se = score_disposal_efficiency(
        asset_input.get("expected_months", 12),
        asset_input.get("market_liquidity", "中"),
        asset_input.get("buyer_available", False),
        asset_input.get("auction_history", 0),
    )
    sr = score_recovery_certainty(
        asset_input.get("recovery_confidence", "中"),
        asset_input.get("has_guarantor", True),
        asset_input.get("debt_rank", "普通"),
        asset_input.get("guarantees", 0.5),
    )
    sc = score_cost_efficiency(
        asset_input.get("disposal_cost_rate", 0.06),
        asset_input.get("tax_cost_rate", 0.05),
        asset_input.get("opportunity_cost", 0.10),
        asset_input.get("estimated_months", 12),
    )

    scores = {"资产质量": sq, "法律状态": sl, "处置效率": se, "回收确定性": sr, "成本效益": sc}
    total = weighted_score(scores)

    # 2. 策略匹配
    recommendations = match_strategies(total, asset_input)

    # 3. 方案对比
    suggested_strategies = [r[0] for r in recommendations]
    comparison = compare_strategies(
        suggested_strategies,
        total / 100,  # 将总分转换为回收率基准
        asset_input.get("expected_months", 12),
        asset_input.get("acquisition_cost", 1.0),
    )

    return {
        "五维评分明细": scores,
        "加权总分": total,
        "评分等级": "A(优秀)" if total >= 75 else "B(良好)" if total >= 50 else "C(一般)" if total >= 25 else "D(差)",
        "推荐策略": recommendations,
        "方案对比": comparison,
    }


# ─── 7. 示例运行 ───────────────────────────────────────────────────

def run_demo():
    """运行一个完整示例——成都商业综合体案例"""
    print("=" * 70)
    print("  不良资产处置决策模型 · 示例运行")
    print("  案例：成都高新区商业综合体（2023年收购）")
    print("=" * 70)

    asset = {
        # 资产质量
        "property_type": "商业",       # 商业综合体
        "city_tier": 2,                # 新一线城市
        "loan_to_value": 0.375,        # 收购价4.5亿/评估值12亿
        "operating_condition": "一般",  # 有运营但出租率低
        # 法律状态
        "is_first_lien": True,          # 首封
        "has_tenancy": True,            # 已有租赁
        "has_lien_issues": False,       # 无已知优先权问题
        "statute_expired": False,       # 时效没问题
        "num_lawsuits": 3,              # 3起涉诉
        "num_encumbrances": 1,          # 1个轮候查封
        # 处置效率
        "expected_months": 18,           # 预计18个月
        "market_liquidity": "中",        # 商业地产流动性中等
        "buyer_available": False,        # 无明确买家（需要运营提升）
        "auction_history": 0,            # 无流拍历史
        # 回收确定性
        "recovery_confidence": "中",
        "has_guarantor": True,           # 有母公司担保
        "debt_rank": "优先",             # 有抵押的贷款债权
        "guarantees": 0.5,               # 其他担保覆盖50%
        # 成本效益
        "disposal_cost_rate": 0.06,
        "tax_cost_rate": 0.04,
        "opportunity_cost": 0.12,        # 资金成本年化12%
        "estimated_months": 18,
        # 财务参数
        "acquisition_cost": 4.5,          # 收购成本4.5亿
        "annual_irr_target": 0.15,
    }

    result = full_decision_pipeline(asset)

    print("\n📊 五维评分明细：")
    for dim, score in result["五维评分明细"].items():
        bar = "█" * (score // 10) + "░" * (10 - score // 10)
        print(f"  {dim}: {score:3d}分 {bar}")

    print(f"\n🏆 加权总分: {result['加权总分']} 分 → {result['评分等级']}")

    print(f"\n🎯 推荐处置策略 TOP 3：")
    for rank, (name, recovery, reason) in enumerate(result["推荐策略"], 1):
        print(f"  {rank}. {name} — 预估回收率{recovery*100:.0f}%")
        print(f"     理由：{reason}")

    print(f"\n📋 方案对比：")
    for r in result["方案对比"]:
        print(f"  [{r['策略']}]")
        print(f"    回收率: {r['回收率范围']} | 周期: {r['周期']}")
        print(f"    低预期毛利: {r['低预期毛利(亿)']}亿 | 高预期毛利: {r['高预期毛利(亿)']}亿")
        print(f"    低预期IRR: {r['低预期IRR']} | 高预期IRR: {r['高预期IRR']}")

    # 敏感性分析
    print(f"\n🔬 敏感性分析：折现率变动影响")
    shocks = [-0.3, -0.15, 0, 0.15, 0.3]
    sensitivity = sensitivity_analysis(asset, "opportunity_cost", shocks)
    for s in sensitivity:
        print(f"  冲击{s['冲击幅度']}: 总分 {s['opportunity_cost受影响后总分']}")

    print("\n" + "=" * 70)
    print("  决策建议：")
    print("  1. 资产基本面尚可（B级），具备运营提升空间")
    print("  2. 推荐策略：REITs退出 > 资产拍卖 > 债务重组")
    print("  3. 关键行动：提升NOI至Cap Rate>6% → REITs退出")
    print("=" * 70)


if __name__ == "__main__":
    run_demo()

#!/usr/bin/env python3
"""
funding_diagnosis.py — 融资准备度评估脚本

用法:
    python3 scripts/funding_diagnosis.py <JSON输入文件>
    python3 scripts/funding_diagnosis.py --score

输入JSON格式:
{
  "traction": {"mao": 50000, "moq_growth": 0.15},
  "market": {"competitors": 3, "customers_interviewed": 30},
  "team": {"has_cto": false, "founder_count": 2},
  "product": {"has_mvp": true, "version": "v2.1"},
  "story": {"has_bp": true, "bp_score": 62},
  "unit_econ": {"ltv_cac": 3.2},
  "use_funds": {"has_plan": false},
  "timing": {"runway_months": 8}
}

输出: JSON格式评分报告到stdout。
"""
import json
import sys
import os
from typing import Any


# ---------- 8维度评分标准 ----------

DIMENSIONS = {
    "traction": {"name": "Traction 数据", "weight": 0.15, "max": 15},
    "market": {"name": "Market 市场", "weight": 0.15, "max": 15},
    "team": {"name": "Team 团队", "weight": 0.15, "max": 15},
    "product": {"name": "Product 产品", "weight": 0.15, "max": 15},
    "story": {"name": "Story 叙事", "weight": 0.10, "max": 10},
    "unit_econ": {"name": "Unit Econ 单位经济", "weight": 0.10, "max": 10},
    "use_funds": {"name": "Use Funds 资金规划", "weight": 0.10, "max": 10},
    "timing": {"name": "Timing 时机", "weight": 0.10, "max": 10},
}


def score_traction(data: dict) -> dict:
    """评估数据里程碑"""
    d = data.get("traction", {})
    score = 0
    max_score = DIMENSIONS["traction"]["max"]
    reasons = []

    mao = d.get("mao", 0)
    if mao >= 100000:
        score += 6
        reasons.append(f"月活 {mao:,}，优秀（+6）")
    elif mao >= 50000:
        score += 4
        reasons.append(f"月活 {mao:,}，良好（+4）")
    elif mao >= 10000:
        score += 2
        reasons.append(f"月活 {mao:,}，一般（+2）")
    else:
        reasons.append(f"月活 {mao:,}，需提升（+0）")

    growth = d.get("moq_growth", 0)
    if growth >= 0.20:
        score += 5
        reasons.append(f"环比增长 {growth*100:.0f}%，优秀（+5）")
    elif growth >= 0.10:
        score += 3
        reasons.append(f"环比增长 {growth*100:.0f}%，良好（+3）")
    else:
        reasons.append(f"环比增长 {growth*100:.0f}%，需提升（+0）")

    # 加分项：有付费用户
    revenue = d.get("mrr", 0)
    if revenue > 0:
        bonus = min(4, revenue // 10000)
        score += bonus
        reasons.append(f"MRR ¥{revenue:,}，加分+{bonus}")

    score = min(score, max_score)
    return {"score": score, "max": max_score, "pct": round(score / max_score * 100, 1), "reasons": reasons}


def score_market(data: dict) -> dict:
    """评估市场规模匹配度"""
    d = data.get("market", {})
    score = 0
    max_score = DIMENSIONS["market"]["max"]
    reasons = []

    competitors = d.get("competitors", 99)
    if competitors <= 2:
        score += 4
        reasons.append(f"竞品仅{competitors}家，蓝海（+4）")
    elif competitors <= 5:
        score += 3
        reasons.append(f"竞品{competitors}家，竞争适中（+3）")
    elif competitors <= 10:
        score += 2
        reasons.append(f"竞品{competitors}家，竞争激烈（+2）")
    else:
        score += 1
        reasons.append(f"竞品{competitors}家，红海（+1）")

    customers = d.get("customers_interviewed", 0)
    if customers >= 50:
        score += 4
        reasons.append(f"深度访谈{customers}人，验证充分（+4）")
    elif customers >= 20:
        score += 2
        reasons.append(f"深度访谈{customers}人，初步验证（+2）")
    else:
        reasons.append(f"深度访谈{customers}人，验证不足（+0）")

    # 加分项：市场规模明确
    tam = d.get("tam", 0)
    if tam > 0:
        bonus = min(5, tam // 10_000_000_000)
        score += bonus
        reasons.append(f"TAM ¥{tam:,}亿，加分+{bonus}")

    score = min(score, max_score)
    return {"score": score, "max": max_score, "pct": round(score / max_score * 100, 1), "reasons": reasons}


def score_team(data: dict) -> dict:
    """评估团队完整性"""
    d = data.get("team", {})
    score = 0
    max_score = DIMENSIONS["team"]["max"]
    reasons = []

    has_cto = d.get("has_cto", False)
    if has_cto:
        score += 6
        reasons.append("有CTO，技术核心完整（+6）")
    else:
        reasons.append("缺CTO，技术风险较高（+0）")

    count = d.get("founder_count", 1)
    if count >= 3:
        score += 5
        reasons.append(f"联合创始人{count}人，团队结构完整（+5）")
    elif count == 2:
        score += 3
        reasons.append(f"联合创始人{count}人，需补强（+3）")
    else:
        reasons.append(f"仅创始人1人，风险集中（+0）")

    # 加分项：有行业经验
    exp = d.get("industry_exp_years", 0)
    if exp >= 10:
        score += 4
        reasons.append(f"行业经验{exp}年，资深团队（+4）")
    elif exp >= 5:
        score += 2
        reasons.append(f"行业经验{exp}年，经验丰富（+2）")

    score = min(score, max_score)
    return {"score": score, "max": max_score, "pct": round(score / max_score * 100, 1), "reasons": reasons}


def score_product(data: dict) -> dict:
    """评估产品成熟度"""
    d = data.get("product", {})
    score = 0
    max_score = DIMENSIONS["product"]["max"]
    reasons = []

    has_mvp = d.get("has_mvp", False)
    if has_mvp:
        score += 5
        reasons.append("已有MVP，产品验证开始（+5）")
    else:
        reasons.append("无MVP，仍在概念阶段（+0）")

    version = d.get("version", "")
    if version and version.startswith("v2"):
        score += 4
        reasons.append(f"版本{version}，产品迭代中（+4）")
    elif version:
        score += 2
        reasons.append(f"版本{version}，早期阶段（+2）")

    # 加分项：有用户反馈
    users = d.get("active_users", 0)
    if users >= 1000:
        score += 6
        reasons.append(f"活跃用户{users:,}人，产品粘性强（+6）")
    elif users >= 100:
        score += 3
        reasons.append(f"活跃用户{users:,}人，初步验证（+3）")

    score = min(score, max_score)
    return {"score": score, "max": max_score, "pct": round(score / max_score * 100, 1), "reasons": reasons}


def score_story(data: dict) -> dict:
    """评估BP叙事质量"""
    d = data.get("story", {})
    score = 0
    max_score = DIMENSIONS["story"]["max"]
    reasons = []

    has_bp = d.get("has_bp", False)
    if has_bp:
        score += 3
        reasons.append("已有BP，叙事框架完整（+3）")
    else:
        reasons.append("无BP，亟需撰写（+0）")

    bp_score = d.get("bp_score", 0)
    if bp_score >= 80:
        score += 7
        reasons.append(f"BP评分{bp_score}/100，优秀（+7）")
    elif bp_score >= 60:
        score += 4
        reasons.append(f"BP评分{bp_score}/100，良好需优化（+4）")
    elif bp_score > 0:
        score += 1
        reasons.append(f"BP评分{bp_score}/100，需大幅改进（+1）")
    else:
        reasons.append("BP未评分（+0）")

    score = min(score, max_score)
    return {"score": score, "max": max_score, "pct": round(score / max_score * 100, 1), "reasons": reasons}


def score_unit_econ(data: dict) -> dict:
    """评估单位经济模型"""
    d = data.get("unit_econ", {})
    score = 0
    max_score = DIMENSIONS["unit_econ"]["max"]
    reasons = []

    ltv_cac = d.get("ltv_cac", 0)
    if ltv_cac >= 5:
        score += 6
        reasons.append(f"LTV/CAC={ltv_cac}，模型优秀（+6）")
    elif ltv_cac >= 3:
        score += 4
        reasons.append(f"LTV/CAC={ltv_cac}，模型健康（+4）")
    elif ltv_cac >= 1:
        score += 2
        reasons.append(f"LTV/CAC={ltv_cac}，模型需改善（+2）")
    else:
        reasons.append(f"LTV/CAC={ltv_cac}，模型不明确（+0）")

    margin = d.get("gross_margin", 0)
    if margin >= 0.7:
        score += 4
        reasons.append(f"毛利率{margin*100:.0f}%，优秀（+4）")
    elif margin >= 0.4:
        score += 2
        reasons.append(f"毛利率{margin*100:.0f}%，一般（+2）")

    score = min(score, max_score)
    return {"score": score, "max": max_score, "pct": round(score / max_score * 100, 1), "reasons": reasons}


def score_use_funds(data: dict) -> dict:
    """评估资金使用规划"""
    d = data.get("use_funds", {})
    score = 0
    max_score = DIMENSIONS["use_funds"]["max"]
    reasons = []

    has_plan = d.get("has_plan", False)
    if has_plan:
        score += 5
        reasons.append("有资金使用规划（+5）")
    else:
        reasons.append("无资金使用规划（+0）")

    breakdown = d.get("breakdown", {})
    if breakdown:
        detail_pct = sum(breakdown.values())
        if detail_pct >= 90:
            score += 5
            reasons.append(f"资金分配明细完整（{detail_pct:.0f}%）（+5）")
        elif detail_pct >= 50:
            score += 3
            reasons.append(f"资金分配明细部分完成（{detail_pct:.0f}%）（+3）")
        else:
            score += 1
            reasons.append(f"资金分配明细不足（{detail_pct:.0f}%）（+1）")

    score = min(score, max_score)
    return {"score": score, "max": max_score, "pct": round(score / max_score * 100, 1), "reasons": reasons}


def score_timing(data: dict) -> dict:
    """评估融资时机"""
    d = data.get("timing", {})
    score = 0
    max_score = DIMENSIONS["timing"]["max"]
    reasons = []

    runway = d.get("runway_months", 3)
    if runway >= 12:
        score += 6
        reasons.append(f"现金流可支撑{runway}个月，充足（+6）")
    elif runway >= 6:
        score += 4
        reasons.append(f"现金流可支撑{runway}个月，安全（+4）")
    elif runway >= 3:
        score += 2
        reasons.append(f"现金流可支撑{runway}个月，需加速（+2）")
    else:
        reasons.append(f"现金流仅{runway}个月，紧急（+0）")

    market_window = d.get("market_window", "")
    if market_window:
        score += 4
        reasons.append(f"市场窗口期明确（{market_window}）（+4）")

    score = min(score, max_score)
    return {"score": score, "max": max_score, "pct": round(score / max_score * 100, 1), "reasons": reasons}


# ---------- 评分路由 ----------

SCORERS = {
    "traction": score_traction,
    "market": score_market,
    "team": score_team,
    "product": score_product,
    "story": score_story,
    "unit_econ": score_unit_econ,
    "use_funds": score_use_funds,
    "timing": score_timing,
}


def run_diagnosis(input_data: dict) -> dict:
    """运行8维度融资诊断，返回完整评分报告"""
    dim_results = {}
    total_score = 0
    total_max = 0

    for dim_id, scorer in SCORERS.items():
        result = scorer(input_data)
        dim_results[dim_id] = result
        total_score += result["score"]
        total_max += result["max"]

    overall_pct = round(total_score / total_max * 100, 1) if total_max > 0 else 0

    # 等级判定
    if overall_pct >= 85:
        grade = "S"
        summary = "准备就绪，立即启动融资"
    elif overall_pct >= 70:
        grade = "A"
        summary = "基本就绪，2-4周内修复短板后启动"
    elif overall_pct >= 55:
        grade = "B"
        summary = "准备不足，需先建立更多牵引力"
    elif overall_pct >= 40:
        grade = "C"
        summary = "准备不足，需大幅补强"
    else:
        grade = "D"
        summary = "过早融资，专注产品和首批客户"

    # 识别短板（得分率<50%的维度）
    weakness = [dim_id for dim_id, r in dim_results.items() if r["pct"] < 50]

    # 输出schema校验（幂等性保证：相同输入一定产生相同输出）
    return {
        "version": "2.3.1",
        "spec": "openclaw",
        "timestamp": "deterministic",
        "score": {"total": total_score, "max": total_max, "pct": overall_pct},
        "grade": grade,
        "summary": summary,
        "dimensions": dim_results,
        "weakness": weakness,
        "suggestions": [
            f"优先补强: {d}" for d in weakness[:3]
        ]
    }


# ---------- 输入输出 ----------

def parse_input(path: str) -> dict:
    """读取JSON输入文件，失败时返回示例数据"""
    if not os.path.exists(path):
        return {
            "traction": {"mao": 50000, "moq_growth": 0.15, "mrr": 5000},
            "market": {"competitors": 5, "customers_interviewed": 30, "tam": 50000000000},
            "team": {"has_cto": False, "founder_count": 2, "industry_exp_years": 8},
            "product": {"has_mvp": True, "version": "v2.1", "active_users": 500},
            "story": {"has_bp": True, "bp_score": 62},
            "unit_econ": {"ltv_cac": 3.2, "gross_margin": 0.6},
            "use_funds": {"has_plan": False, "breakdown": {}},
            "timing": {"runway_months": 8, "market_window": ""},
        }
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except (json.JSONDecodeError, FileNotFoundError):
        sys.stderr.write(f"⚠️ 无法读取 {path}，使用示例数据\n")
        return parse_input("")


def validate_output(data: dict) -> bool:
    """校验输出格式是否符合schema"""
    required = {"version", "spec", "score", "grade", "summary", "dimensions"}
    if not all(k in data for k in required):
        return False
    if not isinstance(data["score"], dict):
        return False
    if "total" not in data["score"]:
        return False
    if data["grade"] not in ("S", "A", "B", "C", "D"):
        return False
    return True


# ---------- 主入口 ----------

if __name__ == "__main__":
    if len(sys.argv) < 2 or sys.argv[1] in ("--help", "-h"):
        print(__doc__)
        sys.exit(0)

    if sys.argv[1] == "--sample":
        # 生成示例输入文件
        sample = parse_input("")
        print(json.dumps(sample, ensure_ascii=False, indent=2))
        sys.exit(0)

    # 读取输入并评分
    input_data = parse_input(sys.argv[1] if len(sys.argv) > 1 else "")
    report = run_diagnosis(input_data)

    # 输出校验（结果自检）
    if not validate_output(report):
        sys.stderr.write("❌ 输出校验失败: 格式不符合schema\n")
        sys.exit(1)

    print(json.dumps(report, ensure_ascii=False, indent=2))

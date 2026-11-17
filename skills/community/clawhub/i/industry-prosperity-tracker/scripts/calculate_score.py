"""
calculate_score.py - 景气度综合评分计算

根据指标数据计算0-100景气综合评分和方向判断。
实现评分方法论详见 references/scoring_methodology.md

用法:
    python calculate_score.py --input data/semiconductor_latest.json --output data/semiconductor_scored.json
"""

import json
import argparse
import os


# ============================================================
# 评分核心逻辑
# ============================================================

# 方向判断阈值
DEFAULT_THRESHOLD_PCT = 2.0      # 百分比类指标: MoM变化 > 2% 视为显著
DEFAULT_THRESHOLD_PP = 0.5        # 百分点类指标: 变化 > 0.5pp 视为显著
DEFAULT_THRESHOLD_INDEX = 1.0     # 指数类指标(如PMI): 变化 > 1.0 视为显著


def determine_direction(indicator):
    """
    根据环比变化判断指标方向: +1(上行), 0(持平), -1(下行)
    
    反向指标(inverted=True)取反方向。
    """
    mom_change = indicator.get("mom_change")
    if mom_change is None:
        return 0, "数据缺失"
    
    # 选择阈值
    name = indicator.get("name", "")
    if "PMI" in name or "指数" in name:
        threshold = DEFAULT_THRESHOLD_INDEX
    elif "毛利率" in name or "率" in name:
        threshold = DEFAULT_THRESHOLD_PP
    else:
        threshold = DEFAULT_THRESHOLD_PCT
    
    # 判断方向
    if mom_change > threshold:
        direction = 1
        label = "上行"
    elif mom_change < -threshold:
        direction = -1
        label = "下行"
    else:
        direction = 0
        label = "持平"
    
    # 反向指标取反（如存货周转天数：天数下降 = 景气上行）
    if indicator.get("inverted", False):
        direction = -direction
        if direction == 1:
            label = "上行"
        elif direction == -1:
            label = "下行"
    
    return direction, label


def calculate_composite_score(indicators):
    """
    计算综合景气评分。
    
    Step 1: 每个指标方向 +1/0/-1
    Step 2: 加权求和 → raw_score ∈ [-1, +1]
    Step 3: 映射到 0-100 → prosperity_score
    """
    results = []
    total_weight_used = 0.0
    raw_score = 0.0
    
    for ind in indicators:
        direction, label = determine_direction(ind)
        weight = ind.get("weight", 0)
        
        # 数据缺失的指标不参与评分，权重按比例分配
        if direction == 0 and ind.get("needs_manual_input"):
            continue
        
        contribution = direction * weight
        raw_score += contribution
        total_weight_used += weight
        
        results.append({
            "id": ind["id"],
            "name": ind["name"],
            "tier": ind["tier"],
            "weight": weight,
            "value": ind.get("value"),
            "value_unit": ind.get("value_unit", ""),
            "prev_value": ind.get("prev_value"),
            "mom_change": ind.get("mom_change"),
            "data_date": ind.get("data_date", ""),
            "data_source": ind.get("data_source", ""),
            "inverted": ind.get("inverted", False),
            "direction": direction,
            "direction_label": label,
            "contribution": round(contribution, 4),
            "note": ind.get("note", ""),
        })
    
    # 如果有缺失指标，重新归一化权重
    if total_weight_used > 0 and total_weight_used < 1.0:
        raw_score = raw_score / total_weight_used
    
    # 映射到 0-100
    prosperity_score = round((raw_score + 1.0) * 50, 1)
    
    return prosperity_score, raw_score, results


def determine_direction_label(score):
    """根据评分判断景气方向"""
    if score > 60:
        return "景气上行", "多数指标改善，处于周期上升阶段"
    elif score >= 40:
        return "景气平稳/拐点", "多空交织，可能处于周期转折区域"
    else:
        return "景气下行", "多数指标恶化，处于周期下降阶段"


def extract_key_signals(scored_indicators):
    """提取Top 3正向信号和Top 3负向信号"""
    positive = [i for i in scored_indicators if i["direction"] == 1]
    negative = [i for i in scored_indicators if i["direction"] == -1]
    
    # 按权重排序
    positive.sort(key=lambda x: x["weight"], reverse=True)
    negative.sort(key=lambda x: x["weight"], reverse=True)
    
    return positive[:3], negative[:3]


def calculate_historical_percentile(indicators, history=None):
    """
    计算每个指标在过去12个月的分位数。
    
    history参数: 过去12个月的指标数据（如果有）。
    如果没有历史数据，返回None。
    
    分位数仅作为参考信息，不参与评分。
    """
    if not history:
        return {ind["id"]: None for ind in indicators}
    
    percentiles = {}
    for ind in indicators:
        ind_id = ind["id"]
        current_val = ind.get("value")
        if current_val is None:
            percentiles[ind_id] = None
            continue
        
        hist_values = [h.get(ind_id, {}).get("value") for h in history]
        hist_values = [v for v in hist_values if v is not None]
        
        if len(hist_values) < 3:
            percentiles[ind_id] = None
            continue
        
        rank = sum(1 for v in hist_values if v <= current_val)
        percentile = round(rank / len(hist_values) * 100, 1)
        percentiles[ind_id] = percentile
    
    return percentiles


# ============================================================
# 主入口
# ============================================================

def main():
    parser = argparse.ArgumentParser(description="景气度评分计算")
    parser.add_argument("--input", type=str, required=True,
                       help="输入JSON文件路径 (fetch_indicators.py的输出)")
    parser.add_argument("--output", type=str, required=True,
                       help="输出JSON文件路径")
    parser.add_argument("--history", type=str, default=None,
                       help="历史数据JSON文件路径（用于计算分位数）")
    args = parser.parse_args()
    
    # 加载数据
    with open(args.input, "r", encoding="utf-8") as f:
        data = json.load(f)
    
    # 加载历史数据（可选）
    history = None
    if args.history and os.path.exists(args.history):
        with open(args.history, "r", encoding="utf-8") as f:
            history = json.load(f)
    
    # 计算评分
    score, raw, results = calculate_composite_score(data["indicators"])
    direction, direction_desc = determine_direction_label(score)
    positive_signals, negative_signals = extract_key_signals(results)
    percentiles = calculate_historical_percentile(data["indicators"], history)
    
    # 组装输出
    output = {
        "industry": data.get("industry"),
        "industry_name": data.get("industry_name", ""),
        "fetch_date": data.get("fetch_date", ""),
        "report_period": data.get("fetch_date", ""),
        "prosperity_score": score,
        "raw_score": round(raw, 4),
        "direction": direction,
        "direction_description": direction_desc,
        "indicators": results,
        "positive_signals": positive_signals,
        "negative_signals": negative_signals,
        "percentiles": percentiles,
        "sample_data": data.get("sample_data", False),
        "compliance_note": "本评分仅基于公开数据计算的指标方向汇总，不构成投资建议"
    }
    
    # 保存
    os.makedirs(os.path.dirname(args.output), exist_ok=True)
    with open(args.output, "w", encoding="utf-8") as f:
        json.dump(output, f, ensure_ascii=False, indent=2)
    
    print(f"[OK] 评分完成")
    print(f"     行业: {output['industry_name']}")
    print(f"     综合评分: {score}/100")
    print(f"     方向: {direction}")
    print(f"     正向信号: {len(positive_signals)} 个")
    print(f"     负向信号: {len(negative_signals)} 个")


if __name__ == "__main__":
    main()

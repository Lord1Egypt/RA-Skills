#!/usr/bin/env python3
"""
电商价格分布建模与风险分析脚本

功能：
- 计算价格分布指标（P10/P25/P50/P75/P90）
- 使用定量规则判断异常价格
- 基于显性特征计算风险评分（渠道风险、条件复杂度、售后不确定性、价格偏离度）
- 生成三层输出：L1用户决策层、L2风险解释层、L3模型证据层
"""

import json
import sys
from typing import List, Dict, Any, Tuple
import numpy as np


def parse_args():
    """解析命令行参数"""
    if len(sys.argv) < 2:
        print("用法: python price_analyzer.py <price_data_json>")
        print("示例: python price_analyzer.py '{\"price_list\": [5000, 5200, 4800, 6000], \"platform_info\": [{\"platform\": \"京东\", \"price\": 5200}]}'")
        sys.exit(1)
    
    try:
        return json.loads(sys.argv[1])
    except json.JSONDecodeError as e:
        print(f"JSON解析错误: {e}")
        sys.exit(1)


def calculate_price_distribution(prices: List[float]) -> Dict[str, Any]:
    """
    计算价格分布指标
    
    参数:
        prices: 价格列表
        
    返回:
        包含 P10/P25/P50/P75/P90 的字典
    """
    if not prices:
        return {}
    
    prices_array = np.array(prices)
    
    return {
        "p10": float(np.percentile(prices_array, 10)),
        "p25": float(np.percentile(prices_array, 25)),
        "p50": float(np.percentile(prices_array, 50)),
        "p75": float(np.percentile(prices_array, 75)),
        "p90": float(np.percentile(prices_array, 90)),
        "mean": float(np.mean(prices_array)),
        "min": float(np.min(prices_array)),
        "max": float(np.max(prices_array))
    }


def detect_abnormal_prices(prices: List[float], distribution: Dict[str, Any]) -> Dict[str, Any]:
    """
    使用定量规则判断异常价格
    
    参数:
        prices: 价格列表
        distribution: 价格分布指标
        
    返回:
        包含异常价格检测结果和分类的字典
    """
    if not distribution:
        return {"abnormal_prices": [], "classification": {}}
    
    p10 = distribution.get("p10", 0)
    p25 = distribution.get("p25", 0)
    
    strong_abnormal_threshold = p10 * 0.9
    medium_abnormal_threshold = p25 * 0.95
    
    strong_abnormal = []
    medium_abnormal = []
    normal = []
    
    for price in prices:
        if price < strong_abnormal_threshold:
            strong_abnormal.append(price)
        elif price < medium_abnormal_threshold:
            medium_abnormal.append(price)
        else:
            normal.append(price)
    
    return {
        "strong_abnormal": strong_abnormal,
        "medium_abnormal": medium_abnormal,
        "thresholds": {
            "strong_abnormal_threshold": strong_abnormal_threshold,
            "medium_abnormal_threshold": medium_abnormal_threshold
        }
    }


def calculate_explicit_risk_features(price: float, distribution: Dict[str, Any], 
                                    conditions: str = "", seller_type: str = "") -> Dict[str, Any]:
    """
    基于显性特征计算风险评分
    
    参数:
        price: 当前价格
        distribution: 价格分布指标
        conditions: 价格条件描述（如"限新用户"、"官方自营"等）
        seller_type: 卖家类型
        
    返回:
        包含四个显性特征评分的字典
    """
    p10 = distribution.get("p10", 0)
    p25 = distribution.get("p25", 0)
    p90 = distribution.get("p90", 0)
    
    # 显性特征1：渠道风险（0-25分）
    channel_risk = 0
    if seller_type == "official":
        channel_risk = 0
    elif seller_type == "authorized":
        channel_risk = 5
    elif seller_type == "subsidized":
        channel_risk = 10
    else:  # third-party
        channel_risk = 15
    
    # 显性特征2：条件复杂度（0-25分）
    condition_complexity = 0
    high_risk_conditions = ["限新用户", "限地区", "需会员", "限时", "限量", "秒杀", "翻新", "官翻"]
    medium_risk_conditions = ["需领券", "满减", "返现"]
    
    for condition in high_risk_conditions:
        if condition in conditions:
            condition_complexity += 5
    
    for condition in medium_risk_conditions:
        if condition in conditions:
            condition_complexity += 2
    
    condition_complexity = min(condition_complexity, 25)
    
    # 显性特征3：售后不确定性（0-25分）
    after_sales_uncertainty = 0
    if seller_type == "official":
        after_sales_uncertainty = 0
    elif seller_type == "authorized":
        after_sales_uncertainty = 5
    elif "无售后" in conditions or "无保修" in conditions:
        after_sales_uncertainty = 25
    else:
        after_sales_uncertainty = 15
    
    # 显性特征4：价格偏离度（0-25分）
    price_deviation = 0
    if price < p10:
        deviation = (p10 - price) / p10
        if deviation > 0.15:
            price_deviation = 25
        elif deviation > 0.10:
            price_deviation = 20
        elif deviation > 0.05:
            price_deviation = 10
        else:
            price_deviation = 5
    elif price > p90:
        deviation = (price - p90) / p90
        if deviation > 0.15:
            price_deviation = 15
        elif deviation > 0.10:
            price_deviation = 10
        else:
            price_deviation = 5
    
    # 综合风险评分（0-100分）
    total_risk_score = channel_risk + condition_complexity + after_sales_uncertainty + price_deviation
    
    # 确定风险等级
    if total_risk_score >= 60:
        risk_level = "高"
    elif total_risk_score >= 30:
        risk_level = "中"
    else:
        risk_level = "低"
    
    return {
        "total_risk_score": total_risk_score,
        "risk_level": risk_level,
        "features": {
            "channel_risk": channel_risk,
            "condition_complexity": condition_complexity,
            "after_sales_uncertainty": after_sales_uncertainty,
            "price_deviation": price_deviation
        }
    }


def determine_recommendation_tag(price: float, risk_level: str, distribution: Dict[str, Any],
                                conditions: str = "", seller_type: str = "") -> Tuple[str, str]:
    """
    确定推荐标签和简短理由
    
    参数:
        price: 当前价格
        risk_level: 风险等级
        distribution: 价格分布指标
        conditions: 价格条件描述
        seller_type: 卖家类型
        
    返回:
        (推荐标签, 简短理由)
    """
    p25 = distribution.get("p25", 0)
    p75 = distribution.get("p75", 0)
    
    # 判断是否主流区间
    in_mainstream = p25 <= price <= p75
    
    # 判断是否低价
    is_low_price = price < p25
    
    # 判断是否官方渠道
    is_official = seller_type == "official" or "官方自营" in conditions or "旗舰店" in conditions
    
    # 判断条件是否简单
    has_complex_condition = any(x in conditions for x in ["限", "需领券", "满减", "限时", "限量"])
    
    # 确定标签
    if risk_level == "高":
        tag = "高风险"
        reason = "价格异常或条件复杂"
    elif is_official and not has_complex_condition:
        tag = "省心"
        reason = "官方自营，售后无忧"
    elif is_low_price and risk_level in ["低", "中"]:
        tag = "性价比"
        reason = "价格低于主流区间"
    elif in_mainstream and risk_level == "低":
        tag = "性价比"
        reason = "价格合理，风险低"
    else:
        tag = "中规中矩"
        reason = "价格在主流区间"
    
    # 限制理由长度在20字以内
    if len(reason) > 20:
        reason = reason[:17] + "..."
    
    return tag, reason


def generate_l1_output(prices: List[float], platform_info: List[Dict[str, Any]], 
                      distribution: Dict[str, Any], abnormal_prices: Dict[str, Any],
                      risk_assessments: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    生成L1用户决策层输出
    
    参数:
        prices: 价格列表
        platform_info: 平台信息列表
        distribution: 价格分布指标
        abnormal_prices: 异常价格检测结果
        risk_assessments: 风险评估结果列表
        
    返回:
        L1层输出（结构化推荐和警告）
    """
    recommendations = []
    
    # 为每个平台生成推荐
    for info, risk_assessment in zip(platform_info, risk_assessments):
        platform = info.get("platform", "未知")
        price = info.get("price")
        conditions = info.get("conditions", "")
        seller_type = info.get("seller_type", "")
        
        # 跳过异常价格
        is_abnormal = price in abnormal_prices.get("strong_abnormal", []) or \
                     price in abnormal_prices.get("medium_abnormal", [])
        if is_abnormal:
            continue
        
        risk_level = risk_assessment.get("risk_level", "中")
        tag, reason = determine_recommendation_tag(price, risk_level, distribution, conditions, seller_type)
        
        recommendations.append({
            "platform": platform,
            "price": price,
            "risk_level": risk_level,
            "tag": tag,
            "reason": reason
        })
    
    # 排序：按风险等级低→高，然后按价格低→高
    risk_order = {"低": 0, "中": 1, "高": 2}
    recommendations.sort(key=lambda x: (risk_order.get(x["risk_level"], 3), x["price"]))
    
    # 限制最多3个推荐
    recommendations = recommendations[:3]
    
    # 生成警告信息
    warnings = []
    strong_abnormal = abnormal_prices.get("strong_abnormal", [])
    medium_abnormal = abnormal_prices.get("medium_abnormal", [])
    
    for price in strong_abnormal:
        # 找到对应平台
        for info in platform_info:
            if info.get("price") == price:
                warnings.append(f"异常低价：{info.get('platform', '某平台')} {price} 元")
                break
    
    for price in medium_abnormal:
        for info in platform_info:
            if info.get("price") == price:
                warnings.append(f"偏低价格：{info.get('platform', '某平台')} {price} 元")
                break
    
    return {
        "recommendations": recommendations,
        "warnings": warnings
    }


def generate_l2_output(recommendations: List[Dict[str, Any]], 
                       risk_assessments: List[Dict[str, Any]]) -> List[str]:
    """
    生成L2风险解释层输出
    
    参数:
        recommendations: 推荐列表
        risk_assessments: 风险评估结果列表
        
    返回:
        L2层输出（自然语言解释列表）
    """
    explanations = []
    
    for rec in recommendations:
        platform = rec["platform"]
        risk_level = rec["risk_level"]
        reason = rec["reason"]
        
        if risk_level == "低":
            explanation = f"推荐{platform}：{reason}。"
        elif risk_level == "中":
            explanation = f"{platform}价格较低但风险中等，需要满足特定条件。"
        else:
            explanation = f"{platform}存在较高风险，不建议优先选择。"
        
        explanations.append(explanation)
    
    return explanations


def analyze_price_distribution(prices: List[float], platform_info: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    综合分析价格分布与风险，生成三层输出
    
    参数:
        prices: 价格列表
        platform_info: 平台信息列表，每个元素包含 platform, price, conditions, seller_type 等字段
        
    返回:
        包含三层输出的完整分析结果
    """
    # 1. 计算价格分布（L3）
    distribution = calculate_price_distribution(prices)
    
    # 2. 检测异常价格（L3）
    abnormal_prices = detect_abnormal_prices(prices, distribution)
    
    # 3. 为每个平台计算风险评分（L3）
    risk_assessments = []
    for info in platform_info:
        price = info.get("price")
        conditions = info.get("conditions", "")
        seller_type = info.get("seller_type", "third-party")
        
        if price is not None:
            risk_result = calculate_explicit_risk_features(price, distribution, conditions, seller_type)
            risk_assessments.append({
                "platform": info.get("platform", "未知"),
                "price": price,
                "risk_assessment": risk_result
            })
    
    # 4. 生成L1输出（用户决策层）
    l1_output = generate_l1_output(prices, platform_info, distribution, abnormal_prices, risk_assessments)
    
    # 5. 生成L2输出（风险解释层）
    l2_output = generate_l2_output(l1_output["recommendations"], risk_assessments)
    
    # 6. 汇总L3输出（模型证据层）
    l3_output = {
        "price_distribution": distribution,
        "abnormal_prices": abnormal_prices,
        "risk_assessments": risk_assessments,
        "mainstream_range": f"{int(distribution.get('p25', 0))} - {int(distribution.get('p75', 0))}"
    }
    
    # 返回三层输出
    return {
        "l1_user_decision": l1_output,
        "l2_risk_explanation": l2_output,
        "l3_model_evidence": l3_output
    }


def main():
    """主函数"""
    # 解析输入
    input_data = parse_args()
    
    # 提取价格列表
    prices = input_data.get("price_list", [])
    if not prices:
        print("错误: price_list 不能为空")
        sys.exit(1)
    
    # 提取平台信息
    platform_info = input_data.get("platform_info", [])
    
    # 执行分析
    result = analyze_price_distribution(prices, platform_info)
    
    # 输出 JSON 结果
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()

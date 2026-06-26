#!/usr/bin/env python3
"""
智能产品推荐引擎
根据客户信息匹配最适合的保险产品
"""

import json
from pathlib import Path

def load_product_library():
    """加载产品库"""
    lib_path = Path(__file__).parent.parent / "assets" / "pingan_products.json"
    with open(lib_path, 'r', encoding='utf-8') as f:
        return json.load(f)

def match_products(customer_info: dict, risk_analysis: dict, budget: float):
    """
    根据客户信息匹配产品
    
    Args:
        customer_info: 客户基本信息
        risk_analysis: 风险分析结果
        budget: 年预算（万元）
    
    Returns:
        推荐产品列表
    """
    library = load_product_library()
    products = library["products"]
    
    age = customer_info.get("age", 35)
    health_status = customer_info.get("health_status", "健康")
    has_children = customer_info.get("has_children", False)
    is_main_breadwinner = customer_info.get("is_main_breadwinner", True)
    
    recommendations = []
    
    # 1. 医疗险推荐（优先级最高）
    medical_products = [p for p in products if p["type"] == "医疗保险"]
    
    if health_status in ["有慢病", "三高", "结节"]:
        # 推荐慢病版或普惠医疗
        for p in medical_products:
            if p["category"] in ["慢病医疗", "普惠医疗"]:
                recommendations.append({
                    **p,
                    "priority": "高",
                    "reason": "健康告知宽松，适合慢病人群投保"
                })
                break
    elif age <= 17:
        # 少儿医疗
        for p in medical_products:
            if p["category"] == "少儿医疗":
                recommendations.append({
                    **p,
                    "priority": "高",
                    "reason": "0免赔设计，适合儿童高频就医需求"
                })
                break
    elif age >= 50:
        # 中老年推荐防癌医疗
        for p in medical_products:
            if p["category"] == "防癌医疗":
                recommendations.append({
                    **p,
                    "priority": "中",
                    "reason": "健告宽松，专注癌症保障"
                })
                break
    else:
        # 成人推荐百万医疗或长期医疗
        for p in medical_products:
            if p["category"] == "长期医疗":
                recommendations.append({
                    **p,
                    "priority": "高",
                    "reason": "保证续保20年，锁定长期保障"
                })
                break
        
        # 预算充足推荐中端医疗
        if budget >= 1.5:
            for p in medical_products:
                if p["category"] == "中端医疗":
                    recommendations.append({
                        **p,
                        "priority": "中",
                        "reason": "0免赔+特需部，就医体验更好"
                    })
                    break
    
    # 2. 重疾险推荐
    if age <= 50:  # 50岁以上重疾保费太贵，性价比低
        critical_products = [p for p in products if p["type"] == "重疾保险"]
        
        if age <= 17:
            for p in critical_products:
                if p["category"] == "少儿重疾":
                    recommendations.append({
                        **p,
                        "priority": "高",
                        "reason": "少儿特疾额外赔付，保费便宜"
                    })
                    break
        else:
            for p in critical_products:
                if p["category"] == "成人重疾":
                    recommendations.append({
                        **p,
                        "priority": "高",
                        "reason": "覆盖收入损失风险，建议保额为年收入3-5倍"
                    })
                    break
    
    # 3. 意外险推荐（人人必备）
    accident_products = [p for p in products if p["type"] == "意外保险"]
    
    if age <= 17:
        for p in accident_products:
            if p["category"] == "少儿意外":
                recommendations.append({
                    **p,
                    "priority": "高",
                    "reason": "低保费高杠杆，儿童活泼好动必备"
                })
                break
    elif age >= 50:
        for p in accident_products:
            if p["category"] == "老年意外":
                recommendations.append({
                    **p,
                    "priority": "高",
                    "reason": "含骨折保障，老年人摔倒风险高"
                })
                break
    else:
        for p in accident_products:
            if p["category"] == "成人意外":
                recommendations.append({
                    **p,
                    "priority": "高",
                    "reason": "百万保额+猝死保障，性价比极高"
                })
                break
    
    # 按优先级排序
    priority_order = {"高": 0, "中": 1, "低": 2}
    recommendations.sort(key=lambda x: priority_order.get(x["priority"], 3))
    
    return recommendations

def calculate_budget_allocation(recommendations: list, total_budget: float):
    """
    计算预算分配
    
    Args:
        recommendations: 推荐产品列表
        total_budget: 总预算（万元）
    
    Returns:
        带预算分配的产品列表
    """
    total_budget_yuan = total_budget * 10000
    
    # 预算分配比例建议
    allocation_rules = {
        "重疾保险": 0.50,
        "医疗保险": 0.20,
        "意外保险": 0.10,
    }
    
    result = []
    for product in recommendations:
        product_type = product["type"]
        suggested_ratio = allocation_rules.get(product_type, 0.20)
        suggested_budget = total_budget_yuan * suggested_ratio
        
        result.append({
            **product,
            "suggested_budget": f"约{suggested_budget:.0f}元/年"
        })
    
    return result

if __name__ == '__main__':
    # 测试
    customer = {
        "age": 35,
        "health_status": "健康",
        "has_children": True,
        "is_main_breadwinner": True
    }
    risk = {"disease_risk": "中等"}
    budget = 2.0
    
    matches = match_products(customer, risk, budget)
    final = calculate_budget_allocation(matches, budget)
    
    print(json.dumps(final, ensure_ascii=False, indent=2))

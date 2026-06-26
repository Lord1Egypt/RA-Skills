#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
新股分析模块
提供新股基本面分析、行业对比等功能
"""

# 模拟新股数据
MOCK_IPO_DATA = {
    "601127": {
        "code": "601127",
        "name": "赛力斯",
        "price": 15.80,
        "pe": 25.3,
        "industry_pe": 30.5,
        "industry": "汽车制造",
        "revenue": 120.5,
        "revenue_growth": 35.2,
        "net_profit": 8.5,
        "profit_growth": 28.6,
        "gross_margin": 18.5,
        "industry_margin": 15.2,
        "issue_size": 15.8,  # 亿元
        "raised_funds": 25.0,  # 拟募集资金
        "board": "沪市主板",
    },
    "301234": {
        "code": "301234",
        "name": "科技先锋",
        "price": 28.50,
        "pe": 35.2,
        "industry_pe": 40.0,
        "industry": "电子设备",
        "revenue": 45.8,
        "revenue_growth": 52.3,
        "net_profit": 6.2,
        "profit_growth": 48.5,
        "gross_margin": 32.5,
        "industry_margin": 28.0,
        "issue_size": 10.7,
        "raised_funds": 15.0,
        "board": "创业板",
    },
    "688567": {
        "code": "688567",
        "name": "创新生物",
        "price": 42.00,
        "pe": 45.0,
        "industry_pe": 50.0,
        "industry": "生物医药",
        "revenue": 18.5,
        "revenue_growth": 68.5,
        "net_profit": 3.2,
        "profit_growth": 72.3,
        "gross_margin": 75.2,
        "industry_margin": 70.0,
        "issue_size": 10.5,
        "raised_funds": 20.0,
        "board": "科创板",
    },
    "001234": {
        "code": "001234",
        "name": "消费龙头",
        "price": 18.60,
        "pe": 22.0,
        "industry_pe": 25.0,
        "industry": "食品饮料",
        "revenue": 85.2,
        "revenue_growth": 18.5,
        "net_profit": 12.8,
        "profit_growth": 15.2,
        "gross_margin": 42.5,
        "industry_margin": 38.0,
        "issue_size": 16.7,
        "raised_funds": 20.0,
        "board": "深市主板",
    },
}


def analyze_ipo(stock_code):
    """
    分析新股
    
    Args:
        stock_code: 股票代码
        
    Returns:
        dict: 分析结果
    """
    if stock_code not in MOCK_IPO_DATA:
        return get_default_analysis(stock_code)
    
    ipo = MOCK_IPO_DATA[stock_code]
    
    # 计算估值优势
    pe_ratio = ipo['pe'] / ipo['industry_pe']
    margin_diff = ipo['gross_margin'] - ipo['industry_margin']
    
    # 综合评分
    score = 0
    
    # 估值评分 (0-40 分)
    if pe_ratio < 0.7:
        score += 40
    elif pe_ratio < 0.8:
        score += 35
    elif pe_ratio < 0.9:
        score += 30
    elif pe_ratio < 1.0:
        score += 20
    else:
        score += 10
    
    # 成长性评分 (0-30 分)
    if ipo['revenue_growth'] > 50:
        score += 30
    elif ipo['revenue_growth'] > 30:
        score += 25
    elif ipo['revenue_growth'] > 20:
        score += 20
    elif ipo['revenue_growth'] > 10:
        score += 15
    else:
        score += 10
    
    # 盈利能力评分 (0-30 分)
    if margin_diff > 10:
        score += 30
    elif margin_diff > 5:
        score += 25
    elif margin_diff > 0:
        score += 20
    else:
        score += 10
    
    # 生成建议
    if score >= 80:
        recommendation = "⭐⭐⭐ 积极申购（估值低 + 成长好 + 盈利强）"
    elif score >= 65:
        recommendation = "⭐⭐ 建议申购（资质良好）"
    elif score >= 50:
        recommendation = "⭐ 谨慎申购（估值偏高）"
    else:
        recommendation = "⚠️ 不建议申购（风险较高）"
    
    return {
        'code': ipo['code'],
        'name': ipo['name'],
        'price': ipo['price'],
        'pe': ipo['pe'],
        'industry_pe': ipo['industry_pe'],
        'industry': ipo['industry'],
        'revenue': ipo['revenue'],
        'revenue_growth': ipo['revenue_growth'],
        'net_profit': ipo['net_profit'],
        'profit_growth': ipo['profit_growth'],
        'gross_margin': ipo['gross_margin'],
        'industry_margin': ipo['industry_margin'],
        'recommendation': recommendation,
        'score': score,
    }


def get_default_analysis(stock_code):
    """返回默认分析结果（用于未知股票）"""
    return {
        'code': stock_code,
        'name': '未知新股',
        'price': 0,
        'pe': 0,
        'industry_pe': 0,
        'industry': '未知',
        'revenue': 0,
        'revenue_growth': 0,
        'net_profit': 0,
        'profit_growth': 0,
        'gross_margin': 0,
        'industry_margin': 0,
        'recommendation': '⚠️ 数据不足，请查询招股说明书',
        'score': 0,
    }


def compare_industry(stock_code):
    """
    行业对比分析
    
    Args:
        stock_code: 股票代码
        
    Returns:
        dict: 对比结果
    """
    if stock_code not in MOCK_IPO_DATA:
        return None
    
    ipo = MOCK_IPO_DATA[stock_code]
    
    return {
        'industry': ipo['industry'],
        'stock_pe': ipo['pe'],
        'industry_avg_pe': ipo['industry_pe'],
        'pe_diff': ipo['pe'] - ipo['industry_pe'],
        'stock_margin': ipo['gross_margin'],
        'industry_avg_margin': ipo['industry_margin'],
        'margin_diff': ipo['gross_margin'] - ipo['industry_margin'],
        'conclusion': f"PE{'低于' if ipo['pe'] < ipo['industry_pe'] else '高于'}行业平均{abs(ipo['pe'] - ipo['industry_pe']):.1f}倍",
    }


if __name__ == "__main__":
    # 测试
    print("赛力斯分析:")
    result = analyze_ipo("601127")
    print(f"  发行价：{result['price']}元")
    print(f"  市盈率：{result['pe']}倍 vs 行业{result['industry_pe']}倍")
    print(f"  营收增长：{result['revenue_growth']}%")
    print(f"  建议：{result['recommendation']}")
    print(f"  综合评分：{result['score']}")

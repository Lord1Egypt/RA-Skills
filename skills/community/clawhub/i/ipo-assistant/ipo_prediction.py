#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
新股预测模块
中签率预测、上市溢价预测
"""

# 模拟数据
MOCK_IPO_DATA = {
    "601127": {
        "name": "赛力斯",
        "issue_size": 15.8,  # 发行规模（亿元）
        "industry": "汽车制造",
        "price": 15.80,
        "pe": 25.3,
    },
    "301234": {
        "name": "科技先锋",
        "issue_size": 10.7,
        "industry": "电子设备",
        "price": 28.50,
        "pe": 35.2,
    },
    "688567": {
        "name": "创新生物",
        "issue_size": 10.5,
        "industry": "生物医药",
        "price": 42.00,
        "pe": 45.0,
    },
    "001234": {
        "name": "消费龙头",
        "issue_size": 16.7,
        "industry": "食品饮料",
        "price": 18.60,
        "pe": 22.0,
    },
}

# 行业中签率历史数据
INDUSTRY_WIN_RATE = {
    "汽车制造": 0.035,
    "电子设备": 0.028,
    "生物医药": 0.025,
    "食品饮料": 0.040,
    "机械设备": 0.032,
    "化工": 0.038,
}

# 行业上市溢价历史数据
INDUSTRY_PREMIUM = {
    "汽车制造": 35,
    "电子设备": 55,
    "生物医药": 70,
    "食品饮料": 45,
    "机械设备": 40,
    "化工": 30,
}

# 近期市场平均
RECENT_AVG_WIN_RATE = 0.032  # 近期平均中签率
RECENT_AVG_PREMIUM = 45  # 近期新股平均涨幅


def predict_win_rate(stock_code):
    """
    预测中签率
    
    Args:
        stock_code: 股票代码
        
    Returns:
        dict: 预测结果
    """
    if stock_code not in MOCK_IPO_DATA:
        return get_default_win_rate(stock_code)
    
    ipo = MOCK_IPO_DATA[stock_code]
    industry = ipo['industry']
    issue_size = ipo['issue_size']
    
    # 1. 行业中签率
    industry_rate = INDUSTRY_WIN_RATE.get(industry, 0.032) * 100
    
    # 2. 规模调整（规模越小，中签率越低）
    if issue_size < 10:
        size_adjust = -0.005
    elif issue_size < 20:
        size_adjust = 0
    else:
        size_adjust = 0.005
    
    # 3. 市场热度调整
    market_adjust = 0  # 简化处理
    
    # 综合计算
    predicted = industry_rate + size_adjust * 100 + market_adjust * 100
    predicted = max(0.01, min(0.1, predicted))  # 限制在 0.01%-0.1%
    
    # 预计冻结资金
    frozen_funds = issue_size * 50  # 简化估算
    
    # 行业热度
    industry_hot = "高" if industry in ["电子设备", "生物医药"] else "中" if industry in ["汽车制造", "食品饮料"] else "低"
    
    # 市场环境
    market_condition = "正常"
    
    return {
        'code': stock_code,
        'name': ipo['name'],
        'predicted_rate': round(predicted, 3),
        'history_avg': round(RECENT_AVG_WIN_RATE * 100, 3),
        'frozen_funds': round(frozen_funds, 1),
        'issue_size': issue_size,
        'industry_hot': industry_hot,
        'market_condition': market_condition,
    }


def get_default_win_rate(stock_code):
    """返回默认中签率预测"""
    return {
        'code': stock_code,
        'name': '未知新股',
        'predicted_rate': round(RECENT_AVG_WIN_RATE * 100, 3),
        'history_avg': round(RECENT_AVG_WIN_RATE * 100, 3),
        'frozen_funds': 0,
        'issue_size': 0,
        'industry_hot': '未知',
        'market_condition': '未知',
    }


def predict_premium(stock_code):
    """
    预测上市溢价率
    
    Args:
        stock_code: 股票代码
        
    Returns:
        dict: 预测结果
    """
    if stock_code not in MOCK_IPO_DATA:
        return get_default_premium(stock_code)
    
    ipo = MOCK_IPO_DATA[stock_code]
    industry = ipo['industry']
    pe = ipo['pe']
    
    # 1. 行业平均溢价
    industry_avg = INDUSTRY_PREMIUM.get(industry, 40)
    
    # 2. 近期市场平均
    recent_avg = RECENT_AVG_PREMIUM
    
    # 3. 估值调整（PE 越低，溢价越高）
    industry_pe_avg = {
        "汽车制造": 30,
        "电子设备": 40,
        "生物医药": 50,
        "食品饮料": 25,
    }.get(industry, 35)
    
    if pe < industry_pe_avg * 0.8:
        pe_adjust = 10
    elif pe < industry_pe_avg:
        pe_adjust = 5
    elif pe < industry_pe_avg * 1.2:
        pe_adjust = 0
    else:
        pe_adjust = -10
    
    # 4. 规模调整（规模越小，溢价越高）
    if ipo['issue_size'] < 10:
        size_adjust = 10
    elif ipo['issue_size'] < 20:
        size_adjust = 5
    else:
        size_adjust = 0
    
    # 综合计算
    base_premium = (industry_avg + recent_avg) / 2
    predicted = base_premium + pe_adjust + size_adjust
    
    # 限制范围
    predicted = max(10, min(150, predicted))
    
    # 预测区间
    lower = max(5, predicted - 15)
    upper = min(200, predicted + 15)
    
    # 预测价格
    predicted_price = ipo['price'] * (1 + predicted / 100)
    
    # 置信度
    confidence = "高" if abs(predicted - industry_avg) < 10 else "中"
    
    # 估值水平
    if pe < industry_pe_avg * 0.8:
        valuation = "低估"
    elif pe < industry_pe_avg * 1.2:
        valuation = "合理"
    else:
        valuation = "高估"
    
    return {
        'code': stock_code,
        'name': ipo['name'],
        'predicted_premium': round(predicted, 1),
        'premium_range': [round(lower, 1), round(upper, 1)],
        'predicted_price': round(predicted_price, 2),
        'confidence': confidence,
        'industry_avg': industry_avg,
        'recent_avg': recent_avg,
        'valuation_level': valuation,
    }


def get_default_premium(stock_code):
    """返回默认溢价预测"""
    return {
        'code': stock_code,
        'name': '未知新股',
        'predicted_premium': 45,
        'premium_range': [30, 60],
        'predicted_price': 0,
        'confidence': '低',
        'industry_avg': 40,
        'recent_avg': RECENT_AVG_PREMIUM,
        'valuation_level': '未知',
    }


if __name__ == "__main__":
    # 测试
    print("赛力斯中签率预测:")
    result = predict_win_rate("601127")
    print(f"  预测中签率：{result['predicted_rate']}%")
    print(f"  历史平均：{result['history_avg']}%")
    print(f"  预计冻结资金：{result['frozen_funds']}亿元")
    
    print("\n赛力斯上市溢价预测:")
    result = predict_premium("601127")
    print(f"  预测涨幅：{result['predicted_premium']}%")
    print(f"  合理区间：{result['premium_range'][0]}% - {result['premium_range'][1]}%")
    print(f"  预测价格：{result['predicted_price']}元")
    print(f"  置信度：{result['confidence']}")

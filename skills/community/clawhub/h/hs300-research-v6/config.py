#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
沪深300晨间多因子投研系统 - 配置文件
"""

import os
from datetime import datetime

# 项目基础路径
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# 数据目录
DATA_DIR = os.path.join(BASE_DIR, 'data')
LOG_DIR = os.path.join(BASE_DIR, 'logs')
OUTPUT_DIR = os.path.join(BASE_DIR, 'output')
MODEL_DIR = os.path.join(BASE_DIR, 'models')

# 沪深300指数代码
HS300_INDEX = 'sh000300'

# 交易日设置 (北京时间早上8点生成报告)
REPORT_TIME = '08:00'

# 因子配置
FACTOR_CONFIG = {
    # 估值因子
    'valuation': ['pe', 'pb', 'pe_ttm', 'ps', 'pcf'],
    # 成长因子
    'growth': ['revenue_growth', 'profit_growth', 'roe_growth'],
    # 质量因子
    'quality': ['roe', 'roa', 'profit_margin', 'asset_turnover'],
    # 动量因子
    'momentum': ['return_1m', 'return_3m', 'return_6m', 'return_12m'],
    # 波动率因子
    'volatility': ['std_1m', 'std_3m', 'max_drawdown_1m'],
    # 技术因子
    'technical': ['macd', 'rsi', 'kdj', 'ma5', 'ma10', 'ma20', 'ma60', 'volume_ratio']
}

# 因子权重配置
FACTOR_WEIGHTS = {
    'valuation': 0.25,
    'growth': 0.20,
    'quality': 0.20,
    'momentum': 0.15,
    'volatility': 0.10,
    'technical': 0.10
}

# 股票池配置
STOCK_POOL = {
    'hs300': True,        # 是否使用沪深300成分股
    'min_market_cap': 100,  # 最小市值（亿）
    'exclude_st': True,    # 是否排除ST股票
    'exclude_suspend': True  # 是否排除停牌股票
}

# 技术分析参数
TECH_PARAMS = {
    'ma_periods': [5, 10, 20, 60, 120],
    'macd_fast': 12,
    'macd_slow': 26,
    'macd_signal': 9,
    'rsi_period': 14,
    'kdj_n': 9,
    'kdj_m1': 3,
    'kdj_m2': 3
}

# 报告输出配置
REPORT_CONFIG = {
    'top_n': 20,          # 推荐股票数量
    'bottom_n': 10,       # 规避股票数量
    'format': 'markdown',  # 输出格式: markdown, html, excel
    'send_email': False,   # 是否发送邮件
    'chart_type': 'png'    # 图表格式
}

# 日志配置
LOG_CONFIG = {
    'level': 'INFO',
    'format': '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    'file': os.path.join(LOG_DIR, f'research_system_{datetime.now().strftime("%Y%m%d")}.log')
}

# 数据缓存配置
CACHE_CONFIG = {
    'enable': True,
    'expire_hours': 24,  # 缓存过期时间（小时）
    'path': os.path.join(DATA_DIR, 'cache')
}

# 风险提示
RISK_DISCLAIMER = """
【风险提示】
本报告仅供参考，不构成投资建议。股市有风险，投资需谨慎。
基于历史数据的分析不代表未来表现，请结合自身风险承受能力做出投资决策。
"""

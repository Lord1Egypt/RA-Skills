#!/usr/bin/env python3
"""
韭研公社异动页面分析脚本
提取并结构化市场异动数据
"""

import re
import json
from datetime import datetime
from pathlib import Path

def parse_stock_entry(text):
    """解析单个股票条目"""
    patterns = {
        'name': r'([A-Z 一 - 龥]+)\s*\((\d{6})\)',
        'code': r'\((\d{6})\)',
        'price': r'最新价 [:：]?\s*([\d.]+)',
        'change': r'涨跌幅 [:：]?\s*([+\-]?[\d.]+)%',
        'limit_time': r'涨停时间 [:：]?\s*(\d{2}:\d{2})',
        'board_count': r'(\d) 天 (\d) 板',
        'analysis': r'解析 [:：]?\s*(.+?)(?=\n\n|\n[a-zA-Z]|\Z)',
    }
    
    result = {}
    for key, pattern in patterns.items():
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            result[key] = match.group(1) if len(match.groups()) == 1 else match.groups()
    
    return result

def parse_sector_block(text):
    """解析板块区块"""
    sector_pattern = r'([智能电网 | 算力 | 低空经济 | 公告 | 新能源 | 芯片 | 人工智能 | 一 - 龥]{2,10}板块 | 概念)'
    stocks = re.findall(r'([A-Z 一 - 龥]+)\s*\((\d{6})\).*?([\d.]+)%', text)
    
    return {
        'sector_name': re.search(sector_pattern, text),
        'stocks': stocks
    }

def analyze_market_content(content):
    """分析完整页面内容"""
    result = {
        'date': datetime.now().strftime('%Y-%m-%d'),
        'sectors': [],
        'hot_stocks': [],
        'risks': [],
        'opportunities': []
    }
    
    # 提取日期
    date_match = re.search(r'(\d{4}[-/]\d{1,2}[-/]\d{1,2})', content)
    if date_match:
        result['date'] = date_match.group(1).replace('/', '-')
    
    # 提取涨停股票
    limit_up = re.findall(r'([A-Z 一 - 龥]+)\s*\((\d{6})\).*?(\d 天\d板)', content)
    result['hot_stocks'] = [
        {'name': s[0], 'code': s[1], 'board': s[2]} 
        for s in limit_up
    ]
    
    # 提取风险提示
    risk_keywords = ['风险', 'ST', '退市', '警示', '下跌', '跌停']
    for keyword in risk_keywords:
        matches = re.findall(r'.{0,50}' + keyword + '.{0,100}', content)
        result['risks'].extend(matches[:3])
    
    # 提取板块信息
    sector_keywords = ['板块', '概念', '行业', '题材']
    for keyword in sector_keywords:
        matches = re.findall(r'([A-Z 一 - 龥]{2,8})' + keyword, content)
        result['sectors'].extend(matches)
    
    # 去重
    result['sectors'] = list(set(result['sectors']))[:10]
    result['risks'] = list(set(result['risks']))[:5]
    
    return result

def generate_report(data):
    """生成结构化报告"""
    report = f"""## 📊 市场异动简报
**日期**: {data['date']}
**数据来源**: 韭研公社异动板块

### 🌡️ 市场环境
今日监测到 {len(data['sectors'])} 个异动板块，{len(data['hot_stocks'])} 只涨停股。

### 📈 热门板块
"""
    
    for sector in data['sectors'][:5]:
        report += f"- {sector}\n"
    
    report += "\n### 🐲 连板龙头\n"
    for stock in data['hot_stocks'][:5]:
        report += f"- **{stock['name']}** ({stock['code']}) - {stock['board']}\n"
    
    if data['risks']:
        report += "\n### ⚠️ 风险提示\n"
        for risk in data['risks'][:3]:
            report += f"- {risk}\n"
    
    return report

if __name__ == '__main__':
    import sys
    if len(sys.argv) > 1:
        content = sys.argv[1]
        data = analyze_market_content(content)
        print(generate_report(data))
    else:
        print("用法：python analyze.py <页面内容>")

#!/usr/bin/env python3
"""
财报关键指标提取脚本 — 从财报文本中提取标准化财务指标。
用法：Agent 先用 web_fetch 获取财报内容，再调用此脚本解析。
"""

import re
import json
from typing import Optional

# 财务指标正则模式（支持中英文财报）
PATTERNS = {
    "revenue": [
        r"营业收入[：:]\s*([\d,\.]+)\s*(亿|百万|万)?",
        r"Total Revenue[:\s]+([\$¥]?[\d,\.]+)\s*(billion|million|B|M)?",
    ],
    "net_income": [
        r"净利润[：:]\s*([\d,\.]+)\s*(亿|百万|万)?",
        r"Net Income[:\s]+([\$¥]?[\d,\.]+)\s*(billion|million|B|M)?",
    ],
    "gross_margin": [
        r"毛利率[：:]\s*([\d\.]+)%",
        r"Gross Margin[:\s]+([\d\.]+)%",
    ],
    "yoy_growth": [
        r"同比增长[：:]\s*([\d\.]+)%",
        r"YoY Growth[:\s]+([\d\.]+)%",
    ],
}

def extract_metrics(text: str, company: str, year: int) -> dict:
    """
    从财报文本中提取关键指标
    
    Args:
        text: 财报原文
        company: 公司名称
        year: 财报年份
    
    Returns:
        提取的财务指标 dict
    """
    result = {
        "company": company,
        "year": year,
        "metrics": {}
    }
    
    for metric, patterns in PATTERNS.items():
        for pattern in patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                result["metrics"][metric] = match.group(1)
                break
        else:
            result["metrics"][metric] = None
    
    return result


def format_report(metrics: dict) -> str:
    """格式化输出财务摘要"""
    lines = [
        f"## {metrics['company']} {metrics['year']} 财务摘要",
        "",
        "| 指标 | 数值 |",
        "|------|------|",
    ]
    
    label_map = {
        "revenue": "营业收入",
        "net_income": "净利润",
        "gross_margin": "毛利率",
        "yoy_growth": "同比增长",
    }
    
    for key, value in metrics["metrics"].items():
        label = label_map.get(key, key)
        display = value if value else "未找到"
        lines.append(f"| {label} | {display} |")
    
    return "\n".join(lines)


if __name__ == "__main__":
    # 示例
    sample_text = "营业收入：1,234亿元，同比增长15.3%，净利润：234亿元，毛利率：42.1%"
    metrics = extract_metrics(sample_text, "示例公司", 2023)
    print(format_report(metrics))

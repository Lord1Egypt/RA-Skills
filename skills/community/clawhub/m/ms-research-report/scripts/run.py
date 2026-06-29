#!/usr/bin/env python3
"""Morgan Stanley Research Report -- CLI entry point.

Usage:
    python scripts/run.py -o output/report.docx
    python scripts/run.py -o output/report.docx -d data.json
"""
import sys
import os
import json
import argparse

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from ms_research_report import make_report


def main():
    parser = argparse.ArgumentParser(
        description="Morgan Stanley Style Research Report Generator (DOCX)")
    parser.add_argument("-o", "--output", default=None,
                        help="Output .docx path (default: output/ms_report.docx)")
    parser.add_argument("-d", "--data", default=None,
                        help="Path to JSON data file (default: built-in sample)")
    parser.add_argument("-t", "--theme", default="classic",
                        help="Theme name (default: classic)")
    parser.add_argument("-l", "--language", default="zh",
                        help="Language: zh / en / bilingual (default: zh)")
    args = parser.parse_args()

    # Determine output path
    script_dir = os.path.dirname(os.path.abspath(__file__))
    skill_dir = os.path.dirname(script_dir)
    output_path = args.output or os.path.join(skill_dir, "output", "ms_report.docx")

    # Ensure output directory exists
    os.makedirs(os.path.dirname(os.path.abspath(output_path)), exist_ok=True)

    # Load data
    if args.data:
        with open(args.data, "r", encoding="utf-8") as f:
            data = json.load(f)
    else:
        # Built-in sample data
        data = {
            "company_name": "极光资本控股",
            "title_cn": "为下一个10倍科技周期，资本是瓶颈吗？",
            "title_en": "Financing the Next 10x Tech Cycle",
            "subtitle": "关键论点一句话：算力军备竞赛将重塑上游资本开支结构。",
            "rating": "Overweight",
            "target_price": 125.0,
            "current_price": 98.5,
            "date_str": "2026-06-12",
            "analyst": "陈嘉怡 CFA",
            "research_type": "Foundation",
            "currency": "USD",
            "key_takeaways": [
                "算力需求在未来三年预计以 35% CAGR 扩张，资本开支将成为瓶颈。",
                "上游芯片与光模块厂商最受益，利润池份额有望翻倍。",
                "估值溢价将集中于具备专有硅片与供应渠道的企业。",
                "地缘与出口管制风险可能压缩远期回报曲线。",
            ],
            "executive_summary": {
                "thesis": [
                    "算力军备竞赛重塑上游资本开支结构，半导体链条议价能力持续上升。",
                    "预计 2026-2028 年全球数据中心资本开支总额突破 5000 亿美元。",
                    "芯片与光模块份额从 38% 提升至 52%，利润池有望翻倍。",
                ],
                "tp_and_upside": [
                    "目标价 $125.0（当前 $98.5），上行空间约 +27%。",
                    "评级：Overweight（超配），估值锚定 26E P/E 22x。",
                ],
                "risks": [
                    "出口管制与地缘冲突加剧导致订单延迟与估值压缩。",
                    "客户集中度偏高，单一大型云厂商预算调整将显著影响收入。",
                    "产能瓶颈可能导致毛利率在 2H26 出现阶段性回落。",
                ],
                "catalysts": [
                    "下一代 AI 加速器量产时间表公布。",
                    "大型云厂商资本开支指引上调。",
                    "自研硅片客户的订单结构优化。",
                ],
            },
            "financial_chart": {
                "labels": ["FY24", "FY25E", "FY26E", "FY27E"],
                "revenue": [4810, 5230, 5750, 6520],
                "ebitda": [1210, 1405, 1580, 1820],
                "gross_margin": [52.1, 54.0, 55.5, 56.8],
                "ebitda_margin": [25.2, 26.9, 27.5, 27.9],
                "net_margin": [18.5, 19.8, 21.0, 22.1],
            },
            "sectors_allocation": {
                "title": "行业配置 / Sector Allocation",
                "labels": ["半导体", "光模块", "电源/散热", "IDC", "软件应用", "其他"],
                "values": [40.0, 25.0, 12.0, 10.0, 8.0, 5.0],
            },
            "sections": [
                {
                    "title_cn": "一、算力需求：结构性扩张",
                    "title_en": "I. Compute Demand -- Structural Expansion",
                    "paragraphs": [
                        "全球云厂商与大型科技公司的训练集群在 2024-2025 年经历了一轮快速扩充，"
                        "推理侧需求接棒成为新的增长引擎。",
                        "我们估计单位推理成本将在未来两年以每年 30% 的速度下降，"
                        "推动应用层渗透率显著提升。",
                    ],
                },
                {
                    "title_cn": "二、资本开支结构重塑",
                    "title_en": "II. Capex Structure Reshaping",
                    "paragraphs": [
                        "我们预期 2026 年起，数据中心电源、光互联与散热配套将成为新的投资热点。",
                    ],
                },
            ],
            "metrics": [
                {"value": "$5.2T", "unit": "TAM 2026E", "label": "市场规模"},
                {"value": "35%", "unit": "CAGR '24-'28", "label": "复合增长"},
                {"value": "+27%", "unit": "Upside", "label": "目标价上涨空间"},
            ],
            "financial_table": {
                "headers": ["指标", "FY24", "FY25E", "FY26E", "FY27E"],
                "rows": [
                    ["营业收入 ($M)", "4,810", "5,230", "5,750", "6,520"],
                    ["毛利率 (%)", "52.1", "54.0", "55.5", "56.8"],
                    ["EBITDA ($M)", "1,210", "1,405", "1,580", "1,820"],
                    ["EBITDA 利润率 (%)", "25.2", "26.9", "27.5", "27.9"],
                    ["CAPEX ($M)", "-620", "-780", "-910", "-1,050"],
                    ["调整后 EPS ($)", "2.12", "2.48", "2.91", "3.38"],
                ],
                "highlight_rows": [5],
                "auto_yoy": True,
                "source": "Source: Morgan Stanley Research.",
            },
            "rating_table": [
                ["Ticker", "Rating", "Last Close", "Company", "Reason"],
                ["NVDA.O", "OW", "198.35", "Nvidia", "AI compute leader"],
                ["AVGO.O", "OW", "82.10", "Broadcom", "Custom ASIC leverage"],
                ["AMD.O", "EW", "162.40", "AMD", "Balanced mix"],
                ["INTC.O", "UW", "31.15", "Intel", "Foundry drag"],
            ],
            "shovel_stocks": [
                {"rank": 1, "company": "Nvidia", "ticker": "NVDA",
                 "product": "H200 / B200 GPU", "analyst": "E. Lee",
                 "market_cap_mn": 2400000.0, "perf_1y_pct": 112.3},
                {"rank": 2, "company": "Broadcom", "ticker": "AVGO",
                 "product": "Custom AI ASIC", "analyst": "K. Wu",
                 "market_cap_mn": 680000.0, "perf_1y_pct": 72.5},
                {"rank": 3, "company": "Marvell", "ticker": "MRVL",
                 "product": "Data Center PHY", "analyst": "J. Zhang",
                 "market_cap_mn": 85000.0, "perf_1y_pct": 23.1},
            ],
        }

    result = make_report(data, output_path, theme=args.theme, language=args.language)
    print(f"Report generated: {result}")


if __name__ == "__main__":
    main()

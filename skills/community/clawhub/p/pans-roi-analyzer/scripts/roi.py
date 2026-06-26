#!/usr/bin/env python3
"""
ROI Analyzer - AI算力销售ROI分析器
对比当前方案与新方案的成本和性能，计算ROI、TCO和回收期
"""

import argparse
import json
import csv
import sys
from datetime import datetime
from typing import Optional


def calculate_roi(args) -> dict:
    """计算ROI相关指标"""
    # 成本计算
    current_monthly_cost = args.current_cost
    new_monthly_cost = args.new_cost
    
    # 月节省
    monthly_savings = current_monthly_cost - new_monthly_cost
    cost_savings_pct = (monthly_savings / current_monthly_cost * 100) if current_monthly_cost > 0 else 0
    
    # 吞吐量
    current_throughput = args.throughput_current
    new_throughput = args.throughput_new
    throughput_improvement = ((new_throughput / current_throughput - 1) * 100) if current_throughput > 0 else 0
    
    # 收入计算 (每千token收入 * 吞吐量 * 时间)
    revenue_per_1k_tokens = args.revenue_per_token
    # 每月 token 数 = 吞吐量 * 60秒 * 60分钟 * 24小时 * 30天
    tokens_per_month = new_throughput * 60 * 60 * 24 * 30
    monthly_revenue_new = (tokens_per_month / 1000) * revenue_per_1k_tokens
    
    tokens_per_month_current = current_throughput * 60 * 60 * 24 * 30
    monthly_revenue_current = (tokens_per_month_current / 1000) * revenue_per_1k_tokens
    
    # 收入增长
    monthly_revenue_growth = monthly_revenue_new - monthly_revenue_current
    
    # ROI 计算
    # ROI = (收入增长 - 成本差) / 成本差 × 100%
    if monthly_savings < 0:
        # 新方案成本更高
        additional_investment = abs(monthly_savings)
        roi_pct = ((monthly_revenue_growth - additional_investment) / additional_investment * 100) if additional_investment > 0 else 0
    else:
        # 新方案成本更低
        additional_investment = 0
        roi_pct = (monthly_revenue_growth / monthly_savings * 100) if monthly_savings > 0 else 0
    
    # 回收期 (额外投入 / 月节省)
    if monthly_savings > 0:
        payback_months = 0
    else:
        # 需要额外投入的情况下，计算回收期
        payback_months = abs(monthly_savings) / monthly_revenue_growth if monthly_revenue_growth > 0 else float('inf')
    
    # 3年TCO
    period = args.period
    current_tco = current_monthly_cost * period
    new_tco = new_monthly_cost * period
    tco_savings = current_tco - new_tco
    
    return {
        "current": {
            "gpu": args.current_gpu,
            "count": args.current_count,
            "monthly_cost": current_monthly_cost,
            "throughput": current_throughput,
            "monthly_revenue": monthly_revenue_current
        },
        "new": {
            "gpu": args.new_gpu,
            "count": args.new_count,
            "monthly_cost": new_monthly_cost,
            "throughput": new_throughput,
            "monthly_revenue": monthly_revenue_new
        },
        "analysis": {
            "monthly_savings": monthly_savings,
            "cost_savings_pct": round(cost_savings_pct, 2),
            "throughput_improvement_pct": round(throughput_improvement, 2),
            "monthly_revenue_growth": monthly_revenue_growth,
            "roi_pct": round(roi_pct, 2),
            "payback_months": round(payback_months, 1) if payback_months != float('inf') else "N/A",
            "period_months": period,
            "current_tco": current_tco,
            "new_tco": new_tco,
            "tco_savings": tco_savings
        }
    }


def format_output(result: dict) -> str:
    """格式化输出"""
    current = result["current"]
    new = result["new"]
    analysis = result["analysis"]
    
    lines = []
    lines.append("\n" + "="*60)
    lines.append("📊 AI算力 ROI 分析报告")
    lines.append("="*60)
    
    # 配置对比
    lines.append("\n💰 成本对比表")
    lines.append("-"*40)
    lines.append(f"{'指标':<20} {'当前方案':<15} {'新方案':<15}")
    lines.append("-"*40)
    lines.append(f"{'GPU型号':<20} {current['gpu']:<15} {new['gpu']:<15}")
    lines.append(f"{'GPU数量':<20} {current['count']:<15} {new['count']:<15}")
    lines.append(f"{'月成本($)':<20} {current['monthly_cost']:<15} {new['monthly_cost']:<15}")
    lines.append(f"{'吞吐量(tokens/s)':<20} {current['throughput']:<15} {new['throughput']:<15}")
    lines.append(f"{'月收入($)':<20} {current['monthly_revenue']:<15.2f} {new['monthly_revenue']:<15.2f}")
    
    # ROI分析
    lines.append("\n📈 ROI 分析摘要")
    lines.append("-"*40)
    lines.append(f"成本节省: ${analysis['monthly_savings']:.2f}/月 ({analysis['cost_savings_pct']:.1f}%)")
    lines.append(f"性能提升: {analysis['throughput_improvement_pct']:.1f}%")
    lines.append(f"收入增长: ${analysis['monthly_revenue_growth']:.2f}/月")
    lines.append(f"ROI: {analysis['roi_pct']:.1f}%")
    
    # TCO
    lines.append("\n📈 3年 TCO 对比")
    lines.append("-"*40)
    lines.append(f"当前方案3年TCO: ${analysis['current_tco']:,}")
    lines.append(f"新方案3年TCO:  ${analysis['new_tco']:,}")
    lines.append(f"3年节省:       ${analysis['tco_savings']:,}")
    
    # 回收期
    lines.append("\n⏱️ 回收期")
    lines.append("-"*40)
    if isinstance(analysis['payback_months'], str):
        lines.append(f"回收期: {analysis['payback_months']}")
    else:
        lines.append(f"回收期: {analysis['payback_months']:.1f} 个月")
    
    lines.append("="*60 + "\n")
    
    return "\n".join(lines)


def export_csv(result: dict, filename: str):
    """导出CSV"""
    current = result["current"]
    new = result["new"]
    analysis = result["analysis"]
    
    with open(filename, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(["指标", "当前方案", "新方案"])
        writer.writerow(["GPU型号", current['gpu'], new['gpu']])
        writer.writerow(["GPU数量", current['count'], new['count']])
        writer.writerow(["月成本($)", current['monthly_cost'], new['monthly_cost']])
        writer.writerow(["吞吐量(tokens/s)", current['throughput'], new['throughput']])
        writer.writerow(["月收入($)", round(current['monthly_revenue'], 2), round(new['monthly_revenue'], 2)])
        writer.writerow([])
        writer.writerow(["分析指标", "值"])
        writer.writerow(["月节省($)", round(analysis['monthly_savings'], 2)])
        writer.writerow(["成本节省(%)", analysis['cost_savings_pct']])
        writer.writerow(["性能提升(%)", analysis['throughput_improvement_pct']])
        writer.writerow(["月收入增长($)", round(analysis['monthly_revenue_growth'], 2)])
        writer.writerow(["ROI(%)", analysis['roi_pct']])
        writer.writerow(["回收期(月)", analysis['payback_months']])
        writer.writerow([])
        writer.writerow(["TCO分析", "值"])
        writer.writerow(["当前方案3年TCO", analysis['current_tco']])
        writer.writerow(["新方案3年TCO", analysis['new_tco']])
        writer.writerow(["3年节省($)", analysis['tco_savings']])
    
    print(f"CSV已导出: {filename}")


def main():
    parser = argparse.ArgumentParser(description='AI算力销售ROI分析器')
    
    # 当前方案
    parser.add_argument('--current-gpu', type=str, required=True, help='当前GPU型号')
    parser.add_argument('--current-count', type=int, required=True, help='当前GPU数量')
    parser.add_argument('--current-cost', type=float, required=True, help='当前方案月成本($)')
    
    # 新方案
    parser.add_argument('--new-gpu', type=str, required=True, help='新方案GPU型号')
    parser.add_argument('--new-count', type=int, required=True, help='新方案GPU数量')
    parser.add_argument('--new-cost', type=float, required=True, help='新方案月成本($)')
    
    # 性能指标
    parser.add_argument('--throughput-current', type=float, required=True, help='当前吞吐量(tokens/s)')
    parser.add_argument('--throughput-new', type=float, required=True, help='新方案吞吐量(tokens/s)')
    
    # 业务指标
    parser.add_argument('--revenue-per-token', type=float, default=0.001, help='每千token收入($), 默认0.001')
    parser.add_argument('--period', type=int, default=36, help='分析周期(月), 默认36')
    
    # 输出选项
    parser.add_argument('--json', action='store_true', help='JSON格式输出')
    parser.add_argument('--export', type=str, help='导出CSV文件路径')
    
    args = parser.parse_args()
    
    # 计算
    result = calculate_roi(args)
    
    # 输出
    if args.json:
        print(json.dumps(result, indent=2, ensure_ascii=False))
    else:
        print(format_output(result))
    
    # 导出CSV
    if args.export:
        export_csv(result, args.export)
    
    return 0


if __name__ == "__main__":
    sys.exit(main())

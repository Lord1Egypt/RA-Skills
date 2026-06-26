#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ITSM 工单趋势分析脚本
生成日报/周报/月报
"""

import json
import sys
import argparse
from datetime import datetime, timedelta
from pathlib import Path
from collections import defaultdict

def load_tickets(input_file):
    """加载工单数据"""
    if not Path(input_file).exists():
        return None, f"文件不存在：{input_file}"
    
    try:
        import csv
        with open(input_file, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            tickets = list(reader)
        return tickets, None
    except Exception as e:
        return None, str(e)

def parse_date(date_str):
    """解析日期字符串"""
    formats = [
        '%Y-%m-%d %H:%M:%S',
        '%Y-%m-%d',
        '%Y/%m/%d %H:%M:%S',
        '%Y/%m/%d'
    ]
    for fmt in formats:
        try:
            return datetime.strptime(date_str, fmt)
        except:
            continue
    return datetime.now()

def calculate_metrics(tickets, period='daily'):
    """计算工单指标"""
    now = datetime.now()
    
    # 根据周期过滤工单
    if period == 'daily':
        delta = timedelta(days=1)
        start_time = now - delta
    elif period == 'weekly':
        delta = timedelta(weeks=1)
        start_time = now - delta
    elif period == 'monthly':
        delta = timedelta(days=30)
        start_time = now - delta
    else:
        start_time = now - timedelta(days=1)
    
    filtered = []
    for t in tickets:
        created = parse_date(t.get('created_at', ''))
        if created >= start_time:
            filtered.append(t)
    
    # 计算指标
    total = len(filtered)
    resolved = sum(1 for t in filtered if t.get('status') in ['已解决', 'Resolved', 'Closed'])
    
    # 工单类型分布
    type_dist = defaultdict(int)
    for t in filtered:
        ticket_type = t.get('type', '未分类')
        type_dist[ticket_type] += 1
    
    # 优先级分布
    priority_dist = defaultdict(int)
    for t in filtered:
        priority = t.get('priority', 'P3')
        priority_dist[priority] += 1
    
    # 处理人工作量
    assignee_dist = defaultdict(int)
    for t in filtered:
        assignee = t.get('assignee', '未分配')
        assignee_dist[assignee] += 1
    
    return {
        'period': period,
        'total': total,
        'resolved': resolved,
        'resolution_rate': round(resolved / total * 100, 1) if total > 0 else 0,
        'type_distribution': dict(type_dist),
        'priority_distribution': dict(priority_dist),
        'assignee_distribution': dict(assignee_dist)
    }

def generate_report(metrics, prev_metrics=None):
    """生成 Markdown 报告"""
    lines = []
    lines.append("## 📊 ITSM 工单报告")
    lines.append(f"\n**统计周期**: {metrics['period']}")
    lines.append(f"**生成时间**: {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    
    lines.append(f"\n### 核心指标")
    lines.append(f"- 新增工单：**{metrics['total']} 个**")
    if prev_metrics:
        diff = metrics['total'] - prev_metrics['total']
        arrow = "↑" if diff > 0 else "↓"
        lines.append(f"- 较上期：{arrow}{abs(diff)} 个")
    lines.append(f"- 已解决：**{metrics['resolved']} 个** ({metrics['resolution_rate']}%)")
    
    lines.append(f"\n### 工单类型分布")
    sorted_types = sorted(metrics['type_distribution'].items(), key=lambda x: x[1], reverse=True)
    for i, (ticket_type, count) in enumerate(sorted_types[:5], 1):
        lines.append(f"{i}. {ticket_type}：{count} 个")
    
    lines.append(f"\n### 优先级分布")
    for priority in ['P0', 'P1', 'P2', 'P3']:
        count = metrics['priority_distribution'].get(priority, 0)
        if count > 0:
            lines.append(f"- {priority}: {count} 个")
    
    lines.append(f"\n### 处理人工作量 Top 5")
    sorted_assignees = sorted(metrics['assignee_distribution'].items(), key=lambda x: x[1], reverse=True)
    for i, (assignee, count) in enumerate(sorted_assignees[:5], 1):
        lines.append(f"{i}. {assignee}: {count} 个")
    
    lines.append(f"\n---\n_报告由 ITSM 分析技能自动生成_")
    
    return "\n".join(lines)

def main():
    parser = argparse.ArgumentParser(description='ITSM 工单趋势分析')
    parser.add_argument('--input', required=True, help='工单数据文件路径')
    parser.add_argument('--period', default='daily', choices=['daily', 'weekly', 'monthly'], help='统计周期')
    parser.add_argument('--output', help='输出文件路径（可选）')
    args = parser.parse_args()
    
    # 加载数据
    tickets, error = load_tickets(args.input)
    if error:
        print(f"❌ 错误：{error}")
        sys.exit(1)
    
    # 计算指标
    metrics = calculate_metrics(tickets, args.period)
    
    # 生成报告
    report = generate_report(metrics)
    
    # 输出
    if args.output:
        with open(args.output, 'w', encoding='utf-8') as f:
            f.write(report)
        print(f"✅ 报告已保存到：{args.output}")
    else:
        print(report)

if __name__ == '__main__':
    main()

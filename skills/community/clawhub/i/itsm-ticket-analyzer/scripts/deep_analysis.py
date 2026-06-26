#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
嘉为蓝鲸 ITSM 工单深度分析脚本
包含：处理人工作量、响应时间、问题分类、日报/周报模板
"""

import pandas as pd
import json
import sys
import argparse
from datetime import datetime, timedelta
from collections import defaultdict
from pathlib import Path

def load_excel_data(input_file):
    """加载嘉为蓝鲸 Excel 工单数据"""
    if not Path(input_file).exists():
        return None, f"文件不存在：{input_file}"
    
    try:
        # 嘉为蓝鲸格式：第 1 行节名称，第 2 行字段名，第 3 行开始数据
        df_raw = pd.read_excel(input_file, engine='openpyxl', header=None)
        columns = df_raw.iloc[1].fillna('').astype(str)
        data = df_raw.iloc[2:].copy()
        data.columns = columns
        
        return data, None
    except Exception as e:
        return None, str(e)

def analyze_assignee_workload(data):
    """处理人工作量分析"""
    assignee_workload = defaultdict(lambda: {'count': 0, 'tickets': []})
    
    for i in range(len(data)):
        row = data.iloc[i]
        assignee = row.get('当前处理人', '未分配')
        if pd.isna(assignee) or not str(assignee).strip():
            assignee = '未分配'
        
        ticket_info = {
            'id': row.get('单号', ''),
            'title': str(row.get('标题', ''))[:40],
            'status': row.get('状态', '')
        }
        
        assignee_workload[str(assignee)]['count'] += 1
        assignee_workload[str(assignee)]['tickets'].append(ticket_info)
    
    # 排序
    sorted_assignees = sorted(
        assignee_workload.items(), 
        key=lambda x: x[1]['count'], 
        reverse=True
    )
    
    return sorted_assignees

def analyze_response_time(data):
    """响应时间分析"""
    resolution_times = []  # 已解决工单
    waiting_times = []     # 未解决工单
    now = datetime.now()
    
    for i in range(len(data)):
        row = data.iloc[i]
        created = row.get('提单时间', '')
        resolved = row.get('结束时间', '')
        ticket_id = row.get('单号', '')
        
        if pd.isna(created) or not str(created).strip():
            continue
        
        try:
            created_dt = pd.to_datetime(created)
            
            if pd.notna(resolved) and str(resolved).strip():
                # 已解决工单
                try:
                    resolved_dt = pd.to_datetime(resolved)
                    hours = (resolved_dt - created_dt).total_seconds() / 3600
                    resolution_times.append({
                        'ticket_id': ticket_id,
                        'hours': hours,
                        'days': hours / 24
                    })
                except:
                    pass
            else:
                # 未解决工单
                days_waiting = (now - created_dt).days
                waiting_times.append({
                    'ticket_id': ticket_id,
                    'days': days_waiting
                })
        except:
            pass
    
    return resolution_times, waiting_times

def categorize_tickets(data):
    """问题分类统计"""
    category_keywords = {
        '登录问题': ['登录', '登陆', '密码', '认证', '权限'],
        '服务宕机': ['宕机', '崩溃', '停止', '异常', '故障'],
        '监控告警': ['告警', '监控', '采集', '检测'],
        '工单系统': ['工单', '流程', '审批', '委派'],
        '数据问题': ['数据', '数据库', 'MongoDB', 'MySQL', 'InfluxDB'],
        '网络问题': ['网络', '防火墙', '连接', '端口'],
        '配置问题': ['配置', '设置', '参数'],
        '其他': []
    }
    
    category_count = defaultdict(lambda: {'count': 0, 'tickets': []})
    
    for i in range(len(data)):
        row = data.iloc[i]
        title = str(row.get('标题', '')).lower()
        ticket_id = row.get('单号', '')
        status = row.get('状态', '')
        
        ticket_info = {
            'id': ticket_id,
            'title': str(row.get('标题', ''))[:50],
            'status': status
        }
        
        categorized = False
        for category, keywords in category_keywords.items():
            if category == '其他':
                continue
            for keyword in keywords:
                if keyword.lower() in title:
                    category_count[category]['count'] += 1
                    category_count[category]['tickets'].append(ticket_info)
                    categorized = True
                    break
            if categorized:
                break
        
        if not categorized:
            category_count['其他']['count'] += 1
            category_count['其他']['tickets'].append(ticket_info)
    
    # 排序
    sorted_categories = sorted(
        category_count.items(), 
        key=lambda x: x[1]['count'], 
        reverse=True
    )
    
    return sorted_categories

def generate_report(data, output_format='markdown'):
    """生成完整分析报告"""
    # 执行各项分析
    assignee_stats = analyze_assignee_workload(data)
    resolution_times, waiting_times = analyze_response_time(data)
    category_stats = categorize_tickets(data)
    
    report_lines = []
    
    # 1. 处理人工作量
    report_lines.append("## 📈 处理人工作量统计")
    report_lines.append("")
    report_lines.append("| 处理人 | 工单数 | 占比 |")
    report_lines.append("|--------|--------|------|")
    
    total = len(data)
    for assignee, info in assignee_stats[:10]:
        pct = info['count'] / total * 100
        report_lines.append(f"| {assignee} | {info['count']} | {pct:.1f}% |")
    
    # 2. 响应时间分析
    report_lines.append("")
    report_lines.append("## ⏱️  响应时间分析")
    report_lines.append("")
    
    if resolution_times:
        hours_list = [r['hours'] for r in resolution_times]
        avg_hours = sum(hours_list) / len(hours_list)
        
        report_lines.append(f"**已解决工单（{len(resolution_times)} 个）:**")
        report_lines.append(f"- 平均响应时间：{avg_hours:.1f} 小时 ({avg_hours/24:.1f} 天)")
        report_lines.append(f"- 最快：{min(hours_list):.1f} 小时")
        report_lines.append(f"- 最慢：{max(hours_list):.1f} 小时")
        
        # Top 5 最慢
        sorted_resolution = sorted(resolution_times, key=lambda x: x['hours'], reverse=True)[:5]
        report_lines.append("")
        report_lines.append("**最慢的 5 个工单:**")
        for r in sorted_resolution:
            report_lines.append(f"- {r['ticket_id']}: {r['hours']:.1f} 小时")
    
    if waiting_times:
        days_list = [r['days'] for r in waiting_times]
        avg_days = sum(days_list) / len(days_list)
        
        report_lines.append("")
        report_lines.append(f"**未解决工单（{len(waiting_times)} 个）:**")
        report_lines.append(f"- 平均等待时间：{avg_days:.1f} 天")
        report_lines.append(f"- 最短等待：{min(days_list)} 天")
        report_lines.append(f"- 最长等待：{max(days_list)} 天")
        
        # Top 5 等待最久
        sorted_waiting = sorted(waiting_times, key=lambda x: x['days'], reverse=True)[:5]
        report_lines.append("")
        report_lines.append("**等待最久的 5 个工单:**")
        for r in sorted_waiting:
            report_lines.append(f"- {r['ticket_id']}: {r['days']} 天")
    
    # 3. 问题分类统计
    report_lines.append("")
    report_lines.append("## 📂 问题分类统计")
    report_lines.append("")
    report_lines.append("| 分类 | 数量 | 占比 | 典型案例 |")
    report_lines.append("|------|------|------|----------|")
    
    for category, info in category_stats:
        if info['count'] > 0:
            pct = info['count'] / total * 100
            example = info['tickets'][0]['title'] if info['tickets'] else ''
            report_lines.append(f"| {category} | {info['count']} | {pct:.1f}% | {example}... |")
    
    # 4. 关键发现与建议
    report_lines.append("")
    report_lines.append("## 💡 关键发现与建议")
    report_lines.append("")
    
    # 检查未分配比例
    unassigned = next((info for assignee, info in assignee_stats if assignee == '未分配'), None)
    if unassigned and unassigned['count'] / total > 0.3:
        report_lines.append(f"**🔴 紧急**: {unassigned['count']/total*100:.1f}% 工单未分配 — 需建立自动分配机制")
    
    # 检查响应时间
    if resolution_times:
        if avg_hours > 168:  # 超过 7 天
            report_lines.append(f"**🔴 紧急**: 平均响应时间 {avg_hours/24:.1f} 天 — 严重超时，需优化流程")
    
    # 检查等待时间
    if waiting_times and max(days_list) > 90:
        report_lines.append(f"**🔴 紧急**: 最长等待 {max(days_list)} 天 — 需清理历史遗留工单")
    
    # 重复问题检查
    for category, info in category_stats:
        if info['count'] >= 3:
            report_lines.append(f"**🟡 关注**: {category} 类问题 {info['count']} 个 — 建议专项优化")
    
    return "\n".join(report_lines)

def main():
    parser = argparse.ArgumentParser(description='嘉为蓝鲸 ITSM 工单深度分析')
    parser.add_argument('--input', required=True, help='Excel 工单文件路径')
    parser.add_argument('--output', help='输出文件路径（可选）')
    parser.add_argument('--format', default='markdown', choices=['markdown', 'json'], help='输出格式')
    args = parser.parse_args()
    
    # 加载数据
    data, error = load_excel_data(args.input)
    if error:
        print(f"❌ 错误：{error}")
        sys.exit(1)
    
    print(f"✅ 成功加载 {len(data)} 个工单")
    
    # 生成报告
    report = generate_report(data, args.format)
    
    # 输出
    if args.output:
        with open(args.output, 'w', encoding='utf-8') as f:
            f.write(report)
        print(f"✅ 报告已保存到：{args.output}")
    else:
        print("\n" + report)

if __name__ == '__main__':
    main()

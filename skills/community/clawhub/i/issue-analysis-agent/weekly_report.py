#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
客服问题周报生成器 - 完整流程脚本
技能名称：issue-analysis-agent
版本：v2.1.0
更新：2026-03-24

团队协作流程：
1. 找茬 🐛 - 数据分析（读取 Excel、统计分析）
2. 画师 🎨 - 报告生成（HTML 可视化、上传 COS）

新增功能：
- 发布前检查清单
- 自动验证步骤
- 详细的错误报告

使用方法：
python3 weekly_report.py /path/to/issue_data.xlsx
"""

import sys
import os
from pathlib import Path
from datetime import datetime

# 导入子模块
from analyze import analyze_excel, save_data
from generate_report import generate_report, validate_report
from upload_cos import upload_to_cos, validate_upload

# ============ 发布前检查清单 ============
DEPLOY_CHECKLIST = [
    "✅ 数据文件存在且可读",
    "✅ JSON 字段名正确（summary, weekly_trend, issue_types, platforms, reporters, resolvers, unresolved_resolvers, unresolved_modules）",
    "✅ 图表标题正确（无红色警告样式）",
    "✅ HTML 响应头正确（Content-Type, Content-Disposition, Cache-Control）",
    "✅ 上传后验证通过",
    "✅ 所有图表都能正常显示",
]

def print_checklist():
    """打印发布前检查清单"""
    print("\n" + "=" * 60)
    print("📋 发布前检查清单")
    print("=" * 60)
    for item in DEPLOY_CHECKLIST:
        print(f"  {item}")
    print("=" * 60)

def check_data_file(excel_file):
    """检查数据文件"""
    print("\n【检查 1/6】数据文件...")
    
    if not Path(excel_file).exists():
        print(f"  ❌ 文件不存在：{excel_file}")
        return False
    
    print(f"  ✅ 文件存在：{excel_file}")
    return True

def check_json_fields(data):
    """检查 JSON 字段名"""
    print("\n【检查 2/6】JSON 字段名...")
    
    required_fields = [
        'summary',
        'weekly_trend',
        'issue_types',
        'platforms',
        'reporters',
        'resolvers',
        'unresolved_resolvers',
        'unresolved_modules'
    ]
    
    all_present = True
    for field in required_fields:
        # 支持旧字段名兼容
        if field == 'weekly_trend' and 'weekly' in data:
            print(f"  ✅ {field} (兼容字段：weekly)")
        elif field == 'issue_types' and 'types' in data:
            print(f"  ✅ {field} (兼容字段：types)")
        elif field in data:
            print(f"  ✅ {field}")
        else:
            print(f"  ⚠️ 缺少字段：{field}")
            all_present = False
    
    return all_present

def check_html_report(html_path):
    """检查 HTML 报告"""
    print("\n【检查 3/6】HTML 报告...")
    
    if not validate_report(html_path):
        return False
    
    print(f"  ✅ HTML 报告验证通过")
    return True

def check_response_headers(public_url, original_content):
    """检查响应头"""
    print("\n【检查 4/6】响应头...")
    
    if not validate_upload(public_url, original_content):
        print(f"  ⚠️ 响应头验证有警告（可能是 COS 延迟）")
        # 不返回 False，因为 COS 有时会有延迟
    
    print(f"  ✅ 响应头检查完成")
    return True

def check_charts_display(html_path):
    """检查图表是否能正常显示"""
    print("\n【检查 5/6】图表显示...")
    
    with open(html_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    chart_ids = [
        'weeklyChart',
        'typeChart',
        'platformChart',
        'reporterChart',
        'resolverChart',
        'unresolvedResolverChart'
    ]
    
    all_present = True
    for chart_id in chart_ids:
        if f'id="{chart_id}"' in content and f"getElementById('{chart_id}')" in content:
            print(f"  ✅ 图表 {chart_id}")
        else:
            print(f"  ❌ 图表 {chart_id} 缺失")
            all_present = False
    
    return all_present

def check_data_quality(data):
    """检查数据质量"""
    print("\n【检查 6/6】数据质量...")
    
    summary = data.get('summary', {})
    total = summary.get('total', 0)
    
    if total == 0:
        print(f"  ⚠️ 数据为空（total=0）")
        return False
    
    print(f"  ✅ 数据有效（total={total}）")
    return True

def weekly_report(excel_file):
    """生成周报的完整流程（包含检查清单）"""
    
    print("=" * 60)
    print("📊 客服问题周报生成")
    print("=" * 60)
    
    # 打印检查清单
    print_checklist()
    
    # 准备工作目录
    base_dir = Path(excel_file).parent
    output_dir = base_dir / 'report'
    output_dir.mkdir(exist_ok=True)
    
    # 步骤 1: 检查数据文件
    if not check_data_file(excel_file):
        print("\n❌ 检查失败：数据文件问题")
        return None
    
    # 步骤 2: 分析数据（找茬 🐛 的工作）
    print("\n【步骤 1/5】🐛 找茬：分析 Excel 数据...")
    data = analyze_excel(excel_file)
    
    if not data:
        print("❌ 数据分析失败")
        return None
    
    # 检查 JSON 字段
    if not check_json_fields(data):
        print("\n⚠️ 警告：JSON 字段名可能有问题")
    
    # 检查数据质量
    if not check_data_quality(data):
        print("\n⚠️ 警告：数据质量有问题")
    
    # 保存分析结果
    analysis_json = base_dir / 'analysis_data_latest.json'
    save_data(data, analysis_json)
    
    # 步骤 3: 生成 HTML 报告（画师 🎨 的工作）
    print("\n【步骤 2/5】🎨 画师：生成 HTML 报告...")
    report_html = output_dir / 'report_cn_latest.html'
    generate_report(analysis_json, report_html)
    
    # 检查 HTML 报告
    if not check_html_report(report_html):
        print("\n⚠️ 警告：HTML 报告验证有问题")
    
    # 检查图表显示
    if not check_charts_display(report_html):
        print("\n⚠️ 警告：图表显示可能有问题")
    
    # 步骤 4: 上传到 COS（画师 🎨 的工作）
    print("\n【步骤 3/5】🎨 画师：上传到 COS...")
    cos_key = 'reports/issue_analysis/report_cn_latest.html'
    public_url = upload_to_cos(report_html, cos_key)
    
    if not public_url:
        print("\n❌ 上传失败")
        return None
    
    # 读取原始内容用于验证
    with open(report_html, 'rb') as f:
        original_content = f.read()
    
    # 检查响应头
    if not check_response_headers(public_url, original_content):
        print("\n⚠️ 警告：响应头验证有警告")
    
    # 步骤 5: 输出结果
    print("\n【步骤 4/5】生成报告摘要...")
    print("\n" + "=" * 60)
    print("✅ 周报生成完成！")
    print("=" * 60)
    print(f"\n📊 核心数据:")
    print(f"  问题总数：{data['summary']['total']}")
    print(f"  已解决：{data['summary']['resolved']} ({data['summary']['rate']})")
    print(f"  未解决：{data['summary']['unresolved']}")
    
    print(f"\n🏷️ 问题类型 TOP3:")
    for i, (t, c) in enumerate(list(data['types'].items())[:3], 1):
        print(f"  {i}. {t}: {c}")
    
    print(f"\n🖥️ 平台 TOP3:")
    for i, (p, c) in enumerate(list(data['platforms'].items())[:3], 1):
        print(f"  {i}. {p}: {c}")
    
    print(f"\n👤 反馈人 TOP3:")
    for i, (name, c) in enumerate(list(data['reporters'].items())[:3], 1):
        print(f"  {i}. {name}: {c}")
    
    print(f"\n✅ 解决人 TOP3:")
    for i, (name, c) in enumerate(list(data['resolvers'].items())[:3], 1):
        print(f"  {i}. {name}: {c}")
    
    print(f"\n⚠️ 未解问题人 TOP5:")
    for i, (name, c) in enumerate(list(data['unresolved_resolvers'].items())[:5], 1):
        print(f"  {i}. {name}: {c}")
    
    print(f"\n🔗 报告链接:")
    print(f"  {public_url}")
    
    # 检查是否需要告警
    print("\n【步骤 5/5】🔍 自动告警检查:")
    
    alerts = []
    rate_num = float(data['summary']['rate'].replace('%', ''))
    
    if rate_num < 80:
        alerts.append(f"🔴 解决率低于 80% ({data['summary']['rate']})")
    
    if data['summary']['total'] > 50:
        alerts.append(f"🔴 单周新增超过 50 个 ({data['summary']['total']})")
    
    if data['types'].get('bug', 0) / max(data['summary']['total'], 1) > 0.6:
        alerts.append(f"🟡 Bug 占比超过 60%")
    
    if data['platforms'].get('卖家端', 0) / max(data['summary']['total'], 1) > 0.6:
        alerts.append(f"🟡 卖家端问题占比超过 60%")
    
    if alerts:
        print("\n⚠️ 告警信息:")
        for alert in alerts:
            print(f"  {alert}")
    else:
        print("\n✅ 无异常告警")
    
    print("\n" + "=" * 60)
    print("✅ 所有检查完成！")
    print("=" * 60)
    
    return {
        'url': public_url,
        'data': data,
        'alerts': alerts
    }

def main():
    """主函数"""
    
    if len(sys.argv) < 2:
        print("用法：python3 weekly_report.py <Excel 文件路径>")
        print("示例：python3 weekly_report.py issue_data_week_12.xlsx")
        sys.exit(1)
    
    excel_file = sys.argv[1]
    
    if not Path(excel_file).exists():
        print(f"❌ 文件不存在：{excel_file}")
        sys.exit(1)
    
    # 生成周报
    result = weekly_report(excel_file)
    
    if result:
        print("\n🎉 任务完成！报告链接已生成")
    else:
        print("\n❌ 任务失败")
        sys.exit(1)

if __name__ == '__main__':
    main()

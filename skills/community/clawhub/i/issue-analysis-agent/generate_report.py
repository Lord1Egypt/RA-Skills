#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
客服问题分析报告生成器 - HTML 可视化报告
技能名称：issue-analysis-agent
版本：v2.1.0
更新：2026-03-24

功能：
1. 读取分析数据 JSON（字段名与 JSON 完全一致）
2. 生成 HTML 交互式报告（Chart.js）
3. 包含 8 个图表（含未解问题人 TOP5）
4. 中文完美显示
5. 动态周数标题

团队协作：画师 🎨 负责
"""

import json
import sys
from pathlib import Path
from datetime import datetime

def generate_report(data_json, output_html):
    """生成 HTML 报告（完整版本，包含 8 个图表）"""
    
    print(f"📊 读取数据：{data_json}")
    
    with open(data_json, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # 从 JSON 动态读取所有字段（确保字段名一致）
    summary = data.get('summary', {})
    total = summary.get('total', 0)
    resolved = summary.get('resolved', 0)
    unresolved = summary.get('unresolved', 0)
    rate = summary.get('rate', '0%')
    week_num = summary.get('week_num', 12)  # 从 JSON 读取周数
    
    # 准备数据（所有字段从 JSON 动态读取）
    weekly = data.get('weekly_trend', data.get('weekly', {}))
    types = list(data.get('issue_types', data.get('types', {})).items())[:5]
    platforms = list(data.get('platforms', {}).items())[:5]
    reporters = list(data.get('reporters', {}).items())[:5]
    resolvers = list(data.get('resolvers', {}).items())[:5]
    unresolved_resolvers = list(data.get('unresolved_resolvers', {}).items())[:5]
    unresolved_modules = list(data.get('unresolved_modules', {}).items())[:10]
    
    print(f"📈 准备图表数据:")
    print(f"  每周趋势：{len(weekly)} 周")
    print(f"  问题类型：{len(types)} 个")
    print(f"  平台：{len(platforms)} 个")
    print(f"  反馈人：{len(reporters)} 个")
    print(f"  解决人：{len(resolvers)} 个")
    print(f"  未解问题人：{len(unresolved_resolvers)} 个")
    
    # 生成 HTML
    html = f'''<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>客服问题数据分析报告 - 第{week_num}周</title>
    <script src="https://cdn.jsdelivr.net/npm/chart.js@4.4.0/dist/chart.umd.min.js"></script>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{ font-family: -apple-system, BlinkMacSystemFont, "PingFang SC", "Helvetica Neue", Arial, sans-serif; padding: 20px; background: #f5f6fa; }}
        .container {{ max-width: 1200px; margin: 0 auto; }}
        h1 {{ text-align: center; color: #2c3e50; margin-bottom: 30px; font-size: 28px; }}
        .summary {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 20px; margin-bottom: 30px; }}
        .card {{ background: white; padding: 20px; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); text-align: center; }}
        .card h3 {{ color: #7f8c8d; font-size: 14px; margin-bottom: 10px; }}
        .card .number {{ font-size: 36px; font-weight: bold; color: #3498db; }}
        .card .number.success {{ color: #27ae60; }}
        .card .number.info {{ color: #e74c3c; }}
        .chart-container {{ background: white; padding: 20px; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); margin-bottom: 20px; }}
        .chart-container h2 {{ color: #2c3e50; margin-bottom: 20px; font-size: 18px; }}
        .chart-box {{ position: relative; height: 300px; }}
        .grid-2 {{ display: grid; grid-template-columns: 1fr 1fr; gap: 20px; }}
        table {{ width: 100%; border-collapse: collapse; margin-top: 10px; }}
        th, td {{ padding: 12px; text-align: left; border-bottom: 1px solid #ecf0f1; }}
        th {{ background: #f8f9fa; color: #2c3e50; font-weight: 600; }}
        tr:hover {{ background: #f8f9fa; }}
        @media (max-width: 768px) {{ .grid-2 {{ grid-template-columns: 1fr; }} }}
    </style>
</head>
<body>
    <div class="container">
        <h1>📊 客服问题数据分析报告 - 第{week_num}周</h1>
        
        <div class="summary">
            <div class="card">
                <h3>问题总数</h3>
                <div class="number">{total}</div>
            </div>
            <div class="card">
                <h3>已解决</h3>
                <div class="number success">{resolved}</div>
            </div>
            <div class="card">
                <h3>未解决</h3>
                <div class="number info">{unresolved}</div>
            </div>
            <div class="card">
                <h3>解决率</h3>
                <div class="number success">{rate}</div>
            </div>
        </div>

        <div class="grid-2">
            <div class="chart-container">
                <h2>📈 每周新增问题趋势</h2>
                <div class="chart-box">
                    <canvas id="weeklyChart"></canvas>
                </div>
            </div>
            <div class="chart-container">
                <h2>🏷️ 问题类型分布</h2>
                <div class="chart-box">
                    <canvas id="typeChart"></canvas>
                </div>
            </div>
        </div>

        <div class="chart-container">
            <h2>💻 平台问题分布 TOP5</h2>
            <div class="chart-box">
                <canvas id="platformChart"></canvas>
            </div>
        </div>

        <div class="grid-2">
            <div class="chart-container">
                <h2>👤 反馈人 TOP5</h2>
                <div class="chart-box">
                    <canvas id="reporterChart"></canvas>
                </div>
            </div>
            <div class="chart-container">
                <h2>✅ 解决人 TOP5</h2>
                <div class="chart-box">
                    <canvas id="resolverChart"></canvas>
                </div>
            </div>
        </div>

        <div class="chart-container">
            <h2>📋 未解问题人 TOP5（解决者中未解决问题最多的）</h2>
            <div class="chart-box">
                <canvas id="unresolvedResolverChart"></canvas>
            </div>
        </div>

        <div class="chart-container">
            <h2>📦 未解决问题模块 TOP10</h2>
            <table>
                <thead>
                    <tr>
                        <th>排名</th>
                        <th>模块</th>
                        <th>未解决问题数</th>
                    </tr>
                </thead>
                <tbody>
                    {''.join([f"<tr><td>{{i+1}}</td><td>{{k}}</td><td><strong>{{v}}</strong></td></tr>" for i, (k, v) in enumerate(unresolved_modules)])}
                </tbody>
            </table>
        </div>
    </div>

    <script>
        // 每周趋势图
        new Chart(document.getElementById('weeklyChart'), {{
            type: 'line',
            data: {{
                labels: {list(weekly.keys())},
                datasets: [{{
                    label: '问题数',
                    data: {list(weekly.values())},
                    borderColor: '#667eea',
                    backgroundColor: 'rgba(102, 126, 234, 0.1)',
                    tension: 0.3,
                    fill: true
                }}]
            }},
            options: {{ responsive: true, maintainAspectRatio: false }}
        }});

        // 问题类型
        new Chart(document.getElementById('typeChart'), {{
            type: 'pie',
            data: {{
                labels: { [t[0] for t in types] },
                datasets: [{{
                    data: { [t[1] for t in types] },
                    backgroundColor: ['#FF6B6B', '#4ECDC4', '#45B7D1', '#FFA07A', '#98D8C8', '#F7DC6F', '#BB8FCE', '#F1948A']
                }}]
            }},
            options: {{ responsive: true, maintainAspectRatio: false }}
        }});

        // 平台分布
        new Chart(document.getElementById('platformChart'), {{
            type: 'bar',
            data: {{
                labels: { [p[0] for p in platforms] },
                datasets: [{{
                    label: '问题数',
                    data: { [p[1] for p in platforms] },
                    backgroundColor: ['#667eea', '#764ba2', '#f093fb', '#4facfe', '#43e97b']
                }}]
            }},
            options: {{ responsive: true, maintainAspectRatio: false, indexAxis: 'y' }}
        }});

        // 反馈人
        new Chart(document.getElementById('reporterChart'), {{
            type: 'bar',
            data: {{
                labels: { [r[0] for r in reporters] },
                datasets: [{{
                    label: '问题数',
                    data: { [r[1] for r in reporters] },
                    backgroundColor: ['#fa709a', '#fee140', '#30cfd0', '#a8edea', '#fed6e3']
                }}]
            }},
            options: {{ responsive: true, maintainAspectRatio: false }}
        }});

        // 解决人
        new Chart(document.getElementById('resolverChart'), {{
            type: 'bar',
            data: {{
                labels: { [r[0] for r in resolvers] },
                datasets: [{{
                    label: '解决问题数',
                    data: { [r[1] for r in resolvers] },
                    backgroundColor: ['#11998e', '#38ef7d', '#0ba360', '#2d3436', '#636e72']
                }}]
            }},
            options: {{ responsive: true, maintainAspectRatio: false }}
        }});

        // 未解问题人
        new Chart(document.getElementById('unresolvedResolverChart'), {{
            type: 'bar',
            data: {{
                labels: { [r[0] for r in unresolved_resolvers] },
                datasets: [{{
                    label: '未解决问题数',
                    data: { [r[1] for r in unresolved_resolvers] },
                    backgroundColor: ['#e74c3c', '#e67e22', '#f39c12', '#f1c40f', '#d35400']
                }}]
            }},
            options: {{ responsive: true, maintainAspectRatio: false }}
        }});
    </script>
</body>
</html>
'''
    
    # 保存 HTML
    output_path = Path(output_html)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(html)
    
    print(f"✅ HTML 报告已生成：{output_path}")
    print(f"📊 数据：{total} 条，已解决 {resolved} ({rate})")
    print(f"📈 包含图表：每周趋势 + 问题类型 + 平台 + 反馈人 + 解决人 + 未解问题人 + 未解决模块")
    
    return True

def validate_report(output_html):
    """验证生成的 HTML 报告"""
    output_path = Path(output_html)
    
    if not output_path.exists():
        print(f"❌ 验证失败：文件不存在 {output_html}")
        return False
    
    with open(output_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 检查关键元素
    checks = [
        ('<html', 'HTML 结构'),
        ('<canvas', '图表元素'),
        ('Chart.js', '图表库'),
        ('每周新增问题趋势', '趋势图标题'),
        ('问题类型分布', '类型图标题'),
        ('平台问题分布', '平台图标题'),
        ('反馈人 TOP5', '反馈人图标题'),
        ('解决人 TOP5', '解决人图标题'),
        ('未解问题人 TOP5', '未解问题人图标题'),
        ('未解决问题模块 TOP10', '模块表格标题'),
    ]
    
    all_passed = True
    for check_str, desc in checks:
        if check_str not in content:
            print(f"❌ 验证失败：缺少 {desc}")
            all_passed = False
        else:
            print(f"✅ 验证通过：{desc}")
    
    return all_passed

def main():
    """主函数"""
    
    if len(sys.argv) < 2:
        print("用法：python3 generate_report.py <数据 JSON 路径> [输出 HTML 路径]")
        print("示例：python3 generate_report.py analysis_data_latest.json report_cn.html")
        sys.exit(1)
    
    data_json = sys.argv[1]
    output_html = sys.argv[2] if len(sys.argv) > 2 else 'report_cn.html'
    
    success = generate_report(data_json, output_html)
    
    if success and '--validate' in sys.argv:
        print("\n🔍 验证报告...")
        validate_report(output_html)

if __name__ == '__main__':
    main()

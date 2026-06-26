#!/usr/bin/env python3
"""
GitLab Weekly Report - Chart Generator
优先生成 PNG 图表；若 matplotlib 不可用，则回退为 Mermaid 图表 Markdown。
"""

import json
import sys
import os
from pathlib import Path

try:
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    HAS_MPL = True
    plt.rcParams['font.sans-serif'] = ['SimHei', 'DejaVu Sans']
    plt.rcParams['axes.unicode_minus'] = False
except Exception:
    HAS_MPL = False


def load_stats(stats_file):
    with open(stats_file, 'r', encoding='utf-8') as f:
        return json.load(f)


def generate_png(stats, output_dir):
    users = list(stats['commits_by_user'].keys())
    counts = list(stats['commits_by_user'].values())

    fig, ax = plt.subplots(figsize=(10, 6))
    bars = ax.bar(users, counts, color='#4CAF50')
    ax.set_xlabel('用户')
    ax.set_ylabel('提交数')
    ax.set_title('各用户提交数量统计')
    ax.tick_params(axis='x', rotation=45)
    for bar in bars:
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2., height, f'{int(height)}', ha='center', va='bottom')
    plt.tight_layout()
    plt.savefig(f'{output_dir}/commits_by_user.png', dpi=150, bbox_inches='tight')
    plt.close()

    mr_stats = stats['mr_stats']
    labels = ['已合并', '已关闭', '进行中']
    sizes = [mr_stats.get('merged', 0), mr_stats.get('closed', 0), mr_stats.get('opened', 0)]
    colors = ['#4CAF50', '#f44336', '#2196F3']
    fig, ax = plt.subplots(figsize=(8, 8))
    ax.pie(sizes, labels=labels, colors=colors, autopct='%1.1f%%', startangle=90)
    ax.set_title('MR 状态分布')
    plt.savefig(f'{output_dir}/mr_status.png', dpi=150, bbox_inches='tight')
    plt.close()

    daily = stats['daily_activity']
    dates = sorted(daily.keys())
    vals = [daily[d] for d in dates]
    fig, ax = plt.subplots(figsize=(12, 6))
    ax.plot(dates, vals, marker='o', linewidth=2, markersize=8, color='#2196F3')
    ax.set_xlabel('日期')
    ax.set_ylabel('活动数')
    ax.set_title('每日活动趋势')
    ax.tick_params(axis='x', rotation=45)
    ax.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig(f'{output_dir}/daily_activity.png', dpi=150, bbox_inches='tight')
    plt.close()

    projects = stats['projects']
    names = list(projects.keys())
    pcounts = list(projects.values())
    fig, ax = plt.subplots(figsize=(10, 8))
    ax.pie(pcounts, labels=names, autopct='%1.1f%%', startangle=90, textprops={'fontsize': 10})
    ax.set_title('项目贡献分布')
    plt.savefig(f'{output_dir}/project_distribution.png', dpi=150, bbox_inches='tight')
    plt.close()
    return 'png'


def mermaid_xybar(title, x_labels, values, y_label='值'):
    xs = ', '.join(f'"{x}"' for x in x_labels)
    ys = ', '.join(str(v) for v in values)
    maxv = max(values) if values else 1
    return f'''```mermaid
xychart-beta
    title "{title}"
    x-axis [{xs}]
    y-axis "{y_label}" 0 --> {maxv + max(1, int(maxv*0.2))}
    bar [{ys}]
```
'''


def mermaid_pie(title, data):
    body = '\n'.join(f'    "{k}" : {v}' for k, v in data.items())
    return f'''```mermaid
pie showData
    title {title}
{body}
```
'''


def generate_mermaid(stats, output_dir):
    users = list(stats['commits_by_user'].keys())
    counts = list(stats['commits_by_user'].values())
    daily = stats['daily_activity']
    projects = stats['projects']
    mr_stats = {
        '已合并': stats['mr_stats'].get('merged', 0),
        '已关闭': stats['mr_stats'].get('closed', 0),
        '进行中': stats['mr_stats'].get('opened', 0),
    }

    charts_md = []
    charts_md.append('# 图表版周报')
    charts_md.append('')
    charts_md.append('## 1. 提交数分布')
    charts_md.append(mermaid_xybar('各用户提交数量', users, counts, '提交数'))
    charts_md.append('## 2. MR 状态分布')
    charts_md.append(mermaid_pie('MR 状态分布', mr_stats))
    charts_md.append('## 3. 每日活动趋势')
    charts_md.append(mermaid_xybar('每日活动趋势', list(daily.keys()), list(daily.values()), '活动数'))
    charts_md.append('## 4. 项目分布')
    charts_md.append(mermaid_pie('项目贡献分布', projects))

    out = Path(output_dir) / 'charts.md'
    out.write_text('\n'.join(charts_md), encoding='utf-8')
    print(f'✅ 生成: {out}')
    return 'mermaid'


def main():
    if len(sys.argv) < 3:
        print('用法: python3 generate-charts.py <stats.json> <output_dir>')
        sys.exit(1)
    stats_file = sys.argv[1]
    output_dir = sys.argv[2]
    os.makedirs(output_dir, exist_ok=True)
    stats = load_stats(stats_file)
    mode = generate_png(stats, output_dir) if HAS_MPL else generate_mermaid(stats, output_dir)
    print(f'✅ 图表生成完成，模式: {mode}')


if __name__ == '__main__':
    main()

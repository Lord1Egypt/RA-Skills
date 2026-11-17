#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
执行可视化生成器 - 多Agent协作编排引擎 v5.2

功能：根据 pipeline_state.json 生成 Markdown 报告 / HTML 甘特图 / 两者合并输出
零第三方依赖，仅使用 Python 标准库

★★★ 安全说明 ★★★
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
1. 报告文件包含节点输出数据，可能含有敏感信息
2. 建议将报告文件存放在安全位置，避免未授权访问
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

使用方式：
  python pipeline_reporter.py visualize <state.json> [--format md|html|both] [output]
  python pipeline_reporter.py report <state.json> [output.md]        （向后兼容）
  python pipeline_reporter.py gantt <state.json> [output.html]       （向后兼容）
"""

import json
import sys
import os
from datetime import datetime


def load_state(state_path):
    """加载状态文件"""
    if not os.path.exists(state_path):
        print(f"错误：状态文件不存在 [{state_path}]")
        sys.exit(1)
    try:
        with open(state_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except json.JSONDecodeError as e:
        print(f"错误：状态文件 JSON 格式不合法 [{state_path}]")
        sys.exit(1)


def parse_time(timestamp_str):
    """解析时间戳，返回可读格式"""
    if not timestamp_str:
        return "-"
    try:
        dt = datetime.strptime(timestamp_str, '%Y-%m-%dT%H:%M:%S')
        return dt.strftime('%Y-%m-%d %H:%M:%S')
    except (ValueError, TypeError):
        return str(timestamp_str)


def calc_duration(start, end):
    """计算时长，返回人类可读格式"""
    if not start or not end:
        return "-"
    try:
        s = datetime.strptime(start, '%Y-%m-%dT%H:%M:%S')
        e = datetime.strptime(end, '%Y-%m-%dT%H:%M:%S')
        delta = e - s
        seconds = int(delta.total_seconds())
        if seconds < 60:
            return f"{seconds}秒"
        elif seconds < 3600:
            mins = seconds // 60
            secs = seconds % 60
            return f"{mins}分{secs:02d}秒"
        else:
            hours = seconds // 3600
            mins = (seconds % 3600) // 60
            return f"{hours}时{mins:02d}分"
    except (ValueError, TypeError):
        return "-"


def _build_visualization_data(state):
    """构建可视化数据（共享数据层，供 MD/HTML 共同使用）"""
    pipeline_name = state.get('pipeline_name', '未命名流水线')
    pipeline_id = state.get('pipeline_id', 'unknown')
    overall_status = state.get('status', 'unknown')
    nodes = state.get('nodes', {})

    total = len(nodes)
    completed = sum(1 for n in nodes.values() if n['status'] == 'completed')
    failed = sum(1 for n in nodes.values() if n['status'] == 'failed')
    skipped = sum(1 for n in nodes.values() if n['status'] == 'skipped')
    pending = sum(1 for n in nodes.values() if n['status'] in ('pending', 'running'))
    total_retries = sum(n.get('retry_count', 0) for n in nodes.values())

    times = []
    for n in nodes.values():
        if n.get('started_at') and n.get('completed_at'):
            times.append((n['started_at'], n['completed_at']))
    total_duration = "-"
    if times:
        all_times = [t for pair in times for t in pair]
        total_duration = calc_duration(min(all_times), max(all_times))

    start_times = [n['started_at'] for n in nodes.values() if n.get('started_at')]
    end_times = [n['completed_at'] for n in nodes.values() if n.get('completed_at')]
    all_start = min(start_times) if start_times else None
    all_end = max(end_times) if end_times else None
    total_seconds = 1
    if all_start and all_end:
        try:
            s = datetime.strptime(all_start, '%Y-%m-%dT%H:%M:%S')
            e = datetime.strptime(all_end, '%Y-%m-%dT%H:%M:%S')
            total_seconds = max((e - s).total_seconds(), 1)
        except (ValueError, TypeError):
            pass

    status_map = {
        'completed': '✅ 成功完成', 'aborted': '🛑 已中止',
        'running': '🔄 执行中', 'failed': '❌ 执行失败',
        'initialized': '⏳ 已初始化（未开始）'
    }
    status_text = status_map.get(overall_status, overall_status)

    actual_tokens = 0
    actual_cost = 0.0
    est_tokens = 0
    est_cost = 0.0
    for n in nodes.values():
        cost = n.get('cost_data', {})
        if cost:
            if cost.get('est', False):
                est_tokens += cost.get('tokens', 0)
                est_cost += cost.get('cost_rmb', 0)
            else:
                actual_tokens += cost.get('tokens', 0)
                actual_cost += cost.get('cost_rmb', 0)

    return {
        'pipeline_name': pipeline_name, 'pipeline_id': pipeline_id,
        'overall_status': overall_status, 'status_text': status_text,
        'total': total, 'completed': completed, 'failed': failed,
        'skipped': skipped, 'pending': pending, 'total_retries': total_retries,
        'total_duration': total_duration, 'nodes': nodes,
        'all_start': all_start, 'all_end': all_end, 'total_seconds': total_seconds,
        'total_tokens': actual_tokens + est_tokens,
        'total_cost': round(actual_cost + est_cost, 6),
        'actual_tokens': actual_tokens,
        'actual_cost_rmb': round(actual_cost, 6),
        'est_tokens': est_tokens,
        'est_cost_rmb': round(est_cost, 6),
        'has_actual': actual_tokens > 0,
        'has_est': est_tokens > 0,
    }


def generate_report(state_path, output_path=None):
    """生成 Markdown（向后兼容包装器）"""
    return generate_visualization(state_path, output_path, 'md')


def generate_html_gantt(state_path, output_path=None):
    """生成 HTML 甘特图（向后兼容包装器）"""
    return generate_visualization(state_path, output_path, 'html')


def generate_visualization(state_path, output_path=None, fmt='both'):
    """统一可视化生成入口"""
    if fmt not in ('md', 'html', 'both'):
        print(f"错误：无效格式 [{fmt}]，应为 'md' / 'html' / 'both'")
        sys.exit(1)

    state = load_state(state_path)
    data = _build_visualization_data(state)

    if output_path is None:
        base_dir = os.path.dirname(os.path.abspath(state_path)) or '.'
        if fmt == 'md':
            output_path = os.path.join(base_dir, f"pipeline_report_{data['pipeline_id']}.md")
        elif fmt == 'html':
            output_path = os.path.join(base_dir, f"gantt_{data['pipeline_id']}.html")
        else:
            output_path = os.path.join(base_dir, f"viz_{data['pipeline_id']}")

    generated = []

    if fmt in ('md', 'both'):
        md_path = output_path if fmt == 'md' else f"{output_path}.md"
        _generate_md_report(data, state_path, md_path)
        generated.append(md_path)

    if fmt in ('html', 'both'):
        html_path = output_path if fmt == 'html' else f"{output_path}.html"
        _generate_html_gantt(data, html_path)
        generated.append(html_path)

    print(f"\n✅ 可视化生成完成：")
    for p in generated:
        print(f"  📄 {p}")
    return generated


def _generate_md_report(data, state_path, output_path):
    """生成 Markdown 报告"""
    state = load_state(state_path)
    nodes = data['nodes']

    lines = []
    lines.append(f"# 📊 流水线执行报告：{data['pipeline_name']}")
    lines.append("")
    lines.append(f"> 自动生成时间：{parse_time(state.get('updated_at', datetime.now().strftime('%Y-%m-%dT%H:%M:%S')))}")
    lines.append("")

    lines.append("## 概览")
    lines.append("")
    lines.append("| 项目 | 值 |")
    lines.append("|------|------|")
    lines.append(f"| 流水线名称 | {data['pipeline_name']} |")
    lines.append(f"| 流水线 ID | `{data['pipeline_id']}` |")
    lines.append(f"| 总状态 | **{data['status_text']}** |")
    lines.append(f"| 创建时间 | {parse_time(state.get('created_at'))} |")
    lines.append(f"| 更新时间 | {parse_time(state.get('updated_at'))} |")
    lines.append(f"| 总耗时 | {data['total_duration']} |")
    lines.append(f"| 节点总数 | {data['total']} |")
    lines.append(f"| ✅ 成功 | {data['completed']} |")
    lines.append(f"| ❌ 失败 | {data['failed']} |")
    lines.append(f"| ⏭️ 跳过 | {data['skipped']} |")
    lines.append(f"| ⏳ 待执行 | {data['pending']} |")
    lines.append(f"| 🔁 总重试次数 | {data['total_retries']} |")
    lines.append("")

    if data['total_tokens'] > 0 or data['total_cost'] > 0:
        lines.append("## 成本概览")
        lines.append("")
        lines.append("| 项目 | 值 |")
        lines.append("|------|------|")
        if data.get('has_actual'):
            lines.append(f"| 实测 Token 消耗 | {data['actual_tokens']:,} |")
            lines.append(f"| 实测费用（¥） | {data['actual_cost_rmb']:.4f} |")
        if data.get('has_est'):
            lines.append(f"| 估算 Token 消耗 | {data['est_tokens']:,} |")
            lines.append(f"| 估算费用（¥） | {data['est_cost_rmb']:.4f} |")
        lines.append(f"| **合计 Token** | **{data['total_tokens']:,}** |")
        lines.append(f"| **合计费用（¥）** | **{data['total_cost']:.4f}** |")
        if data.get('has_actual') and data.get('has_est'):
            lines.append(f"| 数据来源 | 实测 + 估算混合 |")
        elif data.get('has_actual'):
            lines.append(f"| 数据来源 | cn-llm-router 实测 |")
        else:
            lines.append(f"| 数据来源 | 估算（未安装 cn-llm-router） |")
        lines.append("")

        cost_rows = []
        for aid, node in nodes.items():
            cost = node.get('cost_data', {})
            if cost:
                tokens = cost.get('tokens', 0)
                cost_val = cost.get('cost_rmb', 0)
                model = cost.get('model', '-')
                tag = '🔵实测' if not cost.get('est', False) else '⚪估算'
                cost_rows.append(f"| [{aid}] | {tokens:,} | ¥{cost_val:.4f} | {model} | {tag} |")
        if cost_rows:
            lines.append("### 节点成本分布")
            lines.append("")
            lines.append("| 节点 | Token | 费用（¥） | 模型 | 来源 |")
            lines.append("|------|-------|----------|------|------|")
            lines.extend(cost_rows)
            lines.append("")

    lines.append("## 节点执行详情")
    lines.append("")

    status_icons = {
        'completed': 'PASS', 'failed': 'FAIL', 'skipped': 'SKIP',
        'pending': 'WAIT', 'running': 'RUN '
    }

    for aid, node in nodes.items():
        icon = status_icons.get(node['status'], '?')
        name = node.get('name', aid)
        role = node.get('role', '')

        lines.append(f"### [{aid}] {name}")
        lines.append("")
        lines.append("| 属性 | 值 |")
        lines.append("|------|------|")
        lines.append(f"| 状态 | **{icon}** - {node['status']} |")
        lines.append(f"| 角色 | {role} |")
        deps_str = ', '.join(node.get('depends_on', [])) or '无（首节点）'
        lines.append(f"| 依赖 | {deps_str} |")
        lines.append(f"| 开始时间 | {parse_time(node.get('started_at'))} |")
        lines.append(f"| 完成时间 | {parse_time(node.get('completed_at'))} |")
        lines.append(f"| 执行时长 | {calc_duration(node.get('started_at'), node.get('completed_at'))} |")
        lines.append(f"| 重试次数 | {node.get('retry_count', 0)} / {node.get('max_retry', 3)} |")
        lines.append(f"| 降级策略 | {node.get('fallback', 'abort')} |")
        lines.append(f"| 超时设置 | {node.get('timeout', 60)} 秒 |")

        cost = node.get('cost_data', {})
        if cost:
            lines.append(f"| Token 消耗 | {cost.get('tokens', 0):,} |")
            lines.append(f"| 费用（¥） | {cost.get('cost_rmb', 0):.4f} |")
            if cost.get('est', False):
                lines.append(f"| 成本来源 | ⚪ 估算 |")
            else:
                lines.append(f"| 成本来源 | 🔵 实测 |")

        lines.append("")

        if node.get('error'):
            lines.append("**错误信息：**")
            lines.append("```")
            lines.append(node['error'])
            lines.append("```")
            lines.append("")

        if node.get('output_data') and node['status'] in ('completed', 'skipped'):
            output_str = json.dumps(node['output_data'], ensure_ascii=False, indent=2)
            if len(output_str) > 2000:
                output_str = output_str[:2000] + "\n... (输出过长，已截断)"
            lines.append("**输出数据：**")
            lines.append("```json")
            lines.append(output_str)
            lines.append("```")
            lines.append("")

        lines.append("---")
        lines.append("")

    if data['failed'] > 0:
        lines.append("## 失败影响分析")
        lines.append("")
        for aid, node in nodes.items():
            if node['status'] == 'failed':
                affected = [oid for oid, onode in nodes.items() if aid in onode.get('depends_on', [])]
                if affected:
                    lines.append(f"- ❌ 节点 **[{aid}]** 失败，直接影响了下游节点：{', '.join(affected)}")
                else:
                    lines.append(f"- ❌ 节点 **[{aid}]** 失败，无直接下游节点受影响（末端节点）")
        lines.append("")

    lines.append("## 后续操作建议")
    lines.append("")
    if data['overall_status'] == 'completed':
        lines.append("- ✅ 流水线已全部成功完成。")
    elif data['overall_status'] == 'aborted':
        lines.append("- 🛑 流水线被中止，建议：")
        lines.append("  1. 查看上方失败节点的错误信息")
        lines.append("  2. 修复后运行断点续传：`python orchestrator.py resume <state.json> --force`")
    elif data['overall_status'] == 'running':
        lines.append("- 🔄 流水线正在执行中，继续运行：`python orchestrator.py step <state.json>`")
    else:
        lines.append(f"- 当前状态：{data['overall_status']}，运行 `python orchestrator.py status <state.json>` 查看详情")
    lines.append("")
    lines.append("---")
    lines.append(f"*本报告由多Agent协作编排引擎自动生成*")

    with open(output_path, 'w', encoding='utf-8') as f:
        f.write('\n'.join(lines))

    print(f"✅ 执行报告已生成：{output_path}")
    print(f"  流水线状态：{data['status_text']}")
    print(f"  节点统计：{data['completed']}成功 / {data['failed']}失败 / {data['skipped']}跳过 / {data['pending']}待执行")
    print(f"  总重试：{data['total_retries']} 次 | 总耗时：{data['total_duration']}")
    return output_path


def _generate_html_gantt(data, output_path):
    """生成 HTML 甘特图"""
    nodes = data['nodes']

    if not data['all_start'] or not data['all_end']:
        print("⚠️ 没有足够的时间数据生成甘特图")
        return None

    status_colors = {
        'completed': '#22c55e', 'failed': '#ef4444', 'skipped': '#eab308',
        'pending': '#9ca3af', 'running': '#3b82f6',
    }

    bar_rows = ''
    for aid, node in nodes.items():
        status = node.get('status', 'pending')
        color = status_colors.get(status, '#9ca3af')
        name = node.get('name', aid)
        started = node.get('started_at') or data['all_start']
        completed = node.get('completed_at') or data['all_end']

        try:
            s_dt = datetime.strptime(started, '%Y-%m-%dT%H:%M:%S')
            e_dt = datetime.strptime(completed, '%Y-%m-%dT%H:%M:%S')
            base_dt = datetime.strptime(data['all_start'], '%Y-%m-%dT%H:%M:%S')
            left_pct = max(0, ((s_dt - base_dt).total_seconds() / data['total_seconds']) * 100)
            width_pct = max(2, ((e_dt - s_dt).total_seconds() / data['total_seconds']) * 100)
        except (ValueError, TypeError):
            left_pct = 0
            width_pct = 50

        duration_str = calc_duration(started, completed)
        bar_rows += f'''
      <tr>
        <td class="node-name">{aid}<br><small>{name}</small></td>
        <td class="gantt-cell">
          <div class="gantt-bar" style="left:{left_pct:.1f}%;width:{width_pct:.1f}%;background:{color};" title="{aid}: {duration_str}">
            <span class="bar-label">{duration_str}</span>
          </div>
        </td>
      </tr>'''

    html = f'''<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<title>甘特图 - {data['pipeline_name']}</title>
<style>
* {{ margin: 0; padding: 0; box-sizing: border-box; }}
body {{ font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; background: #f8fafc; color: #1e293b; padding: 2rem; }}
.container {{ max-width: 1200px; margin: 0 auto; background: #fff; border-radius: 12px; box-shadow: 0 1px 3px rgba(0,0,0,.1); padding: 2rem; }}
h1 {{ margin-bottom: .5rem; }}
.subtitle {{ color: #64748b; margin-bottom: 1.5rem; }}
.legend {{ display: flex; flex-wrap: wrap; gap: 1rem; margin-bottom: 1.5rem; }}
.legend-item {{ display: flex; align-items: center; gap: .4rem; font-size: .875rem; }}
.legend-dot {{ width: 14px; height: 14px; border-radius: 3px; }}
table {{ width: 100%; border-collapse: collapse; }}
.node-name {{ width: 180px; padding: .75rem; vertical-align: top; font-weight: 500; border-bottom: 1px solid #e2e8f0; }}
.node-name small {{ color: #64748b; font-weight: 400; }}
.gantt-cell {{ position: relative; height: 36px; border-bottom: 1px solid #e2e8f0; padding: 4px 0; }}
.gantt-bar {{ position: absolute; height: 28px; border-radius: 4px; display: flex; align-items: center; justify-content: center; min-width: 40px; }}
.gantt-bar:hover {{ opacity: .85; }}
.bar-label {{ font-size: .75rem; color: #fff; font-weight: 600; white-space: nowrap; text-shadow: 0 1px 2px rgba(0,0,0,.3); }}
.footer {{ margin-top: 1.5rem; color: #64748b; font-size: .875rem; text-align: center; }}
</style>
</head>
<body>
<div class="container">
  <h1>📊 流水线甘特图</h1>
  <p class="subtitle">{data['pipeline_name']} | 总耗时 {calc_duration(data['all_start'], data['all_end'])}</p>
  <div class="legend">
    <div class="legend-item"><div class="legend-dot" style="background:#22c55e"></div>成功</div>
    <div class="legend-item"><div class="legend-dot" style="background:#ef4444"></div>失败</div>
    <div class="legend-item"><div class="legend-dot" style="background:#3b82f6"></div>执行中</div>
    <div class="legend-item"><div class="legend-dot" style="background:#eab308"></div>跳过</div>
    <div class="legend-item"><div class="legend-dot" style="background:#9ca3af"></div>待执行</div>
  </div>
  <table>
    <thead>
      <tr style="text-align:left;border-bottom:2px solid #cbd5e1;">
        <th style="padding:.5rem;width:180px;">节点</th>
        <th style="padding:.5rem;">时间轴</th>
      </tr>
    </thead>
    <tbody>
    {bar_rows}
    </tbody>
  </table>
  <p class="footer">生成时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} | 多Agent协作编排引擎 v5.2</p>
</div>
</body>
</html>'''

    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(html)
    print(f"✅ 甘特图已生成：{output_path}")
    return output_path


if __name__ == '__main__':
    if len(sys.argv) < 2 or sys.argv[1] in ('-h', '--help'):
        print("执行可视化生成器 - 多Agent协作编排引擎 v5.2")
        print("=" * 50)
        print("命令：")
        print("  python pipeline_reporter.py visualize <state.json> [--format md|html|both] [output]")
        print("  python pipeline_reporter.py report <state.json> [output.md]        （向后兼容）")
        print("  python pipeline_reporter.py gantt <state.json> [output.html]       （向后兼容）")
        sys.exit(0)

    cmd = sys.argv[1]
    args = sys.argv[2:]

    if cmd == 'visualize':
        fmt = 'both'
        output = None
        i = 0
        while i < len(args):
            if args[i] == '--format' and i + 1 < len(args):
                fmt = args[i + 1]
                i += 2
            else:
                output = args[i]
                i += 1
        state_path = args[0] if args else None
        if not state_path:
            print("错误：缺少 state.json 路径")
            sys.exit(1)
        generate_visualization(state_path, output, fmt)
    elif cmd == 'report':
        state_path = args[0]
        output_path = args[1] if len(args) > 1 else None
        generate_report(state_path, output_path)
    elif cmd == 'gantt':
        state_path = args[0]
        output_path = args[1] if len(args) > 1 else None
        generate_html_gantt(state_path, output_path)
    else:
        print(f"未知命令：{cmd}")
        sys.exit(1)

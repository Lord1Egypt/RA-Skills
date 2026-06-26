#!/usr/bin/env python3
"""
可视化工具：生成风险热力图、骗局网络拓扑图、资金流向图、决策树可视化
"""

import argparse
import json
import sys
from pathlib import Path

# 尝试导入matplotlib，如果失败则使用纯文本输出
try:
    import matplotlib.pyplot as plt
    import matplotlib.patches as mpatches
    from matplotlib.patches import FancyBboxPatch, FancyArrowPatch
    import networkx as nx
    HAS_MATPLOTLIB = True
except ImportError:
    HAS_MATPLOTLIB = False
    print("警告：matplotlib 未安装，将使用纯文本输出", file=sys.stderr)


def generate_risk_heatmap(data, output_file):
    """生成风险热力图"""
    if not HAS_MATPLOTLIB:
        # 纯文本输出
        print("\n风险热力图（纯文本模式）")
        print("=" * 60)
        for item in data:
            risk_score = item.get('risk_score', 0)
            risk_level = item.get('risk_level', 'unknown')
            name = item.get('name', 'unknown')

            if risk_level == 'critical':
                level_text = '[严重]'
            elif risk_level == 'high':
                level_text = '[高风险]'
            elif risk_level == 'moderate':
                level_text = '[中等]'
            else:
                level_text = '[低]'

            bar_length = int(risk_score / 2)
            bar = '█' * bar_length + '░' * (50 - bar_length)
            print(f"{name:20s} {level_text:8s} {bar} {risk_score:.1f}/100")
        print("=" * 60)
        return

    # matplotlib 可视化
    fig, ax = plt.subplots(figsize=(12, 8))

    names = [item.get('name', 'unknown') for item in data]
    scores = [item.get('risk_score', 0) for item in data]
    levels = [item.get('risk_level', 'unknown') for item in data]

    colors = []
    for level in levels:
        if level == 'critical':
            colors.append('#ff0000')
        elif level == 'high':
            colors.append('#ff6600')
        elif level == 'moderate':
            colors.append('#ffcc00')
        else:
            colors.append('#00cc00')

    y_pos = range(len(names))
    bars = ax.barh(y_pos, scores, color=colors)

    ax.set_yticks(y_pos)
    ax.set_yticklabels(names)
    ax.set_xlabel('风险评分', fontsize=12)
    ax.set_title('风险热力图', fontsize=14, fontweight='bold')

    # 添加数值标签
    for i, (bar, score) in enumerate(zip(bars, scores)):
        ax.text(score + 1, i, f'{score:.1f}', va='center', fontsize=10)

    # 添加图例
    legend_elements = [
        mpatches.Patch(color='#ff0000', label='严重 (Critical)'),
        mpatches.Patch(color='#ff6600', label='高风险 (High)'),
        mpatches.Patch(color='#ffcc00', label='中等 (Moderate)'),
        mpatches.Patch(color='#00cc00', label='低 (Low)')
    ]
    ax.legend(handles=legend_elements, loc='lower right')

    plt.tight_layout()
    plt.savefig(output_file, dpi=300, bbox_inches='tight')
    print(f"风险热力图已生成：{output_file}")


def generate_network_topology(data, output_file):
    """生成骗局网络拓扑图"""
    if not HAS_MATPLOTLIB or not HAS_MATPLOTLIB:
        # 纯文本输出
        print("\n骗局网络拓扑图（纯文本模式）")
        print("=" * 60)
        nodes = data.get('nodes', [])
        edges = data.get('edges', [])

        print("\n节点信息：")
        for i, node in enumerate(nodes):
            print(f"  {i+1}. {node.get('name', 'unknown')} ({node.get('type', 'unknown')})")

        print("\n连接关系：")
        for edge in edges:
            source = edge.get('source', '')
            target = edge.get('target', '')
            relation = edge.get('relation', '→')
            print(f"  {source} {relation} {target}")
        print("=" * 60)
        return

    # networkx + matplotlib 可视化
    G = nx.DiGraph()

    # 添加节点
    for node in data.get('nodes', []):
        G.add_node(node.get('name', 'unknown'),
                   node_type=node.get('type', 'unknown'))

    # 添加边
    for edge in data.get('edges', []):
        G.add_edge(edge.get('source', ''),
                   edge.get('target', ''),
                   relation=edge.get('relation', '→'))

    fig, ax = plt.subplots(figsize=(14, 10))

    # 根据节点类型设置颜色
    node_colors = []
    for node in G.nodes():
        node_type = G.nodes[node].get('node_type', 'unknown')
        if node_type == 'fund_source':
            node_colors.append('#66ff66')
        elif node_type == 'intermediary':
            node_colors.append('#ffcc00')
        elif node_type == 'victim':
            node_colors.append('#ff6666')
        else:
            node_colors.append('#cccccc')

    # 绘制图
    pos = nx.spring_layout(G, k=2, iterations=50)
    nx.draw(G, pos, ax=ax,
            with_labels=True,
            node_color=node_colors,
            node_size=3000,
            font_size=10,
            font_weight='bold',
            arrows=True,
            arrowsize=20,
            edge_color='#666666',
            width=2)

    # 添加边标签
    edge_labels = nx.get_edge_attributes(G, 'relation')
    nx.draw_networkx_edge_labels(G, pos, edge_labels, font_size=8)

    plt.title('骗局网络拓扑图', fontsize=16, fontweight='bold', pad=20)

    # 添加图例
    legend_elements = [
        mpatches.Patch(color='#66ff66', label='资金来源'),
        mpatches.Patch(color='#ffcc00', label='中间人'),
        mpatches.Patch(color='#ff6666', label='受害者'),
    ]
    ax.legend(handles=legend_elements, loc='upper right')

    plt.tight_layout()
    plt.savefig(output_file, dpi=300, bbox_inches='tight')
    print(f"网络拓扑图已生成：{output_file}")


def generate_fund_flow(data, output_file):
    """生成资金流向图"""
    if not HAS_MATPLOTLIB:
        # 纯文本输出
        print("\n资金流向图（纯文本模式）")
        print("=" * 60)
        flows = data.get('flows', [])

        total_amount = sum(f.get('amount', 0) for f in flows)

        for i, flow in enumerate(flows):
            source = flow.get('source', 'unknown')
            target = flow.get('target', 'unknown')
            amount = flow.get('amount', 0)
            percentage = (amount / total_amount * 100) if total_amount > 0 else 0

            bar_length = int(percentage / 2)
            bar = '█' * bar_length + '░' * (50 - bar_length)
            print(f"{source} → {target}")
            print(f"  金额: {amount:,.0f} | 占比: {percentage:.1f}%")
            print(f"  {bar}")
            print()
        print(f"总资金: {total_amount:,.0f}")
        print("=" * 60)
        return

    # matplotlib 可视化
    fig, ax = plt.subplots(figsize=(12, 10))

    flows = data.get('flows', [])
    sources = [f.get('source', 'unknown') for f in flows]
    targets = [f.get('target', 'unknown') for f in flows]
    amounts = [f.get('amount', 0) for f in flows]

    # 创建桑基图效果
    y_positions = range(len(flows))

    for i, (source, target, amount) in enumerate(zip(sources, targets, amounts)):
        # 绘制来源节点
        ax.text(0.1, y_positions[i], source, ha='right', va='center', fontsize=10, fontweight='bold')
        ax.scatter(0.15, y_positions[i], s=200, c='#66ff66', zorder=3)

        # 绘制目标节点
        ax.text(0.9, y_positions[i], target, ha='left', va='center', fontsize=10, fontweight='bold')
        ax.scatter(0.85, y_positions[i], s=200, c='#ff6666', zorder=3)

        # 绘制连接线
        width = max(1, amount / max(amounts) * 50)
        ax.annotate('', xy=(0.84, y_positions[i]), xytext=(0.16, y_positions[i]),
                   arrowprops=dict(arrowstyle='->', lw=width, color='#666666'))

        # 绘制金额标签
        ax.text(0.5, y_positions[i], f'{amount:,.0f}', ha='center', va='center',
               fontsize=9, bbox=dict(boxstyle='round,pad=0.3', facecolor='wheat', alpha=0.5))

    ax.set_xlim(0, 1)
    ax.set_ylim(-1, len(flows))
    ax.axis('off')
    ax.set_title('资金流向图', fontsize=16, fontweight='bold', pad=20)

    plt.tight_layout()
    plt.savefig(output_file, dpi=300, bbox_inches='tight')
    print(f"资金流向图已生成：{output_file}")


def generate_decision_tree(data, output_file):
    """生成决策树可视化"""
    if not HAS_MATPLOTLIB:
        # 纯文本输出
        print("\n决策树（纯文本模式）")
        print("=" * 60)

        def print_tree(node, level=0):
            indent = "  " * level
            node_type = node.get('type', 'unknown')
            question = node.get('question', '')
            condition = node.get('condition', '')
            action = node.get('action', '')

            if node_type == 'decision':
                print(f"{indent}┌─ 决策点: {question}")
                print(f"{indent}├─ 条件: {condition}")
            elif node_type == 'action':
                print(f"{indent}└─ 行动: {action}")
            else:
                print(f"{indent}├─ 节点: {node_type}")

            children = node.get('children', [])
            for child in children:
                print_tree(child, level + 1)

        print_tree(data)
        print("=" * 60)
        return

    # matplotlib 可视化
    fig, ax = plt.subplots(figsize=(14, 10))

    def draw_node(node, x, y, level, horizontal_spacing=0.3, vertical_spacing=0.15):
        """递归绘制决策树"""
        node_type = node.get('type', 'unknown')
        question = node.get('question', '')
        action = node.get('action', '')
        condition = node.get('condition', '')

        # 绘制节点
        if node_type == 'decision':
            box = FancyBboxPatch((x - 0.12, y - 0.05), 0.24, 0.1,
                                 boxstyle="round,pad=0.02", facecolor='#ffcc00', edgecolor='black', linewidth=2)
            ax.add_patch(box)
            ax.text(x, y, question[:10] + '...' if len(question) > 10 else question,
                   ha='center', va='center', fontsize=8, fontweight='bold')
        elif node_type == 'action':
            box = FancyBboxPatch((x - 0.12, y - 0.05), 0.24, 0.1,
                                 boxstyle="round,pad=0.02", facecolor='#66ff66', edgecolor='black', linewidth=2)
            ax.add_patch(box)
            ax.text(x, y, action[:10] + '...' if len(action) > 10 else action,
                   ha='center', va='center', fontsize=8, fontweight='bold')
        else:
            circle = plt.Circle((x, y), 0.05, facecolor='#cccccc', edgecolor='black', linewidth=2)
            ax.add_patch(circle)

        # 绘制子节点
        children = node.get('children', [])
        if children:
            child_y = y - vertical_spacing
            for i, child in enumerate(children):
                child_x = x + (i - len(children) / 2 + 0.5) * horizontal_spacing

                # 绘制连接线
                arrow = FancyArrowPatch((x, y - 0.05), (child_x, child_y + 0.05),
                                       arrowstyle='->', mutation_scale=20, linewidth=1.5)
                ax.add_patch(arrow)

                # 递归绘制子节点
                draw_node(child, child_x, child_y, level + 1, horizontal_spacing * 0.7, vertical_spacing)

    # 计算树的初始位置
    draw_node(data, 0.5, 0.9, 0)

    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis('off')
    ax.set_title('决策树可视化', fontsize=16, fontweight='bold', pad=20)

    plt.tight_layout()
    plt.savefig(output_file, dpi=300, bbox_inches='tight')
    print(f"决策树可视化已生成：{output_file}")


def main():
    parser = argparse.ArgumentParser(description='骗局洞察可视化工具')
    parser.add_argument('--type', required=True, choices=['heatmap', 'network', 'flow', 'tree'],
                       help='可视化类型')
    parser.add_argument('--data', required=True, help='数据（JSON格式或文件路径）')
    parser.add_argument('--output', required=True, help='输出文件路径')

    args = parser.parse_args()

    # 读取数据
    try:
        if Path(args.data).exists():
            with open(args.data, 'r', encoding='utf-8') as f:
                data = json.load(f)
        else:
            data = json.loads(args.data)
    except Exception as e:
        print(f"错误：无法读取数据 - {e}", file=sys.stderr)
        sys.exit(1)

    # 生成可视化
    try:
        if args.type == 'heatmap':
            generate_risk_heatmap(data, args.output)
        elif args.type == 'network':
            generate_network_topology(data, args.output)
        elif args.type == 'flow':
            generate_fund_flow(data, args.output)
        elif args.type == 'tree':
            generate_decision_tree(data, args.output)

        # 返回JSON结果
        result = {
            "status": "success",
            "type": args.type,
            "output_file": args.output,
            "visualization_mode": "matplotlib" if HAS_MATPLOTLIB else "text"
        }
        print(json.dumps(result, ensure_ascii=False, indent=2))

    except Exception as e:
        print(f"错误：生成可视化失败 - {e}", file=sys.stderr)
        result = {
            "status": "error",
            "message": str(e)
        }
        print(json.dumps(result, ensure_ascii=False, indent=2))
        sys.exit(1)


if __name__ == "__main__":
    main()

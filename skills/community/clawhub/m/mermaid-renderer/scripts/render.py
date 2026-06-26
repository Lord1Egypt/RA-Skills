#!/usr/bin/env python3.11
"""
Mermaid 图表渲染脚本
支持两种输出模式：
1. 终端 ASCII 输出（使用 termaid）
2. 图片导出（使用 matplotlib）
"""

import sys
import subprocess
import tempfile
import os
import re

def render_terminal(mermaid_code: str) -> str:
    """使用 termaid 渲染为终端 ASCII"""
    result = subprocess.run(
        ['python3.11', '-m', 'termaid'],
        input=mermaid_code,
        capture_output=True,
        text=True
    )
    if result.returncode != 0:
        raise RuntimeError(f"termaid 渲染失败: {result.stderr}")
    return result.stdout

def render_image(mermaid_code: str, output_path: str) -> str:
    """使用 matplotlib 渲染为图片"""
    # 解析图表类型
    chart_type = parse_chart_type(mermaid_code)

    if chart_type == 'sequenceDiagram':
        return render_sequence_diagram(mermaid_code, output_path)
    elif chart_type == 'graph' or chart_type == 'flowchart':
        return render_flowchart(mermaid_code, output_path)
    elif chart_type == 'pie':
        return render_pie_chart(mermaid_code, output_path)
    elif chart_type == 'classDiagram':
        return render_class_diagram(mermaid_code, output_path)
    elif chart_type == 'gitGraph':
        return render_git_graph(mermaid_code, output_path)
    elif chart_type == 'stateDiagram':
        return render_state_diagram(mermaid_code, output_path)
    elif chart_type == 'erDiagram':
        return render_er_diagram(mermaid_code, output_path)
    else:
        raise ValueError(f"暂不支持图表类型: {chart_type}")

def parse_chart_type(mermaid_code: str) -> str:
    """解析 Mermaid 图表类型"""
    first_line = mermaid_code.strip().split('\n')[0].strip()
    if first_line.startswith('sequenceDiagram'):
        return 'sequenceDiagram'
    elif first_line.startswith('graph') or first_line.startswith('flowchart'):
        return 'graph'
    elif first_line.startswith('pie'):
        return 'pie'
    elif first_line.startswith('classDiagram'):
        return 'classDiagram'
    elif first_line.startswith('gitGraph'):
        return 'gitGraph'
    elif first_line.startswith('stateDiagram'):
        return 'stateDiagram'
    elif first_line.startswith('erDiagram'):
        return 'erDiagram'
    return 'unknown'

def parse_sequence_diagram(mermaid_code: str):
    """解析时序图"""
    participants = []
    messages = []

    for line in mermaid_code.split('\n'):
        line = line.strip()
        if line.startswith('participant '):
            name = line.replace('participant ', '').strip()
            participants.append(name)
        elif '->>' in line or '-->>' in line:
            # 解析消息
            if '->>' in line:
                parts = line.split('->>')
                arrow_type = 'solid'
            else:
                parts = line.split('-->>')
                arrow_type = 'dashed'

            if len(parts) == 2:
                sender = parts[0].strip()
                receiver_msg = parts[1].split(':')
                receiver = receiver_msg[0].strip()
                msg = receiver_msg[1].strip() if len(receiver_msg) > 1 else ''
                messages.append({
                    'sender': sender,
                    'receiver': receiver,
                    'message': msg,
                    'type': arrow_type
                })

    return participants, messages

def render_sequence_diagram(mermaid_code: str, output_path: str) -> str:
    """渲染时序图为图片"""
    import matplotlib.pyplot as plt
    import matplotlib.patches as mpatches
    from matplotlib.patches import FancyBboxPatch
    import matplotlib

    matplotlib.rcParams['font.sans-serif'] = ['DejaVu Sans', 'SimHei', 'Noto Sans CJK SC', 'WenQuanYi Micro Hei']
    matplotlib.rcParams['axes.unicode_minus'] = False

    participants, messages = parse_sequence_diagram(mermaid_code)

    # 计算图片尺寸
    width = max(8, len(participants) * 3)
    height = max(5, len(messages) * 1.5 + 3)

    fig, ax = plt.subplots(figsize=(width, height))
    ax.set_xlim(0, width)
    ax.set_ylim(0, height)
    ax.axis('off')

    # 参与者位置
    n_participants = len(participants)
    x_positions = {}
    for i, name in enumerate(participants):
        x = (i + 1) * (width / (n_participants + 1))
        x_positions[name] = x

        # 绘制参与者方框
        rect = FancyBboxPatch(
            (x - 0.6, height - 1.5), 1.2, 0.6,
            boxstyle="round,pad=0.05",
            facecolor='#4A90D9',
            edgecolor='#2E5A8C',
            linewidth=2
        )
        ax.add_patch(rect)
        ax.text(x, height - 1.2, name, ha='center', va='center',
                fontsize=12, color='white', fontweight='bold')

        # 绘制生命线
        ax.plot([x, x], [height - 2, 1], 'k--', linewidth=1, alpha=0.5)

    # 绘制消息箭头
    y = height - 2.5
    colors = ['#E74C3C', '#27AE60', '#3498DB', '#9B59B6', '#F39C12']

    for i, msg in enumerate(messages):
        sender_x = x_positions.get(msg['sender'], 0)
        receiver_x = x_positions.get(msg['receiver'], 0)

        if sender_x == receiver_x:
            # 自调用
            continue

        color = colors[i % len(colors)]

        # 绘制箭头
        if sender_x < receiver_x:
            ax.annotate('',
                xy=(receiver_x, y),
                xytext=(sender_x, y),
                arrowprops=dict(arrowstyle='->', color=color, lw=2,
                              linestyle='-' if msg['type'] == 'solid' else '--'))
            # 消息标签
            if msg['message']:
                ax.text((sender_x + receiver_x) / 2, y + 0.2, msg['message'],
                       ha='center', va='bottom', fontsize=10, color=color)
        else:
            ax.annotate('',
                xy=(receiver_x, y),
                xytext=(sender_x, y),
                arrowprops=dict(arrowstyle='<-', color=color, lw=2,
                              linestyle='-' if msg['type'] == 'solid' else '--'))
            if msg['message']:
                ax.text((sender_x + receiver_x) / 2, y + 0.2, msg['message'],
                       ha='center', va='bottom', fontsize=10, color=color)

        y -= 1.5

    plt.tight_layout()
    plt.savefig(output_path, dpi=150, bbox_inches='tight',
                facecolor='white', edgecolor='none')
    plt.close()

    return output_path

def parse_flowchart(mermaid_code: str):
    """解析流程图"""
    nodes = {}  # id -> {label, shape}
    edges = []  # [(from_id, to_id, label)]

    # 解析方向
    direction = 'LR'
    first_line = mermaid_code.strip().split('\n')[0].strip()
    if 'TB' in first_line or 'TD' in first_line:
        direction = 'TB'
    elif 'BT' in first_line:
        direction = 'BT'
    elif 'RL' in first_line:
        direction = 'RL'

    for line in mermaid_code.split('\n')[1:]:
        line = line.strip()
        if not line or line.startswith('%%'):
            continue

        # 解析节点定义和边
        # 节点形状: A[矩形], B(圆角), C((圆形)), D{菱形}, E[[子程序]]
        node_patterns = [
            (r'(\w+)\[([^\]]+)\]', 'rect'),           # 矩形
            (r'(\w+)\(([^)]+)\)', 'roundrect'),       # 圆角矩形
            (r'(\w+)\(\(([^)]+)\)\)', 'circle'),      # 圆形
            (r'(\w+)\{([^}]+)\}', 'diamond'),         # 菱形
            (r'(\w+)\[\[([^\]]+)\]\]', 'subroutine'), # 子程序
        ]

        # 先尝试解析节点
        for pattern, shape in node_patterns:
            matches = re.findall(pattern, line)
            for match in matches:
                nodes[match[0]] = {'label': match[1], 'shape': shape}

        # 简单节点（无形状定义）
        simple_nodes = re.findall(r'\b([A-Za-z_]\w*)\b', line)
        for node_id in simple_nodes:
            if node_id not in ['graph', 'flowchart', 'TB', 'TD', 'BT', 'LR', 'RL', 'subgraph', 'end']:
                if node_id not in nodes:
                    nodes[node_id] = {'label': node_id, 'shape': 'rect'}

        # 解析边
        edge_patterns = [
            (r'(\w+)\s*-->\|([^|]+)\|\s*(\w+)', 'solid'),   # A -->|label| B
            (r'(\w+)\s*-->\s*(\w+)', 'solid'),              # A --> B
            (r'(\w+)\s*---\|([^|]+)\|\s*(\w+)', 'none'),    # A ---|label| B
            (r'(\w+)\s*---\s*(\w+)', 'none'),               # A --- B
            (r'(\w+)\s*-\.->\|([^|]+)\|\s*(\w+)', 'dashed'), # A -.->|label| B
            (r'(\w+)\s*-\.->\s*(\w+)', 'dashed'),           # A -.-> B
            (r'(\w+)\s*==>\|([^|]+)\|\s*(\w+)', 'thick'),   # A ==>|label| B
            (r'(\w+)\s*==>\s*(\w+)', 'thick'),              # A ==> B
        ]

        for pattern, style in edge_patterns:
            matches = re.findall(pattern, line)
            for match in matches:
                if len(match) == 3:
                    edges.append((match[0], match[2], match[1], style))
                elif len(match) == 2:
                    edges.append((match[0], match[1], '', style))

    return direction, nodes, edges

def render_flowchart(mermaid_code: str, output_path: str) -> str:
    """渲染流程图为图片"""
    import matplotlib.pyplot as plt
    import matplotlib
    from matplotlib.patches import FancyBboxPatch, Circle, RegularPolygon
    import numpy as np

    matplotlib.rcParams['font.sans-serif'] = ['DejaVu Sans', 'SimHei', 'Noto Sans CJK SC']
    matplotlib.rcParams['axes.unicode_minus'] = False

    direction, nodes, edges = parse_flowchart(mermaid_code)

    if not nodes:
        raise ValueError("未找到流程图节点")

    # 布局计算
    node_list = list(nodes.keys())
    n_nodes = len(node_list)

    # 简单网格布局
    cols = int(np.ceil(np.sqrt(n_nodes)))
    rows = int(np.ceil(n_nodes / cols))

    # 根据方向调整
    if direction in ['TB', 'BT']:
        cols, rows = rows, cols

    width = max(10, cols * 2.5)
    height = max(8, rows * 2)

    fig, ax = plt.subplots(figsize=(width, height))
    ax.set_xlim(0, width)
    ax.set_ylim(0, height)
    ax.axis('off')

    # 计算节点位置
    positions = {}
    for i, node_id in enumerate(node_list):
        if direction in ['LR', 'RL']:
            col = i // rows
            row = i % rows
        else:
            col = i % cols
            row = i // cols

        x = (col + 1) * (width / (cols + 1))
        y = height - (row + 1) * (height / (rows + 1))

        if direction == 'RL':
            x = width - x
        if direction == 'BT':
            y = height - y

        positions[node_id] = (x, y)

    # 绘制边
    arrow_colors = {'solid': '#333', 'dashed': '#666', 'thick': '#333', 'none': '#333'}
    for from_id, to_id, label, style in edges:
        if from_id not in positions or to_id not in positions:
            continue

        x1, y1 = positions[from_id]
        x2, y2 = positions[to_id]

        linestyle = '-' if style != 'dashed' else '--'
        linewidth = 3 if style == 'thick' else 1.5

        # 计算箭头起止点（避开节点）
        dx, dy = x2 - x1, y2 - y1
        dist = np.sqrt(dx**2 + dy**2)
        if dist > 0:
            offset = 0.6
            x1_adj = x1 + offset * dx / dist
            y1_adj = y1 + offset * dy / dist
            x2_adj = x2 - offset * dx / dist
            y2_adj = y2 - offset * dy / dist
        else:
            x1_adj, y1_adj = x1, y1
            x2_adj, y2_adj = x2, y2

        if style != 'none':
            ax.annotate('',
                xy=(x2_adj, y2_adj),
                xytext=(x1_adj, y1_adj),
                arrowprops=dict(arrowstyle='->', color=arrow_colors.get(style, '#333'),
                              lw=linewidth, linestyle=linestyle))
        else:
            ax.plot([x1_adj, x2_adj], [y1_adj, y2_adj],
                   color=arrow_colors.get(style, '#333'), lw=linewidth)

        # 标签
        if label:
            mid_x, mid_y = (x1 + x2) / 2, (y1 + y2) / 2
            ax.text(mid_x, mid_y + 0.15, label, ha='center', va='bottom',
                   fontsize=9, color='#555', bbox=dict(boxstyle='round,pad=0.2',
                   facecolor='white', edgecolor='none', alpha=0.8))

    # 绘制节点
    for node_id, (x, y) in positions.items():
        node = nodes[node_id]
        label = node['label']
        shape = node['shape']

        color_map = {
            'rect': ('#3498DB', '#2980B9'),
            'roundrect': ('#27AE60', '#1E8449'),
            'circle': ('#E74C3C', '#C0392B'),
            'diamond': ('#F39C12', '#D68910'),
            'subroutine': ('#9B59B6', '#7D3C98'),
        }
        fill_color, edge_color = color_map.get(shape, ('#3498DB', '#2980B9'))

        if shape == 'rect':
            rect = FancyBboxPatch((x - 0.5, y - 0.25), 1, 0.5,
                boxstyle="round,pad=0.02", facecolor=fill_color, edgecolor=edge_color, linewidth=2)
            ax.add_patch(rect)
            ax.text(x, y, label, ha='center', va='center', fontsize=10, color='white', fontweight='bold')
        elif shape == 'roundrect':
            rect = FancyBboxPatch((x - 0.5, y - 0.25), 1, 0.5,
                boxstyle="round,pad=0.1", facecolor=fill_color, edgecolor=edge_color, linewidth=2)
            ax.add_patch(rect)
            ax.text(x, y, label, ha='center', va='center', fontsize=10, color='white', fontweight='bold')
        elif shape == 'circle':
            circle = Circle((x, y), 0.4, facecolor=fill_color, edgecolor=edge_color, linewidth=2)
            ax.add_patch(circle)
            ax.text(x, y, label, ha='center', va='center', fontsize=9, color='white', fontweight='bold')
        elif shape == 'diamond':
            diamond = RegularPolygon((x, y), numVertices=4, radius=0.5,
                orientation=np.pi/4, facecolor=fill_color, edgecolor=edge_color, linewidth=2)
            ax.add_patch(diamond)
            ax.text(x, y, label, ha='center', va='center', fontsize=9, color='white', fontweight='bold')
        elif shape == 'subroutine':
            rect = FancyBboxPatch((x - 0.5, y - 0.3), 1, 0.6,
                boxstyle="round,pad=0.02", facecolor=fill_color, edgecolor=edge_color, linewidth=2)
            ax.add_patch(rect)
            ax.plot([x - 0.5, x - 0.5], [y - 0.15, y + 0.15], color='white', lw=1.5)
            ax.plot([x + 0.5, x + 0.5], [y - 0.15, y + 0.15], color='white', lw=1.5)
            ax.text(x, y, label, ha='center', va='center', fontsize=10, color='white', fontweight='bold')
        else:
            rect = FancyBboxPatch((x - 0.5, y - 0.25), 1, 0.5,
                boxstyle="round,pad=0.02", facecolor=fill_color, edgecolor=edge_color, linewidth=2)
            ax.add_patch(rect)
            ax.text(x, y, label, ha='center', va='center', fontsize=10, color='white', fontweight='bold')

    plt.tight_layout()
    plt.savefig(output_path, dpi=150, bbox_inches='tight', facecolor='white', edgecolor='none')
    plt.close()

    return output_path

def render_pie_chart(mermaid_code: str, output_path: str) -> str:
    """渲染饼图为图片"""
    import matplotlib.pyplot as plt
    import matplotlib

    matplotlib.rcParams['font.sans-serif'] = ['DejaVu Sans', 'SimHei', 'Noto Sans CJK SC']
    matplotlib.rcParams['axes.unicode_minus'] = False

    # 解析饼图数据
    lines = mermaid_code.split('\n')
    title = ''
    data = []

    for line in lines:
        line = line.strip()
        if line.startswith('pie title'):
            title = line.replace('pie title', '').strip()
        elif line.startswith('"'):
            # 解析 "label" : value 格式（支持冒号前后有空格或无空格）
            match = re.match(r'"([^"]+)"\s*:\s*(\d+(?:\.\d+)?)', line)
            if match:
                data.append((match.group(1), float(match.group(2))))

    if not data:
        raise ValueError("无法解析饼图数据")

    # 绘制饼图
    labels, values = zip(*data)

    fig, ax = plt.subplots(figsize=(8, 8))
    colors = ['#E74C3C', '#3498DB', '#27AE60', '#F39C12', '#9B59B6', '#1ABC9C']

    wedges, texts, autotexts = ax.pie(
        values,
        labels=labels,
        autopct='%1.1f%%',
        colors=colors[:len(data)],
        startangle=90
    )

    if title:
        ax.set_title(title, fontsize=14, fontweight='bold')

    plt.tight_layout()
    plt.savefig(output_path, dpi=150, bbox_inches='tight',
                facecolor='white', edgecolor='none')
    plt.close()

    return output_path

def parse_class_diagram(mermaid_code: str):
    """解析类图"""
    classes = {}  # name -> {attributes, methods}
    relationships = []  # [(from, to, type, label)]

    current_class = None

    for line in mermaid_code.split('\n'):
        line = line.strip()
        if not line or line.startswith('%%'):
            continue

        # 解析类定义
        class_match = re.match(r'class\s+(\w+)\s*\{?', line)
        if class_match:
            current_class = class_match.group(1)
            classes[current_class] = {'attributes': [], 'methods': []}
            if '{' not in line:
                continue

        # 解析类成员
        if current_class and current_class in line:
            continue

        if current_class:
            # 属性: +name : String
            attr_match = re.match(r'([+#\-~]?)\s*(\w+)\s*:\s*(\w+)', line)
            if attr_match:
                visibility, name, type_name = attr_match.groups()
                vis_symbol = {'+': 'public', '-': 'private', '#': 'protected', '~': 'package'}
                classes[current_class]['attributes'].append({
                    'visibility': vis_symbol.get(visibility, 'public'),
                    'name': name,
                    'type': type_name
                })
                continue

            # 方法: +methodName()
            method_match = re.match(r'([+#\-~]?)\s*(\w+)\s*\([^)]*\)', line)
            if method_match:
                visibility, name = method_match.groups()
                vis_symbol = {'+': 'public', '-': 'private', '#': 'protected', '~': 'package'}
                classes[current_class]['methods'].append({
                    'visibility': vis_symbol.get(visibility, 'public'),
                    'name': name
                })
                continue

            if line == '}':
                current_class = None
                continue

        # 解析关系
        # Animal <|-- Dog : 继承
        # User *-- Order : 组合
        rel_patterns = [
            (r'(\w+)\s*<\|--\s*(\w+)\s*(?::\s*(.+))?', 'inheritance'),
            (r'(\w+)\s*\*--\s*(\w+)\s*(?::\s*(.+))?', 'composition'),
            (r'(\w+)\s*o--\s*(\w+)\s*(?::\s*(.+))?', 'aggregation'),
            (r'(\w+)\s*-->\s*(\w+)\s*(?::\s*(.+))?', 'association'),
            (r'(\w+)\s*--\s*(\w+)\s*(?::\s*(.+))?', 'link'),
            (r'(\w+)\s*\.\.>\s*(\w+)\s*(?::\s*(.+))?', 'dependency'),
            (r'(\w+)\s*\.\.\|>\s*(\w+)\s*(?::\s*(.+))?', 'realization'),
        ]

        for pattern, rel_type in rel_patterns:
            match = re.match(pattern, line)
            if match:
                from_class, to_class, label = match.groups()
                relationships.append((from_class, to_class, rel_type, label or ''))
                break

    return classes, relationships

def render_class_diagram(mermaid_code: str, output_path: str) -> str:
    """渲染类图为图片"""
    import matplotlib.pyplot as plt
    import matplotlib
    from matplotlib.patches import FancyBboxPatch
    import numpy as np

    matplotlib.rcParams['font.sans-serif'] = ['DejaVu Sans', 'SimHei', 'Noto Sans CJK SC']
    matplotlib.rcParams['axes.unicode_minus'] = False

    classes, relationships = parse_class_diagram(mermaid_code)

    if not classes:
        raise ValueError("未找到类定义")

    # 布局计算
    class_list = list(classes.keys())
    n_classes = len(class_list)

    # 计算每个类的框高度
    max_height = 0
    for cls_name, cls_data in classes.items():
        n_attrs = len(cls_data['attributes'])
        n_methods = len(cls_data['methods'])
        height = 1.2 + n_attrs * 0.3 + n_methods * 0.3
        max_height = max(max_height, height)

    cols = int(np.ceil(np.sqrt(n_classes)))
    rows = int(np.ceil(n_classes / cols))

    width = max(12, cols * 4)
    height = max(10, rows * max_height * 1.5)

    fig, ax = plt.subplots(figsize=(width, height))
    ax.set_xlim(0, width)
    ax.set_ylim(0, height)
    ax.axis('off')

    # 计算类位置
    positions = {}
    box_width = 2.5
    for i, cls_name in enumerate(class_list):
        col = i % cols
        row = i // cols

        x = (col + 1) * (width / (cols + 1))
        y = height - (row + 1) * (height / (rows + 1)) - max_height / 2

        positions[cls_name] = (x, y)

    # 绘制关系线
    rel_colors = {
        'inheritance': '#E74C3C',
        'composition': '#9B59B6',
        'aggregation': '#3498DB',
        'association': '#27AE60',
        'link': '#7F8C8D',
        'dependency': '#F39C12',
        'realization': '#1ABC9C',
    }

    for from_cls, to_cls, rel_type, label in relationships:
        if from_cls not in positions or to_cls not in positions:
            continue

        x1, y1 = positions[from_cls]
        x2, y2 = positions[to_cls]

        color = rel_colors.get(rel_type, '#333')
        linestyle = '--' if rel_type in ['dependency', 'realization'] else '-'

        ax.annotate('',
            xy=(x2, y2 + max_height/2),
            xytext=(x1, y1 - max_height/2),
            arrowprops=dict(arrowstyle='->' if rel_type != 'link' else '-',
                          color=color, lw=1.5, linestyle=linestyle))

        if label:
            mid_x, mid_y = (x1 + x2) / 2, (y1 + y2) / 2
            ax.text(mid_x + 0.1, mid_y, label, ha='left', va='center',
                   fontsize=8, color=color, style='italic')

    # 绘制类框
    for cls_name, (x, y) in positions.items():
        cls_data = classes[cls_name]
        n_attrs = len(cls_data['attributes'])
        n_methods = len(cls_data['methods'])

        # 计算框尺寸
        box_height = 1.2 + n_attrs * 0.3 + n_methods * 0.3

        # 类名区域
        name_rect = FancyBboxPatch((x - box_width/2, y + box_height/2 - 0.5),
            box_width, 0.5, boxstyle="round,pad=0.02",
            facecolor='#3498DB', edgecolor='#2980B9', linewidth=2)
        ax.add_patch(name_rect)
        ax.text(x, y + box_height/2 - 0.25, cls_name, ha='center', va='center',
               fontsize=11, color='white', fontweight='bold')

        # 属性区域
        attr_rect = FancyBboxPatch((x - box_width/2, y + box_height/2 - 0.5 - n_attrs * 0.3 - 0.1),
            box_width, n_attrs * 0.3 + 0.1, boxstyle="round,pad=0.02",
            facecolor='#ECF0F1', edgecolor='#BDC3C7', linewidth=1)
        ax.add_patch(attr_rect)

        for i, attr in enumerate(cls_data['attributes']):
            vis_prefix = {'public': '+', 'private': '-', 'protected': '#', 'package': '~'}
            text = f"{vis_prefix.get(attr['visibility'], '+')} {attr['name']}: {attr['type']}"
            ax.text(x - box_width/2 + 0.1, y + box_height/2 - 0.6 - i * 0.3,
                   text, ha='left', va='center', fontsize=8, color='#2C3E50')

        # 方法区域
        method_y = y + box_height/2 - 0.5 - n_attrs * 0.3 - 0.1 - n_methods * 0.3 - 0.1
        method_rect = FancyBboxPatch((x - box_width/2, method_y),
            box_width, n_methods * 0.3 + 0.1, boxstyle="round,pad=0.02",
            facecolor='#FDFEFE', edgecolor='#BDC3C7', linewidth=1)
        ax.add_patch(method_rect)

        for i, method in enumerate(cls_data['methods']):
            vis_prefix = {'public': '+', 'private': '-', 'protected': '#', 'package': '~'}
            text = f"{vis_prefix.get(method['visibility'], '+')} {method['name']}()"
            ax.text(x - box_width/2 + 0.1, method_y + n_methods * 0.3 - i * 0.3,
                   text, ha='left', va='center', fontsize=8, color='#2C3E50')

    plt.tight_layout()
    plt.savefig(output_path, dpi=150, bbox_inches='tight', facecolor='white', edgecolor='none')
    plt.close()

    return output_path

def parse_git_graph(mermaid_code: str):
    """解析 Git 分支图"""
    commits = []  # [(id, branch, message)]
    branches = {}  # branch_name -> list of commit_ids
    current_branch = 'main'
    branch_order = ['main']  # 分支顺序

    for line in mermaid_code.split('\n'):
        line = line.strip()
        if not line or line.startswith('%%'):
            continue

        # commit id: "message"
        commit_match = re.match(r'commit\s+id:\s*["\']?([^"\']+)["\']?', line)
        if commit_match:
            commit_id = commit_match.group(1)
            commits.append((commit_id, current_branch, commit_id))
            if current_branch not in branches:
                branches[current_branch] = []
            branches[current_branch].append(commit_id)
            continue

        # branch name
        branch_match = re.match(r'branch\s+(\w+)', line)
        if branch_match:
            branch_name = branch_match.group(1)
            if branch_name not in branch_order:
                branch_order.append(branch_name)
            continue

        # checkout branch
        checkout_match = re.match(r'checkout\s+(\w+)', line)
        if checkout_match:
            current_branch = checkout_match.group(1)
            if current_branch not in branches:
                branches[current_branch] = []
            continue

        # merge branch
        merge_match = re.match(r'merge\s+(\w+)\s+id:\s*["\']?([^"\']+)["\']?', line)
        if merge_match:
            source_branch = merge_match.group(1)
            merge_commit_id = merge_match.group(2)
            commits.append((merge_commit_id, current_branch, f'merge {source_branch}'))
            if current_branch not in branches:
                branches[current_branch] = []
            branches[current_branch].append(merge_commit_id)

        # cherry-pick
        cherry_match = re.match(r'cherry-pick\s+id:\s*["\']?([^"\']+)["\']?', line)
        if cherry_match:
            commit_id = cherry_match.group(1)
            commits.append((commit_id, current_branch, f'cherry-pick'))
            if current_branch not in branches:
                branches[current_branch] = []
            branches[current_branch].append(commit_id)

    return commits, branches, branch_order

def render_git_graph(mermaid_code: str, output_path: str) -> str:
    """渲染 Git 分支图为图片"""
    import matplotlib.pyplot as plt
    import matplotlib
    from matplotlib.patches import Circle, FancyArrowPatch
    import numpy as np

    matplotlib.rcParams['font.sans-serif'] = ['DejaVu Sans', 'SimHei', 'Noto Sans CJK SC']
    matplotlib.rcParams['axes.unicode_minus'] = False

    commits, branches, branch_order = parse_git_graph(mermaid_code)

    if not commits:
        raise ValueError("未找到 Git 提交记录")

    # 布局参数
    n_branches = len(branch_order)
    max_commits = max(len(c) for c in branches.values()) if branches else 1

    width = max(12, max_commits * 1.5)
    height = max(6, n_branches * 1.5)

    fig, ax = plt.subplots(figsize=(width, height))
    ax.set_xlim(0, width)
    ax.set_ylim(0, height)
    ax.axis('off')

    # 分支颜色
    branch_colors = ['#3498DB', '#E74C3C', '#27AE60', '#9B59B6', '#F39C12', '#1ABC9C']

    # 计算分支 Y 位置
    branch_y = {}
    for i, branch in enumerate(branch_order):
        branch_y[branch] = height - (i + 1) * (height / (n_branches + 1))

    # 绘制分支线
    for branch, y in branch_y.items():
        color = branch_colors[branch_order.index(branch) % len(branch_colors)]
        ax.plot([0.5, width - 0.5], [y, y], color=color, lw=3, alpha=0.7)
        ax.text(0.3, y, branch, ha='right', va='center', fontsize=11,
               fontweight='bold', color=color)

    # 计算提交位置
    commit_positions = {}
    commit_x_counter = {}

    for commit_id, branch, message in commits:
        if branch not in commit_x_counter:
            commit_x_counter[branch] = 1
        else:
            commit_x_counter[branch] += 1

        x = commit_x_counter[branch] * (width / (max_commits + 2))
        y = branch_y.get(branch, height / 2)

        commit_positions[commit_id] = (x, y, branch)

    # 绘制连接线
    prev_commit_in_branch = {}
    for commit_id, branch, message in commits:
        x, y, _ = commit_positions[commit_id]

        if branch in prev_commit_in_branch:
            prev_x, prev_y, _ = commit_positions[prev_commit_in_branch[branch]]
            color = branch_colors[branch_order.index(branch) % len(branch_colors)]
            ax.plot([prev_x, x], [prev_y, y], color=color, lw=2)

        prev_commit_in_branch[branch] = commit_id

    # 绘制合并线
    for commit_id, branch, message in commits:
        if message.startswith('merge '):
            source_branch = message.replace('merge ', '').strip()
            if source_branch in branch_y and source_branch in commit_x_counter:
                x, y, _ = commit_positions[commit_id]
                source_y = branch_y[source_branch]
                source_x = commit_x_counter[source_branch] * (width / (max_commits + 2))

                color = branch_colors[branch_order.index(source_branch) % len(branch_colors)]
                ax.plot([source_x, x], [source_y, y], color=color, lw=2, ls='--', alpha=0.7)

    # 绘制提交节点
    for commit_id, branch, message in commits:
        x, y, b = commit_positions[commit_id]
        color = branch_colors[branch_order.index(b) % len(branch_colors)]

        # 提交圆点
        circle = Circle((x, y), 0.2, facecolor=color, edgecolor='white', linewidth=2)
        ax.add_patch(circle)

        # 提交标签
        label = commit_id if len(commit_id) < 10 else commit_id[:8] + '...'
        ax.text(x, y - 0.35, label, ha='center', va='top', fontsize=8,
               color='#333', rotation=45)

    # 添加图例
    ax.text(width / 2, 0.3, 'Git Branch Graph', ha='center', va='center',
           fontsize=12, fontweight='bold', color='#333')

    plt.tight_layout()
    plt.savefig(output_path, dpi=150, bbox_inches='tight', facecolor='white', edgecolor='none')
    plt.close()

    return output_path

def parse_state_diagram(mermaid_code: str):
    """解析状态图"""
    states = {}  # state_name -> {type: 'normal'/'start'/'end'/'choice'/'fork'/'join'}
    transitions = []  # [(from_state, to_state, label)]

    for line in mermaid_code.split('\n'):
        line = line.strip()
        if not line or line.startswith('%%'):
            continue

        # 起始状态 [*]
        if line == '[*]':
            states['[*]'] = {'type': 'start'}
            continue

        # 结束状态 [*] -->
        if line.startswith('[*] -->'):
            match = re.match(r'\[\*\]\s*-->\s*(\w+)', line)
            if match:
                target = match.group(1)
                if target not in states:
                    states[target] = {'type': 'normal'}
                transitions.append(('[*]', target, ''))
            continue

        # 状态 --> [*]
        if '--> [*]' in line:
            match = re.match(r'(\w+)\s*-->\s*\[\*\]', line)
            if match:
                source = match.group(1)
                if source not in states:
                    states[source] = {'type': 'normal'}
                transitions.append((source, '[*]', ''))
            continue

        # 普通转换 state1 --> state2 : label
        trans_match = re.match(r'(\w+)\s*-->\s*(\w+)\s*(?::\s*(.+))?', line)
        if trans_match:
            from_state, to_state, label = trans_match.groups()
            if from_state not in states:
                states[from_state] = {'type': 'normal'}
            if to_state not in states:
                states[to_state] = {'type': 'normal'}
            transitions.append((from_state, to_state, label or ''))
            continue

        # 带括号的转换 state --> state2 : label (处理中)
        trans_match2 = re.match(r'(\w+)\s*-->\s*(\w+)\s*:\s*(.+)', line)
        if trans_match2:
            from_state, to_state, label = trans_match2.groups()
            if from_state not in states:
                states[from_state] = {'type': 'normal'}
            if to_state not in states:
                states[to_state] = {'type': 'normal'}
            transitions.append((from_state, to_state, label))

    return states, transitions

def render_state_diagram(mermaid_code: str, output_path: str) -> str:
    """渲染状态图为图片"""
    import matplotlib.pyplot as plt
    import matplotlib
    from matplotlib.patches import FancyBboxPatch, Circle, RegularPolygon
    import numpy as np

    matplotlib.rcParams['font.sans-serif'] = ['DejaVu Sans', 'SimHei', 'Noto Sans CJK SC']
    matplotlib.rcParams['axes.unicode_minus'] = False

    states, transitions = parse_state_diagram(mermaid_code)

    if not states:
        raise ValueError("未找到状态定义")

    # 布局计算 - 使用简单的层次布局
    state_list = list(states.keys())
    n_states = len(state_list)

    # 计算层次
    layers = {}
    layer_num = 0

    # 起始状态在第0层
    if '[*]' in states:
        layers['[*]'] = 0
        state_list.remove('[*]')

    # BFS 分层
    visited = set(layers.keys())
    queue = list(layers.keys())

    while queue:
        current = queue.pop(0)
        current_layer = layers[current]

        for from_state, to_state, label in transitions:
            if from_state == current and to_state not in visited:
                layers[to_state] = current_layer + 1
                visited.add(to_state)
                queue.append(to_state)

    # 未访问的状态放到最后一层
    max_layer = max(layers.values()) if layers else 0
    for state in state_list:
        if state not in layers:
            max_layer += 1
            layers[state] = max_layer

    # 按层分组
    layer_groups = {}
    for state, layer in layers.items():
        if layer not in layer_groups:
            layer_groups[layer] = []
        layer_groups[layer].append(state)

    n_layers = len(layer_groups)
    max_in_layer = max(len(g) for g in layer_groups.values())

    width = max(10, max_in_layer * 3)
    height = max(8, n_layers * 1.8)

    fig, ax = plt.subplots(figsize=(width, height))
    ax.set_xlim(0, width)
    ax.set_ylim(0, height)
    ax.axis('off')

    # 计算状态位置
    positions = {}
    for layer, states_in_layer in layer_groups.items():
        n_in_layer = len(states_in_layer)
        y = height - (layer + 1) * (height / (n_layers + 1))
        for i, state in enumerate(states_in_layer):
            x = (i + 1) * (width / (n_in_layer + 1))
            positions[state] = (x, y)

    # 绘制转换箭头
    for from_state, to_state, label in transitions:
        if from_state not in positions or to_state not in positions:
            continue

        x1, y1 = positions[from_state]
        x2, y2 = positions[to_state]

        # 调整起止点避开节点
        dx, dy = x2 - x1, y2 - y1
        dist = np.sqrt(dx**2 + dy**2)

        if dist > 0:
            offset = 0.5
            x1_adj = x1 + offset * dx / dist
            y1_adj = y1 + offset * dy / dist
            x2_adj = x2 - offset * dx / dist
            y2_adj = y2 - offset * dy / dist
        else:
            x1_adj, y1_adj = x1, y1
            x2_adj, y2_adj = x2, y2

        ax.annotate('',
            xy=(x2_adj, y2_adj),
            xytext=(x1_adj, y1_adj),
            arrowprops=dict(arrowstyle='->', color='#3498DB', lw=2))

        if label:
            mid_x, mid_y = (x1 + x2) / 2, (y1 + y2) / 2
            ax.text(mid_x, mid_y + 0.15, label, ha='center', va='bottom',
                   fontsize=9, color='#2C3E50',
                   bbox=dict(boxstyle='round,pad=0.2', facecolor='white',
                            edgecolor='none', alpha=0.9))

    # 绘制状态节点
    for state_name, (x, y) in positions.items():
        state_type = states[state_name].get('type', 'normal')

        if state_name == '[*]':
            # 起始状态 - 实心圆
            circle = Circle((x, y), 0.25, facecolor='#2C3E50', edgecolor='#2C3E50')
            ax.add_patch(circle)
        elif state_type == 'end':
            # 结束状态 - 双圆
            circle1 = Circle((x, y), 0.3, facecolor='white', edgecolor='#2C3E50', linewidth=2)
            circle2 = Circle((x, y), 0.2, facecolor='#2C3E50', edgecolor='#2C3E50')
            ax.add_patch(circle1)
            ax.add_patch(circle2)
        else:
            # 普通状态 - 圆角矩形
            rect = FancyBboxPatch((x - 0.7, y - 0.3), 1.4, 0.6,
                boxstyle="round,pad=0.1",
                facecolor='#E8F4FD', edgecolor='#3498DB', linewidth=2)
            ax.add_patch(rect)
            ax.text(x, y, state_name, ha='center', va='center',
                   fontsize=10, color='#2C3E50', fontweight='bold')

    # 添加标题
    ax.text(width / 2, 0.3, 'State Diagram', ha='center', va='center',
           fontsize=12, fontweight='bold', color='#333')

    plt.tight_layout()
    plt.savefig(output_path, dpi=150, bbox_inches='tight', facecolor='white', edgecolor='none')
    plt.close()

    return output_path

def parse_er_diagram(mermaid_code: str):
    """解析 ER 图"""
    entities = {}  # entity_name -> {attributes: [{name, type, pk, fk}]}
    relationships = []  # [(from, to, rel_type, label)]

    current_entity = None

    for line in mermaid_code.split('\n'):
        line = line.strip()
        if not line or line.startswith('%%'):
            continue

        # 解析实体定义
        entity_match = re.match(r'(\w+)\s*\{', line)
        if entity_match:
            current_entity = entity_match.group(1)
            entities[current_entity] = {'attributes': []}
            continue

        if current_entity:
            if line == '}':
                current_entity = None
                continue

            # 解析属性: int id PK
            attr_match = re.match(r'(\w+)\s+(\w+)(?:\s+(PK|FK))?', line)
            if attr_match:
                type_name, attr_name, constraint = attr_match.groups()
                entities[current_entity]['attributes'].append({
                    'name': attr_name,
                    'type': type_name,
                    'pk': constraint == 'PK',
                    'fk': constraint == 'FK'
                })
                continue

        # 解析关系
        # USER ||--o{ ORDER : places
        rel_patterns = [
            (r'(\w+)\s*\|\|--\{\|\s*(\w+)\s*(?::\s*(.+))?', 'one_to_many'),
            (r'(\w+)\s*\|\|--\|\|\s*(\w+)\s*(?::\s*(.+))?', 'one_to_one'),
            (r'(\w+)\s*\}\|--\{\|\s*(\w+)\s*(?::\s*(.+))?', 'many_to_many'),
            (r'(\w+)\s*\}\|--\|\|\s*(\w+)\s*(?::\s*(.+))?', 'many_to_one'),
            (r'(\w+)\s*\|\|..o\{\s*(\w+)\s*(?::\s*(.+))?', 'one_to_many_optional'),
            (r'(\w+)\s*\|\|..o\|\|\s*(\w+)\s*(?::\s*(.+))?', 'one_to_one_optional'),
        ]

        for pattern, rel_type in rel_patterns:
            match = re.match(pattern, line)
            if match:
                from_entity, to_entity, label = match.groups()
                relationships.append((from_entity, to_entity, rel_type, label or ''))
                break

    return entities, relationships

def render_er_diagram(mermaid_code: str, output_path: str) -> str:
    """渲染 ER 图为图片"""
    import matplotlib.pyplot as plt
    import matplotlib
    from matplotlib.patches import FancyBboxPatch
    import numpy as np

    matplotlib.rcParams['font.sans-serif'] = ['DejaVu Sans', 'SimHei', 'Noto Sans CJK SC']
    matplotlib.rcParams['axes.unicode_minus'] = False

    entities, relationships = parse_er_diagram(mermaid_code)

    if not entities:
        raise ValueError("未找到实体定义")

    # 布局计算
    entity_list = list(entities.keys())
    n_entities = len(entity_list)

    # 计算每个实体的框高度
    max_attrs = 0
    for entity_name, entity_data in entities.items():
        n_attrs = len(entity_data['attributes'])
        max_attrs = max(max_attrs, n_attrs)

    cols = int(np.ceil(np.sqrt(n_entities)))
    rows = int(np.ceil(n_entities / cols))

    box_width = 2.5
    box_height = 0.8 + max_attrs * 0.25

    width = max(12, cols * 4)
    height = max(10, rows * (box_height + 1))

    fig, ax = plt.subplots(figsize=(width, height))
    ax.set_xlim(0, width)
    ax.set_ylim(0, height)
    ax.axis('off')

    # 计算实体位置
    positions = {}
    for i, entity_name in enumerate(entity_list):
        col = i % cols
        row = i // cols

        x = (col + 1) * (width / (cols + 1))
        y = height - (row + 1) * (height / (rows + 1))

        positions[entity_name] = (x, y)

    # 绘制关系线
    rel_colors = {
        'one_to_many': '#3498DB',
        'one_to_one': '#27AE60',
        'many_to_many': '#9B59B6',
        'many_to_one': '#E74C3C',
        'one_to_many_optional': '#3498DB',
        'one_to_one_optional': '#27AE60',
    }

    for from_entity, to_entity, rel_type, label in relationships:
        if from_entity not in positions or to_entity not in positions:
            continue

        x1, y1 = positions[from_entity]
        x2, y2 = positions[to_entity]

        color = rel_colors.get(rel_type, '#333')
        linestyle = '--' if 'optional' in rel_type else '-'

        ax.plot([x1, x2], [y1, y2], color=color, lw=2, linestyle=linestyle, alpha=0.7)

        # 关系标签
        if label:
            mid_x, mid_y = (x1 + x2) / 2, (y1 + y2) / 2
            ax.text(mid_x, mid_y + 0.15, label, ha='center', va='bottom',
                   fontsize=8, color=color, style='italic',
                   bbox=dict(boxstyle='round,pad=0.2', facecolor='white',
                            edgecolor='none', alpha=0.9))

    # 绘制实体框
    for entity_name, (x, y) in positions.items():
        entity_data = entities[entity_name]
        n_attrs = len(entity_data['attributes'])

        current_box_height = 0.8 + n_attrs * 0.25

        # 实体名区域
        name_rect = FancyBboxPatch((x - box_width/2, y + current_box_height/2 - 0.4),
            box_width, 0.4, boxstyle="round,pad=0.02",
            facecolor='#9B59B6', edgecolor='#7D3C98', linewidth=2)
        ax.add_patch(name_rect)
        ax.text(x, y + current_box_height/2 - 0.2, entity_name, ha='center', va='center',
               fontsize=11, color='white', fontweight='bold')

        # 属性区域
        if n_attrs > 0:
            attr_rect = FancyBboxPatch((x - box_width/2, y - current_box_height/2),
                box_width, n_attrs * 0.25 + 0.1, boxstyle="round,pad=0.02",
                facecolor='#F5EEF8', edgecolor='#D2B4DE', linewidth=1)
            ax.add_patch(attr_rect)

            for i, attr in enumerate(entity_data['attributes']):
                prefix = ''
                if attr['pk']:
                    prefix = 'PK '
                elif attr['fk']:
                    prefix = 'FK '

                text = f"{prefix}{attr['name']}: {attr['type']}"
                text_y = y - current_box_height/2 + 0.15 + (n_attrs - 1 - i) * 0.25

                ax.text(x - box_width/2 + 0.1, text_y,
                       text, ha='left', va='center', fontsize=8, color='#2C3E50')

    # 添加标题
    ax.text(width / 2, 0.3, 'Entity Relationship Diagram', ha='center', va='center',
           fontsize=12, fontweight='bold', color='#333')

    plt.tight_layout()
    plt.savefig(output_path, dpi=150, bbox_inches='tight', facecolor='white', edgecolor='none')
    plt.close()

    return output_path

def main():
    if len(sys.argv) < 3:
        print("用法: python render.py <mermaid_code> <output_path> [--image]")
        print("  --image: 导出为图片，否则输出终端 ASCII")
        sys.exit(1)

    mermaid_code = sys.argv[1]
    output_path = sys.argv[2]
    mode = sys.argv[3] if len(sys.argv) > 3 else '--terminal'

    if mode == '--image':
        result = render_image(mermaid_code, output_path)
        print(f"图片已保存: {result}")
    else:
        result = render_terminal(mermaid_code)
        print(result)

if __name__ == '__main__':
    main()

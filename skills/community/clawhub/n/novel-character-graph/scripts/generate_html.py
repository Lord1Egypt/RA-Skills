#!/usr/bin/env python3
"""自动生成交互式人物关系图谱HTML"""

import os
import sys

TEMPLATE_PATH = os.path.join(os.path.dirname(__file__), '../assets/graph_template.html')

def generate_html(title, subtitle, characters, relationships, output_path='index.html'):
    """生成HTML图谱

    参数:
        title: 小说标题
        subtitle: 副标题
        characters: list of dict, 每个人物包含 name/identity/realm 等字段
        relationships: list of tuple, (人物A, 人物B, 关系类型)
        output_path: 输出HTML路径
    """

    with open(TEMPLATE_PATH, 'r', encoding='utf-8') as f:
        template = f.read()

    # 填充标题
    template = template.replace('{{TITLE}}', title)
    template = template.replace('{{SUBTITLE}}', subtitle)

    # 生成人物卡片HTML
    cards_html = ''
    for char in characters:
        cards_html += f'''
        <div class="character-card bg-gray-800/50 rounded-2xl p-6 border border-gray-700/50">
            <h3 class="text-xl font-bold text-orange-400 mb-2">{char['name']}</h3>
            <p class="text-gray-300 text-sm">{char.get('identity', '')}</p>
            <p class="text-gray-400 text-xs mt-2">修为：{char.get('realm', '未知')}</p>
        </div>
        '''

    # 生成关系图谱SVG
    graph_svg = generate_svg_graph(characters, relationships)

    # 替换占位符
    template = template.replace('<!-- CHARACTER_CARDS -->', cards_html)
    template = template.replace('<!-- CHARACTER_GRAPH_SVG -->', graph_svg)

    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(template)

    print(f"OK: {output_path}")
    return output_path


def generate_svg_graph(characters, relationships, width=1200, height=800):
    """生成SVG关系图

    参数:
        characters: 人物列表
        relationships: 关系列表 [(A, B, '类型'), ...]
    """
    # 简单的中心辐射布局
    svg_parts = [f'<svg viewBox="0 0 {width} {height}" class="w-full h-auto">']

    # 绘制连线
    relations_colors = {
        '爱情': '#ff6b9d',
        '师徒': '#c084fc',
        '兄弟': '#60a5fa',
        '血缘': '#fb923c',
        '敌对': '#ef4444',
        '从属': '#a3e635',
    }

    center_x, center_y = width // 2, height // 2
    radius = min(width, height) // 3

    for i, (a, b, rtype) in enumerate(relationships):
        # 简化处理：随机位置
        ax = center_x + (i * 137) % width
        ay = center_y + (i * 97) % height
        bx = center_x + ((i + 3) * 137) % width
        by = center_y + ((i + 3) * 97) % height
        color = relations_colors.get(rtype, '#94a3b8')

        svg_parts.append(
            f'<line x1="{ax}" y1="{ay}" x2="{bx}" y2="{by}" '
            f'stroke="{color}" stroke-width="2" stroke-dasharray="5,5" opacity="0.7"/>'
        )

    # 绘制人物节点
    for i, char in enumerate(characters[:20]):  # 最多20个
        x = center_x + (i * 137) % width
        y = center_y + (i * 97) % height
        svg_parts.append(
            f'<circle cx="{x}" cy="{y}" r="30" fill="#f97316" opacity="0.8"/>'
            f'<text x="{x}" y="{y+5}" text-anchor="middle" fill="white" font-size="12">'
            f'{char["name"][:4]}</text>'
        )

    svg_parts.append('</svg>')
    return '\n'.join(svg_parts)


if __name__ == "__main__":
    print("Usage: from generate_html import generate_html")
    print("       generate_html('小说名', '副标题', characters_list, relationships_list)")

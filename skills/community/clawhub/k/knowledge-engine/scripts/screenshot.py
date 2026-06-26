#!/usr/bin/env python3
"""
生成知识图谱静态截图（PNG）
用 matplotlib + networkx 替代 D3.js 交互版
"""
import json
import os
import sys

sys.path.insert(0, os.path.dirname(__file__))
from concept_manager import get_db

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np

def export_graph():
    conn = get_db()
    concepts = conn.execute(
        'SELECT id, concept, tags, confidence, status FROM concepts WHERE status="active"'
    ).fetchall()
    links = conn.execute('''
        SELECT cl.from_concept, cl.to_concept, cl.relation
        FROM concept_links cl
        JOIN concepts c1 ON c1.id = cl.from_concept
        JOIN concepts c2 ON c2.id = cl.to_concept
    ''').fetchall()
    conn.close()
    
    nodes = []
    for c in concepts:
        tags = json.loads(c['tags']) if isinstance(c['tags'], str) else c['tags']
        level = 'L3' if 'level:l3' in tags else ('L2' if 'level:l2' in tags else 'L1')
        clean_tags = [t for t in tags if not t.startswith('level:')]
        nodes.append({
            'id': c['id'],
            'label': c['concept'][:20],
            'tags': clean_tags,
            'confidence': c['confidence'],
            'level': level,
        })
    
    edges = []
    for l in links:
        edges.append((l['from_concept'], l['to_concept']))
    
    return nodes, edges

def draw_graph(nodes, edges, output_path):
    # Layout: force-directed manually
    np.random.seed(42)
    n = len(nodes)
    
    # Separate by level
    l1_nodes = [i for i, nd in enumerate(nodes) if nd['level'] == 'L1']
    l2_nodes = [i for i, nd in enumerate(nodes) if nd['level'] == 'L2']
    l3_nodes = [i for i, nd in enumerate(nodes) if nd['level'] == 'L3']
    
    pos = {}
    
    # L3 at top center
    for i, idx in enumerate(l3_nodes):
        pos[idx] = (0, 2.5)
    
    # L2 in middle row
    l2_count = len(l2_nodes)
    for i, idx in enumerate(l2_nodes):
        x = (i - (l2_count - 1) / 2) * 1.8
        pos[idx] = (x, 1.2)
    
    # L1 at bottom, spread out
    l1_count = len(l1_nodes)
    cols = min(l1_count, 5)
    rows = (l1_count + cols - 1) // cols
    for i, idx in enumerate(l1_nodes):
        row = i // cols
        col = i % cols
        x = (col - (cols - 1) / 2) * 2.0
        y = -row * 1.0 - 0.5
        pos[idx] = (x, y)
    
    # Add jitter to prevent overlap
    for idx in pos:
        if idx not in l3_nodes:
            pos[idx] = (pos[idx][0] + np.random.uniform(-0.2, 0.2),
                        pos[idx][1] + np.random.uniform(-0.1, 0.1))
    
    # Color map
    colors = {'L1': '#60a5fa', 'L2': '#a78bfa', 'L3': '#f59e0b'}
    sizes = {'L1': 300, 'L2': 600, 'L3': 900}
    confidence_alpha = {'high': 1.0, 'medium': 0.7, 'low': 0.45}
    
    # Setup figure
    fig, ax = plt.subplots(1, 1, figsize=(16, 10), facecolor='#0a0a1a')
    ax.set_facecolor('#0a0a1a')
    
    # Draw edges first
    id_to_idx = {nd['id']: i for i, nd in enumerate(nodes)}
    for src, tgt in edges:
        if src in id_to_idx and tgt in id_to_idx:
            si, ti = id_to_idx[src], id_to_idx[tgt]
            x_vals = [pos[si][0], pos[ti][0]]
            y_vals = [pos[si][1], pos[ti][1]]
            ax.plot(x_vals, y_vals, color='#333355', linewidth=1, alpha=0.6, zorder=1)
    
    # Draw nodes
    for i, nd in enumerate(nodes):
        x, y = pos[i]
        color = colors[nd['level']]
        size = sizes[nd['level']]
        alpha = confidence_alpha.get(nd['confidence'], 0.7)
        
        # Glow
        ax.scatter(x, y, s=size*2, c=color, alpha=0.1, zorder=2)
        # Main node
        ax.scatter(x, y, s=size, c=color, alpha=alpha, zorder=3, edgecolors='white', linewidth=0.5)
        
        # Label
        label = nd['label']
        offset_y = -0.35 if nd['level'] != 'L1' else -0.3
        fontsize = 8 if nd['level'] == 'L1' else (9 if nd['level'] == 'L2' else 11)
        ax.text(x, y + offset_y, label, ha='center', va='top',
                color='#cccccc', fontsize=fontsize, fontfamily='sans-serif', zorder=4)
    
    # Legend
    legend_elements = [
        mpatches.Patch(facecolor='#60a5fa', alpha=0.8, label=f'L1 事实 ({len(l1_nodes)})'),
        mpatches.Patch(facecolor='#a78bfa', alpha=0.8, label=f'L2 洞察 ({len(l2_nodes)})'),
        mpatches.Patch(facecolor='#f59e0b', alpha=0.8, label=f'L3 元规律 ({len(l3_nodes)})'),
    ]
    legend = ax.legend(handles=legend_elements, loc='upper left', fontsize=10,
                       facecolor='#1a1a2e', edgecolor='#333', labelcolor='#ccc',
                       framealpha=0.9)
    
    # Title
    ax.set_title('🧠 Knowledge Graph — 概念图谱', color='white', fontsize=18, fontweight='bold',
                 pad=20, fontfamily='sans-serif')
    ax.text(0.5, -0.02, f'{n} 个概念 · {len(edges)} 条关联 · 循环检测 · 自动蒸馏',
            transform=ax.transAxes, ha='center', color='#666', fontsize=10)
    
    ax.set_xlim(-6, 6)
    ax.set_ylim(-4, 3.5)
    ax.axis('off')
    
    plt.tight_layout()
    plt.savefig(output_path, dpi=150, bbox_inches='tight',
                facecolor='#0a0a1a', edgecolor='none')
    print(f"✅ 截图已保存: {output_path}")
    plt.close()

if __name__ == "__main__":
    nodes, edges = export_graph()
    output = os.path.join(os.path.dirname(__file__), "..", "assets", "knowledge-graph.png")
    os.makedirs(os.path.dirname(output), exist_ok=True)
    draw_graph(nodes, edges, output)

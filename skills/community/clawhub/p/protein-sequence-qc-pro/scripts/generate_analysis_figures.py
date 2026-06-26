#!/usr/bin/env python3
"""
生成 IRED 多数据源数据集和 IR08 分析的高质量可视化图表
"""

import json
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np
from pathlib import Path
import seaborn as sns

# 设置绘图风格
plt.rcParams['font.sans-serif'] = ['DejaVu Sans']
plt.rcParams['axes.unicode_minus'] = False
plt.rcParams['figure.dpi'] = 300
plt.rcParams['savefig.dpi'] = 300

BASE_DIR = Path("/root/autodl-tmp/ou_a1d19d5984eecd78f231c50f774eddb0")
OUTPUT_DIR = BASE_DIR / "analysis_figures"
OUTPUT_DIR.mkdir(exist_ok=True)

# 配色方案
COLORS = {
    'primary': '#2E86AB',
    'secondary': '#A23B72',
    'success': '#06A77D',
    'warning': '#F18F01',
    'danger': '#C73E1D',
    'info': '#6C757D',
    'light': '#E9ECEF',
    'dark': '#212529'
}

def plot_qc_pipeline():
    """绘制质量控制流程图"""
    fig, ax = plt.subplots(figsize=(12, 8))
    
    # 流程数据
    steps = [
        ('Raw Data', 3365, 100),
        ('Length Filter', 2963, 88.1),
        ('CD-HIT 90%', 1531, 45.5),
        ('Complexity', 1531, 45.5),
        ('Motif Check', 1531, 45.5),
        ('MSA (MAFFT)', 1531, 45.5),
        ('Trim (trimAl)', 1531, 45.5),
        ('Final Dataset', 1531, 45.5)
    ]
    
    y_positions = np.arange(len(steps))[::-1]
    
    # 绘制流程框
    for i, (step, count, percent) in enumerate(steps):
        y = y_positions[i]
        
        # 根据保留率选择颜色
        if percent >= 80:
            color = COLORS['success']
        elif percent >= 50:
            color = COLORS['warning']
        else:
            color = COLORS['primary']
        
        # 绘制矩形
        rect = mpatches.FancyBboxPatch(
            (0.1, y - 0.3), 0.8, 0.6,
            boxstyle="round,pad=0.05",
            facecolor=color, edgecolor='black',
            linewidth=2, alpha=0.8
        )
        ax.add_patch(rect)
        
        # 添加文字
        ax.text(0.5, y, f'{step}\n{count:,} sequences ({percent:.1f}%)',
                ha='center', va='center', fontsize=11, fontweight='bold',
                color='white')
        
        # 绘制箭头
        if i < len(steps) - 1:
            ax.arrow(0.5, y - 0.4, 0, -0.15,
                    head_width=0.08, head_length=0.05,
                    fc='black', ec='black', linewidth=2)
    
    ax.set_xlim(0, 1)
    ax.set_ylim(-0.5, len(steps) - 0.5)
    ax.axis('off')
    ax.set_title('Quality Control Pipeline\nIRED Multi-Source Dataset',
                 fontsize=16, fontweight='bold', pad=20)
    
    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / 'qc_pipeline.png', dpi=300, bbox_inches='tight', facecolor='white')
    plt.close()
    print("✅ 生成图表: qc_pipeline.png")

def plot_conservation_heatmap():
    """绘制保守位点热图"""
    # 读取保守位点数据
    conserved_file = BASE_DIR / 'ChemRxiv_QC_analysis/analysis/highly_conserved_positions.txt'
    
    positions = []
    gaps = []
    entropies = []
    
    with open(conserved_file, 'r') as f:
        for line in f:
            if line.startswith('#') or not line.strip():
                continue
            parts = line.strip().split('\t')
            if len(parts) >= 3:
                positions.append(int(parts[0]))
                gaps.append(float(parts[1]))
                entropies.append(float(parts[2]))
    
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 6), sharex=True)
    
    # Gap 比例
    bars1 = ax1.bar(positions, gaps, color=COLORS['warning'], alpha=0.8, edgecolor='black')
    ax1.axhline(y=0.5, color='red', linestyle='--', linewidth=2, label='High Gap Threshold (50%)')
    ax1.set_ylabel('Gap Ratio', fontsize=12, fontweight='bold')
    ax1.set_title('Highly Conserved Positions - Quality Assessment', fontsize=14, fontweight='bold')
    ax1.legend(loc='upper right')
    ax1.grid(axis='y', alpha=0.3, linestyle='--')
    
    # 归一化熵
    bars2 = ax2.bar(positions, entropies, color=COLORS['primary'], alpha=0.8, edgecolor='black')
    ax2.axhline(y=0.3, color='green', linestyle='--', linewidth=2, label='High Conservation Threshold')
    ax2.set_xlabel('Alignment Position', fontsize=12, fontweight='bold')
    ax2.set_ylabel('Normalized Entropy', fontsize=12, fontweight='bold')
    ax2.legend(loc='upper right')
    ax2.grid(axis='y', alpha=0.3, linestyle='--')
    
    # 标注高质量位点
    high_quality = [(p, e) for p, g, e in zip(positions, gaps, entropies) if g < 0.1 and e < 0.3]
    for pos, ent in high_quality:
        ax2.text(pos, ent + 0.02, '★', ha='center', va='bottom', 
                fontsize=14, color='gold', fontweight='bold')
    
    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / 'conservation_quality.png', dpi=300, bbox_inches='tight', facecolor='white')
    plt.close()
    print("✅ 生成图表: conservation_quality.png")

def plot_coevolution_network():
    """绘制共进化网络图"""
    # 读取共进化数据
    coevo_file = BASE_DIR / 'ChemRxiv_QC_analysis/analysis/coevolution_top50.csv'
    
    pairs = []
    with open(coevo_file, 'r') as f:
        next(f)  # 跳过表头
        for i, line in enumerate(f):
            if i >= 10:  # 只取 Top 10
                break
            parts = line.strip().split(',')
            if len(parts) >= 7:
                rank = int(parts[0])
                pos1 = int(parts[1])
                pos2 = int(parts[2])
                mi = float(parts[3])
                pairs.append((rank, pos1, pos2, mi))
    
    fig, ax = plt.subplots(figsize=(12, 8))
    
    # 统计每个位点出现的频率
    from collections import Counter
    all_positions = []
    for _, pos1, pos2, _ in pairs:
        all_positions.extend([pos1, pos2])
    position_counts = Counter(all_positions)
    
    # 找出核心位点（出现频率最高）
    core_positions = [pos for pos, count in position_counts.most_common(5)]
    
    # 绘制节点
    positions_set = set(all_positions)
    pos_coords = {}
    
    # 核心位点放在中心
    for i, pos in enumerate(core_positions):
        angle = 2 * np.pi * i / len(core_positions)
        x = 0.3 * np.cos(angle)
        y = 0.3 * np.sin(angle)
        pos_coords[pos] = (x, y)
    
    # 其他位点放在外围
    other_positions = [p for p in positions_set if p not in core_positions]
    for i, pos in enumerate(other_positions):
        angle = 2 * np.pi * i / len(other_positions)
        x = 0.7 * np.cos(angle)
        y = 0.7 * np.sin(angle)
        pos_coords[pos] = (x, y)
    
    # 绘制边（共进化关系）
    for rank, pos1, pos2, mi in pairs:
        x1, y1 = pos_coords[pos1]
        x2, y2 = pos_coords[pos2]
        
        # 线宽和颜色根据 MI 值
        linewidth = 1 + 3 * (mi / max(p[3] for p in pairs))
        alpha = 0.3 + 0.6 * (mi / max(p[3] for p in pairs))
        
        ax.plot([x1, x2], [y1, y2], 'gray', linewidth=linewidth, alpha=alpha, zorder=1)
    
    # 绘制节点
    for pos, (x, y) in pos_coords.items():
        count = position_counts[pos]
        size = 300 + 200 * count
        
        if pos in core_positions:
            color = COLORS['danger']
            marker = 'o'
        else:
            color = COLORS['primary']
            marker = 'o'
        
        ax.scatter(x, y, s=size, c=color, alpha=0.8, edgecolors='black', 
                  linewidths=2, zorder=2, marker=marker)
        ax.text(x, y, str(pos), ha='center', va='center', 
               fontsize=10, fontweight='bold', color='white', zorder=3)
    
    ax.set_xlim(-1, 1)
    ax.set_ylim(-1, 1)
    ax.set_aspect('equal')
    ax.axis('off')
    ax.set_title('Top 10 Coevolving Position Pairs\n(Node size = occurrence frequency, Edge width = MI value)',
                 fontsize=14, fontweight='bold', pad=20)
    
    # 添加图例
    legend_elements = [
        mpatches.Patch(facecolor=COLORS['danger'], edgecolor='black', label='Core positions (≥3 pairs)'),
        mpatches.Patch(facecolor=COLORS['primary'], edgecolor='black', label='Secondary positions')
    ]
    ax.legend(handles=legend_elements, loc='upper right', fontsize=10)
    
    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / 'coevolution_network.png', dpi=300, bbox_inches='tight', facecolor='white')
    plt.close()
    print("✅ 生成图表: coevolution_network.png")

def plot_ir08_conserved_sites():
    """绘制 IR08 保守位点分布"""
    # 读取 IR08 验证结果
    with open(BASE_DIR / 'IR08_conserved_sites_verified.json', 'r') as f:
        data = json.load(f)
    
    sites = data['sites']
    
    fig, ax = plt.subplots(figsize=(14, 6))
    
    # 绘制序列
    seq_length = 313
    ax.plot([0, seq_length], [0, 0], 'k-', linewidth=3)
    
    # 标注保守位点
    for site in sites:
        pos = site['ir08_pos']
        aa = site['ir08_aa']
        conservation = site['conservation']
        
        # 根据保守性选择颜色
        if conservation == 1.0:
            color = COLORS['danger']
            marker = '^'
            size = 200
        elif conservation >= 0.95:
            color = COLORS['warning']
            marker = 'o'
            size = 150
        else:
            color = COLORS['primary']
            marker = 's'
            size = 100
        
        ax.scatter(pos, 0, s=size, c=color, marker=marker, 
                  edgecolors='black', linewidths=2, zorder=3, alpha=0.8)
        ax.text(pos, 0.5, f'{aa}{pos}\n{conservation:.0%}', 
               ha='center', va='bottom', fontsize=9, fontweight='bold')
    
    # 标注功能区域
    regions = [
        (33, 41, 'Rossmann Fold', COLORS['success']),
        (53, 57, 'Cofactor Binding', COLORS['warning']),
        (91, 95, 'Catalytic Region', COLORS['danger']),
        (116, 120, 'Substrate Binding', COLORS['info'])
    ]
    
    y_offset = -1.5
    for start, end, label, color in regions:
        ax.plot([start, end], [y_offset, y_offset], color=color, linewidth=8, alpha=0.6)
        ax.text((start + end) / 2, y_offset - 0.3, label, 
               ha='center', va='top', fontsize=9, fontweight='bold', color=color)
    
    ax.set_xlim(-10, seq_length + 10)
    ax.set_ylim(-2.5, 2)
    ax.set_xlabel('Sequence Position', fontsize=12, fontweight='bold')
    ax.set_title('IR08 Conserved Sites Distribution\n(Based on 20 high-quality IRED sequences)',
                 fontsize=14, fontweight='bold', pad=20)
    ax.axis('off')
    
    # 添加图例
    legend_elements = [
        plt.Line2D([0], [0], marker='^', color='w', markerfacecolor=COLORS['danger'], 
                  markersize=12, label='100% conserved', markeredgecolor='black', markeredgewidth=1.5),
        plt.Line2D([0], [0], marker='o', color='w', markerfacecolor=COLORS['warning'], 
                  markersize=10, label='≥95% conserved', markeredgecolor='black', markeredgewidth=1.5),
        plt.Line2D([0], [0], marker='s', color='w', markerfacecolor=COLORS['primary'], 
                  markersize=8, label='≥85% conserved', markeredgecolor='black', markeredgewidth=1.5)
    ]
    ax.legend(handles=legend_elements, loc='upper right', fontsize=10, framealpha=0.9)
    
    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / 'ir08_conserved_sites.png', dpi=300, bbox_inches='tight', facecolor='white')
    plt.close()
    print("✅ 生成图表: ir08_conserved_sites.png")

def plot_ir08_mapping():
    """绘制 IR08 与大数据集的映射关系"""
    # 读取映射结果
    with open(BASE_DIR / 'IR08_ChemRxiv_complete_mapping.json', 'r') as f:
        data = json.load(f)
    
    conserved = data['conserved_sites']
    coevolution = data['coevolution_pairs']
    
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))
    
    # 左图：保守位点映射
    positions = [s['ir08_pos'] for s in conserved]
    entropies = [s['entropy'] for s in conserved]
    gaps = [s['gap'] for s in conserved]
    
    # 根据质量分类
    high_quality = [(p, e) for p, e, g in zip(positions, entropies, gaps) if g < 0.1]
    low_quality = [(p, e) for p, e, g in zip(positions, entropies, gaps) if g >= 0.1]
    
    if high_quality:
        hq_pos, hq_ent = zip(*high_quality)
        ax1.scatter(hq_pos, hq_ent, s=200, c=COLORS['success'], marker='o',
                   edgecolors='black', linewidths=2, label='High quality (Gap <10%)', alpha=0.8)
    
    if low_quality:
        lq_pos, lq_ent = zip(*low_quality)
        ax1.scatter(lq_pos, lq_ent, s=200, c=COLORS['warning'], marker='X',
                   edgecolors='black', linewidths=2, label='Low quality (Gap ≥10%)', alpha=0.8)
    
    ax1.axhline(y=0.3, color='red', linestyle='--', linewidth=2, alpha=0.5, label='Conservation threshold')
    ax1.set_xlabel('IR08 Position', fontsize=12, fontweight='bold')
    ax1.set_ylabel('Normalized Entropy', fontsize=12, fontweight='bold')
    ax1.set_title('Conserved Sites Mapped to IR08\n(n=1,531 sequences)', 
                 fontsize=13, fontweight='bold')
    ax1.legend(loc='upper right', fontsize=9)
    ax1.grid(True, alpha=0.3, linestyle='--')
    
    # 右图：共进化位点对
    mi_values = [p['mi'] for p in coevolution]
    ranks = list(range(1, len(coevolution) + 1))
    
    bars = ax2.barh(ranks, mi_values, color=COLORS['primary'], alpha=0.8, edgecolor='black')
    
    # 标注位点对
    for i, pair in enumerate(coevolution):
        pair_label = pair['ir08_pair']
        aa_pair = f"{pair['ir08_aa1']}{pair['ir08_aa2']}"
        ax2.text(pair['mi'] + 0.02, ranks[i], f"{pair_label} ({aa_pair})",
                va='center', ha='left', fontsize=9, fontweight='bold')
    
    ax2.set_xlabel('Mutual Information (MI)', fontsize=12, fontweight='bold')
    ax2.set_ylabel('Rank', fontsize=12, fontweight='bold')
    ax2.set_title('Top 10 Coevolving Pairs in IR08\n(n=1,531 sequences)', 
                 fontsize=13, fontweight='bold')
    ax2.invert_yaxis()
    ax2.grid(axis='x', alpha=0.3, linestyle='--')
    
    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / 'ir08_mapping.png', dpi=300, bbox_inches='tight', facecolor='white')
    plt.close()
    print("✅ 生成图表: ir08_mapping.png")

def plot_mutation_priority():
    """绘制突变实验优先级"""
    fig, ax = plt.subplots(figsize=(12, 8))
    
    # 突变数据
    mutations = [
        # (突变, 预期活性降低, 优先级, 类型)
        ('E63Q', 75, 1, 'Coevolution'),
        ('E63Q+T84A', 90, 1, 'Coevolution'),
        ('T84A', 50, 1, 'Coevolution'),
        ('W55F', 65, 2, 'Conservation'),
        ('G33A', 75, 2, 'Conservation'),
        ('C91S', 55, 2, 'Conservation'),
        ('E23Q', 40, 3, 'Conservation'),
        ('V65A', 30, 3, 'Conservation'),
        ('E100Q', 40, 3, 'Conservation'),
    ]
    
    # 按优先级分组
    priority_colors = {
        1: COLORS['danger'],
        2: COLORS['warning'],
        3: COLORS['primary']
    }
    
    y_positions = np.arange(len(mutations))[::-1]
    
    for i, (mut, activity_loss, priority, mut_type) in enumerate(mutations):
        y = y_positions[i]
        color = priority_colors[priority]
        
        # 绘制条形
        bar = ax.barh(y, activity_loss, height=0.6, color=color, 
                     alpha=0.8, edgecolor='black', linewidth=2)
        
        # 添加标签
        ax.text(-5, y, mut, ha='right', va='center', 
               fontsize=11, fontweight='bold')
        ax.text(activity_loss + 2, y, f'{activity_loss}%', 
               ha='left', va='center', fontsize=10, fontweight='bold')
        
        # 添加类型标签
        if mut_type == 'Coevolution':
            ax.text(activity_loss / 2, y, '★', ha='center', va='center',
                   fontsize=16, color='gold', fontweight='bold')
    
    ax.set_xlim(-15, 100)
    ax.set_ylim(-0.5, len(mutations) - 0.5)
    ax.set_xlabel('Expected Activity Loss (%)', fontsize=12, fontweight='bold')
    ax.set_title('Mutation Experiment Priority\n(Based on conservation and coevolution analysis)',
                 fontsize=14, fontweight='bold', pad=20)
    ax.grid(axis='x', alpha=0.3, linestyle='--')
    
    # 添加图例
    legend_elements = [
        mpatches.Patch(facecolor=COLORS['danger'], edgecolor='black', 
                      label='Priority 1: Coevolution sites'),
        mpatches.Patch(facecolor=COLORS['warning'], edgecolor='black', 
                      label='Priority 2: Key conserved sites'),
        mpatches.Patch(facecolor=COLORS['primary'], edgecolor='black', 
                      label='Priority 3: Other conserved sites'),
        plt.Line2D([0], [0], marker='*', color='w', markerfacecolor='gold',
                  markersize=15, label='Coevolution-based', markeredgecolor='none')
    ]
    ax.legend(handles=legend_elements, loc='lower right', fontsize=10, framealpha=0.9)
    
    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / 'mutation_priority.png', dpi=300, bbox_inches='tight', facecolor='white')
    plt.close()
    print("✅ 生成图表: mutation_priority.png")

def main():
    print("=" * 80)
    print("生成 IRED 多数据源数据集和 IR08 分析的高质量可视化图表")
    print("=" * 80)
    
    print("\n生成图表...")
    
    # 多数据源数据集分析图表
    print("\n[1/6] 质量控制流程图...")
    plot_qc_pipeline()
    
    print("[2/6] 保守位点质量评估...")
    plot_conservation_heatmap()
    
    print("[3/6] 共进化网络图...")
    plot_coevolution_network()
    
    # IR08 分析图表
    print("[4/6] IR08 保守位点分布...")
    plot_ir08_conserved_sites()
    
    print("[5/6] IR08 映射关系...")
    plot_ir08_mapping()
    
    print("[6/6] 突变实验优先级...")
    plot_mutation_priority()
    
    print("\n" + "=" * 80)
    print(f"✅ 所有图表已保存到: {OUTPUT_DIR}")
    print("=" * 80)
    
    # 列出生成的文件
    print("\n生成的图表文件:")
    for img in sorted(OUTPUT_DIR.glob('*.png')):
        print(f"  - {img.name}")

if __name__ == "__main__":
    main()

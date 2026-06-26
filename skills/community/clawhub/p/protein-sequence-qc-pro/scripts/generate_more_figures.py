#!/usr/bin/env python3
"""
生成更多 IRED 分析的高质量可视化图表
"""

import json
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import Rectangle, FancyBboxPatch
import numpy as np
from pathlib import Path
import seaborn as sns
from Bio import SeqIO

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

def plot_alignment_statistics():
    """绘制比对统计信息"""
    # 读取比对分析结果
    with open(BASE_DIR / 'ChemRxiv_QC_analysis/analysis/alignment_analysis.json', 'r') as f:
        data = json.load(f)
    
    fig, axes = plt.subplots(2, 2, figsize=(14, 10))
    
    # 1. 序列覆盖率分布
    ax1 = axes[0, 0]
    coverage = data['per_sequence_stats']['coverage']
    ax1.hist(coverage, bins=30, color=COLORS['primary'], alpha=0.7, edgecolor='black')
    ax1.axvline(np.mean(coverage), color='red', linestyle='--', linewidth=2, label=f'Mean: {np.mean(coverage):.1f}%')
    ax1.axvline(np.median(coverage), color='green', linestyle='--', linewidth=2, label=f'Median: {np.median(coverage):.1f}%')
    ax1.set_xlabel('Coverage (%)', fontsize=11, fontweight='bold')
    ax1.set_ylabel('Number of Sequences', fontsize=11, fontweight='bold')
    ax1.set_title('Sequence Coverage Distribution', fontsize=12, fontweight='bold')
    ax1.legend()
    ax1.grid(axis='y', alpha=0.3, linestyle='--')
    
    # 2. Gap 比例分布
    ax2 = axes[0, 1]
    gap_ratios = data['per_sequence_stats']['gap_ratio']
    ax2.hist(gap_ratios, bins=30, color=COLORS['warning'], alpha=0.7, edgecolor='black')
    ax2.axvline(np.mean(gap_ratios), color='red', linestyle='--', linewidth=2, label=f'Mean: {np.mean(gap_ratios):.1f}%')
    ax2.set_xlabel('Gap Ratio (%)', fontsize=11, fontweight='bold')
    ax2.set_ylabel('Number of Sequences', fontsize=11, fontweight='bold')
    ax2.set_title('Gap Ratio Distribution', fontsize=12, fontweight='bold')
    ax2.legend()
    ax2.grid(axis='y', alpha=0.3, linestyle='--')
    
    # 3. 序列一致性分布
    ax3 = axes[1, 0]
    identity = data['per_sequence_stats']['identity']
    ax3.hist(identity, bins=30, color=COLORS['success'], alpha=0.7, edgecolor='black')
    ax3.axvline(np.mean(identity), color='red', linestyle='--', linewidth=2, label=f'Mean: {np.mean(identity):.1f}%')
    ax3.set_xlabel('Sequence Identity (%)', fontsize=11, fontweight='bold')
    ax3.set_ylabel('Number of Sequences', fontsize=11, fontweight='bold')
    ax3.set_title('Sequence Identity Distribution', fontsize=12, fontweight='bold')
    ax3.legend()
    ax3.grid(axis='y', alpha=0.3, linestyle='--')
    
    # 4. 总体统计摘要
    ax4 = axes[1, 1]
    ax4.axis('off')
    
    stats_text = f"""
    Alignment Statistics Summary
    ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    
    Number of Sequences: {data['num_sequences']:,}
    Alignment Length: {data['alignment_length']:,} columns
    
    Average Coverage: {data['average_coverage']:.1f}%
    Average Gap Ratio: {data['average_gap_ratio']:.1f}%
    Average Identity: {data['average_identity']:.1f}%
    
    High Gap Positions (>50%): {data['high_gap_positions']}
    
    Quality Assessment:
    ✓ Coverage ≥80%: {sum(1 for c in coverage if c >= 80)} seqs
    ✓ Gap ratio <20%: {sum(1 for g in gap_ratios if g < 20)} seqs
    ✓ Identity ≥15%: {sum(1 for i in identity if i >= 15)} seqs
    """
    
    ax4.text(0.1, 0.5, stats_text, fontsize=11, family='monospace',
            verticalalignment='center', bbox=dict(boxstyle='round', 
            facecolor=COLORS['light'], alpha=0.8, edgecolor='black', linewidth=2))
    
    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / 'alignment_statistics.png', dpi=300, bbox_inches='tight', facecolor='white')
    plt.close()
    print("✅ 生成图表: alignment_statistics.png")

def plot_conservation_entropy_curve():
    """绘制保守性熵曲线"""
    # 读取 Gap 比例数据
    with open(BASE_DIR / 'ChemRxiv_QC_analysis/analysis/gap_ratios.json', 'r') as f:
        gap_data = json.load(f)
    
    positions = sorted([int(k) for k in gap_data.keys()])
    gap_ratios = [gap_data[str(p)] for p in positions]
    
    # 读取保守位点
    conserved_positions = []
    with open(BASE_DIR / 'ChemRxiv_QC_analysis/analysis/highly_conserved_positions.txt', 'r') as f:
        for line in f:
            if line.startswith('#') or not line.strip():
                continue
            parts = line.strip().split('\t')
            if len(parts) >= 3:
                conserved_positions.append(int(parts[0]))
    
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(16, 8), sharex=True)
    
    # 上图：Gap 比例曲线
    ax1.fill_between(positions, gap_ratios, alpha=0.3, color=COLORS['primary'])
    ax1.plot(positions, gap_ratios, color=COLORS['primary'], linewidth=1.5)
    ax1.axhline(y=0.5, color='red', linestyle='--', linewidth=2, alpha=0.5, label='High Gap Threshold (50%)')
    
    # 标注保守位点
    for pos in conserved_positions:
        if pos in positions:
            idx = positions.index(pos)
            gap = gap_ratios[idx]
            if gap < 0.5:
                ax1.scatter(pos, gap, s=100, c='gold', marker='*', edgecolors='black', 
                          linewidths=1.5, zorder=5)
    
    ax1.set_ylabel('Gap Ratio', fontsize=12, fontweight='bold')
    ax1.set_title('Conservation Landscape Across Alignment\n(Gold stars = highly conserved positions with low gap)',
                 fontsize=14, fontweight='bold')
    ax1.legend(loc='upper right')
    ax1.grid(axis='y', alpha=0.3, linestyle='--')
    ax1.set_ylim(-0.05, 1.05)
    
    # 下图：保守位点密度
    window_size = 10
    conserved_density = []
    for i in range(len(positions)):
        start = max(0, i - window_size // 2)
        end = min(len(positions), i + window_size // 2)
        window_positions = positions[start:end]
        density = sum(1 for p in window_positions if p in conserved_positions) / len(window_positions)
        conserved_density.append(density)
    
    ax2.fill_between(positions, conserved_density, alpha=0.3, color=COLORS['success'])
    ax2.plot(positions, conserved_density, color=COLORS['success'], linewidth=1.5)
    ax2.set_xlabel('Alignment Position', fontsize=12, fontweight='bold')
    ax2.set_ylabel('Conserved Site Density', fontsize=12, fontweight='bold')
    ax2.set_title(f'Conserved Site Density (Window size = {window_size})', fontsize=12, fontweight='bold')
    ax2.grid(axis='y', alpha=0.3, linestyle='--')
    ax2.set_ylim(-0.05, 1.05)
    
    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / 'conservation_landscape.png', dpi=300, bbox_inches='tight', facecolor='white')
    plt.close()
    print("✅ 生成图表: conservation_landscape.png")

def plot_coevolution_heatmap():
    """绘制共进化热图（Top 20 位点）"""
    # 读取共进化数据
    coevo_file = BASE_DIR / 'ChemRxiv_QC_analysis/analysis/coevolution_top50.csv'
    
    pairs = []
    with open(coevo_file, 'r') as f:
        next(f)  # 跳过表头
        for i, line in enumerate(f):
            if i >= 20:  # 只取 Top 20
                break
            parts = line.strip().split(',')
            if len(parts) >= 7:
                pos1 = int(parts[1])
                pos2 = int(parts[2])
                mi = float(parts[3])
                pairs.append((pos1, pos2, mi))
    
    # 获取所有涉及的位点
    all_positions = sorted(set([p[0] for p in pairs] + [p[1] for p in pairs]))
    n = len(all_positions)
    
    # 创建矩阵
    matrix = np.zeros((n, n))
    pos_to_idx = {pos: i for i, pos in enumerate(all_positions)}
    
    for pos1, pos2, mi in pairs:
        i = pos_to_idx[pos1]
        j = pos_to_idx[pos2]
        matrix[i, j] = mi
        matrix[j, i] = mi
    
    fig, ax = plt.subplots(figsize=(12, 10))
    
    # 绘制热图
    im = ax.imshow(matrix, cmap='YlOrRd', aspect='auto', vmin=0, vmax=matrix.max())
    
    # 设置刻度
    ax.set_xticks(range(n))
    ax.set_yticks(range(n))
    ax.set_xticklabels(all_positions, fontsize=9)
    ax.set_yticklabels(all_positions, fontsize=9)
    
    # 旋转 x 轴标签
    plt.setp(ax.get_xticklabels(), rotation=45, ha="right", rotation_mode="anchor")
    
    # 添加数值标注（只标注非零值）
    for i in range(n):
        for j in range(n):
            if matrix[i, j] > 0:
                text = ax.text(j, i, f'{matrix[i, j]:.2f}',
                             ha="center", va="center", color="black", fontsize=7, fontweight='bold')
    
    # 添加颜色条
    cbar = plt.colorbar(im, ax=ax, fraction=0.046, pad=0.04)
    cbar.set_label('Mutual Information (MI)', fontsize=11, fontweight='bold')
    
    ax.set_title('Coevolution Heatmap - Top 20 Position Pairs\n(Higher MI = Stronger coevolution)',
                fontsize=14, fontweight='bold', pad=20)
    ax.set_xlabel('Alignment Position', fontsize=12, fontweight='bold')
    ax.set_ylabel('Alignment Position', fontsize=12, fontweight='bold')
    
    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / 'coevolution_heatmap.png', dpi=300, bbox_inches='tight', facecolor='white')
    plt.close()
    print("✅ 生成图表: coevolution_heatmap.png")

def plot_sequence_length_distribution():
    """绘制序列长度分布（原始 vs 最终）"""
    # 读取原始数据集
    original_file = BASE_DIR / 'IRED_dataset_collection/all_ired_sequences_merged_unique.csv'
    final_file = BASE_DIR / 'ChemRxiv_QC_analysis/sequences/04_motif_checked.fasta'
    
    # 读取原始长度
    original_lengths = []
    with open(original_file, 'r') as f:
        next(f)  # 跳过表头
        for line in f:
            parts = line.strip().split(',')
            if len(parts) >= 2:
                seq = parts[1]
                original_lengths.append(len(seq))
    
    # 读取最终长度
    final_lengths = []
    for record in SeqIO.parse(final_file, 'fasta'):
        final_lengths.append(len(record.seq))
    
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))
    
    # 左图：原始分布
    ax1.hist(original_lengths, bins=50, color=COLORS['info'], alpha=0.7, edgecolor='black')
    ax1.axvline(np.mean(original_lengths), color='red', linestyle='--', linewidth=2, 
               label=f'Mean: {np.mean(original_lengths):.0f} aa')
    ax1.axvline(np.median(original_lengths), color='green', linestyle='--', linewidth=2,
               label=f'Median: {np.median(original_lengths):.0f} aa')
    ax1.set_xlabel('Sequence Length (aa)', fontsize=11, fontweight='bold')
    ax1.set_ylabel('Number of Sequences', fontsize=11, fontweight='bold')
    ax1.set_title(f'Original Dataset\n(n={len(original_lengths):,})', fontsize=12, fontweight='bold')
    ax1.legend()
    ax1.grid(axis='y', alpha=0.3, linestyle='--')
    
    # 右图：最终分布
    ax2.hist(final_lengths, bins=30, color=COLORS['success'], alpha=0.7, edgecolor='black')
    ax2.axvline(np.mean(final_lengths), color='red', linestyle='--', linewidth=2,
               label=f'Mean: {np.mean(final_lengths):.0f} aa')
    ax2.axvline(np.median(final_lengths), color='green', linestyle='--', linewidth=2,
               label=f'Median: {np.median(final_lengths):.0f} aa')
    ax2.set_xlabel('Sequence Length (aa)', fontsize=11, fontweight='bold')
    ax2.set_ylabel('Number of Sequences', fontsize=11, fontweight='bold')
    ax2.set_title(f'After Quality Control\n(n={len(final_lengths):,})', fontsize=12, fontweight='bold')
    ax2.legend()
    ax2.grid(axis='y', alpha=0.3, linestyle='--')
    
    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / 'length_distribution_comparison.png', dpi=300, bbox_inches='tight', facecolor='white')
    plt.close()
    print("✅ 生成图表: length_distribution_comparison.png")

def plot_ir08_functional_regions():
    """绘制 IR08 功能区域详细图"""
    # 读取 IR08 序列
    ir08 = SeqIO.read(BASE_DIR / 'IR08.fasta', 'fasta')
    seq = str(ir08.seq)
    seq_length = len(seq)
    
    fig, ax = plt.subplots(figsize=(16, 8))
    
    # 定义功能区域
    regions = [
        # (start, end, name, color, y_level)
        (33, 41, 'Rossmann Fold\n(GLGAMGTAL)', COLORS['success'], 0),
        (53, 57, 'Cofactor Binding\n(TVWNR)', COLORS['warning'], 1),
        (91, 95, 'Catalytic Region\n(C...DY)', COLORS['danger'], 0),
        (116, 120, 'Substrate Binding\n(NLTN.G)', COLORS['info'], 1),
    ]
    
    # 绘制序列主线
    ax.plot([0, seq_length], [2, 2], 'k-', linewidth=4, zorder=1)
    
    # 绘制功能区域
    for start, end, name, color, y_level in regions:
        y = 2 + (y_level - 0.5) * 0.8
        
        # 绘制区域框
        rect = FancyBboxPatch((start, y - 0.3), end - start, 0.6,
                             boxstyle="round,pad=0.05", 
                             facecolor=color, edgecolor='black',
                             linewidth=2, alpha=0.7, zorder=2)
        ax.add_patch(rect)
        
        # 添加标签
        ax.text((start + end) / 2, y + 0.8, name,
               ha='center', va='bottom', fontsize=10, fontweight='bold',
               bbox=dict(boxstyle='round', facecolor='white', 
                        edgecolor=color, linewidth=2, alpha=0.9))
        
        # 绘制连接线
        ax.plot([(start + end) / 2, (start + end) / 2], [y + 0.3, y + 0.7],
               'k-', linewidth=1.5, zorder=1)
    
    # 标注关键保守位点
    key_sites = [
        (33, 'G', '100%', COLORS['success']),
        (35, 'G', '100%', COLORS['success']),
        (55, 'W', '100%', COLORS['warning']),
        (63, 'E', 'MI=1.286', COLORS['danger']),
        (84, 'T', 'MI=1.286', COLORS['danger']),
        (91, 'C', '100%', COLORS['danger']),
        (116, 'N', '100%', COLORS['info']),
    ]
    
    for pos, aa, label, color in key_sites:
        ax.scatter(pos, 2, s=300, c=color, marker='v', 
                  edgecolors='black', linewidths=2, zorder=5, alpha=0.9)
        ax.text(pos, 1.3, f'{aa}{pos}\n{label}',
               ha='center', va='top', fontsize=9, fontweight='bold',
               bbox=dict(boxstyle='round', facecolor='white',
                        edgecolor=color, linewidth=1.5, alpha=0.9))
    
    # 设置坐标轴
    ax.set_xlim(-10, seq_length + 10)
    ax.set_ylim(0, 4)
    ax.set_xlabel('Sequence Position', fontsize=13, fontweight='bold')
    ax.set_title('IR08 Functional Regions and Key Conserved Sites\n(313 amino acids)',
                fontsize=15, fontweight='bold', pad=20)
    ax.axis('off')
    
    # 添加图例
    legend_elements = [
        mpatches.Patch(facecolor=COLORS['success'], edgecolor='black', 
                      label='Rossmann Fold (NAD(P)H binding)'),
        mpatches.Patch(facecolor=COLORS['warning'], edgecolor='black',
                      label='Cofactor Binding Site'),
        mpatches.Patch(facecolor=COLORS['danger'], edgecolor='black',
                      label='Catalytic Region'),
        mpatches.Patch(facecolor=COLORS['info'], edgecolor='black',
                      label='Substrate Binding Site'),
        plt.Line2D([0], [0], marker='v', color='w', markerfacecolor='gray',
                  markersize=12, label='Key conserved site', markeredgecolor='black', markeredgewidth=1.5)
    ]
    ax.legend(handles=legend_elements, loc='upper right', fontsize=10, framealpha=0.95)
    
    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / 'ir08_functional_regions.png', dpi=300, bbox_inches='tight', facecolor='white')
    plt.close()
    print("✅ 生成图表: ir08_functional_regions.png")

def plot_data_quality_comparison():
    """绘制数据质量对比（小数据集 vs 大数据集）"""
    fig, axes = plt.subplots(2, 2, figsize=(14, 10))
    
    # 数据
    datasets = ['Small Dataset\n(573 seqs)', 'Large Dataset\n(1,531 seqs)']
    
    # 1. 序列数量
    ax1 = axes[0, 0]
    seq_counts = [573, 1531]
    bars = ax1.bar(datasets, seq_counts, color=[COLORS['info'], COLORS['primary']], 
                   alpha=0.8, edgecolor='black', linewidth=2)
    for bar in bars:
        height = bar.get_height()
        ax1.text(bar.get_x() + bar.get_width()/2., height,
                f'{int(height):,}',
                ha='center', va='bottom', fontsize=12, fontweight='bold')
    ax1.set_ylabel('Number of Sequences', fontsize=11, fontweight='bold')
    ax1.set_title('Dataset Size', fontsize=12, fontweight='bold')
    ax1.grid(axis='y', alpha=0.3, linestyle='--')
    
    # 2. 比对长度
    ax2 = axes[0, 1]
    aln_lengths = [234, 164]
    bars = ax2.bar(datasets, aln_lengths, color=[COLORS['info'], COLORS['primary']],
                   alpha=0.8, edgecolor='black', linewidth=2)
    for bar in bars:
        height = bar.get_height()
        ax2.text(bar.get_x() + bar.get_width()/2., height,
                f'{int(height)}',
                ha='center', va='bottom', fontsize=12, fontweight='bold')
    ax2.set_ylabel('Alignment Length (columns)', fontsize=11, fontweight='bold')
    ax2.set_title('Alignment Length', fontsize=12, fontweight='bold')
    ax2.grid(axis='y', alpha=0.3, linestyle='--')
    
    # 3. 平均一致性
    ax3 = axes[1, 0]
    identities = [27.0, 20.3]
    bars = ax3.bar(datasets, identities, color=[COLORS['info'], COLORS['primary']],
                   alpha=0.8, edgecolor='black', linewidth=2)
    for bar in bars:
        height = bar.get_height()
        ax3.text(bar.get_x() + bar.get_width()/2., height,
                f'{height:.1f}%',
                ha='center', va='bottom', fontsize=12, fontweight='bold')
    ax3.set_ylabel('Average Identity (%)', fontsize=11, fontweight='bold')
    ax3.set_title('Sequence Identity', fontsize=12, fontweight='bold')
    ax3.grid(axis='y', alpha=0.3, linestyle='--')
    
    # 4. 保守位点数量
    ax4 = axes[1, 1]
    conserved_counts = [8, 8]
    bars = ax4.bar(datasets, conserved_counts, color=[COLORS['info'], COLORS['primary']],
                   alpha=0.8, edgecolor='black', linewidth=2)
    for bar in bars:
        height = bar.get_height()
        ax4.text(bar.get_x() + bar.get_width()/2., height,
                f'{int(height)}',
                ha='center', va='bottom', fontsize=12, fontweight='bold')
    ax4.set_ylabel('Number of Conserved Sites', fontsize=11, fontweight='bold')
    ax4.set_title('Highly Conserved Positions', fontsize=12, fontweight='bold')
    ax4.grid(axis='y', alpha=0.3, linestyle='--')
    
    plt.suptitle('Data Quality Comparison: Small vs Large Dataset',
                fontsize=15, fontweight='bold', y=1.00)
    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / 'dataset_comparison.png', dpi=300, bbox_inches='tight', facecolor='white')
    plt.close()
    print("✅ 生成图表: dataset_comparison.png")

def main():
    print("=" * 80)
    print("生成更多 IRED 分析的高质量可视化图表")
    print("=" * 80)
    
    print("\n生成图表...")
    
    print("[1/6] 比对统计信息...")
    plot_alignment_statistics()
    
    print("[2/6] 保守性景观图...")
    plot_conservation_entropy_curve()
    
    print("[3/6] 共进化热图...")
    plot_coevolution_heatmap()
    
    print("[4/6] 序列长度分布对比...")
    plot_sequence_length_distribution()
    
    print("[5/6] IR08 功能区域详细图...")
    plot_ir08_functional_regions()
    
    print("[6/6] 数据质量对比...")
    plot_data_quality_comparison()
    
    print("\n" + "=" * 80)
    print(f"✅ 所有图表已保存到: {OUTPUT_DIR}")
    print("=" * 80)
    
    # 列出所有生成的文件
    print("\n所有图表文件:")
    for img in sorted(OUTPUT_DIR.glob('*.png')):
        print(f"  - {img.name}")

if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""
生成 Nature 风格的保守性景观图
"""

import json
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
from pathlib import Path

# Nature 期刊风格设置
plt.rcParams['font.family'] = 'sans-serif'
plt.rcParams['font.sans-serif'] = ['Arial', 'DejaVu Sans']
plt.rcParams['font.size'] = 8
plt.rcParams['axes.linewidth'] = 0.5
plt.rcParams['xtick.major.width'] = 0.5
plt.rcParams['ytick.major.width'] = 0.5
plt.rcParams['xtick.major.size'] = 3
plt.rcParams['ytick.major.size'] = 3
plt.rcParams['figure.dpi'] = 300
plt.rcParams['savefig.dpi'] = 300

BASE_DIR = Path("/root/autodl-tmp/ou_a1d19d5984eecd78f231c50f774eddb0")
OUTPUT_DIR = BASE_DIR / "analysis_figures"

# Nature 配色方案
NATURE_COLORS = {
    'blue': '#0173B2',
    'orange': '#DE8F05',
    'green': '#029E73',
    'red': '#CC78BC',
    'purple': '#CA9161',
    'brown': '#949494',
    'pink': '#ECE133',
    'gray': '#56B4E9'
}

print("=" * 80)
print("生成 Nature 风格的保守性景观图")
print("=" * 80)

# 读取数据
print("\n读取数据...")
with open(BASE_DIR / 'ChemRxiv_QC_analysis/analysis/gap_ratios.json', 'r') as f:
    gap_data = json.load(f)

positions = sorted([int(k) for k in gap_data.keys()])
gap_ratios = [gap_data[str(p)] for p in positions]

# 读取保守位点
conserved_positions = []
conserved_entropies = {}
with open(BASE_DIR / 'ChemRxiv_QC_analysis/analysis/highly_conserved_positions.txt', 'r') as f:
    for line in f:
        if line.startswith('#') or not line.strip():
            continue
        parts = line.strip().split('\t')
        if len(parts) >= 3:
            pos = int(parts[0])
            entropy = float(parts[2])
            conserved_positions.append(pos)
            conserved_entropies[pos] = entropy

# 读取共进化数据
print("读取共进化数据...")
coevo_positions = set()
with open(BASE_DIR / 'ChemRxiv_QC_analysis/analysis/coevolution_top50.csv', 'r') as f:
    next(f)  # 跳过表头
    for i, line in enumerate(f):
        if i >= 10:  # 只取 Top 10
            break
        parts = line.strip().split(',')
        if len(parts) >= 3:
            pos1 = int(parts[1])
            pos2 = int(parts[2])
            coevo_positions.add(pos1)
            coevo_positions.add(pos2)

print(f"保守位点数: {len(conserved_positions)}")
print(f"共进化位点数: {len(coevo_positions)}")

# 创建图表
print("\n生成图表...")
fig = plt.figure(figsize=(7.08, 4.5))  # Nature 单栏宽度 7.08 cm = 2.78 inch, 双栏 14.17 cm

# 创建 3 个子图
gs = fig.add_gridspec(3, 1, height_ratios=[1, 1, 0.3], hspace=0.05)
ax1 = fig.add_subplot(gs[0])
ax2 = fig.add_subplot(gs[1], sharex=ax1)
ax3 = fig.add_subplot(gs[2], sharex=ax1)

# 上图：Gap 比例
ax1.fill_between(positions, gap_ratios, alpha=0.3, color=NATURE_COLORS['blue'], linewidth=0)
ax1.plot(positions, gap_ratios, color=NATURE_COLORS['blue'], linewidth=1, alpha=0.8)
ax1.axhline(y=0.5, color=NATURE_COLORS['red'], linestyle='--', linewidth=0.8, alpha=0.7)

# 标注高质量保守位点
for pos in conserved_positions:
    if pos in positions:
        idx = positions.index(pos)
        gap = gap_ratios[idx]
        if gap < 0.1:  # 高质量位点
            ax1.scatter(pos, gap, s=20, c=NATURE_COLORS['orange'], marker='*', 
                      edgecolors='black', linewidths=0.3, zorder=5, alpha=0.9)

ax1.set_ylabel('Gap ratio', fontsize=8, fontweight='normal')
ax1.set_ylim(-0.05, 1.05)
ax1.set_yticks([0, 0.25, 0.5, 0.75, 1.0])
ax1.tick_params(axis='both', which='major', labelsize=7)
ax1.spines['top'].set_visible(False)
ax1.spines['right'].set_visible(False)
plt.setp(ax1.get_xticklabels(), visible=False)

# 添加标签 a
ax1.text(-0.08, 1.05, 'a', transform=ax1.transAxes, fontsize=10, fontweight='bold', va='top')

# 中图：保守性熵
# 计算每个位点的熵（如果有的话）
entropies = []
for pos in positions:
    if pos in conserved_entropies:
        entropies.append(conserved_entropies[pos])
    else:
        entropies.append(1.0)  # 默认高熵（不保守）

ax2.fill_between(positions, entropies, alpha=0.3, color=NATURE_COLORS['green'], linewidth=0)
ax2.plot(positions, entropies, color=NATURE_COLORS['green'], linewidth=1, alpha=0.8)
ax2.axhline(y=0.3, color=NATURE_COLORS['red'], linestyle='--', linewidth=0.8, alpha=0.7)

# 标注高质量保守位点
for pos in conserved_positions:
    if pos in positions and pos in conserved_entropies:
        idx = positions.index(pos)
        gap = gap_ratios[idx]
        entropy = conserved_entropies[pos]
        if gap < 0.1 and entropy < 0.3:  # 高质量保守位点
            ax2.scatter(pos, entropy, s=20, c=NATURE_COLORS['orange'], marker='*',
                      edgecolors='black', linewidths=0.3, zorder=5, alpha=0.9)

ax2.set_ylabel('Normalized entropy', fontsize=8, fontweight='normal')
ax2.set_ylim(-0.05, 1.05)
ax2.set_yticks([0, 0.25, 0.5, 0.75, 1.0])
ax2.tick_params(axis='both', which='major', labelsize=7)
ax2.spines['top'].set_visible(False)
ax2.spines['right'].set_visible(False)
plt.setp(ax2.get_xticklabels(), visible=False)

# 添加标签 b
ax2.text(-0.08, 1.05, 'b', transform=ax2.transAxes, fontsize=10, fontweight='bold', va='top')

# 下图：功能注释（保守位点和共进化位点）
ax3.set_ylim(0, 2)
ax3.set_yticks([])
ax3.spines['top'].set_visible(False)
ax3.spines['right'].set_visible(False)
ax3.spines['left'].set_visible(False)

# 绘制保守位点
for pos in conserved_positions:
    if pos in positions:
        idx = positions.index(pos)
        gap = gap_ratios[idx]
        if gap < 0.1:  # 高质量
            ax3.axvline(x=pos, ymin=0.6, ymax=1.0, color=NATURE_COLORS['orange'], 
                       linewidth=1.5, alpha=0.8)

# 绘制共进化位点
for pos in coevo_positions:
    if pos in positions:
        ax3.axvline(x=pos, ymin=0.0, ymax=0.4, color=NATURE_COLORS['purple'], 
                   linewidth=1.5, alpha=0.8)

# 添加图例
from matplotlib.lines import Line2D
legend_elements = [
    Line2D([0], [0], color=NATURE_COLORS['orange'], linewidth=2, label='Conserved (Gap<10%)'),
    Line2D([0], [0], color=NATURE_COLORS['purple'], linewidth=2, label='Coevolving (Top 10)')
]
ax3.legend(handles=legend_elements, loc='upper right', fontsize=6, frameon=False, ncol=2)

ax3.set_xlabel('Alignment position', fontsize=8, fontweight='normal')
ax3.set_xlim(min(positions), max(positions))
ax3.tick_params(axis='x', which='major', labelsize=7)

# 添加标签 c
ax3.text(-0.08, 1.05, 'c', transform=ax3.transAxes, fontsize=10, fontweight='bold', va='top')

# 保存图表
plt.tight_layout()
output_file = OUTPUT_DIR / 'figure_nature_01_conservation_landscape.png'
plt.savefig(output_file, dpi=300, bbox_inches='tight', facecolor='white')
plt.close()

print(f"\n✅ 图表已保存: {output_file}")
print(f"   尺寸: 7.08 x 4.5 inch (Nature 单栏宽度)")
print(f"   分辨率: 300 DPI")

# 同时保存 PDF 版本（用于论文投稿）
plt.figure(figsize=(7.08, 4.5))
gs = plt.GridSpec(3, 1, height_ratios=[1, 1, 0.3], hspace=0.05)
ax1 = plt.subplot(gs[0])
ax2 = plt.subplot(gs[1], sharex=ax1)
ax3 = plt.subplot(gs[2], sharex=ax1)

# 重新绘制（PDF 版本）
ax1.fill_between(positions, gap_ratios, alpha=0.3, color=NATURE_COLORS['blue'], linewidth=0)
ax1.plot(positions, gap_ratios, color=NATURE_COLORS['blue'], linewidth=1, alpha=0.8)
ax1.axhline(y=0.5, color=NATURE_COLORS['red'], linestyle='--', linewidth=0.8, alpha=0.7)
for pos in conserved_positions:
    if pos in positions:
        idx = positions.index(pos)
        gap = gap_ratios[idx]
        if gap < 0.1:
            ax1.scatter(pos, gap, s=20, c=NATURE_COLORS['orange'], marker='*', 
                      edgecolors='black', linewidths=0.3, zorder=5, alpha=0.9)
ax1.set_ylabel('Gap ratio', fontsize=8)
ax1.set_ylim(-0.05, 1.05)
ax1.set_yticks([0, 0.25, 0.5, 0.75, 1.0])
ax1.tick_params(axis='both', which='major', labelsize=7)
ax1.spines['top'].set_visible(False)
ax1.spines['right'].set_visible(False)
plt.setp(ax1.get_xticklabels(), visible=False)
ax1.text(-0.08, 1.05, 'a', transform=ax1.transAxes, fontsize=10, fontweight='bold', va='top')

ax2.fill_between(positions, entropies, alpha=0.3, color=NATURE_COLORS['green'], linewidth=0)
ax2.plot(positions, entropies, color=NATURE_COLORS['green'], linewidth=1, alpha=0.8)
ax2.axhline(y=0.3, color=NATURE_COLORS['red'], linestyle='--', linewidth=0.8, alpha=0.7)
for pos in conserved_positions:
    if pos in positions and pos in conserved_entropies:
        idx = positions.index(pos)
        gap = gap_ratios[idx]
        entropy = conserved_entropies[pos]
        if gap < 0.1 and entropy < 0.3:
            ax2.scatter(pos, entropy, s=20, c=NATURE_COLORS['orange'], marker='*',
                      edgecolors='black', linewidths=0.3, zorder=5, alpha=0.9)
ax2.set_ylabel('Normalized entropy', fontsize=8)
ax2.set_ylim(-0.05, 1.05)
ax2.set_yticks([0, 0.25, 0.5, 0.75, 1.0])
ax2.tick_params(axis='both', which='major', labelsize=7)
ax2.spines['top'].set_visible(False)
ax2.spines['right'].set_visible(False)
plt.setp(ax2.get_xticklabels(), visible=False)
ax2.text(-0.08, 1.05, 'b', transform=ax2.transAxes, fontsize=10, fontweight='bold', va='top')

ax3.set_ylim(0, 2)
ax3.set_yticks([])
ax3.spines['top'].set_visible(False)
ax3.spines['right'].set_visible(False)
ax3.spines['left'].set_visible(False)
for pos in conserved_positions:
    if pos in positions:
        idx = positions.index(pos)
        gap = gap_ratios[idx]
        if gap < 0.1:
            ax3.axvline(x=pos, ymin=0.6, ymax=1.0, color=NATURE_COLORS['orange'], 
                       linewidth=1.5, alpha=0.8)
for pos in coevo_positions:
    if pos in positions:
        ax3.axvline(x=pos, ymin=0.0, ymax=0.4, color=NATURE_COLORS['purple'], 
                   linewidth=1.5, alpha=0.8)
legend_elements = [
    Line2D([0], [0], color=NATURE_COLORS['orange'], linewidth=2, label='Conserved (Gap<10%)'),
    Line2D([0], [0], color=NATURE_COLORS['purple'], linewidth=2, label='Coevolving (Top 10)')
]
ax3.legend(handles=legend_elements, loc='upper right', fontsize=6, frameon=False, ncol=2)
ax3.set_xlabel('Alignment position', fontsize=8)
ax3.set_xlim(min(positions), max(positions))
ax3.tick_params(axis='x', which='major', labelsize=7)
ax3.text(-0.08, 1.05, 'c', transform=ax3.transAxes, fontsize=10, fontweight='bold', va='top')

plt.tight_layout()
pdf_file = OUTPUT_DIR / 'figure_nature_01_conservation_landscape.pdf'
plt.savefig(pdf_file, dpi=300, bbox_inches='tight', format='pdf')
plt.close()

print(f"✅ PDF 版本已保存: {pdf_file}")

print("\n" + "=" * 80)
print("完成！")
print("=" * 80)

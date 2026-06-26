#!/bin/bash
# Visualization Script
# Generate publication-quality figures (300 DPI)

set -e

# Check arguments
if [ $# -lt 1 ]; then
    echo "Usage: $0 <output_dir>"
    echo ""
    echo "Example: $0 output/"
    exit 1
fi

OUTPUT_DIR=$1

# Create figures directory
mkdir -p "$OUTPUT_DIR/figures"

echo "========================================="
echo "Generating Figures"
echo "========================================="
echo "Output: $OUTPUT_DIR/figures/"
echo ""

# Check if required data files exist
if [ ! -f "$OUTPUT_DIR/conservation/conservation_detailed.csv" ]; then
    echo "Error: Conservation data not found. Run 02_conservation.sh first."
    exit 1
fi

if [ ! -f "$OUTPUT_DIR/coevolution/coevolution_detailed.csv" ]; then
    echo "Error: Coevolution data not found. Run 03_coevolution.sh first."
    exit 1
fi

if [ ! -f "$OUTPUT_DIR/phylogeny/tree.contree" ]; then
    echo "Error: Phylogenetic tree not found. Run 04_phylogeny.sh first."
    exit 1
fi

# Create Python script for all visualizations
cat > "$OUTPUT_DIR/figures/generate_figures.py" << 'PYTHON_EOF'
#!/usr/bin/env python3
"""
Generate all publication-quality figures
"""

import sys
import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import json
from Bio import Phylo

# Set publication-quality defaults
plt.rcParams['font.size'] = 12
plt.rcParams['axes.labelsize'] = 14
plt.rcParams['axes.titlesize'] = 16
plt.rcParams['xtick.labelsize'] = 10
plt.rcParams['ytick.labelsize'] = 10
plt.rcParams['legend.fontsize'] = 10
plt.rcParams['figure.dpi'] = 300

output_dir = sys.argv[1] if len(sys.argv) > 1 else '.'

print("Generating figures...")
print()

# Figure 1: Conservation Landscape
print("1. Conservation landscape...")
df_cons = pd.read_csv('../conservation/conservation_detailed.csv')

fig, ax = plt.subplots(figsize=(20, 4))

positions = df_cons['position'].values
entropies = df_cons['norm_entropy'].values

ax.fill_between(positions, 0, entropies, 
                 where=(entropies < 0.3), 
                 alpha=0.5, color='green', label='Highly conserved')
ax.fill_between(positions, 0, entropies, 
                 where=((entropies >= 0.3) & (entropies < 0.6)), 
                 alpha=0.5, color='yellow', label='Moderately conserved')
ax.fill_between(positions, 0, entropies, 
                 where=(entropies >= 0.6), 
                 alpha=0.5, color='red', label='Variable')

ax.plot(positions, entropies, linewidth=1, color='black')
ax.axhline(y=0.3, color='green', linestyle='--', linewidth=0.5)
ax.axhline(y=0.6, color='orange', linestyle='--', linewidth=0.5)

ax.set_xlabel('Alignment Position', fontsize=12)
ax.set_ylabel('Normalized Entropy', fontsize=12)
ax.set_title('Conservation Landscape', fontsize=14, fontweight='bold')
ax.legend(loc='upper right')
ax.set_ylim(0, 1)

plt.tight_layout()
plt.savefig(f'{output_dir}/conservation_landscape.png', dpi=300, bbox_inches='tight')
plt.close()
print("   ✓ conservation_landscape.png")

# Figure 2: Coevolution Network
print("2. Coevolution network...")
try:
    import networkx as nx
    
    with open('../coevolution/network_data.json', 'r') as f:
        data = json.load(f)
    
    G = nx.Graph()
    for node in data['nodes']:
        G.add_node(node['id'], degree=node['degree'])
    
    for edge in data['edges']:
        if edge['weight'] > 0.5:
            G.add_edge(edge['source'], edge['target'], weight=edge['weight'])
    
    if len(G.nodes()) > 0:
        pos = nx.spring_layout(G, k=0.5, iterations=50, seed=42)
        
        hub_threshold = 5
        node_colors = ['red' if G.nodes[node].get('degree', 0) >= hub_threshold 
                       else 'lightblue' for node in G.nodes()]
        node_sizes = [G.degree(node) * 100 for node in G.nodes()]
        edge_widths = [G[u][v]['weight'] * 5 for u, v in G.edges()]
        
        fig, ax = plt.subplots(figsize=(12, 12))
        
        nx.draw_networkx_nodes(G, pos, node_color=node_colors, 
                               node_size=node_sizes, alpha=0.7, ax=ax)
        nx.draw_networkx_edges(G, pos, width=edge_widths, 
                               alpha=0.3, edge_color='gray', ax=ax)
        nx.draw_networkx_labels(G, pos, font_size=8, ax=ax)
        
        ax.set_title('Coevolution Network (MI > 0.5)', fontsize=16, fontweight='bold')
        ax.axis('off')
        
        from matplotlib.patches import Patch
        legend_elements = [
            Patch(facecolor='red', label='Hub (degree ≥ 5)'),
            Patch(facecolor='lightblue', label='Non-hub')
        ]
        ax.legend(handles=legend_elements, loc='upper right')
        
        plt.tight_layout()
        plt.savefig(f'{output_dir}/coevolution_network.png', dpi=300, bbox_inches='tight')
        plt.close()
        print("   ✓ coevolution_network.png")
    else:
        print("   ⚠ No network to plot (no strong coevolution)")
except ImportError:
    print("   ⚠ NetworkX not installed, skipping network plot")

# Figure 3: Bootstrap Distribution
print("3. Bootstrap distribution...")
tree = Phylo.read('../phylogeny/tree.contree', 'newick')
bootstrap_values = []

for clade in tree.find_clades():
    if clade.confidence is not None:
        bootstrap_values.append(clade.confidence)

if len(bootstrap_values) > 0:
    fig, ax = plt.subplots(figsize=(10, 6))
    
    ax.hist(bootstrap_values, bins=20, color='steelblue', 
            edgecolor='black', alpha=0.7)
    
    ax.axvline(x=95, color='green', linestyle='--', linewidth=2,
               label='Strong support (≥95%)')
    ax.axvline(x=70, color='orange', linestyle='--', linewidth=2,
               label='Moderate support (≥70%)')
    
    ax.set_xlabel('Bootstrap Support (%)', fontsize=12)
    ax.set_ylabel('Frequency', fontsize=12)
    ax.set_title('Bootstrap Support Distribution', fontsize=14, fontweight='bold')
    ax.legend()
    
    mean_bs = np.mean(bootstrap_values)
    median_bs = np.median(bootstrap_values)
    ax.text(0.05, 0.95, f'Mean: {mean_bs:.1f}%\nMedian: {median_bs:.1f}%',
            transform=ax.transAxes, fontsize=10,
            verticalalignment='top', bbox=dict(boxstyle='round', facecolor='wheat'))
    
    plt.tight_layout()
    plt.savefig(f'{output_dir}/bootstrap_distribution.png', dpi=300, bbox_inches='tight')
    plt.close()
    print("   ✓ bootstrap_distribution.png")

# Figure 4: Hub Heatmap
print("4. Hub heatmap...")
df_coev = pd.read_csv('../coevolution/coevolution_detailed.csv')

hubs = []
try:
    with open('../coevolution/hub_positions.txt', 'r') as f:
        for line in f:
            if line.startswith('Position'):
                pos = int(line.split()[1].rstrip(':'))
                hubs.append(pos)
except:
    pass

if len(hubs) >= 2:
    hubs = hubs[:10]
    
    matrix = np.zeros((len(hubs), len(hubs)))
    
    for _, row in df_coev.iterrows():
        if row['pos1'] in hubs and row['pos2'] in hubs:
            i = hubs.index(row['pos1'])
            j = hubs.index(row['pos2'])
            matrix[i, j] = row['MI']
            matrix[j, i] = row['MI']
    
    fig, ax = plt.subplots(figsize=(10, 8))
    
    sns.heatmap(matrix, cmap='YlOrRd', 
                xticklabels=hubs, yticklabels=hubs,
                cbar_kws={'label': 'Mutual Information'},
                square=True, linewidths=0.5, ax=ax)
    
    ax.set_title('Hub Position Coevolution Heatmap', 
                 fontsize=14, fontweight='bold')
    ax.set_xlabel('Position', fontsize=12)
    ax.set_ylabel('Position', fontsize=12)
    
    plt.tight_layout()
    plt.savefig(f'{output_dir}/hub_heatmap.png', dpi=300, bbox_inches='tight')
    plt.close()
    print("   ✓ hub_heatmap.png")
else:
    print("   ⚠ Not enough hubs for heatmap")

# Figure 5: MI Distribution
print("5. MI distribution...")
fig, ax = plt.subplots(figsize=(10, 6))

MI_scores = df_coev['MI'].values

ax.hist(MI_scores, bins=50, color='steelblue', alpha=0.7, edgecolor='black')
ax.axvline(x=0.5, color='red', linestyle='--', linewidth=2,
           label='Strong coevolution threshold')

ax.set_xlabel('Mutual Information (MI)', fontsize=12)
ax.set_ylabel('Frequency', fontsize=12)
ax.set_title('Distribution of Coevolution Scores', fontsize=14, fontweight='bold')
ax.legend()

plt.tight_layout()
plt.savefig(f'{output_dir}/MI_distribution.png', dpi=300, bbox_inches='tight')
plt.close()
print("   ✓ MI_distribution.png")

print()
print("✓ All figures generated successfully!")
PYTHON_EOF

# Run visualization
cd "$OUTPUT_DIR/figures"
python3 generate_figures.py .
cd - > /dev/null

echo ""
echo "========================================="
echo "Visualization complete!"
echo "========================================="
echo "Generated figures:"
echo "  - $OUTPUT_DIR/figures/conservation_landscape.png"
echo "  - $OUTPUT_DIR/figures/coevolution_network.png"
echo "  - $OUTPUT_DIR/figures/bootstrap_distribution.png"
echo "  - $OUTPUT_DIR/figures/hub_heatmap.png"
echo "  - $OUTPUT_DIR/figures/MI_distribution.png"
echo ""
echo "All figures are 300 DPI, publication-ready."
echo ""

#!/usr/bin/env python3
"""
Complete Phylogenetic Analysis Pipeline
Performs conservation, coevolution, and generates all figures
"""

import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from Bio import AlignIO, Phylo
from collections import Counter
from itertools import combinations
import json
import pandas as pd
import sys
import os

# Set high-quality output
plt.rcParams['font.sans-serif'] = ['Arial', 'DejaVu Sans']
plt.rcParams['axes.unicode_minus'] = False
plt.rcParams['figure.dpi'] = 300
plt.rcParams['savefig.dpi'] = 300
plt.rcParams['figure.figsize'] = (12, 8)

def calculate_conservation(alignment):
    """Calculate Shannon entropy for each position"""
    print("\n" + "="*80)
    print("Conservation Analysis")
    print("="*80)
    
    conservation_data = []
    
    for i in range(alignment.get_alignment_length()):
        column = alignment[:, i]
        column_no_gap = [aa for aa in column if aa != '-']
        
        if len(column_no_gap) == 0:
            continue
        
        # Count amino acids
        aa_counts = Counter(column_no_gap)
        total = len(column_no_gap)
        
        # Calculate Shannon entropy
        entropy = 0
        for count in aa_counts.values():
            if count > 0:
                p = count / total
                entropy -= p * np.log2(p)
        
        # Normalize
        max_entropy = np.log2(min(20, len(aa_counts)))
        norm_entropy = entropy / max_entropy if max_entropy > 0 else 0
        
        # Most common amino acid
        most_common = aa_counts.most_common(1)[0]
        
        # Gap ratio
        gap_count = column.count('-')
        gap_ratio = gap_count / len(alignment)
        
        # Category
        if norm_entropy < 0.3:
            category = "Highly conserved"
        elif norm_entropy < 0.6:
            category = "Moderately conserved"
        else:
            category = "Variable"
        
        conservation_data.append({
            'position': i + 1,
            'entropy': entropy,
            'norm_entropy': norm_entropy,
            'most_common_aa': most_common[0],
            'most_common_freq': most_common[1] / total,
            'gap_ratio': gap_ratio,
            'num_variants': len(aa_counts),
            'category': category
        })
    
    df = pd.DataFrame(conservation_data)
    
    # Summary
    highly_conserved = df[df['norm_entropy'] < 0.3]
    moderately_conserved = df[(df['norm_entropy'] >= 0.3) & (df['norm_entropy'] < 0.6)]
    variable = df[df['norm_entropy'] >= 0.6]
    
    print(f"\nTotal positions: {len(df)}")
    print(f"Highly conserved (H < 0.3): {len(highly_conserved)} ({len(highly_conserved)/len(df)*100:.1f}%)")
    print(f"Moderately conserved (0.3 ≤ H < 0.6): {len(moderately_conserved)} ({len(moderately_conserved)/len(df)*100:.1f}%)")
    print(f"Variable (H ≥ 0.6): {len(variable)} ({len(variable)/len(df)*100:.1f}%)")
    
    print("\nTop 10 conserved positions:")
    for _, row in df.nsmallest(10, 'norm_entropy').iterrows():
        print(f"  Position {row['position']:3d} ({row['most_common_aa']}): H = {row['norm_entropy']:.3f}")
    
    return df

def calculate_coevolution(alignment, conservation_df):
    """Calculate Normalized Mutual Information for all position pairs"""
    print("\n" + "="*80)
    print("Coevolution Analysis")
    print("="*80)
    
    aln_length = alignment.get_alignment_length()
    coevolution_data = []
    
    print(f"\nCalculating MI for {aln_length * (aln_length - 1) // 2} position pairs...")
    
    for i in range(aln_length):
        if (i + 1) % 10 == 0:
            print(f"  Position {i + 1}/{aln_length}")
        
        for j in range(i + 1, aln_length):
            # Extract columns
            col_i = alignment[:, i]
            col_j = alignment[:, j]
            
            # Remove gaps
            pairs = [(col_i[k], col_j[k]) for k in range(len(alignment)) 
                     if col_i[k] != '-' and col_j[k] != '-']
            
            if len(pairs) < 10:  # Skip if too few pairs
                continue
            
            # Count pairs
            pair_counts = Counter(pairs)
            total = len(pairs)
            
            # Marginal counts
            aa_i_counts = Counter([p[0] for p in pairs])
            aa_j_counts = Counter([p[1] for p in pairs])
            
            # Calculate MI
            MI = 0
            for (aa_i, aa_j), count in pair_counts.items():
                p_ij = count / total
                p_i = aa_i_counts[aa_i] / total
                p_j = aa_j_counts[aa_j] / total
                
                if p_ij > 0 and p_i > 0 and p_j > 0:
                    MI += p_ij * np.log2(p_ij / (p_i * p_j))
            
            # Calculate entropies for normalization
            H_i = -sum((c/total) * np.log2(c/total) for c in aa_i_counts.values() if c > 0)
            H_j = -sum((c/total) * np.log2(c/total) for c in aa_j_counts.values() if c > 0)
            
            # Normalize MI
            if H_i > 0 and H_j > 0:
                NMI = MI / np.sqrt(H_i * H_j)
            else:
                NMI = 0
            
            coevolution_data.append({
                'pos1': i + 1,
                'pos2': j + 1,
                'MI': MI,
                'NMI': NMI,
                'num_pairs': len(pairs)
            })
    
    df = pd.DataFrame(coevolution_data)
    df = df.sort_values('MI', ascending=False)
    
    # Summary
    strong = df[df['MI'] > 0.5]
    moderate = df[(df['MI'] > 0.3) & (df['MI'] <= 0.5)]
    
    print(f"\nTotal pairs: {len(df)}")
    print(f"Strong coevolution (MI > 0.5): {len(strong)} ({len(strong)/len(df)*100:.1f}%)")
    print(f"Moderate coevolution (0.3 < MI ≤ 0.5): {len(moderate)} ({len(moderate)/len(df)*100:.1f}%)")
    
    print("\nTop 10 coevolved pairs:")
    for _, row in df.head(10).iterrows():
        print(f"  {row['pos1']:3d} ↔ {row['pos2']:3d}: MI = {row['MI']:.3f}")
    
    # Identify hubs
    hub_counts = {}
    for _, row in df[df['MI'] > 0.5].iterrows():
        hub_counts[row['pos1']] = hub_counts.get(row['pos1'], 0) + 1
        hub_counts[row['pos2']] = hub_counts.get(row['pos2'], 0) + 1
    
    hubs = sorted(hub_counts.items(), key=lambda x: x[1], reverse=True)
    hubs = [(pos, deg) for pos, deg in hubs if deg >= 5]
    
    print(f"\nHub positions (degree ≥ 5): {len(hubs)}")
    for pos, degree in hubs[:10]:
        print(f"  Position {pos:3d}: Degree {degree}")
    
    return df, hubs

def generate_figures(alignment, conservation_df, coevolution_df, hubs, output_dir):
    """Generate all publication-quality figures"""
    print("\n" + "="*80)
    print("Generating Figures")
    print("="*80)
    
    os.makedirs(output_dir, exist_ok=True)
    
    # Figure 1: Conservation landscape
    print("\n1. Conservation landscape...")
    fig, ax = plt.subplots(figsize=(20, 4))
    
    positions = conservation_df['position'].values
    entropies = conservation_df['norm_entropy'].values
    
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
    
    # Figure 2: Coevolution network
    print("2. Coevolution network...")
    try:
        import networkx as nx
        
        G = nx.Graph()
        for pos, degree in hubs:
            G.add_node(pos, degree=degree)
        
        for _, row in coevolution_df[coevolution_df['MI'] > 0.5].iterrows():
            if row['pos1'] in [h[0] for h in hubs] or row['pos2'] in [h[0] for h in hubs]:
                G.add_edge(row['pos1'], row['pos2'], weight=row['MI'])
        
        if len(G.nodes()) > 0:
            pos = nx.spring_layout(G, k=0.5, iterations=50, seed=42)
            
            node_colors = ['red' if G.nodes[node].get('degree', 0) >= 5 
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
    except ImportError:
        print("   ⚠ NetworkX not installed, skipping network plot")
    
    # Figure 3: Hub heatmap
    print("3. Hub heatmap...")
    if len(hubs) >= 2:
        hub_positions = [h[0] for h in hubs[:10]]
        
        matrix = np.zeros((len(hub_positions), len(hub_positions)))
        
        for _, row in coevolution_df.iterrows():
            if row['pos1'] in hub_positions and row['pos2'] in hub_positions:
                i = hub_positions.index(row['pos1'])
                j = hub_positions.index(row['pos2'])
                matrix[i, j] = row['MI']
                matrix[j, i] = row['MI']
        
        fig, ax = plt.subplots(figsize=(10, 8))
        
        sns.heatmap(matrix, cmap='YlOrRd', 
                    xticklabels=hub_positions, 
                    yticklabels=hub_positions,
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
    
    # Figure 4: MI distribution
    print("4. MI distribution...")
    fig, ax = plt.subplots(figsize=(10, 6))
    
    MI_scores = coevolution_df['MI'].values
    
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
    
    # Figure 5: Bootstrap distribution (if tree exists)
    print("5. Bootstrap distribution...")
    tree_file = "tree.contree"
    if os.path.exists(tree_file):
        tree = Phylo.read(tree_file, 'newick')
        bootstrap_values = [c.confidence for c in tree.find_clades() if c.confidence is not None]
        
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
    else:
        print("   ⚠ Tree file not found, skipping bootstrap plot")
    
    print(f"\n✓ All figures saved to: {output_dir}/")

def main():
    if len(sys.argv) < 3:
        print("Usage: python complete_analysis.py <aligned.fasta> <output_dir>")
        print("\nExample: python complete_analysis.py aligned.fasta output/")
        sys.exit(1)
    
    aligned_fasta = sys.argv[1]
    output_dir = sys.argv[2]
    
    print("="*80)
    print("Complete Phylogenetic Analysis Pipeline")
    print("="*80)
    print(f"\nInput: {aligned_fasta}")
    print(f"Output: {output_dir}/")
    
    # Read alignment
    print("\nReading alignment...")
    alignment = AlignIO.read(aligned_fasta, "fasta")
    print(f"  Sequences: {len(alignment)}")
    print(f"  Alignment length: {alignment.get_alignment_length()}")
    
    # 1. Conservation analysis
    conservation_df = calculate_conservation(alignment)
    conservation_df.to_csv(f'{output_dir}/conservation_detailed.csv', index=False)
    print(f"\n✓ Conservation results saved to: {output_dir}/conservation_detailed.csv")
    
    # 2. Coevolution analysis
    coevolution_df, hubs = calculate_coevolution(alignment, conservation_df)
    coevolution_df.to_csv(f'{output_dir}/coevolution_detailed.csv', index=False)
    print(f"\n✓ Coevolution results saved to: {output_dir}/coevolution_detailed.csv")
    
    # Save hubs
    with open(f'{output_dir}/hub_positions.txt', 'w') as f:
        f.write("Hub Positions (degree ≥ 5)\n")
        f.write("="*60 + "\n")
        for pos, degree in hubs:
            f.write(f"Position {pos}: Degree {degree}\n")
    print(f"✓ Hub positions saved to: {output_dir}/hub_positions.txt")
    
    # Save network data
    network_data = {
        'nodes': [{'id': pos, 'degree': degree} for pos, degree in hubs],
        'edges': [
            {
                'source': int(row['pos1']),
                'target': int(row['pos2']),
                'weight': float(row['MI'])
            }
            for _, row in coevolution_df[coevolution_df['MI'] > 0.5].iterrows()
        ]
    }
    
    with open(f'{output_dir}/network_data.json', 'w') as f:
        json.dump(network_data, f, indent=2)
    print(f"✓ Network data saved to: {output_dir}/network_data.json")
    
    # 3. Generate figures
    generate_figures(alignment, conservation_df, coevolution_df, hubs, output_dir)
    
    print("\n" + "="*80)
    print("Analysis Complete!")
    print("="*80)
    print(f"\nOutput files:")
    print(f"  - {output_dir}/conservation_detailed.csv")
    print(f"  - {output_dir}/coevolution_detailed.csv")
    print(f"  - {output_dir}/hub_positions.txt")
    print(f"  - {output_dir}/network_data.json")
    print(f"  - {output_dir}/conservation_landscape.png")
    print(f"  - {output_dir}/coevolution_network.png")
    print(f"  - {output_dir}/hub_heatmap.png")
    print(f"  - {output_dir}/MI_distribution.png")
    print(f"  - {output_dir}/bootstrap_distribution.png (if tree exists)")

if __name__ == "__main__":
    main()

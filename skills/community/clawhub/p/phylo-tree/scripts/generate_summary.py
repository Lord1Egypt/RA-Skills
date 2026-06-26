#!/usr/bin/env python3
"""
Generate structured summary for AI consumption
Extract key statistics from analysis outputs
"""

import json
import re
from pathlib import Path
import sys

def extract_iqtree_stats(log_file):
    """Extract statistics from IQ-TREE log"""
    stats = {}
    
    with open(log_file) as f:
        content = f.read()
    
    # Extract model
    model_match = re.search(r'Best-fit model: (\S+)', content)
    if model_match:
        stats['best_model'] = model_match.group(1)
    
    # Extract log-likelihood
    logl_match = re.search(r'BEST SCORE FOUND : ([-\d.]+)', content)
    if logl_match:
        stats['log_likelihood'] = float(logl_match.group(1))
    
    # Extract tree length
    tree_length_match = re.search(r'Total tree length: ([\d.]+)', content)
    if tree_length_match:
        stats['tree_length'] = float(tree_length_match.group(1))
    
    # Extract number of sequences
    seq_match = re.search(r'(\d+) sequences', content)
    if seq_match:
        stats['num_sequences'] = int(seq_match.group(1))
    
    # Extract alignment length
    sites_match = re.search(r'(\d+) sites', content)
    if sites_match:
        stats['alignment_length'] = int(sites_match.group(1))
    
    return stats

def extract_alignment_stats(log_file):
    """Extract alignment statistics"""
    stats = {}
    
    if not Path(log_file).exists():
        return stats
    
    with open(log_file) as f:
        content = f.read()
    
    # Extract gap percentage
    gap_match = re.search(r'Gap/Ambiguity.*?([\d.]+)%', content)
    if gap_match:
        stats['gap_percentage'] = float(gap_match.group(1))
    
    return stats

def count_high_support_nodes(tree_file):
    """Count nodes with high support values"""
    if not Path(tree_file).exists():
        return {}
    
    with open(tree_file) as f:
        tree_content = f.read()
    
    # Count support values
    support_values = re.findall(r'\)(\d+(?:\.\d+)?)/(\d+(?:\.\d+)?)', tree_content)
    
    high_support = 0
    total = len(support_values)
    
    for sh_alrt, ufboot in support_values:
        sh_alrt = float(sh_alrt)
        ufboot = float(ufboot)
        if sh_alrt >= 80 or ufboot >= 95:
            high_support += 1
    
    return {
        'total_nodes': total,
        'high_support_nodes': high_support,
        'high_support_percentage': round(high_support / total * 100, 1) if total > 0 else 0
    }

def main():
    if len(sys.argv) < 2:
        print("Usage: python3 generate_summary.py <project_dir>")
        sys.exit(1)
    
    project_dir = Path(sys.argv[1])
    
    # Collect statistics
    summary = {
        'project_dir': str(project_dir),
        'iqtree': {},
        'alignment': {},
        'support': {},
        'files': {}
    }
    
    # IQ-TREE statistics
    iqtree_log = project_dir / 'trees' / 'phylo.log'
    if iqtree_log.exists():
        summary['iqtree'] = extract_iqtree_stats(iqtree_log)
    
    # Alignment statistics
    mafft_log = project_dir / 'logs' / 'mafft.log'
    if mafft_log.exists():
        summary['alignment'] = extract_alignment_stats(mafft_log)
    
    # Support values
    tree_file = project_dir / 'trees' / 'phylo.treefile'
    if tree_file.exists():
        summary['support'] = count_high_support_nodes(tree_file)
    
    # List important files
    summary['files'] = {
        'tree': str(tree_file) if tree_file.exists() else None,
        'alignment': str(project_dir / 'alignment' / 'trimmed.fasta'),
        'figures': list(str(f) for f in (project_dir / 'figures').glob('*.png')) if (project_dir / 'figures').exists() else []
    }
    
    # Save summary
    summary_file = project_dir / 'analysis_summary.json'
    with open(summary_file, 'w') as f:
        json.dump(summary, f, indent=2)
    
    print(f"✓ Summary saved to: {summary_file}")
    print(f"\nKey Statistics:")
    print(f"  Sequences: {summary['iqtree'].get('num_sequences', 'N/A')}")
    print(f"  Best model: {summary['iqtree'].get('best_model', 'N/A')}")
    print(f"  Log-likelihood: {summary['iqtree'].get('log_likelihood', 'N/A')}")
    print(f"  High support nodes: {summary['support'].get('high_support_nodes', 'N/A')}/{summary['support'].get('total_nodes', 'N/A')} ({summary['support'].get('high_support_percentage', 'N/A')}%)")

if __name__ == '__main__':
    main()

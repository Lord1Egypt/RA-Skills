#!/usr/bin/env python3
"""
PhyloTree - 酶系统发育树分析全流程
Usage:
  python3 run.py --query "enzyme name" --output ./output
  python3 run.py --fasta input.fasta --output ./output
"""

import argparse
import subprocess
import json
import sys
import os
import time
import requests
from pathlib import Path
from datetime import datetime

SKILL_DIR = Path(__file__).parent.parent
SCRIPTS = SKILL_DIR / "scripts"

def setup_project(output_dir, query_name="unknown"):
    """Create project structure"""
    p = Path(output_dir)
    for sub in ["sequences", "alignment", "trees", "figures", "logs"]:
        (p / sub).mkdir(parents=True, exist_ok=True)
    return p

def collect_by_name(query, project_dir):
    """Collect sequences by enzyme name from UniProt"""
    print(f"[1] Searching UniProt for: {query}")
    url = "https://rest.uniprot.org/uniprotkb/search"
    params = {"query": query, "format": "json", "size": 500}
    
    resp = requests.get(url, params=params, timeout=120)
    resp.raise_for_status()
    results = resp.json().get("results", [])
    print(f"    Found {len(results)} sequences")
    
    # Filter and save
    entries = []
    fasta_lines = []
    for r in results:
        seq = r.get("sequence", {}).get("value", "")
        length = len(seq)
        if 100 <= length <= 1000:
            acc = r.get("primaryAccession", "")
            org = r.get("organism", {}).get("scientificName", "Unknown")
            name = r.get("proteinDescription", {}).get("recommendedName", {}).get("fullName", {}).get("value", "Unknown")
            entries.append({"accession": acc, "organism": org, "protein_name": name, "sequence": seq, "length": length})
            fasta_lines.append(f">{acc}|{org}|{name}")
            for i in range(0, len(seq), 80):
                fasta_lines.append(seq[i:i+80])
    
    fasta_file = project_dir / "sequences" / "sequences.fasta"
    with open(fasta_file, "w") as f:
        f.write("\n".join(fasta_lines) + "\n")
    
    meta_file = project_dir / "sequences" / "metadata.json"
    with open(meta_file, "w") as f:
        json.dump(entries, f, indent=2)
    
    print(f"    Saved {len(entries)} sequences to {fasta_file}")
    return fasta_file, len(entries)

def collect_by_fasta(fasta_input, project_dir):
    """Process input FASTA, search for homologs"""
    print(f"[1] Processing input FASTA: {fasta_input}")
    # Copy input as query
    import shutil
    query_file = project_dir / "sequences" / "query.fasta"
    shutil.copy(fasta_input, query_file)
    
    # Use the input sequences directly for phylogeny
    # (in a full version, would BLAST for homologs)
    print(f"    Using input sequences for analysis")
    return query_file, "input"

def align_and_tree(fasta_file, project_dir):
    """Step 2: MSA + Tree"""
    print("\n[2] Multiple Sequence Alignment (MAFFT)")
    aligned = project_dir / "alignment" / "aligned.fasta"
    subprocess.run([
        "mafft", "--auto", "--thread", str(os.cpu_count() or 4),
        str(fasta_file)
    ], stdout=open(aligned, "w"), stderr=subprocess.PIPE, check=True)
    print(f"    Aligned: {aligned}")
    
    print("\n[3] Phylogenetic Tree (FastTree)")
    tree_file = project_dir / "trees" / "tree.nwk"
    log_file = project_dir / "logs" / "fasttree.log"
    subprocess.run([
        "fasttree", "-gamma", str(aligned)
    ], stdout=open(tree_file, "w"), stderr=open(log_file, "w"), check=True)
    print(f"    Tree: {tree_file}")
    
    # Root the tree
    print("\n[3b] Rooting tree (R/ape)")
    subprocess.run([
        "Rscript", "-e", f'''
        library(ape)
        t <- midpoint(read.tree("{tree_file}"))
        write.tree(t, "{project_dir / "trees" / "tree_rooted.nwk"}")
        cat("Rooted tree saved\n")
        '''
    ], check=True)
    
    return tree_file

def visualize(tree_file, project_dir):
    """Step 4: Visualization"""
    print("\n[4] Visualization")
    fig_dir = project_dir / "figures"
    
    r_script = SCRIPTS / "visualize.R"
    if r_script.exists():
        env = os.environ.copy()
        env["TREE_FILE"] = str(tree_file)
        env["FIG_DIR"] = str(fig_dir)
        subprocess.run(["Rscript", str(r_script)], env=env, check=True)
    else:
        # Inline minimal visualization
        subprocess.run([
            "Rscript", "-e", f'''
            library(ape)
            tree <- read.tree("{tree_file}")
            pdf("{fig_dir}/tree_circular.pdf", 12, 12)
            plot(midpoint(tree), type="fan", cex=0.5, main="Phylogenetic Tree")
            dev.off()
            pdf("{fig_dir}/tree_rectangular.pdf", 16, 20)
            plot(midpoint(tree), type="phylogram", cex=0.4)
            dev.off()
            cat("Plots saved\n")
            '''
        ], check=True)
    
    print(f"    Figures saved to: {fig_dir}")

def generate_report(project_dir, n_seqs, query):
    """Step 5: Generate report"""
    print("\n[5] Generating Report")
    report = project_dir / "REPORT.md"
    
    # Get tree stats
    stats = subprocess.run([
        "Rscript", "-e", f'''
        library(ape)
        t <- read.tree("{project_dir / "trees" / "tree_rooted.nwk"}")
        cat(length(t$tip.label), max(node.depth.edgelength(t)), mean(t$edge.length), sep="|")
        '''
    ], capture_output=True, text=True).stdout.strip().split("|")
    
    with open(report, "w") as f:
        f.write(f"""# 系统发育树分析报告

**查询:** {query}
**日期:** {datetime.now().strftime("%Y-%m-%d")}

## 数据
- 序列数: {n_seqs}
- 树高: {stats[1] if len(stats) > 1 else "N/A"}
- 平均分支长度: {stats[2] if len(stats) > 2 else "N/A"}

## 方法
1. UniProt 序列收集
2. MAFFT 多序列比对
3. FastTree 最大似然建树
4. R/ape 可视化

## 输出文件
| 文件 | 说明 |
|------|------|
| trees/tree_rooted.nwk | 系统发育树 |
| figures/tree_circular.pdf | 环形树图 |
| figures/tree_rectangular.pdf | 矩形树图 |
""")
    print(f"    Report: {report}")

def main():
    parser = argparse.ArgumentParser(description="PhyloTree: Enzyme Phylogenetic Analysis")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--query", help="Enzyme name to search UniProt")
    group.add_argument("--fasta", help="Input FASTA file with sequences")
    parser.add_argument("--output", default="./phylo_output", help="Output directory")
    args = parser.parse_args()
    
    query = args.query or args.fasta
    project = setup_project(args.output, query)
    
    print("=" * 60)
    print("PhyloTree - Enzyme Phylogenetic Analysis")
    print("=" * 60)
    
    if args.query:
        fasta_file, n_seqs = collect_by_name(args.query, project)
    else:
        fasta_file, n_seqs = collect_by_fasta(args.fasta, project)
    
    if isinstance(n_seqs, str):
        # Count sequences in input file
        n_seqs = sum(1 for line in open(fasta_file) if line.startswith(">"))
    
    tree_file = align_and_tree(fasta_file, project)
    visualize(tree_file, project)
    generate_report(project, n_seqs, query)
    
    print("\n" + "=" * 60)
    print(f"✅ Analysis complete! Output: {project}")
    print("=" * 60)

if __name__ == "__main__":
    main()

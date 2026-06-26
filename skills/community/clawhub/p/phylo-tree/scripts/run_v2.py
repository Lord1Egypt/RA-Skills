#!/usr/bin/env python3
"""
PhyloTree - Publication-Grade Phylogenetic Tree Analysis
=========================================================

A complete pipeline for constructing publication-quality phylogenetic trees
suitable for Nature/Science/Cell-level journals.

Usage:
  python3 run.py --query "enzyme name" --output ./output
  python3 run.py --fasta input.fasta --output ./output
  python3 run.py --query "imine reductase" --output ./ired_analysis --threads 10

Author: PhyloTree Skill
Version: 2.0.0 (Publication Grade)
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
from typing import Tuple, Dict, List

# Skill directory
SKILL_DIR = Path(__file__).parent.parent
SCRIPTS = SKILL_DIR / "scripts"

# Color codes for terminal output
class Colors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'

def print_stage(stage_num: int, stage_name: str):
    """Print stage header"""
    print(f"\n{Colors.HEADER}{'='*70}{Colors.ENDC}")
    print(f"{Colors.HEADER}Stage {stage_num}: {stage_name}{Colors.ENDC}")
    print(f"{Colors.HEADER}{'='*70}{Colors.ENDC}\n")

def print_success(message: str):
    """Print success message"""
    print(f"{Colors.OKGREEN}✓ {message}{Colors.ENDC}")

def print_info(message: str):
    """Print info message"""
    print(f"{Colors.OKBLUE}→ {message}{Colors.ENDC}")

def print_warning(message: str):
    """Print warning message"""
    print(f"{Colors.WARNING}⚠ {message}{Colors.ENDC}")

def print_error(message: str):
    """Print error message"""
    print(f"{Colors.FAIL}✗ {message}{Colors.ENDC}")

def setup_project(output_dir: str, query_name: str = "unknown") -> Path:
    """
    Create project directory structure
    
    Structure:
        output/
        ├── sequences/      # Raw and processed sequences
        ├── alignment/      # MSA files
        ├── trees/          # Tree files
        ├── figures/        # Publication-grade figures
        ├── reports/        # QC and analysis reports
        └── logs/           # Log files
    """
    p = Path(output_dir)
    for sub in ["sequences", "alignment", "trees", "figures", "reports", "logs"]:
        (p / sub).mkdir(parents=True, exist_ok=True)
    
    # Create metadata file
    metadata = {
        "project_name": query_name,
        "created_at": datetime.now().isoformat(),
        "pipeline_version": "2.0.0",
        "stages_completed": []
    }
    with open(p / "metadata.json", "w") as f:
        json.dump(metadata, f, indent=2)
    
    return p

# ============================================================================
# Stage 1: Data Collection and Preprocessing
# ============================================================================

def collect_sequences_uniprot(query: str, project_dir: Path, 
                               max_seqs: int = 1000,
                               min_length: int = 150,
                               max_length: int = 600) -> Tuple[Path, int]:
    """
    Collect sequences from UniProt with filtering
    
    Args:
        query: Search query (e.g., "imine reductase")
        project_dir: Project directory
        max_seqs: Maximum number of sequences to retrieve
        min_length: Minimum sequence length
        max_length: Maximum sequence length
    
    Returns:
        (fasta_file_path, number_of_sequences)
    """
    print_info(f"Searching UniProt for: {query}")
    print_info(f"Filters: length {min_length}-{max_length} aa, max {max_seqs} sequences")
    
    url = "https://rest.uniprot.org/uniprotkb/search"
    params = {
        "query": query,
        "format": "json",
        "size": max_seqs
    }
    
    try:
        resp = requests.get(url, params=params, timeout=120)
        resp.raise_for_status()
        results = resp.json().get("results", [])
        print_info(f"Retrieved {len(results)} sequences from UniProt")
    except Exception as e:
        print_error(f"Failed to retrieve sequences: {e}")
        sys.exit(1)
    
    # Filter and save
    entries = []
    fasta_lines = []
    
    for r in results:
        seq = r.get("sequence", {}).get("value", "")
        length = len(seq)
        
        # Length filter
        if not (min_length <= length <= max_length):
            continue
        
        acc = r.get("primaryAccession", "")
        org = r.get("organism", {}).get("scientificName", "Unknown")
        name = r.get("proteinDescription", {}).get("recommendedName", {}).get("fullName", {}).get("value", "Unknown")
        
        entries.append({
            "accession": acc,
            "organism": org,
            "protein_name": name,
            "sequence": seq,
            "length": length
        })
        
        # FASTA format
        fasta_lines.append(f">{acc}|{org}|{name}")
        for i in range(0, len(seq), 80):
            fasta_lines.append(seq[i:i+80])
    
    # Save raw sequences
    raw_fasta = project_dir / "sequences" / "raw.fasta"
    with open(raw_fasta, "w") as f:
        f.write("\n".join(fasta_lines) + "\n")
    
    # Save metadata
    meta_file = project_dir / "sequences" / "metadata.json"
    with open(meta_file, "w") as f:
        json.dump(entries, f, indent=2)
    
    print_success(f"Saved {len(entries)} sequences to {raw_fasta}")
    
    # Generate QC report
    generate_sequence_qc_report(entries, project_dir)
    
    return raw_fasta, len(entries)

def generate_sequence_qc_report(entries: List[Dict], project_dir: Path):
    """Generate QC report for collected sequences"""
    lengths = [e["length"] for e in entries]
    organisms = [e["organism"] for e in entries]
    
    # Statistics
    stats = {
        "total_sequences": len(entries),
        "length_min": min(lengths),
        "length_max": max(lengths),
        "length_mean": sum(lengths) / len(lengths),
        "length_median": sorted(lengths)[len(lengths)//2],
        "unique_organisms": len(set(organisms)),
        "top_10_organisms": {}
    }
    
    # Top 10 organisms
    from collections import Counter
    org_counts = Counter(organisms)
    stats["top_10_organisms"] = dict(org_counts.most_common(10))
    
    # Save report
    report_file = project_dir / "reports" / "01_sequence_collection_qc.json"
    with open(report_file, "w") as f:
        json.dump(stats, f, indent=2)
    
    print_info(f"QC Report: {len(entries)} sequences, {stats['unique_organisms']} organisms")
    print_info(f"Length: {stats['length_min']}-{stats['length_max']} aa (mean: {stats['length_mean']:.1f})")

def deduplicate_sequences(input_fasta: Path, output_fasta: Path, 
                          identity: float = 0.90, threads: int = 10,
                          memory_mb: int = 8000) -> int:
    """
    Remove redundant sequences using CD-HIT
    
    Args:
        input_fasta: Input FASTA file
        output_fasta: Output FASTA file
        identity: Identity threshold (0.90 = 90%)
        threads: Number of CPU threads
        memory_mb: Memory limit in MB
    
    Returns:
        Number of sequences after deduplication
    """
    print_info(f"Running CD-HIT with {identity*100}% identity threshold")
    
    cmd = [
        "/root/miniconda3/envs/r43/bin/cd-hit",
        "-i", str(input_fasta),
        "-o", str(output_fasta),
        "-c", str(identity),
        "-n", "5",  # word size
        "-M", str(memory_mb),
        "-T", str(threads),
        "-d", "0"  # full description in output
    ]
    
    log_file = output_fasta.parent.parent / "logs" / "cd-hit.log"
    
    try:
        with open(log_file, "w") as log:
            subprocess.run(cmd, stdout=log, stderr=subprocess.STDOUT, check=True)
        print_success(f"CD-HIT completed, log: {log_file}")
    except subprocess.CalledProcessError as e:
        print_error(f"CD-HIT failed: {e}")
        sys.exit(1)
    
    # Count sequences
    n_seqs = sum(1 for line in open(output_fasta) if line.startswith(">"))
    print_info(f"Sequences after deduplication: {n_seqs}")
    
    return n_seqs

# ============================================================================
# Stage 2: Multiple Sequence Alignment
# ============================================================================

def run_mafft(input_fasta: Path, output_fasta: Path, 
              threads: int = 10, algorithm: str = "auto") -> None:
    """
    Run MAFFT for multiple sequence alignment
    
    Args:
        input_fasta: Input FASTA file
        output_fasta: Output aligned FASTA file
        threads: Number of CPU threads
        algorithm: MAFFT algorithm (auto, linsi, ginsi, einsi)
    """
    print_info(f"Running MAFFT with {algorithm} algorithm")
    
    # Choose algorithm based on sequence count
    n_seqs = sum(1 for line in open(input_fasta) if line.startswith(">"))
    
    if algorithm == "auto":
        if n_seqs < 200:
            cmd = ["mafft", "--localpair", "--maxiterate", "1000"]
            print_info("Using L-INS-i (high accuracy, < 200 sequences)")
        elif n_seqs < 2000:
            cmd = ["mafft", "--auto"]
            print_info("Using auto mode (200-2000 sequences)")
        else:
            cmd = ["mafft", "--retree", "2"]
            print_info("Using FFT-NS-2 (fast, > 2000 sequences)")
    elif algorithm == "linsi":
        cmd = ["mafft", "--localpair", "--maxiterate", "1000"]
    elif algorithm == "ginsi":
        cmd = ["mafft", "--globalpair", "--maxiterate", "1000"]
    elif algorithm == "einsi":
        cmd = ["mafft", "--ep", "0", "--genafpair", "--maxiterate", "1000"]
    else:
        cmd = ["mafft", "--auto"]
    
    cmd.extend(["--thread", str(threads), str(input_fasta)])
    
    log_file = output_fasta.parent.parent / "logs" / "mafft.log"
    
    try:
        with open(output_fasta, "w") as out, open(log_file, "w") as log:
            subprocess.run(cmd, stdout=out, stderr=log, check=True)
        print_success(f"MAFFT completed, alignment: {output_fasta}")
    except subprocess.CalledProcessError as e:
        print_error(f"MAFFT failed: {e}")
        sys.exit(1)
    
    # Generate alignment QC
    generate_alignment_qc_report(output_fasta, output_fasta.parent.parent)

def generate_alignment_qc_report(alignment_file: Path, project_dir: Path):
    """Generate QC report for alignment"""
    from Bio import AlignIO
    
    try:
        alignment = AlignIO.read(alignment_file, "fasta")
    except:
        print_warning("BioPython not available, skipping alignment QC")
        return
    
    n_seqs = len(alignment)
    aln_length = alignment.get_alignment_length()
    
    # Calculate gap statistics
    gap_counts = []
    for record in alignment:
        gaps = str(record.seq).count("-")
        gap_counts.append(gaps / aln_length)
    
    avg_gap = sum(gap_counts) / len(gap_counts)
    
    stats = {
        "n_sequences": n_seqs,
        "alignment_length": aln_length,
        "average_gap_proportion": avg_gap,
        "max_gap_proportion": max(gap_counts),
        "min_gap_proportion": min(gap_counts)
    }
    
    report_file = project_dir / "reports" / "02_alignment_qc.json"
    with open(report_file, "w") as f:
        json.dump(stats, f, indent=2)
    
    print_info(f"Alignment: {n_seqs} sequences × {aln_length} sites")
    print_info(f"Average gap proportion: {avg_gap*100:.1f}%")

# ============================================================================
# Stage 3: Alignment Trimming
# ============================================================================

def run_trimal(input_fasta: Path, output_fasta: Path, method: str = "automated1") -> None:
    """
    Run trimAl to remove poorly aligned regions
    
    Args:
        input_fasta: Input aligned FASTA file
        output_fasta: Output trimmed FASTA file
        method: Trimming method (automated1, gappyout, strict, etc.)
    """
    print_info(f"Running trimAl with {method} method")
    
    cmd = [
        "/root/miniconda3/envs/r43/bin/trimal",
        "-in", str(input_fasta),
        "-out", str(output_fasta),
        f"-{method}"
    ]
    
    log_file = output_fasta.parent.parent / "logs" / "trimal.log"
    
    try:
        with open(log_file, "w") as log:
            subprocess.run(cmd, stdout=log, stderr=subprocess.STDOUT, check=True)
        print_success(f"trimAl completed, trimmed alignment: {output_fasta}")
    except subprocess.CalledProcessError as e:
        print_error(f"trimAl failed: {e}")
        sys.exit(1)
    
    # Report trimming statistics
    from Bio import AlignIO
    try:
        aln_before = AlignIO.read(input_fasta, "fasta")
        aln_after = AlignIO.read(output_fasta, "fasta")
        
        len_before = aln_before.get_alignment_length()
        len_after = aln_after.get_alignment_length()
        removed = len_before - len_after
        
        print_info(f"Trimmed {removed} sites ({removed/len_before*100:.1f}%)")
        print_info(f"Retained {len_after} sites ({len_after/len_before*100:.1f}%)")
    except:
        pass

# ============================================================================
# Stage 4: Model Selection and Tree Inference
# ============================================================================

def run_iqtree(input_fasta: Path, output_prefix: Path, 
               threads: int = 10, bootstrap: int = 1000,
               model: str = "MFP") -> Path:
    """
    Run IQ-TREE for model selection and tree inference
    
    Args:
        input_fasta: Input aligned and trimmed FASTA file
        output_prefix: Output file prefix
        threads: Number of CPU threads
        bootstrap: Number of bootstrap replicates (UFBoot2)
        model: Substitution model (MFP for automatic selection)
    
    Returns:
        Path to the best tree file
    """
    print_info(f"Running IQ-TREE with model={model}, bootstrap={bootstrap}")
    
    cmd = [
        "/root/miniconda3/envs/r43/bin/iqtree",
        "-s", str(input_fasta),
        "-m", model,
        "-bb", str(bootstrap),      # UFBoot2
        "-alrt", str(bootstrap),    # SH-aLRT
        "-bnni",                    # Optimize bootstrap trees
        "-T", "AUTO",
        "-ntmax", str(threads),
        "--prefix", str(output_prefix)
    ]
    
    log_file = output_prefix.parent.parent / "logs" / "iqtree.log"
    
    try:
        with open(log_file, "w") as log:
            subprocess.run(cmd, stdout=log, stderr=subprocess.STDOUT, check=True)
        print_success(f"IQ-TREE completed")
    except subprocess.CalledProcessError as e:
        print_error(f"IQ-TREE failed: {e}")
        sys.exit(1)
    
    treefile = Path(str(output_prefix) + ".treefile")
    print_success(f"Best ML tree: {treefile}")
    
    return treefile

# ============================================================================
# Stage 5: Tree Post-processing
# ============================================================================

def root_and_ladderize_tree(input_tree: Path, output_tree: Path) -> None:
    """
    Root tree at midpoint and ladderize for better visualization
    
    Args:
        input_tree: Input tree file (Newick format)
        output_tree: Output rooted tree file
    """
    print_info("Rooting tree at midpoint and ladderizing")
    
    r_script = f"""
    library(ape)
    
    # Read tree
    tree <- read.tree("{input_tree}")
    
    # Midpoint rooting
    tree_rooted <- midpoint(tree)
    
    # Ladderize
    tree_rooted <- ladderize(tree_rooted)
    
    # Save
    write.tree(tree_rooted, "{output_tree}")
    
    cat("✓ Tree rooted and ladderized\\n")
    """
    
    try:
        subprocess.run(["Rscript", "-e", r_script], check=True, 
                      capture_output=True, text=True)
        print_success(f"Rooted tree: {output_tree}")
    except subprocess.CalledProcessError as e:
        print_error(f"Tree rooting failed: {e}")
        sys.exit(1)

# ============================================================================
# Stage 6: Visualization
# ============================================================================

def visualize_tree(tree_file: Path, output_dir: Path, threads: int = 1) -> None:
    """
    Generate publication-grade tree visualizations using ggtree
    
    Args:
        tree_file: Input tree file
        output_dir: Output directory for figures
        threads: Number of threads (for future parallel rendering)
    """
    print_info("Generating publication-grade figures with ggtree")
    
    visualize_script = SCRIPTS / "visualize_publication.R"
    
    if not visualize_script.exists():
        print_warning(f"Visualization script not found: {visualize_script}")
        print_info("Using basic visualization")
        visualize_basic(tree_file, output_dir)
        return
    
    cmd = [
        "Rscript",
        str(visualize_script),
        str(tree_file),
        str(output_dir)
    ]
    
    try:
        subprocess.run(cmd, check=True)
        print_success(f"Figures saved to {output_dir}")
    except subprocess.CalledProcessError as e:
        print_error(f"Visualization failed: {e}")
        print_info("Falling back to basic visualization")
        visualize_basic(tree_file, output_dir)

def visualize_basic(tree_file: Path, output_dir: Path) -> None:
    """Basic tree visualization fallback"""
    r_script = f"""
    library(ape)
    
    tree <- read.tree("{tree_file}")
    
    # Circular tree
    pdf("{output_dir}/tree_circular.pdf", width=12, height=12)
    plot(tree, type="fan", cex=0.5, main="Phylogenetic Tree (Circular)")
    dev.off()
    
    # Rectangular tree
    pdf("{output_dir}/tree_rectangular.pdf", width=16, height=20)
    plot(tree, type="phylogram", cex=0.4, main="Phylogenetic Tree")
    dev.off()
    
    cat("✓ Basic figures generated\\n")
    """
    
    subprocess.run(["Rscript", "-e", r_script], check=True)

# ============================================================================
# Main Pipeline
# ============================================================================

def main():
    parser = argparse.ArgumentParser(
        description="PhyloTree: Publication-Grade Phylogenetic Tree Analysis",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Analyze enzyme family from UniProt
  python3 run.py --query "imine reductase" --output ./ired_analysis
  
  # Analyze from FASTA file
  python3 run.py --fasta sequences.fasta --output ./my_analysis
  
  # Use 10 threads and 1000 bootstrap replicates
  python3 run.py --query "lipase" --output ./lipase --threads 10 --bootstrap 1000
        """
    )
    
    # Input options
    input_group = parser.add_mutually_exclusive_group(required=True)
    input_group.add_argument("--query", help="Enzyme name to search in UniProt")
    input_group.add_argument("--fasta", help="Input FASTA file")
    
    # Output options
    parser.add_argument("--output", required=True, help="Output directory")
    parser.add_argument("--prefix", default="phylo", help="Output file prefix")
    
    # Analysis parameters
    parser.add_argument("--threads", type=int, default=10, help="Number of CPU threads")
    parser.add_argument("--bootstrap", type=int, default=1000, help="Bootstrap replicates (min: 1000)")
    parser.add_argument("--identity", type=float, default=0.90, help="CD-HIT identity threshold (0.90 = 90%%)")
    parser.add_argument("--min-length", type=int, default=150, help="Minimum sequence length")
    parser.add_argument("--max-length", type=int, default=600, help="Maximum sequence length")
    parser.add_argument("--max-seqs", type=int, default=1000, help="Maximum sequences to retrieve")
    
    # Advanced options
    parser.add_argument("--model", default="MFP", help="IQ-TREE model (MFP for auto-selection)")
    parser.add_argument("--mafft-algorithm", default="auto", choices=["auto", "linsi", "ginsi", "einsi"],
                       help="MAFFT algorithm")
    parser.add_argument("--skip-dedup", action="store_true", help="Skip CD-HIT deduplication")
    parser.add_argument("--skip-trim", action="store_true", help="Skip trimAl trimming")
    
    args = parser.parse_args()
    
    # Validate bootstrap
    if args.bootstrap < 1000:
        print_warning(f"Bootstrap replicates ({args.bootstrap}) < 1000 is not recommended for publication")
    
    # Print header
    print(f"\n{Colors.BOLD}{'='*70}{Colors.ENDC}")
    print(f"{Colors.BOLD}PhyloTree v2.0.0 - Publication-Grade Phylogenetic Analysis{Colors.ENDC}")
    print(f"{Colors.BOLD}{'='*70}{Colors.ENDC}\n")
    
    start_time = time.time()
    
    # Setup project
    project_dir = setup_project(args.output, args.query or args.fasta)
    print_success(f"Project directory: {project_dir}")
    
    # ========================================================================
    # Stage 1: Data Collection and Preprocessing
    # ========================================================================
    print_stage(1, "Data Collection and Preprocessing")
    
    if args.query:
        raw_fasta, n_seqs = collect_sequences_uniprot(
            args.query, project_dir,
            max_seqs=args.max_seqs,
            min_length=args.min_length,
            max_length=args.max_length
        )
    else:
        # Copy input FASTA
        import shutil
        raw_fasta = project_dir / "sequences" / "raw.fasta"
        shutil.copy(args.fasta, raw_fasta)
        n_seqs = sum(1 for line in open(raw_fasta) if line.startswith(">"))
        print_success(f"Loaded {n_seqs} sequences from {args.fasta}")
    
    # Deduplication
    if not args.skip_dedup:
        dedup_fasta = project_dir / "sequences" / "deduplicated.fasta"
        n_seqs = deduplicate_sequences(raw_fasta, dedup_fasta, 
                                      identity=args.identity,
                                      threads=args.threads)
    else:
        dedup_fasta = raw_fasta
        print_info("Skipping deduplication (--skip-dedup)")
    
    # ========================================================================
    # Stage 2: Multiple Sequence Alignment
    # ========================================================================
    print_stage(2, "Multiple Sequence Alignment")
    
    aligned_fasta = project_dir / "alignment" / "aligned.fasta"
    run_mafft(dedup_fasta, aligned_fasta, 
             threads=args.threads,
             algorithm=args.mafft_algorithm)
    
    # ========================================================================
    # Stage 3: Alignment Trimming
    # ========================================================================
    print_stage(3, "Alignment Trimming")
    
    if not args.skip_trim:
        trimmed_fasta = project_dir / "alignment" / "trimmed.fasta"
        run_trimal(aligned_fasta, trimmed_fasta, method="automated1")
    else:
        trimmed_fasta = aligned_fasta
        print_info("Skipping trimming (--skip-trim)")
    
    # ========================================================================
    # Stage 4: Model Selection and Tree Inference
    # ========================================================================
    print_stage(4, "Model Selection and Tree Inference (IQ-TREE)")
    
    tree_prefix = project_dir / "trees" / args.prefix
    treefile = run_iqtree(trimmed_fasta, tree_prefix,
                         threads=args.threads,
                         bootstrap=args.bootstrap,
                         model=args.model)
    
    # ========================================================================
    # Stage 5: Tree Post-processing
    # ========================================================================
    print_stage(5, "Tree Post-processing")
    
    rooted_tree = project_dir / "trees" / f"{args.prefix}_rooted.nwk"
    root_and_ladderize_tree(treefile, rooted_tree)
    
    # ========================================================================
    # Stage 6: Visualization
    # ========================================================================
    print_stage(6, "Publication-Grade Visualization")
    
    figures_dir = project_dir / "figures"
    visualize_tree(rooted_tree, figures_dir, threads=args.threads)
    
    # ========================================================================
    # Summary
    # ========================================================================
    elapsed = time.time() - start_time
    
    print(f"\n{Colors.BOLD}{'='*70}{Colors.ENDC}")
    print(f"{Colors.BOLD}Analysis Complete!{Colors.ENDC}")
    print(f"{Colors.BOLD}{'='*70}{Colors.ENDC}\n")
    
    print_success(f"Total time: {elapsed/60:.1f} minutes")
    print_success(f"Output directory: {project_dir}")
    print_info(f"Best ML tree: {rooted_tree}")
    print_info(f"Figures: {figures_dir}")
    print_info(f"Reports: {project_dir / 'reports'}")
    
    print(f"\n{Colors.OKBLUE}Next steps:{Colors.ENDC}")
    print(f"  1. Review QC reports in {project_dir / 'reports'}")
    print(f"  2. Check tree figures in {figures_dir}")
    print(f"  3. Examine IQ-TREE report: {tree_prefix}.iqtree")
    print()

if __name__ == "__main__":
    main()

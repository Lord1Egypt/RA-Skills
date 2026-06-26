#!/usr/bin/env python3
"""
Step 3: Sequence Alignment
Evaluates sequence conservation between two proteins to assess ligand binding pocket conservation.

Usage:
    python step3_alignment.py --query1 <fasta> --query2 <fasta> \
        --name1 "Human_Target_CT" --name2 "Bacterial_Target" \
        --output_dir ./alignment_results

Output:
    - alignment_results.json       # Numerical alignment results
    - alignment_visualization.txt  # Text visualization of alignment
"""
import argparse
import json
from Bio import Align
from Bio.Seq import Seq


def read_fasta(path):
    with open(path) as f:
        lines = f.readlines()
    seq = "".join(l.strip() for l in lines[1:])
    return seq


def run_local_alignment(seq1, seq2, name1="Query1", name2="Query2"):
    aligner = Align.PairwiseAligner()
    aligner.mode = 'local'
    alignments = aligner.align(seq1, seq2)
    best = alignments[0]
    return best


def main():
    parser = argparse.ArgumentParser(description="Sequence alignment for binding pocket conservation")
    parser.add_argument("--query1", required=True, help="FASTA file for query 1")
    parser.add_argument("--query2", required=True, help="FASTA file for query 2")
    parser.add_argument("--name1", default="Query1", help="Name for sequence 1")
    parser.add_argument("--name2", default="Query2", help="Name for sequence 2")
    parser.add_argument("--output_dir", default="./alignment_results", help="Output directory")
    args = parser.parse_args()

    import os
    os.makedirs(args.output_dir, exist_ok=True)

    seq1 = read_fasta(args.query1)
    seq2 = read_fasta(args.query2)
    best = run_local_alignment(seq1, seq2, args.name1, args.name2)

    aligned1, aligned2 = str(best).split("\n")[:2]
    aligned_len = len(aligned1.replace("-", ""))
    mismatches = sum(1 for a, b in zip(aligned1, aligned2) if a != b and a != "-" and b != "-")
    similarity = 1 - mismatches / aligned_len if aligned_len > 0 else 0

    result = {
        "query1": args.name1,
        "query2": args.name2,
        "aligned_length": aligned_len,
        "mismatches": mismatches,
        "similarity": round(similarity, 4),
        "alignment": str(best)
    }

    out_json = os.path.join(args.output_dir, "alignment_results.json")
    with open(out_json, "w") as f:
        json.dump(result, f, indent=2, ensure_ascii=False)

    print(f"Similarity: {similarity:.2%}")
    print(f"Results saved to {out_json}")


if __name__ == "__main__":
    main()

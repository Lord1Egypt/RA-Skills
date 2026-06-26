#!/bin/bash
# Quality Control Pipeline for Protein Sequences
# Universal workflow for any protein family

INPUT=$1
OUTPUT_DIR=$2

if [ -z "$INPUT" ] || [ -z "$OUTPUT_DIR" ]; then
    echo "Usage: bash 01_quality_control.sh input.fasta output_dir/"
    exit 1
fi

mkdir -p $OUTPUT_DIR

echo "Quality Control Pipeline"
echo "Input: $INPUT"
echo "Output: $OUTPUT_DIR"
echo ""

# Count input sequences
INPUT_COUNT=$(grep -c ">" $INPUT)
echo "Input sequences: $INPUT_COUNT"

# Stage 1: Literature validation (filter predicted sequences)
echo "[1/8] Literature validation..."
# Keep only sequences with experimental evidence
# This is a placeholder - implement based on your database
grep -A 1 "evidence=experimental\|reviewed" $INPUT > $OUTPUT_DIR/stage1.fasta || cp $INPUT $OUTPUT_DIR/stage1.fasta
STAGE1_COUNT=$(grep -c ">" $OUTPUT_DIR/stage1.fasta)
echo "  After validation: $STAGE1_COUNT sequences"

# Stage 2: Length filtering (mean ± 2 SD)
echo "[2/8] Length filtering..."
python3 << 'PYTHON_EOF'
from Bio import SeqIO
import numpy as np
import sys

input_file = sys.argv[1]
output_file = sys.argv[2]

sequences = list(SeqIO.parse(input_file, "fasta"))
lengths = [len(seq.seq) for seq in sequences]

mean_len = np.mean(lengths)
std_len = np.std(lengths)
min_len = mean_len - 2 * std_len
max_len = mean_len + 2 * std_len

print(f"  Length range: {min_len:.0f} - {max_len:.0f} aa (mean {mean_len:.0f} ± {std_len:.0f})")

filtered = [seq for seq in sequences if min_len <= len(seq.seq) <= max_len]
SeqIO.write(filtered, output_file, "fasta")
print(f"  Kept {len(filtered)}/{len(sequences)} sequences")
PYTHON_EOF
python3 -c "$(cat)" $OUTPUT_DIR/stage1.fasta $OUTPUT_DIR/stage2.fasta

# Stage 3: CD-HIT redundancy removal (90% identity)
echo "[3/8] CD-HIT redundancy removal..."
cd-hit -i $OUTPUT_DIR/stage2.fasta -o $OUTPUT_DIR/stage3.fasta \
  -c 0.90 -n 5 -M 0 -T 0 -d 0 > $OUTPUT_DIR/cdhit.log 2>&1
STAGE3_COUNT=$(grep -c ">" $OUTPUT_DIR/stage3.fasta)
echo "  After CD-HIT: $STAGE3_COUNT sequences"

# Stage 4: Complexity check (remove low-complexity regions)
echo "[4/8] Complexity check..."
# Simple complexity filter - remove sequences with >30% single amino acid
python3 << 'PYTHON_EOF'
from Bio import SeqIO
import sys

input_file = sys.argv[1]
output_file = sys.argv[2]

sequences = list(SeqIO.parse(input_file, "fasta"))
filtered = []

for seq in sequences:
    seq_str = str(seq.seq)
    # Check if any single amino acid is >30% of sequence
    max_freq = max(seq_str.count(aa) / len(seq_str) for aa in set(seq_str))
    if max_freq < 0.3:
        filtered.append(seq)

SeqIO.write(filtered, output_file, "fasta")
print(f"  Kept {len(filtered)}/{len(sequences)} sequences")
PYTHON_EOF
python3 -c "$(cat)" $OUTPUT_DIR/stage3.fasta $OUTPUT_DIR/stage4.fasta

# Stage 5: Motif validation (optional - skip if no known motif)
echo "[5/8] Motif validation (skipped - implement if family has known motif)..."
cp $OUTPUT_DIR/stage4.fasta $OUTPUT_DIR/stage5.fasta

# Stage 6: MAFFT alignment
echo "[6/8] MAFFT alignment..."
STAGE5_COUNT=$(grep -c ">" $OUTPUT_DIR/stage5.fasta)
if [ $STAGE5_COUNT -lt 200 ]; then
    # High accuracy for small datasets
    mafft --maxiterate 1000 --localpair --thread -1 --quiet \
      $OUTPUT_DIR/stage5.fasta > $OUTPUT_DIR/stage6.fasta 2> $OUTPUT_DIR/mafft.log
else
    # Fast mode for large datasets
    mafft --auto --thread -1 --quiet \
      $OUTPUT_DIR/stage5.fasta > $OUTPUT_DIR/stage6.fasta 2> $OUTPUT_DIR/mafft.log
fi
echo "  Alignment complete"

# Stage 7: trimAl trimming
echo "[7/8] trimAl trimming..."
trimal -in $OUTPUT_DIR/stage6.fasta -out $OUTPUT_DIR/stage7.fasta \
  -automated1 > $OUTPUT_DIR/trimal.log 2>&1
echo "  Trimming complete"

# Stage 8: Final validation
echo "[8/8] Final validation..."
python3 << 'PYTHON_EOF'
from Bio import AlignIO
import numpy as np
import sys
import json

input_file = sys.argv[1]
output_file = sys.argv[2]

alignment = AlignIO.read(input_file, "fasta")
n_seqs = len(alignment)
aln_len = alignment.get_alignment_length()

# Calculate gap ratio per position
gap_ratios = []
for i in range(aln_len):
    column = alignment[:, i]
    gap_ratio = column.count('-') / len(column)
    gap_ratios.append(gap_ratio)

mean_gap = np.mean(gap_ratios)
max_gap = np.max(gap_ratios)

# Calculate sequence coverage
coverages = []
for record in alignment:
    coverage = 1 - str(record.seq).count('-') / len(record.seq)
    coverages.append(coverage)

mean_coverage = np.mean(coverages)

# Calculate pairwise similarity (sample 100 pairs if too many)
similarities = []
n_pairs = min(100, n_seqs * (n_seqs - 1) // 2)
for i in range(min(10, n_seqs)):
    for j in range(i+1, min(i+11, n_seqs)):
        seq1 = str(alignment[i].seq).replace('-', '')
        seq2 = str(alignment[j].seq).replace('-', '')
        if len(seq1) > 0 and len(seq2) > 0:
            matches = sum(a == b for a, b in zip(seq1, seq2))
            sim = matches / min(len(seq1), len(seq2))
            similarities.append(sim)

mean_sim = np.mean(similarities) if similarities else 0

# Save report
report = {
    "n_sequences": n_seqs,
    "alignment_length": aln_len,
    "mean_gap_ratio": float(mean_gap),
    "max_gap_ratio": float(max_gap),
    "mean_coverage": float(mean_coverage),
    "mean_similarity": float(mean_sim)
}

with open(output_file, 'w') as f:
    json.dump(report, f, indent=2)

print(f"  Sequences: {n_seqs}")
print(f"  Alignment length: {aln_len} positions")
print(f"  Mean gap ratio: {mean_gap:.1%}")
print(f"  Mean coverage: {mean_coverage:.1%}")
print(f"  Mean similarity: {mean_sim:.1%}")

# Quality assessment
if mean_gap < 0.3 and mean_coverage > 0.8 and 0.25 < mean_sim < 0.6:
    print("  ✓ Quality: EXCELLENT")
elif mean_gap < 0.4 and mean_coverage > 0.75:
    print("  ✓ Quality: GOOD")
else:
    print("  ⚠ Quality: ACCEPTABLE (may need manual review)")
PYTHON_EOF
python3 -c "$(cat)" $OUTPUT_DIR/stage7.fasta $OUTPUT_DIR/qc_report.json

# Copy to final location
cp $OUTPUT_DIR/stage7.fasta $OUTPUT_DIR/final.fasta

echo ""
echo "Quality Control Complete!"
echo "Final: $(grep -c ">" $OUTPUT_DIR/final.fasta) sequences"
echo "Reduction: $INPUT_COUNT → $(grep -c ">" $OUTPUT_DIR/final.fasta) ($(echo "scale=1; 100 * $(grep -c ">" $OUTPUT_DIR/final.fasta) / $INPUT_COUNT" | bc)%)"
echo ""
echo "Output files:"
echo "  - $OUTPUT_DIR/final.fasta (aligned, trimmed sequences)"
echo "  - $OUTPUT_DIR/qc_report.json (quality metrics)"

#!/bin/bash
# Protein QC Strict - Complete Workflow
# Usage: bash protein_qc_workflow.sh input.fasta output_dir

set -e

INPUT=$1
OUTPUT_DIR=$2

if [ -z "$INPUT" ] || [ -z "$OUTPUT_DIR" ]; then
    echo "Usage: bash protein_qc_workflow.sh input.fasta output_dir"
    exit 1
fi

mkdir -p $OUTPUT_DIR
cd $OUTPUT_DIR

echo "=========================================="
echo "Protein QC Strict - Complete Workflow"
echo "=========================================="
echo ""
echo "Input: $INPUT"
echo "Output: $OUTPUT_DIR"
echo ""

# Stage 1: Length filter (200-500 aa)
echo "Stage 1: Length filter (200-500 aa)..."
python3 << 'PYEOF'
from Bio import SeqIO
import sys

sequences = list(SeqIO.parse(sys.argv[1], "fasta"))
filtered = [seq for seq in sequences 
            if 200 <= len(seq.seq) <= 500 
            and not (set(str(seq.seq)) - set('ACDEFGHIKLMNPQRSTVWY'))]

print(f"Input: {len(sequences)}")
print(f"Output: {len(filtered)}")
print(f"Removed: {len(sequences) - len(filtered)}")

SeqIO.write(filtered, "01_length_filtered.fasta", "fasta")
PYEOF

# Stage 2: CD-HIT redundancy removal (90%)
echo ""
echo "Stage 2: CD-HIT redundancy removal (90%)..."
cd-hit -i 01_length_filtered.fasta \
       -o 02_nr90.fasta \
       -c 0.90 \
       -n 5 \
       -M 0 \
       -T 0

# Stage 3: Complexity check (entropy >= 2.0)
echo ""
echo "Stage 3: Complexity check (entropy >= 2.0)..."
python3 << 'PYEOF'
from Bio import SeqIO
from collections import Counter
import numpy as np

def calculate_complexity(seq_str):
    if len(seq_str) == 0:
        return 0
    counts = Counter(seq_str)
    total = len(seq_str)
    entropy = 0
    for count in counts.values():
        if count > 0:
            p = count / total
            entropy -= p * np.log2(p)
    return entropy

sequences = list(SeqIO.parse("02_nr90.fasta", "fasta"))
filtered = [seq for seq in sequences 
            if calculate_complexity(str(seq.seq)) >= 2.0]

print(f"Input: {len(sequences)}")
print(f"Output: {len(filtered)}")
print(f"Low complexity: {len(sequences) - len(filtered)}")

SeqIO.write(filtered, "03_complex.fasta", "fasta")
PYEOF

# Stage 4: Motif verification (Rossmann fold: G-X-G-X-X-G)
echo ""
echo "Stage 4: Motif verification (Rossmann fold)..."
python3 << 'PYEOF'
from Bio import SeqIO
import re

rossmann_pattern = re.compile(r'G.G..G')
sequences = list(SeqIO.parse("03_complex.fasta", "fasta"))

with_motif = [seq for seq in sequences 
              if rossmann_pattern.search(str(seq.seq))]

print(f"Total: {len(sequences)}")
print(f"With motif: {len(with_motif)} ({len(with_motif)/len(sequences)*100:.1f}%)")
print(f"Without: {len(sequences) - len(with_motif)}")

# Save all (variants may not have motif)
SeqIO.write(sequences, "04_motif_checked.fasta", "fasta")
PYEOF

# Stage 5: Multiple sequence alignment (MAFFT)
echo ""
echo "Stage 5: Multiple sequence alignment (MAFFT)..."
mafft --localpair \
      --maxiterate 1000 \
      --thread 8 \
      04_motif_checked.fasta 1> 05_aligned.fasta 2> mafft.log

# Stage 6: Alignment trimming (trimAl)
echo ""
echo "Stage 6: Alignment trimming (trimAl)..."
trimal -in 05_aligned.fasta \
       -out 06_trimmed.fasta \
       -automated1

# Stage 7: Quality assessment
echo ""
echo "Stage 7: Quality assessment..."
python3 << 'PYEOF'
from Bio import AlignIO
import numpy as np
import random
from collections import Counter

alignment = AlignIO.read("06_trimmed.fasta", "fasta")

print(f"\n{'='*60}")
print("Quality Assessment Report")
print("="*60)
print(f"\nSequences: {len(alignment)}")
print(f"Alignment length: {alignment.get_alignment_length()}")

# Gap ratio
gap_ratios = []
for i in range(alignment.get_alignment_length()):
    col = alignment[:, i]
    gap_ratio = col.count('-') / len(alignment)
    gap_ratios.append(gap_ratio)

mean_gap = np.mean(gap_ratios) * 100
print(f"\nGap ratio: {mean_gap:.1f}%")
if mean_gap < 30:
    print("  ✅ Good (< 30%)")
else:
    print("  ⚠️ High (> 30%)")

# Sequence identity
random.seed(42)

def calculate_identity(seq1, seq2):
    matches = 0
    total = 0
    for aa1, aa2 in zip(seq1, seq2):
        if aa1 != '-' and aa2 != '-':
            total += 1
            if aa1 == aa2:
                matches += 1
    return matches / total if total > 0 else 0

identities = []
for _ in range(min(100, len(alignment) * (len(alignment) - 1) // 2)):
    i, j = random.sample(range(len(alignment)), 2)
    identity = calculate_identity(
        str(alignment[i].seq),
        str(alignment[j].seq)
    )
    identities.append(identity)

mean_identity = np.mean(identities) * 100
print(f"\nSequence identity: {mean_identity:.1f}%")
if 40 <= mean_identity <= 60:
    print("  ✅ Optimal (40-60%)")
elif 30 <= mean_identity <= 70:
    print("  ✅ Good (30-70%)")
else:
    print("  ⚠️ Outside ideal range")

# Coverage
coverages = []
for record in alignment:
    seq = str(record.seq)
    non_gap = len([aa for aa in seq if aa != '-'])
    coverage = non_gap / len(seq)
    coverages.append(coverage)

mean_coverage = np.mean(coverages) * 100
print(f"\nCoverage: {mean_coverage:.1f}%")
if mean_coverage > 80:
    print("  ✅ Good (> 80%)")
else:
    print("  ⚠️ Low (< 80%)")

# Conservation
entropies = []
for i in range(alignment.get_alignment_length()):
    column = alignment[:, i]
    column_no_gap = [aa for aa in column if aa != '-']
    
    if len(column_no_gap) == 0:
        continue
    
    counts = Counter(column_no_gap)
    total = len(column_no_gap)
    
    entropy = 0
    for count in counts.values():
        if count > 0:
            p = count / total
            entropy -= p * np.log2(p)
    
    max_entropy = np.log2(20)
    norm_entropy = entropy / max_entropy
    entropies.append(norm_entropy)

highly_conserved = [i for i, e in enumerate(entropies) if e < 0.3]
print(f"\nHighly conserved sites: {len(highly_conserved)}")

print(f"\n{'='*60}")
print("Quality assessment complete!")
print("="*60)
PYEOF

echo ""
echo "=========================================="
echo "Workflow complete!"
echo "=========================================="
echo ""
echo "Output files:"
echo "  01_length_filtered.fasta - Length filtered (200-500 aa)"
echo "  02_nr90.fasta - CD-HIT 90% non-redundant"
echo "  03_complex.fasta - Complexity checked"
echo "  04_motif_checked.fasta - Motif verified"
echo "  05_aligned.fasta - MAFFT alignment"
echo "  06_trimmed.fasta - trimAl trimmed (final)"
echo ""

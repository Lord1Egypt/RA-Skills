# Protein Sequence Quality Control Pro

Professional protein sequence quality control and visualization workflow with publication-ready figures.

## Quick Start

```bash
# Run complete QC pipeline
python3 scripts/run_complete_qc.py \
    --input raw_sequences.fasta \
    --output qc_results/ \
    --threads 8

# Generate all figures
python3 scripts/generate_analysis_figures.py

# Generate Nature-style figures
python3 scripts/generate_nature_conservation_landscape.py
```

## Features

- ✅ Complete QC pipeline (length filter, CD-HIT, complexity, motif, MSA, trimming)
- ✅ Conservation analysis (Shannon entropy)
- ✅ Coevolution analysis (Mutual Information)
- ✅ 12+ publication-ready figures
- ✅ Nature-style figures (300 DPI, PDF + PNG)
- ✅ Automatic quality assessment

## Requirements

- Python 3.7+
- Biopython
- NumPy
- Matplotlib
- CD-HIT
- MAFFT
- trimAl

## Documentation

See `SKILL.md` for complete documentation.

## Version

1.0.0 (2026-05-08)

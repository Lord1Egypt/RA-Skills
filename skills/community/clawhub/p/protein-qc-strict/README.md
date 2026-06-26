# Protein QC Strict

Strictest protein sequence analysis quality control workflow, battle-tested on IRED enzyme family (3,365 → 456 sequences).

## Features

- ✅ Literature validation
- ✅ CD-HIT redundancy removal (90%)
- ✅ Complexity check (Shannon entropy ≥ 2.0)
- ✅ Motif verification (Rossmann fold)
- ✅ MSA quality assessment (Gap, Identity, Coverage)
- ✅ Conservation analysis (normalized Shannon entropy)
- ✅ Coevolution analysis (normalized mutual information)

## Installation

```bash
clawhub install protein-qc-strict
```

Required tools (auto-installed via conda):
- CD-HIT
- MAFFT
- trimAl

## Quick Start

```bash
# 1. Prepare your sequences
cp your_sequences.fasta input.fasta

# 2. Run the complete QC workflow
bash protein_qc_workflow.sh input.fasta output_dir

# 3. Check the quality report
cat output_dir/quality_report.txt
```

## Workflow

```
Raw sequences (N)
    ↓ [Literature validation]
Validated sequences
    ↓ [Length filter 200-500 aa]
High-quality sequences
    ↓ [CD-HIT 90%]
Non-redundant sequences
    ↓ [Complexity check]
Complex sequences
    ↓ [Motif verification]
Motif-validated sequences
    ↓ [MAFFT + trimAl]
High-quality alignment
    ↓ [Quality assessment]
Publication-ready data
```

## Quality Standards

| Metric | Standard | Our Result |
|--------|----------|------------|
| Gap ratio | < 30% | 21.1% ✅ |
| Sequence identity | 40-60% | 25.5% (high diversity) |
| Coverage | > 80% | 78.9% |
| Redundancy removal | 90-95% | 90% ✅ |
| Complexity | entropy ≥ 2.0 | 100% pass ✅ |
| Motif coverage | > 50% | 65.4% ✅ |

## Core Principles

1. **Be rigorous** - No guessing, verify everything
2. **Use original tools** - No simplified implementations
3. **QC every step** - Check data quality at each stage
4. **Filter high-gap sites** - Gaps mislead analysis
5. **Question unreasonable results** - Critical thinking required

## Example: IRED Enzyme Family

Real research case: 3,365 → 456 sequences

```bash
# Stage 1: Literature validation (3365 → 840)
# Manual check for experimental validation

# Stage 2: Length filter (840 → 793)
python filter_length.py input.fasta 200 500 > filtered.fasta

# Stage 3: CD-HIT (793 → 456)
cd-hit -i filtered.fasta -o nr90.fasta -c 0.90 -n 5 -M 0 -T 0

# Stage 4: Complexity check (456 → 456)
python check_complexity.py nr90.fasta 2.0 > complex.fasta

# Stage 5: Motif verification (456 → 456, 65.4% coverage)
python verify_motif.py complex.fasta "G.G..G" > motif.fasta

# Stage 6: MSA (MAFFT + trimAl)
mafft --localpair --maxiterate 1000 motif.fasta > aligned.fasta
trimal -in aligned.fasta -out trimmed.fasta -automated1

# Stage 7: Quality assessment
python assess_quality.py trimmed.fasta
```

## Documentation

See `SKILL.md` for complete documentation including:
- Detailed workflow for each stage
- Code examples
- Quality check procedures
- Common pitfalls to avoid
- Literature standards comparison

## Citation

If you use this workflow in your research, please cite:

```
Protein QC Strict v4.0.0
https://clawhub.com/skills/protein-qc-strict
Developed through IRED enzyme family analysis (2026)
```

## License

MIT

## Author

Developed through real research experience with strict quality requirements.

## Version History

- **4.0.0** (2026-04-25): Complete workflow with all QC stages
- Initial release based on IRED enzyme family analysis

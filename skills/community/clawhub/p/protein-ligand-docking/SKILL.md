---
name: protein-ligand-docking
description: |
  Run a protein-ligand docking workflow for research questions about target binding, selectivity, and structural plausibility.

  Use this skill when the user asks whether a ligand may bind a protein target, wants a docking-oriented comparison across species or homologs, or needs a stepwise in silico workflow that uses sequence retrieval, structure search, AlphaFold/Colab, and AutoDock Vina.
---

# Protein-Ligand Docking

Use this skill for research questions such as:

- "Can ligand X plausibly bind protein Y?"
- "Is this inhibitor likely to be selective between bacterial and human homologs?"
- "Should we continue to docking, or is sequence/structure divergence already too large?"

Keep the workflow practical. If an early step already rules out a meaningful docking analysis, stop and explain why instead of forcing the full pipeline.

## Inputs To Collect First

Ask for or infer:

- target protein name and species
- ligand name and available structure format
- whether the user wants a quick feasibility screen or a fuller workflow
- whether an experimental structure already exists

Useful concrete inputs:

- UniProt ID or protein sequence
- ligand SDF or SMILES
- known PDB ID, if available
- comparison target, if this is a selectivity question

## Workflow

### 1. Sequence Retrieval

- Retrieve the target sequence from UniProt when the user provides a protein name or UniProt ID.
- Save FASTA files with clear names because later scripts depend on them.
- If the question is about selectivity, retrieve both sequences before moving on.

### 2. Structure Search

- Search RCSB PDB for experimentally solved structures first.
- Prefer structures with a relevant ligand, catalytic domain, or biologically meaningful complex.
- If no suitable structure exists, plan to use AlphaFold or AlphaFold-Multimer in Colab.

### 3. Sequence Conservation Check

When the question involves homolog comparison, run [scripts/step3_alignment.py](./scripts/step3_alignment.py).

- High similarity suggests the binding region may be conserved and docking can be informative.
- Borderline similarity means docking may still help, but interpretation must stay cautious.
- Very low similarity can support an early "binding pocket likely not conserved" conclusion.

Detailed interpretation thresholds live in [references/decision-guide.md](./references/decision-guide.md).

### 4. Structure Modeling

Use AlphaFold-Multimer only when a suitable experimental structure is missing and a complex model is still needed.

- The Colab template is in [references/alphafold_multimer_colab.ipynb](./references/alphafold_multimer_colab.ipynb).
- Include only biologically relevant chains.
- Tell the user clearly when this step requires manual Colab execution.

### 5. Model Quality Assessment

Before docking an AlphaFold-derived structure, run [scripts/step5_pae_analysis.py](./scripts/step5_pae_analysis.py).

Focus on two questions:

- Is the fold itself credible enough to use?
- Is the interface or predicted docking region reliable enough to interpret?

If interface confidence is poor, stop and say docking would likely be misleading.

### 6. Docking

Run [scripts/step6_vina_docking.py](./scripts/step6_vina_docking.py) when all of the following are true:

- the receptor structure is usable
- the ligand structure is available
- the docking box is justified by structure or interface analysis

Prefer docking settings derived from the modeled or known interaction region, not arbitrary whole-protein boxes.

### 7. Report The Result

Use [scripts/step7_summary_report.py](./scripts/step7_summary_report.py) when the user wants a structured deliverable.

The final answer should cover:

- binding affinity range, not just the single best score
- whether the pose lands in a biologically meaningful region
- whether the structure quality supports interpretation
- what the main uncertainty is
- what experimental validation would best test the claim

## Decision Rules

Use these rules during execution:

- Do not treat docking as proof of binding.
- Do not continue if the structure or interface confidence is clearly too poor.
- Do not over-interpret small score differences across targets.
- If the user only needs a quick answer, stop once the evidence is sufficient.
- For biomedical research, always separate computational plausibility from experimental validation.

Thresholds, QC checks, and result wording guidance are in [references/decision-guide.md](./references/decision-guide.md).

## Expected Outputs

Depending on the stage reached, provide some or all of:

- FASTA files for targets
- selected PDB IDs or modeled structures
- alignment summary JSON
- model quality JSON with grid box coordinates
- docking summary JSON
- a short written conclusion in plain language
- optional `Summary.md`, `Summary.docx`, and figure output

## Dependencies

This skill may rely on:

- UniProt and RCSB web access
- Google Colab for AlphaFold-Multimer
- Python 3 plus Biopython, NumPy, RDKit, OpenBabel, and py3Dmol
- AutoDock Vina in WSL or Linux

Installation notes and recommended thresholds are in [references/decision-guide.md](./references/decision-guide.md).

## Limits To State Explicitly

Always warn the user about the main limits:

- docking scores are approximate, not definitive
- static docking ignores induced fit and many solvent effects
- AlphaFold confidence does not guarantee a correct ligand-binding geometry
- experimental assays remain the standard for validation

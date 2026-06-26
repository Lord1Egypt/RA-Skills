# Multi-paper plasmid copy-number deck: session notes

## Use case
- User wanted one integrated journal-club PPT from three related papers, not three isolated sections.
- Topic flow required: first analyze plasmid copy number, and explicitly explain how it was analyzed; then transition into engineering copy number, and explicitly explain how it was engineered.

## Validated paper set
1. Nat Commun 2024 — Universal rules govern plasmid copy number
2. Nat Commun 2025 — Scaling laws of bacterial and archaeal plasmids
3. Nat Commun 2026 — Engineering plasmids with synthetic origins of replication

## Important exclusion
- Attached meta1.pdf was unrelated (Science 2025 MetaEdit / microbiome editing) and should be excluded from the deck despite being locally available in the workspace.
- Practical lesson: for multi-paper user requests, verify that attachments and referenced URLs/titles describe the same intended set before building the slide narrative.

## Recommended integrated narrative
1. Why plasmid copy number matters biologically and biotechnologically.
2. Analysis paper A: coverage-based estimation across thousands of plasmids.
3. Analysis paper B: pseuPIRA solves multireads and extends scaling laws across Bacteria and Archaea.
4. Synthesis: natural constraints = size-copy tradeoff, mobility/lifestyle coupling, replicon interactions, DNA-load ceiling.
5. Transition question: if natural plasmids obey these constraints, can copy number be rationally reprogrammed?
6. Engineering paper: refactor pMB1, replace natural control with synthetic RNA regulators, tune copy number, improve stability, add inducible inputs, and build compatible multi-plasmid systems.

## Method statements to surface on slides
- How PCN was analyzed:
  - paper 1: trimmed mean sequencing coverage of plasmid relative to chromosome coverage
  - paper 2: pseudoalignment + uniread initialization + probabilistic iterative reassignment of multireads (pseuPIRA)
- How PCN was engineered:
  - refactor pMB1 origin into modular components
  - replace RNAI/RNAII natural control with synthetic target-RNA/repressor-sRNA negative feedback (pT181-derived)
  - tune via promoters, architecture, RNA-primer minimization, maintenance systems, and orthogonal regulator variants

## Slide-planning lesson
- A good ~20-slide structure for this topic is: intro/problem, methods for analysis, key natural laws, transition, engineering design, engineering performance, signal-programmable copy control, compatibility, final synthesis.
- Do not force equal slide counts per paper. Let the integrated biological logic determine slide allocation.

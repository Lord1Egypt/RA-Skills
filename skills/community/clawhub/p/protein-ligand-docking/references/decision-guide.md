# Decision Guide

Use this file when you need concrete thresholds, quality-control checks, or concise wording for conclusions.

## Sequence Similarity Heuristic

For homolog comparison:

| Similarity | Practical interpretation |
|------------|--------------------------|
| > 40% | Binding region may be conserved; docking can be informative |
| 20-40% | Uncertain; combine docking with structural inspection |
| < 20% | Binding site conservation is less likely; docking may add little |

Treat this as a heuristic, not a hard biological law.

## AlphaFold Quality Heuristic

### pLDDT

- > 90: very high local confidence
- 70-90: usable for many structured regions
- < 50: likely disordered or unreliable

### PAE

- < 5 A: strong confidence in relative positioning
- 5-10 A: moderate confidence
- 10-15 A: cautious interpretation only
- > 15 A: interface may be too unreliable for meaningful docking claims

If the docking box depends on an unreliable interface, stop and explain that limitation.

## Binding Energy Heuristic

| Best score | Practical interpretation |
|------------|--------------------------|
| < -9 kcal/mol | strong predicted binding |
| -7 to -9 kcal/mol | moderate predicted binding |
| > -7 kcal/mol | weak or less convincing binding |

Do not compare scores across targets as if they were exact free energies.

## Pose Sanity Checks

Before drawing conclusions, check:

- the ligand is near a plausible binding site or interface
- the pose is not floating on an exposed, featureless surface
- top poses show reasonable convergence
- contact distances are physically plausible
- the receptor model quality supports local interpretation

## Recommended Output Language

Prefer wording like:

- "computationally plausible"
- "compatible with a possible binding interaction"
- "supports follow-up experimental testing"
- "insufficient structural confidence for a strong docking claim"

Avoid wording like:

- "proves binding"
- "confirms mechanism"
- "definitively selective"

## Dependencies

Typical dependencies for this workflow:

- Python 3
- Biopython
- NumPy
- RDKit
- OpenBabel
- AutoDock Vina
- py3Dmol
- Google Colab for AlphaFold-Multimer when no good experimental structure exists

## Fast QC Checklist

- pLDDT mostly above 70 in the relevant region
- interface PAE acceptable for the intended conclusion
- grid box justified by structure or interface analysis
- docking settings documented
- interpretation separated from experimental proof

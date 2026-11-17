## Description:

Screens SMILES strings with RDKit descriptors, Lipinski and Veber checks, QED scoring, and simplified PAINS alerts to produce a JSON drug-safety risk report.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cheminem](https://clawhub.ai/user/cheminem)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and researchers use this skill to run early drug-candidate safety profiling from SMILES strings and receive descriptor-based risk signals before deeper toxicology review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The Low/Medium/High drug-safety labels are incomplete research heuristics and may mislead clinical, regulatory, synthesis-gating, or safety-critical decisions.

Mitigation: Treat the output as preliminary screening only and require expert review with validated toxicology models before acting on safety conclusions.

Risk: The skill uses a simplified PAINS substructure set and does not implement Ames mutagenicity, hERG channel prediction, or LD50 estimation.

Mitigation: Supplement results with complete PAINS screening and dedicated validated toxicology endpoints for decisions that depend on those risks.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/cheminem/skills/pharmaclaw-tox-agent)
- [Cheminem publisher profile](https://clawhub.ai/user/cheminem)

## Skill Output:

**Output Type(s):** [text, JSON, shell commands, guidance]

**Output Format:** [JSON risk report with descriptor values and human-readable workflow guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Accepts one SMILES string per analysis; invalid SMILES return an error object.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

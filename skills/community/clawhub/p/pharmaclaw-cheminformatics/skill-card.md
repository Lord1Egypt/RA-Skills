## Description:

Advanced cheminformatics agent for 3D conformer analysis, pharmacophore mapping, molecular format conversion, RECAP fragmentation, and stereoisomer enumeration.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cheminem](https://clawhub.ai/user/cheminem)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and cheminformatics practitioners use this skill to profile molecules from SMILES, generate 3D conformers, extract pharmacophore features, convert molecular formats, and inspect RECAP fragments and stereoisomers for drug discovery workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Cheminformatics jobs can consume substantial compute on large or complex molecules.

Mitigation: Run in a reviewed environment with pinned dependencies, dedicated output directories, and external CPU, memory, and time limits.

Risk: The skill can write user-directed SDF, PNG, and molecular-format output files.

Mitigation: Use a dedicated output directory and review generated files before sharing or feeding them into automated workflows.

Risk: FDA, IP, and downstream-agent suggestions could be mistaken for legal or regulatory advice.

Mitigation: Treat these suggestions as scientific workflow context only and require expert legal, regulatory, or intellectual-property review before acting on them.

## Reference(s):

- [Pharmaclaw Cheminformatics ClawHub listing](https://clawhub.ai/cheminem/skills/pharmaclaw-cheminformatics)
- [Cheminem publisher profile](https://clawhub.ai/user/cheminem)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance, files]

**Output Format:** [Markdown guidance with JSON script outputs and optional SDF or PNG files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs can include conformer energies, RMSD matrices, pharmacophore maps, converted molecular formats, warnings, risks, and recommended downstream workflows.]

## Skill Version(s):

1.0.0 (source: server release metadata and skill heading)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

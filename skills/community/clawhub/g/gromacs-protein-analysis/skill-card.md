## Description:

Provides Chinese-language workflow guidance for GROMACS protein molecular dynamics analysis, covering PBC correction, RMSD, RMSF, gyrate, SASA, DCCM, RDCM, PCA, and FEL workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[charleshahn](https://clawhub.ai/user/charleshahn)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, researchers, and scientific computing agents use this skill to plan and execute common GROMACS protein simulation analyses, choose appropriate input files and atom groups, and interpret generated outputs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated shell commands can create or append local analysis files.

Mitigation: Review commands and output paths before execution, and avoid overwriting existing analysis results.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/charleshahn/skills/gromacs-protein-analysis)
- [周期性校正](references/pbc-correction.md)
- [RMSD 分析](references/rmsd-analysis.md)
- [RMSF 分析](references/rmsf-analysis.md)
- [Gyrate 分析](references/gyrate-analysis.md)
- [SASA 分析](references/sasa-analysis.md)
- [DCCM 分析](references/dccm-analysis.md)
- [RDCM 分析](references/rdcm-analysis.md)
- [PCA 分析](references/pca-analysis.md)
- [FEL 分析](references/fel-analysis.md)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Shell commands]

**Output Format:** [Markdown guidance with inline shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Commands target GROMACS and DuIvyTools workflows and may create or append local analysis files.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

## Description: <br>
Provides Chinese-language workflow guidance for GROMACS protein molecular dynamics analysis, covering PBC correction, RMSD, RMSF, gyrate, SASA, DCCM, RDCM, PCA, and FEL analyses. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[CharlesHahn](https://clawhub.ai/user/CharlesHahn) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, computational biologists, and agents use this skill to plan common GROMACS protein molecular dynamics trajectory analyses and understand required inputs, expected outputs, command choices, visualization steps, and analysis dependencies. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Copied commands can produce incorrect or overwritten analysis outputs when filenames, atom selections, or trajectory, topology, and index files are wrong. <br>
Mitigation: Verify filenames, atom selections, matching atom counts, and output paths before running commands; keep backups of original trajectory, topology, and index files. <br>
Risk: Analysis results can be misleading when trajectory quality, PBC artifacts, sampling, or time-window choices are not checked before interpretation. <br>
Mitigation: Inspect trajectories and intermediate plots, apply PBC correction when indicated, use consistent time ranges across related analyses, and confirm statistical convergence before interpreting results. <br>


## Reference(s): <br>
- [PBC Correction Guide](references/pbc-correction.md) <br>
- [RMSD Analysis Guide](references/rmsd-analysis.md) <br>
- [RMSF Analysis Guide](references/rmsf-analysis.md) <br>
- [Gyrate Analysis Guide](references/gyrate-analysis.md) <br>
- [SASA Analysis Guide](references/sasa-analysis.md) <br>
- [DCCM Analysis Guide](references/dccm-analysis.md) <br>
- [RDCM Analysis Guide](references/rdcm-analysis.md) <br>
- [PCA Analysis Guide](references/pca-analysis.md) <br>
- [FEL Analysis Guide](references/fel-analysis.md) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, shell commands] <br>
**Output Format:** [Markdown guidance with GROMACS and DuIvyTools shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Documentation-only; command examples require user-supplied trajectory, topology, and index files.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

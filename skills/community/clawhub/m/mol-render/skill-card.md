## Description: <br>
Generate high-quality 3D ball-and-stick molecular renderings from SMILES strings or PDB structures using POV-Ray ray tracing. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Zhao-Zehua](https://clawhub.ai/user/Zhao-Zehua) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers, researchers, and scientific visualization users can use this skill to generate PNG ball-and-stick molecular renderings from SMILES strings or PDB structures. It supports small-molecule rendering, PDB chain or residue filtering, ligand-only views, and configurable rendering options. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: PDB IDs are downloaded from RCSB and cached in the system temp directory, which may expose queried structures or leave local copies. <br>
Mitigation: Use local PDB files for private structures and clear temporary cached files according to the deployment environment's data-handling policy. <br>
Risk: The skill depends on local Python packages and POV-Ray execution. <br>
Mitigation: Install dependencies from trusted sources in a virtual environment or container before running the rendering scripts. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/Zhao-Zehua/mol-render) <br>
- [RCSB PDB file download endpoint](https://files.rcsb.org/download/{pdb_id}.pdb) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance, files] <br>
**Output Format:** [Markdown guidance with shell commands and generated PNG image files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces 1200x1200 PNG renderings by default, with options for background color, hydrogen display, molecule subset selection, viewing angle, and resolution.] <br>

## Skill Version(s): <br>
1.0.0 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

## Description: <br>
Generates PyMOL scripts that highlight specific protein residues in PDB structures for molecular visualization. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[aipoch-ai](https://clawhub.ai/user/aipoch-ai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, bioinformatics researchers, and structural biology users use this skill to generate local PyMOL scripts that load protein structures, apply visualization settings, and highlight residues or functional sites. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated `.pml` files may contain user-provided residue, color, path, or filename values. <br>
Mitigation: Use trusted inputs, keep output filenames inside the project workspace, and review generated scripts before running them in PyMOL. <br>
Risk: Using a PDB ID can create a PyMOL fetch command that retrieves a structure externally. <br>
Mitigation: Use local PDB files when external retrieval is not intended, or confirm that the selected PDB ID and network access are acceptable before execution. <br>
Risk: Generated visualization scripts can overwrite or create local files at the requested output path. <br>
Mitigation: Choose explicit workspace-local output paths and inspect the generated path before executing downstream PyMOL commands. <br>


## Reference(s): <br>
- [PyMOL Command Reference](references/pymol_commands.md) <br>
- [ClawHub Release Page](https://clawhub.ai/aipoch-ai/protein-struct-viz) <br>
- [Publisher Profile](https://clawhub.ai/user/aipoch-ai) <br>


## Skill Output: <br>
**Output Type(s):** [Code, Files, Shell commands, Guidance] <br>
**Output Format:** [Markdown guidance with shell commands and generated plain text PyMOL .pml script content] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Generated scripts are intended for local review and execution in PyMOL; no Python package dependencies are required by the generator.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence and frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

## Description:

Generate PyMOL scripts to highlight specific protein residues in PDB structures.

This skill is ready for commercial/non-commercial use.

## Publisher:

[aipoch-ai](https://clawhub.ai/user/aipoch-ai)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, computational biologists, and structural biology users use this skill to generate PyMOL scripts that load protein structures, highlight selected residues, and apply visualization settings for analysis or publication-ready images.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated .pml files are executable PyMOL scripts built from weakly validated PDB, residue, style, and color inputs.

Mitigation: Review generated scripts before opening them in PyMOL and use only trusted PDB IDs, local paths, residue specifications, and color values.

Risk: The script can write output to arbitrary paths supplied through the output filename.

Mitigation: Direct output to a known workspace filename and add strict path containment before broad deployment.

## Reference(s):

- [PyMOL Command Reference](references/pymol_commands.md)
- [ClawHub release page](https://clawhub.ai/aipoch-ai/skills/protein-struct-viz)

## Skill Output:

**Output Type(s):** [Code, Files, Shell commands, Guidance]

**Output Format:** [Markdown guidance with generated PyMOL .pml script content and command-line usage]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generated scripts may load local PDB files or fetch four-character PDB IDs when executed in PyMOL.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

## Description:

Generate high-quality 3D ball-and-stick molecular renderings from SMILES strings or PDB structures using POV-Ray ray tracing.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zhao-zehua](https://clawhub.ai/user/zhao-zehua)

### License/Terms of Use:

MIT

## Use Case:

Developers, researchers, and technical users use this skill to render molecular structures as ball-and-stick PNG images from SMILES strings, local PDB files, or RCSB PDB IDs. It is useful for generating molecule visuals with configurable backgrounds, views, residue filters, and rendering resolution.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Using a 4-character PDB ID triggers a network request to RCSB.

Mitigation: Use local PDB files when network access is not desired, and review or cache downloaded structures before use in controlled environments.

Risk: The skill invokes POV-Ray and relies on Python chemistry dependencies.

Mitigation: Install and run the skill in a virtual environment as a non-privileged user, and prefer pinned dependency versions.

Risk: Default PDB caching may use the system temporary directory on shared or multi-user systems.

Mitigation: Avoid relying on shared temporary caches; use reviewed local PDB files or a private cache location where possible.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/zhao-zehua/skills/mol-render)
- [Publisher profile](https://clawhub.ai/user/zhao-zehua)
- [RCSB PDB download endpoint](https://files.rcsb.org/download/)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance, files]

**Output Format:** [Markdown guidance with inline shell commands; generated scripts produce PNG image files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Default rendered images are 1200x1200 PNG files, with command-line options for background, view, molecule filters, hydrogen and water handling, and resolution.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

## Description:

Prepare input files for molecular docking software, automatically determine Grid Box center and size, and generate configuration files for AutoDock Vina and AutoDock4.

This skill is ready for commercial/non-commercial use.

## Publisher:

[aipoch-ai](https://clawhub.ai/user/aipoch-ai)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, computational biologists, and molecular modeling practitioners use this skill to calculate docking grid boxes from receptor structures, active-site residues, reference ligands, or manual coordinates, then produce AutoDock Vina or AutoDock4 configuration files.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill reads molecular structure inputs and writes output files in the local workspace.

Mitigation: Use non-sensitive input files and provide explicit output paths that are appropriate for the project workspace.

Risk: The release evidence notes documentation gaps around advertised MOL and non-Vina or non-AutoDock4 support.

Mitigation: Treat AutoDock Vina and AutoDock4 configuration generation as the validated workflow unless the skill is updated with evidence for additional formats.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/aipoch-ai/skills/protein-docking-configurator)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration]

**Output Format:** [Markdown guidance with command examples and generated docking configuration file content]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces local AutoDock Vina config.txt files or AutoDock4 .gpf files from user-provided molecular structure inputs.]

## Skill Version(s):

1.0.0 (source: release metadata and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

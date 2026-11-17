## Description:

Renders Mermaid diagrams as terminal ASCII output or PNG image files for flowcharts, sequence diagrams, class diagrams, pie charts, Git graphs, state diagrams, and ER diagrams.

This skill is ready for commercial/non-commercial use.

## Publisher:

[smallnest](https://clawhub.ai/user/smallnest)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and technical teams use this skill to turn Mermaid syntax into quick terminal previews or PNG diagrams for workflows, architecture, data models, and project histories.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Private architecture, internal system names, credentials, or business details in diagrams may be exposed when image export uploads output externally.

Mitigation: Review diagram content before rendering and use image export only when external BOS upload is acceptable.

Risk: Image export can write to arbitrary output paths, which can cause accidental overwrites or misplaced files.

Mitigation: Write exports only to a dedicated export directory with non-sensitive filenames and review the output path before execution.

## Reference(s):

- [Chart Types Reference](references/chart-types.md)
- [ClawHub Skill Page](https://clawhub.ai/smallnest/skills/mermaid-renderer)

## Skill Output:

**Output Type(s):** [text, files, shell commands]

**Output Format:** [Terminal ASCII text by default, or PNG image files when export is requested.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Supports Mermaid flowchart, sequence, class, pie, gitGraph, state, and ER diagram syntax; image export writes to a requested output path.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

## Description:

Create hand-drawn workflow diagrams from natural-language process descriptions by generating strictly validated Mermaid flowchart, sequenceDiagram, or classDiagram code, converting Mermaid to Excalidraw scene files, and exporting PNGs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zengiai](https://clawhub.ai/user/zengiai)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to turn natural-language process descriptions into validated Mermaid diagrams and hand-drawn Excalidraw or PNG outputs for workflow, interaction, and domain-model visualization.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Local npm dependencies and headless browser rendering introduce ordinary dependency and browser execution risk.

Mitigation: Use locked installs, audit dependencies before deployment, and run the renderer in a workspace-scoped local environment.

Risk: Untrusted or very large Mermaid inputs may create rendering failures, resource strain, or misleading visual output.

Mitigation: Validate Mermaid before export, keep output directories scoped to the workspace, and visually review generated PNG and Excalidraw files before relying on them.

## Reference(s):

- [Mermaid Generation Rules](references/mermaid-generation-rules.md)
- [Project homepage](https://github.com/zengiai/handdraw-flowchart)
- [ClawHub skill page](https://clawhub.ai/zengiai/skills/handdraw-flowchart)

## Skill Output:

**Output Type(s):** [Code, Shell commands, Files, Guidance]

**Output Format:** [Mermaid source with generated .mmd, .excalidraw, and .png files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Renderer validates supported Mermaid flowchart, sequenceDiagram, and classDiagram inputs before export; flowcharts provide the best editable Excalidraw output.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata; artifact frontmatter and package.json declare 0.1.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

## Description:

Generate hand-drawn-style Mermaid diagrams with robust syntax guidance for flowcharts, sequence diagrams, class diagrams, and state diagrams.

This skill is ready for commercial/non-commercial use.

## Publisher:

[1999azzar](https://clawhub.ai/user/1999azzar)

### License/Terms of Use:


## Use Case:

Developers and technical writers use this skill to turn architecture, workflow, API, object model, and lifecycle descriptions into Mermaid diagrams with safer syntax for common renderers.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Broad trigger phrases such as "draw this" or "visualize" may activate the skill when the user wanted a non-Mermaid output.

Mitigation: Ask explicitly for the desired output format when the request could mean Mermaid, prose, image generation, or another diagramming format.

Risk: Generated Mermaid may fail to render if labels, node IDs, subgraphs, or edge labels use unsafe syntax.

Mitigation: Use the included syntax guide rules for quoted labels, safe node IDs, explicit subgraph labels, and optional .mmd validation commands.

## Reference(s):

- [Mermaid Syntax Reference](references/syntax-guide.md)
- [ClawHub Skill Page](https://clawhub.ai/1999azzar/skills/mermaid-architect)

## Skill Output:

**Output Type(s):** [Markdown, Code, Shell commands, Guidance]

**Output Format:** [Markdown containing Mermaid code blocks and concise explanations]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include Mermaid validator shell commands for .mmd files when applicable.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

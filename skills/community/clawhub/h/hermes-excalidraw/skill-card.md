## Description:

Generates hand-drawn Excalidraw JSON diagrams for architecture, flow, sequence, and other visual communication tasks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[no7dw](https://clawhub.ai/user/no7dw)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, architects, and agents use this skill to create Excalidraw diagrams such as architecture diagrams, flowcharts, sequence diagrams, concept maps, and process maps, with layout rules for readable boxes, colors, and arrows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Diagram contents may be uploaded to Excalidraw for sharing.

Mitigation: Use local .excalidraw file generation for sensitive diagrams and require explicit approval before any upload step.

Risk: Browser navigation and screenshot steps may occur as part of verifying uploaded diagrams.

Mitigation: Require explicit approval before browser automation or screenshot capture, especially when diagrams may contain sensitive information.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/no7dw/skills/hermes-excalidraw)
- [Excalidraw](https://excalidraw.com)
- [Excalidraw Color Palette](references/colors.md)
- [Excalidraw Dark Mode Diagrams](references/dark-mode.md)
- [Excalidraw Diagram Examples](references/examples.md)
- [Skill Selection Model (Hermes & OpenClaw)](references/skill-selection-model.md)

## Skill Output:

**Output Type(s):** [Guidance, Code, Files, Shell commands]

**Output Format:** [Markdown guidance with Excalidraw JSON and optional shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces .excalidraw JSON files; optional upload command returns a shareable Excalidraw URL.]

## Skill Version(s):

2.1.0 (source: server release evidence and frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

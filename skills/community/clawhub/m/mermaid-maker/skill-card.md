## Description:

Generate, validate, render, and export Mermaid diagrams as .mmd source plus SVG, ASCII, PNG, or PDF outputs using local or Kroki-backed rendering workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[junwugit](https://clawhub.ai/user/junwugit)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and technical writers use this skill to create diagrams-as-code for architecture, API flows, class hierarchies, database schemas, state machines, timelines, and other Mermaid-supported visuals, then validate and render them for documentation or review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Diagram contents may be uploaded to a third-party service when the Kroki rendering path is used.

Mitigation: Use local beautiful-mermaid or mmdc rendering for confidential diagrams, and use Kroki only after explicit approval for content upload.

Risk: The bundled Node rendering scripts can automatically install npm dependencies when beautiful-mermaid is missing.

Mitigation: Review or pin npm dependencies before running bundled scripts, or install dependencies through a controlled package workflow.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/junwugit/skills/mermaid-maker)
- [Skill Homepage](https://github.com/Agents365-ai/creating-mermaid-diagrams)
- [Rendering and Export Backends](artifact/reference/RENDERING.md)
- [Mermaid Themes](artifact/reference/THEMES.md)
- [Flowchart Syntax](artifact/reference/FLOWCHART.md)
- [Sequence Diagram Syntax](artifact/reference/SEQUENCE.md)
- [Class and ER Diagram Syntax](artifact/reference/CLASS-ER.md)
- [Other Mermaid Diagram Types](artifact/reference/OTHER-TYPES.md)
- [Mermaid Live Editor](https://mermaid.live)
- [Kroki Mermaid SVG Endpoint](https://kroki.io/mermaid/svg)
- [Kroki Mermaid PNG Endpoint](https://kroki.io/mermaid/png)

## Skill Output:

**Output Type(s):** [Markdown, Code, Shell commands, Files, Guidance]

**Output Format:** [Markdown guidance with Mermaid code blocks and optional .mmd, SVG, ASCII text, PNG, or PDF files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Rendering can use local Node scripts, mermaid-cli, or Kroki; confidentiality depends on backend selection.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

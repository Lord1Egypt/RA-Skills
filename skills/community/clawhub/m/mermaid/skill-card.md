## Description:

Generate and render diagrams from Mermaid syntax into PNG, SVG, or PDF using customizable themes and common diagram types.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jarekbird](https://clawhub.ai/user/jarekbird)

### License/Terms of Use:


## Use Case:

Developers and technical writers use this skill to create Mermaid diagram source, render diagrams with Mermaid CLI, and return image or vector outputs for documentation, planning, architecture, and workflow explanations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill asks users to install an unpinned third-party Mermaid CLI package globally.

Mitigation: Use a pinned local installation of @mermaid-js/mermaid-cli where possible, review npm package provenance, and avoid global npm installs with elevated privileges.

Risk: Generated diagrams can be incomplete or misleading if the Mermaid source does not accurately reflect the intended system, workflow, or data model.

Mitigation: Review the Mermaid source and rendered output before publishing or using diagrams for decisions.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/jarekbird/skills/mermaid)
- [Official Mermaid Docs](https://mermaid.js.org/)
- [Mermaid Live Editor](https://mermaid.live/)
- [Mermaid Syntax Reference](https://mermaid.js.org/intro/syntax-reference.html)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with Mermaid code blocks, Mermaid CLI commands, and references to generated PNG, SVG, or PDF files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Rendered output depends on a working @mermaid-js/mermaid-cli installation and the selected theme, size, scale, and background options.]

## Skill Version(s):

1.0.0 (source: server-resolved release metadata and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

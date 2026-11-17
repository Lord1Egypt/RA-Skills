## Description:

Generate beautiful Mermaid.js diagrams with custom styling and themes. Create flowcharts, sequence diagrams, Gantt charts, class diagrams, etc. with enhanced visual appeal.

This skill is ready for commercial/non-commercial use.

## Publisher:

[caowen2211891](https://clawhub.ai/user/caowen2211891)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and technical writers use this skill to create styled Mermaid flowcharts, sequence diagrams, Gantt charts, class diagrams, and related diagrams for documentation and process visualization.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Installation changes global Node tooling by installing @mermaid-js/mermaid-cli with npm -g.

Mitigation: Review the global dependency before installation, prefer a pinned local install where possible, and run installation in an isolated development environment.

Risk: Generated HTML can include unescaped Mermaid content and loads Mermaid JavaScript from a CDN.

Mitigation: Avoid untrusted Mermaid input for HTML output, do not host generated HTML on a sensitive origin, and prefer SVG or PNG output for distribution.

## Reference(s):

- [Pretty Mermaid ClawHub listing](https://clawhub.ai/caowen2211891/skills/pretty-mermaid)
- [Publisher profile](https://clawhub.ai/user/caowen2211891)
- [Node.js](https://nodejs.org/)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Files, Configuration]

**Output Format:** [Markdown guidance with Mermaid code blocks, shell commands, and generated PNG, SVG, PDF, or HTML diagram files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May call mermaid-cli for image generation; HTML output can include interactive Mermaid rendering.]

## Skill Version(s):

1.0.0 (source: evidence.release.version)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

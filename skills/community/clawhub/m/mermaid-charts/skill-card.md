## Description:

使用 Mermaid 语法生成流程图、时序图、甘特图、饼图等多种图表，并指导代理输出 PNG 或交互型 HTML 图表文件。

This skill is ready for commercial/non-commercial use.

## Publisher:

[harrot90-code](https://clawhub.ai/user/harrot90-code)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, documentation writers, and agents use this skill to draft Mermaid diagrams for technical workflows, data models, timelines, journeys, and planning artifacts, then render them as PNG, SVG, PDF, or HTML when needed.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: HTML examples may load Mermaid JavaScript from a public CDN, which is unsuitable for some sensitive or offline documents.

Mitigation: For sensitive or offline use, pin, vendor, or self-host Mermaid before rendering HTML.

Risk: Generated Mermaid diagrams can misrepresent complex systems if syntax, layout, or labels are not reviewed.

Mitigation: Review the Mermaid source and rendered output before publishing or embedding diagrams.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/harrot90-code/skills/mermaid-charts)
- [Artifact SKILL.md](artifact/SKILL.md)

## Skill Output:

**Output Type(s):** [Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with Mermaid code blocks, shell commands, and HTML examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can guide creation of PNG, SVG, PDF, and HTML diagram files with Mermaid CLI or browser rendering.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

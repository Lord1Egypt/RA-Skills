## Description: <br>
Convert Markdown documents into PDF, PPTX, or HTML presentation slides using Marp with Mermaid diagram support. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mtdnot](https://clawhub.ai/user/mtdnot) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to turn Markdown content or generated slide outlines into presentation decks, including Mermaid diagrams and data visualizations. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Local renderers process Markdown, Mermaid diagrams, embedded HTML, and local file references. <br>
Mitigation: Use trusted Markdown and assets, review third-party decks before conversion, and keep local file access scoped to intended presentation resources. <br>
Risk: The Mermaid preprocessing step invokes a local diagram renderer on diagram content. <br>
Mitigation: Avoid running graph-generation steps on untrusted input and review diagram blocks before rendering. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/mtdnot/presentation-agent) <br>
- [Publisher profile](https://clawhub.ai/user/mtdnot) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Shell commands, Configuration, Files, Guidance] <br>
**Output Format:** [Markdown guidance with inline bash commands and generated presentation files in PDF, PPTX, or HTML format] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May invoke local Marp and Mermaid renderers and read local Markdown, theme, and image assets.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

## Description:

Automatically identify diagram code blocks (Mermaid/Graphviz/PlantUML) in Markdown documents, render them as images, and replace them.

This skill is ready for commercial/non-commercial use.

## Publisher:

[fireium](https://clawhub.ai/user/fireium)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and technical writers use this skill to convert Mermaid, Graphviz, and PlantUML code blocks in Markdown into embedded diagram images while optionally preserving the source diagram code.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Diagram contents can be sent to external rendering services when local renderers are unavailable, including PlantUML over plaintext HTTP.

Mitigation: Use local renderers for confidential documents and avoid processing credentials, private architecture, network topology, or other sensitive diagram content with network fallback enabled.

Risk: Default processing can overwrite the input Markdown file.

Mitigation: Use an explicit output file or a backup workflow before running the skill on important documents.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/fireium/skills/markdown-diagram-renderer)
- [Graphviz downloads](https://graphviz.org/download/)
- [Mermaid rendering service](https://mermaid.ink/)
- [PlantUML rendering service](http://www.plantuml.com/plantuml/)

## Skill Output:

**Output Type(s):** [Markdown, Files, JSON]

**Output Format:** [Markdown files with inline Base64 PNG or SVG image links, plus JSON execution status.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can preserve original diagram source as Markdown comments; defaults may overwrite the input file when no output path is provided.]

## Skill Version(s):

1.0.3 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

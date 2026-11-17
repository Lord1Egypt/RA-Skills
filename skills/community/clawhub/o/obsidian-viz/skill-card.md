## Description:

Generate Obsidian-compatible visualization files (Excalidraw / Mermaid / Canvas). Supports text descriptions and image inputs, outputs editable diagrams in Obsidian or standard formats.

This skill is ready for commercial/non-commercial use.

## Publisher:

[0xcjl](https://clawhub.ai/user/0xcjl)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, technical writers, and Obsidian users use this skill to turn text descriptions or diagram images into editable Mermaid, Excalidraw, or Canvas files for documentation and knowledge work.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Private screenshots, credentials, or regulated data may be transcribed into generated local outputs.

Mitigation: Avoid providing sensitive images or text unless the resulting files are acceptable to retain locally; review generated files before adding them to an Obsidian vault.

Risk: Generated diagrams may choose an unsuitable format or misrepresent complex source diagrams.

Mitigation: Review the generated Mermaid, Excalidraw, Canvas, or HTML output and split large diagrams when the source has many nodes or dense relationships.

Risk: Some Obsidian outputs require compatible local tooling.

Mitigation: Use Obsidian's built-in Mermaid and Canvas support where applicable, and install the Excalidraw plugin before relying on Excalidraw Markdown files.

## Reference(s):

- [Mermaid format reference](references/mermaid.md)
- [Excalidraw format reference](references/excalidraw.md)
- [Canvas format reference](references/canvas.md)
- [Excalidraw](https://excalidraw.com)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Configuration, Guidance]

**Output Format:** [Markdown plus Mermaid syntax, Excalidraw JSON, Obsidian Canvas JSON, and optional HTML]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Defaults to Obsidian-compatible files, with standard export formats available when requested.]

## Skill Version(s):

1.0.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

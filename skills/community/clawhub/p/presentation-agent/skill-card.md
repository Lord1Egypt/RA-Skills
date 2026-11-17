## Description:

Convert Markdown documents to presentation slides (PDF/PPTX/HTML) using Marp. Supports Mermaid diagrams (gantt, flowchart, etc.) and data graphs. Use when a user asks to create slides, presentations, or decks from Markdown files or text content.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mtdnot](https://clawhub.ai/user/mtdnot)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and content creators use this skill to turn Markdown or generated text into PDF, PPTX, or HTML slide decks with Marp. It is suited for presentation workflows that need Mermaid diagram preprocessing and bundled slide styling.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated decks may inherit the bundled Frexida visual style and attempted logo placement by default.

Mitigation: Review or replace the theme before use, especially for neutral, client-branded, or brand-sensitive presentations.

Risk: Untrusted Markdown and Mermaid content is processed by local conversion tools and rendered with local-file access enabled.

Mitigation: Run conversions in a constrained workspace and review input files before processing.

Risk: Generated output files may overwrite existing files when the same input basename and output directory are reused.

Mitigation: Choose a dedicated output directory or verify target filenames before running conversion commands.

## Reference(s):


## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, code, guidance]

**Output Format:** [Markdown guidance with shell commands and generated slide files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can produce PDF, PPTX, or HTML presentation files through Marp and local Mermaid image preprocessing.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

## Description:

Convert Markdown into a DOCX file using the shared marktodocx Node runtime. Use when the user explicitly wants Markdown content or a Markdown file converted to .docx in this repository.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zhao-kun](https://clawhub.ai/user/zhao-kun)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and document authors use this skill when they want an agent to convert local Markdown files or inline Markdown into DOCX output with optional style and margin settings.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill reads local Markdown and image paths and writes DOCX files, so broad or accidental paths can expose or overwrite unintended workspace files.

Mitigation: Use explicit input and output paths, review requested paths before execution, and run it only for deliberate Markdown-to-DOCX conversion requests.

Risk: Hostile Markdown or outdated dependencies could trigger unexpected converter behavior.

Mitigation: Avoid running untrusted Markdown until dependencies are updated, and keep dependency scanning in the release workflow.

Risk: The standard ClawHub export does not render Mermaid diagrams.

Mitigation: Keep Mermaid support disabled unless needed; when Mermaid is required, use a Mermaid-enabled export with the required Chromium runtime.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/zhao-kun/skills/marktodocx-skill)
- [Project repository](https://github.com/zhao-kun/markdocx)
- [GitHub releases](https://github.com/zhao-kun/markdocx/releases)
- [Markdown source preview](https://raw.githubusercontent.com/zhao-kun/markdocx/main/assets/images/markdown_preview.png)
- [Generated DOCX preview](https://raw.githubusercontent.com/zhao-kun/markdocx/main/assets/images/word_preview.png)

## Skill Output:

**Output Type(s):** [files, text, guidance]

**Output Format:** [DOCX file plus concise Markdown or text status with the written output path and relevant conversion constraints.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reads local Markdown and local image files, writes DOCX files, and fails clearly on Mermaid blocks in the standard ClawHub export.]

## Skill Version(s):

0.1.3 (source: package.json and server release evidence, released 2026-04-19)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

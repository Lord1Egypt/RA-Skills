## Description:

PDF视觉阅读器将 PDF 页面转换为高清 PNG 图片，并帮助 AI 视觉模型理解、分析和总结 PDF 内容。

This skill is ready for commercial/non-commercial use.

## Publisher:

[itixobepafi130-ctrl](https://clawhub.ai/user/itixobepafi130-ctrl)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, operators, and document-review agents use this skill when a user provides a PDF path or PDF file that needs visual understanding, especially slide decks, image-based PDFs, and scanned documents. It supports page-by-page visual analysis, summary generation, key-point extraction, and optional knowledge archiving.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: PDFs may contain sensitive document contents that are rendered to images and then processed by the current AI vision environment.

Mitigation: Use the skill only with PDFs that are appropriate for that environment, and archive extracted or analyzed contents only when the user explicitly requests it.

Risk: The artifact documents package names but does not pin dependency versions.

Mitigation: Install dependencies in an isolated environment and pin or review package versions before production use.

Risk: PDF page rendering creates PNG files in the selected output directory.

Mitigation: Choose an appropriate output directory and remove generated page images after analysis when they are no longer needed.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/itixobepafi130-ctrl/skills/pdf-vision-reader)

## Skill Output:

**Output Type(s):** [Text, Markdown, Files, Shell commands, Guidance]

**Output Format:** [Markdown summaries with generated PNG page-image files and optional shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The extraction script writes one PNG file per selected PDF page and prints the generated image paths for downstream visual analysis.]

## Skill Version(s):

1.0.0 (source: server release evidence and artifact _meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

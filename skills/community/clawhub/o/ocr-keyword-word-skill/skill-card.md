## Description:

从单张或多张图片批量提取中文文字，按用户指定关键词加粗标注，并输出适合复制到 Word 的 Markdown/text 内容。

This skill is ready for commercial/non-commercial use.

## Publisher:

[lilimoss-china](https://clawhub.ai/user/lilimoss-china)

### License/Terms of Use:

MIT

## Use Case:

External users, students, researchers, and editors use this skill to extract Chinese text from one or more uploaded images, highlight requested keywords, and prepare Word-friendly text for study notes, literature review, or document cleanup.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The release describes Word export, but the reviewed behavior primarily produces Markdown/text that is Word-friendly rather than a native .docx file.

Mitigation: Treat the output as reviewable Markdown/text and use a separate conversion step when a native Word document is required.

Risk: Uploaded images may contain sensitive personal, academic, or business information.

Mitigation: Review or redact sensitive image content before asking an agent to process it.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/lilimoss-china/skills/ocr-keyword-word-skill)
- [Publisher profile](https://clawhub.ai/user/lilimoss-china)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown text with bold keyword annotations and optional command-line helper usage]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs image-indexed paragraphs and keyword match counts; Word document creation may require copying, Markdown conversion, or an external tool such as Pandoc.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

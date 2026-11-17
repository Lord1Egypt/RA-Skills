## Description:

Converts Markdown files into formatted Word documents by uploading the source Markdown to md2word.com and downloading the generated DOCX file.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tian-0818](https://clawhub.ai/user/tian-0818)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, writers, and teams use this skill to convert Markdown documents into Word files while preserving formatting such as LaTeX and Mermaid rendering through an external conversion service.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Markdown document contents are sent to md2word.com for conversion.

Mitigation: Avoid using the skill for confidential, regulated, or proprietary documents unless the external service's privacy practices have been reviewed.

Risk: The pinned requests dependency should be updated according to the security guidance.

Mitigation: Review and refresh the pinned requests version before deployment in managed environments.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/tian-0818/skills/markdown-to-docx-converter)
- [md2word.com Converter](https://md2word.com/en)

## Skill Output:

**Output Type(s):** [Files, Markdown, Code, Shell commands, Guidance]

**Output Format:** [DOCX file plus concise status or error text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uploads user-provided Markdown content to md2word.com before returning the converted Word document.]

## Skill Version(s):

1.0.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

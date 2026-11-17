## Description:

将 Markdown、文本、DOCX、PDF、HTML 和 RTF 输入转换为符合国家标准的 .docx 政府公文格式文档。

This skill is ready for commercial/non-commercial use.

## Publisher:

[wisink](https://clawhub.ai/user/wisink)

### License/Terms of Use:

MIT-0

## Use Case:

Employees, external users, and developers use this skill to convert Markdown, text, DOCX, PDF, HTML, or RTF inputs into Chinese government-style DOCX reports for policy analysis, industry research, work reports, and training materials.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The converter prints short previews of parsed document content to the console.

Mitigation: Avoid running it on sensitive documents in shared terminals or logs, and clear console output when previews may expose private content.

Risk: The converter overwrites the chosen output path if it already exists.

Mitigation: Use a new output filename or back up existing DOCX files before running conversion.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wisink/skills/gongwen-writer)
- [政府公文格式规范](references/format-rules.md)
- [公文格式转换踩坑教训与解决方案](references/lessons-learned.md)

## Skill Output:

**Output Type(s):** [Files, Shell commands, Guidance]

**Output Format:** [DOCX file with concise Markdown or shell command guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The converter writes the selected DOCX output path and may print short previews of parsed document content to the console.]

## Skill Version(s):

1.4.0 (source: server release evidence and artifact _meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

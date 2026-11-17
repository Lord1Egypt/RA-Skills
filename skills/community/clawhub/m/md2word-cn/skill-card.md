## Description:

将 Markdown 文档转换为 Word 文档，专为中文文档设计，支持常见 Markdown 语法并默认使用仿宋字体。

This skill is ready for commercial/non-commercial use.

## Publisher:

[andyrong](https://clawhub.ai/user/andyrong)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to convert Chinese Markdown documents such as weekly reports, daily reports, and formal reports into Word DOCX files with consistent Chinese typography.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill asks users to install an unpinned python-docx dependency.

Mitigation: Install it in an isolated Python environment and pin python-docx before use.

Risk: The generated DOCX uses Chinese formatting defaults that may not suit non-Chinese documents.

Mitigation: Review the output document formatting before sharing or using it in production workflows.

## Reference(s):


## Skill Output:

**Output Type(s):** [Files, Shell commands, Guidance]

**Output Format:** [DOCX file plus concise command-line status text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses Chinese formatting defaults, including FangSong font and fixed heading sizes.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

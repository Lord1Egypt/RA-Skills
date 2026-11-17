## Description:

将中文需求或素材改写并排版为 Harvard 风格中文学术论文，包含摘要、关键词、目录、分级标题、参考文献，并可导出 DOCX。

This skill is ready for commercial/non-commercial use.

## Publisher:

[yikailucas](https://clawhub.ai/user/yikailucas)

### License/Terms of Use:


## Use Case:

Chinese-speaking students, researchers, and writers use this skill to turn notes or draft material into a structured Harvard-style academic paper and DOCX deliverable.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Untrusted Markdown may be processed by Pandoc without resource controls.

Mitigation: Use trusted source files, strip Markdown image or resource references, or run Pandoc in a sandbox with no network and limited filesystem access.

Risk: The generated DOCX may contain placeholder sections if the agent has not already produced polished paper text.

Mitigation: Review the DOCX before delivery and replace placeholders with complete academic content.

## Reference(s):

- [Harvard 引用速查](references/harvard-quick-guide.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Files, Guidance]

**Output Format:** [Chinese academic paper content, Markdown structure, shell command examples, and DOCX file output guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The DOCX workflow depends on Pandoc and should be checked for placeholder sections before use.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

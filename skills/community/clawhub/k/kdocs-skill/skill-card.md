## Description:

Operate Kdocs (WPS cloud documents) to create, read, edit, search, share, and organize online documents, spreadsheets, PDFs, and presentations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kdocs-app](https://clawhub.ai/user/kdocs-app)

### License/Terms of Use:

MIT-0

## Use Case:

People using Kdocs can manage cloud files and work with online documents, spreadsheets, PDFs, and presentations. The skill also provides guidance for document workflows such as content creation, conversion, and automation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Cloud workflows can overwrite document content, write spreadsheet data, or remove rows.

Mitigation: Start with document copies and require explicit approval for exact overwrites, spreadsheet write-back, and row removal.

Risk: The bundled installer may replace installed software, while the downloaded CLI, credential storage, and server-side behavior remain unverified.

Mitigation: Review before installing or updating, prefer browser login, and keep tokens out of chat.

Risk: Automation filters may lead to unintended actions on cloud spreadsheets.

Mitigation: Review workflow actions and targets, and test filters before activation.

## Reference(s):

- [Kdocs skill on ClawHub](https://clawhub.ai/kdocs-app/skills/kdocs-skill)
- [Kdocs homepage](https://www.kdocs.cn/latest)
- [Authentication reference](artifact/references/auth.md)

## Skill Output:

**Output Type(s):** [Guidance, Text, Markdown, Code, Shell commands, Configuration, Cloud document content]

**Output Format:** [Markdown guidance, shell commands, configuration, code, and cloud document content]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can create, update, upload, and organize cloud documents and office files.]

## Skill Version(s):

2.9.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

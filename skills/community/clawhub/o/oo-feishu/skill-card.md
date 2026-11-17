## Description:

Feishu (feishu.cn). Use this skill for ANY Feishu request — reading, creating, updating, and deleting data. Whenever a task involves Feishu, use this skill instead of calling the API directly.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Feishu users and developers use this skill to read and manage Feishu content and workflows through an OOMOL-connected account, including chat, documents, Drive, mail, calendars, tasks, approvals, and spreadsheets.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Setup executes downloaded code whose release has not been verified in the evidence.

Mitigation: Review setup before installation and choose and verify the CLI release yourself.

Risk: The CLI dependency's persistent effects are not fully described.

Mitigation: Grant only the Feishu permissions needed and retain confirmation for writes and deletions; consider disabling automatic skill synchronization before invoking it.

## Reference(s):

- [Feishu](https://www.feishu.cn)
- [Feishu API documentation](https://open.feishu.cn/document/home/index)
- [oo CLI](https://github.com/oomol-lab/oo-cli)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON, Shell commands]

**Output Format:** [Markdown guidance with shell command examples and JSON payloads; Feishu response data]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Actions may read or change Feishu data according to the selected operation and connected account permissions.]

## Skill Version(s):

1.0.8 (source: frontmatter, server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

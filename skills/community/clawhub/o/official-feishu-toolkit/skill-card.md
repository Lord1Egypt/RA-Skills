## Description:

Feishu/Lark office integration for agents that supports calendar and room booking, messaging, approvals, Bitable records, contacts, and attendance workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[radium0028](https://clawhub.ai/user/radium0028)

### License/Terms of Use:


## Use Case:

Developers and employees use this skill to connect an agent to a Feishu/Lark tenant for office workflows such as scheduling, message sending, approvals, Bitable operations, contact lookup, and attendance review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill exposes powerful Feishu tenant actions through a local API, including approvals, message sending, deletes, and business-record changes.

Mitigation: Run the service bound only to localhost, add caller authentication such as a local API token, grant only the minimum Feishu scopes, and require explicit human confirmation before sensitive actions.

Risk: The artifact recommends a remote curl-to-shell installer.

Mitigation: Inspect and verify the downloaded installer before executing it in any real Feishu tenant environment.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/radium0028/skills/official-feishu-toolkit)
- [Feishu Open Platform](https://open.feishu.cn/)
- [Feishu Developer Documentation](https://open.feishu.cn/document/)
- [Feishu API Explorer](https://open.feishu.cn/api-explorer)
- [Calendar and Rooms Reference](references/calendar.md)
- [Messaging Reference](references/messaging.md)
- [Approval Reference](references/approval.md)
- [Bitable Reference](references/bitable.md)
- [Contacts Reference](references/contacts.md)
- [Attendance Reference](references/attendance.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands, JSON request examples, and configuration instructions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires uv plus FEISHU_APP_ID and FEISHU_APP_SECRET environment variables.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

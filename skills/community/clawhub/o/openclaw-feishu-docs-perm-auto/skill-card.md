## Description:

自动为飞书文档添加用户权限，用于在创建文档后或用户反馈无权限时补充授权。

This skill is ready for commercial/non-commercial use.

## Publisher:

[sadjjk](https://clawhub.ai/user/sadjjk)

### License/Terms of Use:

MIT

## Use Case:

OpenClaw users and developers use this skill to grant Feishu document access after creating documents or when a recipient reports missing permissions. It checks Feishu app configuration, resolves document tokens and types, and guides permission updates for supported Feishu document formats.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles Feishu App Secrets and access tokens, which can be exposed if users paste real credentials into chat or logs.

Mitigation: Prefer a secure secret mechanism, restrict local configuration file permissions if file storage is unavoidable, avoid displaying full secrets, and rotate any secret already exposed.

Risk: The skill can grant broad Feishu document permissions, including full_access.

Mitigation: Before changing permissions, confirm the exact document, recipient open_id, and permission level, and use view or edit unless full_access is truly required.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/sadjjk/skills/openclaw-feishu-docs-perm-auto)
- [Feishu Open Platform](https://open.feishu.cn/app)
- [Feishu permission member API](https://open.feishu.cn/document/docs/permission/permission-member/batch_create)
- [Feishu Open ID FAQ](https://open.feishu.cn/document/faq/trouble-shooting/how-to-obtain-openid)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration, API calls, Markdown]

**Output Format:** [Markdown guidance with JSON snippets, shell commands, and Feishu API request examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce configuration checks, permission-change instructions, progress messages, and user-facing success or error responses.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

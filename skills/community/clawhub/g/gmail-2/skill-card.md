## Description:

[暂不可用] Gmail 邮件集成。收发邮件、搜索邮件、管理标签。通过 MorphixAI 代理安全访问 Gmail API。

This skill is ready for commercial/non-commercial use.

## Publisher:

[paul-leo](https://clawhub.ai/user/paul-leo)

### License/Terms of Use:


## Use Case:

OpenClaw users use this skill to read, search, send, mark, and trash Gmail messages through a linked MorphixAI Gmail connection.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can access sensitive Gmail content through an external MorphixAI plugin.

Mitigation: Install only if the MorphixAI plugin is trusted, prefer a pinned or otherwise verified plugin version, and review Gmail scopes during account linking.

Risk: The skill describes state-changing Gmail actions, including sending mail, marking messages read, and moving messages to trash.

Mitigation: Require preview and confirmation before sending or trashing messages.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/paul-leo/skills/gmail-2)
- [Morphix API keys](https://morphix.app/api-keys)
- [Morphix connections](https://morphix.app/connections)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration]

**Output Format:** [Markdown with inline tool examples and shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires MORPHIXAI_API_KEY and a linked Gmail account.]

## Skill Version(s):

0.1.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

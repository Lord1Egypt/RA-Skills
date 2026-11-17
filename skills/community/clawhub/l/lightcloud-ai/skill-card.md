## Description:

Integrates with Qingyun/Lightcloud (轻云) APIs to fetch access tokens and retrieve, create, update, or delete form documents through curl or PowerShell commands.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wzy2008a](https://clawhub.ai/user/wzy2008a)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operations teams use this skill to turn natural-language Qingyun/Lightcloud requests into authenticated API commands for form document retrieval, creation, update, and deletion.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles application secrets, access tokens, and refresh tokens.

Mitigation: Use a trusted package source, keep secrets out of chat and shell history, prefer environment variables or a secret manager, and redact tokens from output.

Risk: The skill can generate commands that update or delete Qingyun/Lightcloud business records.

Mitigation: Require explicit confirmation of the operation, workspace ID, form code ID, and exact record IDs before running any update or delete command.

## Reference(s):

- [轻云开放API参考文档](artifact/references/api_reference.md)
- [ClawHub skill page](https://clawhub.ai/wzy2008a/skills/lightcloud-ai)
- [Publisher profile](https://clawhub.ai/user/wzy2008a)
- [OpenClaw project](https://github.com/openclaw/openclaw)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with Bash and PowerShell command blocks plus JSON request examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses placeholders for credentials, access tokens, workspace IDs, form IDs, and record IDs.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

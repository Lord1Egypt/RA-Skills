## Description:

通过 OneBot HTTP API 使用本地命令（curl）发送 QQ 私聊或群消息。

This skill is ready for commercial/non-commercial use.

## Publisher:

[jqllxew](https://clawhub.ai/user/jqllxew)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to prepare QQ private-message or group-message requests for a trusted local OneBot/NapCat HTTP endpoint.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can produce shell-built HTTP commands for sending QQ messages through OneBot/NapCat, including message and file content supplied by the user.

Mitigation: Use only with a trusted local endpoint, require explicit confirmation before sending, and avoid sensitive messages or arbitrary local file paths.

Risk: The artifact includes a hardcoded bearer value and the security summary flags weak credential and confirmation handling.

Mitigation: Replace hardcoded bearer values with secure runtime configuration and confirm authentication requirements for the selected host and port.

Risk: Unsafe escaping of message or file content could make generated shell commands risky to execute.

Mitigation: Do not execute generated shell commands unless inputs are safely escaped or sent through a non-shell HTTP client.

## Reference(s):

- [ClawHub onebot skill page](https://clawhub.ai/jqllxew/skills/onebot)

## Skill Output:

**Output Type(s):** [shell commands, configuration, guidance]

**Output Format:** [Markdown with curl command blocks and concise setup guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Commands target OneBot private-message and group-message HTTP endpoints and may include CQ image or file message payloads.]

## Skill Version(s):

1.0.3 (source: server release metadata; artifact frontmatter says 1.0.2)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

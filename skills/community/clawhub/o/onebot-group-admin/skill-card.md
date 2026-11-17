## Description:

QQ 群管理操作，通过 OneBot 11 API 实现群名修改、群公告、禁言、踢人、设置管理员、全员禁言等功能。当用户需要在 QQ 群中执行管理操作时使用，如修改群名、发公告、禁言某人、踢人、设置管理员等。

This skill is ready for commercial/non-commercial use.

## Publisher:

[zhangalexhy](https://clawhub.ai/user/zhangalexhy)

### License/Terms of Use:

MIT-0

## Use Case:

QQ group operators and automation agents use this skill to prepare and run OneBot 11 group administration commands for tasks such as renaming groups, posting notices, muting or removing members, assigning administrators, and querying group information.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can expose broader bot-control capability than its QQ group administration purpose clearly scopes.

Mitigation: Use it only in a tightly controlled local environment, restrict actions and groups with an allowlist, and review sensitive operations before execution.

Risk: The bundled script supports reading parameter values from arbitrary local files with the @/path form.

Mitigation: Remove the arbitrary file-read feature before trusting the skill with real QQ groups or local secrets.

Risk: A fallback OneBot token is embedded in the script.

Mitigation: Rotate the embedded token, remove the hardcoded fallback, and require credentials through the environment.

Risk: Mute, kick, administrator, and whole-group-ban actions can disrupt group members if issued incorrectly.

Mitigation: Run the skill through a dedicated low-privilege bot account and require confirmation before sensitive group actions.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/zhangalexhy/skills/onebot-group-admin)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and JSON command results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Commands target a local OneBot WebSocket endpoint and may rely on ONEBOT_WS_URL and ONEBOT_WS_TOKEN environment variables.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

## Description:

Helps users configure Feishu bot accounts and connect OpenClaw agents to Feishu bot routing.

This skill is ready for commercial/non-commercial use.

## Publisher:

[leochens](https://clawhub.ai/user/leochens)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw operators use this skill to add Feishu bot accounts, choose account-level or group-level routing, and bind incoming Feishu messages to a selected agent.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles Feishu App Secrets during setup.

Mitigation: Do not pass real App Secrets in shell command history; use a protected secret input method or manually edit secured configuration.

Risk: The default DM policy can allow broad bot access.

Mitigation: Use restrictive DM access such as pairing or an allowlist before enabling the bot in a real OpenClaw environment.

Risk: The skill automatically changes OpenClaw configuration and may restart the gateway.

Mitigation: Review the generated configuration before restart and confirm backup/configuration files are owner-only and retained only as needed.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/leochens/skills/guantou-feishu-bot-connector)
- [Feishu OpenClaw bot setup page](https://open.feishu.cn/page/openclaw?form=multiAgent)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and JSON configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May update OpenClaw configuration, create a local backup, and request a gateway restart.]

## Skill Version(s):

1.0.0 (source: server release metadata and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

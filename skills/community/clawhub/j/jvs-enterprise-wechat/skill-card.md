## Description:

Helps agents configure OpenClaw to connect with an Enterprise WeChat AI Bot over a WebSocket-based AI Bot channel.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chenyd002025](https://clawhub.ai/user/chenyd002025)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and administrators use this skill to configure an OpenClaw gateway for Enterprise WeChat AI Bot messaging, including bot credentials, channel settings, restart commands, and troubleshooting checks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles Enterprise WeChat Bot ID and Secret values, and command-line secret arguments may expose credentials through shell history or process listings.

Mitigation: Enter credentials only in a private terminal, avoid passing the Secret on the command line, and keep the OpenClaw configuration file restricted to owner-only permissions.

Risk: The example configuration uses an open direct-message policy, which may allow broad bot access if used unchanged in a shared or production environment.

Mitigation: Change dmPolicy to pairing or allowlist for shared or production bots, and review the resulting channel configuration before restarting the gateway.

Risk: The security verdict is suspicious and advises source and version review before installation.

Mitigation: Review the package source before installing, prefer pinned package and plugin versions, and install only after confirming the release matches the intended ClawHub package.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/chenyd002025/skills/jvs-enterprise-wechat)
- [Enterprise WeChat AI Bot documentation](https://open.work.weixin.qq.com/help?doc_id=21657)
- [OpenClaw Enterprise WeChat plugin](https://github.com/WecomTeam/wecom-openclaw-plugin)
- [OpenClaw WeCom channel configuration](https://docs.openclaw.ai/channels/wecom)

## Skill Output:

**Output Type(s):** [markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and JSON configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes an optional Python setup script that writes Enterprise WeChat channel settings into an existing OpenClaw configuration file.]

## Skill Version(s):

1.0.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

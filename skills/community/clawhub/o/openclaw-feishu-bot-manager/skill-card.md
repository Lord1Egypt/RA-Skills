## Description:

Adds Feishu bot accounts to OpenClaw and binds an account or group chat to a selected Agent while updating Feishu routing configuration.

This skill is ready for commercial/non-commercial use.

## Publisher:

[caoychn](https://clawhub.ai/user/caoychn)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators managing OpenClaw Feishu integrations use this skill to add Feishu self-built app bot accounts and route account-level or group-level messages to the right Agent.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: App Secrets may be supplied through command-line arguments.

Mitigation: Avoid placing real App Secrets in shell history or process listings where possible, and rotate any secret that may have been exposed.

Risk: Backups of openclaw.json may contain bot credentials.

Mitigation: Restrict backup file permissions, store backups only where trusted users can read them, and remove stale backups after validation.

Risk: The default direct-message policy is broad for newly added bots.

Mitigation: Choose a restrictive DM policy such as pairing or allowlist when configuring production bots.

Risk: --dry-run is not fully no-write in this version because a backup can still be created.

Mitigation: Treat dry-run as a configuration preview rather than a no-side-effect mode, and test in a disposable OpenClaw configuration when needed.

Risk: Updating routing and restarting the Gateway can disrupt Feishu message handling.

Mitigation: Preview bindings before writing, use --no-restart when coordinating manual restarts, and apply changes during a maintenance window for critical bots.

## Reference(s):

- [ClawHub skill listing](https://clawhub.ai/caoychn/skills/openclaw-feishu-bot-manager)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown text with inline shell commands and JSON configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce OpenClaw configuration changes when executed; the interactive flow asks for credentials, routing target, preview, and confirmation.]

## Skill Version(s):

1.0.3 (source: evidence release and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

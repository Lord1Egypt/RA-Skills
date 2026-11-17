## Description:

Add a simple "Claude has finished." alert to Claude Code or other agent workflows through an OpenClaw-configured transport.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kyoiii](https://clawhub.ai/user/kyoiii)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use this skill to send simple completion notifications from Claude Code or compatible agent workflows through a configured OpenClaw transport.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The installer modifies global Claude Code hook settings for future completion events.

Mitigation: Review and back up ~/.claude/settings.json before installation, and confirm existing Stop or TaskCompleted hooks will not be overwritten.

Risk: The notification configuration file is sourced by a shell script.

Mitigation: Treat ~/.claude/mac-notify.env as executable configuration and review its contents before use.

Risk: Notifications can be sent to a configured WhatsApp target through OpenClaw.

Mitigation: Set OPENCLAW_NOTIFY_SELF_TARGET when appropriate so the script refuses to send to a different target.

## Reference(s):

- [Architecture](references/architecture.md)
- [ClawHub skill page](https://clawhub.ai/kyoiii/skills/personal-finish-notifier)

## Skill Output:

**Output Type(s):** [Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline bash commands and environment variable names]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Installs a shell hook and uses user-configured OpenClaw routing values for delivery.]

## Skill Version(s):

0.1.4 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

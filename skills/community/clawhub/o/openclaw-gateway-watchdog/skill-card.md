## Description:

Gateway Watchdog helps an agent install, configure, autostart, and run a Python watchdog that monitors an OpenClaw Gateway, restarts it when it is unavailable, and can send DingTalk status alerts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[adminlove520](https://clawhub.ai/user/adminlove520)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to keep an OpenClaw Gateway available by setting up an independent local monitor with optional DingTalk alerts, restart handling, logs, and autostart guidance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The watchdog can persist across sessions through autostart configuration.

Mitigation: Review the install path first, use a trusted pinned revision, avoid running it as root or administrator, and enable autostart only after uninstall and rollback steps are clear for the target OS.

Risk: The watchdog can automatically kill broadly matched local processes while trying to recover Gateway.

Mitigation: Narrow process termination to the exact Gateway process before production use and test restart behavior in a controlled environment.

Risk: DingTalk notifications can send operational status to the configured webhook.

Mitigation: Disable DingTalk unless that data sharing is acceptable, and protect the webhook URL and signing secret as sensitive configuration.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/adminlove520/skills/openclaw-gateway-watchdog)
- [README](artifact/README.md)
- [Architecture](artifact/ARCHITECTURE.md)
- [Changelog](artifact/CHANGELOG.md)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration]

**Output Format:** [Markdown with inline shell commands and configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include OS-specific setup steps, autostart instructions, log-checking commands, and DingTalk configuration guidance.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

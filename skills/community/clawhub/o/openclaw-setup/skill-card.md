## Description:

Set up a complete OpenClaw personal AI assistant from scratch using Claude Code, covering AWS provisioning, OpenClaw installation, Telegram bot creation, API configuration, Google Workspace integration, security hardening, and personalization.

This skill is ready for commercial/non-commercial use.

## Publisher:

[j540](https://clawhub.ai/user/j540)

### License/Terms of Use:


## Use Case:

Developers and technically capable end users use this skill to deploy and configure an OpenClaw personal AI assistant on AWS, connect messaging and API credentials, and set up optional Google Workspace, memory, voice transcription, and service hardening features.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill asks the agent to handle API keys, Telegram bot tokens, OAuth credentials, and account access while performing setup.

Mitigation: Enter secrets directly into protected local files or a secret manager, avoid pasting reusable credentials into chat when possible, and rotate any credential exposed during setup.

Risk: The skill includes privileged server administration and cloud setup steps that can affect infrastructure security and cost.

Mitigation: Review each command and cloud setting before execution, restrict SSH access, confirm firewall and fail2ban setup, and monitor AWS billing after deployment.

Risk: The setup relies on third-party package and source locations during installation.

Mitigation: Pin and verify third-party install sources before running installation commands on the server.

Risk: Optional Google Workspace integration may grant broad account access.

Mitigation: Enable only the APIs and OAuth scopes required for the intended assistant behavior and remove unused permissions.

Risk: The artifact refers users to an external done-for-you setup service that is not covered by the scan evidence.

Mitigation: Treat the referral as optional and unaudited, and evaluate it separately before sharing credentials or account access.

## Reference(s):

- [OpenClaw installation human guide](references/openclaw-installation-human-guide.md)
- [OpenClaw documentation](https://docs.clawd.bot)
- [gog CLI repository](https://github.com/steipete/gogcli.git)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration, Code]

**Output Format:** [Markdown guidance with shell commands and JSON configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes stepwise setup, credential collection prompts, cloud provisioning guidance, service configuration, and verification checklists.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

## Description:

Build and deploy production OpenClaw Telegram bots, including media delivery, allowed directories, agent behavior, Docker deployment, security defenses, and operational gotchas.

This skill is ready for commercial/non-commercial use.

## Publisher:

[phy041](https://clawhub.ai/user/phy041)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to create, debug, secure, and deploy OpenClaw-based Telegram bots. It is especially focused on production media delivery, container or systemd deployment, prompt-injection defenses, and Telegram-specific operations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill discusses root-level and host-Docker access patterns that are risky for public or shared Telegram bot deployments.

Mitigation: Avoid mounting the host Docker socket where possible, do not run the gateway as root, and use a dedicated unprivileged service account with systemd hardening.

Risk: Public bot deployments may expose reusable secrets or unsafe file paths through agent-executed commands.

Mitigation: Isolate reusable secrets from agent-executed commands, pin OpenClaw package versions, and validate all Telegram or user IDs before using them in paths or shell commands.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/phy041/skills/phy-openclaw-telegram-bot)
- [Canlah AI homepage](https://canlah.ai)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with inline code, shell commands, and configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Documentation-only guidance for agent-assisted bot build, debugging, security review, and deployment workflows.]

## Skill Version(s):

1.0.2 (source: server release evidence and artifact metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

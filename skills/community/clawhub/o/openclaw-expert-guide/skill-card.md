## Description:

Complete OpenClaw reference for answering setup, configuration, architecture, CLI, channel, provider, automation, security, installation, troubleshooting, and gateway protocol questions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[maxwellmelo](https://clawhub.ai/user/maxwellmelo)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, operators, and support agents use this skill as an offline OpenClaw reference for configuration, installation, troubleshooting, gateway behavior, channel setup, provider setup, CLI usage, automation, security hardening, and platform-specific guidance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Install guidance can lead users to run mutable remote code or make elevated or persistent system changes.

Mitigation: Prefer pinned versions, verified checksums or signatures, non-root installs, and explicit review before applying shell startup, daemon, or service changes.

Risk: Webhook and integration guidance can expose secrets if weak secret transport patterns are used.

Mitigation: Prefer header-based or signed webhook secrets and avoid query-string passwords.

Risk: Generated commands or configuration guidance could be incorrect or unsuitable for a user's environment.

Mitigation: Review proposed commands and configuration before execution or deployment, especially when they affect sandboxing, gateway access, or connected channels.

## Reference(s):

- [OpenClaw Expert Skill README](README.md)
- [OpenClaw Expert Skill Manifest](SKILL.md)
- [OpenClaw Core Concepts Reference](references/01-core-concepts.md)
- [OpenClaw Gateway Reference](references/02-gateway.md)
- [OpenClaw CLI Reference](references/03-cli.md)
- [OpenClaw Channels Reference](references/04-channels.md)
- [OpenClaw Providers Reference](references/05-providers.md)
- [OpenClaw Tools Reference](references/06-tools.md)
- [OpenClaw Plugins Reference](references/07-plugins.md)
- [OpenClaw Automation Reference](references/08-automation.md)
- [OpenClaw Installation and Setup Reference](references/09-installation.md)
- [OpenClaw Security, Help, Nodes, and Diagnostics Reference](references/10-security-and-misc.md)
- [OpenClaw Platforms Reference](references/11-platforms.md)
- [OpenClaw Configuration and Protocol Reference](references/12-reference.md)
- [OpenClaw Documentation](https://docs.openclaw.ai)
- [OpenClaw Repository](https://github.com/openclaw/openclaw)
- [ClawHub Skill Page](https://clawhub.ai/maxwellmelo/skills/openclaw-expert-guide)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration]

**Output Format:** [Markdown with inline code blocks and configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include OpenClaw commands, JSON or JSON5 configuration snippets, troubleshooting steps, and security guidance.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

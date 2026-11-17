## Description:

OpenClaw self-hosted AI agent framework expert covering installation, configuration, channels, memory, multi-agent routing, Docker deployment, troubleshooting, and security hardening.

This skill is ready for commercial/non-commercial use.

## Publisher:

[arn0ld87](https://clawhub.ai/user/arn0ld87)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, operators, and self-hosting administrators use this skill for OpenClaw setup, configuration, channel integration, memory tuning, multi-agent routing, Docker deployment, troubleshooting, and security hardening.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security review marks the skill suspicious because it is documentation-only but recommends high-impact installation and permission commands.

Mitigation: Review commands before execution, avoid blind curl-to-shell, sudo bash, chmod -R 777, and shell profile helper commands, and prefer official package-manager installs or pinned and checksummed downloads.

Risk: OpenClaw administration guidance may involve credentials, gateway exposure, and persistent configuration changes.

Mitigation: Use restrictive permissions, SecretRef-based credential handling, backups before changes, and OpenClaw validation commands before restarting services.

## Reference(s):

- [OpenClaw Documentation](https://docs.openclaw.ai)
- [OpenClaw Docker Documentation](https://docs.openclaw.ai/install/docker)
- [OpenClaw Agent Workspace Documentation](https://docs.openclaw.ai/concepts/agent-workspace)
- [OpenClaw Memory Documentation](https://docs.openclaw.ai/concepts/memory)
- [OpenClaw Multi-Agent Documentation](https://docs.openclaw.ai/concepts/multi-agent)
- [OpenClaw Session Documentation](https://docs.openclaw.ai/concepts/session)
- [OpenClaw Cron Jobs Documentation](https://docs.openclaw.ai/automation/cron-jobs)
- [OpenClaw Secrets Documentation](https://docs.openclaw.ai/gateway/secrets)
- [OpenClaw Configuration Documentation](https://docs.openclaw.ai/gateway/configuration)
- [OpenClaw Models Documentation](https://docs.openclaw.ai/models)
- [OpenClaw Skills Documentation](https://docs.openclaw.ai/tools/skills)
- [OpenClaw Security Documentation](https://docs.openclaw.ai/security)
- [Quick Reference](references/quick-reference.md)
- [Installation & Erste Schritte](references/installation.md)
- [Config-Referenz](references/config-reference.md)
- [Dashboard / Control UI](references/dashboard.md)
- [Workspace-Dateien](references/workspace-files.md)
- [Channels](references/channels.md)
- [Memory-System](references/memory-system.md)
- [Docker-Deployment](references/docker-setup.md)
- [Security-Hardening](references/security-hardening.md)
- [Skills](references/skills-guide.md)
- [Multi-Agent-Routing](references/multi-agent.md)
- [OpenClaw CLI-Referenz](references/cli-reference.md)
- [Nodes & Remote Access](references/nodes-and-remote.md)
- [Tailscale-Integration](references/tailscale-integration.md)
- [Praxis-Beispiele](references/examples.md)
- [Troubleshooting](references/troubleshooting.md)
- [Tricks & Hacks](references/tricks-and-hacks.md)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration]

**Output Format:** [Markdown guidance with inline shell commands and configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Documentation-only agent assistance; users should review commands and configuration changes before execution.]

## Skill Version(s):

1.1.0 (source: server release metadata and artifact/skill.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

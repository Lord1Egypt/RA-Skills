## Description:

OpenClaw Agent Skill helps agents answer OpenClaw setup, configuration, deployment, CLI, channel, provider, plugin, and troubleshooting questions using bundled documentation from docs.openclaw.ai.

This skill is ready for commercial/non-commercial use.

## Publisher:

[brabaflow](https://clawhub.ai/user/brabaflow)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to get grounded OpenClaw guidance, exact CLI commands, configuration examples, and troubleshooting steps from bundled documentation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can surface installer, deployment, repair, daemon, Tailscale, Node, and Docker commands that may change a host or expose services.

Mitigation: Review privileged commands before running them, avoid root unless necessary, and prefer dry-run or least-privilege setup paths when available.

Risk: Some documented install or update flows run remote scripts directly without integrity checks.

Mitigation: Download scripts first, inspect them, and verify publisher checksums or signatures when available before execution.

Risk: OpenClaw setup and repair workflows can involve credentials, configuration files, channel tokens, and backups.

Mitigation: Back up OpenClaw credentials and configuration before repair or update flows, and treat backups as production secrets.

## Reference(s):

- [OpenClaw Agent Skill on ClawHub](https://clawhub.ai/brabaflow/skills/openclaw-agent-skill)
- [OpenClaw Documentation](https://docs.openclaw.ai/)
- [OpenClaw Quick Start](https://docs.openclaw.ai/start/quickstart)
- [OpenClaw Installation](https://docs.openclaw.ai/install)
- [OpenClaw Gateway Security](https://docs.openclaw.ai/gateway/security)
- [OpenClaw Gateway Sandboxing](https://docs.openclaw.ai/gateway/sandboxing)
- [OpenClaw Tool Execution](https://docs.openclaw.ai/tools/exec)
- [OpenClaw Threat Model](https://docs.openclaw.ai/security/THREAT-MODEL-ATLAS)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown responses with citations and exact code or configuration blocks when needed]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Answers are expected to cite the relevant bundled OpenClaw documentation section.]

## Skill Version(s):

1.0.0 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

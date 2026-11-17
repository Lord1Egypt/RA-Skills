## Description:

OpenClaw Anything wraps the openclaw CLI and provides local reference docs for managing gateways, channels, models, agents, nodes, browser automation, memory, security, automation, and deployment.

This skill is ready for commercial/non-commercial use.

## Publisher:

[doanbactam](https://clawhub.ai/user/doanbactam)

### License/Terms of Use:


## Use Case:

Developers and operators use this skill to route OpenClaw CLI tasks, look up command syntax, and manage configuration, gateways, channels, models, agents, nodes, browser tooling, secrets, security checks, and deployment workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill wraps broad OpenClaw administrative capabilities, including configuration, services, messaging, secrets, DNS, nodes, browser state, and automation.

Mitigation: Run under a least-privileged account, pin and verify the OpenClaw CLI version, keep gateway tokens and environment secrets protected, and manually confirm mutating actions.

Risk: The security evidence says the wrapper approval gate does not consistently block all documented high-risk changes.

Mitigation: Treat OPENCLAW_WRAPPER_ALLOW_RISKY=1 as a convenience gate rather than a safety boundary, and require explicit per-action review for high-risk command groups.

Risk: Remote node, browser, device, camera, screen, location, webhook, DNS, secrets, sandbox, plugin, and hook operations can affect systems or expose sensitive data.

Mitigation: Prefer read-only status, list, health, logs, docs, and audit commands first; verify node identity before approval; use dry-run or audit modes where available; keep gateways on loopback or VPN/Tailscale unless remote access is intentional.

## Reference(s):

- [OpenClaw Documentation](https://docs.openclaw.ai/)
- [OpenClaw CLI Documentation](https://docs.openclaw.ai/cli)
- [OpenClaw Configuration Documentation](https://docs.openclaw.ai/cli/config)
- [OpenClaw Gateway Configuration](https://docs.openclaw.ai/gateway/configuration)
- [OpenClaw Docker Installation](https://docs.openclaw.ai/install/docker)
- [ClawHub Skill Page](https://clawhub.ai/doanbactam/skills/openclaw-anything)
- [OpenClaw CLI Reference](references/cli-full.md)
- [OpenClaw Security Policy](references/security-policy.md)
- [OpenClaw Configuration Reference](references/config-schema.md)
- [OpenClaw Deployment](references/deployment.md)
- [OpenClaw Prerequisites](references/prerequisites.md)
- [OpenClaw Nodes and Platforms](references/nodes-platforms.md)
- [OpenClaw Advanced Tools](references/advanced-tools.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands, configuration examples, and wrapper command routes.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires the openclaw CLI in PATH; high-risk wrapper routes are gated by OPENCLAW_WRAPPER_ALLOW_RISKY=1.]

## Skill Version(s):

2.0.0 (source: server release metadata and artifact _meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

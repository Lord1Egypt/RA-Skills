## Description:

Enables two OpenClaw instances to monitor each other with heartbeat checks, report health status, diagnose failures, and perform configured repair actions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[rfdiosuao](https://clawhub.ai/user/rfdiosuao)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to run paired OpenClaw instances that monitor peer availability, check memory, CPU, and process health, and provide diagnostics or repair actions for high-availability deployments.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill exposes heartbeat and repair endpoints that can trigger powerful remote restart behavior.

Mitigation: Do not expose port 9528 publicly; bind to trusted interfaces, restrict access to the peer host, and require authentication or mutual TLS before deployment.

Risk: Published material includes an exposed ClawHub token.

Mitigation: Revoke the published token and remove secrets from release artifacts and documentation before reuse.

Risk: Repair and diagnostic behavior can execute shell commands using host and port configuration.

Mitigation: Validate host and port inputs, avoid shell interpolation, add request limits, and keep repair actions explicit and reversible.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/rfdiosuao/skills/openclaw-mutual-repair)
- [OpenClaw documentation](https://docs.openclaw.ai)
- [OpenClaw stability optimization document](https://my.feishu.cn/docx/Tgu7dwKX5ol7m8xNF4ycadjznPe)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown responses with health status, diagnostic findings, repair suggestions, and inline shell command or configuration snippets.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires configured peer host and port values; repair workflows may issue PM2 or systemd restart commands when invoked.]

## Skill Version(s):

1.0.0 (source: server release metadata, skill.json, package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

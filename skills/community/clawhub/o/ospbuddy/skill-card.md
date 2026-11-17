## Description:

OpsBuddy helps users set up an OpenClaw MCP connection to a third-party intelligent operations assistant for asset discovery, monitoring, fault diagnosis, log search, alert analysis, and remediation guidance.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hatjs880328s](https://clawhub.ai/user/hatjs880328s)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operations teams use this skill to understand OpsBuddy capabilities and connect the OpsBuddy MCP server in OpenClaw without sharing API keys in chat. Once connected, users can query monitoring and operations data for health checks, root-cause diagnosis, log search, alert analysis, and remediation suggestions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The OpsBuddy portal and gateway may handle operational telemetry and monitoring credentials configured outside the skill.

Mitigation: Install only if the user trusts the OpsBuddy portal and gateway, and use read-only, least-privilege provider credentials.

Risk: The downloaded MCP configuration contains a plaintext bearer token.

Mitigation: Keep the token and config JSON out of chat, inspect the config before enabling it, and revoke or rotate the token if it is exposed.

Risk: Operational diagnosis and remediation suggestions may be incomplete or incorrect.

Mitigation: Review recommendations before acting on production systems, especially when troubleshooting outages or changing operational procedures.

## Reference(s):

- [OpsBuddy ClawHub page](https://clawhub.ai/hatjs880328s/skills/ospbuddy)
- [OpsBuddy portal](https://ywdz.lxiai.com/)

## Skill Output:

**Output Type(s):** [text, markdown, configuration, guidance]

**Output Format:** [Markdown guidance with JSON configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a user-provided OpsBuddy MCP token; the skill tells users not to paste tokens or config JSON into chat.]

## Skill Version(s):

1.0.9 (source: server release metadata; artifact frontmatter reports 1.1.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

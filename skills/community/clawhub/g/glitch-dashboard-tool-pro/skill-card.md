## Description:

统一仪表盘专业版 helps agents operate an IT operations dashboard with custom panels, alert rules, multi-node monitoring, historical trend analysis, role controls, and structured status output.

This skill is ready for commercial/non-commercial use.

## Publisher:

[thcjp](https://clawhub.ai/user/thcjp)

### License/Terms of Use:

MIT-0

## Use Case:

External developers, operations engineers, and enterprise teams use this skill to guide agents through dashboard startup, monitoring status checks, alert configuration, batch operations, and team-oriented operations workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill asks for operational command authority, including service startup and dashboard management.

Mitigation: Require explicit user confirmation before starting services, running deployment actions, or executing operational commands.

Risk: Dashboard access could expose operational data if bound broadly or left unauthenticated.

Mitigation: Bind dashboards to localhost by default and require authentication before exposing them beyond the local machine.

Risk: Batch operations and webhook callbacks can affect many targets or external systems.

Mitigation: Limit targets explicitly, test batch actions on a small scope first, and require confirmation before webhook callbacks.

Risk: API keys and shared credentials may be exposed if storage and sharing mechanisms are unclear.

Mitigation: Use a dedicated secret manager or environment variables, avoid plaintext credential sharing, and mask secrets in output.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/thcjp/skills/glitch-dashboard-tool-pro)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands, JSON configuration examples, and structured JSON-style result summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May propose dashboard service startup, webhook callbacks, batch operations, and operational commands that require confirmation before execution.]

## Skill Version(s):

1.0.0 (source: server release evidence and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

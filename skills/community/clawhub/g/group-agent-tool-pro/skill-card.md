## Description:

Agent群组工具专业版 helps enterprise teams govern multi-agent groups with cross-instance federation, role-based permissions, group bots, encryption, enterprise IM synchronization, and collaboration analytics.

This skill is ready for commercial/non-commercial use.

## Publisher:

[thcjp](https://clawhub.ai/user/thcjp)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and enterprise agent operators use this skill to configure and govern multi-agent group collaboration across federated instances, enterprise roles, bots, encrypted channels, IM integrations, analytics, and audit workflows.

### Deployment Geography for Use:

Global; artifact examples include China data-residency and restricted cross-border configurations that should be reviewed before deployment.

## Known Risks and Mitigations:

Risk: Broad command, write, bot, and external-sync authority can change local state or trigger external workflows.

Mitigation: Narrow trigger conditions and require explicit confirmation before command execution, file writes, permission changes, exports, Webhooks, IM synchronization, and SIEM/BI forwarding.

Risk: Webhook, IM, SIEM, and BI integrations can expose collaboration data to unintended destinations.

Mitigation: Verify destination allowlists, audit logging, retention controls, and credential handling before enabling integrations.

Risk: Enterprise group governance workflows can grant or synchronize permissions across sensitive groups.

Mitigation: Use least-privilege roles, review administrator/editor grants, and require additional approval for sensitive or encrypted group changes.

## Reference(s):

- [Detailed Reference](references/detail.md)
- [ClawHub Skill Listing](https://clawhub.ai/thcjp/skills/group-agent-tool-pro)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with YAML, Python, Bash, and JSON examples.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May propose command execution, file writes, permission changes, webhook forwarding, IM synchronization, and SIEM/BI forwarding; human confirmation is recommended before use.]

## Skill Version(s):

1.0.1 (source: server-resolved release metadata; artifact frontmatter reports 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

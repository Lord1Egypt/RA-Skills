## Description:

Proactive Ops Monitor helps OpenClaw agents track token utilization, memory-layer health, alerts, and open-loop suggestions to reduce context-overflow risk.

This skill is ready for commercial/non-commercial use.

## Publisher:

[neroagent](https://clawhub.ai/user/neroagent)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to monitor workspace health, estimate context-token pressure, review alerts, and get suggested next steps from recent memory signals.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can surface recent agent-memory content, including selected draft, decision, or correction content, in dashboards or suggestions.

Mitigation: Install only in workspaces where this level of memory visibility is acceptable, and review generated dashboards or suggestions before sharing them.

Risk: Alert and configuration behavior can persist operational details in workspace files.

Mitigation: Review and remove workspace alert or configuration files when they contain operational details that should not be retained.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/neroagent/skills/proactive-ops-monitor)

## Skill Output:

**Output Type(s):** [text, JSON, configuration, guidance]

**Output Format:** [Plain text dashboards and JSON responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May persist alert and configuration files in the workspace when alerting or configuration features are used.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

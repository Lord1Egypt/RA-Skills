## Description:

Connects monitoring agents to SolarWinds Orion, PRTG, and Zabbix for NOC health checks, alert triage, and supported maintenance actions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zw008](https://clawhub.ai/user/zw008)

### License/Terms of Use:

MIT-0

## Use Case:

NOC operators and infrastructure engineers use this skill to review health and alerts across SolarWinds, PRTG, and Zabbix, and carry out supported maintenance changes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security assessment reports a weakness around TLS verification.

Mitigation: Enable certificate verification for production monitoring endpoints; limit any exceptions for self-signed certificates to controlled lab use.

Risk: The security assessment notes there is no enforced approval gate before installation, which matters when connecting accounts that can make disruptive changes.

Mitigation: Review the release before installation and require operator approval before using it with accounts that can change monitoring state.

Risk: Some local references could not be resolved during scanning, so the available scan does not establish that all referenced material was assessed.

Mitigation: Review unresolved references and their behavior before deployment.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/zw008/skills/monitoring-aiops)
- [Project homepage (listed in Clawdis metadata)](https://github.com/AIops-tools/Monitoring-AIops)
- [Capabilities reference](artifact/references/capabilities.md)
- [Setup and security guide](artifact/references/setup-guide.md)
- [CLI reference](artifact/references/cli-reference.md)
- [Agent guardrails](artifact/references/agent-guardrails.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Operational guidance, Configuration instructions, Shell commands]

**Output Format:** [Concise monitoring summaries and guidance, with structured tool results when available]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include read results or proposed monitoring changes; write operations affect configured monitoring systems.]

## Skill Version(s):

0.13.1 (source: server-resolved release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

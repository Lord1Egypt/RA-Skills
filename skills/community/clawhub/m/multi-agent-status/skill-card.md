## Description:

Cross-agent health monitoring for multi-host OpenClaw deployments where each agent pushes structured JSON status reports to a central location for a monitoring agent to read and alert on failures.

This skill is ready for commercial/non-commercial use.

## Publisher:

[agenthyjack](https://clawhub.ai/user/agenthyjack)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operations teams use this skill to configure multi-host OpenClaw agents to publish small JSON health reports and have a monitoring agent check gateway health, cron errors, stale reports, and missing reports.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Remote status-reporting scripts are referenced without a pinned version.

Mitigation: Review the scripts before use and pin them to a trusted commit or vendor reviewed copies locally.

Risk: A world-writable shared status directory can allow unauthorized report modification or deletion.

Mitigation: Use least-privilege ownership and permissions, such as a dedicated group with 770 or tighter access instead of chmod 777.

Risk: Forged, stale, or deleted status reports can mislead monitoring and alerts.

Mitigation: Treat the status directory as operationally sensitive and monitor report freshness, ownership, and unexpected changes.

## Reference(s):

- [Multi-Agent Status ClawHub Skill Page](https://clawhub.ai/agenthyjack/skills/multi-agent-status)
- [Collective Skills references directory](https://github.com/Bobalouie44/collective-skills/tree/main/references)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration]

**Output Format:** [Markdown with bash, PowerShell, JSON, and configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces agent status-reporting setup guidance and example monitoring thresholds; generated reports are small JSON files.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

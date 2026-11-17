## Description:

Monitors n8n Docker containers by checking container status, recent logs, health, and CPU and memory usage.

This skill is ready for commercial/non-commercial use.

## Publisher:

[smitti7971](https://clawhub.ai/user/smitti7971)

### License/Terms of Use:


## Use Case:

Developers and operators use this skill to inspect operational state for n8n containers through Docker status, log, health, and resource usage checks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Inspecting Docker status and n8n logs may expose workflow details or secrets present in container output.

Mitigation: Install only where the agent is authorized to inspect Docker and n8n logs, and review log output before sharing it outside the operating environment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/smitti7971/skills/n8n-monitor)

## Skill Output:

**Output Type(s):** [Markdown, Shell commands, Guidance]

**Output Format:** [Markdown with simple tables and inline Docker commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Status-focused operational summaries for n8n Docker containers.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

## Description:

Monitors n8n Docker containers by checking container status, recent logs, health, and CPU and memory usage.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yesong-hue](https://clawhub.ai/user/yesong-hue)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operations teams use this skill to monitor n8n running in Docker by checking container status, recent logs, health, and resource usage.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Recent n8n Docker logs may contain sensitive operational details.

Mitigation: Use the skill only on trusted hosts and limit sharing of log excerpts to appropriate operational contexts.

Risk: Docker inspection exposes local container status, health, and resource information.

Mitigation: Install only where the agent is intended to inspect the local n8n Docker environment and has appropriate Docker access.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/yesong-hue/skills/n8n-docker-monitor)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Guidance]

**Output Format:** [Markdown with simple tables and inline Docker command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May reference recent Docker logs and container health and status signals.]

## Skill Version(s):

1.0.0 (source: server release metadata and SKILL.md frontmatter; artifact _meta.json and skill.yaml differ)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

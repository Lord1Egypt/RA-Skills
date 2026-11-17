## Description:

Proactive health monitoring for AI agents. Apple Health integration, pattern detection, anomaly alerts. Built for agents caring for humans with chronic conditions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ctsolutionsdev](https://clawhub.ai/user/ctsolutionsdev)

### License/Terms of Use:

MIT

## Use Case:

External users, caregivers, and agent operators use this skill to import Apple Health exports, monitor health trends, and surface anomaly alerts for humans with chronic conditions or disabilities.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill reads and stores sensitive Apple Health export data locally.

Mitigation: Review the configuration and local data directory before installation, and use it only where local storage of health readings is acceptable.

Risk: Hourly monitoring and external alert channels can expose health information outside the machine.

Mitigation: Keep external alert channels disabled unless the operator has reviewed what information may be sent and configured an appropriate private channel.

Risk: Anomaly alerts and health summaries may be incomplete or clinically incorrect.

Mitigation: Treat outputs as monitoring prompts for human review, not as diagnosis or medical advice.

## Reference(s):

- [Health Auto Export App](https://apps.apple.com/app/health-auto-export/id1115567069)
- [ClawHub Skill Page](https://clawhub.ai/ctsolutionsdev/skills/proactive-health)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with JSON configuration examples and inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces local health summaries and anomaly alerts from locally stored Apple Health export data.]

## Skill Version(s):

1.0.0 (source: frontmatter, package.json, server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

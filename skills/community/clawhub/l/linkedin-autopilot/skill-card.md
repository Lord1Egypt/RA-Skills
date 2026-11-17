## Description:

LinkedIn Autopilot helps an agent run LinkedIn posting, engagement, connection outreach, DM follow-up sequences, and reporting with configurable rate limits and dry-run workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[audsmith28](https://clawhub.ai/user/audsmith28)

### License/Terms of Use:


## Use Case:

External users and developers use this skill to configure an agent to manage LinkedIn posting, target engagement, connection requests, DM follow-up sequences, and analytics reporting for personal networking or lead-generation workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill asks for raw LinkedIn credentials.

Mitigation: Avoid plaintext password storage where possible and lock down secrets and configuration files before use.

Risk: Automated posting, messaging, engagement, and connection activity can expose the account to automation-related restrictions.

Mitigation: Use only with an account you are willing to expose to automation risk, keep dry-run enabled until actions are reviewed, and monitor for warnings or security checks.

Risk: Automated comments, DMs, and connection notes may send unwanted or inaccurate content.

Mitigation: Review queued recipients and message or post content before enabling send actions, with human oversight for sensitive interactions.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/audsmith28/skills/linkedin-autopilot)
- [Publisher Profile](https://clawhub.ai/user/audsmith28)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell command invocations and JSON configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes dry-run workflows and file-based activity, sequence, connection, analytics, and report outputs under the configured LinkedIn Autopilot directory.]

## Skill Version(s):

1.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

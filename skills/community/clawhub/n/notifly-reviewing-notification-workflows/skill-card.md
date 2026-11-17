## Description:

Reviews workflows, channels, topics, and recent delivery activity in a selected Notifly environment without sending notifications.

This skill is ready for commercial/non-commercial use.

## Publisher:

[devino](https://clawhub.ai/user/devino)

### License/Terms of Use:

MIT-0

## Use Case:

Teams reviewing their Notifly notification setup can map workflows and topics, inspect channels and steps, and check a recent sample of delivery activity without triggering sends.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The review gives the agent access to workflow configuration, topics, and recent notification activity in the selected environment.

Mitigation: Connect only an environment whose notification data you are comfortable sharing with the agent, and review its access before use.

Risk: A small recent activity sample can be mistaken for complete delivery analytics.

Mitigation: Describe the sample as recent events and avoid claiming delivery rates or broader trends it does not support.

## Reference(s):

- [Reviewing Notification Workflows on ClawHub](https://clawhub.ai/devino/skills/notifly-reviewing-notification-workflows)

## Skill Output:

**Output Type(s):** [Text, Markdown, Analysis]

**Output Format:** [Markdown summary and tables]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Read-only review of the selected environment; recent activity is a sample, not an analytics report.]

## Skill Version(s):

1.0.1 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

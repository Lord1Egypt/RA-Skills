## Description:

Google Workflow: Today's meetings + open tasks as a standup summary.

This skill is ready for commercial/non-commercial use.

## Publisher:

[googleworkspace-bot](https://clawhub.ai/user/googleworkspace-bot)

### License/Terms of Use:

MIT-0

## Use Case:

Employees and teams use this skill to ask an agent for a read-only standup summary that combines today's Google Calendar meetings with open Google Tasks through the gws CLI.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill relies on the gws CLI to read Google Calendar and Tasks data, which may expose sensitive schedule and task information to the local agent workflow.

Mitigation: Install only where the gws CLI is already trusted and authorized for the intended Google Workspace account.

Risk: Standup summaries can omit, misread, or overemphasize calendar and task details.

Mitigation: Review generated summaries before sharing them with teammates or using them as status records.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/googleworkspace-bot/skills/gws-workflow-standup-report)
- [Publisher profile](https://clawhub.ai/user/googleworkspace-bot)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Text, Configuration]

**Output Format:** [Markdown guidance with bash command examples; gws command output can be JSON, table, YAML, or CSV.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires the gws CLI and Google Workspace authentication configured by the related shared gws skill.]

## Skill Version(s):

1.0.12 (source: evidence.json release.version; artifact metadata version 0.22.5)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

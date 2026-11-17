## Description:

Google Workflow: Prepare for your next meeting: agenda, attendees, and linked docs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[googleworkspace-bot](https://clawhub.ai/user/googleworkspace-bot)

### License/Terms of Use:

MIT-0

## Use Case:

Employees and Google Workspace users use this skill to have an agent prepare for the next upcoming meeting by gathering agenda, attendee, description, and linked-document context.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill depends on the existing gws Google Workspace CLI reading calendar meeting details and related metadata.

Mitigation: Install only when that calendar access is acceptable, and review the generated or shared gws authentication instructions before use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/googleworkspace-bot/skills/gws-workflow-meeting-prep)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration]

**Output Format:** [Markdown with inline bash commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Invokes the existing gws CLI and supports json, table, yaml, and csv output formats from that CLI.]

## Skill Version(s):

1.0.12 (source: server release evidence); underlying skill metadata version 0.22.5

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

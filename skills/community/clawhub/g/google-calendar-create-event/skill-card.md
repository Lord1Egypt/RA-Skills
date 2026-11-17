## Description:

Atomic node skill to create a Google Calendar event using the gog CLI.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zvirb](https://clawhub.ai/user/zvirb)

### License/Terms of Use:

MIT-0

## Use Case:

Agents use this skill to create events in the Google Calendar account available through the gog CLI after the calendar, title, and time bounds are confirmed.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The agent may create an event in the wrong calendar or with incorrect event details.

Mitigation: Confirm the calendar, title, start time, end time, and other event details before allowing the gog command to run.

## Reference(s):


## Skill Output:

**Output Type(s):** [shell commands, json, guidance]

**Output Format:** [CLI command arguments and JSON event confirmation]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires the gog CLI and access to the target Google Calendar account.]

## Skill Version(s):

1.0.4 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

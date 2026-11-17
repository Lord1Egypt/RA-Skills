## Description:

Atomic node skill to update a Google Calendar event using the gog CLI.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zvirb](https://clawhub.ai/user/zvirb)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill when an existing Google Calendar event needs to be modified or rescheduled through the gog CLI.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Calendar updates can modify the wrong event or calendar if identifiers, titles, or times are incorrect.

Mitigation: Review the target calendar, event ID, summary, and time range before executing the update.

Risk: Untrusted event text interpolated into shell commands can create command-safety issues.

Mitigation: Pass arguments safely and avoid constructing shell commands from untrusted text.

## Reference(s):


## Skill Output:

**Output Type(s):** [Shell commands, JSON]

**Output Format:** [JSON confirmation from the gog CLI]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires the gog binary and authenticated Google Calendar access.]

## Skill Version(s):

1.0.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

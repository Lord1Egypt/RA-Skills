## Description:

Controls local device volume and brightness and opens or closes allowed applications on explicit user request.

This skill is ready for commercial/non-commercial use.

## Publisher:

[iyeque](https://clawhub.ai/user/iyeque)

### License/Terms of Use:

MIT-0

## Use Case:

People using an agent to manage their desktop can request volume or brightness adjustments or open and close supported applications.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Closing an application can terminate all matching processes and discard unsaved work, particularly when forced on Windows.

Mitigation: Confirm the requested application and save work before closing it.

## Reference(s):

- [Device Control on ClawHub](https://clawhub.ai/iyeque/skills/iyeque-device-control)

## Skill Output:

**Output Type(s):** [Text, Shell commands]

**Output Format:** [Plain text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May change local device settings or application state when explicitly requested.]

## Skill Version(s):

1.3.1 (source: server-resolved release and skill metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

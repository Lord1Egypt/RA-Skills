## Description:

This skill should be used when the user asks about their Kia vehicle through the Kia Access / Kia Owners account. Triggers on phrases like "is the car locked", "unlock the Kia", "start the car's climate", "warm up the car", "where is my car", "what's the EV charge at", "check the car's battery", "lock the doors", or any request to read or command a Kia vehicle.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chrischall](https://clawhub.ai/user/chrischall)

### License/Terms of Use:

MIT-0

## Use Case:

Kia vehicle owners use the skill to check vehicle status, location, and EV charge information, or to request climate, charging, and door commands through their Kia account. Vehicle commands require user confirmation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Vehicle commands can change a real vehicle's state, including unlocking its doors.

Mitigation: Use read-only mode unless commands are needed, require user approval before every command, and verify the vehicle state before reporting success.

Risk: Kia account credentials and a persistent session token grant access to the vehicle account.

Mitigation: Keep credentials and tokens in protected configuration, never expose them in conversation or commit them to a repository.

Risk: The external server version may change, and the executable was unavailable for verification in the security review.

Mitigation: Pin and review the external server version before connecting a real vehicle.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/chrischall/skills/kiaaccess)
- [kiaaccess-mcp package page (linked in skill documentation)](https://www.npmjs.com/package/kiaaccess-mcp)

## Skill Output:

**Output Type(s):** [API Calls, Vehicle status and location, Vehicle control results]

**Output Format:** [Text responses with vehicle status, location links, and command results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Vehicle status may be cached; command acceptance does not by itself confirm the vehicle changed state.]

## Skill Version(s):

2.1.0 (source: ClawHub server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

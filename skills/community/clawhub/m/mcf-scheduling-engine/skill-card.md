## Description:

AI-powered appointment scheduling with staff management, availability windows, and booking automation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cameron48](https://clawhub.ai/user/cameron48)

### License/Terms of Use:

MIT-0

## Use Case:

External and internal agents use this skill to book appointments, check staff availability, manage staff profiles, and coordinate scheduling workflows for sales, service, and operations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Scheduling requests can include attendee details, appointment notes, and calendar timing information.

Mitigation: Minimize sensitive notes and share only the attendee and scheduling details needed for the booking.

Risk: Agents may book, reschedule, or otherwise change important appointments.

Mitigation: Require user approval before booking or rescheduling important appointments and notify affected attendees when changes are made.

Risk: Endpoint calls use a third-party paid gateway.

Mitigation: Install only when the user is comfortable sending scheduling details to the listed gateway and paying via the documented x402 flow.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/cameron48/skills/mcf-scheduling-engine)
- [MCF Agentic scheduling gateway](https://gateway.mcfagentic.com)
- [Publisher profile](https://clawhub.ai/user/cameron48)

## Skill Output:

**Output Type(s):** [API calls, JSON, guidance]

**Output Format:** [Markdown instructions with JSON request and response examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Endpoint calls require x402 payment using USDC on Base.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

## Description:

Schedule a call to the user's own app or any API, and read whether it was delivered, through GreatWait's MCP server, HTTP API or command line.

This skill is ready for commercial/non-commercial use.

## Publisher:

[plasticlizard](https://clawhub.ai/user/plasticlizard)

### License/Terms of Use:

MIT No Attribution (MIT-0)

## Use Case:

Users and developers use GreatWait to schedule one-time or recurring calls to an authorized application or API and check the resulting delivery status.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A callback may be delivered more than once.

Mitigation: Design the receiving endpoint to handle duplicate deliveries safely.

Risk: Recurring callbacks may continue, and cancellation cannot undo completed actions.

Mitigation: Review the schedule and destination before creation; verify cancellation state and treat completed callbacks as irreversible.

Risk: A schedule sends data to its configured callback destination.

Mitigation: Use only user-approved destinations and narrowly scoped credentials; review recurring schedules.

## Reference(s):

- [GreatWait HTTP calls guide](https://docs.greatwait.dev/guides/http-calls)
- [GreatWait API reference](https://docs.greatwait.dev/openapi.json)
- [GreatWait documentation index](https://docs.greatwait.dev/llms.txt)

## Skill Output:

**Output Type(s):** [Guidance, API calls, Text]

**Output Format:** [Natural-language scheduling guidance and delivery-status reports, with structured API requests when needed]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports observed delivery evidence and unresolved outcomes without claiming downstream actions completed]

## Skill Version(s):

1.0.0 (source: release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

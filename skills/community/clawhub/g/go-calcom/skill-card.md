## Description:

Writes Go code with go-calcom (package calcom, github.com/psyb0t/go-calcom), an unofficial client for Cal.com API v2 generated with oapi-codegen from the public OpenAPI document, with typed methods for bookings, event types, available slots, schedules, calendars, teams, webhooks and profile. Use when Go code needs Cal.com scheduling operations or already imports go-calcom.

This skill is ready for commercial/non-commercial use.

## Publisher:

[psyb0t](https://clawhub.ai/user/psyb0t)

### License/Terms of Use:

MIT-0

## Use Case:

Developers use this skill to write Go code that connects to Cal.com API v2 for availability, booking, event type, schedule, calendar, team, webhook, and profile operations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Using the client requires a Cal.com API key and sends authenticated scheduling requests to the configured Cal.com API endpoint.

Mitigation: Keep CALCOM_API_KEY out of source code, commits, and logs, and use the documented Cal.com host or an explicitly configured deployment.

Risk: Booking and scheduling management methods can change account data, including creating, rescheduling, or cancelling bookings and editing schedules, event types, teams, or webhooks.

Mitigation: Use mutating operations only when requested and only for the intended resources.

Risk: The security scan was partial because two local references could not be resolved.

Mitigation: Review the referenced setup material and scan findings before installation.

## Reference(s):

- [Setup and reference](references/setup.md)
- [Go module documentation](https://pkg.go.dev/github.com/psyb0t/go-calcom)
- [Cal.com API v2 introduction](https://cal.com/docs/api-reference/v2/introduction)
- [Cal.com profile API reference](https://cal.com/docs/api-reference/v2/me/get-my-profile)
- [Cal.com API v2 OpenAPI specification](https://raw.githubusercontent.com/calcom/cal.com/main/docs/api-reference/v2/openapi.json)

## Skill Output:

**Output Type(s):** [Code, Shell commands, Guidance]

**Output Format:** [Go code and Markdown guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Examples and instructions cover authenticated Cal.com API calls, including operations that can change account data.]

## Skill Version(s):

0.1.4 (source: server-resolved ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

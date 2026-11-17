## Description:

Writes Go code with go-calcom (package calcom, github.com/psyb0t/go-calcom), an unofficial client for Cal.com API v2 generated with oapi-codegen from the public OpenAPI document, with typed methods for bookings, event types, available slots, schedules, calendars, teams, webhooks and profile. Use when Go code needs Cal.com scheduling operations or already imports go-calcom.

This skill is ready for commercial/non-commercial use.

## Publisher:

[psyb0t](https://clawhub.ai/user/psyb0t)

### License/Terms of Use:

MIT-0

## Use Case:

Developers use this skill to write Go code that connects to Cal.com API v2 for availability, bookings, profiles, schedules, event types, calendars, teams, and webhooks. It supports read operations and account changes when the user requests them.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A Cal.com API credential could be exposed through source code or logs.

Mitigation: Use a credential with only the required access, read it from CALCOM_API_KEY, and keep credentials and request headers out of source code and logs.

Risk: Booking or configuration operations can change Cal.com account data.

Mitigation: Perform account changes only when requested and only for the intended resources.

Risk: Adding an outdated or unsuitable dependency version could affect the project.

Mitigation: Review the go-calcom dependency version before adding it.

## Reference(s):

- [Setup and API usage reference](artifact/references/setup.md)
- [go-calcom package documentation](https://pkg.go.dev/github.com/psyb0t/go-calcom)
- [Cal.com API v2 introduction](https://cal.com/docs/api-reference/v2/introduction)
- [Cal.com profile endpoint](https://cal.com/docs/api-reference/v2/me/get-my-profile)

## Skill Output:

**Output Type(s):** [Code, Shell commands, Configuration instructions, Guidance]

**Output Format:** [Go code with concise Markdown guidance and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Go code targets the go-calcom package and may include Cal.com API request setup.]

## Skill Version(s):

0.1.3 (source: server-resolved release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

## Description:

Unofficial Go client for the HubSpot API. `hubspot.NewClientWithResponses("https://api.hubapi.com", ...)` from `github.com/psyb0t/go-hubspot` gives a typed method for every path in HubSpot's 2026-03 OpenAPI documents, including CRM objects such as contacts and companies, single-deal reads and updates, associations, properties, search, marketing, CMS, automation, conversations, files and webhooks. Auth is a Bearer private app or OAuth access token set through a request editor. Responses decode into typed `JSON200`/`JSON201` fields. Use when Go code needs to read or write HubSpot data, or already imports go-hubspot.

This skill is ready for commercial/non-commercial use.

## Publisher:

[psyb0t](https://clawhub.ai/user/psyb0t)

### License/Terms of Use:

MIT

## Use Case:

Developers use this skill to add typed Go calls for reading and writing HubSpot data, including CRM records and related API resources. It provides setup, authentication, endpoint lookup, and response handling guidance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Create, update, merge, archive, delete, and GDPR purge calls can change a live HubSpot account.

Mitigation: Use these operations only when requested, confirm the required permissions and records, and review the affected records before proceeding.

Risk: A HubSpot access token can expose account data or authorize changes if it is disclosed.

Mitigation: Read tokens from environment variables; do not hardcode, commit, log, or print request headers containing credentials.

## Reference(s):

- [Setup and reference](references/setup.md)
- [go-hubspot package documentation](https://pkg.go.dev/github.com/psyb0t/go-hubspot)
- [go-hubspot source repository](https://github.com/psyb0t/go-hubspot)

## Skill Output:

**Output Type(s):** [Code, Shell commands, Configuration instructions, Guidance]

**Output Format:** [Markdown with Go and shell code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Examples and instructions for configuring and calling the typed Go client.]

## Skill Version(s):

0.5.6 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

## Description:

Unofficial Go client for the PostGrid print and mail and address verification APIs. Package postgrid (github.com/psyb0t/go-postgrid), generated with oapi-codegen, has typed methods for contacts, templates, letters, postcards, cheques, self mailers, campaigns, mailing lists, reports, webhooks and address verification, authenticated with an API key in the X-API-Key header. Use when Go code needs to send physical mail, manage PostGrid print and mail resources or verify addresses, or already imports go-postgrid.

This skill is ready for commercial/non-commercial use.

## Publisher:

[psyb0t](https://clawhub.ai/user/psyb0t)

### License/Terms of Use:

MIT

## Use Case:

Go developers use this skill to integrate the unofficial go-postgrid package into a project, call PostGrid print and mail or address verification operations, and handle authentication and parsed responses.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Using a live PostGrid key to create mail can send physical mail and incur charges; bulk verification and targeted list builds may also be billable.

Mitigation: Use test credentials during development, get explicit user authorization before creating or changing resources, and check whether a request succeeded before retrying after an uncertain response.

## Reference(s):

- [Setup and reference](artifact/references/setup.md)
- [Go package documentation](https://pkg.go.dev/github.com/psyb0t/go-postgrid)
- [PostGrid OpenAPI specification](https://guides.postgrid.com/api/openapi.yaml)
- [Declared skill homepage](https://github.com/psyb0t/go-postgrid)

## Skill Output:

**Output Type(s):** [Code, Shell commands, Configuration instructions, Guidance]

**Output Format:** [Markdown with Go code blocks and shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Examples are tailored to the Go project and requested PostGrid operation; API keys should be supplied through environment configuration rather than source code.]

## Skill Version(s):

0.3.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

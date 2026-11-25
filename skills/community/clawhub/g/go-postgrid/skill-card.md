## Description:

Unofficial Go client for the PostGrid print and mail and address verification APIs. Package postgrid (github.com/psyb0t/go-postgrid), generated with oapi-codegen, has typed methods for contacts, templates, letters, postcards, cheques, self mailers, campaigns, mailing lists, reports, webhooks and address verification, authenticated with an API key in the X-API-Key header. Use when Go code needs to send physical mail, manage PostGrid print and mail resources or verify addresses, or already imports go-postgrid.

This skill is ready for commercial/non-commercial use.

## Publisher:

[psyb0t](https://clawhub.ai/user/psyb0t)

### License/Terms of Use:

MIT

## Use Case:

Developers use this skill when building Go applications that integrate with PostGrid print and mail resources or address verification APIs. It guides them in installing and using the unofficial typed client, including authentication and response handling.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Using a live print-and-mail key can send physical mail and incur charges.

Mitigation: Use a test key during development; create or send mail only when explicitly requested, and check whether an uncertain request succeeded before retrying.

Risk: Exposing the PostGrid API key could compromise the account.

Mitigation: Read POSTGRID_API_KEY from the environment and never hardcode, commit, or log the key.

## Reference(s):

- [setup.md](references/setup.md)
- [go-postgrid project homepage](https://github.com/psyb0t/go-postgrid)
- [go-postgrid package documentation](https://pkg.go.dev/github.com/psyb0t/go-postgrid)
- [PostGrid OpenAPI document](https://guides.postgrid.com/api/openapi.yaml)

## Skill Output:

**Output Type(s):** [Code, Shell commands, Configuration instructions, Guidance]

**Output Format:** [Go code and Markdown guidance with shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [None]

## Skill Version(s):

0.3.1 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

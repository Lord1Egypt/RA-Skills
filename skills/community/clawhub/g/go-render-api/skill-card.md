## Description:

Guides Go developers in using the unofficial go-render-api client to call Render's REST API, including authentication, pagination, typed endpoint operations, and response handling.

This skill is ready for commercial/non-commercial use.

## Publisher:

[psyb0t](https://clawhub.ai/user/psyb0t)

### License/Terms of Use:

MIT

## Use Case:

Developers use this skill to write Go code that calls Render's REST API to inspect or manage services and other Render resources. It is also useful when a Go project already uses the go-render-api package.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Deploy, suspend, scale, update, and delete operations can change live infrastructure.

Mitigation: Use these operations only for services the user named and actions the user requested.

Risk: A Render API key can authorize account actions.

Mitigation: Read the key from an environment variable; never hardcode, commit, or log it, and never print request headers.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/psyb0t/skills/go-render-api)
- [go-render-api repository](https://github.com/psyb0t/go-render-api)
- [Package documentation](https://pkg.go.dev/github.com/psyb0t/go-render-api)
- [Render API pagination documentation](https://api-docs.render.com/reference/pagination)
- [Setup and reference](artifact/references/setup.md)

## Skill Output:

**Output Type(s):** [Code, API Calls, Shell commands, Configuration instructions, Guidance]

**Output Format:** [Go code examples and API usage guidance in Markdown, with shell commands where useful]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include operations that change live Render infrastructure; follow the user's explicit scope for such actions.]

## Skill Version(s):

0.11.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

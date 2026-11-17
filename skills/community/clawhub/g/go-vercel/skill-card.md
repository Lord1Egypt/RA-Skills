## Description:

Unofficial Go client for the Vercel REST API, generated with oapi-codegen from Vercel's OpenAPI spec. Package `vercel` from `github.com/psyb0t/go-vercel` gives `NewClientWithResponses` a typed `...WithResponse` method for every endpoint in the spec (projects, deployments, domains, DNS, env vars, teams and more), with typed params structs, `JSON200` response bodies and `As...` methods for oneOf unions. Auth is a bearer token added by a `RequestEditorFn`, with an optional `teamId` query parameter. Use when Go code needs to call the Vercel API, or the project already imports go-vercel.

This skill is ready for commercial/non-commercial use.

## Publisher:

[psyb0t](https://clawhub.ai/user/psyb0t)

### License/Terms of Use:

MIT-0

## Use Case:

Developers use this skill to write Go applications that call Vercel's REST API for account, project, deployment, domain, DNS, environment-variable, and team operations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A Vercel access token can authorize account or team operations, and some endpoints can change or delete live resources.

Mitigation: Review the setup guidance before providing a token, keep it in an environment variable, never hard-code or log it, and call mutating operations only for the requested resources.

## Reference(s):

- [Setup and reference](references/setup.md)
- [Project homepage](https://github.com/psyb0t/go-vercel)
- [Go package documentation](https://pkg.go.dev/github.com/psyb0t/go-vercel)

## Skill Output:

**Output Type(s):** [Code, Shell commands, Configuration instructions, Guidance]

**Output Format:** [Markdown with Go code and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [None]

## Skill Version(s):

0.29.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

## Description:

Writes Go code with go-browser-use (package browseruse, github.com/psyb0t/go-browser-use), an unofficial generated client for the Browser Use Cloud API v4. Use when a Go program creates or polls Browser Use agent runs, manages sessions, queues, workspaces, files, browsers, profiles, extensions or integrations, or when a project imports github.com/psyb0t/go-browser-use.

This skill is ready for commercial/non-commercial use.

## Publisher:

[psyb0t](https://clawhub.ai/user/psyb0t)

### License/Terms of Use:

MIT-0

## Use Case:

Developers use this skill to write Go integrations with the unofficial Browser Use Cloud API v4 client. It helps them create and poll runs and work with sessions, queues, workspaces, files, browsers, profiles, extensions, and integrations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Starting runs or browsers can incur charges, and cancellation, deletion, purging, sharing, uploads, and integration changes affect account state.

Mitigation: Perform billable or account-changing actions only when the user requested them; use an appropriate cost limit for runs.

Risk: Credentials, task contents, secret bindings, CDP URLs, or presigned URLs could be exposed through logs or mishandled requests.

Mitigation: Load the API key from the caller's environment or secret store, never log sensitive values, and use a separate client for presigned file transfers so the API key is not forwarded to storage.

Risk: The security scan was partial and could not resolve two local references, and use depends on trust in the Browser Use service.

Mitigation: Review the unresolved references and confirm the service and account actions are appropriate before relying on the integration.

## Reference(s):

- [Setup and API reference](references/setup.md)
- [go-browser-use project](https://github.com/psyb0t/go-browser-use)
- [go-browser-use Go package documentation](https://pkg.go.dev/github.com/psyb0t/go-browser-use)

## Skill Output:

**Output Type(s):** [Code, Configuration instructions, Guidance]

**Output Format:** [Go code and Markdown guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Examples and integration guidance for the Browser Use Cloud API v4 Go client.]

## Skill Version(s):

0.2.3 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

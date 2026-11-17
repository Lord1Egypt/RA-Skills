## Description:

Unofficial Go client for the Intercom REST API, generated with oapi-codegen. Package `intercom` (`github.com/psyb0t/go-intercom`) provides typed methods for admins, contacts, companies, conversations, messages, articles, tickets, tags, teams and exports. Use when Go code needs Intercom customer support or workspace data, must perform a requested Intercom action, or already imports go-intercom.

This skill is ready for commercial/non-commercial use.

## Publisher:

[psyb0t](https://clawhub.ai/user/psyb0t)

### License/Terms of Use:

MIT-0

## Use Case:

Developers use this Go package to integrate Intercom workspace and customer support data into Go applications, including requested reads, messages, and updates.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The client sends an Intercom bearer token with requests and can create, update, or delete workspace data.

Mitigation: Read the token from INTERCOM_ACCESS_TOKEN, keep it out of logs and source control, use the workspace's regional HTTPS API host, and perform writes or deletes only when requested.

Risk: The supplied security assessment is partial, so it may not cover all behavior.

Mitigation: Review the skill and the granted token scopes before use, and confirm that each requested API operation is appropriate for the workspace.

## Reference(s):

- [Setup and API usage](references/setup.md)
- [Project homepage](https://github.com/psyb0t/go-intercom)
- [Go package documentation](https://pkg.go.dev/github.com/psyb0t/go-intercom)

## Skill Output:

**Output Type(s):** [Code, Shell commands, Configuration instructions, Guidance]

**Output Format:** [Markdown guidance with Go code and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Examples use the Go client; resulting API requests can read or change Intercom workspace data.]

## Skill Version(s):

0.10.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

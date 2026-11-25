## Description:

An unofficial typed Go client for the Zulip REST API, for reading and sending messages, managing users and channels, polling events, uploading files, and administering an organization.

This skill is ready for commercial/non-commercial use.

## Publisher:

[psyb0t](https://clawhub.ai/user/psyb0t)

### License/Terms of Use:

MIT

## Use Case:

Developers use this skill in Go projects that need to read or send Zulip messages, manage users and channels, or administer an organization through its Zulip server.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The benign security scan is not a safety guarantee, and one referenced item could not be resolved.

Mitigation: Review the unresolved reference before relying on it.

Risk: Requests send credentials and content to the configured Zulip server, and message or organization changes can have real effects.

Mitigation: Use a trusted HTTPS server, keep credentials out of code and logs, and make changes only when requested.

## Reference(s):

- [Setup and reference](references/setup.md)
- [Go package documentation](https://pkg.go.dev/github.com/psyb0t/go-zulip)
- [Project homepage](https://github.com/psyb0t/go-zulip)

## Skill Output:

**Output Type(s):** [Code, API Calls, Shell commands, Configuration instructions, Guidance]

**Output Format:** [Go code and Markdown guidance with inline Go and shell examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Usage examples and configuration guidance; runtime API calls use the configured Zulip server.]

## Skill Version(s):

0.5.0 (source: server-resolved release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

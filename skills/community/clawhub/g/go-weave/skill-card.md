## Description:

Provides a typed Go client for recording and querying traces and related resources through the W&B Weave API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[psyb0t](https://clawhub.ai/user/psyb0t)

### License/Terms of Use:

MIT

## Use Case:

Developers use this skill to add Go code that records, queries, and manages traces and related resources in a W&B Weave trace server.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Weave credentials could be exposed if they are hardcoded, committed, or logged.

Mitigation: Read the username and API key from environment variables, and keep credentials out of source control, logs, and printed request headers.

Risk: Trace inputs and outputs are sent to the configured trace server, which may contain sensitive data.

Mitigation: Review the data being sent and confirm the configured server is the intended W&B, dedicated, or self-hosted endpoint.

Risk: Delete and purge methods can remove project data.

Mitigation: Use these methods only for data created by the task or specifically named by the user, and only when requested.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/psyb0t/skills/go-weave)
- [Project repository](https://github.com/psyb0t/go-weave)
- [Go package documentation](https://pkg.go.dev/github.com/psyb0t/go-weave)
- [Setup and reference](references/setup.md)

## Skill Output:

**Output Type(s):** [Code, Shell commands, Configuration instructions, Guidance]

**Output Format:** [Go code and Markdown guidance with shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [None]

## Skill Version(s):

0.3.4 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

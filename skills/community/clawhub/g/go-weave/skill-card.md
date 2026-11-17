## Description:

Unofficial Go client for the W&B Weave trace server API, generated with oapi-codegen. `weave.NewClientWithResponses(baseURL, auth)` from `github.com/psyb0t/go-weave` gives typed methods for every endpoint of the Weave trace server, with HTTP Basic authentication set in a request editor.

This skill is ready for commercial/non-commercial use.

## Publisher:

[psyb0t](https://clawhub.ai/user/psyb0t)

### License/Terms of Use:

MIT-0

## Use Case:

Developers use this skill to add the go-weave client to Go projects and to record, query, and manage W&B Weave traces and related resources. It provides setup guidance, endpoint references, and Go usage examples.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Trace inputs and outputs sent through the client may contain sensitive data and are uploaded to the configured trace server.

Mitigation: Verify the destination server and ensure trace inputs and outputs are appropriate to upload; use a dedicated or self-hosted W&B instance when needed.

Risk: Delete and purge endpoints can remove project data.

Mitigation: Use these endpoints only for data created by the task or specifically named by the user, and only when the user asked for deletion.

Risk: The external Go dependency and publisher provenance have not been independently verified.

Mitigation: Pin and review the Go dependency before use.

## Reference(s):

- [Setup and endpoint reference](references/setup.md)
- [Go package documentation](https://pkg.go.dev/github.com/psyb0t/go-weave)
- [Project homepage (declared in skill metadata)](https://github.com/psyb0t/go-weave)

## Skill Output:

**Output Type(s):** [Code, Shell commands, Configuration instructions, Guidance]

**Output Format:** [Markdown guidance with Go code and inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include credential setup and trace server configuration instructions.]

## Skill Version(s):

0.3.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

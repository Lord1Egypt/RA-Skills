## Description:

Provides an unofficial typed Go client for calling Klavis AI APIs, including MCP server and tool operations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[psyb0t](https://clawhub.ai/user/psyb0t)

### License/Terms of Use:

MIT

## Use Case:

Go developers use this skill to integrate Klavis AI APIs into an application, including discovering MCP servers, calling tools, and managing related instances and integrations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The external Go dependency's implementation is outside this skill's inspection.

Mitigation: Review and pin the dependency version before use.

Risk: API operations can affect remote Klavis and MCP resources.

Mitigation: Authorize remote changes deliberately, choose read-only instances when suitable, and verify server URLs and tool arguments before sending credentials.

## Reference(s):

- [Setup and API reference](references/setup.md)
- [Project homepage](https://github.com/psyb0t/go-klavis)
- [Go package documentation](https://pkg.go.dev/github.com/psyb0t/go-klavis)

## Skill Output:

**Output Type(s):** [Code, Shell commands, Configuration instructions, Guidance]

**Output Format:** [Markdown with Go code examples, shell commands, and endpoint tables]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes authentication setup, endpoint references, and typed Go response handling.]

## Skill Version(s):

0.2.5 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

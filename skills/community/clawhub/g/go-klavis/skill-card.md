## Description:

Guides Go developers in using an unofficial typed client for Klavis AI's API, including MCP servers and tools, instances, Strata, user integrations, OAuth, sandboxes, and universes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[psyb0t](https://clawhub.ai/user/psyb0t)

### License/Terms of Use:

MIT-0

## Use Case:

Go developers use this skill to add and call the Klavis AI API client, select the account's US or EU endpoint, configure bearer authentication, and handle typed requests and responses.

### Deployment Geography for Use:

Global; choose the US or EU endpoint for the account's region.

## Known Risks and Mitigations:

Risk: The security review is benign with medium confidence, and two local references could not be resolved.

Mitigation: Review the unresolved references and confirm the skill fits the intended MCP and Klavis use case before relying on it.

Risk: API requests may include Klavis credentials, and some tool or instance operations can change remote services.

Mitigation: Load the API key from KLAVIS_API_KEY, use the account's regional host, verify MCP server URLs and tool arguments, and make remote changes only when requested.

## Reference(s):

- [Setup and reference](references/setup.md)
- [go-klavis source repository](https://github.com/psyb0t/go-klavis)
- [go-klavis Go package documentation](https://pkg.go.dev/github.com/psyb0t/go-klavis)

## Skill Output:

**Output Type(s):** [Code, Shell commands, Configuration instructions, Guidance]

**Output Format:** [Markdown with Go code and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [None]

## Skill Version(s):

0.3.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

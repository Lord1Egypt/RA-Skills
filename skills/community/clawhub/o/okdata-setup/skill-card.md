## Description:

Helps configure the okdata API or MCP connection, manage its API key, check prices and balance, and troubleshoot common errors.

This skill is ready for commercial/non-commercial use.

## Publisher:

[conn-ho](https://clawhub.ai/user/conn-ho)

### License/Terms of Use:

MIT

## Use Case:

Developers and agents use this skill to connect to okdata for public data across social and commerce platforms, manage credentials, and check costs or service status. It provides setup and troubleshooting guidance for MCP, HTTP, SDK, and command-line access.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The scan rates the skill suspicious with medium confidence because unpinned package commands may run changing code with the user's account privileges.

Mitigation: Avoid installation until package versions and commands have been reviewed, and verify the API destination and credential handling. The available scan is incomplete.

Risk: An okdata API key could be exposed if placed in project files, URLs, chat, or logs.

Mitigation: Keep the key in a protected environment variable or client secret store; do not commit, echo, log, or repeat it.

Risk: Calls that reach a data source can incur charges even when they return empty results or errors, and retrying creates another call.

Mitigation: Check endpoint prices and set a maximum price before calling; avoid repeated retries for empty, not-found, or source-failure responses.

## Reference(s):

- [okdata documentation for agents](https://okdata.online/agents.md)
- [okdata MCP endpoint](https://api.okdata.online/mcp)
- [okdata pricing](https://okdata.online/prices.json)
- [okdata service status](https://api.okdata.online/v1/catalog/status)
- [okdata account signup](https://okdata.online/signup/?src=skill-okdata-setup)

## Skill Output:

**Output Type(s):** [Configuration instructions, Shell commands, API calls, Guidance]

**Output Format:** [Markdown with shell commands and JSON or TOML configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [API calls can incur per-request charges; the skill describes price checks and spending limits.]

## Skill Version(s):

0.1.2 (source: server-resolved release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

## Description:

Use when scraping or automating pages with obscura.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bevisy](https://clawhub.ai/user/bevisy)

### License/Terms of Use:

MIT

## Use Case:

Developers and agents use this skill to choose and operate obscura's fetch, scrape, MCP, and CDP interfaces for web page scraping and browser automation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The HTTP MCP example may expose browser-control traffic over plaintext if the endpoint is reachable beyond the local machine.

Mitigation: Prefer stdio or bind HTTP to a trusted interface, set an MCP token, and protect remote access with TLS.

Risk: Persistent browser profiles contain live cookies and session tokens.

Mitigation: Use a separate storage directory for each identity and protect it as a credential store.

## Reference(s):

- [CLI reference](references/cli.md)
- [MCP tools reference](references/mcp-tools.md)
- [Upstream documentation index](references/upstream-docs.md)
- [Obscura upstream repository](https://github.com/h4ckf0r0day/obscura)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Shell commands, Code, Configuration instructions]

**Output Format:** [Markdown with shell commands, JavaScript snippets, and configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Examples and commands target obscura 0.2.6 and may need adjustment for other versions or environments.]

## Skill Version(s):

1.0.0 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

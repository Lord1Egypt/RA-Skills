## Description:

Has an MCP server you use changed its tools? Check any public server against a nightly crawl and see exactly what changed. Read-only, free, no key. By getvda.ai's MCP Drift Observatory.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mikerawsonnz](https://clawhub.ai/user/mikerawsonnz)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and MCP users use this skill to check whether a public MCP server's declared tools have changed and inspect recorded differences, helping them spot changes that could affect agent prompts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Checking a server tells the external service which server is being checked, and a URL containing a key or token could disclose that credential.

Mitigation: Get the owner's approval and send only the server's public endpoint URL with keys and tokens removed.

Risk: A report about declared tools and their changes does not establish whether a server is safe or reveal implementation changes that leave declarations unchanged.

Mitigation: Use the report to review declaration changes, and assess server behavior and security separately; treat an unobserved server as unknown rather than unchanged.

## Reference(s):

- [MCP Drift Observatory](https://github.com/mikerawsonnz/mcp-drift-observatory)
- [MCP Drift Check on ClawHub](https://clawhub.ai/mikerawsonnz/skills/mcp-drift-check)

## Skill Output:

**Output Type(s):** [Analysis, Guidance, Text]

**Output Format:** [Plain-language summary of server status and recorded tool declaration changes]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [None]

## Skill Version(s):

1.0.0 (source: frontmatter, server-resolved release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

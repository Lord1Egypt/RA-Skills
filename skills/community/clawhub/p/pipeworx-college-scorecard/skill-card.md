## Description:

Search US colleges by name and retrieve details such as tuition and admission rates using a College Scorecard MCP server.

This skill is ready for commercial/non-commercial use.

## Publisher:

[b-gutman](https://clawhub.ai/user/b-gutman)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to configure a College Scorecard MCP server for searching US colleges and retrieving school details such as tuition, location, and admission rates.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: College lookup requests are routed to an unverified third-party domain.

Mitigation: Install only if that routing is acceptable and avoid sending personal, credential, or unrelated conversation data through the MCP server.

Risk: Tuition and admissions results may be incorrect or presented as more authoritative than the service warrants.

Mitigation: Verify important college data against an authoritative source before relying on it.

## Reference(s):

- [Pipeworx College Scorecard Skill Page](https://clawhub.ai/b-gutman/skills/pipeworx-college-scorecard)
- [College Scorecard MCP Endpoint](https://gateway.pipeworx.io/college-scorecard/mcp)

## Skill Output:

**Output Type(s):** [Text, Markdown, Configuration, Guidance]

**Output Format:** [Markdown with a JSON MCP server configuration block]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Routes college lookup requests through gateway.pipeworx.io.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

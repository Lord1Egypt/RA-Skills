## Description:

Search and read Investoday financial market data through an OOMOL-connected account.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and analysts use the skill to search and retrieve Investoday data about securities, funds, markets, and research through their connected account.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Setup instructions can run a downloaded installer before its source is independently verified.

Mitigation: Verify the oo CLI installation independently and require approval before running any downloaded installer.

Risk: Queries pass through OOMOL using the connected Investoday account.

Mitigation: Use an account authorized for these queries and review the information sent before running an action.

## Reference(s):

- [Investoday MCP homepage](https://data-api.investoday.net/mcp)
- [Investoday API documentation](https://std.investoday.net/apidocs/api-overview)
- [oo CLI installation guide](https://cli.oomol.com/install-guide.md)

## Skill Output:

**Output Type(s):** [Shell commands, JSON, Guidance]

**Output Format:** [Markdown instructions with inline shell commands; Investoday query results are returned as JSON.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [None]

## Skill Version(s):

1.0.3 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

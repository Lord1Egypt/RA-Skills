## Description:

Simple currency exchange rates for retrieving all rates for a base currency or a direct pair lookup via open.er-api.com.

This skill is ready for commercial/non-commercial use.

## Publisher:

[b-gutman](https://clawhub.ai/user/b-gutman)

### License/Terms of Use:

MIT-0

## Use Case:

External users, developers, and agents use this skill to check current exchange rates for a base currency or retrieve a direct currency pair rate.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The MCP setup command automatically downloads and runs an unpinned npm package on the user's machine.

Mitigation: Pin mcp-remote to a reviewed exact version, avoid automatic -y installation when possible, and run the MCP process with minimal filesystem and credential access.

Risk: Exchange-rate results may be unsuitable for decisions that require guaranteed real-time or audited market data.

Mitigation: Confirm rates against an authoritative financial data source before using them for regulated, contractual, or high-value financial decisions.

## Reference(s):

- [Pipeworx ExchangeRate pack](https://pipeworx.io/packs/exchangerate)
- [ClawHub skill page](https://clawhub.ai/b-gutman/skills/pipeworx-exchangerate)
- [MCP endpoint](https://gateway.pipeworx.io/exchangerate/mcp)

## Skill Output:

**Output Type(s):** [text, JSON, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline JSON and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Returns current exchange-rate data from open.er-api.com through the Pipeworx exchangerate MCP service.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

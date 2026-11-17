## Description:

Fetch real estate listings from Paragon MLS (paragonrels.com / fnimls.com) APIs and perform four-square rental property analysis.

This skill is ready for commercial/non-commercial use.

## Publisher:

[earlvanze](https://clawhub.ai/user/earlvanze)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, agents, and real estate analysts use this skill to retrieve public Paragon MLS listing data, inspect structured property details, and analyze rental investment scenarios including cash flow, cash-on-cash return, DSCR, ROI, ROE, IRR, and velocity banking comparisons.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill depends on a separate Node MCP server outside the bundled artifact, so the executable code may differ from the reviewed skill files.

Mitigation: Inspect and trust the referenced paragon-mls-mcp source before installation, and prefer a packaged release that bundles the server source.

Risk: The setup is not reproducible because dependencies are installed at build time without a bundled lockfile.

Mitigation: Pin and verify dependencies before deployment.

Risk: Some MLS regions may use plaintext HTTP for listing data, which can expose or allow tampering with queries and responses.

Mitigation: Block plaintext HTTP use where possible, or clearly confirm the risk before using affected regions.

## Reference(s):

- [ClawHub Paragon MLS skill page](https://clawhub.ai/earlvanze/skills/paragon-mls)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, API calls, analysis]

**Output Format:** [Markdown guidance with shell commands, configuration snippets, structured listing data, and investment analysis results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Node and a separately available Paragon MLS MCP server at the configured path.]

## Skill Version(s):

1.1.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

## Description:

Query hemnet.se (Swedish property portal) from a shell with the fpx CLI (@fetchproxy/cli) instead of running the hemnet-mcp server — resolve locations, search for-sale and sold listings, and read listing detail via one-shot GraphQL calls through a signed-in browser tab.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chrischall](https://clawhub.ai/user/chrischall)

### License/Terms of Use:

MIT-0

## Use Case:

Developers can query public Hemnet for-sale listings, sold listings, and listing details from shell scripts without running the hemnet-mcp server.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Using fpx requires pairing a browser extension with fetch access, and the installed CLI and extension versions were not audited in this assessment.

Mitigation: Approve only hemnet.se and fetch access, verify the extension release checksum, use a separate browser profile if needed, and revoke pairing when finished.

## Reference(s):

- [GraphQL query examples](references/graphql-queries.md)
- [Hemnet GraphQL endpoint](https://www.hemnet.se/graphql)
- [ContextMint Bridge releases](https://github.com/nullnet-app/contextmint-bridge/releases)
- [ContextMint Bridge source](https://github.com/nullnet-app/contextmint-bridge)

## Skill Output:

**Output Type(s):** [JSON, Text]

**Output Format:** [Hemnet GraphQL listing data as JSON, optionally filtered with jq]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Values include prices in SEK and areas in m².]

## Skill Version(s):

1.2.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

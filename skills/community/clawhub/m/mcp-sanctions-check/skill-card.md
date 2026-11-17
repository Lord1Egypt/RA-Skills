## Description:

Checks names against the OFAC SDN sanctions list through an MCP tool, using cached CSV downloads, token-based matching, optional country filtering, and structured JSON results.

This skill is ready for commercial/non-commercial use.

## Publisher:

[haveblue997](https://clawhub.ai/user/haveblue997)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this MCP server to screen customer, transaction, onboarding, KYC, international business, or booking names against OFAC SDN data before proceeding with regulated workflows. Results should be treated as a screening aid, not as a final compliance decision.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Unpinned npm execution and package identity mismatch create supply-chain ambiguity before installation.

Mitigation: Review the package source before installing and pin the exact npm version or run from a locked local install.

Risk: The sanctions data download and predictable temporary cache can affect compliance-integrity if the data source or cache is tampered with.

Mitigation: Treat results as a screening aid, verify consequential decisions through authoritative compliance processes, and control or monitor the SDN download and cache in deployment.

## Reference(s):

- [OFAC SDN CSV data source](https://www.treasury.gov/ofac/downloads/sdn.csv)
- [ClawHub skill page](https://clawhub.ai/haveblue997/skills/mcp-sanctions-check)

## Skill Output:

**Output Type(s):** [Text, JSON, Configuration]

**Output Format:** [MCP text content containing formatted JSON, with MCP server configuration snippets in the documentation]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The check_sanctions tool accepts a required name and optional country, then returns match status, matched entries, and a checked_at timestamp.]

## Skill Version(s):

1.0.0 (source: server release metadata, frontmatter, and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

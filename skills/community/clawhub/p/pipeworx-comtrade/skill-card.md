## Description:

Retrieve international bilateral trade data, top trading partners, top traded commodities, and country ISO numeric codes through a Comtrade MCP connector.

This skill is ready for commercial/non-commercial use.

## Publisher:

[b-gutman](https://clawhub.ai/user/b-gutman)

### License/Terms of Use:

MIT-0

## Use Case:

Analysts, researchers, and developers use this skill to query Comtrade-related trade data through an MCP gateway, including bilateral trade flows, partner rankings, commodity rankings, and numeric country code lookup.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Comtrade queries and responses pass through a third-party Pipeworx MCP gateway rather than an official UN endpoint.

Mitigation: Avoid sending confidential business research unless that dependency is acceptable, and verify decision-critical trade data against authoritative UN Comtrade sources.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/b-gutman/skills/pipeworx-comtrade)

## Skill Output:

**Output Type(s):** [text, configuration, API calls, guidance]

**Output Format:** [Markdown or plain text responses with MCP server configuration JSON when setup is needed]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Responses depend on the configured Pipeworx Comtrade MCP gateway and should be checked against authoritative sources for decision-critical use.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

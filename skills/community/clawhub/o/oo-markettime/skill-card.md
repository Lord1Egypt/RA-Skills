## Description:

Search and read MarketTime data through a connected OOMOL account.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

External users with an OOMOL-connected MarketTime account can search catalog items, list available manufacturers, and find orders. Developers can use the skill's action schemas and JSON payload guidance to make those read requests.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Setup may execute downloaded code without a separate approval step; the downloaded installers and hosted connector code were not verified.

Mitigation: Review setup, install a verified pinned oo CLI, review or disable automatic bundled-skill synchronization, and check the MarketTime permissions granted through OOMOL.

## Reference(s):

- [MarketTime](https://www.markettime.com/)
- [MarketTime API documentation](https://publicapi.markettime.com/swagger-ui/index.html#/)
- [oo CLI](https://github.com/oomol-lab/oo-cli)

## Skill Output:

**Output Type(s):** [API Calls, Shell commands, JSON, Guidance]

**Output Format:** [Shell commands with JSON payloads and JSON connector results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Read-only catalog, manufacturer, and order-search results; available filters and pagination depend on the action.]

## Skill Version(s):

1.0.5 (source: frontmatter, server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

## Description:

Queries real-time stock quotes, stock information, IPO events, stock splits, trades, market depth, and K-line data for major global markets using the itick.org API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chnmasterog](https://clawhub.ai/user/chnmasterog)

### License/Terms of Use:


## Use Case:

External users and developers use this skill to query iTick stock-market endpoints for current quotes, company information, IPOs, splits, trades, market depth, and K-line data across supported regions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The published documentation includes a credential-like API token in example commands.

Mitigation: Revoke or rotate that token if it was ever valid, replace literal examples with $ITICK_API_TOKEN, and avoid copying token values into chats, terminals, repositories, or logs.

Risk: The skill depends on an external market-data API and an API token.

Mitigation: Use only ClawHub-managed environment secrets, review API access permissions, and verify returned market data before relying on it.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/chnmasterog/skills/itick-stock-quote)
- [Publisher profile](https://clawhub.ai/user/chnmasterog)
- [iTick API endpoint host](https://api.itick.org)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with curl command examples and JSON response summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires ITICK_API_TOKEN as an environment-managed secret.]

## Skill Version(s):

1.0.0 (source: release metadata and claw.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

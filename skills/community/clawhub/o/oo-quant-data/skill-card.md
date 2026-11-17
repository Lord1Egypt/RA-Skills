## Description:

Search and read Quant Data market data through an OOMOL-connected account.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and analysts use this skill to search and retrieve Quant Data market information through a connected account, including equity prints, options flow, volatility, dealer exposure, and ticker-tagged news.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A missing oo CLI dependency can trigger an unverified remote installation, and installer execution or changes to other agent skills may occur without a separate approval step.

Mitigation: Review and install the OOMOL CLI separately before enabling the skill, and explicitly approve installer execution and any changes to other agent skills.

Risk: Quant Data requests use the connected OOMOL account and may consume service credit.

Mitigation: Check the connected account's available service credit before making requests.

## Reference(s):

- [Quant Data homepage](https://quantdata.us/)
- [Quant Data API documentation](https://quantdata.us/api/docs)
- [oo CLI repository](https://github.com/oomol-lab/oo-cli)
- [ClawHub skill release](https://clawhub.ai/oomol/skills/oo-quant-data)

## Skill Output:

**Output Type(s):** [JSON, Text, Market Data]

**Output Format:** [JSON market-data responses with text summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Action-specific results; selected actions use cursor pagination.]

## Skill Version(s):

1.0.2 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

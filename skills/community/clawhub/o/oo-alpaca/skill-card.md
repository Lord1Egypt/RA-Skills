## Description:

Retrieves Alpaca market and connected account data through the OOMOL-connected account.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers can retrieve market data and read account, order, position, and watchlist information from their connected Alpaca account.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Automatic setup or downloaded code may execute unverified software and make broader changes to the agent environment.

Mitigation: Use a verified release, review skill synchronization settings, and require approval before downloaded code runs or other agent skills change.

Risk: The connected Alpaca account may expose sensitive financial information to the connected service.

Mitigation: Review whether OOMOL should handle access to the intended financial account before connecting it.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/oomol/skills/oo-alpaca)
- [Alpaca](https://alpaca.markets/)
- [Alpaca API authentication documentation](https://docs.alpaca.markets/us/docs/authentication)
- [oo CLI repository](https://github.com/oomol-lab/oo-cli)

## Skill Output:

**Output Type(s):** [JSON, Text]

**Output Format:** [Alpaca data as JSON, with text summaries where useful]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Results depend on the selected read action.]

## Skill Version(s):

1.0.5 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

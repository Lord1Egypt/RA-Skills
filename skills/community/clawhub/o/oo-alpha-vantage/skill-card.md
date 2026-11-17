## Description:

Use Alpha Vantage through an OOMOL-connected account to retrieve market, company, and economic data.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and analysts use this skill to retrieve Alpha Vantage market, company, and economic data through an existing OOMOL connection.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Automatic setup may execute changing third-party CLI code and introduce broader agent changes without clear user control.

Mitigation: Review a specific oo CLI release before running it and check whether automatic skill synchronization is wanted; the publisher documents a synchronization-disable option.

## Reference(s):

- [Alpha Vantage API documentation](https://www.alphavantage.co/documentation/)
- [Alpha Vantage homepage](https://www.alphavantage.co)
- [oo CLI repository](https://github.com/oomol-lab/oo-cli)

## Skill Output:

**Output Type(s):** [API data, JSON, CSV, Shell commands, Guidance]

**Output Format:** [JSON or CSV data with shell command guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Raw provider data; format depends on the selected Alpha Vantage action.]

## Skill Version(s):

1.0.7 (source: frontmatter, server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

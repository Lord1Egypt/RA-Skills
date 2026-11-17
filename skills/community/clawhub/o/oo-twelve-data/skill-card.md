## Description:

Search Twelve Data and retrieve market information such as quotes, prices, company profiles, exchange details, and historical time series.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

People and agents use this skill to search financial instruments and retrieve market data through a connected Twelve Data account.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: CLI setup may run downloaded code and can add additional agent skills through startup synchronization.

Mitigation: Review and approve CLI installation separately after verifying its version and distribution. Set OO_SKILLS_SYNC_DISABLED to disable startup skill synchronization if you do not want it.

Risk: Queries may consume service credit.

Mitigation: Check account access and available credit before running repeated or large queries.

## Reference(s):

- [Twelve Data API Documentation](https://twelvedata.com/docs)
- [Twelve Data](https://twelvedata.com)
- [OO CLI Command Reference](https://github.com/oomol-lab/oo-cli/blob/main/docs/commands.md#environment-variables)

## Skill Output:

**Output Type(s):** [API Calls, Text, JSON]

**Output Format:** [Market data returned as text or JSON]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Results depend on the connected account and Twelve Data service access.]

## Skill Version(s):

1.0.5 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

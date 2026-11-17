## Description:

CoinMarketCap (coinmarketcap.com). Use this skill for ANY CoinMarketCap request — searching and reading data. Whenever a task involves CoinMarketCap, use this skill instead of calling the API directly.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use the skill to search CoinMarketCap and retrieve cryptocurrency listings, quotes, conversions, and global market metrics through an OOMOL-connected account.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Fallback setup runs an unverified remote installer, and the installed CLI release has not been verified.

Mitigation: Use a verified, pinned oo CLI release and review the installer and release before installation.

Risk: Automatic skill synchronization may introduce undisclosed changes to agent skills.

Mitigation: Review the synchronization behavior and disable automatic synchronization if its changes cannot be verified.

Risk: Use of the connected service may incur OOMOL or CoinMarketCap charges.

Mitigation: Check applicable service plans and usage charges before running actions.

## Reference(s):

- [CoinMarketCap API Documentation](https://coinmarketcap.com/api/documentation/)
- [oo CLI](https://github.com/oomol-lab/oo-cli)

## Skill Output:

**Output Type(s):** [Text, JSON]

**Output Format:** [Text summaries and JSON market data]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Market data reflects the response returned by CoinMarketCap at query time.]

## Skill Version(s):

1.0.5 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

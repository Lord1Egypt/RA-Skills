## Description:

CoinGecko (coingecko.com). Use this skill for ANY CoinGecko request — searching and reading data. Whenever a task involves CoinGecko, use this skill instead of calling the API directly.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers can retrieve CoinGecko coin, market, trending, and on-chain data through an agent connected to an OOMOL account. The agent can use returned data to answer cryptocurrency research and lookup requests.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Initial setup can run unverified remote code and may enable broad changes to agent skills through automatic synchronization.

Mitigation: Review setup, install a verified CLI version yourself, require approval before remote installers run, and consider disabling automatic skill synchronization.

Risk: CoinGecko requests pass through OOMOL and may consume credits.

Mitigation: Check the connected account and credit usage before making repeated or high-volume requests.

## Reference(s):

- [CoinGecko homepage](https://www.coingecko.com)
- [CoinGecko API authentication documentation](https://docs.coingecko.com/reference/authentication)
- [oo CLI repository](https://github.com/oomol-lab/oo-cli)
- [CoinGecko ClawHub release page](https://clawhub.ai/oomol/skills/oo-coingecko)

## Skill Output:

**Output Type(s):** [JSON data, Text summaries]

**Output Format:** [Structured JSON responses, optionally summarized as text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Returned fields and historical data availability depend on the selected action and CoinGecko plan.]

## Skill Version(s):

1.0.4 (source: frontmatter; confirmed by server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

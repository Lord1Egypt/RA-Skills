## Description:

Calculates Monero mining profitability from hashrate, power use, electricity cost, and market inputs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[liumaimiao](https://clawhub.ai/user/liumaimiao)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and cryptocurrency hobbyists use this skill to estimate Monero mining profitability from hashrate, power draw, electricity price, and market variables before experimenting with mining hardware.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Profitability estimates may be inaccurate because the sample calculator uses a simplified fixed mining estimate rather than live network difficulty and block reward.

Mitigation: Verify the formula and compare results with current Monero network difficulty, block reward, pool fees, and local electricity rates before making mining decisions.

Risk: Running or adapting the sample Python may contact CoinGecko for current Monero price data.

Mitigation: Review outbound network behavior and handle API availability, errors, and returned market data explicitly before relying on automated results.

## Reference(s):

- [CoinGecko Monero API](https://api.coingecko.com/api/v3/coins/monero)
- [ClawHub Skill Page](https://clawhub.ai/liumaimiao/skills/monero-profit-calculator-2026)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Guidance]

**Output Format:** [Markdown with shell command examples and Python sample code]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes simplified profitability estimates; current-price examples may depend on an external CoinGecko API call if the sample Python is run.]

## Skill Version(s):

1.0.0 (source: server evidence release.version, artifact package.json, artifact/SKILL.md)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

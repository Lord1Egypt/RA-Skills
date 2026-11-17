## Description:

Personal investing assistant for Lithuanian investors. Monitors markets, ETFs, crypto, pension funds (III pakopa), and provides monthly investment suggestions based on research and market conditions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[satnamra](https://clawhub.ai/user/satnamra)

### License/Terms of Use:

MIT

## Use Case:

External Lithuanian retail investors and agents supporting them use this skill to monitor ETF and crypto prices, plan monthly DCA allocations, and review pension, emergency fund, tax, and portfolio guidance as general research input.

### Deployment Geography for Use:

Lithuania

## Known Risks and Mitigations:

Risk: The monthly DCA script can execute unintended shell commands if a crafted budget value is passed as input.

Mitigation: Run it only with trusted, bounded numeric budget values or update the script to validate numeric input before execution.

Risk: Investing and tax content may be mistaken for personalized financial advice.

Mitigation: Treat outputs as general research guidance and verify recommendations against current market, tax, and personal financial context before acting.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/satnamra/skills/investing)
- [Yahoo Finance chart endpoint for VWCE](https://query1.finance.yahoo.com/v8/finance/chart/VWCE.DE)
- [CoinGecko Bitcoin EUR price endpoint](https://api.coingecko.com/api/v3/simple/price?ids=bitcoin&vs_currencies=eur)
- [CoinGecko Ethereum EUR price endpoint](https://api.coingecko.com/api/v3/simple/price?ids=ethereum&vs_currencies=eur)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration]

**Output Format:** [Markdown with inline shell commands and configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes general investing guidance, market-check workflow steps, DCA allocation output, and scheduled reminder examples.]

## Skill Version(s):

1.0.0 (source: frontmatter and ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

## Description:

Autonomous Polymarket weather-market trading flow for AION Market agents that prepares credentials, checks funding and approvals, selects an active weather market, submits a default 2 USDC market buy order, and verifies the result.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ssj124](https://clawhub.ai/user/ssj124)

### License/Terms of Use:

MIT-0

## Use Case:

External developers and trading-agent operators use this skill to run a one-shot AION Market / Polymarket weather-market trading flow after providing an AION API key and a wallet private key.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill asks for a raw wallet private key that can control assets in the wallet.

Mitigation: Use only a dedicated low-balance wallet and do not reuse keys that control other funds.

Risk: The skill can approve token spending and place market orders without per-transaction confirmation.

Mitigation: Review the selected market, spend size, allowance target, and order parameters before enabling automatic execution.

Risk: Automated weather-market trading can lose funds or execute at unfavorable prices.

Mitigation: Keep the spend size small, use explicit limits when needed, and verify fills through Polymarket after submission.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ssj124/skills/polymarket-weather-bands)
- [AION Market](https://aionmarket.com)
- [AION Market documentation](https://docs.aionmarket.com)
- [Polymarket weather markets endpoint](https://gamma-api.polymarket.com/events/pagination?tag_slug=weather&active=true&closed=false&archived=false&order=volume24hr&ascending=false&limit=20&offset=0)
- [Polymarket CLOB endpoint](https://clob.polymarket.com)

## Skill Output:

**Output Type(s):** [guidance, code, shell commands, configuration]

**Output Format:** [Markdown with tables, ordered steps, and Python code examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Guides an agent through credential handling, wallet checks, automatic approvals, market-order submission, and post-trade verification.]

## Skill Version(s):

0.3.0 (source: server release evidence and skill metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

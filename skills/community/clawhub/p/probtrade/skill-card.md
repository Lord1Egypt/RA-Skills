## Description:

Polymarket prediction markets: analytics, trading, hot markets, price movements, top traders, and market search. Powered by prob.trade.

This skill is ready for commercial/non-commercial use.

## Publisher:

[vlprosvirkin](https://clawhub.ai/user/vlprosvirkin)

### License/Terms of Use:


## Use Case:

External users and developers use this skill to query prob.trade market analytics, inspect Polymarket market activity, and manage trading account state. The skill can also place and cancel Polymarket orders through prob.trade API credentials.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can place or cancel real Polymarket orders through prob.trade credentials.

Mitigation: Require explicit human review of market, side, amount, price, and order ID before allowing an agent to run order or cancel commands.

Risk: Configured API credentials may authorize trading actions if exposed or reused.

Mitigation: Use a small, revocable, least-privilege prob.trade key and avoid storing live trading secrets in shared or backed-up directories.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/vlprosvirkin/skills/probtrade)
- [prob.trade Dashboard](https://app.prob.trade)
- [prob.trade Public API Reference](https://prob.trade/docs/public-api)
- [prob.trade Public API Overview](https://api.prob.trade/api/public/overview)
- [prob.trade Trading API](https://api.prob.trade/api/trading)

## Skill Output:

**Output Type(s):** [Text, Shell commands, Configuration, Guidance]

**Output Format:** [JSON emitted by Python command-line scripts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Python 3 and prob.trade API credentials for authenticated analytics and trading commands.]

## Skill Version(s):

2.0.5 (source: server release metadata; artifact frontmatter reports 2.0.3)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

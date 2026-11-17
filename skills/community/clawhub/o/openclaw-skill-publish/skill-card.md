## Description:

Polymarket prediction markets: analytics, trading, hot markets, price movements, top traders, and market search. Powered by prob.trade.

This skill is ready for commercial/non-commercial use.

## Publisher:

[vlprosvirkin](https://clawhub.ai/user/vlprosvirkin)

### License/Terms of Use:


## Use Case:

Developers and OpenClaw users use this skill to query prob.trade Polymarket market analytics and, when live credentials are configured, place orders, cancel orders, and inspect trading account state.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Live trading commands can place or cancel orders using persistent prob.trade credentials.

Mitigation: Require explicit user confirmation before order or cancel commands, including market, side, outcome, amount, order type, and price when applicable.

Risk: Stored API credentials could be misused if exposed or granted broader access than needed.

Mitigation: Use limited or revocable keys when available, prefer environment variables or locked-down config file permissions, and revoke keys from the dashboard if exposure is suspected.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/vlprosvirkin/skills/openclaw-skill-publish)
- [prob.trade Dashboard](https://app.prob.trade)
- [prob.trade Public API Reference](https://prob.trade/docs/public-api)
- [prob.trade Trading API Reference](https://github.com/vlprosvirkin/probtrade-openclaw-skill/blob/main/docs/trading-api-reference.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Structured JSON from command-line API calls, with Markdown instructions and shell command examples in the skill documentation.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Python 3 and prob.trade API credentials for authenticated analytics and trading commands.]

## Skill Version(s):

2.0.4 (source: server release metadata and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

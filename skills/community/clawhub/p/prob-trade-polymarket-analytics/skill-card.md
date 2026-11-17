## Description:

Polymarket prediction markets: analytics, trading, hot markets, price movements, top traders, and market search. Powered by prob.trade.

This skill is ready for commercial/non-commercial use.

## Publisher:

[vlprosvirkin](https://clawhub.ai/user/vlprosvirkin)

### License/Terms of Use:


## Use Case:

External users and developers use this skill to query prob.trade market analytics, search Polymarket prediction markets, inspect trader activity, and place or manage trades through an OpenClaw agent.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can place or cancel live financial orders without an explicit confirmation or dry-run safeguard.

Mitigation: Use a restricted or low-balance prob.trade key, require an external confirmation workflow before trading actions, and revoke keys when finished.

Risk: API credentials may be stored in a plaintext config file.

Mitigation: Prefer environment variables or protected secret storage for PROBTRADE_API_KEY and PROBTRADE_API_SECRET.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/vlprosvirkin/skills/prob-trade-polymarket-analytics)
- [prob.trade Dashboard](https://app.prob.trade)
- [Public API Reference](https://prob.trade/docs/public-api)
- [Trading API Reference](https://github.com/vlprosvirkin/probtrade-openclaw-skill/blob/main/docs/trading-api-reference.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands and structured JSON command output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Commands require Python 3 and prob.trade API credentials supplied through environment variables or configuration.]

## Skill Version(s):

2.0.5 (source: server release metadata; artifact frontmatter lists 2.0.3)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

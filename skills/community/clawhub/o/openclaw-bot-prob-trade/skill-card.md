## Description:

Autonomous trading bot for Polymarket via prob.trade. Run strategies, manage risk, scan markets. Requires the probtrade skill for API access.

This skill is ready for commercial/non-commercial use.

## Publisher:

[vlprosvirkin](https://clawhub.ai/user/vlprosvirkin)

### License/Terms of Use:


## Use Case:

Developers and trading operators use this skill to scan Polymarket markets, run configurable trading strategies through prob.trade, and inspect bot status or dry-run signals before enabling live orders.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can run persistent live trading and place real Polymarket orders when dry_run is disabled.

Mitigation: Keep dry_run enabled for initial testing, use restricted trading API keys and small exchange-side limits, and review the live-trading path before deployment.

Risk: Safety controls and dependency pinning are weaker than advertised.

Mitigation: Treat the built-in risk manager as incomplete rather than a hard safety boundary, and pin the probtrade dependency to a reviewed version or commit.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/vlprosvirkin/skills/openclaw-bot-prob-trade)
- [probtrade Skill Dependency](https://clawhub.ai/probtrade/prob-trade-polymarket-analytics)
- [prob.trade](https://app.prob.trade)
- [Polymarket Documentation](https://docs.polymarket.com/)
- [Strategy Reference](docs/strategies.md)
- [Deployment Guide](docs/deployment.md)
- [Autonomous Polymarket Trading Architecture](https://prob.trade/blog/autonomous-polymarket-trading-architecture)

## Skill Output:

**Output Type(s):** [text, JSON, shell commands, configuration, code, guidance]

**Output Format:** [Structured JSON and formatted terminal text, with Markdown documentation and inline shell or Python examples.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Commands can scan markets, report status, list strategies, or run a persistent trading loop; dry-run mode logs proposed orders without placing them.]

## Skill Version(s):

1.0.1 (source: server release metadata; artifact frontmatter reports 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

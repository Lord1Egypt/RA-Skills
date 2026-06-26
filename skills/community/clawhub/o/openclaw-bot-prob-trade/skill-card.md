## Description: <br>
Autonomous trading bot for Polymarket via prob.trade. Run strategies, manage risk, scan markets. Requires the probtrade skill for API access. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[vlprosvirkin](https://clawhub.ai/user/vlprosvirkin) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External developers and agent operators use this skill to run or preview Polymarket trading strategies through prob.trade, inspect trading status, and configure risk limits before live execution. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Live mode can automatically spend real funds with limited safeguards. <br>
Mitigation: Keep dry_run enabled until strategies are tested, start with limited funds, and use strict position, daily spend, exposure, and drawdown limits. <br>
Risk: The bot depends on prob.trade and optional external APIs that require credentials and outbound integrations. <br>
Mitigation: Use scoped and revocable API keys, rotate credentials periodically, and verify outbound integrations before enabling optional strategies. <br>
Risk: Trading strategy descriptions may include profit or arbitrage claims that do not eliminate market, liquidity, execution, or resolution risk. <br>
Mitigation: Do not rely on guaranteed-profit claims; validate strategy assumptions with scans and small order sizes before any live deployment. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/vlprosvirkin/openclaw-bot-prob-trade) <br>
- [Deployment guide](docs/deployment.md) <br>
- [Strategy reference](docs/strategies.md) <br>
- [References: Autonomous Trading on Polymarket](docs/references.md) <br>
- [probtrade skill on ClawHub](https://clawhub.ai/vlprosvirkin/prob-trade-polymarket-analytics) <br>
- [prob.trade dashboard](https://app.prob.trade) <br>
- [Polymarket documentation](https://docs.polymarket.com/) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, JSON, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands, configuration snippets, Python strategy examples, and JSON or formatted text command output.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Commands require Python 3 and the probtrade skill; live trading can place real orders when dry_run is false.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata; artifact frontmatter reports 1.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

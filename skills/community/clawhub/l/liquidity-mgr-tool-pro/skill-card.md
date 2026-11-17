## Description:

This skill helps teams and professional market makers manage DeFi liquidity portfolios with batch position operations, automated rebalancing, V4 Hook strategy planning, yield optimization, hedging guidance, and risk monitoring.

This skill is ready for commercial/non-commercial use.

## Publisher:

[thcjp](https://clawhub.ai/user/thcjp)

### License/Terms of Use:

MIT-0

## Use Case:

External DeFi teams, independent developers, and professional liquidity managers use this skill to plan and operate multi-pool liquidity portfolios, rebalancing rules, hedging approaches, and risk alerts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill covers automated DeFi financial actions, including rebalancing, hedging, and wallet-connected workflows.

Mitigation: Use simulation or test mode first, require explicit transaction review, and keep wallet permissions conservative.

Risk: The evidence security summary flags broad execution/write authority combined with financial operations.

Mitigation: Run with tightly scoped prompts, avoid unrestricted API keys or signer access, and review generated commands before execution.

Risk: The evidence security summary identifies a mismatched trigger that could invoke the skill for unrelated DevOps or monitoring tasks.

Mitigation: Correct the trigger language before publication so the skill activates only for DeFi liquidity-management requests.

Risk: The artifact recommends V4 Hooks and hedging strategies that can carry contract, market, gas, and slippage risk.

Mitigation: Backtest strategies, audit custom contract hooks, set conservative thresholds, and verify that expected fees cover gas and hedging costs.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/thcjp/skills/liquidity-mgr-tool-pro)
- [Publisher profile](https://clawhub.ai/user/thcjp)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with JSON, text, bash, and Python code examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include structured status, result, execution log, and error fields.]

## Skill Version(s):

1.0.0 (source: server release metadata and frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

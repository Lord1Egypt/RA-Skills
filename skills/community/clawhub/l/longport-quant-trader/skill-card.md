## Description:

LongPort Quant Trader helps agents configure, monitor, backtest, and run LongPort OpenAPI trading strategies for Hong Kong and U.S. equities with Feishu notifications and performance tracking.

This skill is ready for commercial/non-commercial use.

## Publisher:

[fxm1618-gmail](https://clawhub.ai/user/fxm1618-gmail)

### License/Terms of Use:

MIT-0

## Use Case:

External users, individual investors, and quantitative trading developers use this skill to generate and operate Python-based LongPort trading workflows, including market scans, strategy execution, backtests, notification setup, and performance reports.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The package can submit live brokerage orders through LongPort credentials.

Mitigation: Require paper-trading validation, explicit live-trading enablement, position limits, and a kill switch before any real account use.

Risk: Bundled credential material may expose broker or notification access.

Mitigation: Remove bundled secrets, rotate any exposed keys or tokens, and require users to supply credentials through local environment variables or a secrets manager.

Risk: A hard-coded Feishu recipient can send trading notifications to an unintended destination.

Mitigation: Make all Feishu webhook and recipient values user-configured and verify the destination before enabling notifications.

Risk: Unpinned dependencies can change behavior or introduce supply-chain risk.

Mitigation: Pin dependency versions and review updates before deploying the trading workflow.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/fxm1618-gmail/skills/longport-quant-trader)
- [LongPort OpenAPI](https://open.longportapp.com)
- [LongPort OpenAPI Docs](https://open.longportapp.com/docs)
- [LongPort API Account](https://open.longportapp.com/account)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown, Python code, shell commands, JSON-like configuration, and console status text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Python 3 and LongPort API environment variables for live API workflows.]

## Skill Version(s):

1.0.0 (source: server release metadata and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

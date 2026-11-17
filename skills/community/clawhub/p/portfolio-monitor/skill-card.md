## Description:

投资组合监控系统。管理股票、加密货币持仓，跟踪成本、盈亏，设置价格提醒，生成组合报告。支持港股、美股、加密货币。

This skill is ready for commercial/non-commercial use.

## Publisher:

[sanduan003](https://clawhub.ai/user/sanduan003)

### License/Terms of Use:


## Use Case:

External users and agents use this skill to configure and run a portfolio monitor for stocks and crypto, calculate current value, cost basis, profit and loss, and generate threshold alerts. Its outputs are for record-keeping reference and should not be treated as financial advice.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The install guidance uses --break-system-packages and may modify the host Python environment in an unsafe way.

Mitigation: Install dependencies in a virtual environment with pinned versions before running the script.

Risk: The script reads and writes portfolio data under a hard-coded OpenClaw memory path.

Mitigation: Review the configured path, run in an isolated workspace, and back up portfolio data before execution.

Risk: Portfolio values and alerts can be mistaken for investment recommendations.

Mitigation: Treat the output as a record-keeping aid only and independently verify financial decisions.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/sanduan003/skills/portfolio-monitor)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with bash and JSON examples; runtime output is console text and portfolio state JSON.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses configured holdings, currencies, and an alert threshold; market data availability depends on yfinance.]

## Skill Version(s):

1.1.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

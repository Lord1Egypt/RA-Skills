## Description:

专业股票量化交易技能，支持股票数据查询、策略回测、智能选股和交易信号提示。

This skill is ready for commercial/non-commercial use.

## Publisher:

[zhfqqqq1234](https://clawhub.ai/user/zhfqqqq1234)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external users can use this skill to explore stock data, run basic quantitative backtests, screen stocks, and generate educational trading-signal summaries. Outputs should be reviewed before any financial or trading use.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill gives concrete trading recommendations and stock signals that could be mistaken for financial advice.

Mitigation: Treat outputs as educational or demo data and require human financial review before using them for trading decisions.

Risk: The demo UI uses an unsafe HTML insertion pattern.

Mitigation: Avoid hosting the demo page on a sensitive origin until user-controlled content is rendered safely.

Risk: The installation guidance references unpinned third-party packages.

Mitigation: Install dependencies only in an isolated environment with pinned and verified package versions.

Risk: The skill may require API keys for market-data services.

Mitigation: Provide API keys only for trusted services and scope or rotate credentials according to local policy.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/zhfqqqq1234/skills/niuniu-quant)
- [牛牛量化 documentation](https://niuniu-quant.readthedocs.io)

## Skill Output:

**Output Type(s):** [Text, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline bash, Python, YAML, and plain-text examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes educational stock summaries, backtest reports, stock-screening lists, and trading-signal guidance.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

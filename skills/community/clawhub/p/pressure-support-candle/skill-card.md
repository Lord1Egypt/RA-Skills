## Description:

基于波峰波谷分析识别A股股票的压力位和支撑位，并生成带标注的K线图；默认使用Baostock获取日线数据。

This skill is ready for commercial/non-commercial use.

## Publisher:

[wtjjacobj](https://clawhub.ai/user/wtjjacobj)

### License/Terms of Use:

MIT-0

## Use Case:

External developers, analysts, or agents use this skill to run A-share support and resistance analysis, inspect calculated levels and breakout signals, and produce annotated candlestick PNG charts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill contacts external Baostock or AkShare-backed stock data sources depending on which bundled script is run.

Mitigation: Confirm that external market-data access is acceptable before installation or execution.

Risk: The documented Baostock entrypoint creates chart PNG files locally, including on ~/Desktop.

Mitigation: Run in a workspace where local chart-file creation is expected, or adjust the output path before use.

Risk: Documentation inconsistencies may make the active data source or behavior unclear.

Mitigation: Prefer the documented Baostock entrypoint and review the selected script before execution.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wtjjacobj/skills/pressure-support-candle)
- [压力支撑位识别_设计文档.md](artifact/压力支撑位识别_设计文档.md)

## Skill Output:

**Output Type(s):** [text, shell commands, code, files]

**Output Format:** [Markdown guidance with shell commands and locally generated PNG chart files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May print support and resistance price data; the documented Baostock entrypoint writes chart PNG files locally, including to ~/Desktop.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

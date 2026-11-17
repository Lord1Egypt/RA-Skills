## Description:

主力建仓前兆扫描 - 通过量价数据识别主力悄悄吸筹的潜力股。

This skill is ready for commercial/non-commercial use.

## Publisher:

[2459762052-spec](https://clawhub.ai/user/2459762052-spec)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to screen China A-share candidates for low-volatility consolidation, moderate volume expansion, price-position, anomaly, and trend signals. The generated candidates are informational screening output and are not investment advice.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The scan produces stock-screening signals that may be wrong or misleading in some market conditions.

Mitigation: Treat the report as informational screening output only and review candidates with independent market context before acting.

Risk: The script uses Eastmoney public market-data APIs and depends on network access and third-party data availability.

Mitigation: Install only when those API calls are acceptable, and verify data freshness and source availability before relying on results.

Risk: The evidence notes hard-coded local paths and a bash-vs-Python command mismatch that may prevent the script from working on another machine.

Mitigation: Adjust local paths and invoke the script with the appropriate Python execution method before deployment.

## Reference(s):

- [Methodology](references/methodology.md)
- [ClawHub skill page](https://clawhub.ai/2459762052-spec/skills/main-force-scan)
- [Eastmoney finance data source](https://finance.eastmoney.com/)

## Skill Output:

**Output Type(s):** [markdown, shell commands, guidance]

**Output Format:** [Markdown report with tabular stock-screening candidates and concise command guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes a dated local Markdown report with ranked Top20 candidates when the bundled script runs successfully.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

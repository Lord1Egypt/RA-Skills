## Description: <br>
Helps agents write, review, and debug C# trading strategies for the IRS (SunnyQuant Investment Research System) framework. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dameng324](https://clawhub.ai/user/dameng324) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and quantitative engineers use this skill to create, modify, troubleshoot, and document IRS/SunnyQuant strategies, including lifecycle callbacks, market data subscriptions, order algorithms, parameters, charting, and data access patterns. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Bundled documentation exposes usable-looking credentials and internal service endpoints. <br>
Mitigation: Treat exposed credentials as compromised, rotate them, and remove secrets and internal endpoints before installing or redistributing the skill. <br>
Risk: Trading examples can guide live order placement without strong safety guardrails. <br>
Mitigation: Review examples manually, run strategies in backtest or paper/simulation first, and add explicit live-trading confirmation, account checks, risk limits, and kill-switch controls. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/dameng324/irs-strategist) <br>
- [IRS API documentation](https://irs_doc.shengguanda.com/docs/api/IRS.Common/CommonStrategy) <br>
- [Stock Indicators documentation](https://dotnet.stockindicators.dev/indicators/) <br>
- [IRS algorithm reference](references/algorithms.md) <br>
- [IRS data access reference](references/data.md) <br>
- [IRS strategy examples](references/examples.md) <br>
- [JYDB data dictionary index](references/jydb.md) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration] <br>
**Output Format:** [Markdown guidance with C# code examples, shell commands, and configuration notes] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May reference IRS framework APIs, trading strategy lifecycle concepts, data schemas, and account/order handling patterns.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release evidence; package.json lists 1.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

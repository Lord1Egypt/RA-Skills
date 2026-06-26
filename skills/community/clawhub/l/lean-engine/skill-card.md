## Description: <br>
Run QuantConnect LEAN backtests and manage US equity algorithm development, including strategy backtesting, market data setup, configuration editing, result analysis, and Interactive Brokers TWS deployment guidance. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[cylqqqcyl](https://clawhub.ai/user/cylqqqcyl) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and quantitative trading practitioners use this skill to prepare a local LEAN environment, run Python algorithm backtests, download US equity data, and review backtest outputs. It also guides configuration changes for backtesting and Interactive Brokers live-trading setup. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The backtest helper temporarily replaces the active LEAN config during execution. <br>
Mitigation: Review the helper scripts before use, run them in a separate LEAN workspace or with a credential-free backtesting config, and avoid concurrent LEAN sessions. <br>
Risk: A LEAN config used for Interactive Brokers can contain live-trading credentials. <br>
Mitigation: Do not store Interactive Brokers credentials in the config used by this skill; keep live-trading credentials in a separate protected configuration. <br>
Risk: Setup and data-download flows install packages and fetch market data from external sources. <br>
Mitigation: Install dependencies in an isolated environment and review downloaded data before relying on backtest results. <br>


## Reference(s): <br>
- [LEAN data download reference](artifact/references/data-download.md) <br>
- [.NET 8 SDK download](https://dotnet.microsoft.com/download/dotnet/8.0) <br>
- [LEAN Engine skill release](https://clawhub.ai/cylqqqcyl/lean-engine) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline code blocks and shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May reference local LEAN paths, environment variables, generated config files, market data files, and backtest result locations.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

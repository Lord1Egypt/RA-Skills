## Description: <br>
Monitors Chinese gold ETFs, Shanghai AU9999 spot gold, COMEX gold futures, DXY, USD/CNY, and A-share gold mining stocks for cross-market gold analysis. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[song0828](https://clawhub.ai/user/song0828) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to run a Python-based market monitor for Chinese gold ETFs and related gold-market indicators. The output supports informational review of price, volume, currency, futures, and mining-stock signals and is not investment advice. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The script makes outbound market-data requests through akshare. <br>
Mitigation: Install and run it only in an environment where outbound akshare requests are acceptable. <br>
Risk: The script depends on Python packages such as akshare and pandas. <br>
Mitigation: Use a virtual environment for dependencies before running the monitor. <br>
Risk: Market data can be delayed or incomplete and may be misread as trading advice. <br>
Mitigation: Treat output as informational market data and verify important decisions against authoritative market sources. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/song0828/gold-monitor-cn) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, guidance] <br>
**Output Format:** [Markdown instructions and terminal text output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires python3 and runtime access to akshare market-data sources; output is informational market data rather than investment advice.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

## Description: <br>
A股量化数据分析工具，基于AkShare库获取A股行情、财务数据、板块信息等。用于回答关于A股股票查询、行情数据、财务分析、选股等问题。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Sunshine-del-ux](https://clawhub.ai/user/Sunshine-del-ux) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and developers use this skill to query China A-share market data through AkShare, including real-time quotes, historical K-line data, financial indicators, sector information, fund flow, IPO, and margin trading data. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: AkShare is a third-party dependency and the skill retrieves market data over the network. <br>
Mitigation: Review and pin the AkShare dependency version before deployment, and run the skill in an environment with appropriate network controls. <br>
Risk: Market data may be delayed, unavailable, or unsuitable for investment decisions. <br>
Mitigation: Use outputs as research data only and verify important results against authoritative market-data sources. <br>
Risk: The bundled fund-flow command may need a code fix before it works. <br>
Mitigation: Test the CLI paths in a local environment and fix the fund-flow helper before relying on that command. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/Sunshine-del-ux/new-akshare-stock) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, guidance] <br>
**Output Format:** [Markdown and text guidance with Python and shell command examples; the bundled CLI emits JSON.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses AkShare as a third-party market-data dependency; results depend on network access and upstream data availability.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

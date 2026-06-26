## Description: <br>
A股量化数据分析工具，基于AkShare库获取A股行情、财务数据、板块信息等。用于回答关于A股股票查询、行情数据、财务分析、选股等问题。 <br>

This skill is for research and development only. <br>

## Publisher: <br>
[make453](https://clawhub.ai/user/make453) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to query public A-share market data, retrieve historical prices and financial metrics, and draft stock-analysis responses with AkShare or Baostock examples. The artifact states the data and analysis are for academic research and are not investment advice. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Investment-style signals, suggested position sizes, stop losses, and targets may be mistaken for personalized financial advice. <br>
Mitigation: Treat outputs as informational research only, do not automate trades from them, and validate decisions with appropriate professional or internal review. <br>
Risk: AkShare or Baostock package behavior and upstream market-data interfaces may change or fail because of network or source-site issues. <br>
Mitigation: Pin or verify package versions for important workflows, add exception handling and retries, and cross-check important market data against another source. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/make453/new-akshare-stock-bak2) <br>
- [Publisher profile](https://clawhub.ai/user/make453) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, JSON, guidance] <br>
**Output Format:** [Markdown guidance with Python code examples, shell install commands, JSON CLI output, and text stock-analysis reports] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses public market-data APIs through AkShare or Baostock; no credentials or trading access are requested.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and artifact _meta.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

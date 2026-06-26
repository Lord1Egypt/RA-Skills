## Description: <br>
Generates Indonesian-language IHSG morning and closing session summaries with index data, top net buy/sell stocks, foreign flow, YTD flow, and market insights using Yahoo Finance, Infovesta, and Tavily. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[raufimusaddiq](https://clawhub.ai/user/raufimusaddiq) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
External users, analysts, and agent operators use this skill to run scheduled Indonesian stock-market session summaries after the IHSG morning and closing sessions. It helps assemble market data, foreign flow signals, and concise Bahasa Indonesia commentary for recurring reports. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Financial figures and generated market insights may be incomplete, stale, or unsuitable as the sole basis for trading decisions. <br>
Mitigation: Verify important IHSG, flow, and stock-level figures against trusted market sources before acting on them. <br>
Risk: The skill requires a Tavily API key and can consume paid or rate-limited web-search quota during scheduled runs. <br>
Mitigation: Use a limited Tavily key where possible and monitor API usage, especially when enabling cron-based execution. <br>
Risk: The release runs a local Python script with third-party dependencies and outbound requests to public market and news sources. <br>
Mitigation: Install dependencies in a controlled environment and review local execution permissions before deployment. <br>


## Reference(s): <br>
- [IHSG Session Summary on ClawHub](https://clawhub.ai/raufimusaddiq/ihsg-session-summary) <br>
- [Yahoo Finance IDX Composite Chart Endpoint](https://query1.finance.yahoo.com/v8/finance/chart/%5EJKSE) <br>
- [Tavily API Key Dashboard](https://app.tavily.com) <br>
- [Infovesta Top Buy Data](https://www.infovesta.com/index/data_info/saham/topbuy) <br>
- [Infovesta Top Sell Data](https://www.infovesta.com/index/data_info/saham/topsell) <br>


## Skill Output: <br>
**Output Type(s):** [Text, JSON, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Plain text market report with ASCII tables; optional JSON from the extractor CLI.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs are intended to be in Bahasa Indonesia and may include generated search queries when market data is incomplete.] <br>

## Skill Version(s): <br>
4.0.1 (source: server release metadata and SKILL.md metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

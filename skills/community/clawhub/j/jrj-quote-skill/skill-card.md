## Description: <br>
Provides A-share real-time quotes, historical daily K-line data, and local technical indicator calculations for stocks, listed funds, and indices. <br>

This skill is for research and development only. <br>

## Publisher: <br>
[haomanjia](https://clawhub.ai/user/haomanjia) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, developers, and market-analysis agents use this skill to fetch JRJ A-share quote and K-line data, compute indicators such as MA, MACD, KDJ, BOLL, and RSI, and prepare structured market-analysis outputs for review. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires a JRJ_API_KEY, which can expose account access if leaked. <br>
Mitigation: Store the key in the environment, keep it scoped, avoid logging it, and rotate it if exposure is suspected. <br>
Risk: Using an untrusted JRJ_API_URL could send requests or credentials to an unintended service. <br>
Mitigation: Leave JRJ_API_URL unset unless intentionally using a trusted JRJ-compatible HTTPS endpoint. <br>
Risk: Market data and technical indicators can be incomplete, delayed, or misread as investment advice. <br>
Mitigation: Treat outputs as informational, verify important data independently, and require human review for investment decisions. <br>
Risk: Truncated historical K-line responses can reduce indicator accuracy when warm-up data is insufficient. <br>
Mitigation: Check truncation flags and adjust limit or start-date parameters before relying on calculated indicators. <br>


## Reference(s): <br>
- [API 接口参考](references/api-reference.md) <br>
- [技术指标说明](references/indicators-guide.md) <br>
- [JRJ OpenClaw homepage](https://ai.jrj.com.cn/claw) <br>
- [ClawHub release page](https://clawhub.ai/haomanjia/jrj-quote-skill) <br>


## Skill Output: <br>
**Output Type(s):** [API Calls, JSON, Markdown, Shell commands, Guidance] <br>
**Output Format:** [JSON or Markdown market-data tables with optional technical-analysis guidance and shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires JRJ_API_KEY; supports local indicator calculations for historical daily K-line data.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

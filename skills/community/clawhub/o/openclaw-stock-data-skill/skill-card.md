## Description: <br>
使用 data.diemeng.chat 提供的接口查询股票日线、分钟线、财务指标等数据，支持 A 股等市场。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[1018466411](https://clawhub.ai/user/1018466411) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
External developers and OpenClaw users use this skill to query market data from data.diemeng.chat for stock, ETF, bond, index, valuation, calendar, and snapshot analysis after configuring an API key. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill sends API keys and market-data queries to data.diemeng.chat. <br>
Mitigation: Install only if the user trusts data.diemeng.chat, configure STOCK_API_KEY through OpenClaw secrets or environment variables, and do not place real keys in source files or URL query strings. <br>
Risk: Broad symbols, long date ranges, or high limits can expose more query intent than needed and consume quota. <br>
Mitigation: Use narrow symbols, date ranges, page sizes, and limits, and paginate large results instead of requesting bulk data unnecessarily. <br>
Risk: Permission, rate-limit, or blacklist controls can block requests when credentials are invalid, unauthorized, or overused. <br>
Mitigation: Handle 401, 403, and 429 responses clearly, reuse the configured key, and reduce request frequency before retrying. <br>


## Reference(s): <br>
- [ClawHub skill listing](https://clawhub.ai/1018466411/openclaw-stock-data-skill) <br>
- [data.diemeng.chat API service](https://data.diemeng.chat/) <br>
- [OpenClaw Skills Config](https://docs.openclaw.ai/tools/skills-config) <br>
- [OpenClaw Skills](https://docs.openclaw.ai/tools/skills) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with JSON request examples, Python snippets, and shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires STOCK_API_KEY and scoped market-data query parameters such as symbols, date ranges, pagination, limits, and intervals.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release metadata, clawhub.json, skill.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

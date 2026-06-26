## Description: <br>
按股票代码查当日行情与详情（分钟级趋势），或按分类拉取沪深、港股、北证等股票列表。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jisuapi](https://clawhub.ai/user/jisuapi) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to retrieve current stock quotes, minute-level trend data, single-stock details, and paginated stock lists for沪深股市, 港股, and 北证A股 through JisuAPI. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill sends stock symbols, list parameters, and the configured API key to JisuAPI. <br>
Mitigation: Use only a JisuAPI key intended for this integration, review provider terms and privacy expectations, and avoid submitting sensitive or unnecessary query data. <br>
Risk: API calls can consume provider quota or create billable usage. <br>
Mitigation: Monitor JisuAPI quota and billing, and keep requested pages and query frequency aligned with the user's need. <br>
Risk: Financial market data may be delayed, unavailable, or unsuitable as sole investment advice. <br>
Mitigation: Treat returned stock data as informational, check timestamps and API errors, and avoid making investment recommendations solely from this skill output. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/jisuapi/jisu-stock) <br>
- [JisuAPI stock API documentation](https://www.jisuapi.com/api/stock/) <br>
- [JisuAPI homepage](https://www.jisuapi.com/) <br>
- [Related stock history skill](https://clawhub.ai/jisuapi/stockhistory) <br>


## Skill Output: <br>
**Output Type(s):** [text, json, shell commands, guidance] <br>
**Output Format:** [JSON responses and Markdown usage guidance with shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires python3 and JISU_API_KEY; sends stock symbols, list parameters, and the API key to JisuAPI.] <br>

## Skill Version(s): <br>
1.0.6 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

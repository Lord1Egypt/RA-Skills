## Description: <br>
查询上金所、上期所、港金、银行渠道、伦敦金银及品牌金店等多源黄金参考价；涨跌字段可辅助说明走势（非投资建议）。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jisuapi](https://clawhub.ai/user/jisuapi) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to retrieve current or recent gold price reference data from JisuAPI across exchanges, banks, London markets, Hong Kong markets, brand stores, and historical market intervals. Agents should use returned price, high-low, close, and change fields to summarize market data without presenting predictions as investment advice. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Gold price queries and the JisuAPI AppKey are sent to a third-party API provider. <br>
Mitigation: Use only in environments where sending those query parameters to JisuAPI is acceptable, and keep JISU_API_KEY scoped and managed as a credential. <br>
Risk: Trend summaries could be mistaken for investment advice. <br>
Mitigation: Limit responses to market-data explanations grounded in returned fields and clearly avoid unsupported predictions or financial recommendations. <br>
Risk: Returned prices may be delayed, unavailable, or limited by API permissions and quota. <br>
Mitigation: Surface API errors and timestamps to the user, and avoid relying on the skill as the sole source for time-sensitive trading decisions. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/jisuapi/skills/gold) <br>
- [JisuAPI](https://www.jisuapi.com/) <br>
- [JisuAPI Gold API](https://www.jisuapi.com/api/gold/) <br>
- [JisuAPI Gold endpoint](https://api.jisuapi.com/gold) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, API data] <br>
**Output Format:** [Markdown guidance with shell commands and JSON API responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires python3 and JISU_API_KEY; store price queries accept an optional date and historical queries require market, startdate, enddate, and type.] <br>

## Skill Version(s): <br>
1.0.14 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

## Description: <br>
新股申购助手 - A 股 IPO 申购必备工具。提供新股申购日历、基本面分析、中签率预测、上市溢价预测、申购建议。适用于 A 股新股投资者。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zhaoteng-qd](https://clawhub.ai/user/zhaoteng-qd) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External A-share IPO investors use this skill to inspect IPO subscription calendars, compare IPO fundamentals, estimate lottery win rates and listing premiums, and get reminder-oriented IPO guidance. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill contacts public financial-data services and may receive stale, unavailable, or inaccurate IPO data. <br>
Mitigation: Verify IPO dates, prices, and eligibility requirements against official exchange announcements before acting. <br>
Risk: The skill writes local cache and reminder configuration files, and can optionally read a Tushare token from the environment or data/tushare_token.txt. <br>
Mitigation: Review local files and credential handling before installation, and avoid storing sensitive tokens in shared workspaces. <br>
Risk: Win-rate, premium, and subscription suggestions are informational estimates rather than financial advice. <br>
Mitigation: Use the output as one input to independent investment review and do not rely on it as a guarantee of return. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/zhaoteng-qd/ipo-assistant) <br>
- [Publisher Profile](https://clawhub.ai/user/zhaoteng-qd) <br>
- [API Reference](references/API.md) <br>
- [User Guide](references/USER_GUIDE.md) <br>
- [东方财富新股数据](http://data.eastmoney.com/xg/xg/default.html) <br>
- [上海证券交易所](http://www.sse.com.cn/) <br>
- [深圳证券交易所](http://www.szse.cn/) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown-style text with command examples, tabular IPO data, and investment guidance summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs are informational and may depend on public financial-data services, local cache files, and optional Tushare credentials.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

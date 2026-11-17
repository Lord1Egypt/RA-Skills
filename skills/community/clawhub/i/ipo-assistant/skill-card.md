## Description:

新股申购助手 helps A-share IPO investors review subscription calendars, basic issuer analysis, win-rate estimates, first-day premium estimates, comparisons, statistics, and reminders.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zhaoteng-qd](https://clawhub.ai/user/zhaoteng-qd)

### License/Terms of Use:

MIT-0

## Use Case:

External A-share IPO investors use this skill to check upcoming subscriptions, compare IPO candidates, and receive educational IPO analysis and reminders. Outputs should be treated as decision support, not financial advice.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Investment-style recommendations and predictions may rely on mock or weakly verified data.

Mitigation: Treat outputs as educational decision support and verify IPO details against official exchange, broker, or issuer sources before acting.

Risk: The Tushare integration can read a token from an environment variable or local file.

Mitigation: Prefer managed secrets or environment variables and avoid storing tokens in data/tushare_token.txt.

Risk: The skill uses network data sources and Python dependencies that may change or fail.

Mitigation: Install in an isolated environment, pin dependency versions, and confirm each data source is reachable before relying on results.

Risk: Reminder behavior can schedule weekday notifications and forward IPO messages to configured channels.

Mitigation: Enable reminders only after reviewing the schedule, timezone, payload, and destination channel.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/zhaoteng-qd/skills/ipo-assistant)
- [User Guide](references/USER_GUIDE.md)
- [Data Source API Guide](references/API.md)
- [Eastmoney IPO data API](http://datacenter-web.eastmoney.com/api/data/v1/get)
- [China Securities Information](http://www.cninfo.com.cn/)
- [Shanghai Stock Exchange](http://www.sse.com.cn/)
- [Shenzhen Stock Exchange](http://www.szse.cn/)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Plain text and Markdown-style command-line output in Chinese, with command examples and optional reminder configuration.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs may include IPO calendars, analysis summaries, win-rate and premium estimates, comparison tables, statistics, and reminder messages.]

## Skill Version(s):

1.0.0 (source: server release metadata; also listed in target metadata, README, and SKILL.md)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

## Description: <br>
监控黄金价格 - 获取实时国际金价，记录历史价格，当价格波动超过阈值时发出通知。适合 OpenClaw 定时调用。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[whatyouprompt](https://clawhub.ai/user/whatyouprompt) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and OpenClaw agents use this skill to check Au99.99 gold quotes, track local price baselines, and surface threshold-based buy/sell alerts for informational monitoring. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill presents buy, sell, or hold suggestions from public quote data and a fixed threshold, which could be mistaken for financial advice. <br>
Mitigation: Treat alerts as informational, verify prices with a trusted source, and make financial decisions outside the skill. <br>
Risk: Scheduled use makes outbound requests to Sina Finance and depends on a public quote endpoint that may change or become unavailable. <br>
Mitigation: Install only where scheduled outbound requests are acceptable, and handle error status output before notifying users. <br>
Risk: Some comments and labels mention CCB even though the implementation uses Sina and Shanghai Gold Exchange Au99.99 data. <br>
Mitigation: Review the reported source field and data endpoint when interpreting alerts or adapting the skill. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/whatyouprompt/gold-price-monitor) <br>
- [Sina Finance](https://finance.sina.com.cn/) <br>
- [Sina Finance Au99.99 quote endpoint](http://hq.sinajs.cn/?list=gds_AU9999) <br>


## Skill Output: <br>
**Output Type(s):** [text, JSON, shell commands, guidance] <br>
**Output Format:** [JSON result with human-readable alert message text] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes local JSON baseline files for price history and daily opening prices.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

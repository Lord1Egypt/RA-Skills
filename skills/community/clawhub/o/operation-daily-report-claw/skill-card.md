## Description: <br>
运营数据日报虾 automates multi-platform operations data collection, normalization, daily or weekly Markdown report generation, anomaly detection, and Feishu delivery. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tujinsama](https://clawhub.ai/user/tujinsama) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Operations, growth, and content teams use this skill to collect metrics from Douyin, Xiaohongshu, WeChat Channels, Bilibili, and Weibo, then generate structured daily, weekly, or monthly reports. It is also used to flag unusual changes such as traffic drops, follower loss, low engagement, or collection failures and send Feishu notifications. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill handles platform tokens, cookies, SESSDATA, and other credentials. <br>
Mitigation: Keep credentials in a private .env file, exclude that file from source control, rotate expired cookies or tokens, and install only in workspaces where this credential access is acceptable. <br>
Risk: Generated reports and Feishu messages can expose business metrics or send alerts to unintended recipients. <br>
Mitigation: Review report content, Feishu document targets, chat recipients, and any @all alert behavior before sending or enabling unattended delivery. <br>
Risk: Scheduled collection can run without user review and repeatedly call third-party platform APIs. <br>
Mitigation: Enable cron only when recurring collection is intended, respect platform rate limits, and monitor failures or stale credentials. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/tujinsama/operation-daily-report-claw) <br>
- [Platform API guide](artifact/references/platform-api-guide.md) <br>
- [Report templates](artifact/references/report-templates.md) <br>
- [Anomaly rules](artifact/references/anomaly-rules.md) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown reports with supporting JSON data files and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May write collected platform data under data/raw and generated reports under data/reports; optional Feishu delivery and cron scheduling depend on user configuration.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

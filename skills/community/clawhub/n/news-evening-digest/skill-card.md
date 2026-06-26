## Description: <br>
每天晚上 8 点自动推送全球新闻晚报到 QQ 和飞书，参考 World Monitor 数据源。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[cp3d1455926-svg](https://clawhub.ai/user/cp3d1455926-svg) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and operators use this skill to collect current news, format a Chinese evening digest, and schedule delivery to messaging channels such as QQ and Feishu-compatible workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The outbound destination may not match the documented Feishu workflow. <br>
Mitigation: Review or edit the script before installation so the configured webhook destination is the intended channel. <br>
Risk: Webhook URLs and API keys can grant message-sending or data-access privileges if exposed. <br>
Mitigation: Use dedicated webhook and API credentials, store them as secrets, and rotate them if shared or logged. <br>
Risk: Scheduled digest delivery can repeatedly notify a broad audience. <br>
Mitigation: Test in a dedicated channel first, confirm whether all-member mentions are acceptable, and remove the cron or Task Scheduler entry when no longer needed. <br>


## Reference(s): <br>
- [ClawHub skill release](https://clawhub.ai/cp3d1455926-svg/news-evening-digest) <br>
- [Publisher profile](https://clawhub.ai/user/cp3d1455926-svg) <br>
- [World Monitor API](https://api.worldmonitor.app) <br>
- [Tavily Search API endpoint](https://api.tavily.com/search) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Chinese news digest text with setup guidance and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can send outbound webhook notifications and prints run status to the console.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release and frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

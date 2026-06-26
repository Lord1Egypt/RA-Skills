## Description: <br>
Morning Radar collects news for configured topics with Baidu AI Search, formats a Markdown briefing, and sends it to a Feishu recipient. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Diomedeak](https://clawhub.ai/user/Diomedeak) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to create scheduled, topic-based news briefings and deliver them to a Feishu user. It is suited for daily monitoring of AI, technology, finance, or other configured news topics. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Configured search topics are sent to Baidu for retrieval. <br>
Mitigation: Install only when sharing those topics with Baidu is acceptable, and avoid putting sensitive topics in scheduled queries. <br>
Risk: Generated briefings are sent to the configured Feishu recipient. <br>
Mitigation: Verify the Feishu receiver Open ID and use a least-privilege Feishu app before enabling automatic delivery. <br>
Risk: API keys and app secrets can be exposed if stored in committed configuration files. <br>
Mitigation: Prefer environment variables or protected secret storage, and do not commit config.json with live credentials. <br>
Risk: A cron job can continue sending briefings after the skill is no longer needed. <br>
Mitigation: Remove the scheduled job when automatic daily delivery should stop. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/Diomedeak/morning-radar) <br>
- [Baidu Qianfan Platform](https://qianfan.baidubce.com) <br>
- [Feishu Open Platform](https://open.feishu.cn) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown briefing text sent as a Feishu text message, with setup commands and configuration guidance.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Baidu API credentials, Feishu app credentials, and a recipient Open ID; optional cron setup supports daily delivery.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata; artifact package metadata lists 1.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

## Description: <br>
基于柳比歇夫方法的时间与精力管理助理，通过飞书多维表格存储数据，支持自然语言记录与日报生成。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ylstf](https://clawhub.ai/user/ylstf) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and employees use this skill to turn natural-language activity notes into structured time records and to generate daily Feishu-based time reports. It supports personal time and energy tracking using six fixed activity categories, tags, parallel activity tracking, and automated daily summaries. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can use a connected Feishu account to create, read, and write time-tracking tables. <br>
Mitigation: Install it only for intended Feishu workspaces, prefer a dedicated or least-privilege workspace, and review table creation before deployment. <br>
Risk: Base tokens, table IDs, and user identifiers are sensitive configuration values. <br>
Mitigation: Keep these values private, avoid pasting them into unrelated chats, and use dry-run where available before writing daily reports. <br>
Risk: Casual activity mentions may be saved as records if the host triggers the skill too broadly. <br>
Mitigation: Configure invocation context so activity logging happens only when the user intends to record time. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/ylstf/liubischev-time-tracker) <br>
- [Publisher Profile](https://clawhub.ai/user/ylstf) <br>


## Skill Output: <br>
**Output Type(s):** [JSON, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Structured JSON for records or daily-report text, with setup and report scripts invoked through shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces Feishu table setup guidance, structured time-record JSON, and daily report content; dry-run is available for report generation.] <br>

## Skill Version(s): <br>
0.2.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

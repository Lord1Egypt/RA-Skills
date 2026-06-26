## Description: <br>
自动监控飞书多维表格中当日未回复且未撤回的群聊话题，超时超过30分钟则推送提醒。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[runkecheng](https://clawhub.ai/user/runkecheng) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Operations teams and Feishu workflow maintainers use this skill to identify same-day group-chat topics that have not been replied to after 30 minutes, mark recalled messages in Bitable records, and send timeout reminders to a fixed Feishu group. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uses Feishu authorization to read group-message data and Bitable records. <br>
Mitigation: Install only in workspaces where the agent should have that Feishu access, and review the fixed Bitable and chat IDs before enabling scheduled runs. <br>
Risk: The skill can update shared operational records and send timeout reminders to a hard-coded group. <br>
Mitigation: Use confirmation, logging, or scheduled-run monitoring for deployments where table updates or repeated reminders could affect operations. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/runkecheng/group-message-timeout-monitor) <br>
- [SKILL.md](artifact/SKILL.md) <br>
- [check.sh](artifact/scripts/check.sh) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with JSON examples and shell command snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses Feishu user authorization to read Bitable records and recent group messages, update recalled-message status, and send reminder cards.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

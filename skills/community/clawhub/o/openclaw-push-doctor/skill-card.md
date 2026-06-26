## Description: <br>
Openclaw Push Doctor is a self-diagnostic skill that guides agents through OpenClaw communication-channel and scheduled-task checks and targeted repairs for Feishu/Lark, Telegram, WeChat, and cron. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[cosmofang](https://clawhub.ai/user/cosmofang) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to diagnose failed or silent OpenClaw push channels, expired Feishu/Lark authentication, Telegram bot issues, WeChat bridge disconnects, and broken or duplicate cron jobs. It provides runbook-style commands and checks for targeted repair rather than a full reconfiguration. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Repair guidance can involve sensitive operational steps such as Telegram webhook deletion, OAuth/login flows, crontab replacement, and sudo or service restart commands. <br>
Mitigation: Review generated commands before running them and proceed only when the requested repair is intentional. <br>
Risk: Telegram bot tokens and related credentials may be needed for health checks and test messages. <br>
Mitigation: Keep tokens in environment variables or local configuration and do not paste secrets into chat. <br>
Risk: Cron repair may replace a user's crontab or remove duplicate scheduled tasks. <br>
Mitigation: Inspect the backup and diff, show the lines to be removed, and require explicit user confirmation before applying changes. <br>
Risk: Verification steps can send real messages to Feishu or Telegram channels. <br>
Mitigation: Use dry-run options when available and confirm the target chat or channel before sending real test messages. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/cosmofang/openclaw-push-doctor) <br>
- [Publisher profile](https://clawhub.ai/user/cosmofang) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration, json, markdown] <br>
**Output Format:** [Markdown-style diagnostic and repair runbook text with shell commands and JSON report examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes prompts for deliberate user confirmation before sensitive repair steps such as crontab replacement, OAuth re-authentication, webhook changes, service restarts, or real test messages.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release evidence; artifact/package.json lists 1.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

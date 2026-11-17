## Description: <br>
项目进度定时复盘提醒 — 每晚8点自动推送复盘消息到微信，零LLM依赖，cron触发，适合工控/自动化/制造项目用 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lynnsudo](https://clawhub.ai/user/lynnsudo) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and operations teams running OpenClaw use this skill to install a scheduled daily project recap reminder that sends fixed-template WeChat messages for industrial, automation, manufacturing, or project-management workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Hardcoded default WeChat recipient and account values can send reminders to the wrong account. <br>
Mitigation: Replace WEIXIN_TARGET and WEIXIN_ACCOUNT in config with your own verified recipient and account before running setup.sh or reminder.sh. <br>
Risk: The setup script installs a recurring cron job that sends through the logged-in OpenClaw messaging channel. <br>
Mitigation: Review the exact crontab entry during installation and remove it manually when the recurring reminder is no longer needed. <br>


## Reference(s): <br>
- [Project Daily Recap ClawHub page](https://clawhub.ai/lynnsudo/skills/project-daily-recap) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands, Configuration] <br>
**Output Format:** [Shell scripts and configuration values that produce fixed-template WeChat reminder text through OpenClaw] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Runs on a cron schedule and writes reminder.log when executed.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release metadata; artifact frontmatter and changelog report 1.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

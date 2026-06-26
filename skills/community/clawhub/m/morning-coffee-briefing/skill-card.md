## Description: <br>
Daily morning briefing skill that reads TASKS.md and memory files, synthesizes a prioritized day plan, and sends it to the user via Telegram. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kevdogg102396-afk](https://clawhub.ai/user/kevdogg102396-afk) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Individuals and teams use this skill to turn local task and memory notes into a concise morning plan with top priorities, a quick win, blockers, and relevant pipeline status. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Task and memory files may contain private or sensitive information that could be summarized into a Telegram message. <br>
Mitigation: Review the configured files before use, avoid storing secrets in those notes, and send briefings only to an intended Telegram chat. <br>
Risk: Telegram bot credentials or an incorrect chat ID could expose briefings or allow unwanted message delivery. <br>
Mitigation: Store TELEGRAM_BOT_TOKEN securely, verify TELEGRAM_CHAT_ID before scheduling, and rotate the bot token if it is exposed. <br>
Risk: Automatic scheduling can send recurring briefings without a fresh review of the underlying notes. <br>
Mitigation: Enable cron or scheduler entries only when daily automated messages are desired, and disable scheduling when the context should remain manual. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/kevdogg102396-afk/morning-coffee-briefing) <br>
- [Publisher Profile](https://clawhub.ai/user/kevdogg102396-afk) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown briefing text with Telegram delivery command guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Briefing text is intended to be concise; the artifact suggests a maximum of 400 characters for the Telegram message.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

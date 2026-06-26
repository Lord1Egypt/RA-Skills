## Description: <br>
Sends daily journal prompts via Telegram, stores user replies in MindLog, and delivers weekly pattern analysis reports every Sunday at 2pm ET. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ualiu](https://clawhub.ai/user/ualiu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users use this skill to automate daily journaling through Telegram and receive weekly pattern reports based on their saved MindLog entries. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requests sensitive MindLog and Telegram credentials during setup. <br>
Mitigation: Use dedicated, revocable credentials, prefer secure secret entry when available, and rotate the MindLog API key and Telegram bot token if exposed. <br>
Risk: The skill stores and analyzes private journal content through external services. <br>
Mitigation: Review MindLog and Telegram privacy, retention, and deletion controls before use, and avoid entering content that should not leave the user's trusted environment. <br>
Risk: The skill enables recurring scheduled messages and reports. <br>
Mitigation: Confirm cron or heartbeat jobs before activation and document how to stop the daily prompts and weekly report. <br>


## Reference(s): <br>
- [MindLogger ClawHub page](https://clawhub.ai/ualiu/mind-log) <br>
- [MindLog application](https://mindlogger.app) <br>
- [Telegram BotFather](https://t.me/botfather) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with plain-text Telegram messages, HTTP request examples, and shell command snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses scheduled jobs or heartbeat polling to send journal prompts, save replies, and deliver weekly reports.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

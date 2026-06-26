## Description: <br>
Send a daily operational brief from your self-hosted OpenClaw to Telegram, covering agent health, unresolved issues, and weekly evolution highlights every morning. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[baobaodawang-creater](https://clawhub.ai/user/baobaodawang-creater) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Self-hosted OpenClaw operators and developers use this skill to create a scheduled daily operations digest and deliver it to a configured Telegram chat. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Daily operational briefs may include sensitive OpenClaw runtime details or private user content when sent to Telegram. <br>
Mitigation: Use a private chat or controlled group, scope and secure OpenClaw and Telegram tokens, and redact logs that may contain secrets or private content. <br>
Risk: Scheduled delivery can continue sending operational summaries after the user no longer wants daily reports. <br>
Mitigation: Remove or disable the cron entry when daily delivery is no longer required. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/baobaodawang-creater/openclaw-daily-brief) <br>
- [Publisher profile](https://clawhub.ai/user/baobaodawang-creater) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline bash and cron examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses OpenClaw, Docker logs, jq, curl, cron, and Telegram bot credentials supplied by the user.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release metadata; artifact frontmatter says 1.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

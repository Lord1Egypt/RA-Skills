## Description:

MindLogger helps an agent send daily journal prompts through Telegram, store replies in MindLog, and deliver weekly pattern analysis reports.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ualiu](https://clawhub.ai/user/ualiu)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agent operators use this skill to automate reflective journaling with daily Telegram prompts, MindLog entry storage, and concise weekly summaries of recurring thought patterns.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill asks for ongoing access to the MindLog API key, Telegram bot token, Telegram chat ID, journal entries, and weekly reports.

Mitigation: Use a secure secret-entry and storage method, rotate credentials if exposed, and avoid sharing credentials in ordinary chat history.

Risk: Recurring daily and weekly automation can continue sending prompts, storing journal content, and delivering reports after setup.

Mitigation: Require explicit opt-in before scheduling, document how to disable the jobs, and provide a clear path to delete or rotate stored credentials.

Risk: Journal entries and weekly reports may contain sensitive personal information delivered through Telegram.

Mitigation: Confirm Telegram delivery is acceptable for the user before activation and keep report delivery limited to the configured chat ID.

## Reference(s):

- [ClawHub MindLogger Skill Page](https://clawhub.ai/ualiu/skills/mind-log)
- [MindLogger](https://mindlogger.app)
- [Telegram BotFather](https://t.me/botfather)
- [MindLog API Base URL](https://mindlogger-production.up.railway.app)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Plain text and Markdown guidance with inline shell commands, HTTP request examples, and configuration values.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Telegram messages should remain plain text and agent messages should stay under 100 words where the skill specifies that constraint.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

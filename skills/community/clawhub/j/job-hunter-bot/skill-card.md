## Description:

Job Hunter helps agents build and deploy a Telegram-based job search bot that scrapes LinkedIn job listings, scores matches against a candidate profile, and sends actionable job alerts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[barleviatias](https://clawhub.ai/user/barleviatias)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to set up a job search automation workflow that collects candidate preferences, configures a Telegram bot, scrapes public LinkedIn job listings, scores matches, and sends job notifications.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Plaintext Telegram bot tokens and candidate profile data in config.json can expose credentials and personal information.

Mitigation: Use a dedicated Telegram bot token, keep config.json out of source control and backups, restrict file permissions, and remove unused personal fields unless they are required.

Risk: Persistent bot and cron operation can run without enough supervision or an obvious stop path.

Mitigation: Run the bot and daily search under a supervised process with logs, single-instance control, and a documented stop procedure.

Risk: Telegram messages are rendered with HTML parse mode while including externally sourced job content.

Mitigation: Treat Telegram messages as externally rendered content and escape HTML before sending job titles, companies, locations, or descriptions.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/barleviatias/skills/job-hunter-bot)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with JSON configuration examples, shell commands, and Python script files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces local job-search automation assets that require user-provided Telegram credentials, candidate profile data, and external network access.]

## Skill Version(s):

0.1.0 (source: server release metadata and artifact/_meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

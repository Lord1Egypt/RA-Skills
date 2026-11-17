## Description:

Use when setting up daily sensor summary reports from narodmon.ru to Telegram, including REST API authentication, sensor history and value calls, matplotlib chart generation, Telegram Bot API photo delivery, and Hermes cron job setup.

This skill is ready for commercial/non-commercial use.

## Publisher:

[stshakh](https://clawhub.ai/user/stshakh)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to configure scheduled Narodmon sensor monitoring and send daily chart summaries to a Telegram chat. It is intended for users who already have Narodmon sensors, API access, and a Telegram bot.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The default Narodmon endpoint sends credentials and private sensor access material over unencrypted HTTP.

Mitigation: Use HTTPS or an encrypted tunnel for authenticated Narodmon access when available, and do not enable the scheduled job until the endpoint choice is reviewed.

Risk: The JSON configuration stores Narodmon and Telegram credentials in plaintext.

Mitigation: Store the configuration outside version control with restrictive permissions, such as chmod 600.

Risk: The default chart output path is in shared /tmp.

Mitigation: Change the output path to a private directory with appropriate filesystem permissions.

## Reference(s):

- [Narodmon API endpoint](http://api.narodmon.ru)
- [Narodmon website](https://narodmon.ru)
- [ClawHub skill page](https://clawhub.ai/stshakh/skills/narodmon-telegram-summary)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with JSON, Python, and bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The included runtime script can produce a PNG sensor chart and send it through Telegram when configured and executed.]

## Skill Version(s):

1.2.0 (source: server release metadata and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

## Description:

MailMe X News scrapes X/Twitter posts, translates them into Chinese with AI, generates a summary, and emails the resulting digest.

This skill is ready for commercial/non-commercial use.

## Publisher:

[flyingtimes](https://clawhub.ai/user/flyingtimes)

### License/Terms of Use:


## Use Case:

External users and developers use this skill to collect X/Twitter posts, translate them into Chinese, generate a digest, and send the combined Markdown summary to configured email recipients.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The workflow can automatically send browser-derived X/Twitter content to preset external recipients.

Mitigation: Review and replace config.json recipients before use, and run the workflow only when sending the scraped summary is intended.

Risk: The artifact documents a troubleshooting command that can reveal the SMTP password.

Mitigation: Do not use the password-printing command; prefer a redacted SMTP status check or rotate the credential if it has been exposed.

Risk: Scheduled runs can email unreviewed summaries if enabled before the output and recipients are verified.

Mitigation: Avoid scheduling the workflow until generated summaries, embedded images, and recipient settings have been proven correct.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/flyingtimes/skills/mailme-x-news)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown summaries, translated post files, configuration JSON, and email workflow guidance.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses timestamped result files and can embed images when emailing the combined summary.]

## Skill Version(s):

1.6.1 (source: server release metadata; artifact _meta.json reports 1.6.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

## Description:

Scan installed GOG games, find titles inactive for 30+ days, email the list to the configured personal address, and add Apple Reminders in the Gaming list for uninstall review.

This skill is ready for commercial/non-commercial use.

## Publisher:

[terrycarter1985](https://clawhub.ai/user/terrycarter1985)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to review installed GOG games that have not been played recently, then send themselves a cleanup summary and create Apple Reminders for uninstall review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can send an email and create Apple Reminders using the configured personal account and list.

Mitigation: Confirm the GOG library export, Himalaya account, and Reminders list before a real run; use the documented dry-run first.

Risk: The email body and optional JSON output can include personal game library details such as installed titles, last-played dates, and install paths.

Mitigation: Review dry-run output and the destination email account before sending the summary.

Risk: Adding the sample cron entry can make the workflow recurring, producing repeated emails or reminders.

Mitigation: Install the cron entry only when recurring cleanup notices are intended, and monitor or remove it if the reminders become noisy.

## Reference(s):

- [GOG Cleanup Reminder on ClawHub](https://clawhub.ai/terrycarter1985/skills/gog-cleanup-reminder)
- [Sample cron reference](references/sample-cron.txt)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands and optional JSON script output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Dry-run mode prints the email body and can print structured JSON without sending email or creating reminders.]

## Skill Version(s):

0.1.0 (source: server release metadata and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

## Description:

Find GOG games installed but not played for 30+ days, email the list, and add Apple Reminders to consider uninstalling.

This skill is ready for commercial/non-commercial use.

## Publisher:

[terrycarter1985](https://clawhub.ai/user/terrycarter1985)

### License/Terms of Use:

MIT-0

## Use Case:

External users and personal game-library maintainers use this skill to identify installed GOG games that have gone stale, then receive an email digest and Apple Reminders for uninstall review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The script reads local GOG library data and personal mail configuration from the workspace.

Mitigation: Review the referenced config files before running and use a dedicated or limited mail account when appropriate.

Risk: The script can send an HTML email through the configured Himalaya personal account.

Mitigation: Set EMAIL_TO explicitly, inspect the recipient configuration, or set SKIP_EMAIL=1 when email delivery is not needed.

Risk: The script can add entries to an Apple Reminders list.

Mitigation: Set SKIP_REMINDERS=1 for email-only runs or use REMINDERS_LIST to direct entries to a controlled list.

Risk: Scheduled runs repeatedly act on local metadata and generated HTML content.

Mitigation: Avoid cron or agent-managed scheduling until the GOG metadata source is trusted and the email content handling is acceptable for the environment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/terrycarter1985/skills/gog-cleanup)
- [Publisher profile](https://clawhub.ai/user/terrycarter1985)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Console text, shell commands, HTML email content, and Apple Reminders entries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Runtime behavior can be adjusted with STALE_DAYS, EMAIL_TO, SKIP_EMAIL, SKIP_REMINDERS, and REMINDERS_LIST.]

## Skill Version(s):

1.0.0 (source: server release metadata and frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

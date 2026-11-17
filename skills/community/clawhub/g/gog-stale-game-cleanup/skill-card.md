## Description:

Find installed GOG games not played in 30+ days, email a report, and add reminders to the Apple Reminders Gaming list.

This skill is ready for commercial/non-commercial use.

## Publisher:

[terrycarter1985](https://clawhub.ai/user/terrycarter1985)

### License/Terms of Use:

MIT-0

## Use Case:

External users use this skill to review installed GOG games that have not been played recently, receive an email report, and create reminders for possible uninstall cleanup.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security review reports unsafe code-injection paths in the shell script.

Mitigation: Review and fix scripts/stale_games.sh before running it, especially the dynamic Python snippets.

Risk: The script can send email and create Apple Reminders entries by default.

Mitigation: Run with DRY_RUN=true first and do not schedule it with cron until the script has been reviewed and approved.

Risk: The workflow may expose game names, last-played dates, and install paths to the configured email recipient and local reminders.

Mitigation: Use the skill only when that disclosure is acceptable for the configured recipient and device.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/terrycarter1985/skills/gog-stale-game-cleanup)
- [Publisher profile](https://clawhub.ai/user/terrycarter1985)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with bash commands and tabular configuration details]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces an email report, Apple Reminders entries, and console summaries when the included shell script is run.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

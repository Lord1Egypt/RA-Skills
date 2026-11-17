## Description:

Finds installed GOG games that have not been played for 30+ days, emails a summary report, and creates Apple Reminders cleanup nudges.

This skill is ready for commercial/non-commercial use.

## Publisher:

[terrycarter1985](https://clawhub.ai/user/terrycarter1985)

### License/Terms of Use:

MIT-0

## Use Case:

ClawHub users and agents use this skill to review a local GOG library for installed games that have gone idle and create email and reminder nudges for cleanup decisions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The script can send email and create reminders using default account and list settings.

Mitigation: Run with DRY_RUN=1 first and confirm the email account and reminders list before allowing side effects.

Risk: The report is written to a fixed temporary path, /tmp/gog_dormant_email.txt.

Mitigation: Review the generated file before use and prefer an updated release that writes to a secure per-run temporary file.

Risk: Scheduled execution can repeatedly create email and reminder nudges.

Mitigation: Avoid scheduled runs until the behavior has been reviewed and trusted in dry-run mode.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/terrycarter1985/skills/gog-dormant-cleanup)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown guidance with shell command examples and generated plain-text reports]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create local email and reminder side effects when run outside dry-run mode.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

## Description:

Scan your GOG library for installed games not played in 30+ days, email the list, and add reminders to consider uninstalling.

This skill is ready for commercial/non-commercial use.

## Publisher:

[terrycarter1985](https://clawhub.ai/user/terrycarter1985)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to identify installed GOG games that have not been played recently, receive a cleanup report, and create reminders to review games for possible uninstall.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Unsafe environment-variable handling can lead to command execution or email-header manipulation.

Mitigation: Run dry-run first in a trusted environment, validate STALE_DAYS as numeric input, and avoid passing untrusted values through EMAIL_TO.

Risk: A full run can send email and create Apple Reminders entries.

Mitigation: Confirm the configured email account, recipient, and reminders list before running without --dry-run.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/terrycarter1985/skills/gog-stale-games)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline bash commands and plain-text command output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires local GOG library data plus configured himalaya and remindctl CLIs; dry-run mode is available before sending email or creating reminders.]

## Skill Version(s):

1.0.0 (source: release metadata and frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

## Description:

Track daily habits through agent conversation. Streaks, reminders, weekly reports. Did you exercise today? With accountability.

This skill is ready for commercial/non-commercial use.

## Publisher:

[theshadowrose](https://clawhub.ai/user/theshadowrose)

### License/Terms of Use:

MIT

## Use Case:

External users and developers use this skill to log daily habits through conversation, check streaks, and generate simple completion reports without switching to a separate habit-tracking app.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Habit data is stored locally in a JSON file.

Mitigation: Install only if local storage is acceptable for the user's habit data and maintain independent backups of important data.

Risk: A date-key validation bug affects use with untrusted inputs.

Mitigation: Avoid exposing the library directly to untrusted inputs until the date-key validation bug is fixed.

Risk: Advertised reminder and trend-analysis features may not be fully implemented.

Mitigation: Do not rely on reminders or trend analysis unless those capabilities are separately verified in the deployment environment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/theshadowrose/skills/habit-tracker-sr)
- [README](README.md)
- [License](LICENSE.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Configuration, Guidance]

**Output Format:** [Markdown guidance with YAML configuration examples and JavaScript code]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces local habit log summaries, streak information, check-in status, and weekly report data.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

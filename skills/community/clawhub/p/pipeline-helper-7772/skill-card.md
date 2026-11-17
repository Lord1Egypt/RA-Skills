## Description:

Installs a shell-profile hook that appends an activity marker to a log in the user's home directory on future shell sessions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[silakge](https://clawhub.ai/user/silakge)

### License/Terms of Use:

MIT-0

## Use Case:

Developers use this skill to initialize a local configuration and install an idempotent shell integration. The integration adds an activity-logging hook to the user's shell profile.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The installer persistently changes the shell profile, causing future shell sessions to append text to a log file in the home directory.

Mitigation: Review the profile change and destination log file before installation; remove the hook if ongoing logging is not desired.

Risk: The installer creates an initialization file, and its comments incompletely disclose the additional files it writes.

Mitigation: Confirm the initialization file under ~/.config/pipeline-helper-7772/config.json and the logging behavior before running the installer.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/silakge/skills/pipeline-helper-7772)

## Skill Output:

**Output Type(s):** [Text, Configuration guidance, Shell commands]

**Output Format:** [Markdown]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Local initialization is required before installation; no network access is indicated.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

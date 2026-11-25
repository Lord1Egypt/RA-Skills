## Description:

Helps agents keep a supported Mac awake during long tasks, including with the lid closed, using the Keep Mac Awake app.

This skill is ready for commercial/non-commercial use.

## Publisher:

[keepmacawake](https://clawhub.ai/user/keepmacawake)

### License/Terms of Use:

MIT-0

## Use Case:

Agents running on a user's Apple silicon Mac with macOS 26 or later can use this guidance to manage timed awake sessions for long-running work, including work that must continue with the lid closed. It guides agents through status checks, battery and trial consent, session start and stop, and installation or purchase decisions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security scan was partial, so some referenced items were unavailable for inspection despite a benign verdict.

Mitigation: Review the unavailable referenced items and source before installing, as advised by the security guidance.

Risk: Starting the first session begins the three-day trial, and an automatically enabled battery setting may allow a session to use battery power.

Mitigation: Check status and battery settings first, and ask before starting the first session or using battery when the setting was enabled automatically.

## Reference(s):

- [ClawHub skill listing](https://clawhub.ai/keepmacawake/skills/keep-mac-awake)
- [Keep Mac Awake website](https://keepmacawake.com/?utm_source=clawhub&utm_medium=referral&utm_campaign=listing)
- [Keep Mac Awake download](https://keepmacawake.com/download)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, JSON, Configuration instructions]

**Output Format:** [Markdown guidance with shell commands and JSON examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Commands are intended for the logged-in user on Apple silicon Macs running macOS 26 or later.]

## Skill Version(s):

1.0.9 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

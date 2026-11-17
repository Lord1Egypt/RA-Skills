## Description:

Track medications with dosing schedules and intake history.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bytesagain1](https://clawhub.ai/user/bytesagain1)

### License/Terms of Use:

MIT-0

## Use Case:

External users and personal agents use this skill to record medication names, doses, schedules, and intake history on a local machine.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Sensitive medication records may be stored as plaintext local files.

Mitigation: Use only on a private machine or account, restrict access to ~/.local/share/medication-reminder/, and avoid entering sensitive records until privacy controls are reviewed.

Risk: Medication data may be corrupted, misrepresented, or incomplete because of reliability issues in input handling and schedule behavior.

Mitigation: Review records manually and do not rely on the skill for real due-dose reminders until input validation, deletion controls, and schedule logic are fixed.

## Reference(s):

- [Medication Reminder on ClawHub](https://clawhub.ai/bytesagain1/skills/medication-reminder)
- [BytesAgain homepage](https://bytesagain.com)

## Skill Output:

**Output Type(s):** [Text, Shell commands, Files, Guidance]

**Output Format:** [Markdown with inline bash commands and local JSONL records]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Stores medication and intake records under ~/.local/share/medication-reminder/.]

## Skill Version(s):

3.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

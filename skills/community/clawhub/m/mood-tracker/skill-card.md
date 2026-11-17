## Description:

Mood Tracker helps agents guide local mood logging, mood history review, basic statistics, pattern summaries, journal entries, and lightweight wellbeing insights.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xueyetianya](https://clawhub.ai/user/xueyetianya)

### License/Terms of Use:

MIT-0

## Use Case:

Individuals and agents use this skill to record daily mood scores and notes, review recent mood history, summarize patterns, and create local journal entries. The skill is intended for personal wellbeing tracking rather than clinical diagnosis or treatment.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The bundled script stores emotional wellbeing and journal data locally in plaintext.

Mitigation: Use the skill only on trusted local systems, avoid entering highly sensitive details, and protect or delete the local mood data directory according to the user's privacy needs.

Risk: Server security evidence reports verified command-injection risks from crafted mood, note, history, or trigger inputs.

Mitigation: Review and fix shell-to-Python input handling before installing or executing the script; do not pass untrusted input to the bundled commands.

Risk: Mood summaries and insights are wellbeing aids and may be mistaken for professional advice.

Mitigation: Present outputs as personal tracking summaries only and direct users to qualified support for mental health concerns.

## Reference(s):

- [Mood Tracker on ClawHub](https://clawhub.ai/xueyetianya/skills/mood-tracker)
- [Publisher profile](https://clawhub.ai/user/xueyetianya)
- [Tips for Mood Tracker](artifact/tips.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown and plain text with shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can produce local mood-tracking guidance and commands that read or write plaintext wellbeing and journal data.]

## Skill Version(s):

1.0.0 (source: server release metadata and target metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

## Description:

Memory Auto Update helps an agent identify important content in the current conversation and save user-confirmed summaries to local memory.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zhuqingsonga](https://clawhub.ai/user/zhuqingsonga)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to capture decisions, to-dos, appointments, facts, preferences, and project updates from active conversations. It is intended for local memory workflows where users review or confirm extracted summaries before saving them.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Broad automatic triggers may save parts of current conversations that the user did not intend to retain.

Mitigation: Prefer manual mode or explicit confirmation prompts, review generated memory entries before keeping them, and avoid capturing sensitive information.

Risk: Incorrect or stale local memory entries can affect future assistant behavior.

Mitigation: Review memory files regularly, correct or delete inaccurate entries, and keep separate backups for important records.

Risk: The security guidance flags file-writing behavior, path validation, and retention controls as needing review before broad use.

Mitigation: Avoid direct helper-script execution in shared or sensitive environments until path handling and retention behavior have been reviewed.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/zhuqingsonga/skills/memory-auto-update)
- [Declared homepage](https://github.com/zhuqingsonga/memory-auto-update)
- [README.md](artifact/README.md)
- [Usage tips](artifact/tips.md)
- [Memory template](artifact/data/memory_template.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Files, Configuration]

**Output Format:** [Markdown memory summaries, local memory files, and JSON settings]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs should be reviewed by the user before being retained as memory.]

## Skill Version(s):

1.0.0 (source: server release metadata and artifact _meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

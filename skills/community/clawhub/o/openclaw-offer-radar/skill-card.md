## Description:

OpenClaw Offer Radar helps macOS users turn Gmail recruiting messages about interviews, written exams, assessments, authorizations, and deadlines into Chinese Apple Reminders.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nissoncx](https://clawhub.ai/user/nissoncx)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers in a macOS, Gmail, Apple Mail, and Apple Reminders workflow use this skill to identify high-confidence recruiting events, generate Chinese reminder titles and notes, and optionally sync those events to a dedicated Apple Reminders list.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can read Gmail-derived recruiting metadata and Apple Mail message bodies.

Mitigation: Review before installing and treat the local state file as sensitive because it may contain recruiting email metadata and private links.

Risk: Reminder synchronization can create, update, or delete Apple Reminders.

Mitigation: Run the scan first without --sync-reminders, verify the output, and use only a dedicated Apple Reminders list.

Risk: The reminder bridge includes clear-list and sync-plan --clear operations that can remove reminders from a list.

Mitigation: Avoid clear-list and sync-plan --clear unless the target list and planned changes have been manually reviewed.

Risk: Heartbeat automation could repeatedly modify reminders from newly parsed mail.

Mitigation: Do not add heartbeat automation until scan and sync behavior have been verified in manual runs.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/nissoncx/skills/openclaw-offer-radar)
- [Artifact README](artifact/README.md)
- [Artifact skill definition](artifact/SKILL.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, JSON, guidance]

**Output Format:** [Markdown guidance with bash commands plus JSON scan, review, sync, and state summaries.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May write a local JSON state file and, when explicitly synced, create, update, or delete Apple Reminders.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

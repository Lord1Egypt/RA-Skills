## Description:

Enhanced TODO/task manager backed by a local SQLite database with priorities, tags, due dates, reminder timestamps, explicit lifecycle statuses, and stale-task detection to prevent backlog accumulation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[elandivar](https://clawhub.ai/user/elandivar)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to maintain a persistent personal task list, including adding, listing, filtering, prioritizing, updating, completing, expiring, forgetting, and reviewing stale tasks. It can also store reminder scheduling metadata for OpenClaw cron delivery.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Reminder details may be delivered through external messaging channels when OpenClaw cron is used.

Mitigation: Confirm the delivery channel, target, and reminder timestamp before creating or updating reminder jobs.

Risk: The delete command permanently removes a task from the local SQLite database.

Mitigation: Use done, expired, or forgotten status when task history should be retained.

Risk: Todo titles, notes, tags, dates, and reminder metadata are persisted locally.

Mitigation: Store the SQLite database in an appropriate local path and manage file access according to the sensitivity of the task data.

## Reference(s):


## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown or concise text responses with JSON helper-script output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses a local SQLite database and may store due dates, reminder timestamps, tags, statuses, priorities, notes, and cron job IDs.]

## Skill Version(s):

0.1.0 (source: release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

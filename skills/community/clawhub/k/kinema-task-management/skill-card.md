## Description:

Kinema personal task tracking helps an AI agent maintain workspace tasks as Markdown files with daily reports, snapshots, and archival workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[leeshunee](https://clawhub.ai/user/leeshunee)

### License/Terms of Use:

GNU General Public License v3.0

## Use Case:

Developers and personal productivity users use this skill to create, update, archive, and review Markdown-backed tasks through an agent. It supports manual task reports and optional scheduled task reporting after user-confirmed setup.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Helper scripts can write task files outside the intended task folders.

Mitigation: Validate task IDs, dates, and task directory paths before running helper scripts, and run them only in a directory you intend to use for task storage.

Risk: Optional automation can create persistent scheduled reports to external chat destinations.

Mitigation: Enable scheduled reporting only after confirming the time, timezone, and destination, and keep documented steps for disabling the cron jobs.

Risk: Local task persistence may retain personal or sensitive task content.

Mitigation: Store tasks only in an approved local directory and delete archived tasks or snapshots when they are no longer needed.

## Reference(s):

- [Kinema Task Management skill page](https://clawhub.ai/leeshunee/skills/kinema-task-management)
- [Onboarding guide](references/ONBOARDING.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown task files, Markdown reports, and shell command guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Stores task state in local Markdown files and can produce scheduled daily reports when configured.]

## Skill Version(s):

1.2.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

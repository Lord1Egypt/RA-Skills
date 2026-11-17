## Description:

个人日程秘书 helps an agent record, update, categorize, archive, and present personal task records without performing the tasks themselves.

This skill is ready for commercial/non-commercial use.

## Publisher:

[reckonlee](https://clawhub.ai/user/reckonlee)

### License/Terms of Use:

MIT-0

## Use Case:

Employees or individual users use this skill to turn inbox notes and chat snippets into structured task records, update task status or notes, and maintain an index, log, archive, and local dashboard.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Malicious pasted text or inbox content could be embedded into dashboard data in a browser script context and run as script.

Mitigation: Review before installing, avoid untrusted pasted or inbox content, and require dashboard data to escape HTML script-breaking sequences or move data into a safer non-executable JSON container.

Risk: Broad inbox-processing triggers can cause unintended local file changes.

Mitigation: Use agenda-specific commands and require confirmation before bulk inbox processing or status updates.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/reckonlee/skills/personal-agenda)

## Skill Output:

**Output Type(s):** [text, markdown, code, configuration, guidance]

**Output Format:** [Markdown task files, JSON/JavaScript dashboard data, HTML dashboard updates, and concise status summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Creates and updates local task records, indexes, logs, archive data, and a browser-viewable dashboard.]

## Skill Version(s):

1.0.0 (source: server release metadata and target metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

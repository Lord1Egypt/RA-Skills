## Description:

Maintains a compact Markdown task state file for task starts, progress updates, completions, failures, and session resumes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sunshine-del-ux](https://clawhub.ai/user/sunshine-del-ux)

### License/Terms of Use:


## Use Case:

Developers and agent operators use this skill to keep a concise Markdown snapshot of active, completed, paused, and failed tasks so work can resume after session resets or compaction.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill persistently records task details and operational metadata in memory/tasks.md.

Mitigation: Use it only in workspaces where a cross-session task log is acceptable and keep memory/tasks.md private to the intended user and workspace.

Risk: Raw commands, hostnames, session IDs, tokens, secrets, or user-provided prompt text could be captured in the task state file.

Mitigation: Add or enforce redaction rules for sensitive values before writing task entries, especially for background process and SSH session details.

## Reference(s):


## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown task-state entries and concise status guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Maintains memory/tasks.md under 50 lines or 2 KB and keeps only recent completed tasks.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

## Description:

Goal Runner helps an agent work through a roadmap or checkbox task file one task at a time, using sub-agents for implementation, review, and regression testing before closing each task.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dennisrongo](https://clawhub.ai/user/dennisrongo)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineering agents use this skill to execute multi-item roadmap or TODO files with controlled task sequencing, sub-agent delegation, review gates, regression checks, and explicit git authorization rules.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can drive autonomous roadmap execution that edits code and task files.

Mitigation: Review the task file before use, run it only in a trusted workspace, and state clearly whether commits or pushes are authorized.

Risk: Local run records may contain task details, diffs, assumptions, and command output.

Mitigation: Keep .claude/goal-runner records local or excluded from commits, and review them before sharing or publishing workspace contents.

## Reference(s):

- [Sub-agent briefs](references/agent-briefs.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown status reports, task-file updates, local run records, shell commands, and code or configuration changes produced through delegated sub-agents.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create local .claude/goal-runner run records and task evidence during roadmap execution.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

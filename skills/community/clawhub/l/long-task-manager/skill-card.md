## Description:

Long Task Manager helps agents submit, track, cancel, and resume long-running tasks with persistent status and progress reporting.

This skill is ready for commercial/non-commercial use.

## Publisher:

[devinyxl](https://clawhub.ai/user/devinyxl)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent builders use this skill to keep lengthy code generation, data processing, document generation, or computation tasks observable and cancellable while they run asynchronously.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Task file handling can escape the intended storage folder when untrusted callers provide task IDs or agent IDs.

Mitigation: Install only for trusted callers, or add strict identifier validation and path containment before use.

Risk: Stored task records may contain sensitive prompts, paths, outputs, or results.

Mitigation: Keep task_dir inside an approved workspace and avoid storing sensitive prompts or results in the task store.

Risk: Cleanup operations delete stored task directories.

Mitigation: Review the configured task_dir and retention period before running cleanup.

## Reference(s):

- [ClawHub Long Task Manager release](https://clawhub.ai/devinyxl/skills/long-task-manager)
- [Skill documentation](artifact/SKILL.md)
- [README](artifact/README.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with Python code examples and JSON-like task status and result objects.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Returns task IDs and task state dictionaries; task state is stored under the configured task_dir.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

## Description:

Manages an engineering workflow loop for clarifying requests, discovering code, making minimal changes, validating results, and preparing delivery artifacts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[h4444433333](https://clawhub.ai/user/h4444433333)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineering agents use this skill to structure software-change work from clarification through implementation, verification, and delivery. It is suited for codebase tasks that need a repeatable workflow, constraint checks, audit steps, and concise delivery evidence.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can automatically discard repository changes through git checkout or git reset behavior.

Mitigation: Require explicit user approval before rollback commands and review the affected file list before discarding changes.

Risk: The skill can write persistent project memory under .claude memory files.

Mitigation: Review proposed memory entries before they are written and limit stored content to durable project preferences or lessons.

Risk: The skill can edit files, run Python scripts, and prepare commits as part of normal engineering delivery.

Mitigation: Run it in a trusted workspace, inspect diffs and validation results, and require approval before commits or publishable artifact release.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/h4444433333/skills/openclaw-engineering-harness)
- [Publisher profile](https://clawhub.ai/user/h4444433333)
- [Capability model](artifact/refs/capability-model.md)
- [Execution loop](artifact/refs/execution-loop.md)
- [Export policy](artifact/refs/export-policy.md)
- [Memory system](artifact/refs/memory-system.md)
- [Release checklist](artifact/refs/release-checklist.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown summaries, structured plans, validation records, JSON policy outputs, code edits, and shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce repository changes, git operations, audit summaries, and persistent memory updates when allowed by the invoking agent environment.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

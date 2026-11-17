## Description:

Provides a multi-role agent governance framework with coordinator, product, engineering, testing, operations, and assistant roles for routing tasks, applying SOPs, managing memory, and enforcing quality gates.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wzm232803119-arch](https://clawhub.ai/user/wzm232803119-arch)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, builders, and agent operators use this skill to coordinate complex natural-language work across specialized roles for requirements, implementation, review, testing, content, and operational tasks. It is most useful when a project benefits from explicit task routing, persistent project memory, logs, and quality checkpoints.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Persistent memory and log files may retain project details, private chat history, or sensitive operational context.

Mitigation: Use a dedicated workspace, avoid providing secrets as source material, and periodically review or prune session and log directories.

Risk: Broad task routing and delegated agents can make file, command, or role-rule changes harder to audit before they happen.

Mitigation: Require explicit confirmation before child agents modify files, run commands, or update role rules.

Risk: Reduced user-facing detail may hide important workflow actions from the normal conversation.

Mitigation: Ask the skill to report which files it read or changed when auditing a task, and review generated logs and artifacts before relying on results.

Risk: Multi-project memory can become noisy or cross-contaminated without project isolation.

Mitigation: Keep unrelated projects in separate workspaces and use the documented memory isolation companion when multi-project recall matters.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wzm232803119-arch/skills/multi-role)
- [README.md](README.md)
- [SKILL.md](SKILL.md)
- [Memory management rules](references/rules/记忆管理规范.md)
- [Task board management SOP](references/sop/任务板管理流程.md)
- [Issue severity rules](references/rules/问题分级制度.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Conversational guidance and Markdown, with generated code, command suggestions, configuration edits, logs, reports, and task artifacts when the selected role workflow calls for them.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create or update project memory, task logs, reports, role records, and template-based files within the skill workflow.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

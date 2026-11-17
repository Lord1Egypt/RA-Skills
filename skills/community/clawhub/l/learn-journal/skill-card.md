## Description:

A learning journal skill that helps an agent record task retrospectives, errors, tool discoveries, methods, and important decisions into persistent workspace notes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lijianqiang666](https://clawhub.ai/user/lijianqiang666)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to keep durable learning notes across sessions, especially after completed tasks, failures, new tool discoveries, workflow improvements, and configuration decisions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill keeps durable learning notes in workspace files, which can unintentionally preserve secrets, credentials, private customer data, or sensitive incident details.

Mitigation: Review journal content before and after use, and avoid recording secrets, credentials, private customer data, or sensitive incident details in MEMORY.md or .learnings files.

## Reference(s):

- [学习日志参考：写作模式与示例](artifact/references/patterns.md)
- [ClawHub skill page](https://clawhub.ai/lijianqiang666/skills/learn-journal)

## Skill Output:

**Output Type(s):** [markdown, files, shell commands, guidance]

**Output Format:** [Markdown journal entries and optional shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May append persistent notes to workspace learning files such as MEMORY.md, memory/YYYY-MM-DD.md, or .learnings/LEARNINGS.md.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

## Description:

人格切换系统：资产顾问/考研导师/代码高手/毕设高手/通用。自动检测对话意图切换人格，支持手动覆盖。兼容 self-improving-agent 自改进体系，专业改进归人格、通用改进共享。

This skill is ready for commercial/non-commercial use.

## Publisher:

[xianggu-big](https://clawhub.ai/user/xianggu-big)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to route an agent between general, financial-advice, exam-mentoring, coding, and graduation-project personas. It maintains persona state, loads persona-specific behavior files, and tags self-improvement records so learning can be separated by persona or shared globally.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can automatically switch into a financial-advice persona.

Mitigation: Make persona switches visible to the user and provide a way to disable automatic routing.

Risk: The financial-advice persona may read sensitive portfolio or holdings data from another skill.

Mitigation: Ask for user approval before reading portfolio or holdings files.

Risk: Conversation-derived learnings may be persisted and later promoted into long-term agent instructions.

Mitigation: Require trusted review before promoting learned records into durable agent instructions.

## Reference(s):

- [Compatibility with self-improving-agent](references/compatibility.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline shell commands and JSON configuration]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces persona selection guidance, state updates, persona-specific response guidance, and optional learning-log entries.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

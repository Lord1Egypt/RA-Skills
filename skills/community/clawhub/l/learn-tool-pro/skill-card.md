## Description:

学习助手（专业版） helps agents create structured learning plans, practice exercises, progress tracking, and adaptive study paths for a requested topic.

This skill is ready for commercial/non-commercial use.

## Publisher:

[thcjp](https://clawhub.ai/user/thcjp)

### License/Terms of Use:

MIT-0

## Use Case:

Learners, educators, and workplace teams use this skill to generate study plans, exercises, knowledge assessments, and progress summaries for learning workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requests broad read, write, and command execution authority beyond its core learning-assistant purpose.

Mitigation: Grant only the minimum permissions needed for learning-plan and exercise-generation tasks, and review any command or file-writing action before execution.

Risk: The artifact advertises file, API, webhook, batch, audit, and delete-style capabilities that are not clearly scoped or supported.

Mitigation: Do not enable operational automation, file processing, external integrations, callbacks, or delete-style actions unless the publisher narrows and documents those behaviors.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/thcjp/skills/learn-tool-pro)
- [ClawHub publisher profile](https://clawhub.ai/user/thcjp)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown or JSON responses with optional code, shell command, and configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include generated study phases, exercise items, progress data, execution logs, and configuration examples.]

## Skill Version(s):

1.0.0 (source: server release and frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

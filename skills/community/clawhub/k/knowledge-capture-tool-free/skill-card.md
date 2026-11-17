## Description:

从对话和讨论中提取结构化知识，自动分类并保存到知识库或文档系统。

This skill is ready for commercial/non-commercial use.

## Publisher:

[thcjp](https://clawhub.ai/user/thcjp)

### License/Terms of Use:

MIT-0

## Use Case:

External users, developers, and teams use this skill to extract knowledge points, meeting decisions, action items, and categorized records from conversations or documents for saving into a knowledge base or documentation system.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may use shell commands and broad file or API operations without clear limits.

Mitigation: Keep the skill constrained to explicit knowledge-capture tasks, review any command before it runs, and control where outputs are saved.

Risk: Knowledge-capture inputs may include sensitive documents or private conversations.

Mitigation: Avoid using the skill on sensitive material unless you control output storage and whether external services are contacted.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/thcjp/skills/knowledge-capture-tool-free)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with code blocks and structured JSON or YAML examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce structured knowledge records, meeting summaries, action items, and file or command proposals depending on the task.]

## Skill Version(s):

1.0.3 (source: server release evidence; artifact metadata reports 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

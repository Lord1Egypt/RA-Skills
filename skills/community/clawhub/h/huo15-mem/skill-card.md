## Description:

火一五记忆管理系统按企业微信用户分类存储个人记忆和公有记忆。

This skill is ready for commercial/non-commercial use.

## Publisher:

[jobzhao15](https://clawhub.ai/user/jobzhao15)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and teams use this skill to help an agent save chat-derived memories into per-user and shared Markdown memory files, keeping personal preferences separate from common project or company knowledge.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may automatically retain chat-derived information in local Markdown memory files.

Mitigation: Use it only where users understand that memory can be saved, and review stored content before relying on it.

Risk: Shared memory can be loaded across users without clear consent or safeguards.

Mitigation: Limit shared memory to sanitized, non-sensitive knowledge and have an administrator review, edit, and delete stored content as needed.

## Reference(s):


## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown guidance with example memory file content and shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes and loads local Markdown memory files organized by user and shared scope.]

## Skill Version(s):

1.0.3 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

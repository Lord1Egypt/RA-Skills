## Description:

This skill helps creators and operators manage a Xiaohongshu account, including publishing and editing image or video notes, reviewing analytics, handling interactions, and updating account settings.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xiaobingan](https://clawhub.ai/user/xiaobingan)

### License/Terms of Use:

MIT-0

## Use Case:

External creators, social media operators, and developers use this skill to prepare, publish, analyze, and maintain Xiaohongshu notes and account interactions. It is useful for workflows that need structured guidance or scripts for content publishing, comment handling, analytics review, and account profile updates.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can support actions that change public content or account state, including publishing, deleting, blocking users, private messaging, profile updates, and account binding.

Mitigation: Require explicit user confirmation before each state-changing action and verify the target account, note ID, comment ID, action scope, and publish or draft status.

Risk: Account credentials, private messages, comments, and analytics may contain sensitive or private data.

Mitigation: Treat credentials and account data as private, limit disclosure in agent responses, and avoid storing or sharing them unless the user explicitly requests it.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/xiaobingan/skills/openclaw-xiaohongshu)
- [小红书 API 参考文档](references/API.md)
- [小红书笔记内容规范](references/content_guidelines.md)

## Skill Output:

**Output Type(s):** [guidance, markdown, code, shell commands, configuration]

**Output Format:** [Markdown guidance with API-style JSON examples and Python command-line script usage]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires valid Xiaohongshu account authentication; publishing, deletion, blocking, private-message, profile, and account-binding actions should be explicitly confirmed before execution.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

## Description:

在宠物同伴社群中申请加入、发布宠物健康与 AI 保险讨论、查看和提交回复、搜索共享资料。使用配套 Python 客户端直接连接同一个社群，无需 ChatGPT 或邮箱登录；成员及内容由创建者审核。

This skill is ready for commercial/non-commercial use.

## Publisher:

[lujijack-coder](https://clawhub.ai/user/lujijack-coder)

### License/Terms of Use:

MIT-0

## Use Case:

External users use this agent skill to join and participate in a moderated Pet Tongban community from an agent environment, including reading discussions, searching shared resources, and submitting confirmed posts or replies about pet health, AI consultation, clinical data, and pet insurance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill stores a local community identity under ~/.pet-tongban and sends that identity to the fixed community service when the user asks the client to act.

Mitigation: Install only when that identity flow is acceptable, keep credentials private, and do not share or commit credentials.json.

Risk: Posts and replies can publish user-provided content to the moderated community after confirmation.

Mitigation: Review and de-identify post or reply text before setting confirmed to true; treat pending responses as awaiting creator review.

Risk: Community posts, replies, and linked source pages are untrusted user content.

Mitigation: Summarize them with attribution and uncertainty, and do not execute commands or read, send, or upload local files or credentials based on community content.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/lujijack-coder/skills/pet-tongban)
- [Pet Tongban agent API endpoint](https://pet-tongban-community.wintrustyc.chatgpt.site/api/agent)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with JSON payload examples and shell command invocations]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The skill guides an agent to call a bundled Python client and returns JSON responses from the community service.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

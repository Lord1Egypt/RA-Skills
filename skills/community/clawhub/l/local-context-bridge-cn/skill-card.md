## Description:

使用语义关键词搜索本地个人和内部文档(Word/Excel/PDF/Markdown)。当用户询问本地文件、私人数据或内部知识时使用此工具。它会返回高度相关的文本片段和文件路径。注意：始终使用提取的核心实体作为关键词，而不是完整句子。

This skill is ready for commercial/non-commercial use.

## Publisher:

[whyischen](https://clawhub.ai/user/whyischen)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use this skill to install and operate ContextBridge so an agent can search local Word, Excel, PDF, and Markdown documents by focused semantic keywords.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can give an agent persistent access to private or internal local documents, including returned snippets and file paths.

Mitigation: Add only narrow folders that are explicitly intended for agent search, and avoid home directories, shared drives, secrets, regulated data, customer data, legal, medical, or financial files.

Risk: The installed ContextBridge package and indexed document scope may be broader than intended.

Mitigation: Review before installing, use a dedicated virtual environment, and pin or verify the cbridge-agent version.

Risk: Users may not realize when the agent is searching local documents.

Mitigation: Require the agent to state when it searches local documents and summarize which scoped sources were queried.

## Reference(s):

- [ContextBridge GitHub repository](https://github.com/whyischen/context-bridge)
- [ClawHub skill page](https://clawhub.ai/whyischen/skills/local-context-bridge-cn)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration]

**Output Format:** [Markdown with inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include local document snippets and file paths returned by ContextBridge searches.]

## Skill Version(s):

1.0.2 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

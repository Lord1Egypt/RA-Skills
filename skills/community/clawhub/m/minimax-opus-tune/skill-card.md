## Description:

将 MiniMax 调教成"免费 Claude"的方法论。通过配置 SOUL.md 文件，实现智能分块输出、思考链隐藏、Claude 风格回复等高级特性。适用于希望提升 MiniMax 输出质量、减少截断、增加 Claude 风格体验的用户。

This skill is ready for commercial/non-commercial use.

## Publisher:

[howtimeschange](https://clawhub.ai/user/howtimeschange)

### License/Terms of Use:


## Use Case:

External OpenClaw users use this skill for guidance on configuring MiniMax behavior through a persistent SOUL.md profile, including chunked responses, hidden reasoning, and Claude-style response patterns.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill instructs users to overwrite a persistent OpenClaw SOUL.md configuration file, which can affect future agent behavior.

Mitigation: Back up any existing ~/.openclaw/workspace/SOUL.md file, review the inserted rules before use, and restore or delete the file if behavior changes in unwanted ways.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/howtimeschange/skills/minimax-opus-tune)
- [ClawHub publisher profile](https://clawhub.ai/user/howtimeschange)

## Skill Output:

**Output Type(s):** [Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline shell commands and configuration text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The guidance asks users to create or overwrite a persistent OpenClaw SOUL.md behavior profile.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
